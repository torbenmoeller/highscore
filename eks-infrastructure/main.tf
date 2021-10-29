locals {
#  name            = "managed_node_groups-${random_string.suffix.result}"
#  cluster_version = "1.21"
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



################################################################################
# Supporting Resources
################################################################################

#data "aws_availability_zones" "available" {
#  state = "available"
#}
#
#resource "random_string" "suffix" {
#  length  = 8
#  special = false
#}
#
#module "vpc" {
#  source = "terraform-aws-modules/vpc/aws"
#
#  name = "highscore-vpc"
#  cidr = "10.0.0.0/16"
#
#  azs             = data.aws_availability_zones.available.names
#  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
#  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
#
#  enable_nat_gateway   = true
#  single_nat_gateway   = true
#  enable_dns_hostnames = true
#
#  tags = {
#    Name        = "highscore"
#  }
#}
