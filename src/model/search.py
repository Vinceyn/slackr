"""
Given a query string, return all messages matching the query string from all the user's channel.
"""
from datastore import store
from .auth import auth_check_token
from .channel import channels_list
# ------
# token: str
#     token of the requester
# query_str: str
#     str searched by the requester
# ------
# returns: all of the messages that contains the query_str as substring
#
def search(token, query_str):
    """
    The function searches for all the messages matching the query_str in all the user's channels
    and returns them.
    """
    check_arguments(token, query_str)
    
    channel_list = channels_list(token)['channels']    
    channel_id_belongs = [d['channel_id'] for d in channel_list]

    all_messages = []
    for channel_id in channel_id_belongs:
        one_channel_messages = store.get('channel_data', 'channel_id', channel_id)[0]['messages']
        all_messages.append(one_channel_messages)

    messages_output = []

    for messages_in_list in all_messages:
        for message in messages_in_list:
            if query_str.lower() in message['message'].lower():
                messages_output.append(message)

    return {"messages": messages_output}

def check_arguments(token, query_str):
    """
    Following function checks if the arguments are of correct type or not.
    """
    if not isinstance(token, str):
        raise ValueError('token is not a string')
    if not isinstance(query_str, str):
        raise ValueError('query_str is not a string')
