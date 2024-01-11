import os
import pprint
from pathlib import Path
from typing import Dict

import yaml
from hmd_lib_librarian_client.hmd_lib_librarian_client import HmdLibrarianClient
from requests import request
from robot.api.deco import keyword, library
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal


from hmd_cli_tools.hmd_cli_tools import (
    make_standard_name,
    get_session,
    get_cloud_region,
    get_account_session,
    get_deployer_target_session,
    get_secret,
)
from hmd_graphql_client import BaseClient
from hmd_graphql_client.hmd_rest_client import RestClient
from hmd_lang_librarian.hmd_lang_librarian_client import HmdLangLibrarianClient
from hmd_schema_loader import DefaultLoader
from hmd_lib_auth.hmd_lib_auth import okta_service_account_token


@library
class LibrarianLib:
    def __init__(
        self,
        instance_name,
        repo_name,
        deployment_id,
        environment,
        hmd_region,
        customer_code,
        account_number=None,
        okta_secret_name=None,
    ):
        self.instance_name = instance_name
        self.repo_name = repo_name
        self.deployment_id = deployment_id
        self.environment = environment
        self.hmd_region = hmd_region
        self.customer_code = customer_code
        self.account_number = account_number
        self.okta_secret_name = okta_secret_name
        self.standard_name = make_standard_name(
            instance_name,
            repo_name,
            deployment_id,
            environment,
            hmd_region,
            customer_code,
        )
        base_url = os.environ.get("LIBRARIAN_URL")
        api_key = None
        auth_token = self._get_auth_token()
        if not base_url:
            base_url = self._generate_url()
            api_key = self._get_api_key()

        self.librarian_client = HmdLibrarianClient(
            base_url=base_url, api_key=api_key, auth_token=auth_token
        )
        self.client = HmdLangLibrarianClient(
            RestClient(
                base_url=base_url,
                loader=DefaultLoader("./schemas"),
                api_key=api_key,
                auth_token=auth_token,
            )
        )

    def _generate_url(self):
        if self.environment == "local":
            return f"http://proxy/{self.instance_name}/"
        env_str = "" if self.environment == "prod" else f"-{self.environment}"
        return f"https://{self.instance_name}-{self.deployment_id}-{self.hmd_region}.{self.customer_code}{env_str}-neuronsphere.io"

    # TODO: Refactor to a shared lib. Duplication present in the basic client
    def _get_auth_token(self):
        session = get_deployer_target_session(
            self.hmd_region, profile=None, account=self.account_number
        )

        client_secrets = get_secret(
            session, (self.okta_secret_name or "okta-cicd-service"), use_cache=True
        )

        return okta_service_account_token(
            client_secrets["client_id"], client_secrets["client_secret"], session
        )

    # TODO: Refactor to a shared lib. Duplication present in the basic client
    def _get_api_key(self):
        session = get_session(aws_region=get_cloud_region(self.hmd_region))
        if self.account_number:
            session = get_account_session(
                session,
                self.account_number,
                "hmd.neuronsphere.deploy",
                get_cloud_region(self.hmd_region),
            )

        apigw = session.client("apigateway")
        results = apigw.get_api_keys(
            nameQuery=f"{self.instance_name}_{self.repo_name}_{self.deployment_id}_{self.environment}_{self.hmd_region}_{self.customer_code}",
            includeValues=True,
        )

        return results["items"][0]["value"] if len(results["items"]) == 1 else None

    def _get_gozer_client(self, instance_name: str) -> BaseClient:
        url = f"https://{instance_name}-{self.deployment_id}-{self.hmd_region}.{self.customer_code}-{self.environment}-neuronsphere.io"
        return RestClient(url, None, auth_token=self._get_auth_token())

    @keyword
    def clear_librarian_databases(
        self, gozer_instance_name: str, pre_test_db_clear: Dict[str, list]
    ):
        if self.environment == "local":
            remoteConn = DriverRemoteConnection("ws://global-graph:8182/gremlin", "g")

            g = traversal().withRemote(remoteConn)

            g.V().drop().iterate()
            g.E().drop().iterate()

            session = get_session(aws_region=get_cloud_region(self.hmd_region))
            dynamo_client = session.client(
                "dynamodb", endpoint_url="http://dynamodb:8000/"
            )
            with open("instance_configuration.yaml", "r") as fl:
                instance_config = yaml.safe_load(fl)
            results = dynamo_client.scan(
                TableName=f"{instance_config.get('service_config', {}).get('hmd_db_engines',{}).get('dynamo', {}).get('engine_config', {}).get('dynamo_table', f'{self.repo_name}-librarian')}"
            )
            for item in results["Items"]:
                if item["entity_name"]["S"] != "hmd_lang_librarian.content_item_type":
                    dynamo_client.delete_item(
                        TableName=f"{instance_config.get('service_config', {}).get('hmd_db_engines',{}).get('dynamo', {}).get('engine_config', {}).get('dynamo_table', f'{self.repo_name}-librarian')}",
                        Key={
                            "identifier": {"S": item["identifier"]["S"]},
                            "version": {"S": item["version"]["S"]},
                        },
                    )

        else:
            session = get_deployer_target_session(
                self.hmd_region, profile=None, account=self.account_number
            )

            # delete the dynamo table
            # todo: handle case when too many rows to delete in one iteration
            dynamo_client = session.client("dynamodb")
            dynamo_resource = session.resource("dynamodb")
            existing_tables = [t.table_name for t in dynamo_resource.tables.all()]
            if self.standard_name in existing_tables:
                results = dynamo_client.scan(TableName=self.standard_name)
                for item in results["Items"]:
                    if (
                        item["entity_name"]["S"]
                        != "hmd_lang_librarian.content_item_type"
                    ):
                        dynamo_client.delete_item(
                            TableName=self.standard_name,
                            Key={
                                "identifier": {"S": item["identifier"]["S"]},
                                "version": {"S": item["version"]["S"]},
                            },
                        )
            # clear the databases...
            gozer_client = self._get_gozer_client(gozer_instance_name)
            for neptune_db in pre_test_db_clear.get("neptune_dbs", []):
                gozer_client.invoke_custom_operation(f"clear_db/{neptune_db}", {})
            for rds_service in pre_test_db_clear.get("rds_services", []):
                gozer_client.invoke_custom_operation(f"clear_db/{rds_service}", {})

    @keyword
    def clear_librarian(
        self, gozer_instance_name: str, pre_test_db_clear: Dict[str, list]
    ):
        self.clear_librarian_databases(gozer_instance_name, pre_test_db_clear)
        if self.environment == "local":
            session = get_session(aws_region=get_cloud_region(self.hmd_region))
            s3_client = session.resource(
                "s3",
                endpoint_url="http://minio:9000/",
                aws_access_key_id="minioadmin",
                aws_secret_access_key="minioadmin",
            )
            bucket = s3_client.Bucket(f"{self.repo_name}-default-bucket")
            bucket.objects.all().delete()
        else:
            session = get_deployer_target_session(
                self.hmd_region, profile=None, account=self.account_number
            )
            with open("instance_configuration.yaml", "r") as fl:
                instance_config = yaml.safe_load(fl)
            s3 = session.resource("s3")
            bucket_instance_name = instance_config["dependencies"]["lib-repo"][
                "instance_name"
            ]
            bucket_repo_name = instance_config["dependencies"]["lib-repo"]["repo_name"]
            bucket_deployment_id = instance_config["dependencies"]["lib-repo"][
                "deployment_id"
            ]

            bucket_name = f"{bucket_instance_name}-{bucket_repo_name}-{bucket_deployment_id}-{self.environment}-{self.hmd_region}-{self.customer_code}".replace(
                "_", "-"
            )
            bucket = s3.Bucket(bucket_name)
            bucket.objects.all().delete()

        # this should warm up the lambda so that tests don't have to
        # worry about timeouts
        try:
            self.librarian_search({})
        except:
            pass

    @keyword
    def librarian_put(self, data):
        return self.librarian_client._put(data)

    @keyword
    def librarian_close(self, data):
        path = f"{data}"
        return self.librarian_client._close(data)

    @keyword
    def librarian_upload(self, url, data, content_type="text/json"):
        if isinstance(data, dict):
            resp = request(
                "PUT", url, json=data, headers={"Content-Type": content_type}
            )
        else:
            resp = request(
                "PUT", url, data=data, headers={"Content-Type": content_type}
            )
        resp.raise_for_status()
        return

    @keyword
    def librarian_put_file(
        self,
        content_path: str,
        file_name: str,
        content_item_type: str = None,
        max_part_size: int = 10000000,
        number_of_threads: int = 2,
        number_of_tries: int = 3,
        seconds_between_retries: int = 2,
    ):
        def callback(data):
            print("\n****")
            print(
                f"Parts: {data['parts_complete']}/{data['total_parts']}; {data['parts_percent']:2.2%}"
            )
            print(
                f"Bytes: {data['bytes_complete']}/{data['total_bytes']}; {data['bytes_percent']:2.2%}"
            )
            pprint.pprint(data["parts"][:5])

        return self.librarian_client.put_file(
            content_path=content_path,
            file_name=file_name,
            content_item_type=content_item_type,
            max_part_size=max_part_size,
            number_of_threads=number_of_threads,
            number_of_tries=number_of_tries,
            seconds_between_retries=seconds_between_retries,
            status_callback=callback,
        )

    @keyword
    def librarian_search(self, data):
        return self.librarian_client._search(data)

    @keyword
    def librarian_get(self, data):
        return self.librarian_client._get(data)

    @keyword
    def librarian_get_file(
        self, file_name: str, content_path: str, force_overwrite: bool = False
    ):
        return self.librarian_client.get_file(
            file_name=file_name,
            content_path=content_path,
            force_overwrite=force_overwrite,
        )

    @keyword
    def librarian_get_by_nid(self, nid: str):
        nids = {"nids": [nid]}
        return self.librarian_client._get_by_nid(nids)

    @keyword
    def librarian_download(self, url):
        resp = request("GET", url)
        resp.raise_for_status()
        if resp.headers["Content-Type"] in ["text/json", "application/json"]:
            return resp.json()
        elif resp.headers["Content-Type"].startswith("text"):
            return resp.text
        else:
            return resp.content

    @keyword
    def librarian_get_file_by_nid(
        self, nid: str, file_name: str, force_overwrite: bool = False
    ):
        return self.librarian_client.get_file_by_nid(
            nid=nid, file_name=file_name, force_overwrite=force_overwrite
        )

    @keyword
    def search_by_named_query(self, query_name: str, query_params: Dict):
        return self.librarian_client.search_by_named_query(
            query_name=query_name, parameters=query_params
        )

    @keyword
    def get_queryable_schema_names(self):
        queryable_schemas = self.librarian_client.get_queryable_schemas()
        return [f'{qs["namespace"]}.{qs["name"]}' for qs in queryable_schemas]

    @keyword
    def search_librarian(self, filter: Dict):
        return self.librarian_client.search_librarian(filter)

    @keyword
    def librarian_scan(self):
        self.librarian_client.base_client.invoke_custom_operation("/scan_bucket", {})

    @keyword
    def librarian_index(self):
        return self.librarian_client.base_client.invoke_custom_operation(
            "/index_bucket", {}
        )
