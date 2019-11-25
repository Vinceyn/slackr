from datastore import store
from .errors import AccessError
from .auth import auth_check_token

def admin_userpermission_change(token, u_id, permission_id):
    """
    Given a user ID, set their permissions to new permissions described by permission_id.
    """
    if not isinstance(u_id, int):
        raise ValueError("u_id is not an int")
    if not isinstance(permission_id, int):
        raise ValueError("permission_id is not an int")
    if permission_id < 1 or permission_id > 3:
        raise ValueError("permission_id is not valid")

    # Check requesting user's permissions
    req_u_id = auth_check_token(token)
    req_user = store.get("users", "u_id", req_u_id)[0]
    req_perm = req_user.get("permission_id")
    if req_perm == 3:
        raise AccessError("requesting user is not an owner or admin")
    if req_perm == 2 and permission_id == 1:
        raise AccessError("admins cannot make users owners")

    # Check target user
    results = store.get("users", "u_id", u_id)
    if len(results) != 1:
        raise ValueError(f"user with u_id {u_id} does not exist")
    target = results[0]

    target_perm = target.get("permission_id")
    if req_perm == 2 and target_perm == 1:
        raise AccessError("admins cannot change owners' permissions")

    # Execute permission change
    index = store.update("users", "permission_id", permission_id, "u_id", u_id)
    if index == 0:
        raise ValueError("Invalid user ID")
    return {}
