'''
validates that the user has access permissions for the type and id being requested
token: users token
update_id: channel_id, message_id, react_id
type: "channel", "message", "react", "pin"

Errors:
    - AccessError: user doesn't have access permissions
    - ValueError: Entry doesn't exist
'''
from datastore import store
from .errors import AccessError
from .auth import auth_check_token

# pylint: disable=too-many-arguments, too-many-return-statements, too-many-nested-blocks, too-many-branches
def validate_user(token, update_id, input_type: str, pin=False, \
    react_channel_id="tmp", react_message_id="tmp"):
    ''' Function determined if the user has sufficient permissions to perform
    functionality specified in arguments'''
    u_id = auth_check_token(token)
    if input_type == "channel":
        user_data = store.get("users", "u_id", u_id)[0]
        for channel in user_data["channels"]:
            if channel["channel_id"] == update_id:
                return
        raise AccessError("User is not part of channel or channel does not exist")
    if input_type == "message":
        message_data = get_message_data_from_m_id(update_id)
        if u_id == message_data["u_id"]:
            return
        channel_data = get_channel_data_from_m_id(update_id)
        for owner in channel_data["owners"]:
            if owner["u_id"] == u_id:
                return
        if is_admin(token):
            return
        raise AccessError("User doesn't have permission to alter message")
    if input_type == "react":
        # Not sure the values a react id should have hence jsut return
        message_data = store.get("channel_data", "channel_id", react_channel_id)[0]["messages"]
        for message in message_data:
            if message["message_id"] == react_message_id:
                for react in message["reacts"]:
                    for uid in react["u_ids"]:
                        if uid["u_id"] == u_id:
                            if pin:
                                return
                            raise ValueError("User already reacted")
        if pin:
            raise ValueError
        return
    if input_type == "pin":
        message = get_message_data_from_m_id(update_id)
        if not is_admin(token):
            raise ValueError("User not admin, must be admin to pin")
        if message["is_pinned"] and pin:
            raise ValueError("Message already pinned")
        if not message["is_pinned"] and not pin:
            raise ValueError("Message is not pinned")
        return
    raise ValueError("Incorrect type to validate: use 'channel', 'message' or 'react'")

def is_admin(token):
    ''' Returns if user is admin'''
    uid = auth_check_token(token)
    return store.get("users", "u_id", uid)[0]["permission_id"] == 1

####### Helper functions #######
def get_message_data_from_m_id(message_id):
    ''' Helper function to get message data from message_id'''
    channel_data = store.get("channel_data")
    for channel in channel_data:
        for message in channel["messages"]:
            if message["message_id"] == message_id:
                return message
    raise ValueError("message id doesn't exist")

def get_channel_data_from_m_id(message_id):
    ''' Helper function to get channel data from channel_id'''
    channel_data = store.get("channel_data")
    for channel in channel_data:
        for message in channel["messages"]:
            if message["message_id"] == message_id:
                return channel
    raise ValueError("Message id doesn't exist")
