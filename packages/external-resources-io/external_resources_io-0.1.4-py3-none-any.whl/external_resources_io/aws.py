from pydantic import BaseModel

class AwsResourceMetadata(BaseModel):
    region: str
    tags: dict[str, str]

class TerraformAwsResourcesMetdata(AwsResourceMetadata):
    state_key: str
