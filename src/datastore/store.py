"""
in-memory datastore with terrible performance
"""
import pickle

s = {}

"""
Insert a row into the store, creating the table if it doesn't exist

Arguments:
table_name: string
vals: dict

Returns True if the insert was successful
"""
def insert(table_name, vals):
	global s

	if type(vals) != dict:
		raise ValueError("vals must be a dict")

	if table_name not in s.keys():
		s[table_name] = []

	s[table_name].append(vals)

	return True

"""
Get one or more rows from a table in the store, optionally filtered by key

Arguments:
table_name: string
key_name (optional): string
val (optional): string

Returns a list, containing all dicts that match the criteria
"""
def get(table_name, key_name=None, val=None):
	global s

	table = s.get(table_name, None)
	if table == None:
		raise ValueError(f"Table '{table_name}' does not exist in store")

	result = []

	if key_name == None or val == None: # no filter criteria
		result = [row for row in table] # deep copy of table
		return result

	for row in table:
		if row.get(key_name, None) == val:
			result.append(row)

	return [row for row in result]

"""
Update a row in the store, filtered by key

Arguments:
table_name: string
new_key: string
new_val: string
filter_key (optional): string
filter_val (optional): string

Returns the number of rows that were successfully updated
"""
def update(table_name, new_key, new_val, filter_key=None, filter_val=None):
	global s

	table = s.get(table_name, None)
	if table == None:
		raise ValueError(f"Table '{table_name}' does not exist in store")

	update_all = filter_key == None and filter_val == None # boolean - whether or not to update all
	rows_updated = 0
	
	for i, row in enumerate(table):
		if update_all or row.get(filter_key, None) == filter_val:
			table[i][new_key] = new_val
			rows_updated += 1

	return rows_updated

"""
Remove a row, or rows, in the store, filtered by key or row

Arguments:
table_name: string
to_delete: dict OR key: string
val (optional): string

Returns number of rows deleted
"""
def remove(table_name, arg1, val=None):
	global s

	table = s.get(table_name, None)
	if table == None:
		raise ValueError(f"Table '{table_name}' does not exist in store")

	if val == None:
		# delete specified row
		to_delete = arg1
		table.remove(to_delete)

		return 1
	else:
		# delete all matching criteria
		key = arg1
		idx_to_delete = []

		for i, row in enumerate(table):
			if row.get(key, None) == val:
				idx_to_delete.append(i)

		idx_to_delete.sort(reverse=True) # sort in reverse so we don't get our indices mixed up
		for idx in idx_to_delete:
			del table[idx]

		return len(idx_to_delete)

"""
Use pickle to save the current state of the store to a file.

Arguments:
file_name: string
"""
def save(file_name):
	global s

	with open(file_name, "wb") as of:
		pickle.dump(s, of)

	return

"""
Deserialise pickled store state from file_name
"""
def restore(file_name):
	global s

	with open(file_name, "rb") as inf:
		s = pickle.load(inf)

	return

"""
Give the length of one entry in the dataset

Arguments:
table_name:String

Returns the number of element of one elem
"""
def n_elems(table_name):
	global s
	
	table = s.get(table_name, None)

	if (table == None):
		return 0
		#raise ValueError(f"Table '{table_name}' does not exist in store")
	return len(table)

"""
Reset the store to initial state
"""
def reset():
	global s
	s = {}

"""
Print the store's contents for debugging purposes
"""
def show():
	global s
	for key in s:
		print(f"table '{key}':")
		for e in s.get(key):
			print("    ", e)