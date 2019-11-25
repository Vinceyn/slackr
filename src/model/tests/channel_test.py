import datetime
import pytest
import sys
import random

from ..errors import AccessError
from ..search import *
from ..auth import *
from ..message import *
from ..channel import *
    
'''
@pytest.fixture
def supply_token():
    store.reset()
    # SETUP BEGIN
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]
    # SETUP END

    return (token1, token2, id_1, id_2)

@pytest.fixture
def supply_channel(supply_token):
    #Return a Tuple (channel_id, token1, token2, id_1, id_2), when token1 is the owner of the channel
    channelCreated = channels_create(supply_token[0], "Channel 1", True)["channel_id"]
    return (channelCreated, supply_token[0], supply_token[1], supply_token[2], supply_token[3])
'''   
def test_channel_id_checker():

    number = get_num(1001)
    assert number > 0
    # SETUP BEGIN
    store.reset()
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    # SETUP END

    for i in range (1, number):
        channels_create(token1, (f"Channel: {i}") , True)

    all_channels = channels_listall(token1)
    for element in all_channels:
        for index in all_channels:
            if element != index:
                assert element["id"] != index["id"]

# Function to generate a random number.
def get_num(maximum):
    for x in range(1):
        return (random.randint(1,maximum))

#Test channel_invite _________________________________________________________________________________________________________________

##.invite
def test_channel_invite_1():
    #Test1: check about error raised
    store.reset()
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]

    #With non-valid arguments
    with pytest.raises(ValueError):
        channel_invite(token1, "ImABadChannelID", 12345)
    with pytest.raises(ValueError):
        channel_invite(token1, 12345, "ImABadUserID")
    with pytest.raises(ValueError):
        channel_invite(12345, channel_id, "ImABadUserID")

    #Invite someone who is already in the channel
    with pytest.raises(ValueError):
        channel_invite(token1, channel_id, id_1)
    
    #Invite in a channel that doesn't exist
    with pytest.raises(ValueError):
        channel_invite(token1, 12345, id_2)

    #Invite in a private channel when you don't have access to it
    privateChannelID = channels_create(token1, "Channel 2", False)["channel_id"]
    authRegisterDict3 = auth_register("Harrison.ford@gmail.com", "Hello its me", "Harrison", "ford")
    id_3 = authRegisterDict3["u_id"]
    with pytest.raises(AccessError):
        channel_invite(token2, privateChannelID, id_3)

    #Invite in a channel you're not part of 
    publicChannelID = channels_create(token1, "Channel 3", True)["channel_id"]
    with pytest.raises(AccessError):
        channel_invite(token2, privateChannelID, id_3)    


##.invite
def test_channel_invite_3():
    store.reset()
    #Test3: Test case for a private channel
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]

    #SETUP
    authRegisterDict3 = auth_register("Harrison.ford@gmail.com", "Hello its me", "Harrison", "ford")
    token3 = authRegisterDict3["token"]
    id_3 = authRegisterDict3["u_id"]
    #ENDSETUP

    #Private Channel Test
    channel_2_ID = channels_create(token2, "Channel 2", False)["channel_id"]
    channel_invite(token2, channel_2_ID, id_3)

    channel2IdMembers = channel_details(token2, channel_2_ID)["all_members"]
    print(channel2IdMembers)
    for member in channel2IdMembers:
        if member["u_id"] == id_3:
            isID3InMembers = True
    assert isID3InMembers

##.invite
def test_channel_invite_2():
    #Test2: General cases test, with invite from admin/owner/user
    store.reset()
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]

    #Admin case
    channel_invite(token1, channel_id, id_2)
    
    channel1IdMembers = channel_details(token1, channel_id)["all_members"]
    isID2InMembers = False
    for member in channel1IdMembers:
        if member["u_id"] == id_2:
            isID2InMembers = True
    assert isID2InMembers

    #SETUP
    authRegisterDict3 = auth_register("Harrison.ford@gmail.com", "Hello its me", "Harrison", "ford")
    token3 = authRegisterDict3["token"]
    id_3 = authRegisterDict3["u_id"]
    #ENDSETUP

    #Owner Case
    channel_2_ID = channels_create(token2, "Channel 2", True)["channel_id"]
    channel_invite(token2, channel_2_ID, id_3)

    channel2IdMembers = channel_details(token2, channel_2_ID)["all_members"]
    isID3InMembers = False
    for member in channel2IdMembers:
        if member["u_id"] == id_3:
            isID3InMembers = True
    assert isID3InMembers

    #User Case
    channel_invite(token3, channel_2_ID, id_1)

    channel2IdMembers = channel_details(token3, channel_2_ID)["all_members"]
    isID1InMembers = False
    for member in channel2IdMembers:
        if member["u_id"] == id_1:
            isID1InMembers = True
    assert isID1InMembers
