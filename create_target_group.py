import boto3

# Initialize the Boto3 client for Elastic Load Balancing (ALB)
elbv2_client = boto3.client('elbv2', region_name='us-east-1')  # Update the region if needed

# Step 1: Create a Target Group (If not already created)
response = elbv2_client.create_target_group(
    Name='my-target-group',  # Name of the target group
    Protocol='HTTP',  # Protocol for the target group
    Port=80,  # The port on which the targets (EC2 instances) will receive traffic
    VpcId='vpc-09f02049d6176fe30',  # VPC ID where your EC2 instances are located
    HealthCheckProtocol='HTTP',  # Health check protocol
    HealthCheckPort='80',  # Port for health check
    HealthCheckPath='/health',  # Path for health checks
    Matcher={'HttpCode': '200'},  # HTTP code indicating a healthy instance
)

# Get the Target Group ARN
target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
print("Target Group ARN:", target_group_arn)

# Step 2: Register the EC2 instance with the Target Group
instances = [
    {'Id': 'i-0bb2096a4db8d0f42'},  # EC2 instance ID to register
]

# Register EC2 instance(s) with the target group
register_response = elbv2_client.register_targets(
    TargetGroupArn=target_group_arn,
    Targets=instances
)
print("EC2 instance registered with target group.")

# Step 3: Create a Listener for the ALB
# Replace the Load Balancer ARN with your actual ALB ARN
listener_response = elbv2_client.create_listener(
    LoadBalancerArn='arn:aws:elasticloadbalancing:us-east-1:975050024946:loadbalancer/app/my-application-load-balancer/a6db7bfe889270f6',  # ALB ARN
    Protocol='HTTP',  # The protocol the listener will handle
    Port=80,  # The port the listener will listen on
    DefaultActions=[{
        'Type': 'forward',
        'TargetGroupArn': target_group_arn  # Forward traffic to the created target group
    }]
)

print("Listener created and attached to ALB.")
