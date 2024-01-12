from pydantic import BaseModel
from typing import Optional
import base64
import json
from typing import TypeVar, Type

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


def parse_provision(b64input: str) -> AppInterfaceProvision:
    str_provision = base64.b64decode(b64input.encode("utf-8")).decode("utf-8")
    provision = AppInterfaceProvision.model_validate(json.loads(str_provision))
    return provision


T = TypeVar('T', bound=BaseModel)
def parse_input(b64input: str, Type[T]) -> T:
    str_input = base64.b64decode(b64input.encode("utf-8")).decode("utf-8")
    input = T.model_validate(json.loads(str_input))
    return input