#Test channel_join ___________________________________________________________________________________________________________________

#.join
def test_channel_join_1():
    #Test1: Check about error raised 
    store.reset()
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]

    #With non-valid argument: string channel_id
    with pytest.raises(ValueError):
        channel_join(token2, "dakjlw")
    
    #with non-valid argument: channel_id that doesn't exist
    with pytest.raises(ValueError):
        channel_join(token2, 12345) 

    # token is of wront type.
    with pytest.raises(ValueError):
        channel_join(12345, channel_id) 

    #with non-valid argument: the token is already in the channel
    with pytest.raises(ValueError):
        channel_join(token1, channel_id) 

    #with a access error, when a user try to join one unauthorized channel
    privateChannelID = channels_create(token1, "Channel 2", False)["channel_id"]
    with pytest.raises(AccessError):
        channel_join(token2, privateChannelID)

#.join
def test_channel_join_2():
    #Test2: join a public channel works
    store.reset()
    #Take the supply data, then token2 join the channel
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_join(token2, channel_id)

    #Check that token2 is in the channel
    isID2InChannel = False
    for member in channel_details(token1, channel_id)['all_members']:
        if member["u_id"] == id_2:
            isID2InChannel = True
    assert isID2InChannel

#.join
def test_channel_join_3():
    #Test3: Join a private channel when you're an admin work
    store.reset()
    #SETUP CHANNEL
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    privateChannelID = channels_create(token2, "Channel 2", False)["channel_id"]
    #END SETUP CHANNEL

    #Token1, as admin, join the private channel
    channel_join(token1, privateChannelID)

    #Check that token1 is in the channel
    isID1InChannel = False
    for member in channel_details(token1, privateChannelID)['all_members']:
        if member["u_id"] == id_1:
            isID1InChannel = True

    assert isID1InChannel


#Test channel_details_________________________________________________________________________________________________________________

#.details
def test_channel_details_1():
    store.reset()
    #Test1: Raise Error function
    #SETUP CHANNEL
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    #END SETUP CHANNEL
    #ValueError when channel_id is not an int
    with pytest.raises(ValueError):
        channel_details(token1, "dalkjwd")
    
    #ValueError when token is not a string
    with pytest.raises(ValueError):
        channel_details(12345, channel_id)
    
    #ValueError when channel_id does not exist
    with pytest.raises(ValueError):
        channel_details(token1, 12345)

    #AccessError when a user which is not member of the channel tries to get details
    with pytest.raises(AccessError):
        channel_details(token2, channel_id)

#.details
def test_channel_details_2():
    
    #Test2: Check the trivial case (one owner which is the only user). Then one member joins as an user, check he's on all_member and the name of the channel is good
    #SETUP CHANNEL
    store.reset()
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    #END SETUP CHANNEL

    #Check the channel name, owner_members and all_members
    channelDetailsDict = channel_details(token1, channel_id)

    #Check the channel name is good
    assert channelDetailsDict["name"] == "Channel 1"

    #Check that there's only one owner, and check its details
    assert len(channelDetailsDict["owner_members"]) == 1
    assert channelDetailsDict["owner_members"][0]["u_id"] == id_1
    assert channelDetailsDict["owner_members"][0]["name_first"] == "hayden"
    assert channelDetailsDict["owner_members"][0]["name_last"] == "smith" 
    

    #Check that there's only one member, and check its details
    assert len(channelDetailsDict["all_members"]) == 1
    assert channelDetailsDict["all_members"][0]["u_id"] == id_1
    assert channelDetailsDict["all_members"][0]["name_first"] == "hayden"
    assert channelDetailsDict["all_members"][0]["name_last"] == "smith" 

    #Token2 joins channel
    channel_join(token2, channel_id)

    #Check that token2 can search for details in the channel
    channelDetailsDict = channel_details(token2, channel_id)

    #Check that there are 2 members
    assert len(channelDetailsDict["all_members"]) == 2

