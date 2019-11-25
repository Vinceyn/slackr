import os
import jwt
from urllib import request as urlrequest
from urllib.error import HTTPError
from PIL import Image

from datastore import store
from model.auth import auth_check_token, is_valid_email, verify_token

HMAC_SECRET = "we push to master development secret"

"""
For a valid user, returns information about their email, first name, last name, and handle
"""
@verify_token
def user_profile(u_id):
    results = store.get("users", "u_id", u_id)
    if len(results) != 1:
        raise ValueError("u_id is not valid")

    user = results[0]

    return {"email": user.get("email"),
            "name_first": user.get("name_first"),
            "name_last": user.get("name_last"),
            "handle_str": user.get("handle_str"),
            "profile_img_url": user.get("profile_img_url")}

"""
Update the authorised user's first and last name
"""
@verify_token
def user_profile_setname(name_first, name_last, caller_u_id=None):
    # check name length requirements
    if len(name_first) < 1 or len(name_first) > 50:
        raise ValueError("Names must be between 1 and 50 characters long")
    if len(name_last) < 1 or len(name_last) > 50:
        raise ValueError("Names must be between 1 and 50 characters long")

    # update names in store
    store.update("users", "name_first", name_first, "u_id", caller_u_id)# != 1:
    #    raise Exception("Error updating first name")
    store.update("users", "name_last", name_last, "u_id", caller_u_id)# != 1:
    #    raise Exception("Error updating last name")

    return {}

"""
Update the authorised user's email address
"""
@verify_token
def user_profile_setemail(email, caller_u_id=None):
    # check email validity
    if not is_valid_email(email):
        raise ValueError(f"{email} is not a valid email")

    # check if user with email exists
    results = store.get("users", "email", email)
    if len(results) > 0:
        raise ValueError(f"User with email {email} already exists")

    # update email in store
    store.update("users", "email", email, "u_id", caller_u_id)# != 1:
    #    raise Exception("Error updating email")

    return {}

"""
Update the authorised user's handle (i.e. display name)
"""
@verify_token
def user_profile_sethandle(handle_str, caller_u_id=None):
    # check handle length requirements
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise ValueError("handle must be between 3 and 20 characters long")

    # check if user with handle exists
    results = store.get("users", "handle_str", handle_str)
    if len(results) > 0:
        raise ValueError(f"user with handle {handle_str} already exists")

    # update handle in store
    store.update("users", "handle_str", handle_str, "u_id", caller_u_id)# != 1:
    #    raise Exception("error updating handle")

    return {}

"""
Given a URL of an image on the internet, crops the image within bounds
(x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.
"""
@verify_token
def user_profiles_uploadphoto(img_url, x_start, y_start, x_end, y_end, caller_u_id=None):
    # Ideally, we'd have some kind of configuration system to provide us with a way to access
    # the absolute path we need, and our server's URL.
    # However, for the purposes of this project, I think it's good enough to use a relative
    # path and hardcode our URL - especially since the frontend has the loopback address
    # hardcoded too.

    # Check paramater validity
    if x_start >= x_end or y_start >= y_end or min(x_start, x_end, y_start, y_end) < 0:
        raise ValueError("Invalid crop coordinates")

    # Get response object for image, and check validity of response
    try:
        resp = urlrequest.urlopen(img_url)
    except HTTPError:
        # non-200 response
        raise ValueError("Image URL did not open successfully")

    if resp.getheader("Content-Type") == None or "image/jpeg" not in resp.getheader("Content-Type"):
        raise ValueError("URL did not point to a JPEG image")

    # Get PIL.Image object for the image
    img = Image.open(resp)
    if x_start > img.width or x_end > img.width or y_start > img.height or y_end > img.height:
        raise ValueError("Invalid crop coordinates")

    # Crop & save the image
    img_cropped = img.crop((x_start, y_start, x_end, y_end))

    file_path = f"../static/img/{str(caller_u_id)}.jpg" # shady relative path but it's fine
    img_cropped.save(os.path.abspath(file_path))

    # Close images to release memory
    img_cropped.close()
    img.close()

    # Update user dict with URL to profile photo
    photo_URL = f"http://127.0.0.1:5001/img/{str(caller_u_id)}.jpg"
    store.update("users", "profile_img_url", photo_URL, "u_id", caller_u_id)

    return {}

"""
Return a list of all registered users in the store
"""
@verify_token
def user_all():
    # We need to filter the dicts we get from the store, so we only return
    # relevant, non-sensitive information
    all_users = store.get("users")
    filtered_users = [{
        "u_id": i.get("u_id"),
        "email": i.get("email"),
        "name_first": i.get("name_first"),
        "name_last": i.get("name_last"),
        "handle_str": i.get("handle_str"),
        "profile_img_url": i.get("profile_img_url")
    } for i in all_users]

    return {"users": filtered_users}
