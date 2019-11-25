import pytest
from datetime import datetime, timedelta
import time as timeSleep

from ..standup import *
from ..auth import *
from ..channel import *
from ..errors import AccessError
from datastore import store


def supply_token():
    # SETUP BEGIN
    authRegisterDict = auth_register("hayden@gmail.com", "passwstandup_length", "Hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]

    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]
    # SETUP END

    return (token1, token2, id_1, id_2)

def supply_channel(function=supply_token):
    #Return a Tuple (channel_id, token1, token2, id_1, id_2), when token1 is the owner of the channel
    name = "Channel_1"
    supplyToken = function()
    channelCreated = channels_create(supplyToken[0], name, True)["channel_id"]
    return (channelCreated, supplyToken[0], supplyToken[1], supplyToken[2], supplyToken[3])

##### Test for checking if the standup works correctly

def test_standup_default():
    # Testing that at the end of a standup, a nicely formated message is returned
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()

    messages = ["Hi", "Hello", "What's up?", "Not much", "Cool, nice standup, bye"]
    usernames = [getNameFromToken(token1), getNameFromToken(token2)]
    tokens = [token1, token2]
    # This is what the result of the standup should look like:
    standup = "Standup summary:\n"
    for i in range(len(messages)-1):
        standup += usernames[i%2] + ' - ' + messages[i] + '\n'
    standup += usernames[(len(messages)-1)%2] + ' - ' + messages[-1]+'\n'

    channel_join(token2, channel_id)
    standup_active(token1, channel_id)
    standup_start(token1, channel_id, 0.01)

    for i in range(len(messages)):
        standup_send(tokens[i%2], channel_id, messages[i])
    standup_active(token1, channel_id)

    timeSleep.sleep(0.02)
    standupSummaryDict = channel_messages(token1, channel_id, 0)["messages"]
    result = standupSummaryDict[0]["message"]
    assert(result == standup)
    standup_active(token1, channel_id)

    messages = ["Well there bob", "what did you do?", "Nothing", "Haha", "Nice standup, bye"]
    usernames = [getNameFromToken(token1), getNameFromToken(token2)]
    tokens = [token1, token2]
    # This is what the result of the standup should look like:
    standup = "Standup summary:\n"
    for i in range(len(messages)-1):
        standup += usernames[i%2] + ' - ' + messages[i] + '\n'
    standup += usernames[(len(messages)-1)%2] + ' - ' + messages[-1]+'\n'

    standup_start(token1, channel_id, 0.01)

    for i in range(len(messages)):
        standup_send(tokens[i%2], channel_id, messages[i])
        
    timeSleep.sleep(0.02)
    standupSummaryDict = channel_messages(token1, channel_id, 0)["messages"]
    result = standupSummaryDict[0]["message"]
    assert(result == standup)

# @pytest.mark.skip
def test_standup_no_messages():
    # Checks that the number of messages before and after the standup are the
    # same if no standup messages are sent (i.e, no standup summary was made)
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()

    numInit = getNumMessages(token1, channel_id)
    standup_start(token1, channel_id, 0.01)
    timeSleep.sleep(0.02)
    assert(getNumMessages(token1, channel_id) == numInit)

##### Tests for standup_start #####

# @pytest.mark.skip
def test_standup_start_test_correct_stop_time():
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    length = 0.01
    endmin = datetime.now() + timedelta(seconds=length)
    ret = standup_start(token1,channel_id, length)["time_finish"]
    endmax = datetime.now() + timedelta(seconds=length)
    assert(ret <= convert_time(endmax) and ret >= convert_time(endmin))

# @pytest.mark.skip
def test_standup_start_AccessError_2():
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    with pytest.raises(AccessError):
        standup_start(token2, channel_id)
    standup_start(token1, channel_id, 0.015)
    with pytest.raises(ValueError):
        standup_start(token1, channel_id, 0.01)
    timeSleep.sleep(0.02)

# @pytest.mark.skip
def test_standup_start_AccessError():
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    channel_id += 1 # This should not be a valid channel
    with pytest.raises(AccessError):
        standup_start(token1, channel_id)

##### Tests for standup_send #####

# @pytest.mark.skip
def test_standup_send_invalidType():
    # Should return any exception
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    message = 1
    with pytest.raises(Exception):
        standup_send(token1, channel_id, message)

def test_standup_send_ValueError_1():
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    channel_id += 1
    message = "Hi there"
    with pytest.raises(AccessError):
        standup_send(token1, channel_id, message)

# @pytest.mark.skip
def test_standup_send_ValueError_2():
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    longMessage = "Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:"
    standup_start(token1, channel_id, 0.01)
    with pytest.raises(ValueError):
        standup_send(token1, channel_id, longMessage)
    timeSleep.sleep(0.02)

# @pytest.mark.skip
def test_standup_send_AccessError_1():
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    message = "Hi there"
    with pytest.raises(AccessError):
        standup_send(token2, channel_id, message)

# @pytest.mark.skip
def test_standup_send_AccessError_2():
    # Not currently sure about the data structure will be setup yet, however
    # this function will need to disable a standup active flag or change the
    # time the standup began before it tests if it can post a message
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    message = "Hi there"
    standup_start(token1, channel_id, 0.01)
    timeSleep.sleep(0.02)
    with pytest.raises(AccessError):
        standup_send(token1, channel_id, message)

def getNameFromToken(token):
    uid = auth_check_token(token)
    user = store.get("users", "u_id", uid)[0]
    return user["name_first"]

def getNumMessages(token, channel_id):
    channelMessages = store.get("channel_data", "channel_id", channel_id)[0]["messages"]
    if channelMessages == None:
        return 0
    return len(channelMessages)