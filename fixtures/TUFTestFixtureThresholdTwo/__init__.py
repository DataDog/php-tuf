from fixtures.builder import FixtureBuilder
import os

def build(base_dir=os.path.dirname(__file__)):
    fixture = FixtureBuilder('TUFTestFixtureThresholdTwo', base_dir)\
        .add_key('timestamp')
    fixture._role('timestamp').threshold = 2
    fixture.repository.mark_dirty(['timestamp'])
    fixture.publish(with_client=True)
