import pytest
import datetime

from ..search import *
from ..message import *
from ..auth import *
from ..user import *
from ..channel import *
from ..errors import AccessError
from ..admin_userpermission_change import *

"""
Fixture to reset store before each test run
"""
@pytest.fixture
def reset_store():
	store.reset()

"""
Fixture to register two users
"""
@pytest.fixture
def reg_users():
	details = auth_register("z5555555@student.unsw.edu.au", "passsss", "Fn", "Ln")
	details2 = auth_register("taken@liam.neeson.com", "passsss", "Fnn", "Ln")

	uid = details['u_id']
	token = details['token']
	uid2 = details2['u_id']
	token2 = details2['token']

	return uid, token, uid2, token2

"""
Tests for user_profile behaviour
"""
def test_user_profile(reset_store, reg_users):
	"""
	Verify types for user_profile return
	"""
	def verif_types(ret):
		VALID_KEYS = ["email", "name_first", "name_last", "handle_str", "profile_img_url"]
		for key in ret.keys():
			if key not in VALID_KEYS or type(ret[key]) not in [str, int, list, type(None)]:
				return False
				
		return True

	### Setup
	uid1, token1, uid2, token2 = reg_users

	### Test functionality
	assert(verif_types(
		user_profile(token1, uid1)
	))
	assert(verif_types(
		user_profile(token2, uid2)
	))

	### Test invalid u_id
	with pytest.raises(ValueError):
		user_profile(token1, "nonexistant uid")
	with pytest.raises(ValueError):
		user_profile(token2, "803cdb0f-3722-47ce-a1ca-7b3b24cde7e7")
		
	#Test that user_profile returns same value as we used to register 
	assert (user_profile(token1, uid1)["email"] == "z5555555@student.unsw.edu.au")
	assert (user_profile(token1, uid1)["name_first"] == "Fn")  
	assert (user_profile(token1, uid1)["name_last"] == "Ln")

"""
Tests for user_profile_setname
"""
def test_user_profile_setname(reset_store, reg_users):
	REALLYLONGSTR = "heylilpissbaby,youthinkyou'resofrickingcool,huh?youthinkyou'resofrickingtough?"
	ANOTHERLONGSTR = "youtalkalottabiggameforsomeonewithsuchasmalltruck...ohlookatthosearmsyourarmslooksocutetheylooklikelilcigarettes"
	FIFTYCHARSTR = "ibeticouldsmokeyouicouldroastyouandyoudloveittheny"
	FIFTYONECHAR = "BOYSCOMINWITHDBIGTRUCKSFEELSOCLEANLIKEAMONEYMACHINE"

	### Setup
	u_id, token, u_id2, token2 = reg_users

	### Functionality tests
	assert(user_profile_setname(token, "Fn", "Ln") == {})

	### Name length tests
	assert(user_profile_setname(token, FIFTYCHARSTR, FIFTYCHARSTR) == {})
	with pytest.raises(ValueError):
		user_profile_setname(token, FIFTYONECHAR, FIFTYONECHAR)
	with pytest.raises(ValueError):
		user_profile_setname(token, REALLYLONGSTR, ANOTHERLONGSTR)
	with pytest.raises(ValueError):
		user_profile_setname(token, "normallength", ANOTHERLONGSTR)
	with pytest.raises(ValueError):
		user_profile_setname(token, REALLYLONGSTR, "normallength")
	
	#change name then check that name was correctly changed
	user_profile_setname(token, "Fn2", "Ln2")
	assert user_profile(token, u_id)["name_first"] == "Fn2"
	assert user_profile(token, u_id)["name_last"] == "Ln2"


