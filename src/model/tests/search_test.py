import datetime
import pytest
import random
import string

from ..errors import AccessError
from ..search import *
from ..auth import *
from ..message import *
from ..channel import *
from datetime import *
from hypothesis import given, strategies

'''
@pytest.fixture
def supply_token ():

    # SETUP BEGIN
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token = authRegisterDict['token']
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    # SETUP END

    return (token, token2)
    
@pytest.fixture
def supply_channel (supply_token):
    #return a tuple (channel_id, token1, token2)
    channel_id = channels_create(supply_token[0], "Channel 1", True)["channel_id"]
    channel_join(supply_token[1], channel_id)
    return (channel_id, supply_token[0], supply_token[1])
'''
def test_search():

    # SETUP BEGIN
    store.reset()
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]
    # SETUP END

    channel_id = channels_create(token1, "Channel New", True)["channel_id"]
    channel_join(token2, channel_id)
    
    for i in range (1, 50):
        new_str = get_strings(10)
        message_send(token1, channel_id, (f"{new_str}"))
    
    all_messages_List = search(token1, "e")["messages"]
    found = len(all_messages_List)
    
    for i in range (1, 50):
        new_str = get_strings(9)
        message_send(token2, channel_id, (f"{new_str}"))

    new_message_list = search(token1, "e")["messages"]
    list_common = []
    
    for i in all_messages_List:
        for j in new_message_list:
            if i == j:
                list_common.append(i)
  
    assert (len(all_messages_List) == len(list_common))
    for i in range(1, len(all_messages_List)):
        assert (all_messages_List[i] == list_common[i])

def get_strings(string_len = 10):
    letter = string.ascii_lowercase
    return ''.join(random.choice(letter) for i in range(string_len))

@pytest.mark.search
def test_search_1 ():
    # Test1: Checking in empty channel.
    store.reset()
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    
    emptyList = search(token1, "Hi")["messages"]
    assert len(emptyList) == 0

@pytest.mark.search
def test_search_2 ():
    # Test2: Checking that the return type is a list. (List of Dictionaries)
    store.reset()
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    
    emptyDict = search(token1, "Hi")
    assert type(emptyDict) is dict
    assert type(emptyDict["messages"]) is list

@pytest.mark.search
def test_search_3 ():
    store.reset()
    #Test3: Checking for a message that has not been previously sent. (No result for a search)
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_join(token2, channel_id)

    message_send(token1, channel_id, "Hi")
    message_send(token1, channel_id, "Hello")

    searchList = search(token1, "chocolate")["messages"]
    assert len(searchList) == 0

@pytest.mark.search
def test_search_4 ():
    store.reset()
    #Test4: Testing Case: if the search query matches one of the messages.

    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_join(token2, channel_id)

    message_send(token1, channel_id, "Hi")
    message_send(token1, channel_id, "Hello")

    searchList = search(token1, "Hi")["messages"]
    assert len(searchList) == 1
    assert searchList[0]["message"] == "Hi"
    
@pytest.mark.search
def test_search_5 ():
    store.reset()
    #Test5: Testing Case: if multiple messages got the search query as substring

    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_join(token2, channel_id)

    message_send(token1, channel_id, "Hi")
    message_send(token2, channel_id, "Hello")
    message_send(token1, channel_id, "I am rob.")
    message_send(token2, channel_id, "I am hayden.")

    searchList = search(token2, "I am")["messages"]
    assert len(searchList) == 2
    assert searchList[0]["message"] == "I am rob."
    assert searchList[1]["message"] == "I am hayden."

@pytest.mark.search
def test_search_6 ():
    store.reset()
    #Test6: Testing Case: if the search query is launched from a user that didn't send the message

    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_join(token2, channel_id)

    message_send(token1, channel_id, "Hi")
    message_send(token1, channel_id, "Hello")
    message_send(token1, channel_id, "Anyone there?")
    message_send(token1, channel_id, "Why I am so lonely!")

    searchList = search(token2, "Anyone there?")["messages"]
    assert len(searchList) == 1
     
@pytest.mark.search
def test_search_7 ():
    store.reset()
    #Test7: Testing Case: if the search query is launched from a user which is not in the channel, but the channel is public

    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_join(token2, channel_id)
     
    authRegisterDict3 = auth_register("GandalfTheGrey@dwad.fra", "IShouldPass", "Gandalf", "Grey")
    token3 = authRegisterDict3['token']
    message_send(token1, channel_id, "Line1")
    message_send(token2, channel_id, "Line2")
    message_send(token1, channel_id, "Line3")
    message_send(token2, channel_id, "Line4")
    message_send(token2, channel_id, "Line5")
    searchList = search(token3, "lINE")["messages"]
    assert len(searchList) == 0
    channel_join(token3, channel_id)
    searchList = search(token3, "lINE")["messages"]
    assert len(searchList) == 5

@pytest.mark.search
def test_search_8 ():
    store.reset()
    #Test8: If the search query is repeated multiple times in a message, only one occurence of the message will appear

    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_join(token2, channel_id)

    message_send(token1, channel_id, "Hi. Hi")
    searchList = search(token1, "Hi")["messages"]
    assert len(searchList) == 1

@pytest.mark.search
def test_search_9 ():
    store.reset()
    #Test9: The search function is not case-sensitive

    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_join(token2, channel_id)

    message_send(token1, channel_id, "HI")
    searchList = search(token1, "hi")["messages"]
    assert len(searchList) == 1

@pytest.mark.search
def test_search_10 ():
    store.reset()
    #Test10: A search query don't find messages from a private channel where the user don't belong to


    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']

    channel_id = channels_create(token1, "Channel 1", False)['channel_id']
    message_send(token1, channel_id, "Hi")

    searchList = search(token2, "Hi")["messages"]
    assert len(searchList) == 0

@pytest.mark.search
def test_search_11 ():
    store.reset()
    #Test11: Check types of the value in dictionary 

    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_join(token2, channel_id)
    
    message_send(token1, channel_id, "hi")
    searchList = search(token1, "hi")["messages"]

    assert len(searchList) == 1
    assert type(searchList[0]["message_id"]) is int
    assert type(searchList[0]["u_id"]) is int   
    assert type(searchList[0]["message"]) is str
    assert type(searchList[0]["time_created"]) is int

@pytest.mark.search
def test_search_12():
    store.reset()
    authRegisterDict = auth_register("hayden@gmail.com", "password", "hayden", "smith")
    token1 = authRegisterDict['token']
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    channel_join(token2, channel_id)
    
    with pytest.raises(ValueError):
        search(1, "ewla")
    
    with pytest.raises(ValueError):
        search("dwa", 21321)
