from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import functools
import threading


class CallbackContext(object):
    __instances = dict()
    __instances_lock = threading.Lock()

    def __init__(self, subscription_id, resource_group, workspace_name) -> None:
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.workspace_name = workspace_name

    @staticmethod
    def get(subscription_id, resource_group, workspace_name):
        if (subscription_id, resource_group, workspace_name) not in CallbackContext.__instances:
            with CallbackContext.__instances_lock:
                if (subscription_id, resource_group, workspace_name) not in CallbackContext.__instances:
                    CallbackContext.__instances[(subscription_id, resource_group, workspace_name)] =\
                        CallbackContext(subscription_id, resource_group, workspace_name)

        return CallbackContext.__instances[(subscription_id, resource_group, workspace_name)]

    @property
    def arm_id(self):
        return f'/subscriptions/{self.subscription_id}' +\
            f'/resourceGroups/{self.resource_group}' +\
            f'/providers/Microsoft.MachineLearningServices/workspaces/{self.workspace_name}'

    @property
    @functools.cache
    def credential(self):
        return DefaultAzureCredential()

    @property
    @functools.cache
    def ml_client(self):
        return MLClient(
            credential=self.credential,
            subscription_id=self.subscription_id,
            resource_group_name=self.resource_group,
            workspace_name=self.workspace_name)


def tool_ui_callback(func):
    def wrapped(subscription_id, resource_group_name, workspace_name, *args, **kwargs):
        context = CallbackContext.get(subscription_id, resource_group_name, workspace_name)
        return func(context, *args, **kwargs)

    return wrapped
