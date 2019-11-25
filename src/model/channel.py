
from datastore import store
from .errors import AccessError
from .auth import auth_check_token

'''
This file contain the channel methods of the slackr:
    -Basic channels command: channel_create, channel_message, channel_details
    -User's command to join/leave: channel_invite, channel_join, channel_leave
    -Owner's command: channel_addowner, channel_removeowner
'''
def channel_invite(token, channel_id, u_id):
    '''
    Invite a user in the channel
    -------
    token: string
        Inviter token
    channel_id: int
        id of the channel
    u_id: int
        id of the user invited
    --------
    ValueError when:

        channel_id does not refer to a valid channel that the authorised user is part of.
        u_id does not refer to a valid user which is part of the channel
        token does not refer to a valid user

    AccessError when

        the authorised user is not already a member of the channel
    --------
    Returns {}
    '''
    type_check_token(token)
    type_check_channel_id(channel_id)
    type_check_u_id(u_id)

    check_channel_exists(channel_id)
    check_user_not_in_channel_value_error(u_id, channel_id, 'u_id is already part of the channel')
    check_user_in_channel_access_error(auth_check_token(token), channel_id,
                                       'The token is not a member of channel')

    channel_members = store.get('channel_data', 'channel_id', channel_id)[0]['members']
    new_member = create_member_from_u_id(u_id)
    channel_members.append(new_member)
    store.update('channel_data', 'members', channel_members, 'channel_id', channel_id)

    user_channels = store.get('users', 'u_id', u_id)[0]['channels']
    user_channels.append(get_channel(channel_id))
    store.update('users', 'channels', user_channels, 'u_id', u_id)

    return {}

def channel_join(token, channel_id):
    '''
    Join a channel
    -------
    token: string
        joiner token
    channel_id: int
        id of the channel
    --------
    ValueError when:

        channel_id does not refer to a valid channel that the authorised user is part of.
        token does not refer to a valid user which is not part of the channel

    AccessError whenchannel_id refers to a channel that is private
    - when the authorised user is not an admins
    --------
    Returns {}
    '''
    type_check_token(token)
    type_check_channel_id(channel_id)

    check_channel_exists(channel_id)
    req_u_id = auth_check_token(token)
    check_user_not_in_channel_value_error(req_u_id, channel_id, 'token is already in channel')

    req_permission = store.get('users', 'u_id', req_u_id)[0]['permission_id']
    channel_is_public = store.get('channel_data', 'channel_id', channel_id)[0]['is_public']
    if (not channel_is_public) and (req_permission == 3):
        raise AccessError('The user is not an admin and he tries to access a private channel')

    member = create_member_from_u_id(req_u_id)
    new_list_members = store.get('channel_data', 'channel_id', channel_id)[0]['members']
    new_list_members.append(member)
    store.update('channel_data', 'members', new_list_members, 'channel_id', channel_id)

    user_channels = store.get('users', 'u_id', req_u_id)[0]['channels']
    user_channels.append(get_channel(channel_id))
    store.update('users', 'channels', user_channels, 'u_id', req_u_id)

    return {}

def channel_leave(token, channel_id):
    '''
    Leaves a channel
    -------
    token: string
        leaver token
    channel_id: int
        id of the channel
    --------
    ValueError when:

        channel_id does not refer to a valid channel that the authorised user is part of.
        token does not refer to a valid user which is part of the channel
    --------
    Returns {}
    '''
    type_check_token(token)
    type_check_channel_id(channel_id)
    check_channel_exists(channel_id)

    req_u_id = auth_check_token(token)
    check_user_in_channel_value_error(req_u_id, channel_id, 'User is not in channel')

    if nb_of_channel_members(channel_id) == 1:
        raise ValueError('You can\'t quit a channel with 1 member')
    if nb_of_channel_owners(channel_id) == 1 and owner_in_channel(req_u_id, channel_id):
        raise ValueError('You are the only owner of the channel')

    members_before = store.get("channel_data", "channel_id", channel_id)[0].get("members")
    remove_member_from_list(req_u_id, members_before)
    store.update("channel_data", "members", members_before, "channel_id", channel_id)

    owners_before = store.get("channel_data", "channel_id", channel_id)[0].get("owners")
    try:
        remove_member_from_list(req_u_id, owners_before)
        store.update("channel_data", "owners", owners_before, "channel_id", channel_id)
    except ValueError:
        pass

    channels_before = store.get("users", "u_id", req_u_id)[0].get("channels")
    remove_channel_from_list(channel_id, channels_before)
    store.update("users", "channels", channels_before, "u_id", req_u_id)

    return {}

