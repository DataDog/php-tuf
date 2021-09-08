from fixtures.builder import FixtureBuilder
import os

def build(rotate_keys=None, root_expires_start=None, root_expires_end=None, base_dir=os.path.dirname(__file__), tag=None):
    """
    Generates a TUF test fixture that publishes twice -- once on the client,
    and twice on the server -- and, in between those two publications, can
    optionally rotate the keys of a given role.
    """
    name = 'PublishedTwice'
    if rotate_keys is not None:
        name += 'WithRotatedKeys_' + rotate_keys
    
    if tag is not None:
        name += "_" + tag

    fixture = FixtureBuilder(name, base_dir)    

    fixture.set_expiration("root", root_expires_start)    
    
    fixture.publish(with_client=True)

    if rotate_keys is not None:
        fixture.add_key(rotate_keys)\
            .revoke_key(rotate_keys, key_index=0)

        fixture.set_expiration("root", root_expires_end)

    fixture.publish()
