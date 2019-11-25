Before each test is run, the datastore isn't automatically reset - you must reset it
yourself using store.reset() - see auth_test.py

If you run into any module import errors, make sure the PYTHONPATH env var is set to src/; e.g.
```sh
project/src/model/tests ~ $ PYTHONPATH=../.. pytest-3 test_file.py
```