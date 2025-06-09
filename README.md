# Akka

This project contains a sample Akka application, along with configurations for local execution and deployment to various platforms.

## Local Development & Execution

### Build & Run Locally

#### Docker

##### Prerequisites

- docker installed

##### Instructions

1. Build the container image (or pull the pre-built one):

    # To build locally (optional)

    ```bash
    docker build -t ghcr.io/platform-engineering-org/akka:latest .
    ```

2. Run the application using the public image:

    ```bash
    docker run -p 5000:5000 ghcr.io/platform-engineering-org/akka:latest
    ```

3. Access the application at `http://127.0.0.1:5000`.

#### Kind

##### Prerequisites

- kind installed
- kubectl installed

##### Instructions

1. Build the container image:

    ```bash
    docker build -t ghcr.io/platform-engineering-org/akka:latest .
    ```

2. Create cluster

    ```bash
    kind create cluster
    ```

3. Load image

    ```bash
    kind load docker-image ghcr.io/platform-engineering-org/akka:latest
    ```

4. Deploy the application:

    ```bash
    kubectl apply -f deploy/kind.yaml
    ```

5. Port forwarding

    ```bash
    kubectl port-forward service/akka-app-service 5000:5000
    ```

6. Access the application at `http://127.0.0.1:5000`.

7. Delete cluster

    ```bash
    kind delete cluster
    ```

## AWS ECS Fargate Deployment (via OpenTofu)

This setup deploys the Akka application to AWS ECS Fargate, making it accessible via its private IP address within the configured VPC.

### Prerequisites

- AWS Account & IAM User with necessary permissions to create ECS, IAM, EC2 (Security Groups), CloudWatch Logs resources.
- AWS CLI configured with credentials (e.g., via `aws configure` or environment variables for the `us-east-1` region).
- OpenTofu installed.
- Docker installed (primarily to be aware of the image source, pulling locally is optional for deployment).

### Deployment Steps

1. **Navigate to the deployment directory:**

    ```bash
    cd deployment
    ```

2. **Configure VPC and Subnet IDs:**
    - Copy the example variables file: `cp terraform.tfvars.example terraform.tfvars`
    - Edit `terraform.tfvars` and replace the placeholder values for `vpc_id` and `subnet_id` with your specific AWS VPC ID and Subnet ID for the `us-east-1` region. The subnet should be a private subnet if you intend to follow the default Fargate configuration without a public IP.

3. **Verify Image in `main.tf`:**
    The configuration in `deploy/main.tf` should use `image = "ghcr.io/platform-engineering-org/akka:latest"`.
    If you intend to use a different image for the AWS deployment:
    - Build and push your custom Docker image to a container registry (e.g., Amazon ECR, Docker Hub).
    - Update the `image` value in `aws_ecs_task_definition.akka_app` within `deploy/main.tf` to point to your custom image URI.

4. **Initialize OpenTofu:**
    This downloads the necessary provider plugins.

    ```bash
    tofu init
    ```

5. **Review the Plan (Optional but Recommended):**

    See what resources will be created/modified.

    ```bash
    tofu plan
    ```

6. **Apply the Configuration:**
    This will provision the AWS resources. You will be prompted to confirm the changes.

    ```bash
    # Ensure AWS_PROFILE is set if needed, e.g., export AWS_PROFILE=your-profile
    tofu apply
    ```

### Accessing the Service (AWS)

- Once deployed, the ECS tasks will be running in private subnets.
- To get the private IP address of a running Fargate task, you can use the following AWS CLI command (ensure your AWS CLI is configured for the `us-east-1` region):

  ```bash
  TASK_ARN=$(aws ecs list-tasks --cluster akka-app-cluster --service-name akka-app-service --desired-status RUNNING --region us-east-1 --query "taskArns[0]" --output text) && \
  aws ecs describe-tasks --cluster akka-app-cluster --tasks $TASK_ARN --region us-east-1 --query "tasks[0].attachments[0].details[?name=='privateIPv4Address'].value | [0]" --output text
  ```

  *(This command retrieves the IP of the first running task. If you have multiple tasks, you might need to adapt it.)*
- The application, by default (as per the current `main.tf`), exposes port 5000. Access it via `http://<FARGATE_TASK_PRIVATE_IP>:5000` (replace `<FARGATE_TASK_PRIVATE_IP>` with the IP obtained above).
- Ensure you are accessing it from a machine within the same VPC or a peered VPC, or via a VPN connection that has access to the VPC. The security group `akka-internal-sg` by default allows access from `10.0.0.0/8`.

### Tagging (AWS)

- All created AWS resources are tagged with `Project = "akka"`.
- Tags from the ECS Task Definition are propagated to the running ECS tasks.

### Cleaning Up (AWS)

To remove all AWS resources created by this configuration, you will be prompted to confirm:

```bash
# Navigate to the deployment directory
cd deployment

# Ensure AWS_PROFILE is set if needed
tofu destroy
```

## OpenShift Deployment

This section outlines deploying the Akka application to an OpenShift cluster using the `deploy/openshift-deployment.yaml` file as a template.

### Prerequisites

- OpenShift CLI (`oc`) installed and configured to connect to your cluster.
- The image `ghcr.io/platform-engineering-org/akka:latest` should be accessible by your OpenShift cluster.

### Preparing the Deployment File

- The provided `deploy/openshift-deployment.yaml` serves as a starting point. It is pre-configured to use `image: ghcr.io/platform-engineering-org/akka:latest`.
- Before applying, consider the following customizations for your environment:
  - **Image (If different):** If you use an image other than `ghcr.io/platform-engineering-org/akka:latest`, update `spec.template.spec.containers[0].image` in the Deployment resource.
  - **Route Host (Optional):** If you want a specific hostname for your application, ensure the `spec.host` field in the Route resource is set. If omitted, OpenShift will generate a hostname.
  - Review other configurations like resource requests/limits, replicas, labels, etc., and adjust as needed.

### Deployment Steps

1. **Login to OpenShift (if not already):**

    ```bash
    oc login ...
    ```

2. **Target Namespace:**
    The `deploy/openshift-deployment.yaml` file does not specify a namespace. You must target the desired OpenShift project (namespace) when applying the configuration.
    You can either switch to your target project first:

    ```bash
    oc project <your-target-namespace>
    # or, if creating for the first time:
    # oc new-project <your-target-namespace>
    ```

    And then apply:

    ```bash
    oc apply -f deploy/openshift-deployment.yaml
    ```

    Alternatively, specify the namespace directly with the `apply` command:

    ```bash
    oc apply -f deploy/openshift-deployment.yaml -n <your-target-namespace>
    ```

3. **Apply the Deployment Configuration:**
    (Covered in the step above)

### Accessing the Service (OpenShift)

- The `deploy/openshift-deployment.yaml` (once applied) creates a `Service` that typically exposes the application internally and a `Route` to make it accessible externally.
- The example service maps port 80 to container port 5000. The route, if configured with a host or if one is generated by OpenShift, will provide the external URL.
- To find the hostname (replace `<your-target-namespace>` with the actual namespace used):

    ```bash
    oc get routes -n <your-target-namespace>
    ```

- Access the application via `http://<ROUTE_HOSTNAME>`.

### Cleaning Up (OpenShift)

To remove the resources deployed to OpenShift (replace `<your-target-namespace>` with the actual namespace used):

```bash
oc delete -f deploy/openshift-deployment.yaml -n <your-target-namespace>
# Or delete by label, type, name, etc., ensuring you target the correct namespace.
# oc delete all -l app=akka-app -n <your-target-namespace> # Example if your resources are labeled
```