#.details
def test_channel_details_3():
    store.reset()
    #Test3: One member is invited as an user by the owner, then he become one owner. Check he's in owner_members and in all_members. Then remove original owner and check the values are good

    #SETUP CHANNEL
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    #END SETUP CHANNEL

    #Token2 is invited by Token1
    channel_invite(token1, channel_id, id_2)

    #Check the channel name, owner_members and all_members
    channelDetailsDict = channel_details(token2, channel_id)
    assert channelDetailsDict["name"] == "Channel 1"
    assert len(channelDetailsDict["owner_members"]) == 1
    assert len(channelDetailsDict["all_members"]) == 2

    #Make Token2 owner
    channel_addowner(token1, channel_id, id_2)

    #Check there are 2 owners, and check that the creator details is also good 
    channelDetailsDict = channel_details(token1, channel_id)
    assert len(channelDetailsDict["owner_members"]) == 2

    #Make the first owner quit
    channel_leave(token1, channel_id)

    #Check there's one user, which is the owner  
    channelDetailsDict = channel_details(token2, channel_id)
    assert len(channelDetailsDict["owner_members"]) == 1
    assert len(channelDetailsDict["all_members"]) == 1
        

#Test channel_messages _______________________________________________________________________________________________________________

#.messages
def test_channel_messages_1():
    #Test1: Test Error raised by the function
    store.reset()
    #SETUP CHANNEL
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    message_send(token1, channel_id, "Hey I've just met you")
    #END SETUP CHANNEL

    #ValueError when channel_id is not an int
    with pytest.raises(ValueError):
        channel_messages(token1, "dalkjwd", 0)
    
    #ValueError when channel_id does not exist
    with pytest.raises(ValueError):
        channel_messages(token1, 12345, 0)

    #ValueError when start is not an int
    with pytest.raises(ValueError):
        channel_messages(token1, channel_id, "dlkaw")

    #ValueError when the start index is negative
    with pytest.raises(ValueError):
        channel_messages(token1, channel_id, -1)
    
    #ValueError when the start index is bigger than number of messages
    with pytest.raises(ValueError):
        channel_messages(token1, channel_id, 1234)

    #SETUP CHANNEL
    message_send(token1, channel_id, "Hey I've just met you")
    #END SETUP CHANNEL
    #AccessError when a user which is not member of the channel tries to get messages
    with pytest.raises(AccessError):
        channel_details(token2, channel_id)

#.messages
def test_channel_messages_2():
    #Test2: Test index of start and end, and messages returned values if there is only one user
    #SETUP CHANNEL
    store.reset()
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    #END SETUP CHANNEL

    #SETUP CHANNEL MESSAGES
    for i in range(143):
        msg = "I know how to count until {}"
        new_msg = msg.format(i)
        message_send(token1, channel_id, new_msg)

    #Take the first 50 messages
    firstMsgDict = channel_messages(token1, channel_id, 0)
    #Check the index of start and end
    assert firstMsgDict["start"] == 0
    assert firstMsgDict["end"] == 49
    a = 0
    for i in range(142, 92,-1):
        msg = "I know how to count until {}"
        new_msg = msg.format(i)
        assert firstMsgDict["messages"][a]["message"] == new_msg
        assert firstMsgDict["messages"][a]["u_id"] == id_1
        a += 1
    
    #Take the last messages
    lastMsgDict = channel_messages(token1, channel_id, 100)
    
    #Check the index of start, and that end is -1
    assert lastMsgDict["start"] == 100
    assert lastMsgDict["end"] == -1

