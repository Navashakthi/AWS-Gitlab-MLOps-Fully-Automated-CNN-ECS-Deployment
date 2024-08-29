import os
import boto3

def get_load_balancer_dns(cluster_name, service_name):
    region_name = 'us-east-1'  # Default to 'us-east-1' if not set
    ecs_client = boto3.client('ecs', region_name=region_name)
    elb_client = boto3.client('elbv2', region_name=region_name)  # For Application Load Balancer
    elb_classic_client = boto3.client('elb', region_name=region_name)  # For Classic Load Balancer

    # Describe the ECS service
    response = ecs_client.describe_services(cluster=cluster_name, services=[service_name])
    service = response['services'][0]

    print("Service Details:", service)  # Debug print

    dns_names = []

    # Get the load balancer ARNs from the service
    for load_balancer in service.get('loadBalancers', []):
        print("Load Balancer:", load_balancer)  # Debug print

        target_group_arn = load_balancer.get('targetGroupArn')
        if target_group_arn:
            # Describe target group (for ALB/NLB)
            tg_response = elb_client.describe_target_groups(TargetGroupArns=[target_group_arn])
            print("Target Group Response:", tg_response)  # Debug print

            target_group = tg_response['TargetGroups'][0]
            lb_arn = target_group['LoadBalancerArns']
            lb_response = elb_client.describe_load_balancers(LoadBalancerArns=lb_arn)
            print("Load Balancer Response:", lb_response)  # Debug print

            lb = lb_response['LoadBalancers'][0]
            dns_names.append(lb['DNSName'])
        else:
            # For Classic Load Balancers
            lb_name = load_balancer['loadBalancerName']
            lb_response = elb_classic_client.describe_load_balancers(LoadBalancerNames=[lb_name])
            print("Classic Load Balancer Response:", lb_response)  # Debug print

            lb = lb_response['LoadBalancerDescriptions'][0]
            dns_names.append(lb['DNSName'])

    return dns_names


 

if __name__ == "__main__":
    cluster_name = 'test'
    service_name = os.getenv('ECS_SERVICE_NAME')
    
    if not cluster_name or not service_name:
        print("CLUSTER_NAME and SERVICE_NAME environment variables must be set")
        exit(1)

    dns_names = get_load_balancer_dns(cluster_name, service_name)
    
    if dns_names:
        for dns_name in dns_names:
            print(f"Load Balancer DNS Name: {dns_name}")
    else:
        print("No DNS names found.")
