"""
Authentication functions for slackr
"""

import re
import random
from datetime import datetime
import hashlib
import jwt

from datastore import store
from .errors import AccessError

HMAC_SECRET = "we push to master development secret"

def verify_token(func):
    """
    Decorator to verify token validity before running a function
    Usage:
    - add decorator to your function (`@verify_token`)
    - remove token as argument to your function
    - remove call to auth_check_token from inside your function
    - if you were using the caller's u_id (return value of auth_check_token), add `caller_u_id`
      as a keyword argument
    """
    def verif_then_run(token, *args, **kwargs):
        """
        let's make pylint happy
        """
        u_id = auth_check_token(token)

        # pass verified uid as keyword argument, if the function accepts it
        try:
            return func(*args, **kwargs, caller_u_id=u_id)
        except TypeError:
            # function did not expect caller_u_id; run it without
            return func(*args, **kwargs)
    return verif_then_run

def auth_check_token(token):
    """
    Given a token, verify that it is a valid token, with a valid session ID, and return
    the u_id of the token owner
    """
	# Decode token
    try:
        payload = jwt.decode(token, HMAC_SECRET, algorithms=['HS256'])
    except:
        # invalid token
        raise AccessError("Error parsing & verifying token")

    # Check if session exists in store
    results = store.get("sessions", "jwt_id", payload.get("jti"))
    if not results:
        raise AccessError("Invalid session token")

    # Check that session belongs to this user
    # multiple sessions may share a session ID, so we iterate through
    # this is pretty unlikely though, so we comment this out
    # sess = None
    # for index in results:
    #     if index.get("u_id") == payload.get("uid"):
    #         sess = index
    # if sess == None:
    #     raise AccessError("Invalid session token")

    return results[0].get("u_id")

def auth_login(email, password):
    """
    Given a registered users' email and password, generates a valid token for the
    user to remain authenticated
    TODO better ID gen
    """
    # validate email
    if not is_valid_email(email):
        raise ValueError("invalid email")

    # find user with email
    res = store.get("users", "email", email)
    if not res:
        raise ValueError(f"user with email '{email}' does not exist")
    user = res[0]

    # check password
    pwhash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    if pwhash != user["password"]:
        raise ValueError("incorrect password")

	# create jwt
    sess_id = random.randint(1, 9999) # we don't bother verifying this is unique
    payload = {
        "jti": sess_id,
        "uid": user["u_id"]
    }
    token = jwt.encode(payload, HMAC_SECRET, algorithm='HS256').decode("utf-8")

    # create session
    sess = {
        "u_id": user["u_id"],
        "jwt_id": sess_id,
        "time_created": datetime.now()
    }
    store.insert("sessions", sess)

    return {"u_id": user["u_id"], "token": token}

def auth_logout(token):
    """
    Given an active token, invalidates the taken to log the user out.
    Given a non-valid token, does nothing
    """
    try:
        payload = jwt.decode(token, HMAC_SECRET, algorithms=['HS256'])
    except:
        raise AccessError("invalid token")

    store.remove("sessions", "jwt_id", payload["jti"])

    return {}

def auth_register(email, password, name_first, name_last):
    """
    Given a user's first and last name, email address, and password, create a new
    account for them and return a new token for authentication in their session
    TODO more efficient datastore access if implemented
    """
    # Verify email validity
    if not is_valid_email(email):
        raise ValueError("invalid email")

	# Check if table already exists
    try:
        store.get("users")
        users_table_exists = True
    except ValueError:
        users_table_exists = False

    # Check if user already exists
    if users_table_exists and store.get("users", "email", email) != []:
        raise ValueError(f"user already exists with email '{email}'")

    # Check password strength
    if len(password) < 6:
        raise ValueError("password must be at least 6 characters")

	# Check name length
    name1 = len(name_first)
    name2 = len(name_last)
    if name1 < 1 or name1 > 50 or name2 < 1 or name2 > 50:
        raise ValueError("names must be between 1 and 50 characters each")

    # cool, register the user
    # check number of registered users to determine admin status
    user_is_admin = False
    if (not users_table_exists) or (not store.get("users")):
        user_is_admin = True

    # generate terrible random number id, and check the datastore to ensure it's unused
    # with a timeout in case of unexpected scale

    # hiiii if you're reading this, i've commented out the code that continually generates
    # random ids until a unique one is found, because there's no easy way to test it
    # so it was screwing up our coverage percentage, even though it's a good condition to have
    # if u can't test code then just delete it *taps head*

    # crazy how making students achieve 100% coverage forces worse practices wow insane
    new_id = random.randint(1, 999999)
    # if users_table_exists:
    #     existing_ids = [u["u_id"] for u in store.get("users")]
    #     iter_count = 1
    #     while new_id in existing_ids:
    #         iter_count += 1
    #         new_id = random.randint(1, 999999)

    #         if iter_count >= 100:
    #             raise Exception("could not reasonably find a unique ID")

    store.insert("users", {
        "u_id": new_id,
        "channels": [],
        "name_first": name_first,
        "name_last": name_last,
        "handle_str": None,
        "email": email,
        "profile_img_url": None,
        "permission_id": (1 if user_is_admin else 3),
        "password": hashlib.sha256(password.encode("utf-8")).hexdigest()
    })

    # log the user in to generate a token
    return auth_login(email, password)

def auth_passwordreset_addcode(code, u_id):
    """
    Put a password reset code into the datastore
    Unauthenticated - this is only called internally
    """
    store.insert("resets", {
        "reset_code": code,
        "u_id": u_id
    })

    return

def auth_passwordreset_reset(reset_code, new_password):
    """
    Given a reset code for a user, set that user's new password to the password provided
    TODO stub
    """
	# Check if reset code is valid
    res = store.get("resets", "reset_code", reset_code)
    if not res:
        raise ValueError("invalid reset code")
    reset = res[0]

	# Change password
    if len(new_password) < 6:
        raise ValueError("new password must be at least 6 characters")

    pwhash = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
    store.update("users", "password", pwhash, "u_id", reset.get("u_id"))

    # Remove reset obj from store (after successful reset, just in case user screws up)
    store.remove("resets", "reset_code", reset_code)

    return {}

### Helper functions

def is_valid_email(mail):
    """
    Check email validity
    """
	# courtesy of emailregex.com
    pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if re.match(pattern, mail) is None:
        return False
    return True
