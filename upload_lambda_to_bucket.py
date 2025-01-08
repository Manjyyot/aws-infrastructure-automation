import boto3

# AWS Configuration
AWS_REGION = "us-east-1"
LAMBDA_FUNCTION_NAME = "MySNSLambdaFunction"
S3_BUCKET_NAME = "creating-new-bucket"
LAMBDA_FUNCTION_KEY = "lambda_code/my_lambda_function.zip"
ROLE_ARN = "arn:aws:iam::975050024946:role/LambdaSNSExecutionRole"

# Initialize Boto3 client
lambda_client = boto3.client('lambda', region_name=AWS_REGION)

try:
    response = lambda_client.create_function(
        FunctionName=LAMBDA_FUNCTION_NAME,
        Runtime='python3.8',
        Role=ROLE_ARN,
        Handler='lambda_function.lambda_handler',
        Code={
            'S3Bucket': S3_BUCKET_NAME,
            'S3Key': LAMBDA_FUNCTION_KEY
        },
        Timeout=60,
        MemorySize=128
    )
    print(f"Lambda function {LAMBDA_FUNCTION_NAME} created successfully!")
except Exception as e:
    print(f"Error creating Lambda function: {e}")