#.messages
def test_channel_messages_3():
    #Test3: Test there is no problem if multiple people send messages, and if someone that didn't send any messages search them
    #SETUP CHANNEL
    store.reset()
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    #END SETUP CHANNEL

    #user2 joins the channel
    channel_join(token2, channel_id)

    #user1, then user2, send messages
    for i in range(30):
        msg = "I know how to count until {}"
        new_msg = msg.format(i)
        message_send(token1, channel_id, new_msg)

    for i in range(30, 60):
        msg = "I don't know how to count until {}"
        new_msg = msg.format(i)
        message_send(token2, channel_id, new_msg)


    #SETUP 3rd user
    authRegisterDict3 = auth_register("Harrison.ford@gmail.com", "Hello its me", "Harrison", "ford")
    token3 = authRegisterDict3["token"]
    id_3 = authRegisterDict3["u_id"]
    channel_join(token3, channel_id)
    #ENDSETUP

    #dict of the first msg, taken by the 3rd user
    firstMsgDict = channel_messages(token3, channel_id, 0)
    #Check the index of start and end
    assert firstMsgDict["start"] == 0
    assert firstMsgDict["end"] == 49

    #check the last 30 messages, sent by ID_2
    a = 0
    for i in range(59, 29, -1):
        msg = "I don't know how to count until {}"
        new_msg = msg.format(i)
        assert firstMsgDict["messages"][a]["message"] == new_msg
        assert firstMsgDict["messages"][a]["u_id"] == id_2
        a+= 1

    #check the messages between 10 and 30, sent by ID_1
    for i in range(29, 10, -1):
        msg = "I know how to count until {}"
        new_msg = msg.format(i)
        assert firstMsgDict["messages"][a]["message"] == new_msg
        assert firstMsgDict["messages"][a]["u_id"] == id_1
        a += 1

#Test channels_create _________________________________________________________________________________________________________________

#.channels_create
def test_channels_create_1():
    store.reset()
    # This tests gives out all the cases for ValueError or AccessError.
    
    # SETUP BEGIN
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token = authRegisterDict['token']
    # SETUP END
    
    # Case 0: Passing in wrong type of arguments and in different order.
    # Passing in an invalid token.
    with pytest.raises(ValueError):
        channels_create(123132, "Channed name", True)
    
    # Passing in invalid channel name type.
    with pytest.raises(ValueError):
        channels_create(token, 78965452, False)

    # Passing in invalid token type.
    with pytest.raises(ValueError):
        channels_create(78965423, "Channed name.", True)

    # Passing in incorrect bool.
    with pytest.raises(ValueError):
        channels_create(token, "Channed name.", "Nope")

    with pytest.raises(ValueError):
        channels_create(token, "Channed name.", 1011)

    # ValueError when channel name is empty.
    with pytest.raises(ValueError):
        channels_create(token, "", True)

    # Case 1: When channel Name is more than 20 characters long.
    # 1.1 Channel is Public.
    with pytest.raises(ValueError):
        channels_create(token, "This channel name is way too long.", True)
    
    # 1.2 Channel is Private.
    with pytest.raises(ValueError):
        channels_create(token, "This channel name is also way too long.", False)

#.channels_create
def test_channels_create_2():
    store.reset()
    # Testing the cases where channels can be successfully created.
    # SETUP BEGIN
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    id_1 = authRegisterDict['u_id']
    token = authRegisterDict['token']
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    id_2 = authRegisterDict2['u_id']
    token2 = authRegisterDict2['token']
    # SETUP END
    
    # Case 1: Creating a public channel.
    ChannelId = channels_create(token, "Channel 1", True)["channel_id"]
    assert type(ChannelId) is int
    channel1Owners = channel_details(token, ChannelId)["owner_members"]
    tokenisOwner = False
    for owner in channel1Owners:
        if owner["u_id"] == id_1:
            tokenisOwner = True

    assert tokenisOwner

    channel_join(token2, ChannelId)
    channelMembers = channel_details(token, ChannelId)["all_members"]
    assert channelMembers[0]["u_id"] == id_1 
    assert channelMembers[1]["u_id"] == id_2

    # Case 2: Creating a private channel.
    ChannelId2 = channels_create(token, "Channel 2", False)["channel_id"]
    assert type(ChannelId2) is int
    channel2Owners = channel_details(token, ChannelId2)["owner_members"]
    tokenisOwner2 = False
    for owner in channel1Owners:
        if owner["u_id"] == id_1:
            tokenisOwner2 = True

    assert tokenisOwner2
    
    # Case 2: As the channel is private, not everyone can join the channel.
    with pytest.raises(AccessError):
        channel_join(token2, ChannelId2)


