from pydantic import BaseModel
from typing import Dict, List

class EndpointInfo(BaseModel):
    pattern: str
    method: str

    # Pydantic's BaseModel includes a __str__ method that uses __repr__
    # and a method .dict() which is equivalent to your to_dict()

class ServiceApiDetails(BaseModel):
    controllerVsApis: Dict[str, List[EndpointInfo]]

    # Pydantic will automatically validate that controllerVsApis is a dict
    # with string keys and lists of EndpointInfo objects as values.
    # The .dict() method and __str__ method are also provided by BaseModel.


class ApiOwner(BaseModel):
    env: str
    team: str
    serviceName: str
    
class ApiSampleWrapper(BaseModel):
    apiOwner: ApiOwner
    apiSamples: List # it is better to mention the type of object in list
    
    