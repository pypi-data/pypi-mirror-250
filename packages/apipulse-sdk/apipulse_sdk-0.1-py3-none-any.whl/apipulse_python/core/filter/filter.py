from typing import Optional

from apipulse_python.core.api_processor import ApiProcessor
from apipulse_python.core.buffer.api_buffer_key import ApiBufferKey
from apipulse_python.core.config.config_manager import ConfigManager
from apipulse_python.core.config.config_update_listener import ConfigUpdateListener
from apipulse_python.core.http.context import RequestResponseContext
from apipulse_python.core.model import AgentConfig
from apipulse_python.core.util.filter_utils import (
    get_api_config,
    get_observed_api_from_request,
    is_blacklisted_api,
)
from apipulse_python.sdk_logger import logger
import time

class ApipulseLoopFilter(ConfigUpdateListener):
    def __init__(self, config_manager, api_processor, application_name):
        self.__agent_config: Optional[AgentConfig] = None
        self.__configManager: ConfigManager = config_manager
        self.__api_processor: ApiProcessor = api_processor
        self.__application_name: str = application_name

    def init(self) -> bool:
        return self.__configManager.subscribe_to_updates(self)

    def on_successful_config_update(self, agent_config: AgentConfig):
        self.__agent_config = agent_config
        logger.debug(f"Config fetch success: {self.__agent_config}")

    def on_erroneous_config_update(self):
        self.__agent_config = AgentConfig.get_no_op_agent_config()
        logger.debug(f"Config fetch failed: {self.__agent_config}")

    def process(self, ctx: RequestResponseContext, next_fn, *args, **kwargs):
        start_time = time.time()
        framework_response, http_response = next_fn(*args, **kwargs)
        end_time = time.time()
        try:
            agent_config_local = self.__agent_config

            if not agent_config_local:
                return framework_response
            if agent_config_local.capture_api_sample is False:
                return framework_response
            if not ctx.request:
                return framework_response

            observed_api = get_observed_api_from_request(ctx.request)

            if is_blacklisted_api(observed_api, agent_config_local):
                return framework_response

            ctx.observed_api = observed_api
            ctx.application_name = self.__application_name
            ctx.agent_config = agent_config_local

            api_config = get_api_config(observed_api, agent_config_local)
            ctx.latency = int((end_time - start_time) * 1000)
            if api_config:
                logger.debug("Found sample for existing API")
                ctx.api_config = api_config
                ctx.api_buffer_key = ApiBufferKey.get_api_buffer_key_from_api_config(ctx.api_config)
                self.__api_processor.process_registered_api(ctx, http_response)
            else:
                logger.debug("Found sample for new API")
                ctx.api_buffer_key = ApiBufferKey.get_api_buffer_key_from_observed_api(ctx.observed_api)
                self.__api_processor.process_discovered_api(ctx, http_response)
        except Exception as e:
            logger.error("Error in Apipulse.process", exc_info=e)
        return framework_response
