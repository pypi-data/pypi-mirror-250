from apipulse_python.core.api_processor import ApiProcessor
from apipulse_python.core.buffer.api_buffer_key import ApiBufferKey
from apipulse_python.core.http.context import RequestResponseContext
from apipulse_python.core.util.filter_utils import get_observed_api_from_request
from apipulse_python.sdk_logger import logger
import time

class AlwaysCaptureApipulseFilter:
    def __init__(self, api_processor, application_name):
        self.__api_processor: ApiProcessor = api_processor
        self.__application_name: str = application_name

    def process(self, ctx: RequestResponseContext, next_fn, *args, **kwargs):
        start_time = time.time()
        framework_response, http_response = next_fn(*args, **kwargs)
        end_time = time.time()
        try:
            observed_api = get_observed_api_from_request(ctx.request)

            ctx.application_name = self.__application_name
            ctx.observed_api = observed_api
            ctx.api_buffer_key = ApiBufferKey.get_api_buffer_key_from_observed_api(observed_api)
            ctx.latency = int((end_time - start_time) * 1000)
            self.__api_processor.process_always_capture(ctx, http_response)
        except Exception as e:
            logger.error("Error in Apipulse.process", exc_info=e)
        return framework_response
