import os
from aws_cdk import Aspects, Stage, Environment
from boto3 import client, session
from cdk_nag import AwsSolutionsChecks
from cdk.cdk_python_pipeline.stacks.oidc_setup_stack import OIDCSetup
from cdk.cdk_python_pipeline.utils import get_stack_name

class SetupStage(Stage):

    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)

        account = client('sts').get_caller_identity()['Account']
        region = session.Session().region_name
        environment = os.getenv('ENVIRONMENT', 'dev')

        service_stack = OIDCSetup(
            self,
            id=get_stack_name(),
            env=Environment(account=os.environ.get('AWS_DEFAULT_ACCOUNT', account), region=os.environ.get('AWS_DEFAULT_REGION', region)),
            is_production_env=True if environment == 'production' else False,
        )

        # Runs CDK Nag on Stack
        Aspects.of(service_stack).add(AwsSolutionsChecks())
