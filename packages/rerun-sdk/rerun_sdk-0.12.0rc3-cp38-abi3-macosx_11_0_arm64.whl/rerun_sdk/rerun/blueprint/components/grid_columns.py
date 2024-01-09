# DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/python.rs
# Based on "crates/re_types/definitions/rerun/blueprint/components/grid_columns.fbs".

# You can extend this class by creating a "GridColumnsExt" class in "grid_columns_ext.py".

from __future__ import annotations

from typing import Any, Sequence, Union

import numpy as np
import numpy.typing as npt
import pyarrow as pa
from attrs import define, field

from ..._baseclasses import BaseBatch, BaseExtensionType, ComponentBatchMixin

__all__ = ["GridColumns", "GridColumnsArrayLike", "GridColumnsBatch", "GridColumnsLike", "GridColumnsType"]


@define(init=False)
class GridColumns:
    """**Component**: How many columns a grid container should have."""

    def __init__(self: Any, columns: GridColumnsLike):
        """
        Create a new instance of the GridColumns component.

        Parameters
        ----------
        columns:
            The number of columns.
        """

        # You can define your own __init__ function as a member of GridColumnsExt in grid_columns_ext.py
        self.__attrs_init__(columns=columns)

    columns: int = field(converter=int)
    # The number of columns.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    def __array__(self, dtype: npt.DTypeLike = None) -> npt.NDArray[Any]:
        # You can define your own __array__ function as a member of GridColumnsExt in grid_columns_ext.py
        return np.asarray(self.columns, dtype=dtype)

    def __int__(self) -> int:
        return int(self.columns)


GridColumnsLike = GridColumns
GridColumnsArrayLike = Union[
    GridColumns,
    Sequence[GridColumnsLike],
]


class GridColumnsType(BaseExtensionType):
    _TYPE_NAME: str = "rerun.blueprint.components.GridColumns"

    def __init__(self) -> None:
        pa.ExtensionType.__init__(self, pa.uint32(), self._TYPE_NAME)


class GridColumnsBatch(BaseBatch[GridColumnsArrayLike], ComponentBatchMixin):
    _ARROW_TYPE = GridColumnsType()

    @staticmethod
    def _native_to_pa_array(data: GridColumnsArrayLike, data_type: pa.DataType) -> pa.Array:
        raise NotImplementedError  # You need to implement native_to_pa_array_override in grid_columns_ext.py
