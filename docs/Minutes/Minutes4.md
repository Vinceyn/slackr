# Minutes Week 5 Meeting 4
Meeting minutes for 14/10/2019, Kristian

## Members present
* Avin
* Kristian
* Vincent
* Eddie

## Discussion
1. Organise user stories into separate boards based on implementation (e.g. auth, message...)
2. Organise git repo and make branches for each functionality.
3. Create an API for storing and retrieving data
4. Begin function development in parallel
5. Keep teamwork file up to date
6. Discussed data structure

### Eddie repo organisation
server/\<file\> becomes src/model/\<file\>

## First idea about data structure:

We discussed about the data structure and we had a first idea about it. 

### Admin Pannel:
* Goal: Pannel of the slack
* List Channels allChannel
* Dictionary allMembers {
    "Normal_users" => {Set of normal Members}
    "Admin_users" => {Set of Admins}
    } //This dictionary contains all of the members in the slack, according to their permission. It links the key which is a string, to the value which are Set of Members.
    
### Members:

* int u_id
* string name_first
* string name_last
* string url_picture
* string handle
* string e_mail

### Channels:
* int channel_id
* boolean isPublic 
* dictionary Members {
    *Owner" => {set of owner members ID"}
    "Admin" => {set of admin members ID"}
    "all_user" => {set of all members ID"}
} //This dictionary contains all of the members in the channel, according to their channel's permission. Link the string keys to u_id values (don't want to have redundant information about members, we do not need to store 20 times a user's email if he's in 20 channels)
* List Messages all_message

###  Messages
* int msg_id
* int u_id
* datetime timeStamp
* boolean react
* boolean edited
* string msg

## Deadline

Avin and Vincent decided to finish the functions they tested (Channel and search) on Sunday

## Actionables

|Action | Person to Implement| Deadline|
|---|---|---|
|1. User story organisation |Avin| Today|
|2. Git organisation| Eddie| Today|
|3. Data API| Eddie| Tonight|
|4. Function development| Everyone|Flexible|
|5. Teamwork.md| Kristian| Continuous|
