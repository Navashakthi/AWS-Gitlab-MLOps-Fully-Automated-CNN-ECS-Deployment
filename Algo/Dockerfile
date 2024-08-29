FROM python:3.9

# Install necessary packages
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    nginx \
    && apt-get clean

# Set environment variable
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_REGION

ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV AWS_DEFAULT_REGION=${AWS_REGION}

# Copy the application files
COPY . .

# Install the required packages
RUN pip3 install -r requirements.txt

# Copy your script into the image
COPY train.py /opt/ml/code/train.py

# Set the entry point to run the script
ENTRYPOINT ["python", "/opt/ml/code/train.py"]