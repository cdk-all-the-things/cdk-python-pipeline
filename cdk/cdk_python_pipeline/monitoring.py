import aws_cdk.aws_sns as sns
from aws_cdk import CfnOutput
from aws_cdk import aws_iam as iam
from aws_cdk import aws_kms as kms
from cdk_monitoring_constructs import (
    AlarmFactoryDefaults,
    MonitoringFacade,
    SnsAlarmActionStrategy,
)
from constructs import Construct

from cdk.cdk_python_pipeline import constants


class ServiceMonitoring(Construct):

    def __init__(
        self,
        scope: Construct,
        id_: str
    ) -> None:
        super().__init__(scope, id_)
        self.id_ = id_
        self.notification_topic = self._build_topic()

    def _build_topic(self) -> sns.Topic:
        key = kms.Key(
            self,
            'MonitoringKey',
            description='KMS Key for SNS Topic Encryption',
            enable_key_rotation=True  # Enables automatic key rotation
        )
        topic = sns.Topic(self, f'{self.id_}alarms', display_name=f'{self.id_}alarms', master_key=key)
        # Grant CloudWatch permissions to publish to the SNS topic
        topic.add_to_resource_policy(
            statement=iam.PolicyStatement(
                actions=['sns:Publish'],
                effect=iam.Effect.ALLOW,
                principals=[iam.ServicePrincipal('cloudwatch.amazonaws.com')],
                resources=[topic.topic_arn],
            ))
        CfnOutput(self, id=constants.MONITORING_TOPIC, value=topic.topic_name).override_logical_id(constants.MONITORING_TOPIC)
        return topic

    def _build_high_level_dashboard(self, topic: sns.Topic):
        high_level_facade = MonitoringFacade(
            self,
            f'{self.id_}HighFacade',
            alarm_factory_defaults=AlarmFactoryDefaults(
                actions_enabled=True,
                alarm_name_prefix=self.id_,
                action=SnsAlarmActionStrategy(on_alarm_topic=topic),
            ),
        )
        high_level_facade.add_large_header('High Level Dashboard')


    def _build_low_level_dashboard(self, topic: sns.Topic):
        low_level_facade = MonitoringFacade(
            self,
            f'{self.id_}LowFacade',
            alarm_factory_defaults=AlarmFactoryDefaults(
                actions_enabled=True,
                alarm_name_prefix=self.id_,
                action=SnsAlarmActionStrategy(on_alarm_topic=topic),
            ),
        )
        low_level_facade.add_large_header('Low Level Dashboard')
