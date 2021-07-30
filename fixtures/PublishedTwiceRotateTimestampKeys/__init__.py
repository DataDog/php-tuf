from fixtures.builder import FixtureBuilder
import os

def build(rotate_keys=None, base_dir=os.path.dirname(__file__)):
    """
    Generates a TUF test fixture that publishes twice -- once on the client,
    and twice on the server -- and, in between those two publications, can
    optionally rotate the keys of a given role.
    """
    name = 'PublishedTwiceRotateTimestampKeys'
    if rotate_keys is not None:
        name += 'WithRotatedKeys_' + rotate_keys

    fixture = FixtureBuilder(name, base_dir).publish(with_client=True)
    if rotate_keys is not None:
        fixture.add_key(rotate_keys)\
            .revoke_key(rotate_keys, key_index=0)
    fixture.add_key("timestamp")
    fixture.publish()
