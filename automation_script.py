import boto3
import time
import json

# AWS Configuration Settings
AWS_REGION = "us-east-1"
SNS_TOPIC_NAME_SCALING = "ScalingEventsTopic"
SNS_TOPIC_NAME_HEALTH = "HealthEventsTopic"
LAMBDA_FUNCTION_NAME = "MySNSLambdaFunction"
SNS_EMAIL = "manjyotsinghchaudhary@gmail.com"  # Enter your email

# Initialize clients for different AWS services
ec2_client = boto3.client('ec2', region_name=AWS_REGION)
sns_client = boto3.client('sns', region_name=AWS_REGION)
elb_client = boto3.client('elbv2', region_name=AWS_REGION)
asg_client = boto3.client('autoscaling', region_name=AWS_REGION)
cloudwatch_client = boto3.client('cloudwatch', region_name=AWS_REGION)
lambda_client = boto3.client('lambda', region_name=AWS_REGION)
iam_client = boto3.client('iam', region_name=AWS_REGION)

# Function to create an S3 bucket
def create_s3_bucket(bucket_name):
    try:
        s3_client = boto3.client('s3', region_name=AWS_REGION)
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Successfully created S3 Bucket: '{bucket_name}'!")
    except Exception as e:
        print(f"Failed to create S3 bucket: {e}")

# Function to launch an EC2 instance
def launch_ec2_instance():
    try:
        response = ec2_client.run_instances(
            ImageId='ami-0047ab179aa1f984f',  # Replace with valid AMI ID
            InstanceType='t3.micro',
            MinCount=1,
            MaxCount=1,
            KeyName='MAnjyotKeyPair',
            SecurityGroupIds=['sg-06572b9fb25c29db9'],  # Update with a valid security group
            SubnetId='subnet-01874c4512136bd62',  # Update with valid subnet ID
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'WebServer'}]
            }]
        )
        instance_id = response['Instances'][0]['InstanceId']
        print(f"EC2 Instance launched with ID: {instance_id}")
        return instance_id
    except Exception as e:
        print(f"Error launching EC2 instance: {e}")
        return None

# Function to create an Application Load Balancer
def create_alb():
    try:
        response = elb_client.create_load_balancer(
            Name='my-app-alb',
            Subnets=['subnet-01874c4512136bd62','subnet-08fa616f96d54dfc2'],  # Update with valid subnets
            SecurityGroups=['sg-06572b9fb25c29db9'],  # Use valid security group ID
            Scheme='internet-facing',
            Tags=[{'Key': 'Name', 'Value': 'my-app-alb'}],
            Type='application',
            IpAddressType='ipv4'
        )
        alb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
        print(f"ALB successfully created with ARN: {alb_arn}")
        return alb_arn
    except Exception as e:
        print(f"Error creating ALB: {e}")
        return None

# Function to create an Auto Scaling Group (ASG)
def create_auto_scaling_group():
    try:
        response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=['my-auto-scaling-group'])
        if response['AutoScalingGroups']:
            print("Auto Scaling Group already exists. Skipping creation.")
        else:
            response = asg_client.create_auto_scaling_group(
                AutoScalingGroupName='my-auto-scaling-group',
                LaunchConfigurationName='my-launch-configuration',
                MinSize=1,
                MaxSize=3,
                DesiredCapacity=1,
                VPCZoneIdentifier='subnet-01874c4512136bd62',  # Replace with valid subnet
                Tags=[{
                    'Key': 'Name',
                    'Value': 'AutoScalingWebServer',
                    'PropagateAtLaunch': True
                }]
            )
            print("Auto Scaling Group created successfully!")
    except Exception as e:
        print(f"Error creating Auto Scaling Group: {e}")

# Function to create SNS topics and subscriptions
def create_sns_topics():
    try:
        scaling_topic = sns_client.create_topic(Name=SNS_TOPIC_NAME_SCALING)
        health_topic = sns_client.create_topic(Name=SNS_TOPIC_NAME_HEALTH)

        sns_client.subscribe(
            TopicArn=scaling_topic['TopicArn'],
            Protocol='email',
            Endpoint=SNS_EMAIL
        )
        sns_client.subscribe(
            TopicArn=health_topic['TopicArn'],
            Protocol='email',
            Endpoint=SNS_EMAIL
        )
        
        print("SNS topics and email subscriptions are set up!")
        return scaling_topic['TopicArn'], health_topic['TopicArn']
    except Exception as e:
        print(f"Error setting up SNS topics: {e}")
        return None, None

