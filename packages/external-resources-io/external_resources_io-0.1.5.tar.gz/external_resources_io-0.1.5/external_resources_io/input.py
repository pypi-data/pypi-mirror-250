from pydantic import BaseModel
from typing import Optional
import base64
import json
from typing import TypeVar, Type, Any
from collections.abc import Mapping
import os

class ProvisionOptions(BaseModel):
    bucket: str
    region: str
    dynamodb_table: str

class AppInterfaceProvision(BaseModel):
    provision_provider: str  # aws
    provisioner: str  # ter-int-dev
    provider: str  # aws-iam-role
    identifier: str

    target_cluster: str
    target_namespace: str
    target_secret_name: Optional[str]
    options: ProvisionOptions

Data = TypeVar("Data", bound=BaseModel)
Metadata = TypeVar("Metadata", bound=BaseModel)

T = TypeVar('T', bound=BaseModel)
def parse_model(model_class: Type[T], data: Mapping[str,Any]) -> T:
    input = model_class.model_validate(data)
    return input

def parse_base64_model(model_class: Type[T], b64data: str) -> T:
    str_input = base64.b64decode(b64data.encode("utf-8")).decode("utf-8")
    data = json.loads(str_input)
    return parse_model(model_class=model_class, data=data)


def check_container_env() -> None:
    if "INPUT" not in os.environ:
        raise Exception("INPUT env var not present")

    if "PROVISION" not in os.environ:
        raise Exception("NAMESPACE env var not present")
