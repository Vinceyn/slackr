''' COMP1531 Project 2019 message function implementations'''
from datetime import datetime
from time import mktime
from datastore import store
from .errors import AccessError
from .validate import validate_user
from .auth import auth_check_token
from .my_timer import my_timer

def message_send_later(token, channel_id, message, time_to_send):
    '''
    Checks if message is valid, then sends a mesasage at the specified time
    Note: timer assumes that the program doesn't crash before the send later date
    '''
    # Validate that user has access to channel
    validate_user(token, channel_id, "channel")

    if len(message) >= 1000:
        raise ValueError

    if time_to_send <= datetime.now():
        raise ValueError
    message_id = get_next_message_id()
    my_timer(time_to_send, message_send, [token, channel_id, message, message_id])
    return {"message_id":message_id}

def message_send(token, channel_id, message, message_id=None):
    '''
    Create a message entry in a given channel
    '''
    # Validate that user has access to channel
    validate_user(token, channel_id, "channel")

    if len(message) >= 1000:
        raise ValueError

    # Get the message_id based on stored data
    if message_id is None:
        message_id = get_next_message_id()

    # Get channel_data table entry for channel_:w
    # id, append a message entry, then update the table
    messages = get_channel_messages(channel_id)
    messages.append(new_message_entry(token, message_id, message))
    return {"message_id": message_id}

def message_remove(token, message_id):
    ''' Removes message with message_id'''
    # Validate user has access to message
    validate_user(token, message_id, "message")
    channel_id = get_channel_id_from_message_id(message_id)

    messages = get_channel_messages(channel_id)
    remove_dictionary_entry_from_list(messages, "message_id", message_id)
    update_channel_messages(channel_id, messages)

    return {}

def message_edit(token, message_id, message):
    ''' Function to edit a specific message'''
    try:
        validate_user(token, message_id, "message")
    except AccessError:
        raise AccessError
    except ValueError:
        raise ValueError

    if len(message) >= 1000:
        raise ValueError

    if message == "":
        message_remove(token, message_id)
        return {}

    channel_id = get_channel_id_from_message_id(message_id)

    messages = get_channel_messages(channel_id)
    update_dictionary_entry_in_list(messages, "message_id", message_id, "message", message)
    update_channel_messages(channel_id, messages)

    return {}

# pylint: disable=inconsistent-return-statements
def message_react(token, message_id, react_id):
    '''
    Function updates data if someone reacts to a message
    Updates a list of react_id entries containing a reacts entry,
    if an entry for the react_id does not yet exist, then an entry is created
    '''
    channel_id = get_channel_id_from_message_id(message_id)
    # Verify user is part of channel making react for, and that the react id is valid
    # (NOTE need to check what a valis react id is)
    validate_user(token, channel_id, "channel")
    validate_user(token, react_id, "react", False, channel_id, message_id)

    uid = auth_check_token(token)
    messages = get_channel_messages(channel_id)
    for message in messages:
        if message["message_id"] == message_id:
            for react in message["reacts"]:
                if react["react_id"] == react_id:
                    if uid == message["u_id"]:
                        react["is_this_user_reacted"] = True
                    add_dictionary_entry_to_list(react["u_ids"], {"u_id": uid})
                    update_channel_messages(channel_id, messages)
                    return {}
            react_entry = new_react_entry(react_id)
            if uid == message["u_id"]:
                react_entry["is_this_user_reacted"] = True
            add_dictionary_entry_to_list(react_entry["u_ids"], {"u_id": uid})
            add_dictionary_entry_to_list(message["reacts"], react_entry)
            update_channel_messages(channel_id, messages)
            return {}

def message_unreact(token, message_id, react_id):
    ''' Unreact to message with message_id and react_id'''
    channel_id = get_channel_id_from_message_id(message_id)
    validate_user(token, channel_id, "channel")
    validate_user(token, react_id, "react", True, channel_id, message_id)

    uid = auth_check_token(token)
    messages = get_channel_messages(channel_id)

    for message in messages:
        if message["message_id"] == message_id:
            for react in message["reacts"]:
                if react["react_id"] == react_id:
                    if uid == message["u_id"]:
                        react["is_this_user_reacted"] = False
                    remove_dictionary_entry_from_list(react["u_ids"], "u_id", uid)

    update_channel_messages(channel_id, messages)
    return {}

def message_pin(token, message_id):
    ''' Pin message with message id, checking if user has correct permission'''
    validate_user(token, message_id, "message")
    validate_user(token, message_id, "pin", True)

    channel_id = get_channel_id_from_message_id(message_id)

    messages = get_channel_messages(channel_id)
    update_dictionary_entry_in_list(messages, "message_id", message_id, "is_pinned", True)
    update_channel_messages(channel_id, messages)
    return {}


def message_unpin(token, message_id):
    ''' Unpin message'''
    validate_user(token, message_id, "message")
    validate_user(token, message_id, "pin")

    channel_id = get_channel_id_from_message_id(message_id)

    messages = get_channel_messages(channel_id)
    update_dictionary_entry_in_list(messages, "message_id", message_id, "is_pinned", False)
    update_channel_messages(channel_id, messages)
    return {}

########################### Helper functions ############################

def new_react_entry(react_id):
    ''' Helper function to create a new react entry'''
    return {
        "react_id": react_id,
        "u_ids": [],
        "is_this_user_reacted": False
    }

def new_message_entry(token, message_id, message):
    ''' Helper function for new message entry'''
    return {
        "message_id": message_id,
        "u_id": auth_check_token(token),
        "message": message,
        "time_created": int(mktime(datetime.now().timetuple())),
        "is_unread": False,
        "reacts": [],
        # "reacts": newReactEntry(),
        "is_pinned": False
    }

def get_next_message_id():
    ''' Helper function to get next message id to be assigned'''
    try:
        message_id = store.get("next_id", "type", "message_id")[0]["value"]
        store.update("next_id", "value", message_id + 1, "type", "message_id")
    except ValueError:
        message_id = 0
        store.insert("next_id", {"type" :  "message_id", "value" :  1})
    return message_id

def get_channel_messages(channel_id):
    ''' Helper function to get messages from channel id'''
    channel_entry = store.get("channel_data", "channel_id", channel_id)[0]
    return channel_entry["messages"]

def update_channel_messages(channel_id, messages):
    ''' Helper function to store updated messages back in channel'''
    store.update("channel_data", "messages", messages, "channel_id", channel_id)

def get_channel_id_from_message_id(message_id):
    ''' Helper function to get channel_id from message id'''
    channel_data = store.get("channel_data")
    for channel in channel_data:
        for message in channel["messages"]:
            if message["message_id"] == message_id:
                return channel["channel_id"]
    raise ValueError("Message ID doesn't exist")

def remove_dictionary_entry_from_list(dictionary_list, key, value):
    ''' Helper function to remove the a dictionary entry from list'''
    dictionary_list[:] = [x for x in dictionary_list if not x[key] == value]

def add_dictionary_entry_to_list(dictionary_list, dictionay_entry):
    ''' Helper function to add a dictionary entry to list'''
    dictionary_list.append(dictionay_entry)

def update_dictionary_entry_in_list(dictionary_list, id_key, id_value, update_key, update_value):
    ''' Helper function to update the dictionar entry in list'''
    for item in dictionary_list:
        if item[id_key] == id_value:
            item[update_key] = update_value

#########################################################
