#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

import trafaret as t

from datarobot import Dataset, DataStore, UseCase
from datarobot._experimental.models.enums import (
    DataWranglingDataSourceTypes,
    DataWranglingDialect,
    RecipeInputType,
)
from datarobot._experimental.models.recipe_operations import (
    DatetimeSamplingOperation,
    DownsamplingOperation,
    RandomSamplingOperation,
    SamplingOperation,
    WranglingOperation,
)
from datarobot.enums import DEFAULT_MAX_WAIT
from datarobot.models.api_object import APIObject
from datarobot.utils import to_api
from datarobot.utils.waiters import wait_for_async_resolution


class DataSourceInput(APIObject):
    """Inputs required to create a new recipe from data store."""

    _converter = t.Dict(
        {
            t.Key("canonical_name"): t.String,
            t.Key("table"): t.String,
            t.Key("schema", optional=True): t.Or(t.String(), t.Null),
            t.Key("catalog", optional=True): t.Or(t.String(), t.Null),
            t.Key("sampling", optional=True): t.Or(SamplingOperation._converter, t.Null),
        }
    ).allow_extra("*")

    def __init__(
        self,
        canonical_name: str,
        table: str,
        schema: Optional[str] = None,
        catalog: Optional[str] = None,
        sampling: Optional[Union[RandomSamplingOperation, DatetimeSamplingOperation]] = None,
    ):
        self.canonical_name = canonical_name
        self.table = table
        self.schema = schema
        self.catalog = catalog
        self.sampling = sampling


class DatasetInput(APIObject):
    _converter = t.Dict(
        {
            t.Key("sampling"): SamplingOperation._converter,
        }
    ).allow_extra("*")

    def __init__(self, sampling: SamplingOperation):
        self.sampling = (
            SamplingOperation.from_server_data(sampling) if isinstance(sampling, dict) else sampling
        )


class JDBCTableDataSourceInput(APIObject):
    """Object, describing inputs for recipe transformations."""

    _converter = t.Dict(
        {
            t.Key("input_type"): t.String,
            t.Key("data_source_id"): t.String,
            t.Key("data_store_id"): t.String,
            t.Key("sampling", optional=True): t.Or(SamplingOperation._converter, t.Null),
            t.Key("alias", optional=True): t.Or(t.String(), t.Null),
        }
    ).allow_extra("*")

    def __init__(
        self,
        input_type: RecipeInputType,
        data_source_id: str,
        data_store_id: str,
        sampling: Optional[Union[SamplingOperation, Dict[str, Any]]] = None,
        alias: Optional[str] = None,
    ):
        self.input_type = input_type
        self.data_source_id = data_source_id
        self.data_store_id = data_store_id
        self.sampling = (
            SamplingOperation.from_server_data(sampling) if isinstance(sampling, dict) else sampling
        )
        self.alias = alias


class RecipeSettings(APIObject):
    """Settings, for example to apply at downsampling stage."""

    _converter = t.Dict(
        {
            t.Key("target", optional=True): t.Or(t.String(), t.Null),
            t.Key("weights_feature", optional=True): t.Or(t.String(), t.Null),
        }
    ).allow_extra("*")

    def __init__(self, target: Optional[str] = None, weights_feature: Optional[str] = None):
        self.target = target
        self.weights_feature = weights_feature