def channel_details(token, channel_id):
    '''
    Give the details of a channel
    -------
    token: string
        Requester token
    channel_id: int
        id of the channel
    --------
    ValueError when:

        channel_id does not refer to a valid channel that the authorised user is part of.
    AccessError when:
        token does not refer to a valid user which is part of the channel
    --------
    Returns a dictionnary containing the name of the channel and info about the users and owners
    '''
    type_check_token(token)
    type_check_channel_id(channel_id)

    check_channel_exists(channel_id)
    check_user_in_channel_access_error(auth_check_token(token), channel_id,
                                       'The requester user is not in channel')

    channel_name = store.get('channel_data', 'channel_id', channel_id)[0]['name']
    channel_owners = store.get('channel_data', 'channel_id', channel_id)[0]['owners']
    channel_members = store.get('channel_data', 'channel_id', channel_id)[0]['members']
    return {'name': channel_name,
            'owner_members': channel_owners,
            'all_members': channel_members}

def channel_messages(token, channel_id, start):
    '''
    Give a list of me    # Checking for a valid channel_id.
    ssages of a channel, starting from an index
    -------
    token: string
        Requester token
    channel_id: int
        id of the channel
    start: int
        starting index of the channel
    --------
    ValueError when:

        channel_id does not refer to a valid channel that the authorised user is part of.
        token does not refer to a valid user
        start is either greater or equal to total number of messages in the channel, or is negative

    AccessError when:
        Authorised user is not a member of channel with channel_id
    --------
    Returns - start and end index (-1 if it reached the end)
            - and all of the messages between the 2 index
    '''
    type_check_token(token)
    type_check_channel_id(channel_id)
    if not isinstance(start, int):
        raise ValueError('start is not an int')

    check_channel_exists(channel_id)
    check_user_in_channel_access_error(auth_check_token(token), channel_id,
                                       'requester is not a member of the channel')

    messages = store.get('channel_data', 'channel_id', channel_id)[0]['messages']
    if (start < 0 or start > len(messages)):
        raise ValueError('Start index is not correctly indexed')

    start_index = - (start + 1)
    end_return = -1
    returned_messages = []
    if start + 50 <= len(messages):
        end_return = start + 49
        returned_messages = messages[start_index: - (start + 51):-1]
    else:
        returned_messages = messages[start_index::-1]

    return {
        'messages': returned_messages,
        'start' : start,
        'end': end_return
    }

def channel_addowner(token, channel_id, u_id):
    '''
    Change a user into an owner in the channel
    -------
    token: string
        Changer token
    channel_id: int
        id of the channel
    u_id: int
        id of the user who will become owner
    --------
    ValueError when:

        channel_id does not refer to a valid channel that the authorised user is part of.
        u_id does not refer to a valid user which is part of the channel
        u_id is already an owner of the channel
        token does not refer to a valid user

    AccessError when

        the authorised user is not already a member of the channel
    --------
    Returns {}
    '''
    type_check_token(token)
    type_check_channel_id(channel_id)
    type_check_u_id(u_id)

    check_channel_exists(channel_id)
    if owner_in_channel(u_id, channel_id):
        raise ValueError('The user with ID u_id is already an owner of the channel')

    requester_u_id = auth_check_token(token)
    req_perm = store.get('users', 'u_id', requester_u_id)[0]['permission_id']
    if req_perm == 3 and not user_in_channel(requester_u_id, channel_id):
        ValueError('Requester is not part of the channel, and is a normal user in the slackr')
    if req_perm == 3 and not owner_in_channel(requester_u_id, channel_id):
        raise AccessError('Requester has not the right to add an owner')

    channel_owners = store.get('channel_data', 'channel_id', channel_id)[0]['owners']
    channel_owners.append(create_member_from_u_id(u_id))
    store.update('channel_data', 'owners', channel_owners, 'channel_id', channel_id)

    return {}

