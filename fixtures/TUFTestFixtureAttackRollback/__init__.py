from fixtures.builder import FixtureBuilder

import os
import shutil

def build(base_dir=os.path.dirname(__file__)):
    fixture = FixtureBuilder('TUFTestFixtureAttackRollback', base_dir)\
        .create_target('testtarget.txt')\
        .publish(with_client=True)

    server_dir = fixture._server_dir
    backup_dir = server_dir + '_backup'
    shutil.copytree(server_dir, backup_dir, dirs_exist_ok=True)

    fixture.create_target('testtarget2.txt')\
        .publish(with_client=True)
    shutil.rmtree(server_dir + '/')

    # Reset the client to previous state to simulate a rollback attack.
    shutil.copytree(backup_dir, server_dir, dirs_exist_ok=True)
    shutil.rmtree(backup_dir + '/')
