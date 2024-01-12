from apipulse_python.core.model.sdk_options import SdkOptions
from apipulse_python.core.apipulse_sdk import options as OPTIONS
from apipulse_python.core.util.common_utils import get_headers

BASE_URL: str = OPTIONS.url
HEADERS: dict = get_headers()
DATA_INGESTION_URL: str = f'{BASE_URL}/api/v1/mirror/data-ingestion/code-sample/'