"""
Tests for user_profile_setemail
"""
def test_user_profile_setemail(reset_store, reg_users):
	### Setup
	uid, token, uid2, token2 = reg_users

	### Functionality tests
	assert(user_profile_setemail(token, "validemail@hotmail.com") == {})
	#Test the email has been changed
	assert user_profile(token, uid)["email"] == "validemail@hotmail.com"

	### Email validity tests
	assert(user_profile_setemail(token, "ano.ther+weirdbut@valid.email.org") == {})

	with pytest.raises(ValueError):
		user_profile_setemail(token, "almostvalid@@but.not.com")
	with pytest.raises(ValueError):
		user_profile_setemail(token, "@#$invalid!$%(chars@gmail.com")
	with pytest.raises(ValueError):
		user_profile_setemail(token, "just not an email")

	### Duplicate email tests
	with pytest.raises(ValueError):
		user_profile_setemail(token, "taken@liam.neeson.com")

"""
Tests for user_profile_sethandle
"""
def test_user_profile_sethandle(reset_store, reg_users):
	TWENTYCHARS = "youthirstygograbaspr"
	TWENTYONECH = "itemycripslurkindontd"
	REALLYLONGG = "ietonightijustwannadancewithubabyjustdontmovetoofast"

	### Setup
	uid, token, uid2, token2 = reg_users

	### Functionality tests
	assert(user_profile_sethandle(token, "normalHandle") == {})
	assert(user_profile_sethandle(token, "realDonaldTrump") == {})
	#Check that the handle has been changed
	assert user_profile(token, uid)["handle_str"] == "realDonaldTrump"

	### Length tests
	assert(user_profile_sethandle(token, TWENTYCHARS) == {})
	with pytest.raises(ValueError):
		user_profile_sethandle(token, TWENTYONECH)
	with pytest.raises(ValueError):
		user_profile_sethandle(token, REALLYLONGG)

	### Test existing handles
	with pytest.raises(ValueError):
		user_profile_sethandle(token2, TWENTYCHARS)

"""
Tests for user_all
"""
def test_user_all(reset_store, reg_users):
	uid, token, uid2, token2 = reg_users

	assert(len(user_all(token).get("users")) == 2)

"""
Tests for user_profiles_uploadphoto
"""
def test_user_profiles_uploadphoto(reset_store):
	### Setup
	details = auth_register("z5555555@student.unsw.edu.au", "passsss", "Fn", "Ln")
	uid = details['u_id']
	token = details['token']

	### Test different HTTP statuses
	assert(user_profiles_uploadphoto(token, "https://i.imgur.com/NtGRL8t.jpg", 0, 0, 200, 200)
		== {})

	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token, "http://imgur.com/not/an/image/jvbkaw", 0, 0, 200, 200)
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token, "http://imgur.com/not/an/image/jvbkaw", 0, 0, 200, 200)

	### Test incorrect content-type
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token, "https://i.imgur.com/RdJ0x4Q.png", 0,0,10,10)

	### Test image dimensions
	# all images are ones I uploaded to imgur
	assert(user_profiles_uploadphoto(token, "https://i.imgur.com/GlTiCfQ.jpg", 0, 0, 200, 200)
		== {})
	assert(user_profiles_uploadphoto(token, "https://i.imgur.com/giVCDPj.jpg", 0, 0, 301, 240)
		== {})

	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token, "https://i.imgur.com/GlTiCfQ.jpg", 0, 0, 201, 200)
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token, "https://i.imgur.com/GlTiCfQ.jpg", 0, 0, 200, 201)
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token, "https://i.imgur.com/GlTiCfQ.jpg", 0, -1, 200, 200)
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token, "https://i.imgur.com/GlTiCfQ.jpg", -1, 0, 200, 200)


# def test_admin_userpermission_change_1():
#     store.reset()

#     # SETUP BEGIN
#     authRegisterDict = auth_register("hayden@gmail.com", "passwordisnotcool", "hayden", "smith")
#     token1 = authRegisterDict['token']
#     id_1 = authRegisterDict["u_id"]
    
#     authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyoyo", "rob", "nicholas")
#     token2 = authRegisterDict2['token']
#     id_2 = authRegisterDict2["u_id"]

#     authRegisterDict3 = auth_register("Harrison.ford@gmail.com", "longpassowrd", "Harrison", "ford")
#     token3 = authRegisterDict3['token']
#     id_3 = authRegisterDict3["u_id"]
    
