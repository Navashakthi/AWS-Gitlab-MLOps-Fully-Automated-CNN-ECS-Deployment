# AWS-Gitlab-MLOps-Fully-Automated-CNN-ECS-Deployment
A fully automated MLOps with Gitlab pipeline that runs a CNN image classification model and serves on ECS cluster
### Overview

This project leverages a CI/CD pipeline for building, training, deploying, and managing machine learning models using AWS services like SageMaker, ECS, and ECR. The pipeline is configured using GitLab CI/CD and facilitates the entire lifecycle of a CNN model, from algorithm containerization to model deployment on an inference endpoint.

## Prerequisites
Before running this pipeline, ensure you have the following prerequisites:

- **AWS Account**: An active AWS account with permissions to use SageMaker, S3, and IAM services.
- **S3 Bucket:** An S3 bucket where training data and model artifacts will be stored.
- **IAM Role:** An IAM role with the necessary permissions for SageMaker to access S3 and ECR.
- **AWS CLI:** AWS CLI configured with your access and secret keys, and the region set.
- **GitLab CI/CD:** A GitLab project with CI/CD enabled and the environment variables set mentioned below.

## Pipeline Stages

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

## Pipeline Configuration

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
To successfully run this pipeline, you need to replace the placeholder variables with your specific AWS and project details.
Also you can set these variables in your Gitlab CI/CD settings.

### Requirements

- Python 3.8 or higher
- Docker
- AWS CLI
- GitLab CI/CD Runner

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/project-name.git
   cd project-name
   ```

2. **Install the necessary Python packages:**
   ```bash
   pip install boto3 sagemaker tensorflow
   ```

3. **Ensure Docker and AWS CLI are installed and configured on your machine:**
   ```bash
   aws configure
   ```
4. **Review the `.gitlab-ci.yml` File**:
   - Verify the pipeline stages and commands in the `.gitlab-ci.yml` file.
   - Make sure the paths and commands match your project structure and requirements.

5. **Push to GitLab**:
   - Commit and push your changes to GitLab:
     ```bash
     git add .
     git commit -m "Initial commit"
     git push origin main
     ```

6. **Monitor the Pipeline**:
   - Navigate to your GitLab project and go to **CI/CD** > **Pipelines**.
   - Monitor the progress of your pipeline stages: preprocess, train, build, config_deploy, deploy, predict, and cleanup.

7. **Verify the Results**:
   - Once the pipeline execution is complete, verify that the ECS endpoint is created and the inferences are successful.
   - Check that the resources are deleted after the cleanup stage to ensure cost savings.

By following these steps, you can execute the entire CI/CD pipeline to automate the training and deployment of a CNN model using Amazon SageMaker with GitLab CI/CD.


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

## CNN Model for Image Classification and Serving

The project involves training and serving a Convolutional Neural Network (CNN) model designed to classify images into six categories: Cat, Dog, Rabbit, Cow, Horse, and Sheep. The process is divided into two primary phases: training the model and serving it via a Flask application.

#### **1. Training the CNN Model**

The `train.py` script handles the training phase:

- **Data Handling**:
  - The script downloads and extracts training and validation datasets from an S3 bucket. 
  - Data augmentation is applied to enhance the model's generalization, using techniques such as rescaling, shearing, zooming, and horizontal flipping.

- **Model Architecture**:
  - The model consists of three convolutional layers with increasing filter sizes (32, 64, and 128 filters, respectively) followed by max-pooling layers.
  - The output from these layers is flattened and passed through a fully connected layer with 256 neurons, followed by a dropout layer to prevent overfitting, and finally, a softmax output layer with six neurons for classification.

- **Training**:
  - The model is trained for 50 epochs using the Adam optimizer and categorical cross-entropy loss, with a batch size of 32.
  - Training is validated using a separate validation dataset, and metrics like loss and accuracy are computed.

- **Saving and Deploying**:
  - After training, the model is saved as `cnn-classification-model.h5`.
  - The trained model is then uploaded to an S3 bucket for storage and deployment.

#### **2. Serving the CNN Model**

The `serve.py` script sets up a Flask application to serve the trained model:

- **Model Loading**:
  - The model is loaded from a local file (`cnn_classification_model.h5`). If the model file is not found, an error is raised.

- **Flask Application**:
  - The application is initialized with CORS enabled, allowing cross-origin requests.
  - The home route (`/`) renders the index page, where users can interact with the model.
  - The `/image` route handles image uploads, preprocesses the image, and makes predictions using the loaded model.

- **Image Prediction**:
  - Uploaded images are resized and transformed to match the input shape expected by the model (64x64 pixels).
  - The model predicts the class of the image, and the result is returned as a JSON response, mapping the predicted class to one of the six categories.

- **Deployment**:
  - The Flask app is configured to run on `0.0.0.0` with port `5000`, making it accessible from any IP address within the network.
  - If the `uploaded_images` directory does not exist, it is created to store uploaded images temporarily.

## Summary
This project demonstrates a complete workflow for building, training, and deploying a CNN model for image classification. The model is capable of distinguishing between six different classes, and the trained model can be easily served and accessed via a web interface, allowing users to upload images and receive predictions in real-time.

## Contributing

Contributions are welcome! Please submit a pull request with any enhancements or bug fixes.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 2 License. See the [LICENSE](LICENSE) file for more information.
