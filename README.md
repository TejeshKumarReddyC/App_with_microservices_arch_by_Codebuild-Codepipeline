# A python app with microservices architecture
## Workflow
Github --> CodePipeline --> CodeBuild --> Build Docker image --> Push to ECR --> Generate task def (imagedefinition.json) --> Update ECS service.
