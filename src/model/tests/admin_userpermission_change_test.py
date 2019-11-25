import pytest
import sys

from ..errors import AccessError
from ..search import *
from ..auth import *
from ..message import *
from ..channel import *
from ..admin_userpermission_change import *

def test_admin_userpermission_change_1():
    store.reset()

    # SETUP BEGIN
    authRegisterDict = auth_register("hayden@gmail.com", "passwordisnotcool", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    authRegisterDict3 = auth_register("Harrison.ford@gmail.com", "longpassowrd", "Harrison", "ford")
    token3 = authRegisterDict3['token']
    id_3 = authRegisterDict3["u_id"]
    
    authRegisterDict4 = auth_register("jenniferaniston@gmail.com", "badpassword", "Jennifer", "Aniston")
    id_4 = authRegisterDict4['u_id']
    token4 = authRegisterDict4['token']   
    # SETUP END
    
    # Testing error and invlaid cases.
    # Token 1 is the admin as it joined slack first.
    # Token 1 is also the owner of Channel 1.

    channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
    # Case 1: Passing invalid arguments.
    # u_id is invalid.
    with pytest.raises(ValueError):
        admin_userpermission_change (token1, 789654123, 2)
    
    # Case 2: Permission_id is not valid.
    with pytest.raises(ValueError):
        admin_userpermission_change (token1, id_2, 2000)

    ChannelId = channels_create(token2, "Channel 2", True)["channel_id"]
    channel_join(token3, ChannelId)
    channel_join(token4, ChannelId)
    # Token 1 is admin, token 2 is owner and 3 & 4 are users.

    # Case 3 : The authorized person is not an owner.
    # 3.1: User tries to make someone an owner.
    with pytest.raises(AccessError):
        admin_userpermission_change (token3, id_4, 1)

    # 3.2: User tries to make someone an admin. 
    with pytest.raises(AccessError): 
        admin_userpermission_change (token3, id_4, 2)
    
    # Case 4: Owner tries to make someone an admin.(As there can only be one admin)
    with pytest.raises(AccessError):
        admin_userpermission_change (token2, id_3, 2)
    
def test_admin_userpermission_change_2():
    # Testing for all the generic cases in which permission id can be changed correctly.
    store.reset()

    # SETUP BEGIN
    authRegisterDict = auth_register("hayden@gmail.com", "passwordisnotcool", "hayden", "smith")
    token1 = authRegisterDict['token']
    id_1 = authRegisterDict["u_id"]
    
    authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyoyo", "rob", "nicholas")
    token2 = authRegisterDict2['token']
    id_2 = authRegisterDict2["u_id"]

    authRegisterDict3 = auth_register("Harrison.ford@gmail.com", "longpassowrd", "Harrison", "ford")
    token3 = authRegisterDict3['token']
    id_3 = authRegisterDict3["u_id"]
    
    authRegisterDict4 = auth_register("jenniferaniston@gmail.com", "badpassword", "Jennifer", "Aniston")
    id_4 = authRegisterDict4['u_id']
    token4 = authRegisterDict4['token']   
    # SETUP END

    # Token1 makes the channel 1.
    channel1Id = channels_create(token1, "Channel 1", True)["channel_id"]
    # Token 2 and token3 joins the channel.
    channel_invite(token1, channel1Id, id_2)
    channel_join(token3, channel1Id)
    # Owner makes user an owner.
    admin_userpermission_change (token1, id_2, 1)
    channelOwners = channel_details(token1, channel1Id)["owner_members"]
    req_user = store.get("users", "u_id", id_2)[0]
    req_perm = req_user.get("permission_id")
    assert req_perm == 1
    
    # Token4 joins the channel and becomes an owner.
    channel_invite(token2, channel1Id, id_4)
    admin_userpermission_change (token2, id_4, 1)
    channelOwners = channel_details(token1, channel1Id)["owner_members"]
    req_user = store.get("users", "u_id", id_4)[0]
    req_perm = req_user.get("permission_id")
    assert req_perm == 1
    
    # Also check id_3 is still as user.
    req_user = store.get("users", "u_id", id_3)[0]
    req_perm = req_user.get("permission_id")
    assert req_perm == 3
