from .utils import CallbackContext, tool_ui_callback
from promptflow.connections import CognitiveSearchConnection
import requests
from typing import Dict, List


@tool_ui_callback
def list_acs_indices(context: CallbackContext, acs_connection: CognitiveSearchConnection) -> List[Dict[str, str]]:
    connections = context.ml_client.connections._operation.list(
        workspace_name=context.workspace_name,
        cls=lambda objs: objs,
        category=None,
        **context.ml_client.connections._scope_kwargs)

    for connection in connections:
        if connection.name == acs_connection:
            selected_connection = connection
            break
    else:
        raise ValueError(f'Unable to find workspace connection "{acs_connection}" in {context.workspace_name}.')

    url = f'https://management.azure.com{context.arm_id}' +\
        f'/connections/{selected_connection.name}/listSecrets?api-version=2022-01-01-preview'
    auth_header = f'Bearer {context.credential.get_token("https://management.azure.com/.default").token}'

    secrets_response = requests.post(url, headers={'Authorization': auth_header}).json()
    api_key = secrets_response.get('properties', dict()).get('credentials', dict()).get('key')

    api_version = selected_connection.properties.metadata.get('ApiVersion', '2023-03-15-preview')
    indexes_response = requests.get(
        f'{selected_connection.properties.target}/indexes?api-version={api_version}',
        headers={'api-key': api_key}).json()

    return [{
        'value': index.get('name'),
        'display_value': index.get('name')} for index in indexes_response.get('value', [])]


@tool_ui_callback
def list_acs_index_fields(
        context: CallbackContext,
        acs_connection: CognitiveSearchConnection,
        acs_index_name: str,
        field_data_type: str
) -> List[Dict[str, str]]:
    connections = context.ml_client.connections._operation.list(
        workspace_name=context.workspace_name,
        cls=lambda objs: objs,
        category=None,
        **context.ml_client.connections._scope_kwargs)

    for connection in connections:
        if connection.name == acs_connection:
            selected_connection = connection
            break
    else:
        raise ValueError(
            f'Unable to find workspace connection "{acs_connection}" in workspace "{context.workspace_name}".')

    url = f'https://management.azure.com{context.arm_id}' +\
        f'/connections/{selected_connection.name}/listSecrets?api-version=2022-01-01-preview'
    auth_header = f'Bearer {context.credential.get_token("https://management.azure.com/.default").token}'

    secrets_response = requests.post(url, headers={'Authorization': auth_header}).json()
    api_key = secrets_response.get('properties', dict()).get('credentials', dict()).get('key')

    api_version = selected_connection.properties.metadata.get('ApiVersion', '2023-03-15-preview')
    indexes_response = requests.get(
        f'{selected_connection.properties.target}/indexes?api-version={api_version}',
        headers={'api-key': api_key}).json()

    for index in indexes_response.get('value', []):
        if index.get('name') == acs_index_name:
            selected_index = index
            break
    else:
        raise ValueError(f'Unable to find index "{acs_index_name}" in connection "{acs_connection}".')

    return [{
        'value': field.get('name'),
        'display_value': field.get('name')}
        for field in selected_index.get('fields', []) if field.get('type') == field_data_type]


@tool_ui_callback
def list_acs_index_semantic_configurations(
        context: CallbackContext,
        acs_connection: CognitiveSearchConnection,
        acs_index_name: str
) -> List[Dict[str, str]]:
    connections = context.ml_client.connections._operation.list(
        workspace_name=context.workspace_name,
        cls=lambda objs: objs,
        category=None,
        **context.ml_client.connections._scope_kwargs)

    for connection in connections:
        if connection.name == acs_connection:
            selected_connection = connection
            break
    else:
        raise ValueError(
            f'Unable to find workspace connection "{acs_connection}" in workspace "{context.workspace_name}".')

    url = f'https://management.azure.com{context.arm_id}' +\
        f'/connections/{selected_connection.name}/listSecrets?api-version=2022-01-01-preview'
    auth_header = f'Bearer {context.credential.get_token("https://management.azure.com/.default").token}'

    secrets_response = requests.post(url, headers={'Authorization': auth_header}).json()
    api_key = secrets_response.get('properties', dict()).get('credentials', dict()).get('key')

    api_version = selected_connection.properties.metadata.get('ApiVersion', '2023-03-15-preview')
    indexes_response = requests.get(
        f'{selected_connection.properties.target}/indexes?api-version={api_version}',
        headers={'api-key': api_key}).json()

    for index in indexes_response.get('value', []):
        if index.get('name') == acs_index_name:
            selected_index = index
            break
    else:
        raise ValueError(f'Unable to find index "{acs_index_name}" in connection "{acs_connection}".')

    configurations = selected_index.get('semantic', {}).get('configurations', [])
    return [{'value': configuration.get('name')} for configuration in configurations]
