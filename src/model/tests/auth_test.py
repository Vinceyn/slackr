import pytest

from ..errors import AccessError
from ..auth import *

"""
Fixture to reset store before each test run
"""
@pytest.fixture
def reset_store():
	store.reset()

"""
Fixture to register some users
"""
@pytest.fixture
def put_users():
	l1 = auth_register("z5555555@student.unsw.edu.au", "secure", "Big", "Man")
	l2 = auth_register("issaman@gmail.com", "coolpassword", "Small", "Man")
	l3 = auth_register("validemailbut@wrong.type.net", "coolpassword", "Moderate", "Man")

	registered = [l1, l2, l3]
	return [i.get("u_id") for i in registered], [i.get("token") for i in registered]

"""
Verify return value types for auth functions that do return
"""
def verif_auth_return(ret):
	return type(ret['u_id']) == int and type(ret['token']) == str

"""
Tests for auth_check_token behaviour
"""
def test_auth_check_token(reset_store, put_users):
	u_ids, tokens = put_users

	## Test normal functionality
	assert(auth_check_token(tokens[0]) == u_ids[0])
	assert(auth_check_token(tokens[1]) == u_ids[1])
	assert(auth_check_token(tokens[2]) == u_ids[2])

	## Test invalid token
	with pytest.raises(AccessError):
		auth_check_token("not a token at all haha xd")

	## Carefully crafted test to achieve 100% coverage haha yes hello marker
	with pytest.raises(AccessError):
		auth_check_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiSGVsbG8sIHRoaXMgaXMgYWJzb2x1dGVseSBub3QgYSBzbGFja3Igand0IiwianRpIjoiaGVubG8ifQ.RsZJJ6RvDbI4bCf2tY5Lnls3qmxsq1z0h-852KLRuYc")


"""
Tests for auth_login behaviour
"""
def test_auth_login(reset_store):
	### Register emails for our passing tests (assuming register works)
	auth_register("z5555555@student.unsw.edu.au", "secure", "Big", "Man")
	auth_register("issaman@gmail.com", "coolpassword", "Small", "Man")
	auth_register("validemailbut@wrong.type.net", "coolpassword", "Moderate", "Man")
	auth_register("validemailbut@no.password.net", "coolpassword", "Chunky", "Man")
	auth_register("w.e.i-r.d+email@cool-and.nicedomain.rocks", "secure123", "Mini", "Man")

	### Passing tests
	assert(verif_auth_return(auth_login("z5555555@student.unsw.edu.au", "secure")))
	assert(verif_auth_return(auth_login("issaman@gmail.com", "coolpassword")))
	# this will fail using the given link's regex, but is a valid email
	# comment out if required
	assert(verif_auth_return(auth_login("w.e.i-r.d+email@cool-and.nicedomain.rocks", "secure123")))

	### Test invalid emails
	with pytest.raises(ValueError):
		auth_login("completely&&invalid\\email@@@aaaaaa.b.c", "hasapassword")
		auth_login("almostvalid@butnoTLD", "coolpassword")
	with pytest.raises(ValueError):
		auth_login("validbutnot@registered.co", "coolpassword")

	### Test missing fields, incorrect field types
	### We catch any exception here because this behaviour is undocumented
	with pytest.raises(Exception):
		auth_login("validemailbut@no.password.net")
		auth_login("validemailbut@wrong.type.net", 123456)
		auth_login(123456, "invalidEmailType")

	### Test incorrect email, password
	with pytest.raises(ValueError):
		auth_login("z5555555@student.unsw.edu.au", "wrongpassword")
		auth_login("nonexistant@email.sydney", "isthispasswordwrong?we'llneverknow")

"""
Tests for auth_logout behaviour
"""
def test_auth_logout(reset_store):
	### Setup - assuming these functions work
	valid_token = auth_register("a@b.com", "passwor", "Cool", "Man")['token']

	### Tests
	assert(auth_logout(valid_token) == {})

	with pytest.raises(AccessError):
		auth_logout("some(invalid)token")
		auth_logout("superreallylong(invalid)token")

	with pytest.raises(Exception):
		auth_logout()

