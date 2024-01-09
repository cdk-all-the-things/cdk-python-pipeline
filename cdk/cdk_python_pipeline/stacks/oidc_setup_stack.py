from aws_cdk import Stack
from aws_cdk import aws_iam as iam
from cdk_nag import NagSuppressions
from cdk_pipelines_github import GitHubActionRole
from constructs import Construct


class OIDCSetup(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        github_provider = iam.OpenIdConnectProvider(
            self,
            "GithubOIDCProvider",
            url="https://token.actions.githubusercontent.com",
            client_ids=["sts.amazonaws.com"],
        )

        deploy_role = GitHubActionRole(
            self,
            "github-action-role",
            repos=["cdk-all-the-things/cdk-python-pipeline"],
            provider=github_provider,
        )

        self.export_value(deploy_role.role.role_arn)

        NagSuppressions.add_stack_suppressions(
            self,
            [
                {"id": "AwsSolutions-IAM5", "reason": "policy for cloudwatch logs."},
            ],
        )