#Test channel_leave _________________________________________________________________________________________________________________
#.channel_leave
def tests_channel_leave_1():
    store.reset()
    #Testing the cases which raise errors.
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    
    # Case 1: Providing non-valid arguments. 
    # 1.1 Channel_id is of wrong type.
    with pytest.raises(ValueError):
        channel_leave(token1, "ImABadChannelID")
    
    # 1.2 Token is of wrong type.
    with pytest.raises(ValueError):
        channel_leave(865, channel_id)

    # Case 2: Try to leave a channel that doesn't exist.
    with pytest.raises(ValueError):
        channel_leave(token1, 12345)
    
    # SETUP BEGIN
    authRegisterDict3 = auth_register("Harrison.ford@gmail.com", "Hello its me", "Harrison", "ford")
    token3 = authRegisterDict3['token']
    id_3 = authRegisterDict3["u_id"]
    # SETUP END

    with pytest.raises(ValueError):
        channel_leave(token1, channel_id)

    # Case 3: User trying to leave a channel it's not in.
    with pytest.raises(ValueError):
        channel_leave(token3, channel_id)

    Channel_id2 = channels_create(token2, "Channel 2", False)["channel_id"]
    channel_invite(token2, Channel_id2, id_3)
    
    # Case 4: Owner Case, owner cannot leave if another owner is not in channel.
    # Channel 2: Token2 is owner and token1 is user.
    with pytest.raises(ValueError):
       channel_leave(token2, Channel_id2)

#.channel_leave
def test_channel_leave_2():
    # Testing cases in which admin/owners/users can successfully leave channel.
    store.reset()
    #SETUP
    authRegisterDict0 = auth_register("admin@gmail.com", "password", "admin", "admin")
    id_0 = authRegisterDict0['u_id']
    token0 = authRegisterDict0['token']
    
    authRegisterDict3 = auth_register("Harrison.ford@gmail.com", "Hello its me", "Harrison", "ford")
    token3 = authRegisterDict3["token"]
    id_3 = authRegisterDict3["u_id"]
    #ENDSETUP

    # Case 1: Admin makes a channel and leaves it.
    channel1Id = channels_create(token0, "Channel 1", False)["channel_id"]
    channel0Members = channel_details(token0, channel1Id)["all_members"]
    assert (len(channel0Members) == 1)

    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    # Case 2: Owner leaves a channel if there are multiple owners.
    channel2Id = channels_create(token1, "Channel 2", True)["channel_id"]
    channel_join(token2, channel2Id)
    channel_join(token3, channel2Id)
    channel_addowner(token1, channel2Id, id_2)

    # Now channel has token1 and token2 as owner and token3 as user.
    channel_leave(token1, channel2Id)
    # Now channel has one owner and one user.
    channel2Members = channel_details(token2, channel2Id)["all_members"]
    assert (len(channel2Members) == 2)
    channel2Owners = channel_details(token2, channel2Id)["owner_members"]
    assert (len(channel2Owners) == 1)

    # Case 3: User leaves the channel.
    # Token3 leaves the channel.
    channel_leave(token3, channel2Id)
    channel2Members = channel_details(token2, channel2Id)["all_members"]
    assert (len(channel2Members) == 1)
    channel2Owners = channel_details(token2, channel2Id)["owner_members"]
    # Checking if the only owner is token2(id_2). Only token2 is in channel 2.
    assert (channel2Owners[0]["u_id"] == id_2)  

    # Case 4: Owner leaves if there are multiple owners or an Admin. (Admin is also an owner of channel if admin is in the channel)
    # In Channel 2 there is only one owner/user - token2.
    channel_join(token0, channel2Id)
    channel_join(token3, channel2Id)
    
    # only token2(owner) and token 0 (admin of slackr/usr of channel) and token3(user) in channel 2.
    channel2Members = channel_details(token3, channel2Id)["all_members"]
    assert (len(channel2Members) == 3)
    channel2Owners = channel_details(token3, channel2Id)["owner_members"]
    assert (len(channel2Owners) == 1)

    # Case 5: Admin leaves if there is one another owner there in channel.
    channel_addowner(token0, channel2Id, id_3)
    channel_leave(token0, channel2Id)
    channel_leave(token2, channel2Id)
    # Only token3(owner) in channel.
    channel2Members = channel_details(token3, channel2Id)["all_members"]
    assert (len(channel2Members) == 1)
    channel2Owners = channel_details(token3, channel2Id)["owner_members"]
    assert (len(channel2Owners) == 1)

