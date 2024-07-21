resource "aws_secretsmanager_secret" "db_host" {
  name = "db_host"
}

resource "aws_secretsmanager_secret_version" "db_host_version" {
  secret_id     = aws_secretsmanager_secret.db_host.id
  secret_string = "pleasechangeme"
   
   lifecycle {
    ignore_changes = [
      secret_string  
    ]
  }

}

resource "aws_secretsmanager_secret" "db_name" {
  name = "db_name"
}

resource "aws_secretsmanager_secret_version" "db_name_version" {
  secret_id     = aws_secretsmanager_secret.db_name.id
  secret_string = "pleasechangeme"

lifecycle {
    ignore_changes = [
      secret_string 
    ]
  }


}

resource "aws_secretsmanager_secret" "db_user" {
  name = "db_user"
}

resource "aws_secretsmanager_secret_version" "db_user_version" {
  secret_id     = aws_secretsmanager_secret.db_user.id
  secret_string = "pleasechange"

   lifecycle {
    ignore_changes = [
      secret_string  
    ]
  }

}

resource "aws_secretsmanager_secret" "db_password" {
  name = "db_password"
}

resource "aws_secretsmanager_secret_version" "db_password_version" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = "pleasechangeme"

   lifecycle {
    ignore_changes = [
      secret_string 
    ]
  }

}
