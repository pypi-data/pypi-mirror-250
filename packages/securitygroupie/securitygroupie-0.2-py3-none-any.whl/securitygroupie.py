import boto3
import botocore
import logging
import datetime
import argparse
from botocore.exceptions import ClientError

from models import SecurityGroup

logging.basicConfig(filename="securitygroupie-log-"
                    + (datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
                    + ".log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.WARN)


def get_current_account() -> str:
    sts_client = boto3.client("sts")
    response = sts_client.get_caller_identity()
    return response.get("Account")


def get_regions() -> list:
    """
    Returns of AWS regions
    Inputs:
        None
    Returns:
        [
            {
                'Endpoint': 'string',
                'RegionName': 'string',
                'OptInStatus': 'string'
            },
        ]
    """

    ec2 = boto3.client("ec2")
    regions_raw = ec2.describe_regions(
        AllRegions=False
    )["Regions"]
    for i in regions_raw:
        yield i.get("RegionName")


def iter_network_interfaces(ec2_client: botocore.client, region: str) -> list:
    """
    Returns elastic network interfaces in a region
    Inputs:
        session = boto3 client object
        region = string
    Returns:
    [
        {
            'Association': {
                'AllocationId': 'string',
                'AssociationId': 'string',
                'IpOwnerId': 'string',
                'PublicDnsName': 'string',
                'PublicIp': 'string',
                'CustomerOwnedIp': 'string',
                'CarrierIp': 'string'
            },
            'NetworkInterfaceId': 'string',
            ...,
},
    ]
    """

    next_token = "X"
    network_interfaces = []
    try:
        while next_token is not None:
            if next_token == "X":
                response = ec2_client.describe_network_interfaces()
            else:
                response = ec2_client.describe_network_interace(
                    NextToken=next_token
                )
            next_token = response.get("NextToken")
            for i in response.get("NetworkInterfaces"):
                network_interfaces.append(i)
        for network_interface in network_interfaces:
            yield network_interface
    except ClientError as e:
        if e.response['Error']['Code'] == 'UnauthorizedOperation':
            logging.warning(f"Unable to access AWS region {region}")
            return None
    return None


def iter_security_groups(ec2_client: botocore.client, region: str) -> list:
    """
    Returns security groups in a region

    Inputs:
        session = boto3 client object
        region = string
    Returns:
{
    'SecurityGroups': [
        {
            'Description': 'string',
            'GroupName': 'string',
            'IpPermissions': ...
            'OwnerId': 'string',
            'GroupId': 'string',
            ...
    """
    security_groups = []
    response = ""
    next_token = "X"
    try:
        while next_token is not None:
            if next_token == "X":
                response = ec2_client.describe_security_groups()
            else:
                response = ec2_client.describe_security_groups(
                    NextToken=next_token
                )
            next_token = response.get("NextToken")
            for security_group in response.get("SecurityGroups"):
                security_groups.append(security_group)
        for security_group in security_groups:
            yield security_group
    except ClientError as e:
        if e.response['Error']['Code'] == 'UnauthorizedOperation':
            logging.warning(f"Unable to access AWS region {region}")
            return None
    return None


def lookup_attachment(ec2_client: botocore.client,
                      region: str,
                      network_interface_id: str) -> str:
    """
    Returns the name of the EC2 instance a network
    interface is attached to or None if there is
    no attachment or no tag

    Inputs:
        session = boto3 client object
        region = string
        network_interface_id = string
    Returns:
        str
    """
    try:
        response = ec2_client.describe_network_interface_attribute(
            Attribute='attachment',
            NetworkInterfaceId=network_interface_id
        )
        if response.get("Attachment"):
            instance_id = response.get("Attachment").get("InstanceId")
            if response.get("Attachment").get("Status") == "attached" and instance_id:  # noqa: E501
                response2 = ec2_client.describe_tags(
                    Filters=[
                        {
                            "Name": "key",
                            "Values": ["Name"]
                        },
                        {
                            "Name": "resource-id",
                            "Values": [response.get("Attachment").get("InstanceId")]  # noqa: E501
                        }
                    ]
                )
                try:
                    return response2.get("Tags")[0].get("Value")
                except IndexError:
                    return None
            else:
                return None
    except ClientError as e:
        if e.response['Error']['Code'] == 'UnauthorizedOperation':
            logging.warning(f"Unable to access AWS region {region}")
            return None
    return None


def output_lookup(account_id: str, security_group: SecurityGroup) -> None:
    print(f"Account: {account_id}")
    print(f"Region: {security_group.get_region_name()}")
    print(f"Security Group Id: {security_group.get_security_group_id()}")
    print(f"Security Group Name: {security_group.get_security_group_name()}")
    print(f"Attached resources: {security_group.get_attached_resources()}")


def output_csv(account_id: str, security_groups: dict) -> None:
    """"
    Outputs CSV to standard out

    Inputs:
        account_id = str
        security_groups = list of Security Group
    Outputs:
        None
    """
    print("Account Id,Region,Security Group Id,"
          "Security Group Name,Attached Resources")
    for sg_key in security_groups.keys():
        attached_resources = None
        if security_groups.get(sg_key).get_attached_resources():
            attached_resources = ' '.join(
                (security_groups.get(sg_key).get_attached_resources()))
        print(f"{account_id},"
              f"{security_groups.get(sg_key).get_region_name()},"
              f"{security_groups.get(sg_key).get_security_group_id()},"
              f"{security_groups.get(sg_key).get_security_group_name()},"
              f"{attached_resources}")


def main(args):
    security_groups = {}
    account_id = get_current_account()
    for region in get_regions():
        ec2_client = boto3.client("ec2", region_name=region)
        for security_group in iter_security_groups(ec2_client, region):
            sg = SecurityGroup.SecurityGroup(
                security_group_id=security_group.get("GroupId"))
            sg.set_security_group_name(security_group.get("GroupName"))
            sg.set_region_name(region)
            security_groups[security_group.get("GroupId")] = sg
        for network_interface in iter_network_interfaces(ec2_client, region):
            for network_interface_sg in network_interface.get("Groups"):
                for sg_key in security_groups.keys():
                    if sg_key == network_interface_sg.get("GroupId"):
                        network_interface_id = network_interface.get(
                                "NetworkInterfaceId")
                        resource_name = lookup_attachment(ec2_client,
                                                          region,
                                                          network_interface_id)
                        if resource_name is not None:
                            security_groups.get(sg_key).add_attached_resource(
                                resource_name)
                        else:
                            security_groups.get(sg_key).add_attached_resource(
                                resource_id=network_interface_id)
    if args.lookup:
        output_lookup(account_id, security_groups.get(args.lookup))
    else:
        output_csv(account_id, security_groups)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='securitygroupie',
                    description='Display security groups and their resources')
    parser.add_argument("-l", "--lookup",
                        help="Display a specific resource")
    args = parser.parse_args()
    main(args)
