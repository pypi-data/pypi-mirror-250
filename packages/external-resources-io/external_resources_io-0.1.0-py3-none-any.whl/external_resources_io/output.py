import base64
import json
import logging
from collections.abc import Mapping
from typing import Optional

from kubernetes import client, config
from kubernetes.client import CoreV1Api
from kubernetes.client.exceptions import ApiException


class Output:
    def read_outputs(self, file_path: str = "/work/output.json") -> dict[str, str]:
        outputs: dict[str, str] = {}
        with open(file_path, "r") as f:
            data = json.load(f)
            for k, v in data["CDKTF"].items():
                outputs[k] = base64.b64encode(bytes(v, "utf-8")).decode("utf-8")
        return outputs


class InClusterSecretOutput(Output):
    v1: CoreV1Api

    def __init__(self) -> None:
        config.load_incluster_config()
        #config.load_kube_config()
        self.v1 = client.CoreV1Api()

    def build_secret(
        self,
        secret_name: str,
        secret_data: Mapping[str, str],
        annotations: Optional[Mapping[str, str]],
    ) -> client.V1Secret:
        if not annotations:
            annotations = {}

        return client.V1Secret(
            api_version="v1",
            metadata=client.V1ObjectMeta(name=secret_name, annotations=annotations),
            data=secret_data,
        )

    def save_outputs(
        self,
        namespace_name: str,
        secret_name: str,
        secret_data: Mapping[str, str],
        annotations: Mapping[str, str],
    ):
        secret = self.build_secret(
            secret_name=secret_name, secret_data=secret_data, annotations=annotations
        )
        try:
            self.v1.read_namespaced_secret(secret_name, namespace_name)
            logging.info("Secret already exists: Replacing")
            self.v1.replace_namespaced_secret("test", namespace_name, body=secret)
        except ApiException as e:
            if e.status == 404:
                logging.info("Secret does not exist: Creating")
                self.v1.create_namespaced_secret(namespace=namespace_name, body=secret)
            else:
                raise


# input: AppInterfaceInput = parse_input(os.environ["INPUT"])

# o = InClusterSecretOutput()
# outputs = o.read_outputs()
# o.save_outputs()
# print(outputs)
