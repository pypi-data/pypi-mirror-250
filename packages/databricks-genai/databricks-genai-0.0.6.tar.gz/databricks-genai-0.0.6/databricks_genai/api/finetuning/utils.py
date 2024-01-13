"""Utils for finetuning API"""
import json
import os
from typing import Optional, Union

from databricks.sdk import WorkspaceClient
from datasets import get_dataset_split_names
from mcli.api.exceptions import ValidationError
from mlflow import MlflowClient

_UC_VOLUME_LIST_API_ENDPOINT = '/api/2.0/fs/list'


def validate_model_registry_path(path: str) -> None:
    split_path = path.split('.')
    if len(split_path) == 2:
        catalog, schema_name = split_path
    elif len(split_path) == 3:
        catalog, schema_name, _ = split_path
    else:
        raise ValidationError(f'model_registry_path must be in the format '
                              f'catalog.schema or catalog.schema.model_name, but got {path}')
    for component in split_path:
        if len(component) == 0:
            raise ValidationError(f'model_registry_path must be in the format '
                                  f'catalog.schema or catalog.schema.model_name, but got {path}')
    validate_catalog_schema(catalog, schema_name, "model_registry_path")


def validate_delta_table(path: str, input_type: str) -> None:
    split_path = path.split('.')
    if len(split_path) != 3:
        raise ValidationError(f'Delta table input to {input_type} must be in the format '
                              f'catalog.schema.table, but got {path}.')
    for component in split_path:
        if len(component) == 0:
            raise ValidationError(f'Delta table input to {input_type} must be in the format '
                                  f'catalog.schema.table, but got {path}.')
    catalog, schema, _ = split_path
    validate_catalog_schema(catalog, schema, input_type)


def validate_catalog_schema(catalog: str, schema_name: str, input_type: str) -> None:
    w = WorkspaceClient()
    schemas = w.schemas.list(catalog)
    if schema_name not in [schema.name for schema in schemas]:
        raise ValidationError(f'Failed to find schema "{schema_name}" in catalog "{catalog}". Please make sure '
                              f'your {input_type} is valid and exists in the Unity Catalog.')


def validate_experiment_path(experiment_path: str) -> None:
    try:
        client = MlflowClient(tracking_uri='databricks')
        experiment = client.get_experiment_by_name(experiment_path)
        if not experiment:
            client.create_experiment(experiment_path)
    except Exception as e:
        raise ValidationError(f'Failed to get or create MLflow experiment {experiment_path}. Please make sure '
                              'your experiment name is valid.') from e


def validate_uc_path(uc_path: str) -> None:
    if not uc_path.startswith("dbfs:/Volumes"):
        raise ValidationError('Databricks Unity Catalog Volumes paths should start with "dbfs:/Volumes".')
    path = os.path.normpath(uc_path[len("dbfs:/"):])
    dirs = path.split(os.sep)
    if len(dirs) < 4:
        raise ValidationError(f'Databricks Unity Catalog Volumes path expected to start with ' \
            f'`dbfs:/Volumes/<catalog-name>/<schema-name>/<volume-name>`. Found path={uc_path}')
    object_path = "/" + path
    client = WorkspaceClient()
    if path.endswith(".jsonl"):
        try:
            client.files.get_status(object_path)
        except Exception as e:
            raise ValidationError(f"Failed to access Unity Catalog path {uc_path}.") from e
    else:
        data = json.dumps({'path': object_path})
        try:
            resp = client.api_client.do(method='GET',
                                        path=_UC_VOLUME_LIST_API_ENDPOINT,
                                        data=data,
                                        headers={'Source': 'mosaicml/finetuning'})
        except Exception as e:
            raise ValidationError(f"Failed to access Unity Catalog path {uc_path}.") from e
        if len([f['path'] for f in resp.get('files', []) if not f['is_dir']]) == 0:
            raise ValidationError(
                f"No files found in Unity Catalog path {uc_path}. Please make sure your path includes input data.")


def validate_hf_dataset(dataset_name_with_split: str) -> None:
    print(f"Assuming {dataset_name_with_split} is a Hugging Face dataset (not in format `dbfs:/Volumes` or "
          "`/Volumes`). Validating...")
    split_dataset_name = dataset_name_with_split.split('/')
    if len(split_dataset_name) < 2:
        raise ValidationError(
            f"Hugging Face dataset {dataset_name_with_split} must be in the format <dataset>/<split> or "
            "<entity>/<dataset>/<split>.")
    dataset_name, split = '/'.join(split_dataset_name[0:-1]), split_dataset_name[-1]
    try:
        splits = get_dataset_split_names(dataset_name)
    except Exception as e:
        raise ValidationError(
            f"Failed to access Hugging Face dataset {dataset_name_with_split}. Please make sure that the split "
            "is valid and that your dataset does not have subsets.") from e
    if split not in splits:
        raise ValidationError(f"Failed to access Hugging Face dataset {dataset_name_with_split}. Split not found.")
    print("Hugging Face dataset validation successful.")


# TODO: add custom weights - needs to support dbfs:/databricks/
def validate_create_finetuning_run_inputs(train_data_path: str,
                                          model_registry_path: Optional[str] = None,
                                          experiment_path: Optional[str] = None,
                                          eval_data_path: Optional[str] = None) -> None:
    if train_data_path.startswith('dbfs:/'):
        validate_uc_path(train_data_path)
    elif "/" in train_data_path:  # assume HF
        validate_hf_dataset(train_data_path)
    else:
        validate_delta_table(train_data_path, "train_data_path")
    if model_registry_path:
        validate_model_registry_path(model_registry_path)
    if experiment_path:
        validate_experiment_path(experiment_path)
    if eval_data_path is None:
        pass
    elif eval_data_path.startswith('dbfs:/'):
        validate_uc_path(eval_data_path)
    elif "/" in eval_data_path:  # assume HF
        validate_hf_dataset(eval_data_path)
    else:
        validate_delta_table(eval_data_path, "eval_data_path")


def format_path(path: Union[str, None]) -> Union[str, None]:
    """
    Prepends `dbfs:` in front of paths that start with `/Volumes`.
    """
    if isinstance(path, str) and path.startswith('/Volumes'):
        return f'dbfs:{path}'
    else:
        return path