# Function to create the Lambda function
def create_lambda_function():
    try:
        role_name = 'LambdaSNSExecutionRole'
        
        # Check if the Lambda role exists
        try:
            role_response = iam_client.get_role(RoleName=role_name)
            role_arn = role_response['Role']['Arn']  # Get the role ARN
            print(f"Lambda role already exists. Using ARN: {role_arn}")
        except iam_client.exceptions.NoSuchEntityException:
            iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps({
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Action": "sts:AssumeRole",
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "lambda.amazonaws.com"
                        }
                    }]
                })
            )
            # Attach necessary policy to the Lambda role
            iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
            )
            role_arn = f"arn:aws:iam::{AWS_REGION}:role/{role_name}"  # Construct ARN

        lambda_function_code = '''
        import json
        def lambda_handler(event, context):
            print("Event received: " + json.dumps(event))
            return {
                'statusCode': 200,
                'body': json.dumps('SNS Notification Processed Successfully!')
            }
        '''
        # Create the Lambda function
        lambda_client.create_function(
            FunctionName=LAMBDA_FUNCTION_NAME,
            Runtime='python3.8',
            Role=role_arn,  # Use ARN for the role
            Handler='index.lambda_handler',
            Code={'ZipFile': bytes(lambda_function_code, 'utf-8')},
            Timeout=30
        )

        print(f"Lambda function '{LAMBDA_FUNCTION_NAME}' created successfully!")
    except Exception as e:
        print(f"Error creating Lambda function: {e}")

# Function to create CloudWatch alarms
def create_cloudwatch_alarms(scaling_topic_arn):
    try:
        cloudwatch_client.put_metric_alarm(
            AlarmName='ScaleOutAlarm',
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=1,
            MetricName='CPUUtilization',
            Namespace='AWS/EC2',
            Period=300,
            Statistic='Average',
            Threshold=70,
            ActionsEnabled=True,
            AlarmActions=[scaling_topic_arn],
            Dimensions=[{'Name': 'InstanceId', 'Value': 'your-ec2-instance-id'}],
            AlarmDescription='Trigger scaling if CPU exceeds 70%',
            Unit='Percent'
        )

        print("CloudWatch alarms set up successfully!")
    except Exception as e:
        print(f"Error setting up CloudWatch alarms: {e}")

# Function to tear down all infrastructure components
def teardown_infrastructure():
    try:
        # Terminate EC2 instance
        ec2_client.terminate_instances(InstanceIds=['i-022fe87264c5b98ae'])
        print("EC2 instance terminated.")

        # Delete SNS topics
        sns_client.delete_topic(TopicArn=f"arn:aws:sns:{AWS_REGION}:975050024946:{SNS_TOPIC_NAME_SCALING}")
        sns_client.delete_topic(TopicArn=f"arn:aws:sns:{AWS_REGION}:975050024946:{SNS_TOPIC_NAME_HEALTH}")
        print("SNS topics deleted.")

        # Delete Lambda function
        lambda_client.delete_function(FunctionName=LAMBDA_FUNCTION_NAME)
        print("Lambda function deleted.")

        # Delete Auto Scaling Group
        asg_client.delete_auto_scaling_group(AutoScalingGroupName='my-auto-scaling-group', ForceDelete=True)
        print("Auto Scaling Group deleted.")

        # Delete ALB using LoadBalancer ARN
        alb_response = elb_client.describe_load_balancers(Names=['my-app-alb'])
        alb_arn = alb_response['LoadBalancers'][0]['LoadBalancerArn']
        
        # Delete the ALB
        elb_client.delete_load_balancer(LoadBalancerArn=alb_arn)
        print("ALB deleted.")

        print("Infrastructure teardown complete.")
    except Exception as e:
        print(f"Error during teardown: {e}")

# Main deployment function
def deploy_infrastructure():
    # Deploy all components sequentially
    create_s3_bucket("my-app-static-bucket")
    instance_id = launch_ec2_instance()
    alb_arn = create_alb()
    create_auto_scaling_group()
    scaling_topic_arn, health_topic_arn = create_sns_topics()
    create_lambda_function()
    create_cloudwatch_alarms(scaling_topic_arn)

# Execute deployment and teardown processes
if __name__ == "__main__":
    deploy_infrastructure()
    teardown_infrastructure()
