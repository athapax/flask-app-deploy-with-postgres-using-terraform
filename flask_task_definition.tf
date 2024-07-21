# ECS Task Definition
resource "aws_ecs_task_definition" "app_task" {
  family                   = "app-task"
  execution_role_arn       = aws_iam_role.ecs_task_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([{
    name      = "app"
    image     = "ooghenekaro/flask-postgres:latest"  # Replace with your Docker image
    cpu       = 256
    memory    = 512
    essential = true
    portMappings = [
      {
        containerPort = 5000
        hostPort      = 5000
      }
    ]
    secrets = [
     {
        name      = "DB_HOST"
        valueFrom = aws_secretsmanager_secret.db_host.arn
      },
      {
        name      = "DB_NAME"
        valueFrom = aws_secretsmanager_secret.db_name.arn
      },
      {
        name      = "DB_USER"
        valueFrom = aws_secretsmanager_secret.db_user.arn
      },
      {
        name      = "DB_PASSWORD"
        valueFrom = aws_secretsmanager_secret.db_password.arn
      }
    ]
  }])


  tags = {
    Name = "app-task"
  }
}
