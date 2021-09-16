# For instructions on using this script, please see the README.

from datetime import datetime, timedelta
from fixtures.builder import Operation
from unittest import mock
import shutil
import glob
import os
import time
from tuf import formats

FIXTURE_OUTPUT_DIR = "./generated_fixtures"

from fixtures import (
    TUFTestFixtureSimple,
    TUFTestFixtureAttackRollback,
    TUFTestFixtureDelegated,
    TUFTestFixtureNestedDelegated,
    TUFTestFixtureUnsupportedDelegation,
    TUFTestFixtureNestedDelegatedErrors,
    TUFTestFixtureThresholdTwo,
    TUFTestFixtureThresholdTwoAttack,
    TUFTestFixtureTerminatingDelegation,
    TUFTestFixtureTopLevelTerminating,
    TUFTestFixtureNestedTerminatingNonDelegatingDelegation,
    TUFTestFixture3LevelDelegation,
    PublishedNTimes,
    PublishedTwice,
    PublishedTwiceWithStaleVersion,
    PublishedTwiceInvalidNewRootSignature,
    PublishedTwiceInvalidOldRootSignature,
    PublishedTwiceForwardVersion,
    PublishedTwiceMultiKeys,
    GenerateByOperations
)

@mock.patch('time.time', mock.MagicMock(return_value=1577836800))
def generate_fixtures_mocked_time():

    FAST_EXPIRATION = 10 
    EXPIRED_TIME = formats.unix_timestamp_to_datetime(int(time.time())+FAST_EXPIRATION)
    global FIXTURE_OUTPUT_DIR
    TUFTestFixtureSimple.build(FIXTURE_OUTPUT_DIR)
    TUFTestFixtureAttackRollback.build(FIXTURE_OUTPUT_DIR)
    TUFTestFixtureDelegated.build(FIXTURE_OUTPUT_DIR)
    TUFTestFixtureNestedDelegated.build(FIXTURE_OUTPUT_DIR)
    TUFTestFixtureUnsupportedDelegation.build(FIXTURE_OUTPUT_DIR)
    TUFTestFixtureNestedDelegatedErrors.build(FIXTURE_OUTPUT_DIR)
    TUFTestFixtureThresholdTwo.build(FIXTURE_OUTPUT_DIR)
    TUFTestFixtureThresholdTwoAttack.build(FIXTURE_OUTPUT_DIR)
    TUFTestFixtureTerminatingDelegation.build(FIXTURE_OUTPUT_DIR)
    TUFTestFixtureTopLevelTerminating.build(FIXTURE_OUTPUT_DIR)
    TUFTestFixtureNestedTerminatingNonDelegatingDelegation.build(FIXTURE_OUTPUT_DIR)
    TUFTestFixture3LevelDelegation.build(FIXTURE_OUTPUT_DIR)

