import json
from typing import List, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from apipulse_python.sdk_logger import logger
from apipulse_python.sdk_version import APIPULSE_SDK_VERSION
from apipulse_python.core.util.common_utils import get_headers

from ..model import AgentConfig, ApiSample


class ApiPulseHttpConnection:
    def __init__(self, ct_url, auth_key, environment, capture):
        self.__base_url = ct_url
        self.__auth_key = auth_key
        self.__environment = environment
        self.__always_capture = capture == "always"
        self.__headers = {"Accept": "application/json", "Connection": "close", **APIPULSE_SDK_VERSION}
        self.__headers.update(get_headers())

        if auth_key:
            self.__headers["authKey"] = self.__auth_key

        if environment and len(environment) > 0:
            self.__headers["environment"] = self.__environment

        if self.__always_capture:
            self.__headers["apipulse-capture"] = "always"

    def agent_config(self, agent_id, app_name) -> Optional[AgentConfig]:
        try:
            if len(self.__base_url) == 0:
                logger.error("Apipulse base url is empty")
                return None

            query_params = {
                "agentId": agent_id,
                "appName": app_name,
            }

            url = self.__base_url + "/api/v1/mirror/agent-config"

            if query_params:
                url = url + "?" + urlencode(query_params)

            self.__headers.update(get_headers())
            http_request = Request(url, method="GET", headers=self.__headers)

            with urlopen(http_request) as response:
                response_obj = json.load(response)
                logger.info(">>> response_obj ",response_obj)
                return AgentConfig(
                    buffer_sync_freq_in_sec=response_obj["bufferSyncFreqInSec"],
                    capture_api_sample=response_obj["captureApiSample"],
                    config_fetch_freq_in_sec=response_obj["configFetchFreqInSec"],
                    registered_api_configs=response_obj["registeredApiConfigs"],
                    timestamp=response_obj["timestamp"],
                    discovery_buffer_size=response_obj["discoveryBufferSize"],
                    discovery_buffer_size_per_api=response_obj["discoveryBufferSizePerApi"],
                    black_list_rules=response_obj["blackListRules"],
                )
        except Exception as e:
            logger.error("Error while fetching agent config", exc_info=e)
            return None

    def send_data_to_api_pulse(self,url,headers, data):
        ...
        # TODO AMIT changes
        import requests,json
        try:
            # modify the data 
            from apipulse_python.api_pulse_middleware.contract import ApiOwner, ApiSampleWrapper
            from apipulse_python.api_pulse_middleware.constants import HEADERS
            apiOwner = ApiOwner(env=HEADERS["X-ENV-NAME"], team = HEADERS["X-TEAM-NAME"], serviceName= HEADERS["X-SERVICE-NAME"] )
            data = json.loads(data)
            apiSampleWrapper = ApiSampleWrapper(apiOwner=apiOwner, apiSamples=data)
            print(f"Apisamplewrapper = {apiSampleWrapper}")
            json_data = apiSampleWrapper.model_dump()
            # json_data = json.loads(json_data)
            custom_header = dict()
            custom_header.update(HEADERS)
            response = requests.post(url=url,headers=custom_header, json=json_data)
            print(f"ApiPulse Ingestion apiSampleWrapper: {response.status_code} {response.text} {response.json()}")
        except Exception as e:
            print(f"Error sending URLs: {e} ")
    
    def send_samples(self, contents: List[ApiSample]):
        logger.debug(f"sending samples: [{','.join(map(lambda s: str(s), contents))}]")
        try:
            if len(self.__base_url) == 0:
                logger.error("Apipulse base url is empty")
                return None

            json_samples = []
            for content in contents:
                json_samples.append(to_json(content))
            data = json.dumps(json_samples, ensure_ascii=False)

            url = self.__base_url + "/api/v1/mirror/data-ingestion/api-sample"

            if self.__always_capture:
                url = self.__base_url + "/api/v1/mirror/data-ingestion/api-sample"
                
            self.__headers.update(get_headers())
            http_request = Request(url, method="POST", headers=self.__headers, data=data.encode("utf-8"))
            # http_request.add_header("Content-Type", "application/json")
            self.send_data_to_api_pulse(url,self.__headers, data)
            # with urlopen(http_request) as response:
            #     print(f"Response = {response}")
            #     if not response.status == 200:
            #         logger.error(f"Send Sample Request failed, API returned {response.status}")
            #         return False

            return True
        except Exception as e:
            logger.error("Error while sending samples", exc_info=e)
            return False


def to_json(sample: ApiSample):
    data = {
        "rawUri": sample.raw_uri,
        "applicationName": sample.application_name,
        "hostName": sample.host_name,
        "port": int(sample.port) if sample.port and isinstance(sample.port, str) else sample.port,
        "scheme": sample.scheme,
        "method": sample.method,
        "statusCode": int(sample.status_code)
        if sample.status_code and isinstance(sample.status_code, str)
        else sample.status_code,
        "requestPayload": sample.request_payload,
        "responsePayload": sample.response_payload,
        "uncaughtExceptionMessage": sample.uncaught_exception_message,
        "payloadCaptureAttempted": sample.payload_capture_attempted,
        "requestPayloadCaptureAttempted": sample.request_payload_capture_attempted,
        "responsePayloadCaptureAttempted": sample.response_payload_capture_attempted,
        "latency": sample.latency,
        "uri":{
        "uriPath": sample.uri.uri_path,
        "hasPathVariable": sample.uri.has_path_variable
        }
    }

    params = {}
    req_headers = {}
    res_headers = {}

    if sample.parameters:
        keys = list(sample.parameters.keys())
        for key in keys:
            params[key] = sample.parameters.get(key)
    if sample.request_headers:
        keys = list(sample.request_headers.keys())
        for key in keys:
            req_headers[key] = sample.request_headers.get(key)
    if sample.response_headers:
        keys = list(sample.response_headers.keys())
        for key in keys:
            res_headers[key] = sample.response_headers.get(key)

    data["parameters"] = params
    data["requestHeaders"] = req_headers
    data["responseHeaders"] = res_headers

    return data
