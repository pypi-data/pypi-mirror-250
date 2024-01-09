# DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/python.rs
# Based on "crates/re_types/definitions/rerun/components/vector3d.fbs".

# You can extend this class by creating a "Vector3DExt" class in "vector3d_ext.py".

from __future__ import annotations

from .. import datatypes
from .._baseclasses import ComponentBatchMixin

__all__ = ["Vector3D", "Vector3DBatch", "Vector3DType"]


class Vector3D(datatypes.Vec3D):
    """**Component**: A vector in 3D space."""

    # You can define your own __init__ function as a member of Vector3DExt in vector3d_ext.py

    # Note: there are no fields here because Vector3D delegates to datatypes.Vec3D
    pass


class Vector3DType(datatypes.Vec3DType):
    _TYPE_NAME: str = "rerun.components.Vector3D"


class Vector3DBatch(datatypes.Vec3DBatch, ComponentBatchMixin):
    _ARROW_TYPE = Vector3DType()
