from fixtures.builder import FixtureBuilder
import os

def build(rotate_keys=None, root_expires_start=None, root_expires_end=None, publish_n_times=2, base_dir=os.path.dirname(__file__), tag=None):
    """
    Generates a TUF test fixture that publishes N times -- N-1 in the client,
    and N on the server -- and, in between those publications, can
    optionally rotate the keys of a given role.
    """
    name = 'Published'+str(publish_n_times)+"Times"
    if rotate_keys is not None:
        name += 'WithRotatedKeys_' + rotate_keys

    if tag is not None:
        name += "_" + tag
        
    fixture = FixtureBuilder(name, base_dir)
    fixture.set_expiration("root", root_expires_start)
    fixture.publish(with_client=True)
    for i in range(publish_n_times-1):
        if rotate_keys is not None:
            fixture.add_key(rotate_keys)\
                .revoke_key(rotate_keys, key_index=0)
        if i<publish_n_times-2:
            fixture.publish(with_client=True)
        else:
            fixture.set_expiration("root", root_expires_end)
            fixture.publish()