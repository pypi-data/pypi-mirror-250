from .cli import init_cli
from .load_balancer import init_alb


def main():
    args = init_cli()
    application_load_balancer = init_alb(
        host=args.host, port=args.port, healthcheck_endpoint=args.healthcheck_endpoint
    )
    application_load_balancer.register_servers(servers=args.servers)
    application_load_balancer.register_routing(routing_algorithm=args.routing)
    application_load_balancer.run()


if __name__ == "__main__":
    main()
