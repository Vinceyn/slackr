import pytest

from .. import store
from . import a
from . import b

def test_global_access():
	assert(store.s == {})

	a.insert("t1", {"a": 5})
	b.insert("t1", {"b": 6})

	assert(store.s == a.show())
	assert(a.show() == b.show())
	assert(store.s == {"t1": [ {"a": 5}, {"b": 6} ]})

@pytest.fixture
def state_1():
	store.s = {}

	tableName = "people"
	person1 = {"name": "John", "age": 24}
	person2 = {"name": "Sally", "age": 21}
	person3 = {"name": "Boomer", "age": 67}
	person4 = {"name": "Zoomer", "age": 12}

	store.insert(tableName, person1)
	store.insert(tableName, person2)
	store.insert(tableName, person3)
	store.insert(tableName, person4)

	tableName = "cars"
	# i know nothing about cars
	car1 = {"model": "2019 Tesla Model S", "price": 200000, "kms": 0, "service_history": False}
	car2 = {"model": "2008 Mitsubishi Lancer", "price": 5045, "kms": 100000, "service_history": True}
	car3 = {"model": "1998 Toyota Camry", "price": 999, "kms": 300000, "service_history": False}
	car4 = {"model": "2021 Elon MuskMobile(tm)", "price": 1278496591, "kms": -4, "service_history": False}

	store.insert(tableName, car1)
	store.insert(tableName, car2)
	store.insert(tableName, car3)
	store.insert(tableName, car4)

	assert store.s == {
		"people": [
			{"name": "John", "age": 24},
			{"name": "Sally", "age": 21},
			{"name": "Boomer", "age": 67},
			{"name": "Zoomer", "age": 12}
		],
		"cars": [
			{"model": "2019 Tesla Model S", "price": 200000, "kms": 0, "service_history": False},
			{"model": "2008 Mitsubishi Lancer", "price": 5045, "kms": 100000, "service_history": True},
			{"model": "1998 Toyota Camry", "price": 999, "kms": 300000, "service_history": False},
			{"model": "2021 Elon MuskMobile(tm)", "price": 1278496591, "kms": -4, "service_history": False}
		]
	}

def test_insert(state_1):
	assert(store.insert("people", {"name": "Elon Musk", "age": 2387}))

	assert(store.get("people", "name", "Elon Musk") == [{"name": "Elon Musk", "age": 2387}])
