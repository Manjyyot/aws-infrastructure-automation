import boto3

ec2 = boto3.client("ec2", region_name="us-east-1")

vpcs = ec2.describe_vpcs()
for vpc in vpcs["Vpcs"]:
    print(f"VPC ID: {vpc['VpcId']} (Default: {vpc.get('IsDefault', False)})")