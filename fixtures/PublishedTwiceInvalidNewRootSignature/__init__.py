from fixtures.builder import FixtureBuilder
import os
import json

def build(rotate_keys=None, base_dir=os.path.dirname(__file__)):
    """
    Generates a TUF test fixture that publishes twice -- once on the client,
    and twice on the server -- and, in between those two publications, can
    optionally rotate the keys of a given role.
    """
    name = 'PublishedTwiceInvalidNewRootSignature'
    if rotate_keys is not None:
        name += 'WithRotatedKeys_' + rotate_keys

    fixture = FixtureBuilder(name, base_dir).publish(with_client=True)
    if rotate_keys is not None:
        fixture.add_key(rotate_keys)\
            .revoke_key(rotate_keys, key_index=0)
    fixture.publish()
    # Load and modify the file signature.
    root_json_file = open(os.path.join(base_dir, name, "server/metadata/", "2.root.json"), "r")
    root_json = json.load(root_json_file)
    root_json['signatures'][0]['sig'] = "INVALID_SIGNATURE"
    root_json_file.close()
    root_json_file_for_write = open(os.path.join(base_dir, name, "server/metadata/", "2.root.json"), "wb")
    root_json_file_for_write.write(json.dumps(root_json, indent=1,
      separators=(',', ': '), sort_keys=True).encode('utf-8'))