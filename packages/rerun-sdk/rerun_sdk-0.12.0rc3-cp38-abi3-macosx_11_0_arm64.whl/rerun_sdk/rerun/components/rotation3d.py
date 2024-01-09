# DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/python.rs
# Based on "crates/re_types/definitions/rerun/components/rotation3d.fbs".

# You can extend this class by creating a "Rotation3DExt" class in "rotation3d_ext.py".

from __future__ import annotations

from .. import datatypes
from .._baseclasses import ComponentBatchMixin

__all__ = ["Rotation3D", "Rotation3DBatch", "Rotation3DType"]


class Rotation3D(datatypes.Rotation3D):
    """**Component**: A 3D rotation, represented either by a quaternion or a rotation around axis."""

    # You can define your own __init__ function as a member of Rotation3DExt in rotation3d_ext.py

    # Note: there are no fields here because Rotation3D delegates to datatypes.Rotation3D
    pass


class Rotation3DType(datatypes.Rotation3DType):
    _TYPE_NAME: str = "rerun.components.Rotation3D"


class Rotation3DBatch(datatypes.Rotation3DBatch, ComponentBatchMixin):
    _ARROW_TYPE = Rotation3DType()
