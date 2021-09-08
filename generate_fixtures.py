# For instructions on using this script, please see the README.

from datetime import datetime, timedelta
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
    PublishedTwiceMultiKeys
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
    PublishedNTimes.build(rotate_keys='root', publish_n_times=5, base_dir=FIXTURE_OUTPUT_DIR)
    PublishedNTimes.build(rotate_keys='root', root_expires_start=FAST_EXPIRATION, publish_n_times=5, base_dir=FIXTURE_OUTPUT_DIR, tag="initialrootexpired")
    PublishedNTimes.build(rotate_keys='root', root_expires_start=FAST_EXPIRATION, root_expires_end=FAST_EXPIRATION, publish_n_times=5, base_dir=FIXTURE_OUTPUT_DIR, tag="initialandlatestrootexpired")
 
 

# Remove all previous fixtures.
for f in glob.glob("fixtures/*/client"):
    shutil.rmtree(f)
for f in glob.glob("fixtures/*/server"):
    shutil.rmtree(f)
# Delete hash files to ensure they are generated again.
for f in glob.glob("fixtures/*/hash.txt"):
    os.remove(f)
generate_fixtures()
generate_fixtures_mocked_time()
