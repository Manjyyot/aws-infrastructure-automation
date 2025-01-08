import boto3
import json
import time

# AWS Configuration
AWS_REGION = "us-east-1"
SNS_TOPIC_NAME_SCALING = "ScalingEventsTopic"
SNS_TOPIC_NAME_HEALTH = "HealthEventsTopic"
LAMBDA_FUNCTION_NAME = "MySNSLambdaFunction"
SNS_EMAIL = "manjyotsinghchaudhary@gmail.com"  # Email to receive notifications (for SNS)

# S3 Bucket name (make sure to create an S3 bucket and upload the Lambda function code)
S3_BUCKET_NAME = "my-lambda-functions-bucket"
LAMBDA_FUNCTION_KEY = "lambda_code/my_lambda_function.zip"  # S3 object key for the Lambda ZIP file

# Initialize Boto3 clients
sns_client = boto3.client('sns', region_name=AWS_REGION)
lambda_client = boto3.client('lambda', region_name=AWS_REGION)
iam_client = boto3.client('iam', region_name=AWS_REGION)
s3_client = boto3.client('s3', region_name=AWS_REGION)

def create_sns_topic(topic_name):
    """Create an SNS topic."""
    try:
        response = sns_client.create_topic(Name=topic_name)
        print(f"SNS Topic {topic_name} created successfully!")
        return response['TopicArn']
    except Exception as e:
        print(f"Error creating SNS topic: {e}")
        return None

def subscribe_to_sns_topic(topic_arn, protocol, endpoint):
    """Subscribe to an SNS topic."""
    try:
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint
        )
        print(f"Subscribed to SNS topic {topic_arn} with {protocol} at {endpoint}.")
    except Exception as e:
        print(f"Error subscribing to SNS topic: {e}")

def create_lambda_execution_role():
    """Create Lambda execution role if it doesn't exist."""
    try:
        role_name = "LambdaSNSExecution"
        existing_role = iam_client.get_role(RoleName=role_name)
        print(f"Lambda role already exists: {existing_role['Role']['Arn']}")
        return existing_role['Role']['Arn']
    except iam_client.exceptions.NoSuchEntityException:
        # Role does not exist, create it
        role_policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "sns:Publish",
                        "sns:Subscribe"
                    ],
                    "Resource": "*"
                }
            ]
        }
        response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "lambda.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            })
        )

        # Attach the policy to the role
        iam_client.put_role_policy(
            RoleName=role_name,
            PolicyName="LambdaSNSPolicy",
            PolicyDocument=json.dumps(role_policy_document)
        )

        role_arn = response['Role']['Arn']
        print(f"Lambda role created: {role_arn}")
        return role_arn

def upload_lambda_code_to_s3():
    """Upload the Lambda function code (ZIP) to S3."""
    lambda_function_code = """
    import json
    import boto3

    def lambda_handler(event, context):
        sns = boto3.client('sns')
        message = "SNS notification received: " + json.dumps(event)
        sns.publish(
            TopicArn="arn:aws:sns:us-east-1:975050024946:ScalingEventsTopic",
            Message=message,
            Subject="Scaling Event Notification"
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Notification sent!')
        }
    """
    zip_file_name = '/tmp/my_lambda_function.zip'
    # Writing the function code to a zip file
    with open(zip_file_name, 'w') as zip_file:
        zip_file.write(lambda_function_code)
    
    # Use boto3 to upload the file to S3
    try:
        s3_client.upload_file(zip_file_name, S3_BUCKET_NAME, LAMBDA_FUNCTION_KEY)
        print(f"Lambda function code uploaded to S3 at {S3_BUCKET_NAME}/{LAMBDA_FUNCTION_KEY}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return False
    return True

def create_lambda_function(role_arn):
    """Create Lambda function for SNS notifications."""
    try:
        # Create Lambda function from the S3 bucket reference
        response = lambda_client.create_function(
            FunctionName=LAMBDA_FUNCTION_NAME,
            Runtime='python3.8',
            Role=role_arn,
            Handler='index.lambda_handler',
            Code={
                'S3Bucket': S3_BUCKET_NAME,
                'S3Key': LAMBDA_FUNCTION_KEY
            },
            Timeout=60,
            MemorySize=128
        )
        print(f"Lambda function {LAMBDA_FUNCTION_NAME} created successfully!")
        return response['FunctionArn']
    except Exception as e:
        print(f"Error creating Lambda function: {e}")
        return None

def main():
    # Step 1: Create SNS topics for scaling events and health alerts
    scaling_topic_arn = create_sns_topic(SNS_TOPIC_NAME_SCALING)
    if scaling_topic_arn:
        subscribe_to_sns_topic(scaling_topic_arn, 'email', SNS_EMAIL)  # Subscribe for email notifications

    health_topic_arn = create_sns_topic(SNS_TOPIC_NAME_HEALTH)
    if health_topic_arn:
        subscribe_to_sns_topic(health_topic_arn, 'email', SNS_EMAIL)  # Subscribe for health issue notifications
    
    # Step 2: Upload Lambda function code to S3
    if upload_lambda_code_to_s3():
        # Step 3: Create Lambda execution role if needed
        role_arn = create_lambda_execution_role()
        
        # Step 4: Create Lambda function to handle notifications
        if role_arn:
            create_lambda_function(role_arn)

    # Step 5: Set up CloudWatch Alarms for scaling policies to trigger SNS notifications
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
        AlarmActions=[scaling_topic_arn],  # SNS topic ARN to notify when alarm triggers
        Dimensions=[{
            'Name': 'InstanceId',
            'Value': 'i-0bb2096a4db8d0f42'  # Your EC2 instance ID
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
        AlarmActions=[scaling_topic_arn],  # SNS topic ARN to notify when alarm triggers
        Dimensions=[{
            'Name': 'InstanceId',
            'Value': 'i-0bb2096a4db8d0f42'  # Your EC2 instance ID
        }],
        AlarmDescription='Scale in if CPU < 30%',
        Unit='Percent'
    )

    print("CloudWatch alarms created successfully!")

if __name__ == "__main__":
    main()