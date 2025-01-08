import boto3
import time

# AWS Configuration
AWS_REGION = "us-east-1"  # Replace with your AWS region if needed
AMI_ID = "ami-03007fc8635b05e46"  # Amazon Linux 2 AMI (ensure this AMI is available in your region)
INSTANCE_TYPE = "t3.micro"  # Updated instance type
KEY_PAIR_NAME = "MAnjyotKeyPair"  # Your key pair name (without .pem)
EXISTING_SECURITY_GROUP_ID = "sg-06572b9fb25c29db9"  # Replace with your existing security group ID

# User data script to install Apache and deploy a sample app
USER_DATA_SCRIPT = """#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<html><h1>Hello, this is your web app running on Apache!</h1></html>" > /var/www/html/index.html
"""

def create_launch_configuration(asg_client, launch_config_name, ami_id, instance_type, security_group_id, key_pair_name):
    """Creates a launch configuration for the Auto Scaling Group."""
    try:
        # Create launch configuration
        response = asg_client.create_launch_configuration(
            LaunchConfigurationName=launch_config_name,
            ImageId=ami_id,
            InstanceType=instance_type,
            SecurityGroups=[security_group_id],
            KeyName=key_pair_name,
            UserData=USER_DATA_SCRIPT,  # Configures Apache and deploys app
        )
        print(f"Launch configuration {launch_config_name} created successfully!")
        return response
    except Exception as e:
        print(f"Error creating launch configuration: {e}")
        return None

def create_auto_scaling_group(asg_client, asg_name, launch_config_name, security_group_id, vpc_zone_identifier):
    """Creates an Auto Scaling Group with a specified launch configuration."""
    try:
        # Create the Auto Scaling Group
        response = asg_client.create_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            LaunchConfigurationName=launch_config_name,
            MinSize=1,
            MaxSize=5,
            DesiredCapacity=2,
            VPCZoneIdentifier=vpc_zone_identifier,  # Subnets for the ASG (comma-separated string)
            HealthCheckType='EC2',
            HealthCheckGracePeriod=300,
            Tags=[{
                'Key': 'Name',
                'Value': 'MyASGInstance',
                'PropagateAtLaunch': True
            }]
        )
        print(f"Auto Scaling Group {asg_name} created successfully!")
        return response
    except Exception as e:
        print(f"Error creating Auto Scaling Group: {e}")
        return None

def create_scaling_policy(asg_client, asg_name, policy_name, scaling_adjustment, cooldown):
    """Create scaling policy to scale in or scale out."""
    try:
        # Create the scaling policy
        response = asg_client.put_scaling_policy(
            AutoScalingGroupName=asg_name,
            PolicyName=policy_name,
            AdjustmentType='ChangeInCapacity',
            ScalingAdjustment=scaling_adjustment,  # Positive for scale-up, negative for scale-down
            Cooldown=cooldown,
        )
        print(f"Scaling policy {policy_name} created successfully!")
        return response
    except Exception as e:
        print(f"Error creating scaling policy: {e}")
        return None

def main():
    ec2 = boto3.client("ec2", region_name=AWS_REGION)
    asg_client = boto3.client("autoscaling", region_name=AWS_REGION)

    # Skip Security Group creation: Use the existing security group ID
    security_group_id = EXISTING_SECURITY_GROUP_ID  # Use your pre-created security group ID

    # Step 1: Create Launch Configuration
    launch_config_name = "my-launch-configuration"
    create_launch_configuration(asg_client, launch_config_name, AMI_ID, INSTANCE_TYPE, security_group_id, KEY_PAIR_NAME)

    # Step 2: Create Auto Scaling Group
    asg_name = "my-auto-scaling-group"
    vpc_zone_identifier = 'subnet-01874c4512136bd62,subnet-08fa616f96d54dfc2'  # Replace with your subnet IDs (comma-separated string)
    create_auto_scaling_group(asg_client, asg_name, launch_config_name, security_group_id, vpc_zone_identifier)

    # Step 3: Create Scaling Policy
    scaling_policy_name = "scale-out-policy"
    create_scaling_policy(asg_client, asg_name, scaling_policy_name, scaling_adjustment=1, cooldown=300)

    # Optional: Create another scaling policy for scale-in
    scale_in_policy_name = "scale-in-policy"
    create_scaling_policy(asg_client, asg_name, scale_in_policy_name, scaling_adjustment=-1, cooldown=300)

if __name__ == "__main__":
    main()