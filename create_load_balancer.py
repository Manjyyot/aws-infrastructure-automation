import boto3
import botocore  # Import botocore for error handling

# Initialize the Boto3 client for Elastic Load Balancing (ALB)
elbv2_client = boto3.client('elbv2', region_name='us-east-1')  # Update with the correct region

try:
    # Create an Application Load Balancer (ALB) with two subnets from different Availability Zones
    response = elbv2_client.create_load_balancer(
        Name='my-application-load-balancer',
        Subnets=['subnet-01874c4512136bd62', 'subnet-08fa616f96d54dfc2'],  # Add the second subnet ID here (ensure it's from a different AZ)
        SecurityGroups=['sg-06572b9fb25c29db9'],  # Your security group ID
        Scheme='internet-facing',  # Exposes the ALB to the public internet
        Type='application',  # Application Load Balancer type
        IpAddressType='ipv4',  # Use IPv4 addresses
        Tags=[
            {'Key': 'Name', 'Value': 'MyALB'}  # Tagging for the ALB
        ]
    )

    # Print the DNS Name of the ALB, which you will use to access the service
    print("ALB DNS Name:", response['LoadBalancers'][0]['DNSName'])

except botocore.exceptions.ClientError as e:
    error_code = e.response['Error']['Code']
    error_message = e.response['Error']['Message']
    print(f"Error Code: {error_code}")
    print(f"Error Message: {error_message}")