# For instructions on using this script, please see the README.

from unittest import mock
import shutil
import glob
import os

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
    PublishedTwice,
    PublishedTwiceWithStaleVersion,
    PublishedTwiceInvalidNewRootSignature,
    PublishedTwiceInvalidOldRootSignature,
    PublishedTwiceRotateTimestampKeys,
    PublishedTwiceForwardVersion
)


@mock.patch('time.time', mock.MagicMock(return_value=1577836800))
def generate_fixtures():
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
    PublishedTwice.build(base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwice.build(rotate_keys='timestamp', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwice.build(rotate_keys='snapshot', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwice.build(rotate_keys='root', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceWithStaleVersion.build(rotate_keys='root', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceInvalidNewRootSignature.build(rotate_keys='root', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceInvalidOldRootSignature.build(rotate_keys='root', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceRotateTimestampKeys.build(rotate_keys='root', base_dir=FIXTURE_OUTPUT_DIR)
    PublishedTwiceForwardVersion.build(rotate_keys='root', base_dir=FIXTURE_OUTPUT_DIR)
 

# Remove all previous fixtures.
for f in glob.glob("fixtures/*/client"):
    shutil.rmtree(f)
for f in glob.glob("fixtures/*/server"):
    shutil.rmtree(f)
# Delete hash files to ensure they are generated again.
for f in glob.glob("fixtures/*/hash.txt"):
    os.remove(f)
generate_fixtures()
