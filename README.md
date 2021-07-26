# TUF Fixture Generator

### Test fixtures generation

1. Install the Python TUF implementation and enable the pipenv:

       pipenv install
       pipenv shell

1. Initialize the repository and add/sign a target:

       python generate_fixtures.py

1. Fixtures should appear in `fixtures/`.

### Leveraging test fixtures directly

1. From `fixtures/*/tufrepo`:

       python3 -m http.server 8001

1. From `fixtures/*/tufclient`:

       mkdir -p tuftargets
       curl http://localhost:8001/targets/testtarget.txt > tuftargets/testtarget.txt
       client.py --repo http://localhost:8001 testtarget.txt
       # A 404 is expected for N.root.json unless a key has been rotated.


The generated fixtures will be placed in a folder called "generated_fixtures".
