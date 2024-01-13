from enum import Enum
from typing import List


class DataConnectorType(str, Enum):
    KAFKA = "kafka"
    GCLOUD_SCHEDULER = "gcscheduler"
    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    GCLOUD_STORAGE = "gcs"
    GCLOUD_STORAGE_HMAC = "gcs_hmac"
    AMAZON_S3 = "s3"
    AMAZON_S3_IAMROLE = "s3_iamrole"

    def __str__(self) -> str:
        return self.value


class DataConnectorSettings:
    kafka = [
        "cli_version",
        "tb_endpoint",
        "kafka_bootstrap_servers",
        "kafka_sasl_plain_username",
        "kafka_sasl_plain_password",
        "kafka_security_protocol",
        "kafka_sasl_mechanism",
        "kafka_schema_registry_url",
    ]
    gcscheduler = ["gcscheduler_region"]
    bigquery = ["account"]
    snowflake = ["account", "username", "password", "warehouse", "warehouse_size", "role", "stage", "integration"]
    gcs_hmac = ["gcs_hmac_access_id", "gcs_hmac_secret"]
    s3 = [
        "s3_access_key_id",
        "s3_secret_access_key",
        "s3_region",
    ]
    s3_iamrole = [
        "s3_iamrole_arn",
        "s3_iamrole_external_id",
        "s3_iamrole_region",
    ]
    gcs = [
        "gcs_private_key_id",
        "gcs_client_x509_cert_url",
        "gcs_project_id",
        "gcs_client_id",
        "gcs_client_email",
        "gcs_private_key",
    ]


class DataLinkerSettings:
    kafka = [
        "tb_datasource",
        "tb_token",
        "kafka_topic",
        "kafka_group_id",
        "kafka_auto_offset_reset",
        "kafka_store_raw_value",
        "kafka_store_headers",
    ]


class DataSinkSettings:
    gcscheduler = ["cron", "timezone", "status", "gcscheduler_target_url", "gcscheduler_job_name", "gcscheduler_region"]
    gcs_hmac = [
        "bucket_path",
        "file_template",
        "partition_node",
        "format",
        "compression",
    ]
    s3 = [
        "bucket_path",
        "file_template",
        "partition_node",
        "format",
        "compression",
    ]
    s3_iamrole = [
        "bucket_path",
        "file_template",
        "partition_node",
        "format",
        "compression",
    ]


class DataSensitiveSettings:
    kafka = ["kafka_sasl_plain_password"]
    gcscheduler = [
        "gcscheduler_target_url",
        "gcscheduler_job_name",
        "gcscheduler_region",
    ]
    bigquery: List[str] = []
    snowflake: List[str] = []
    gcs_hmac: List[str] = ["gcs_hmac_secret"]
    s3: List[str] = ["s3_secret_access_key"]
    s3_iamrole: List[str] = ["s3_iamrole_arn"]
