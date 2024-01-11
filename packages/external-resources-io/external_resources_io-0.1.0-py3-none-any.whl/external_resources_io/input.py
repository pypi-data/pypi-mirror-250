from pydantic import BaseModel
from typing import Optional
import base64
import json


class ProvisionOptions(BaseModel):
    bucket: str
    region: str
    dynamodb_table: str

class AppInterfaceProvision(BaseModel):
    provision_provider: str  # aws
    provisioner: str  # ter-int-dev
    provider: str  # aws-iam-role

    target_cluster: str
    target_namespace: str
    target_secret_name: Optional[str]
    options: ProvisionOptions

def parse_provision(b64input: str) -> AppInterfaceProvision:
    str_provision = base64.b64decode(b64input.encode("utf-8")).decode("utf-8")
    provision = AppInterfaceProvision.model_validate(json.loads(str_provision))
    return provision
