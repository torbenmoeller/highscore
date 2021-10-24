locals {
  region          = "eu-central-1"
}

resource "aws_dynamodb_table" "scores" {
  name         = "Scores"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "userID"
  range_key    = "datetime"

  attribute {
    name = "userID"
    type = "S"
  }

  attribute {
    name = "datetime"
    type = "S"
  }

  attribute {
    name = "season"
    type = "S"
  }

  attribute {
    name = "score"
    type = "S"
  }

  global_secondary_index {
    name            = "HighScoreIndex"
    hash_key        = "season"
    range_key       = "score"
    projection_type = "ALL"
  }

  tags = {
    Name        = "highscore"
    Environment = "production"
  }
}

