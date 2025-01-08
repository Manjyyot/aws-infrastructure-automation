import json
import boto3

def lambda_handler(event, context):
    sns = boto3.client('sns')
    message = "SNS notification received: " + json.dumps(event)
    sns.publish(
        TopicArn="arn:aws:sns:us-east-1:975050024946:ScalingEventsTopic",  # Replace with your topic ARN
        Message=message,
        Subject="Scaling Event Notification"
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent!')
    }