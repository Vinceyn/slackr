# datastore
In datastore, your data is organised in tables, each holding a dictionary of some kind.

Ideally, each dictionary in any one table will have the exact same fields, although this is not enforced.

## Usage
This is just an example, please read the documentation in store.py for a more complete guide.

```python
from datastore import store

tableName = "people"
person1 = {"name": "John", "age": 24}
person2 = {"name": "Sally", "age": 21}
person3 = {"name": "Boomer", "age": 67}
person4 = {"name": "Zoomer", "age": 12}

## Inserting into store
store.insert(tableName, person1)
store.insert(tableName, person2)
store.insert(tableName, person3)
store.insert(tableName, person4)

## Finding data in store
found = store.get(tableName)
# found == [{"name": "John", "age": 24}, {"name": "Sally", "age": 12}]

# You can also specify a single key/value pair to match;
found = store.get(tableName, "name", "John")
# found == [{"name": "John", "age": 24}]

## Updating data in the store
# Here, we update John's age to 25
# Note the order of the arguments
store.update(tableName, "age", 25, "name", "John")

## Deleting data from store
store.remove(tableName, person1)
# person1 is no longer in the store

# alternatively, specify some data
store.remove(tableName, "name", "Sally")
# person2 is deleted from the store
# WARNING this will delete EVERY row satisfying the criteria, not just one

## Debugging
# We can access the underlying store by using .s;
print(store.s)
# will print {"people": [{"name": "Boomer", "age": 67}, {"name": "Zoomer", "age": 12}]}
```

Full API documentation is available in the source code, `store.py`, as doc strings.

## Data structures:
### Given data structures
Theses all are a list of dictoinaries with the following fields:

__messages__
```python
{ message_id, u_id, message, time_created, reacts, is_pinned }
```

__reacts__
```python
{ react_id, u_ids, is_this_user_reacted }
```

__channels__
```python
{ channel_id,  name}
```

__members__
```python
{ u_id, name_first, name_last}
```
__uids__
```python
{ u_id }
```


### Additional data structures
This is a preliminary structure, feel free to add/make changes to them as needed.

__users__
```python
{ u_id, channels, name_first, name_last, handle_str, email, profile_url, permission_id }
```

__sessions__
```python
{ u_id, jwt_id, time_created }
```

__channel_data__
```python
{ channel_id, name, messages, members, owners '''(members type)''', is_public }
```

__resets__
```python
{ reset_code, u_id }
```

### Overall structure
```python
s {
    "users": [{user_entry}, {user_entry}, {user_entry}],
    "sessions": [{session_entry}, {session_entry}, {session_entry}]
    "channel_data": [{channel_entry}, {channel_entry}, {channel_entry}],
    "next_id": [{"type": "message_id", "value": value}, {"type": "react_id", "next": value}]
}
```