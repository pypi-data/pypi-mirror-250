import time
import json
import boto3
import hashlib
import logging

from airflow.providers.amazon.aws.hooks.base_aws import AwsGenericHook as AwsHook
from airflow.providers.amazon.aws.waiters.base_waiter import BaseBotoWaiter

def get_task_definition(aws_conn_id, args, region = None, **context):
    """
    Get ECS task definition by identifier.

    :param aws_conn_id: AWS connection ID
    :type aws_conn_id: str
    :param identifier: ECS task definition identifier
    :type identifier: str
    :return: ECS task definition
    :rtype: dict
    """
    hook = AwsHook(aws_conn_id, client_type='ecs', region_name=region)
    client = hook.get_client_type()

    task_definitions = client.list_task_definitions(**args)

    if len(task_definitions['taskDefinitionArns']) > 0:
        task_definition_arn = task_definitions['taskDefinitionArns'][0]
        task_definition = client.describe_task_definition(
            taskDefinition=task_definition_arn
        )
        return task_definition['taskDefinition']
    else:
        return None
    
def get_task_definitions(aws_conn_id, args, region = None, **context):
    """
    Get ECS task definitions by familyPrefix.

    :param aws_conn_id: AWS connection ID
    :type aws_conn_id: str
    :param args: ECS task definition arguments
    :type args: dict
    :return: ECS task definition arns
    :rtype: list
    """

    hook = AwsHook(aws_conn_id, client_type='ecs', region_name=region)
    client = hook.get_client_type()

    task_definitions = client.list_task_definitions(**args)

    return task_definitions['taskDefinitionArns']
    
    
def register_task_definition(aws_conn_id, args, overrides = None, region = None, **context):
    """
    Register ECS task definition.

    :param aws_conn_id: AWS connection ID
    :type aws_conn_id: str
    :param args: ECS task definition arguments
    :type args: dict
    :return: ECS task definition
    :rtype: dict
    """
    hook = AwsHook(aws_conn_id, client_type='ecs', region_name=region)
    client = hook.get_client_type()

    args['cpu'] = str(args['cpu']) if 'cpu' in args else None
    args['memory'] = str(args['memory']) if 'memory' in args else None

    if overrides:
        if 'logConfiguration' in overrides:
            for container in args['containerDefinitions']:
                container['logConfiguration'] = overrides['logConfiguration']

    task_definition = client.register_task_definition(**args)

    return task_definition['taskDefinition']

def deregister_task_definition(aws_conn_id, args, region = None, **context):
    """
    Deregister ECS task definition.

    :param aws_conn_id: AWS connection ID
    :type aws_conn_id: str
    :param identifier: ECS task definition identifier
    :type identifier: str
    :return: ECS task definition
    :rtype: dict
    """
    hook = AwsHook(aws_conn_id, client_type='ecs', region_name=region)
    client = hook.get_client_type()

    task_definition = client.deregister_task_definition(**args)

    return task_definition['taskDefinition']

def deregister_task_definitions(aws_conn_id, args, region = None, **context):
    """
    Deregister ECS task definitions.

    :param aws_conn_id: AWS connection ID
    :type aws_conn_id: str
    :param identifier: ECS task definition identifier
    :type identifier: str
    :return: ECS task definition
    :rtype: dict
    """
    hook = AwsHook(aws_conn_id, client_type='ecs', region_name=region)
    client = hook.get_client_type()

    for task_definition in args['taskDefinitions']:
        client.deregister_task_definition(taskDefinition=task_definition)

    return args['taskDefinitions']

def delete_task_definitions(aws_conn_id, args, region = None, **context):
    """
    Delete ECS task definitions.

    :param aws_conn_id: AWS connection ID
    :type aws_conn_id: str
    :param identifier: ECS task definition identifier
    :type identifier: str
    :return: ECS task definition
    :rtype: dict
    """
    hook = AwsHook(aws_conn_id, client_type='ecs', region_name=region)
    client = hook.get_client_type()

    task_definition = client.delete_task_definitions(**args)
    return task_definition