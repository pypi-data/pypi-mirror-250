import time
import json
import boto3
import hashlib
import logging

from airflow.providers.amazon.aws.hooks.base_aws import AwsGenericHook as AwsHook

def get_subnets(aws_conn_id, region, filters = [], **context):
    """
    Returns a list of subnet ids based on the filters provided.

    :param aws_conn_id: AWS connection ID
    :type aws_conn_id: str
    :param region: AWS region name
    :type region: str
    :param filters: Filters to apply when searching for subnets
    :type filters: list
    :return: List of subnet ids
    :rtype: list

    Example filters:
    filters = [
        {
            'Name': 'tag:Name',
            'Values': ['subnet-1', 'subnet-2']  
        }
    ]
    """
    
    hook = AwsHook(aws_conn_id, client_type='ec2', region_name=region)
    client = hook.get_client_type()

    response = client.describe_subnets(Filters=filters)
    return [subnet['SubnetId'] for subnet in response['Subnets']]

def get_security_groups(aws_conn_id, region, filters = [], **context):
    """
    Returns a list of security group ids based on the filters provided.
    
    :param aws_conn_id: AWS connection ID
    :type aws_conn_id: str
    :param region: AWS region name
    :type region: str
    :param filters: Filters to apply when searching for security groups
    :type filters: list
    :return: List of security group ids
    :rtype: list

    Example filters:
    filters = [
        {
            'Name': 'tag:Name',
            'Values': ['security-group-1', 'security-group-2']
        }
    ]
    """

    hook = AwsHook(aws_conn_id, client_type='ec2', region_name=region)
    client = hook.get_client_type()

    response = client.describe_security_groups(Filters=filters)
    return [security_group['GroupId'] for security_group in response['SecurityGroups']]