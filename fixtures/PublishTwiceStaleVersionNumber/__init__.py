from fixtures.builder import FixtureBuilder
import os
import shutil

def build(rotate_keys=None, base_dir=os.path.dirname(__file__)):
    """
    Generates a TUF test fixture that publishes twice -- once on the client,
    and twice on the server -- and, in between those two publications, can
    optionally rotate the keys of a given role. It forces write to avoid increamenting the version number.
    """
    name = 'PublishTwiceStaleVersionNumber'
    if rotate_keys is not None:
        name += 'WithRotatedKeys_' + rotate_keys

    fixture = FixtureBuilder(name, base_dir).publish(with_client=True)
    shutil.copyfile(os.path.join(base_dir, name, "server/metadata/", "1.root.json"),
       os.path.join(base_dir, name, "server/metadata/", "2.root.json"))