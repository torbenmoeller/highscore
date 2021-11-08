#
#data "aws_eks_cluster" "eks" {
#  name = module.eks.cluster_id
#}
#
#data "aws_eks_cluster_auth" "eks" {
#  name = module.eks.cluster_id
#}
#
#module "eks" {
#  source          = "terraform-aws-modules/eks/aws"
#
#  cluster_name    = local.name
#  cluster_version = local.cluster_version
#  vpc_id  = module.vpc.vpc_id
#  subnets = module.vpc.private_subnets
#
#  worker_groups = [
#    {
#      instance_type = "m6i.large"
#      asg_max_size  = 1
#    }
#  ]
#}
#
