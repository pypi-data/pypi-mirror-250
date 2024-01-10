import time
import json
import boto3
import hashlib
import logging

from airflow.providers.amazon.aws.hooks.base_aws import AwsGenericHook as AwsHook
from airflow.providers.amazon.aws.waiters.base_waiter import BaseBotoWaiter


def get_efs_filesystem(aws_conn_id, identifier, region = None, **context):
    """
    Get EFS filesystem by identifier.

    :param aws_conn_id: AWS connection ID
    :type aws_conn_id: str
    :param identifier: EFS filesystem identifier
    :type identifier: str
    :return: EFS filesystem
    :rtype: dict
    """
    hook = AwsHook(aws_conn_id, client_type='efs', region_name=region)
    client = hook.get_client_type()

    filesystems = client.describe_file_systems(
        CreationToken=str(identifier)
    )

    if len(filesystems['FileSystems']) > 0:
        return filesystems['FileSystems'][0]
    else:
        return None
    
def create_efs_filesystem(aws_conn_id, identifier, args, region = None, **context):
    """
    Create EFS filesystem by identifier.

    :param aws_conn_id: AWS connection ID
    :type aws_conn_id: str
    :param identifier: EFS filesystem identifier
    :type identifier: str
    :param subnets: Subnets to create mount targets in
    :type subnets: list
    :param security_groups: Security groups to assign to mount targets
    :type security_groups: list
    :return: EFS filesystem
    :rtype: dict
    """

    hook = AwsHook(aws_conn_id, client_type='efs', region_name=region)
    client = hook.get_client_type()

    filesystems = client.describe_file_systems(
        CreationToken=str(identifier)
    )

    if len(filesystems['FileSystems']) > 0:
        filesystem = filesystems['FileSystems'][0]
        logging.info('Filesystem already exists: %s', filesystem)
    else:
        logging.info('Filesystem does not exist yet, creating...')
        filesystem = client.create_file_system(CreationToken=str(identifier), **args)
        logging.info('Filesystem created: %s', filesystem)

        waiter_config = {
            "version": 2,
            "waiters": {
                "EFSLifeCycleStateWaiter": {
                    "operation": "DescribeFileSystems",
                    "delay": 5,
                    "maxAttempts": 5,
                    "acceptors": [
                        {
                            "state": "success",
                            "matcher": "path",
                            "argument": f"length(FileSystems[?FileSystemId == '{filesystem['FileSystemId']}'] | [?"
                                            f"LifeCycleState == 'available'"
                                        "]) > `0`",
                            "expected": True
                        }
                    ]
                }
            }
        }
        base_waiter = BaseBotoWaiter(client, waiter_config)
        waiter = base_waiter.waiter('EFSLifeCycleStateWaiter')
        waiter.wait()

        logging.info('Filesystem available: %s', filesystem)

    return filesystem

def delete_efs_filesystem(aws_conn_id, identifier, region = None, **context):
    """
    Delete EFS filesystem by identifier.

    :param aws_conn_id: AWS connection ID
    :type aws_conn_id: str
    :param identifier: EFS filesystem identifier
    :type identifier: str
    :return: EFS filesystem
    :rtype: dict
    """

    hook = AwsHook(aws_conn_id, client_type='efs', region_name=region)
    client = hook.get_client_type()

    filesystems = client.describe_file_systems(
        CreationToken=str(identifier)
    )

    if len(filesystems['FileSystems']) > 0:
        filesystem = filesystems['FileSystems'][0]
        logging.info('Filesystem exists: %s', filesystem)
        client.delete_file_system(FileSystemId=filesystem['FileSystemId'])
        logging.info('Filesystem deleted: %s', filesystem)
    else:
        logging.info('Filesystem does not exist: %s', identifier)
        return None

    return filesystems