#Test channel_addowner _________________________________________________________________________________________________________________
#.channel_addowner
def test_channel_addowner_1():
    # Testing for cases that should raise errors.
    store.reset()
    # SETUP BEGIN
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    id_1 = authRegisterDict['u_id']
    token1 = authRegisterDict['token']

    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    id_2 = authRegisterDict2['u_id']
    token2 = authRegisterDict2['token']

    authRegisterDict3 = auth_register("noobmaster69@gmail.com", "Minercraft", "Noob", "Master")
    id_3 = authRegisterDict3['u_id']
    token3 = authRegisterDict3['token']
    # SETUP END

    channelCreated = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_join(token2, channelCreated)

    # Channel: token1 owner, token2 user.
    # Case 1: Passing in wrong arguments.
    # 1.1 Passing in wrong channel_id type.
    with pytest.raises(ValueError):
        channel_addowner(token1, "wrong arg type", id_2)

    # 1.2 Passing arguments in wrong order.
    with pytest.raises(ValueError):
        channel_addowner(channelCreated, token1, id_2)

    # 1.3 Passing in invalid channel_id.
    with pytest.raises(ValueError):
        channel_addowner(token1, 789654123, id_2)

    # 1.4 Passing in a u_id that doesn't exist.
    with pytest.raises(ValueError):
        channel_addowner(token1, 789654123, 69841)

    # Case 2: When an owner tries to add itself as an owner of channel.
    with pytest.raises(ValueError):
        channel_addowner(token1, channelCreated, id_1)

    # Case 3: AccessError if the authorised user is not an admin or owner of channel.
    with pytest.raises(AccessError):
        channel_addowner(token2, channelCreated, id_3)

    # SETUP BEGIN

    authRegisterDict4 = auth_register("jenniferaniston@gmail.com", "badpassword", "Jennifer", "Aniston")
    id_4 = authRegisterDict4['u_id']
    token4 = authRegisterDict4['token']    
    # SETUP END

    # Case 4: When a user who is not in channel tries to make a existing user of channel an owner.
    with pytest.raises(AccessError):
        channel_addowner(token3, channelCreated, id_2)

    # Case 5: When a user who is not in channel(token 3) tries to make someone who is also not in channel(token 4) an owner.
    with pytest.raises(AccessError):
        channel_addowner(token3, channelCreated, id_4)

#.channel_addowner
def test_channel_addowner_2():
    # Testing for the cases in which there are successful owner added to the channel.
    store.reset()
    # SETUP BEGIN
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    id_1 = authRegisterDict['u_id']
    token1 = authRegisterDict['token']

    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    id_2 = authRegisterDict2['u_id']
    token2 = authRegisterDict2['token']
    # SETUP END

    # Case 1: Someone makes a channel and adds another person an owner.
    # Token1 makes a channel, token2 join it and token1 makes token2 an owner.
    channelCreated = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_join(token2, channelCreated)
    
    # adding token2 as the owner of channel.
    channel_addowner(token1, channelCreated, id_2)
    
    channelOwners = channel_details(token2, channelCreated)["owner_members"]
    assert len(channelOwners) == 2
    assert channelOwners[0]["u_id"] == id_1
    assert channelOwners[1]["u_id"] == id_2

    # SETUP BEGIN
    authRegisterDict3 = auth_register("noobmaster69@gmail.com", "Minercraft", "Noob", "Master")
    id_3 = authRegisterDict3['u_id']
    token3 = authRegisterDict3['token']
    # SETUP END

    # Case2: Someone makes a private channel then gives another person owner permission. 
    # Token 2 makes a new private channel then token 3 joins and gets owners permission.
    channelCreated2 = channels_create(token2, "Channel 2", False)["channel_id"]
    channel_invite (token2, channelCreated2, id_3)
    
    # adding token3 as the owner of channel.
    channel_addowner(token2, channelCreated2, id_3)
    
    channelOwners2 = channel_details(token3, channelCreated2)["owner_members"]
    assert len(channelOwners2) == 2
    assert channelOwners2[0]["u_id"] == id_2
    assert channelOwners2[1]["u_id"] == id_3

    # Token 1 gets invited to channel 2
    channel_invite (token3, channelCreated2, id_1)

    channelOwners3 = channel_details(token3, channelCreated2)["owner_members"]
    assert len(channelOwners3) == 2
    assert channelOwners3[0]["u_id"] == id_2
    assert channelOwners3[1]["u_id"] == id_3


