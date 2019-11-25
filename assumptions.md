# Assumptions

Assumptions file

## Vincent
* There has to be at least one owner of a channel, if the channel is not empty
* An owner can't leave the channel if he's the only owner of the channel. He needs to give owner's right to another user before leaving
* If a channel is empty after the last user left the channel, the first user that will join the channel will become the owner of it
* Assumption for channel_details: New owners, members are in order such that recent members will be at added to the end of the list.
* Even if slackr admin/owner have the same right as channel owner, they are not considered as owner by the channel until we add them (i.e., a channel owner can't leave a channel if he's the only channel owner, even if there exists slackr owner/admin in the channel)

### Assumptions for channel_invite:
* If a user is in a channel, he can invite anyone he wants unless the invitee is already in the channel
* It doesn't matter if the channel is public or private, as long as the user is in it
* It doesn't matter if the user is an admin, an owner or a user
* You can't invite to a private channel if you don't have access to it
* You can't invite to a channel you're not part of (No test can be done at iteration 1 about this assumption, we don't have yet the token function)

### Assumptions for channel_join
* If the token is not an int, raise a ValueError
* If the token is already in the channel, raise ValueError

### Assumptions for channel_messages
* if start is not an int, raise valueError
* We have a function channel_msgNb(channelID) that return the number of messages in the channel

### Assumption for channel_addowner and channel_removeowner
* AccessError raised if token is not part of the channel

### Assumption for channel_message
* We have a function channel_msgNb() that return the number of messages in the channel
* ValueError raised if start is not an int

## Kristian
* The return value of date time is equal to `datetime.datetime.now() + datetime.timedelta(minutes=15)` (This may need to change if an error occurs and a threshold may be required)
* A user cannot post in a channel if they are not yet members of the channel

### Message function assumptions
* For `send_later()`, if the time is `datetime.datetime.now()` then there should also be an error returned
* For `message_send()`, assuming that a value error will be thrown if the channel does not exist
* For sending messages (`message_send` and `message_send_later()`), it is assumed that and Access Error will be thrown if the user is not part of the channel in which they are trying to post

### standup_send and message_send
* Standup will summarise discussion by creating a final message in the channel in which is formatted as follows:

```
User_1 - <message 1>
User_2 - <message 2>
User_1 - <message 3>
...
```
* Another assumption is that we can get the username based on the u_id from the message
* An empty string should not create a message entry
* A message of an invalid type (not a string) should return an exception

### User stories
* Adding the required fields for login and registration (Email, password for login and email, password, first and last name for registration) will make the user stories too specific
* Keeping details up to date encompasses: first/last name, handle, profile picture and email
* Channel information include: Owners, members, name and messages

## Avin
# Assumptions for search functions:
* Every message has a unique message ID, i.e message_id, even if the messages are the same.
* Search searches for all the substrings occurrences as well as full string searches.
* Upon a search conducted, all the channels that the user has access to are searched.
* Search is not case sensitive.
* Search also searches for messages produced by the user(the search conductor).
* Order of the messages in the list is the same as the order of the messages in the channel. (first in first out)
* Data structure of message is interpreted as each element of the list is a dictionary under the form:
    {"message_id": message_id,"u_id": u_id, "message": message, "time_created": time_created, "is_unread":is_unread}

# Assumption for channel_leave:
* If someone joins an empty channel, they become the owner of the channel.
* Owner of the channel can leave if there are multiple owners or there is no other member/user in the channel.
* Admins become owner of the channel upon join it.
* A user cannot leave a channel he is not in.

# Assumption for channel_addowner:
* You cannot make someone an owner who is not in the channel.
* A person who is not in channel cannot make anyone an owner of that channel.

# Assumption for channel_removeowner:
* You cannot remove ownership from someone of a channel who is not in that channel.
* Someone who is not in a channel cannot remove ownership from anyone who is in that channel.
* Owners can remove ownership of other owners.
* Admin can remove and make anyone an owner from the members of a channel.

# Assumption for channels_listall:
* It doesn't matter for listall if the user is in the channel or not, it just stores all created channels.
* # The order for all the created channels is such that new channels created are added to the end of the list containing all the names of channels made.

# Assumption for admin_userpermission_change:
* There is only one Admin in slack. (The person joining slack first)
* Admin cannot leave slack unless the whole slack is empty.
* Admin can give and take permission from anyone in the channel.
* Owners can give permissions to users, and take permission's from owners as well.


## Eddie
### Assumptions in tests
* The token required by many functions can both identify and verify the identity of the user it's associated with - i.e. the token is similar in functionality to a JSON web token
* Each user will have its own u_id which is unique to that user
* Users can use any valid email - there are no restrictions on which domain the email is associated with, etc.
* Emails are case insensitive
* Each user can only have one email associated with their account
* Each user can only edit their own profile - no user can edit another user's profile
* We only need a user's first and last name - we don't care about middle name
* In the test for each function, we assume that any other functions we call are correctly implemented
* In our tests, I assume that each test runs independently - side effects of one test do not carry over to another
* For argument sanity tests (e.g. incorrect argument types, missing/extra args), we do not care which exception is thrown, as long as *some* exception is thrown by the function.
* Invalid tokens are ignored by user_* functions (since documentation does not specify an error)
* Message reactions are identified sequentially from 1-n
