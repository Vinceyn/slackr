import pytest
from time import sleep
from datetime import datetime, timedelta

from ..message import *
from ..auth import *
from ..channel import *
from ..errors import AccessError
from ..validate import *


def supply_token():

    # SETUP BEGIN
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]

    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]
    # SETUP END

    return (token1, token2, id_1, id_2)

def supply_token2():

    # SETUP BEGIN
    authRegisterDict = auth_register("hn@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]

    authRegisterDict2 = auth_register("ncholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
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

#### message_send_later() test funcitons

# @pytest.mark.skip
# @pytest.mark.simple
def test_message_send_later_simple():
    # Testing whether the message sent is not added initially, but then is added
    # one second later using the message validate function
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()

    message = "Hi there"
    time = datetime.now() + timedelta(seconds=0.01)
    numInit = getNumMessages(token1, channel_id)
    message_send_later(token1, channel_id, message, time)
    assert(getNumMessages(token1, channel_id) == numInit)
    # Uncomment line for actual testing
    sleep(0.02)
    assert(getNumMessages(token1, channel_id) == numInit + 1)
    assert(validMessage(1, message, channel_id, token1))

# @pytest.mark.simple
# @pytest.mark.skip
def test_message_send_later_simple_2():
    # Testing what happens when multiple messages are sent supposed to arrive at
    # the same time

    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    message = "Hi there"
    message2 = "Hi"
    # print(store.get('channel_data'))
    # channelMessages = store.get("channel_data", "channel_id", channel_id)[0]["messages"]
    # print(channelMessages)
    numInit = getNumMessages(token1, channel_id)
    time = datetime.now() + timedelta(seconds=0.01)
    message_send_later(token1, channel_id, message, time)
    sleep(0.02)
    time = datetime.now() + timedelta(seconds=0.01)
    message_send_later(token1, channel_id, message2, time)
    assert(getNumMessages(token1, channel_id) == numInit+1)
    # Uncomment line for actual testing
    sleep(0.02)
    channelMessages = store.get("channel_data", "channel_id", channel_id)[0]["messages"]
    print(channelMessages)
    assert(getNumMessages(token1, channel_id) == numInit + 2)
    assert(validMessage(1, message, channel_id, token1))
    assert(validMessage(2, message2, channel_id, token1))

# @pytest.mark.value
# @pytest.mark.skip
def test_message_send_later_ValueError_1():
    # Testing invalid channel ID
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    channel_id += 1
    message = "Hi there"
    time = datetime.now() + timedelta(seconds=1)
    with pytest.raises(AccessError):
        message_send_later(token1, channel_id, message, time)

# @pytest.mark.value
# @pytest.mark.skip
def test_message_send_later_ValueError_2():
    # Testing message greater than 1000 characters
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    longMessage = "Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:"
    time = datetime.now() + timedelta(seconds=1)
    with pytest.raises(ValueError):
        message_send_later(token1, channel_id, longMessage, time)

# @pytest.mark.value
# @pytest.mark.skip
def test_message_send_later_ValueError_3():
    # Testing time in the past
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    message = "Hi there"
    time = datetime.now() - timedelta(minutes=30)
    with pytest.raises(ValueError):
        message_send_later(token1, channel_id, message, time)

# @pytest.mark.value
# @pytest.mark.skip
def test_message_send_later_ValueError_4():
    # Testing time now
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    longMessage = "Hi there"
    time = datetime.now()
    with pytest.raises(ValueError):
        message_send_later(token1, channel_id, longMessage, time)

# @pytest.mark.access
# @pytest.mark.skip
def test_message_send_later_AccessError():
    # Testing user not a member of the channel
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    message = "Hi there"
    time = datetime.now() + timedelta(minutes=30)
    with pytest.raises(AccessError):
        message_send_later(token2, channel_id, message, time)

#### message_send() test funciton

# @pytest.mark.simple
# @pytest.mark.skip
def test_message_send_simple_1():
    # Testing normal implementation of message when posting 1, 2 and 3 messages
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()

    message = "Hi there"
    message2 = "Yup"
    message3 = "Yello"
    numInit = getNumMessages(token1, channel_id)
    message_send(token1, channel_id, message)
    assert(getNumMessages(token1, channel_id) == numInit + 1)
    assert(validMessage(1, message, channel_id, token1))
    message_send(token1, channel_id, message2)
    message_send(token1, channel_id, message3)
    channelMessages = store.get("channel_data", "channel_id", channel_id)[0]["messages"]
    print(channelMessages)
    assert(validMessage(1, message, channel_id, token1))
    assert(validMessage(2, message2, channel_id, token1))
    assert(validMessage(3, message3, channel_id, token1))


# @pytest.mark.value
# @pytest.mark.skip
def test_message_send_AccessError_1():
    # Testing invalid channel_id
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    channel_id += 1
    message = "Hi there"
    with pytest.raises(AccessError):
        message_send(token1, channel_id, message)

# @pytest.mark.value
# @pytest.mark.skip
def test_message_send_ValueError_2():
    # Testing message with more than 1000 characters
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    longMessage = "Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:"
    with pytest.raises(ValueError):
        message_send(token1, channel_id, longMessage)

# @pytest.mark.access
# @pytest.mark.skip
def test_message_send_AccessError():
    # Testing when user is not a member of group
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    message = "Hi there"
    with pytest.raises(AccessError):
        message_send(token2, channel_id, message)

#### message_remove() test funcitons

# @pytest.mark.skip
def test_message_remove_simple_1():
    # Owner removing owners message, when there are two messages and when there
    # is only one message
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    message1 = "Hi there"
    message2 = "Oh hi"
    numInit = getNumMessages(token1, channel_id)
    message_send(token1, channel_id, message1)
    message_send(token1, channel_id, message2)
    channelMessages = channel_messages(token1, channel_id, 0)["messages"]
    print(channelMessages)
    # print(store.get("channel_data", "channel_id", channel_id)[0]["messages"])
    message_id_1 = channelMessages[1]["message_id"]
    message_id_2 = channelMessages[0]["message_id"]
    message_remove(token1, message_id_1)
    assert(validMessage(1, message2, channel_id, token1))
    message_remove(token1, message_id_2)
    assert(getNumMessages(token1, channel_id) == numInit)

# @pytest.mark.skip
def test_message_remove_user():
    # Same test as above except user (not owner) removing users message
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    channel_join(token2, channel_id)
    message1 = "Hi there"
    message2 = "Oh hi"
    numInit = getNumMessages(token1, channel_id)
    message_send(token2, channel_id, message1)
    message_send(token2, channel_id, message2)
    channelMessages = channel_messages(token2, channel_id, 0)["messages"]
    message_id_1 = channelMessages[1]["message_id"]
    message_id_2 = channelMessages[0]["message_id"]
    message_remove(token2, message_id_1)
    assert(validMessage(1, message2, channel_id, token1))
    message_remove(token2, message_id_2)
    assert(getNumMessages(token1, channel_id) == numInit)

# @pytest.mark.skip
def test_message_remove_owner_user():
    # Owner rmoving users message
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    channel_join(token2, channel_id)
    message1 = "Hi there"
    message2 = "Oh hi"
    numInit = getNumMessages(token1, channel_id)
    message_send(token2, channel_id, message1)
    message_send(token2, channel_id, message2)
    channelMessages = channel_messages(token2, channel_id, 0)["messages"]
    message_id_1 = channelMessages[1]["message_id"]
    message_id_2 = channelMessages[0]["message_id"]
    message_remove(token1, message_id_1)
    assert(validMessage(1, message2, channel_id, token1))
    message_remove(token1, message_id_2)
    assert(getNumMessages(token1, channel_id) == numInit)

# @pytest.mark.skip
def test_message_remove_ValueError():
    # Testing the removal of a message which no longer exists
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()

    message = "G'day mate"
    message_send(token1, channel_id, message)
    channelMessages = channel_messages(token1, channel_id, 0)["messages"]
    message_id = channelMessages[0]["message_id"]
    message_remove(token1, message_id)
    with pytest.raises(ValueError):
        message_remove(token1, message_id)

# @pytest.mark.skip
def test_message_remove_AccessError_1():
    # Testing user trying to remove owner message
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    channel_join(token2, channel_id)

    message = "G'day mate"
    message_send(token1, channel_id, message)
    channelMessages = channel_messages(token1, channel_id, 0)["messages"]
    message_id = channelMessages[0]["message_id"]
    with pytest.raises(AccessError):
        message_remove(token2, message_id)

# @pytest.mark.skip
def test_message_remove_AccessError():
    # Testing user trying to remove another user message
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    (channel_id2, token3, token4, id_3, id_4) = supply_channel(supply_token2)
    channel_join(token2, channel_id)
    channel_join(token3, channel_id)

    message = "G'day mate"
    message_send(token2, channel_id, message)
    channelMessages = channel_messages(token1, channel_id, 0)["messages"]
    message_id = channelMessages[0]["message_id"]
    with pytest.raises(AccessError):
        message_remove(token3, message_id)

#### message_edit() test funcitons

# @pytest.mark.skip
# @pytest.mark.simple
def test_message_edit_simple_1():
    # Owner editing owner message
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    message1 = "Hi there"
    message2 = "Oh hi"
    numInit = getNumMessages(token1, channel_id)
    message_send(token1, channel_id, message1)
    channelMessages = channel_messages(token1, channel_id, 0)["messages"]
    message_id = channelMessages[0]["message_id"]
    message_edit(token1, message_id, message2)
    assert(validMessage(1, message2, channel_id, token1))
    message_edit(token1, message_id, "")
    with pytest.raises(ValueError):
        get_channel_data_from_m_id(2)
    with pytest.raises(ValueError):
        validate_user(token1, channel_id, "random")

# @pytest.mark.simple
# @pytest.mark.skip
def test_message_edit_simple_2():
    # Owner editing user message
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    message1 = "Hi there"
    message2 = "Oh hi"
    numInit = getNumMessages(token1, channel_id)
    channel_join(token2, channel_id)
    message_send(token2, channel_id, message1)
    channelMessages = channel_messages(token1, channel_id, 0)["messages"]
    message_id = channelMessages[0]["message_id"]
    message_edit(token1, message_id, message2)
    assert(validMessage(1, message2, channel_id, token1))

# @pytest.mark.simple
# @pytest.mark.skip
def test_message_edit_simple_3():
    # User editing user message
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    message1 = "Hi there"
    message2 = "Oh hi"
    numInit = getNumMessages(token1, channel_id)
    channel_join(token2, channel_id)
    message_send(token2, channel_id, message1)
    channelMessages = channel_messages(token1, channel_id, 0)["messages"]
    message_id = channelMessages[0]["message_id"]
    message_edit(token2, message_id, message2)
    assert(validMessage(1, message2, channel_id, token1))

# @pytest.mark.skip
def test_message_edit_ValueError():
    # Testing the removal of a function which no longer exists
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()

    message = "G'day mate"
    message2 = "Hi there buddy"
    message_send(token1, channel_id, message)
    channelMessages = channel_messages(token1, channel_id, 0)["messages"]
    message_id = channelMessages[0]["message_id"]
    message_remove(token1, message_id)
    with pytest.raises(ValueError):
        message_edit(token1, message_id, message2)

def test_message_edit_ValueError_2():
    # Testing the removal of a function which no longer exists
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    longMessage = "Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:  Just writing a random string that needs to be longer than one thousand characters now I will copy and paste this line so that I can get heaps of characters more easily:"
    message = "Hi there"
    message_id = message_send(token1, channel_id, message)["message_id"]
    with pytest.raises(ValueError):
        message_edit(token1, message_id, longMessage)

# @pytest.mark.skip
def test_message_edit_AccessError_1():
    # Testing user trying to edit owner message
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    channel_join(token2, channel_id)

    message = "G'day mate"
    message2 = "Hi there buddy"
    message_send(token1, channel_id, message)
    channelMessages = channel_messages(token1, channel_id, 0)["messages"]
    message_id = channelMessages[0]["message_id"]
    with pytest.raises(AccessError):
        message_edit(token2, message_id, message2)

# @pytest.mark.skip
def test_message_edit_AccessError_2():
    # Testing user trying to edit another user message
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    (channel_id2, token3, token4, id_3, id_4) = supply_channel(supply_token2)
    channel_join(token2, channel_id)
    channel_join(token3, channel_id)

    message = "G'day mate"
    message2 = "Hi there buddy"
    message_send(token2, channel_id, message)
    channelMessages = channel_messages(token1, channel_id, 0)["messages"]
    message_id = channelMessages[0]["message_id"]
    with pytest.raises(AccessError):
        message_edit(token3, message_id, message2)
    m_id_2 = message_send(token3, channel_id2, "Hi")["message_id"]
    message_remove(token1, m_id_2)

"""
Tests for message_react behaviour
"""
# @pytest.mark.skip
def test_message_react():
    ### Setup
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    channel_join(token2, channel_id)

    message_id = message_send(token1, channel_id, "React if you're cool")["message_id"]

    ### Functionality test
    reaction1 = 10
    reaction2 = 4
    message_react(token2, message_id, reaction1)
    message_react(token1, message_id, reaction1)
    ### Testing multiple people reacting with same reaction

    message_unreact(token2, message_id, reaction1)
    message_react(token2, message_id, reaction2)

    message_unreact(token2, message_id, reaction2)
    message_react(token2, message_id, reaction1)
    messageData = store.get("channel_data", "channel_id", channel_id)[0]["messages"]
    assert(len(messageData[0]["reacts"]) == 2)

    ### Testing invalid IDs
    with pytest.raises(ValueError):
        message_react(token2, 345765443256, reaction1)
        message_react(token2, message_id, 2436354645674576456874)

    ### Testing pre-existing reactions
    with pytest.raises(ValueError):
        message_react(token2, message_id, reaction1)

    with pytest.raises(ValueError):
        message_react(token1, message_id, reaction2)

    with pytest.raises(ValueError):
        message_react(token2, message_id, reaction1)

    ### Testing user trying to react twice
    with pytest.raises(ValueError):
        message_react(token2, message_id, reaction1)

    ### Testing message ID in unjoined channel
    channel_leave(token2, channel_id)
    with pytest.raises(AccessError):
        message_react(token2, message_id, 12)
    
    

def test_message_react_2():
    ### Setup
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    channel_join(token2, channel_id)

    message_send(token1, channel_id, "React if you're cool")
    message_id = channel_messages(token1, channel_id, 0)['messages'][0]["message_id"]

    ### Functionality test
    reaction1 = 10
    reaction2 = 4

    ### Testing multiple reacts and user reacting
    message_react(token1, message_id, reaction1)
    message_react(token2, message_id, reaction1)
    with pytest.raises(ValueError):
        message_react(token2, message_id, reaction1)


"""
Tests for message_unreact behaviour
"""
# @pytest.mark.skip
def test_message_unreact():
    ### Setup
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    channel_join(token2, channel_id)
    print(store.get("users"))
    message_send(token1, channel_id, "React if you're cool")
    message_id = channel_messages(token1, channel_id, 0)['messages'][0]["message_id"]

    reaction1 = 10
    reaction2 = 4
    message_react(token2, message_id, reaction1)
    message_react(token1, message_id, reaction2)

    ### Functionality tests
    assert(message_unreact(token2, message_id, reaction1) == {})
    assert(message_unreact(token1, message_id, reaction2) == {})

    ### Testing invalid IDs
    with pytest.raises(ValueError):
        message_unreact(token2, 72830725, reaction1)
        message_unreact(token2, message_id, 2436354645674576456874)

    ### Testing nonexistant reactions
    with pytest.raises(ValueError):
        message_unreact(token1, message_id, reaction1)
        message_unreact(token1, message_id, reaction2)

    ### Testing message ID in unjoined channel
    message_react(token2, message_id, 12)
    channel_leave(token2, channel_id)
    with pytest.raises(AccessError):
        message_unreact(token2, message_id, 12)

"""
Tests for message_pin behaviour
"""
# @pytest.mark.skip
def test_message_pin():
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    channel_join(token2, channel_id)
    print(store.get("users"))

    message_send(token2, channel_id, "Pin if you're cool")
    message_id = channel_messages(token2, channel_id, 0)['messages'][0]["message_id"]


    ### Functionality tests
    assert(message_pin(token1, message_id) == {})

    ### Test non-admin pinning
    message_unpin(token1, message_id)
    with pytest.raises(ValueError):
        message_pin(token2, message_id)

    ### Test invalid message IDs
    with pytest.raises(ValueError):
        message_pin(token1, 189203474)
        message_pin(token1, 674182965)

    ### Test messages that have already been pinned
    message_pin(token1, message_id)
    with pytest.raises(ValueError):
        message_pin(token1, message_id)

    ### Test access privileges
    channel_leave(token2, channel_id)
    with pytest.raises(ValueError):
        message_pin(token2, message_id)

"""
Tests for message_unpin behaviour
"""
# @pytest.mark.skip
def test_message_unpin():
    store.reset()
    (channel_id, token1, token2, id_1, id_2) = supply_channel()
    channel_join(token2, channel_id)

    message_send(token2, channel_id, "Pin if you're cool")
    message_id = channel_messages(token2, channel_id, 0)['messages'][0]["message_id"]

    message_pin(token1, message_id)

    ### Functionality test
    message_unpin(token1, message_id)

    ### Test non-admin unpinning
    message_pin(token1, message_id)
    with pytest.raises(ValueError):
        message_unpin(token2, message_id)

    ### Test invalid message IDs
    with pytest.raises(ValueError):
        message_unpin(token1, 7823419067)
        message_unpin(token1, 1728394013)

    ### Test messages that have already been unpinned
    message_unpin(token1, message_id)
    with pytest.raises(ValueError):
        message_unpin(token1, message_id)

    ### Test access privileges
    channel_leave(token2, channel_id)
    with pytest.raises(ValueError):
        message_unpin(token2, message_id)


####### Helper functions #######

def getNumMessages(token, channel_id):
    channelMessages = store.get("channel_data", "channel_id", channel_id)[0]["messages"]
    if channelMessages == None:
        return 0
    return len(channelMessages)


# Tests if the message exists and has the same message
def validMessage(messageNumber, message, channel_id, token):
    channelMessages = store.get("channel_data", "channel_id", channel_id)[0]["messages"]
    index = messageNumber - 1
    messageChannel = channelMessages[index]["message"]
    print(messageChannel)
    return messageChannel == message