#Test channel_removeowner _________________________________________________________________________________________________________________
#.channel_removeowner
def test_channel_removeowner_1():
    # Testing for cases that should raise errors.
    store.reset()
    # SETUP BEGIN
    authRegisterDict0 = auth_register("admin@gmail.com", "password", "admin", "admin")
    id_0 = authRegisterDict0['u_id']
    token0 = authRegisterDict0['token']

    authRegisterDict1 = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    id_1 = authRegisterDict1['u_id']
    token1 = authRegisterDict1['token']

    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    id_2 = authRegisterDict2['u_id']
    token2 = authRegisterDict2['token']
    # SETUP END

    channelCreated = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_join(token2, channelCreated)
    channel_addowner(token1, channelCreated, id_2)
    
    # Case 1: Passing in wrong arguments.
    # 1.1 Passing in arguments in wrong order.
    with pytest.raises(ValueError):
        channel_removeowner(channelCreated, id_1, token1)

    # 1.2 Passing in arguments of wrong type.
    with pytest.raises(ValueError):
        channel_removeowner(token1, "wrong channel_id type", id_2)

    # 1.3 Passing in wrong channel_id.
    with pytest.raises(ValueError):
        channel_removeowner(token1, 789654123, id_2)

    # SETUP BEGIN
    authRegisterDict3 = auth_register("noobmaster69@gmail.com", "Minercraft", "Noob", "Master")
    id_3 = authRegisterDict3['u_id']
    token3 = authRegisterDict3['token']
    # SETUP END

    # Case2 : Trying to remove someone who is not in channel.
    with pytest.raises(ValueError):
        channel_removeowner(token1, channelCreated, id_3)

    # Case3: Trying to remove someone who is in channel but is not an owner.
    channel_join(token3, channelCreated)
    with pytest.raises(ValueError):
        channel_removeowner(token1, channelCreated, id_3)

    # Case 4: User trying to remove an owner.
    with pytest.raises(AccessError):
        channel_removeowner(token3, channelCreated, id_1)

    # Case 5: User trying to remove an admin.
    channel_join(token0, channelCreated)
    with pytest.raises(ValueError):
        channel_removeowner(token3, channelCreated, id_0)

    #Case 6: requester is not part of the channel
    channel_leave(token3, channelCreated)
    with pytest.raises(ValueError):
        channel_removeowner(token3, channelCreated, id_2)

    #Case 7: Only owner removes himself
    channel_leave(token0, channelCreated)
    channel_removeowner(token1, channelCreated, id_2)
    with pytest.raises(ValueError):
        channel_removeowner(token1, channelCreated, id_1)

@pytest.mark.channel_removeowner 
#.channel_removeowner 
def test_channel_removeowner_2():
    store.reset()
    # Testing for cases where there should be successful removal of owners.
    # SETUP BEGIN
    authRegisterDict0 = auth_register("admin@gmail.com", "password", "admin", "admin")
    id_0 = authRegisterDict0['u_id']
    token0 = authRegisterDict0['token']

    authRegisterDict1 = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    id_1 = authRegisterDict1['u_id']
    token1 = authRegisterDict1['token']

    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    id_2 = authRegisterDict2['u_id']
    token2 = authRegisterDict2['token']
    # SETUP END
    
    channelCreated = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_join(token2, channelCreated)
    channel_addowner(token1, channelCreated, id_2)
    
    # Case 1: Owner(token 2) removes another owner(token 1).
    channel_removeowner(token2, channelCreated, id_1)
    channelOwners = channel_details(token1, channelCreated)["owner_members"]
    assert len(channelOwners) == 1
    assert channelOwners[0]["u_id"] == id_2

    channel_join(token0, channelCreated)

    '''    
    # Case 2: Admin (token 0) removes owner (token 2).
    channel_removeowner(token0, channelCreated, id_2)
    channelOwners2 = channel_details(token0, channelCreated)["owner_members"]
    print(store.get('channel_data', 'channel_id', channelCreated)[0]['owners'])
    assert len(channelOwners2) == 1
    assert channelOwners2[0]["u_id"] == id_0
    ''' 

    channelCreated2 = channels_create(token2, "Channel 2", False)["channel_id"]
    channel_invite(token2, channelCreated2, id_1)
    channel_addowner(token2, channelCreated2, id_1)

    # Case 3: Owner(token 1) removes another owner(token 2).
    channel_removeowner(token1, channelCreated2, id_2)
    channelOwners3 = channel_details(token1, channelCreated2)["owner_members"]
    assert len(channelOwners3) == 1
    assert channelOwners3[0]["u_id"] == id_1

    channel_invite(token1, channelCreated2, id_0)
    
    '''
    # Admin (token 0) removes owner (token 1).
    channel_removeowner(token0, channelCreated2, id_1)
    channelOwners4 = channel_details(token0, channelCreated2)["owner_members"]
    assert len(channelOwners2) == 1
    assert channelOwners2[0]["u_id"] == id_0
    '''

