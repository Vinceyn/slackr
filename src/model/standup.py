''' COMP1531 Project standup functions'''
from datetime import datetime, timedelta
from time import mktime
from datastore import store
from .errors import AccessError
from .validate import validate_user
from .my_timer import my_timer
from .message import message_send
from .auth import auth_check_token

def standup_start(token, channel_id, standup_length=15*60):
    ''' Begin standup in channel, calls end standup after the time has expired'''
    validate_user(token, channel_id, "channel")
    except_message = "Already currently active standup"
    try:
        standup_data = store.get("standup", "channel_id", channel_id)[0]
        if standup_data["is_active"]:
            raise ValueError(except_message)
        store.update("standup", "is_active", True, "channel_id", channel_id)
        new_message_index = standup_data["standup_id"]
        store.update("standup", "standup_id", new_message_index+1, "channel_id", channel_id)
        summaries = standup_data["summaries"]
        summaries.append("Standup summary:\n")
        store.update("standup", "summaries", summaries, "channel_id", channel_id)
    except (ValueError) as ex:
        if ex.args[0] == except_message:
            raise ValueError(ex)
        store.insert("standup", {"channel_id": channel_id, "is_active": True,\
            "standup_id": 0, "summaries": ["Standup summary:\n"]})
    end = datetime.now()+timedelta(seconds=standup_length)
    my_timer(end, standup_end, (token, channel_id))
    store.update("standup", "end", end, "channel_id", channel_id)
    return {"time_finish" : convert_time(end)}

def standup_active(token, channel_id):
    ''' Returns if there is an active standup in the channel'''
    validate_user(token, channel_id, "channel")
    active = False
    end_time = None
    try:
        standup_data = store.get("standup", "channel_id", channel_id)[0]
        if standup_data["is_active"]:
            active = True
            end_time = standup_data["end"]
    # pylint: disable=broad-except
    except Exception:
        pass
    return {"is_active":active, "time_finish":convert_time(end_time)}

def standup_send(token, channel_id, message):
    ''' Sends a standup message and a normal message'''
    message_send(token, channel_id, message)
    standup_data = store.get("standup", "channel_id", channel_id)[0]
    if not standup_data["is_active"]:
        raise AccessError
    summaries = standup_data["summaries"]
    summaries[standup_data["standup_id"]] += get_name_from_token(token) + ' - ' + message + '\n'
    store.update("standup", "summaries", summaries, "channel_id", channel_id)
    return {}

def standup_end(token, channel_id):
    ''' Prints executive summary as a message and closes standup'''
    standup_data = store.get("standup", "channel_id", channel_id)[0]
    standup_data["is_active"] = False
    index = standup_data["standup_id"]
    summary = standup_data["summaries"][index]
    print(f"Summary: {summary}")
    if summary != "Standup summary:\n":
        message_send(token, channel_id, summary)

def get_name_from_token(token):
    ''' Returns the name of the user from token'''
    uid = auth_check_token(token)
    user = store.get("users", "u_id", uid)[0]
    return user["name_first"]

def convert_time(time_to_convert):
    ''' Conversts datetime to unix time'''
    if time_to_convert is None:
        return None
    return mktime(time_to_convert.timetuple())
