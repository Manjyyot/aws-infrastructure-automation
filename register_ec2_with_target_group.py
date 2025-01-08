import boto3

# Initialize boto3 client for Elastic Load Balancing
elbv2_client = boto3.client('elbv2', region_name='us-east-1')

# EC2 Instance ID to register
ec2_instance_id = 'i-0bb2096a4db8d0f42'  # Replace with your EC2 instance ID

# Target Group ARN
target_group_arn = 'arn:aws:elasticloadbalancing:us-east-1:975050024946:targetgroup/my-target-group/5f278aaafd36cd3a'  # Replace with your Target Group ARN

# Register EC2 instance with the target group
response = elbv2_client.register_targets(
    TargetGroupArn=target_group_arn,
    Targets=[{'Id': ec2_instance_id}]  # EC2 Instance ID
)

print(f"EC2 instance {ec2_instance_id} registered with the target group.")