"""
Tests for auth_register behaviour
"""
def test_auth_register(reset_store):
	### Setup (assuming some level of functionality)
	auth_register("alreadyTaken@gmail.com", "password", "Good", "Man")

	### Passing tests
	assert(verif_auth_return(
		auth_register("z5555555@student.unsw.edu.au", "secure", "Big", "Man")
	))
	assert(verif_auth_return(
		auth_register("issaman@gmail.com", "coolpassword", "Small", "Man")
	))
	# Another valid email that would be deemed invalid by the linked algorithm
	# Comment out if this is causing issues
	assert(verif_auth_return(
		auth_register("w.e.i-r.d+email@cool-and.nicedomain.rocks", "secure123", "Mini", "Man")
	))

	### Test email validity
	with pytest.raises(ValueError):
		auth_register("completely&&invalid\\email@@@aaaaaa.b.c", "hasapassword", "Fn", "Ln")
		auth_register("almostvalid@butnoTLD", "coolpassword", "Fn", "Ln")

	### Test taken emails
	with pytest.raises(ValueError):
		auth_register("alreadyTaken@gmail.com", "coolpassword", "Fn", "Ln")

	### Test password validity
	with pytest.raises(ValueError):
		auth_register("thinkingofemails@isgetting.exhausting.com", "2srt", "Fn", "Ln")

	### Test length requirements
	REALLYLONGSTR = "heylilpissbaby,youthinkyou'resofrickingcool,huh?youthinkyou'resofrickingtough?"
	ANOTHERLONGSTR = "youtalkalottabiggameforsomeonewithsuchasmalltruck...ohlookatthosearmsyourarmslooksocutetheylooklikelilcigarettes"
	FIFTYCHARSTR = "ibeticouldsmokeyouicouldroastyouandyoudloveittheny"
	FIFTYONECHAR = "BOYSCOMINWITHDBIGTRUCKSFEELSOCLEANLIKEAMONEYMACHINE"

	auth_register("untaken@protonmail.com", "hiimvalid", FIFTYCHARSTR, FIFTYCHARSTR)

	with pytest.raises(ValueError):
		auth_register("boringemail@protonmail.com", "hiimvalid", FIFTYONECHAR, FIFTYONECHAR)
		auth_register("boringemail@protonmail.com", "hiimvalid", REALLYLONGSTR, "Ln")
		auth_register("boringemail@protonmail.com", "hiimvalid", "Fn", ANOTHERLONGSTR)
		auth_register("boringemail@protonmail.com", "hiimvalid", REALLYLONGSTR, ANOTHERLONGSTR)

	### Argument sanity tests
	with pytest.raises(Exception):
		auth_register("boringemail@protonmail.com", "missingargs")
		auth_register()
		auth_register(["Incorrect", "arg", "types"], 765, 123, 456)

"""
Tests for auth_passwordreset behaviour
"""
def test_auth_passwordreset(reset_store, put_users):
	u_ids, tokens = put_users

	## Setup - add some reset codes
	auth_passwordreset_addcode("resetcode123", u_ids[0])
	auth_passwordreset_addcode("resetcode456", u_ids[1])

	## Test resetting password
	auth_passwordreset_reset("resetcode123", "newpassword123")
	assert(auth_login("z5555555@student.unsw.edu.au", "newpassword123")) # if a truthy value is returned we have passed

	## Test password length
	with pytest.raises(ValueError):
		auth_passwordreset_reset("resetcode456", "2shrt")

	## Test invalid reset code
	with pytest.raises(ValueError):
		auth_passwordreset_reset("notacode123", "uijvbneknfklwe")

	## Arg sanity checks
	with pytest.raises(Exception):
		auth_passwordreset_reset("onearg")
		auth_passwordreset_reset("type", 3452617438)
		auth_passwordreset_reset()
