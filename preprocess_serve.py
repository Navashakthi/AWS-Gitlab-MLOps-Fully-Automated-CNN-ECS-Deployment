import os
import tarfile
import boto3

# Get S3 path from environment variable
model_path = os.getenv('MODEL_PATH')
print("model_path:", model_path)

# Define file paths
model_tar_path = 'models/model.tar.gz'
model_file = 'models/cnn_classification_model.h5'

def download_model_from_s3(s3_path, local_path):
    s3 = boto3.client('s3')
    if s3_path.startswith('s3://'):
        s3_path = s3_path[len('s3://'):]
    if '/' not in s3_path:
        raise ValueError("S3 path must contain both bucket and key.")
    bucket_name, key = s3_path.split('/', 1)
    if not bucket_name or not key:
        raise ValueError("Invalid S3 path format. Ensure it contains both bucket and key.")

    try:
        s3.download_file(bucket_name, key, local_path)
        print(f"Model downloaded from s3://{bucket_name}/{key} to {local_path}")
    except Exception as e:
        print(f"Error downloading model from S3: {e}")
        raise

def extract_model_tar(tar_path, extract_path):
    with tarfile.open(tar_path, 'r:gz') as tar:
        tar.extractall(path=extract_path)

def main():
    if not os.path.exists('models'):
        os.makedirs('models')

    if not os.path.exists(model_file):
        print("Downloading model from S3...")
        download_model_from_s3(model_path, model_tar_path)
        print("Extracting model...")
        extract_model_tar(model_tar_path, 'models')
        print("Model extraction completed.")

if __name__ == "__main__":
    main()
