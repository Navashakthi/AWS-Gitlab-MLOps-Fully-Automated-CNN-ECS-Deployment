# AWS-Gitlab-MLOps-Fully-Automated-CNN-ECS-Deployment
A fully automated MLOps with Gitlab pipeline that runs a CNN image classification model and serves on ECS cluster
### Overview

This project leverages a CI/CD pipeline for building, training, deploying, and managing machine learning models using AWS services like SageMaker, ECS, and ECR. The pipeline is configured using GitLab CI/CD and facilitates the entire lifecycle of a CNN model, from algorithm containerization to model deployment on an inference endpoint.

### Pipeline Stages

The pipeline consists of the following stages:

1. **build_algorithm**: Builds the algorithm's Docker image (image of training container used as algorithm source for sagemaker training job) and pushes it to GitLab's image registry.
2. **push_algorithm**: Pushes the algorithm's Docker image from GitLab to AWS ECR.
3. **train_model**: Triggers a SageMaker training job using the algorithm's Docker image and monitors the job's status using create_training_job.py script.
4. **register_model**: Registers the trained model in SageMaker's model registry.
5. **docker_build**: Builds the serving Docker image with the trained model and pushes it to GitLab's image registry.
6. **docker_push**: Pushes the serving Docker image from GitLab to AWS ECR.
7. **deploy_task**: Deploys an ECS task definition using the serving Docker image.
8. **deploy_service**: Deploys an ECS service that runs the task definition created in the previous stage.
9. **inference_endpoint**: Fetches the inference endpoint created by the ECS service for model inference.

### Pipeline Configuration

The pipeline configuration includes several environment variables that need to be set:

```yaml
variables:
  AWS_REGION: us-east-1
  AWS_ACCOUNT_ID: "your-aws-account-id"
  AWS_S3_BUCKET: aws-bucket-name
  AWS_S3_PREFIX: "cnn-classification"
  SAGEMAKER_ROLE: your-sagemaker-role-arn
  AWS_ACCESS_KEY_ID: aws-access-key-id
  AWS_SECRET_ACCESS_KEY: aws-secret-access-key
  ECR_ALGO_REPO_NAME: "your-ecr-algorithm-repo-name"
  ECR_REPO_NAME: "your-ecr-serving-image-repo-name"
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG
  IMAGE_VERSION: "latest"
  ECS_CLUSTER_NAME: "test"
  ECS_TASK_FAMILY: "ecs-task-family-name"
  ECS_SERVICE_NAME: "ecs-service-name" # Change name for every execution
  TARGET_GROUP_ARN: "your-target-group-arn"
  SUBNET_ID1: "subnet-id1"
  SUBNET_ID2: "subnet-id2"
  SECURITY_GROUP: "sg-name"
  TRAINING_JOB_NAME: CNN-Training-Job-7 # Change name for every execution
  MODEL_PACKAGE_GROUP_NAME: "sagemaker-model-registry-group-name"
  MODEL_APPROVAL_STATUS: "Approved" # "PendingManualApproval"
  MODEL_NAME: CNN-Model # Empty model dir for saving latest model
```

### Requirements

- Python 3.8 or higher
- Docker
- AWS CLI
- GitLab CI/CD Runner

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/project-name.git
   cd project-name
   ```

2. Install the necessary Python packages:
   ```bash
   pip install boto3 sagemaker tensorflow
   ```

3. Ensure Docker and AWS CLI are installed and configured on your machine:
   ```bash
   aws configure
   ```

### Usage

1. **Build and Push Algorithm**:
   - The `build_algorithm` and `push_algorithm` stages will build the Docker image for the algorithm and push it to AWS ECR.

2. **Train Model**:
   - The `train_model` stage triggers a SageMaker training job and waits for its completion.

3. **Register Model**:
   - The `register_model` stage registers the trained model in SageMaker's model registry for versioning and deployment.

4. **Build and Push Serving Image**:
   - The `docker_build` and `docker_push` stages build and push the Docker image that contains the trained model to AWS ECR.

5. **Deploy ECS Task and Service**:
   - The `deploy_task` and `deploy_service` stages deploy the Docker image as an ECS task and service, making the model available for inference.

6. **Fetch Inference Endpoint**:
   - The `inference_endpoint` stage fetches the endpoint for making predictions using the deployed model.

### Contributing

Contributions are welcome! Please submit a pull request with any enhancements or bug fixes.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

### Contact

For questions or support, please contact the project maintainer at [your-email@example.com](mailto:your-email@example.com).
