import boto3

# AWS Configuration
AWS_REGION = "us-east-1"
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:975050024946:ScalingEventsTopic"
EC2_INSTANCE_ID = "i-0bb2096a4db8d0f42"  # Your EC2 instance ID

# Initialize Boto3 client
cw_client = boto3.client('cloudwatch', region_name=AWS_REGION)

# Create CloudWatch alarm for Scale-Out event (e.g., CPU > 70)
cw_client.put_metric_alarm(
    AlarmName='ScaleOutAlarm',
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=1,
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Period=300,
    Statistic='Average',
    Threshold=70,
    ActionsEnabled=True,
    AlarmActions=[SNS_TOPIC_ARN],
    Dimensions=[{
        'Name': 'InstanceId',
        'Value': EC2_INSTANCE_ID
    }],
    AlarmDescription='Scale out if CPU > 70%',
    Unit='Percent'
)

# Create CloudWatch alarm for Scale-In event (e.g., CPU < 30)
cw_client.put_metric_alarm(
    AlarmName='ScaleInAlarm',
    ComparisonOperator='LessThanThreshold',
    EvaluationPeriods=1,
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Period=300,
    Statistic='Average',
    Threshold=30,
    ActionsEnabled=True,
    AlarmActions=[SNS_TOPIC_ARN],
    Dimensions=[{
        'Name': 'InstanceId',
        'Value': EC2_INSTANCE_ID
    }],
    AlarmDescription='Scale in if CPU < 30%',
    Unit='Percent'
)

print("CloudWatch alarms created successfully!")