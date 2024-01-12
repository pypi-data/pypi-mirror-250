import requests
from django.urls import get_resolver
from django.urls import URLResolver, URLPattern
from . import constants
from .contract import ServiceApiDetails, EndpointInfo
from .utils import simplify_regex_pattern
import json
# from apipulse_python.core.model.sdk_options import SdkOptions
# from apipulse_python.core.shortlook_sdk import options as OPTIONS



def collect_urls(urllist, prefix=''):
    url_info = []
    for entry in urllist:
        if isinstance(entry, URLPattern):
            pattern = prefix + entry.pattern.regex.pattern
            view = entry.callback
            methods = getattr(view, 'methods', ['GET'])  # Default to ['GET'] if not specified
            url_info.append({'url': pattern, 'methods': methods})
        elif isinstance(entry, URLResolver):
            url_info.extend(collect_urls(entry.url_patterns, prefix + entry.pattern.regex.pattern))
    return url_info

    
def collect_and_send_urls():
    url_info = collect_urls(get_resolver().url_patterns)
    endpoint_url = constants.DATA_INGESTION_URL
    endpoint_list = list()
    for info_dict in url_info:
        url = info_dict["url"]
        methods = info_dict["methods"]
        # create endpoint
        for method in methods:
            url = simplify_regex_pattern(url)
            endpoint_list.append(EndpointInfo(pattern=url,method=method))
    # done endpoint list      
    # print("endpointlist ", endpoint_list) 
    serviceApiDetails = ServiceApiDetails(controllerVsApis={"root": endpoint_list})  
    # print("serviceApiDetails", serviceApiDetails) 
    data = serviceApiDetails.model_dump()
    data["serviceName"] = constants.HEADERS["X-SERVICE-NAME"]
    data["team"] = constants.HEADERS["X-TEAM-NAME"]
    data["env"] = constants.HEADERS["X-ENV-NAME"]
    print("data collected for API : ",data) 
    try:
        response = requests.post(endpoint_url, headers=constants.HEADERS, json=data)
        print(f"URLs sent. Response: {response.status_code} {response.text} {response.json()}")
    except Exception as e:
        print(f"Error sending URLs: {e} ")
        



