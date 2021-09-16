from fixtures.builder import FixtureBuilder
import os
from datetime import datetime, timedelta

def build(rotate_keys=None, add_key = 0, revoke_key=0, threshold=1, base_dir=os.path.dirname(__file__)):
    """
    Generates a TUF test fixture that publishes twice -- once on the client,
    with #add_key keys and sets the treshold to `threshold` -- 
    and, in between those two publications, revokes #revoke_key keys of a given role.
    """
    LONG_EXPIRATION = datetime.now() + timedelta(days=365*10) # expire in 10 years from now.
 
    name = 'PublishedTwiceMultiKeys'
    if rotate_keys is not None:
        name += 'add_' + str(add_key) + "_revoke_" + str(revoke_key) + "_threshold_" + str(threshold) + "_" + rotate_keys

    fixture = FixtureBuilder(name, base_dir)
    
    fixture.set_expiration("root", LONG_EXPIRATION)
    fixture.set_expiration("snapshot", LONG_EXPIRATION) 
    fixture.set_expiration("timestamp", LONG_EXPIRATION) 
    fixture.set_expiration("targets", LONG_EXPIRATION) 
    
    if rotate_keys is not None:
        # One key is already being added in the FixtureBuilder constructor.
        # Therefore, we add add_key-1 keys.
        for i in range(add_key-1):
            fixture.add_key(rotate_keys)
        fixture.set_threshold(rotate_keys, int(threshold)) 
    fixture.publish(with_client=True)

    if rotate_keys is not None:
        for i in range(revoke_key):
            fixture.revoke_key(rotate_keys, key_index=0)
    fixture.publish()
