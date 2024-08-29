# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Set environment variable
ARG MODEL_PATH
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_REGION

ENV MODEL_PATH=${MODEL_PATH}
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV AWS_DEFAULT_REGION=${AWS_REGION}

# Copy the rest of the working directory contents into the image
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p models
RUN python preprocess_serve.py

# Make port 3000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "serve.py"]