def channel_removeowner(token, channel_id, u_id):
    '''
    Change an owner into an user in the channel
    -------
    token: string
        Changer token
    channel_id: int
        id of the channel
    u_id: int
        id of the owner who will become user
    --------
    ValueError when:

        channel_id does not refer to a valid channel that the authorised user is part of.
        u_id does not refer to a valid user which is part of the channel
        u_id is already an owner of the channel
        token does not refer to a valid user

    AccessError when:
        the authorised user is not an owner of the slackr, or an owner of this channel
    --------
    Returns {}
    '''
    type_check_token(token)
    type_check_channel_id(channel_id)
    type_check_u_id(u_id)

    check_channel_exists(channel_id)
    if not owner_in_channel(u_id, channel_id):
        raise ValueError('The user with ID u_id is not an owner of the channel')

    requester_u_id = auth_check_token(token)
    req_perm = store.get('users', 'u_id', requester_u_id)[0]['permission_id']

    if req_perm == 3 and not user_in_channel(requester_u_id, channel_id):
        raise ValueError('The requester is not part of the channel and is also not an admin/owner')
    if req_perm == 3 and not owner_in_channel(requester_u_id, channel_id):
        raise AccessError('Requester has not the right to add an owner')
    if nb_of_channel_owners(channel_id) == 1:
        raise ValueError('The requested u_id is the only owner of the channel')

    channel_owners = store.get('channel_data', 'channel_id', channel_id)[0]['owners']
    remove_member_from_list(u_id, channel_owners)
    store.update('channel_data', 'owners', channel_owners, 'channel_id', channel_id)

    return {}

def channels_list(token):
    '''
    Given a token, list all the channel the token is part of
    --------
    token: string
        token of the requester
    --------
    ValueError when:
        The token doesn't refer to a proper user
    --------
        return: list of all the channels the token is part of
    '''
    type_check_token(token)
    return {"channels": store.get("users", "u_id", auth_check_token(token))[0]["channels"]}

def channels_listall(token):
    '''
    Given a token, list all the channel
    --------
    token: string
        token of the requester
    --------
    ValueError when:
        The token doesn't refer to a proper user
    --------
        return: list of all the channels
    '''
    type_check_token(token)
    if store.n_elems('channel_data') == 0:
        return {'channels': []}
    return {'channels': store.get('channels')}

def channels_create(token, name, is_public):
    '''
    Create a new channel
    --------
    token: string
        token of the requester
    name: string
        name of the channel
    is_public: bool
        boolean indicating if the channel will be public or private
    \u207b-------
    ValueError when:
        name is more than 20 characters long
    --------
    return: channel_id
    '''
    type_check_token(token)
    if not isinstance(name, str):
        raise ValueError('Name is not a string')
    if not isinstance(is_public, bool):
        raise ValueError('is_public is not a boolean')
    if not isinstance(name, str):
        raise ValueError('Name is not a string')
    if len(name) > 20:
        raise ValueError('Name is more than 20 characters long')
    if len(name) <= 0:
        raise ValueError('Name is invalid')

    channel_id = store.n_elems('channel_data') + 1
    u_id = auth_check_token(token)
    member = create_member_from_u_id(u_id)
    store.insert('channel_data', {
        'channel_id': channel_id,
        'name': name,
        'messages': [],
        'members': [member],
        'owners': [member],
        'is_public': is_public
    })

    store.insert('channels', {
        'channel_id': channel_id,
        'name' : name
    })

    channels = store.get('users', 'u_id', u_id)[0]['channels']
    channels.append({
        'channel_id': channel_id,
        'name' : name
    })
    store.update('users', 'channels', channels, 'u_id', u_id)

    return {'channel_id': channel_id}

