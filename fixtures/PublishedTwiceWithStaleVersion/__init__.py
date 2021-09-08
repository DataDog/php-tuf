from fixtures.builder import FixtureBuilder
import os
import shutil

def build(rotate_keys=None, base_dir=os.path.dirname(__file__)):
    """
    Generates a TUF test fixture that publishes twice -- the second time through copying the 1.root.json to 2.root.json.
    As a result, the version id of the 2.root.json is stale.
    """
    name = 'PublishedTwiceWithStaleVersion'
    if rotate_keys is not None:
        name += '_' + rotate_keys

    fixture = FixtureBuilder(name, base_dir)

    fixture.set_expiration("root")   

    fixture.publish(with_client=True)
    
    shutil.copyfile(os.path.join(base_dir, name, "server/metadata/", "1.root.json"),
       os.path.join(base_dir, name, "server/metadata/", "2.root.json"))