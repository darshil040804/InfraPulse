# AWS Deployment Notes

AWS deployment is optional for this project. To keep costs near zero, use AWS as documented architecture evidence unless you explicitly want to deploy.

Recommended portfolio approach:

- Run the full platform locally with Docker Compose.
- Capture screenshots of the dashboard, API docs, Kafka logs, and future Kibana dashboards.
- Deploy only the frontend, backend, and PostgreSQL for a public demo using free-tier-friendly services.

If deploying to AWS later:

- Push backend and frontend images to ECR.
- Run backend on ECS/Fargate.
- Use RDS PostgreSQL or a free external PostgreSQL provider during learning.
- Send container logs to CloudWatch.
- Keep Kafka and ELK local unless you have a cost-controlled reason to host them.
