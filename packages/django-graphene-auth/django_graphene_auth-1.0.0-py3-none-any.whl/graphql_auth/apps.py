from django.apps import AppConfig


class GraphQLAuthConfig(AppConfig):
    name = "graphql_auth"
    verbose_name = "Graphene Auth"

    def ready(self):
        import graphql_auth.signals
