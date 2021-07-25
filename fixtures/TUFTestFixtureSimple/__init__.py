from fixtures.builder import FixtureBuilder
import os

def build(based_dir=os.path.dirname(__file__)):
    FixtureBuilder('TUFTestFixtureSimple', based_dir)\
        .create_target('testtarget.txt')\
        .publish(with_client=True)
