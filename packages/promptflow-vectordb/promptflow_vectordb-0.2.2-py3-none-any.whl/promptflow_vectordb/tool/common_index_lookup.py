from .contracts.telemetry import StoreToolEventCustomDimensions
from .utils.logging import ToolLoggingUtils
from .common_index_lookup_extensions import get_search_func

from ..core.logging.utils import LoggingUtils

from azureml.rag.mlindex import MLIndex
from concurrent.futures import ThreadPoolExecutor
from promptflow import tool
from typing import List, Union
import uuid
import yaml


search_executor = ThreadPoolExecutor()
logging_config = ToolLoggingUtils.generate_config(
    tool_name="promptflow_vectordb.tool.common_index_lookup"
)


@tool
def search(
    mlindex_content: str,
    queries: Union[str, List[str]],
    top_k: int,
    query_type: str,
) -> List[List[dict]]:
    logger = LoggingUtils.sdk_logger(__package__, logging_config)
    logger.update_telemetry_context({
        StoreToolEventCustomDimensions.TOOL_INSTANCE_ID: str(uuid.uuid4())
    })

    if isinstance(queries, str):
        queries = [queries]
        unwrap = True
    else:
        unwrap = False

    mlindex_config = yaml.safe_load(mlindex_content)
    index = MLIndex(mlindex_config=mlindex_config)
    search_func = get_search_func(index, top_k, query_type)

    search_results = search_executor.map(search_func, queries)
    results = [[
        {'text': doc.page_content,
         'metadata': doc.metadata,
         'score': score} for doc, score in search_result] for search_result in search_results]

    if unwrap and len(results) == 1:
        return results[0]
    else:
        return results