######### UTILITY FUNCTIONS #########

def remove_member_from_list(u_id, l_ist):
    '''
    This function removes a single member from a list.
    '''
    for index, count in enumerate(l_ist):
        if count.get("u_id") == u_id:
            del l_ist[index]
            return

    raise ValueError("member does not exist in list")

# Remove a single channel from a list.
def remove_channel_from_list(c_id, l_ist):
    '''
    This function remove a single channel from a list.
    '''
    for index, count in enumerate(l_ist):
        if count.get("channel_id") == c_id:
            del l_ist[index]
            return


def create_member_from_u_id(u_id):
    '''
    Given a u_id, this function returns it under the 'member' form.
    '''
    member = {
        'u_id' : u_id,
        'name_first' : store.get('users', 'u_id', u_id)[0]['name_first'],
        'name_last' : store.get('users', 'u_id', u_id)[0]['name_last']
    }
    return member


def channel_exist(channel_id):
    '''
    This function finds if the channel_id exists or not.
    '''
    channel_list = store.get('channel_data')
    channel_exist_bool = False
    for channel in channel_list:
        if channel_id == channel['channel_id']:
            channel_exist_bool = True
    return channel_exist_bool

def user_in_channel(u_id, channel_id):
    '''
    This functions finds if the user is in the channel or not.
    '''
    members = store.get('channel_data', 'channel_id', channel_id)[0]['members']
    is_in_channel = False
    for member in members:
        if u_id == member['u_id']:
            is_in_channel = True
    return is_in_channel

def check_user_not_in_channel_value_error(u_id, channel_id, message_error):
    '''
    This function checks if the user is in the channel. If he is, raise ValueError.
    '''
    if user_in_channel(u_id, channel_id):
        raise ValueError(str(message_error))

def check_user_in_channel_value_error(u_id, channel_id, message_error):
    '''
    This function checks if the user is in the channel. If not, raise ValueError.
    '''
    if not user_in_channel(u_id, channel_id):
        raise ValueError(str(message_error))

def check_user_in_channel_access_error(u_id, channel_id, message_error):
    '''
    This function checks if the user is in the channel. If not, raise AccessError.
    '''
    if not user_in_channel(u_id, channel_id):
        raise AccessError(str(message_error))

def owner_in_channel(u_id, channel_id):
    '''
    This function finds if the u_id is an owner of the channel or not.
    '''
    members = store.get('channel_data', 'channel_id', channel_id)[0]['owners']
    is_in_channel = False
    for member in members:
        if u_id == member['u_id']:
            is_in_channel = True
    return is_in_channel

def type_check_token(token):
    '''
    This function type checks token.
    '''
    if not isinstance(token, str):
        raise ValueError('token is not a string')

def type_check_channel_id(channel_id):
    '''
    This function type checks channel_id.
    '''
    if not isinstance(channel_id, int):
        raise ValueError('channel_id is not an int')

def type_check_u_id(u_id):
    '''
    This function type checks u_id.
    '''
    if not isinstance(u_id, int):
        raise ValueError('u_id is not an int')

def check_channel_exists(channel_id):
    '''
    This function checks if a channel_id exists or not. If not, it raises a valueError.
    '''
    if not channel_exist(channel_id):
        raise ValueError('channel_id doesnt exist')

def get_channel(channel_id):
    '''
    This function gets channel storage value from channel_id.
    '''
    return {
        'channel_id' : channel_id,
        'name' : store.get('channel_data', 'channel_id', channel_id)[0]['name']
    }

def nb_of_channel_members(channel_id):
    '''
    This function gets all the members of a channel.
    '''
    return len(store.get('channel_data', 'channel_id', channel_id)[0]['members'])

def nb_of_channel_owners(channel_id):
    '''
    This function gets all the owners of a channel.
    '''
    return len(store.get('channel_data', 'channel_id', channel_id)[0]['owners'])