#     authRegisterDict4 = auth_register("jenniferaniston@gmail.com", "badpassword", "Jennifer", "Aniston")
#     id_4 = authRegisterDict4['u_id']
#     token4 = authRegisterDict4['token']   
#     # SETUP END
    
#     # Testing error and invlaid cases.
#     # Token 1 is the admin as it joined slack first.
#     # Token 1 is also the owner of Channel 1.

#     channel_id = channels_create(token1, "Channel 1", True)["channel_id"]
#     # Case 1: Passing invalid arguments.
#     # u_id is invalid.
#     with pytest.raises(ValueError, match=r"*"):
#         admin_userpermission_change (token1, 789654123, 2)
    
#     # Case 2: Permission_id is not valid.
#     with pytest.raises(ValueError, match=r"*"):
#         admin_userpermission_change (token1, id_2, 2000)

#     ChannelId = channels_create(token2, "Channel 2", True)["channel_id"]
#     channel_join(token3, ChannelId)
#     channel_join(token4, ChannelId)
#     # Token 1 is admin, token 2 is owner and 3 & 4 are users.

#     # Case 3 : The authorized person is not an owner.
#     # 3.1: User tries to make someone an owner.
#     with pytest.raises(AccessError,match=r"*"):
#         admin_userpermission_change (token3, id_4, 1)

#     # 3.2: User tries to make someone an admin. 
#     with pytest.raises(AccessError,match=r"*"): 
#         admin_userpermission_change (token3, id_4, 2)
    
#     # Case 4: Owner tries to make someone an admin.(As there can only be one admin)
#     with pytest.raises(AccessError,match=r"*"):
#         admin_userpermission_change (token2, id_3, 2)
    
# def test_admin_userpermission_change_2():
#     # Testing for all the generic cases in which permission id can be changed correctly.
#     store.reset()

#     # SETUP BEGIN
#     authRegisterDict = auth_register("hayden@gmail.com", "passwordisnotcool", "hayden", "smith")
#     token1 = authRegisterDict['token']
#     id_1 = authRegisterDict["u_id"]
    
#     authRegisterDict2 = auth_register("rob.nicholas@gmail.com", "yoyoyoyoyoyo", "rob", "nicholas")
#     token2 = authRegisterDict2['token']
#     id_2 = authRegisterDict2["u_id"]

#     authRegisterDict3 = auth_register("Harrison.ford@gmail.com", "longpassowrd", "Harrison", "ford")
#     token3 = authRegisterDict3['token']
#     id_3 = authRegisterDict3["u_id"]
    
#     authRegisterDict4 = auth_register("jenniferaniston@gmail.com", "badpassword", "Jennifer", "Aniston")
#     id_4 = authRegisterDict4['u_id']
#     token4 = authRegisterDict4['token']   
#     # SETUP END

#     # Token1 makes the channel 1.
#     channel1Id = channels_create(token1, "Channel 1", True)["channel_id"]
#     # Token 2 and token3 joins the channel.
#     channel_invite(token1, channel1Id, id_2)
#     channel_join(token3, channel1Id)
#     # Owner makes user an owner.
#     admin_userpermission_change (token1, id_2, 1)
#     channelOwners = channel_details(token1, channel1Id)["owner_members"]
#     req_user = store.get("users", "u_id", id_2)[0]
#     req_perm = req_user.get("permission_id")
#     assert req_perm == 1
    
#     # Token4 joins the channel and becomes an owner.
#     channel_invite(token2, channel1Id, id_4)
#     admin_userpermission_change (token2, id_4, 1)
#     channelOwners = channel_details(token1, channel1Id)["owner_members"]
#     req_user = store.get("users", "u_id", id_4)[0]
#     req_perm = req_user.get("permission_id")
#     assert req_perm == 1

#     # Also check id_3 is still as user.
#     req_user = store.get("users", "u_id", id_3)[0]
#     req_perm = req_user.get("permission_id")
#     assert req_perm == 3