#Test channels_list _________________________________________________________________________________________________________________
#.channels_list
def test_channels_list_1():
    # Testing cases where a list of all channels that the authorized user is part of can be correctly provided.
    store.reset()
    # SETUP BEGIN
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    id_1 = authRegisterDict['u_id']
    token1 = authRegisterDict['token']

    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    id_2 = authRegisterDict2['u_id']
    token2 = authRegisterDict2['token']
    # SETUP END
    
    # Case 1: When there are no channels.
    channel_id1 = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_id2 = channels_create(token1, "Channel 2", False)["channel_id"]
    # Token 2 is in 0 channels.
    assert (channels_list(token2)["channels"] == [])
    assert (channels_list(token1)["channels"][0]["channel_id"]) == channel_id1
    assert (channels_list(token1)["channels"][1]["channel_id"]) == channel_id2
    # Making some more channels.
    channel_id3 = channels_create(token1, "Channel 3", False)["channel_id"]
    channel_id4 = channels_create(token2, "Channel 4", True)["channel_id"]
    # Joining and inviting some people in channels.
    channel_join(token2, channel_id1)
    channel_invite(token1, channel_id3, id_2)
    # asserting cases that token2 is in these channels
    assert (channel_id4 == channels_list(token2)["channels"][0]["channel_id"])
    assert (channel_id1 == channels_list(token2)["channels"][1]["channel_id"])
    assert (channel_id3 == channels_list(token2)["channels"][2]["channel_id"])


#Test channels_listall _________________________________________________________________________________________________________________

#.channels_listall
def test_channels_listall_1():
    # Testing cases where a list of all channels can be correctly provided.
    store.reset()
    # SETUP BEGIN
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    id_1 = authRegisterDict['u_id']
    token1 = authRegisterDict['token']

    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    id_2 = authRegisterDict2['u_id']
    token2 = authRegisterDict2['token']
    # SETUP END
    # Case 1: When there are no channels.
    assert (channels_listall(token1)["channels"] == [])
     
    # Case 2: When there are some channels.
    channel_id1 = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_id2 = channels_create(token1, "Channel 2", False)["channel_id"]
    # Token 1 is owner of two channels.
    assert (channels_listall(token1)["channels"][0]["channel_id"]) == channel_id1
    assert (channels_listall(token1)["channels"][1]["channel_id"]) == channel_id2
    
    # Creating some more channels.
    channel_id3 = channels_create(token1, "Channel 3", True)["channel_id"]
    channel_id4 = channels_create(token1, "Channel 4", False)["channel_id"]
    # Asserting the channels of which token 1 is in.
    assert (channels_listall(token1)["channels"][0]["channel_id"]) == channel_id1
    assert (channels_listall(token1)["channels"][1]["channel_id"]) == channel_id2
    assert (channels_listall(token1)["channels"][2]["channel_id"]) == channel_id3
    assert (channels_listall(token1)["channels"][3]["channel_id"]) == channel_id4
    # Inviting some people to channels.
    channel_invite(token1, channel_id4, id_2)
    channel_invite(token1, channel_id2, id_2)
    channel_join(token2, channel_id3)
    # Asserting the channels of which token 2 is in.
    # The order of creation of channels: Channel 1,Channel 2,Channel 3, Channel 4
    # It doesn't matter for listall if the user is in the channel or not, it just stores all created channels.
    assert (channels_listall(token2)["channels"][0]["name"]) == "Channel 1"
    assert (channels_listall(token2)["channels"][1]["name"]) == "Channel 2"
    assert (channels_listall(token2)["channels"][2]["name"]) == "Channel 3"
    assert (channels_listall(token2)["channels"][3]["name"]) == "Channel 4"