def create_mount_targets(aws_conn_id, identifier, subnets, security_groups, region = None, **context):
    """
    Create EFS mount targets by identifier.

    :param aws_conn_id: AWS connection ID
    :type aws_conn_id: str
    :param identifier: EFS filesystem identifier
    :type identifier: str
    :param subnets: Subnets to create mount targets in
    :type subnets: list
    :param security_groups: Security groups to assign to mount targets
    :type security_groups: list
    :return: EFS filesystem
    :rtype: dict
    """

    hook = AwsHook(aws_conn_id, client_type='efs', region_name=region)
    client = hook.get_client_type()

    filesystems = client.describe_file_systems(
        CreationToken=str(identifier)
    )

    if len(filesystems['FileSystems']) > 0:
        filesystem = filesystems['FileSystems'][0]
        logging.info('Filesystem exists: %s', filesystem)
    else:
        logging.info('Filesystem does not exist: %s', identifier)
        return None

    mount_targets = client.describe_mount_targets(
        FileSystemId=filesystem['FileSystemId']
    )

    # For each subnets, check if mount target exists and update security group if required
    for subnet in subnets:
        mount_target = next((x for x in mount_targets['MountTargets'] if x['SubnetId'] == subnet), None)

        if mount_target is not None:
            logging.info('Mount target already exists: %s', mount_target)
        else:
            logging.info('Mount target does not exist yet, creating...')
            mount_target = client.create_mount_target(FileSystemId=filesystem['FileSystemId'], SubnetId=subnet, SecurityGroups=security_groups)
            logging.info('Mount target created: %s', mount_target)

            waiter_config = {
                "version": 2,
                "waiters": {
                    "EFSMountTargetLifeCycleStateWaiter": {
                        "operation": "DescribeMountTargets",
                        "delay": 30,
                        "maxAttempts": 10,
                        "acceptors": [
                            {
                                "state": "success",
                                "matcher": "path",
                                "argument": f"length(MountTargets[?MountTargetId == '{mount_target['MountTargetId']}'] | [?"
                                                f"LifeCycleState == 'available'"
                                            "]) > `0`",
                                "expected": True
                            }
                        ]
                    }
                }
            }
            base_waiter = BaseBotoWaiter(client, waiter_config)
            waiter = base_waiter.waiter('EFSMountTargetLifeCycleStateWaiter')
            waiter.wait(MountTargetId=mount_target['MountTargetId'])

            logging.info('Mount target available: %s', mount_target)

            mount_targets = client.describe_mount_targets(
                FileSystemId=filesystem['FileSystemId']
            )

    return mount_targets

def delete_mount_targets(aws_conn_id, identifier, region = None, **context):
    """
    Delete EFS mount targets by identifier.

    :param aws_conn_id: AWS connection ID
    :type aws_conn_id: str
    :param identifier: EFS filesystem identifier
    :type identifier: str
    :return: EFS filesystem
    :rtype: dict
    """

    hook = AwsHook(aws_conn_id, client_type='efs', region_name=region)
    client = hook.get_client_type()

    filesystems = client.describe_file_systems(
        CreationToken=str(identifier)
    )

    if len(filesystems['FileSystems']) > 0:
        filesystem = filesystems['FileSystems'][0]
        logging.info('Filesystem exists: %s', filesystem)
    else:
        logging.info('Filesystem does not exist: %s', identifier)
        return None

    mount_targets = client.describe_mount_targets(
        FileSystemId=filesystem['FileSystemId']
    )

    # For each mount target, check if mount target exists and update security group if required
    for mount_target in mount_targets['MountTargets']:
        logging.info('Mount target exists: %s', mount_target)
        client.delete_mount_target(MountTargetId=mount_target['MountTargetId'])
        logging.info('Mount target deleted: %s', mount_target)

    waiter_config = {
        "version": 2,
        "waiters": {
            "EFSMountTargetLifeCycleStateWaiter": {
                "operation": "DescribeFileSystems",
                "delay": 30,
                "maxAttempts": 10 * len(mount_targets),
                "acceptors": [
                    {
                        "state": "success",
                        "matcher": "path",
                        "argument": f"length(FileSystems[?FileSystemId == '{filesystem['FileSystemId']}'] | [?"
                                        f"NumberOfMountTargets == `0`"
                                    "]) > `0`",
                        "expected": True
                    }
                ]
            }
        }
    }
    base_waiter = BaseBotoWaiter(client, waiter_config)
    waiter = base_waiter.waiter('EFSMountTargetLifeCycleStateWaiter')
    waiter.wait()

    return mount_targets


def put_efs_filesystem_policy(aws_conn_id, identifier, policy, region = None, **context):
    """
    Put EFS filesystem policy by identifier.

    :param aws_conn_id: AWS connection ID
    :type aws_conn_id: str
    :param identifier: EFS filesystem identifier
    :type identifier: str
    :param policy: EFS filesystem policy
    :type policy: str
    :return: EFS filesystem
    :rtype: dict
    """

    hook = AwsHook(aws_conn_id, client_type='efs', region_name=region)
    client = hook.get_client_type()

    filesystems = client.describe_file_systems(
        CreationToken=str(identifier)
    )

    if len(filesystems['FileSystems']) > 0:
        filesystem = filesystems['FileSystems'][0]
        logging.info('Filesystem exists: %s', filesystem)
    else:
        logging.info('Filesystem does not exist: %s', identifier)
        return None
    
    policy_string = json.dumps(policy)
    client.put_file_system_policy(FileSystemId=filesystem['FileSystemId'], Policy=policy_string)

    return filesystem