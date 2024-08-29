import boto3
import time
import os

def create_training_job():
    sm_client = boto3.client('sagemaker', region_name='us-east-1')

    training_job_name = os.getenv('TRAINING_JOB_NAME')
    training_image = os.getenv('TRAIN_IMAGE')
    role = os.getenv('SAGEMAKER_ROLE')
    bucket_name = os.getenv('AWS_S3_BUCKET')
    prefix = os.getenv('AWS_S3_PREFIX')
    
    response = sm_client.create_training_job(
        TrainingJobName=training_job_name,
        AlgorithmSpecification={
            'TrainingImage': training_image,
            'TrainingInputMode': 'File'
        },
        RoleArn=role,
        InputDataConfig=[
            {
                'ChannelName': 'train',
                'DataSource': {
                    'S3DataSource': {
                        'S3DataType': 'S3Prefix',
                        'S3Uri': 'your-training-dataset-s3-path',
                        'S3DataDistributionType': 'FullyReplicated'
                    }
                },
                'InputMode': 'File'
            },
            {
                'ChannelName': 'validation',
                'DataSource': {
                    'S3DataSource': {
                        'S3DataType': 'S3Prefix',
                        'S3Uri': 'your-validation-dataset-s3-path',
                        'S3DataDistributionType': 'FullyReplicated'
                    }
                },
                'InputMode': 'File'
            }
        ],
        OutputDataConfig={
            'S3OutputPath': 'your-output-path'
        },
        ResourceConfig={
            'InstanceType': 'ml.p3.2xlarge',
            'InstanceCount': 1,
            'VolumeSizeInGB': 50
        },
        StoppingCondition={
            'MaxRuntimeInSeconds': 86400
        },
        HyperParameters={
            'epochs': '10',
            'batch_size': '32'
        }
    )

    print("Training job created:", response['TrainingJobArn'])

if __name__ == "__main__":
    create_training_job()
