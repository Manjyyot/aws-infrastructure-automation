import boto3

# Initialize boto3 client for Elastic Load Balancing
elbv2_client = boto3.client('elbv2', region_name='us-east-1')

# ALB ARN (replace with your ALB ARN)
load_balancer_arn = 'arn:aws:elasticloadbalancing:us-east-1:975050024946:loadbalancer/app/my-application-load-balancer/a6db7bfe889270f6'

# Create Listener for the Load Balancer
response = elbv2_client.create_listener(
    LoadBalancerArn=load_balancer_arn,  # Your ALB ARN
    Protocol='HTTP',  # Protocol to use for incoming traffic
    Port=80,  # Port to listen on
    DefaultActions=[{
        'Type': 'forward',
        'TargetGroupArn': 'arn:aws:elasticloadbalancing:us-east-1:975050024946:targetgroup/my-target-group/5f278aaafd36cd3a'  # Forward traffic to your target group
    }]
)

print("Listener created and attached to ALB.")
