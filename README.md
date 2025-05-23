# Blogging_Service_Docker

This repository contains a blogging service built using Flask, Celery, RabbitMQ and Elasticsearch. The application can be run using Docker or Kubernetes. Below are the instructions for both methods.


## Prerequisites

- Docker and Docker Compose installed
- Kubernetes cluster set up (e.g., Minikube, GKE, etc.)
- `kubectl` configured to interact with your cluster

## Running with Docker

1. **Build the Docker images:**

   Navigate to the root directory of the project and run:

   ```bash
   docker-compose build

2. **Start the containers:**

   Run the following command:

   ```bash
   docker-compose up

3. **Access the application:**

   The Flask app will be running on port 5000. You can access it at:

   ```bash
   http://localhost:5000

### Test Requests with Curl

- **Submit a Blog Post:**

   To submit a blog post, use the following command:

   ```bash
   curl -X POST http://localhost:5000/submit_blog -H "Content-Type: application/json" -d '{"blog-title": "My First Blog", "blog-text": "This is the content of my first blog.", "user-id": "user123"}'

- **Search for Blogs:**

   To search for blogs, use the following command:

   ```bash
   curl "http://localhost:5000/search_blog?q=First"

## Running with Kubernetes

1. **Deploy the application:**

   Navigate to the root directory of the project and run:

   ```bash
   kubectl apply -f ./kubernetes_files/

2. **Access the application:**

   The Flask app will be exposed on port 30000. You can access it at:

   ```bash
   http://localhost:30000

### Test Requests with Curl

- **Submit a Blog Post:**

   To submit a blog post, use the following command:

   ```bash
   curl -X POST http://localhost:30000/submit_blog -H "Content-Type: application/json" -d '{"blog-title": "My Second Blog", "blog-text": "This is the content of my Second blog.", "user-id": "userk8s"}'

- **Search for Blogs:**

   To search for blogs, use the following command:

   ```bash
   curl "http://localhost:30000/search_blog?q=Second"
