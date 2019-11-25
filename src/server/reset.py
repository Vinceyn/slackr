# This isn't like the other blueprints in /server - this actually contains logic because all the
# mail stuff has to be here
from flask import Blueprint, request
from flask_mail import Mail, Message
import random
import string

from datastore import store
from model.auth import auth_passwordreset_reset, auth_passwordreset_addcode

SLACKR_ADDR = 'slackr.wepushtomaster@gmail.com'
SLACKR_PASS = "asdfghjkl;'"
RESET_CHARS = string.ascii_letters + string.digits
MAIN_APP = None

# Initialise blueprint
resets = Blueprint("resets", __name__)

# Config function to be called by index
def reset_config(a):
    global MAIN_APP
    MAIN_APP = a
    a.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME = SLACKR_ADDR,
        MAIL_PASSWORD = SLACKR_PASS
    )

@resets.route('/request/', methods=['POST'])
def gen_request():
    global MAIN_APP
    if MAIN_APP == None:
        # should never happen
        raise ValueError()
        pass

    mail = Mail(MAIN_APP)
    email = request.form.get("email")

    # Check if email exists
    results = store.get("users", "email", email)
    if len(results) == 0:
        raise ValueError("Email does not belong to any user") # this should get caught by our handler
    user = results[0]

    # Generate a reset code
    # it's highly unlikely we'll have a clash :))))
    code = "".join([RESET_CHARS[random.randint(0, len(RESET_CHARS) - 1)] for i in range(16)])
    auth_passwordreset_addcode(code, user.get("u_id"))

    # Send email
    msg = Message("Your slackr password reset",
        sender=SLACKR_ADDR,
        recipients=[email])
    msg.body = f"""Hi {user.get("name_first")},

    Someone requested a password reset for your email on slackr.

    Your reset code is: {code}

    If you did not request this, please contact our very existant support team.
    """
    mail.send(msg)

    return {}

@resets.route('/reset/', methods=['POST'])
def reset():
    return auth_passwordreset_reset(
        request.form.get("reset_code"),
        request.form.get("new_password")
    )
