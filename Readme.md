# Hugging Face Image Upload App

This app allows users to upload an image and select a Hugging Face model for inference. The image is uploaded to S3, processed by a Lambda function, and the result is stored in DynamoDB.

## 🧩 Components

- **Frontend**: HTML/JS form to upload an image and select model
- **Backend**:
  - API Gateway + Lambda for image upload
  - S3 for file storage
  - Lambda trigger for processing image with Hugging Face
  - DynamoDB for storing inference result

## 🚀 Deployment

1. Configure S3 bucket and DynamoDB table in AWS.
2. Deploy Lambda function and configure it to be triggered by S3 `ObjectCreated` events.
3. Host `frontend/index.html` on S3 or any static host.

## 📦 Setup

Install dependencies:

```bash
pip install -r requirements.txt
