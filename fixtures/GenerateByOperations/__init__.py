from fixtures.builder import FixtureBuilder
import os
import time
from tuf import formats
from datetime import datetime, timedelta
import json
import shutil

def getPublishRounds(operations):
        c = 0
        for op in operations:
            if op.action == "publish" or op.action == "publish_with_client":
                c += 1
        return c

def generateName(operations):
    name = 'Published'+str(getPublishRounds(operations))+("Times" if getPublishRounds(operations)>1 else "Time")
    for op in operations:
        if op.tag is not None:
            name += "_" + op.tag
    return name

def build(operations=[], base_dir=os.path.dirname(__file__), tag=None):
    """
    Generates a TUF test fixture followsing the operations.
    """
    #testdata/Published1Time
    #testdata/Published2Times_keyrotated_initialrootexpired

    FAST_EXPIRATION = 10 
    EXPIRED = formats.unix_timestamp_to_datetime(int(time.time())+FAST_EXPIRATION)
    LONG_EXPIRATION = datetime.now() + timedelta(days=365*10) # expire in 10 years from now.
 
    currentVersion = 0
    name = generateName(operations)
    fixture = FixtureBuilder(name, base_dir)   
    for i in range(len(operations)):
        op = operations[i]
        if op.action == "tag":
            continue
        if op.action == "add_key":
            fixture.add_key(op.subject)
        elif op.action == "revoke_key":
            fixture.revoke_key(op.subject, key_index=0)
        elif op.action == "set_expired":
            fixture.set_expiration(op.subject, EXPIRED)
        elif op.action == "set_long_expiring":
            fixture.set_expiration(op.subject, LONG_EXPIRATION)
        elif op.action == "publish":
            fixture.publish()
            currentVersion += 1
        elif op.action == "publish_with_client":
            fixture.publish(with_client=True)
            currentVersion += 1
        elif op.action == "copy":
            dest = os.path.join(base_dir, name, "server/metadata/", op.subject)
            source = os.path.join(base_dir, name, "server/metadata/", str(currentVersion)+"."+".".join(op.subject.split(".")[1:]))
            shutil.move(source, dest)
        elif op.action == "set_signature":
            root_json = None
            role = op.subject.split(".")[0]
            file_path = os.path.join(base_dir, name, "server/metadata/", str(currentVersion)+"."+role+".json")
            with open(file_path, "r") as root_json_file:
               root_json = json.load(root_json_file)
            field = None
            for r in op.subject.split(".")[1:-1]:
                r = int(r) if r.isnumeric() else r
                field = root_json[r] if field is None else field[r]
            lastr = op.subject.split(".")[-1]
            lastr = int(lastr) if lastr.isnumeric() else lastr
            field[lastr] = op.value
            with  open(os.path.join(file_path), "wb") as root_json_file_for_write:
               root_json_file_for_write.write(json.dumps(root_json, indent=1,
               separators=(',', ': '), sort_keys=True).encode('utf-8'))