class Recipe(APIObject):
    """Data wrangling entity, which contains all information needed to transform dataset and generate SQL."""

    _path = "recipes/"

    _converter = t.Dict(
        {
            t.Key("dialect"): t.String,
            t.Key("recipe_id"): t.String,
            t.Key("status"): t.String,
            t.Key("inputs"): t.List(JDBCTableDataSourceInput._converter),
            t.Key("operations", optional=True): t.List(WranglingOperation._converter),
            t.Key("downsampling", optional=True): t.Or(DownsamplingOperation._converter, t.Null),
            t.Key("settings", optional=True): t.Or(RecipeSettings._converter, t.Null),
        }
    ).allow_extra("*")

    def __init__(
        self,
        dialect: DataWranglingDialect,
        recipe_id: str,
        status: str,
        inputs: List[Dict[str, Any]],
        operations: Optional[List[Dict[str, Any]]] = None,
        downsampling: Optional[Dict[str, Any]] = None,
        settings: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.dialect = dialect
        self.id = recipe_id
        self.status = status
        self.inputs = [JDBCTableDataSourceInput.from_server_data(input) for input in inputs]
        self.operations = (
            [WranglingOperation.from_server_data(op) for op in operations]
            if operations is not None
            else None
        )
        self.downsampling = (
            DownsamplingOperation.from_server_data(downsampling)
            if isinstance(downsampling, dict)
            else downsampling
        )
        self.settings = (
            RecipeSettings.from_server_data(settings) if isinstance(settings, dict) else settings
        )

    def retrieve_preview(self, max_wait: int = DEFAULT_MAX_WAIT) -> Dict[str, Any]:
        """Retrieve preview and compute it, if absent."""
        path = f"{self._path}{self.id}/preview/"
        response = self._client.post(path)
        finished_url = wait_for_async_resolution(
            self._client, response.headers["Location"], max_wait=max_wait
        )
        r_data = self._client.get(finished_url).json()
        # TODO: create an ApiObject for Preview
        return r_data  # type: ignore[no-any-return]

    @classmethod
    def set_inputs(cls, recipe_id: str, inputs: List[JDBCTableDataSourceInput]) -> Recipe:
        path = f"{cls._path}{recipe_id}/inputs/"
        payload = {"inputs": [to_api(input_) for input_ in inputs]}
        response = cls._client.put(path, json=payload)
        return Recipe.from_server_data(response.json())

    @classmethod
    def set_operations(cls, recipe_id: str, operations: List[WranglingOperation]) -> Recipe:
        path = f"{cls._path}{recipe_id}/operations/"
        payload = {"operations": [to_api(operation) for operation in operations]}
        response = cls._client.put(path, json=payload)
        return Recipe.from_server_data(response.json())

    @classmethod
    def get(cls, recipe_id: str) -> Recipe:
        path = f"{cls._path}{recipe_id}/"
        return cls.from_location(path)

    def get_sql(self, operations: Optional[List[WranglingOperation]] = None) -> str:
        """Generate sql for the given recipe in a transient way, recipe is not modified.
        if operations is None, recipe operations are used to generate sql.
        if operations = [], recipe operations are ignored during sql generation.
        if operations is not empty list, generate sql for them.
        """
        path = f"{self._path}{self.id}/sql/"
        payload = {
            "operations": [to_api(operation) for operation in operations]
            if operations
            else operations
        }
        response = self._client.post(path, data=payload)
        return response.json()["sql"]  # type: ignore[no-any-return]

    @classmethod
    def from_data_store(
        cls,
        use_case: UseCase,
        data_store: DataStore,
        data_source_type: DataWranglingDataSourceTypes,
        dialect: DataWranglingDialect,
        data_source_inputs: List[DataSourceInput],
    ) -> Recipe:
        """Create a wrangling recipe from data store."""
        payload = {
            "use_case_id": use_case.id,
            "data_store_id": data_store.id,
            "data_source_type": data_source_type,
            "dialect": dialect,
            "inputs": [to_api(input_) for input_ in data_source_inputs],
        }
        path = f"{cls._path}fromDataStore/"
        response = cls._client.post(path, data=payload)
        return Recipe.from_server_data(response.json())

    @classmethod
    def from_dataset(
        cls,
        use_case: UseCase,
        dataset: Dataset,
        dialect: Optional[DataWranglingDialect] = None,
        inputs: Optional[List[DatasetInput]] = None,
    ) -> Recipe:
        """Create a wrangling recipe from dataset."""
        payload = {
            "use_case_id": use_case.id,
            "dataset_id": dataset.id,
            "dataset_version_id": dataset.version_id,
            "dialect": dialect,
            "inputs": [to_api(input) for input in inputs] if inputs else None,
        }
        path = f"{cls._path}fromDataset/"
        response = cls._client.post(path, data=payload)
        return Recipe.from_server_data(response.json())
