import json
import boto3

def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    
    if (message['Event'] == 'autoscaling:EC2_INSTANCE_TERMINATE'):
        ec2_instance_id = message['EC2InstanceId']
        ec2 = boto3.client('ec2')
        for tag in ec2.describe_instances(InstanceIds=[ec2_instance_id])['Reservations'][0]['Instances'][0]['Tags']:
            if (tag['Key'] == 'opsworks_stack_id'):
                opsworks_stack_id = tag['Value']
                opsworks = boto3.client('opsworks', 'us-east-1')
                for instance in opsworks.describe_instances(StackId=opsworks_stack_id)['Instances']:
                    if ('Ec2InstanceId' in instance):
                        if (instance['Ec2InstanceId'] == ec2_instance_id):
                            print("Deregistering OpsWorks instance " + instance['InstanceId'])
                            opsworks.deregister_instance(InstanceId=instance['InstanceId'])
    return message