def generate_fixtures():
    FAST_EXPIRATION = formats.unix_timestamp_to_datetime(int(time.time())+10) # 10 seconds from now.
    global FIXTURE_OUTPUT_DIR

    PublishedTwice.build(base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwice.build(rotate_keys='timestamp', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwice.build(rotate_keys='snapshot', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwice.build(rotate_keys='targets', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwice.build(rotate_keys='root', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwice.build(rotate_keys='root', root_expires_start=FAST_EXPIRATION, base_dir=FIXTURE_OUTPUT_DIR, tag="initialrootexpired")
    PublishedTwice.build(rotate_keys='root', root_expires_start=FAST_EXPIRATION, root_expires_end=FAST_EXPIRATION, base_dir=FIXTURE_OUTPUT_DIR, tag="initialandlatestrootexpired")
    PublishedTwiceWithStaleVersion.build(rotate_keys='root', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceForwardVersion.build(rotate_keys='root', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceInvalidNewRootSignature.build(rotate_keys='root', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceInvalidOldRootSignature.build(rotate_keys='root', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceMultiKeys.build(rotate_keys='root', add_key=9 , revoke_key=2, threshold=4, base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceMultiKeys.build(rotate_keys='root', add_key=9 , revoke_key=4, threshold=4, base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceMultiKeys.build(rotate_keys='snapshot', add_key=9 , revoke_key=2, threshold=4, base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceMultiKeys.build(rotate_keys='snapshot', add_key=9 , revoke_key=4, threshold=4, base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceMultiKeys.build(rotate_keys='timestamp', add_key=9 , revoke_key=2, threshold=4, base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceMultiKeys.build(rotate_keys='timestamp', add_key=9 , revoke_key=4, threshold=4, base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceMultiKeys.build(rotate_keys='targets', add_key=9 , revoke_key=2, threshold=4, base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceMultiKeys.build(rotate_keys='targets', add_key=9 , revoke_key=4, threshold=4, base_dir=FIXTURE_OUTPUT_DIR)
    #PublishedNTimes.build(rotate_keys='root', publish_n_times=5, base_dir=FIXTURE_OUTPUT_DIR)
    #PublishedNTimes.build(rotate_keys='root', root_expires_start=FAST_EXPIRATION, publish_n_times=5, base_dir=FIXTURE_OUTPUT_DIR, tag="initialrootexpired")
    #PublishedNTimes.build(rotate_keys='root', root_expires_start=FAST_EXPIRATION, root_expires_end=FAST_EXPIRATION, publish_n_times=5, base_dir=FIXTURE_OUTPUT_DIR, tag="initialandlatestrootexpired")
    # Published1Time
    GenerateByOperations.build(operations=[Operation("set_long_expiring", "root"), Operation("publish_with_client")] , base_dir=FIXTURE_OUTPUT_DIR)
    # Published2Times_keyrotated
    GenerateByOperations.build(operations=[Operation("set_long_expiring", "root"), 
                                           Operation("publish_with_client"),
                                           Operation("add_key", "root"),
                                           Operation("publish"),
                                           Operation("tag", tag="keyrotated")] , base_dir=FIXTURE_OUTPUT_DIR)
    # Published2Times_keyrotated_initialrootexpired
    GenerateByOperations.build(operations=[Operation("set_expired", "root"), 
                                           Operation("publish_with_client"),
                                           Operation("set_long_expiring", "root"),
                                           Operation("add_key", "root"),
                                           Operation("publish"),
                                           Operation("tag", tag="keyrotated_initialrootexpired")] , base_dir=FIXTURE_OUTPUT_DIR)
    # Published3Times_keyrotated_initialrootsexpired
    GenerateByOperations.build(operations=[Operation("set_expired", "root"), 
                                           Operation("publish_with_client"),
                                           Operation("add_key", "root"),
                                           Operation("publish"),
                                           Operation("set_long_expiring", "root"),
                                           Operation("add_key", "root"),
                                           Operation("publish"),
                                           Operation("tag", tag="keyrotated_initialrootsexpired")] , base_dir=FIXTURE_OUTPUT_DIR)
    # Published3Times_keyrotated_initialrootsexpired_clientversionis2
    GenerateByOperations.build(operations=[Operation("set_expired", "root"), 
                                           Operation("publish_with_client"),
                                           Operation("add_key", "root"),
                                           Operation("publish_with_client"),
                                           Operation("set_long_expiring", "root"),
                                           Operation("add_key", "root"),
                                           Operation("publish"),
                                           Operation("tag", tag="keyrotated_initialrootsexpired_clientversionis2")] , base_dir=FIXTURE_OUTPUT_DIR)
    # Published3Times_keyrotated_latestrootexpired
    GenerateByOperations.build(operations=[Operation("set_expired", "root"), 
                                           Operation("publish_with_client"),
                                           Operation("add_key", "root"),
                                           Operation("publish"),
                                           Operation("add_key", "root"),
                                           Operation("publish"),
                                           Operation("tag", tag="keyrotated_latestrootexpired")] , base_dir=FIXTURE_OUTPUT_DIR)
    # Published2Times_keyrotated_invalidOldRootSignature
    GenerateByOperations.build(operations=[Operation("set_long_expiring", "root"),
                                           Operation("publish_with_client"),
                                           Operation("add_key", "root"),
                                           Operation("publish"),
                                           Operation("set_signature", subject="root.signatures.0.sig", value="000000"),
                                           Operation("tag", tag="keyrotated_invalidOldRootSignature")] , base_dir=FIXTURE_OUTPUT_DIR)
    # Published2Times_keyrotated_forwardRootVersion
    GenerateByOperations.build(operations=[Operation("set_long_expiring", "root"),
                                           Operation("publish_with_client"),
                                           Operation("add_key", "root"),
                                           Operation("publish"),
                                           Operation("add_key", "root"),
                                           Operation("publish"),
                                           Operation("copy", "2.root.json"),
                                           Operation("tag", tag="keyrotated_forwardRootVersion")] , base_dir=FIXTURE_OUTPUT_DIR)
    # Published1Time_backwardRootVersion
    GenerateByOperations.build(operations=[
                                           Operation("set_long_expiring", "root"),
                                           Operation("publish_with_client"),
                                           Operation("copy", "2.root.json"),
                                           Operation("tag", tag="backwardRootVersion")] , base_dir=FIXTURE_OUTPUT_DIR)
    # Published2Times_snapshot_keyrotated
    GenerateByOperations.build(operations=[Operation("set_long_expiring", "root"), 
                                           Operation("publish_with_client"),
                                           Operation("add_key", "snapshot"),
                                           Operation("publish"),
                                           Operation("tag", tag="snapshot_keyrotated")] , base_dir=FIXTURE_OUTPUT_DIR)
    # Published2Times_timestamp_keyrotated
    GenerateByOperations.build(operations=[Operation("set_long_expiring", "root"), 
                                           Operation("publish_with_client"),
                                           Operation("add_key", "timestamp"),
                                           Operation("publish"),
                                           Operation("tag", tag="timestamp_keyrotated")] , base_dir=FIXTURE_OUTPUT_DIR)
    # Published2Times_targets_keyrotated
    GenerateByOperations.build(operations=[Operation("set_long_expiring", "root"), 
                                           Operation("publish_with_client"),
                                           Operation("add_key", "targets"),
                                           Operation("publish"),
                                           Operation("tag", tag="targets_keyrotated")] , base_dir=FIXTURE_OUTPUT_DIR)
    
    # Published1Time_client_root_only
    GenerateByOperations.build(operations=[Operation("set_long_expiring", "root"), 
                                            Operation("publish_with_client"),
                                            Operation("delete", "client/metadata/current/*snapshot.json"),
                                            Operation("delete", "client/metadata/current/*timestamp.json"),
                                            Operation("delete", "client/metadata/current/*targets.json"),
                                            Operation("delete", "client/metadata/current/1.root.json"),
                                            Operation("tag", tag="client_root_only")] , base_dir=FIXTURE_OUTPUT_DIR)

    # Published1Time_client_no_root
    GenerateByOperations.build(operations=[Operation("set_long_expiring", "root"), 
                                            Operation("publish_with_client"),
                                            Operation("delete", "client/metadata/current/*root.json"),
                                            Operation("tag", tag="client_no_root")] , base_dir=FIXTURE_OUTPUT_DIR)

# Remove all previous fixtures.
for f in glob.glob("fixtures/*/client"):
    shutil.rmtree(f)
for f in glob.glob("fixtures/*/server"):
    shutil.rmtree(f)
# Delete hash files to ensure they are generated again.
for f in glob.glob("fixtures/*/hash.txt"):
    os.remove(f)
generate_fixtures()
#generate_fixtures_mocked_time()
