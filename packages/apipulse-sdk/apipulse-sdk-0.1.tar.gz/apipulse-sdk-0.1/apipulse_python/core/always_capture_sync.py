import concurrent.futures
from threading import BoundedSemaphore

from apipulse_python.sdk_logger import logger

from .http.http_connection import ApiPulseHttpConnection


class ApiPulseDataSyncService:
    def __init__(self, apipulse_http_connection):
        self.__apipulse_http_connection: ApiPulseHttpConnection = apipulse_http_connection
        self.__drop_count = 0
        self.__executor_service = None
        self.__semaphore = BoundedSemaphore(5)

    def init(self):
        try:
            self.__executor_service = concurrent.futures.ThreadPoolExecutor(
                max_workers=2, thread_name_prefix="sl-sync-"
            )
        except Exception as e:
            logger.error("Error in ApipulseDataSyncService.init", exc_info=e)
            return False
        return True

    def sync_data(self, api_sample):
        try:
            if api_sample is None:
                return

            def send_samples():
                samples = [api_sample]
                result = self.__apipulse_http_connection.send_samples(samples)
                if not result:
                    self.__drop_count += 1
                    logger.info(f"Dropped {self.__drop_count} samples")
                self.__semaphore.release()

            if self.__semaphore.acquire(blocking=False):
                self.__executor_service.submit(send_samples)
            else:
                self.__drop_count += 1
                logger.info(f"Dropped {self.__drop_count} samples")
        except Exception as e:
            logger.error("Error in ApipulseDataSyncService.sync_data", exc_info=e)
