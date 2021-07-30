from fixtures.builder import FixtureBuilder
import os
import shutil

def build(rotate_keys=None, base_dir=os.path.dirname(__file__)):
    """
    Generates a TUF test fixture that publishes twice -- once on the client,
    and twice on the server -- and, in between those two publications, can
    optionally rotate the keys of a given role.
    """
    name = 'PublishedTwiceForwardVersion'
    if rotate_keys is not None:
        name += 'WithRotatedKeys_' + rotate_keys

    fixture = FixtureBuilder(name, base_dir).publish(with_client=True)
    if rotate_keys is not None:
        fixture.add_key(rotate_keys)\
            .revoke_key(rotate_keys, key_index=0)
        fixture.publish()
        fixture.add_key(rotate_keys)\
            .revoke_key(rotate_keys, key_index=0)
            
    fixture.publish()
    shutil.move(os.path.join(base_dir, name, "server/metadata/", "3.root.json"),
    os.path.join(base_dir, name, "server/metadata/", "2.root.json"))