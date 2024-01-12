"""Implements a LEGEND Data Object representing a scalar and corresponding utilities."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

from .. import utils as utils
from .lgdo import LGDO

log = logging.getLogger(__name__)


class Scalar(LGDO):
    """Holds just a scalar value and some attributes (datatype, units, ...)."""

    # TODO: do scalars need proper numpy dtypes?

    def __init__(self, value: int | float | str, attrs: dict[str, Any] = None) -> None:
        """
        Parameters
        ----------
        value
            the value for this scalar.
        attrs
            a set of user attributes to be carried along with this LGDO.
        """
        if not np.isscalar(value):
            raise ValueError("cannot instantiate a Scalar with a non-scalar value")

        self.value = value
        super().__init__(attrs)

    def datatype_name(self) -> str:
        if hasattr(self.value, "datatype_name"):
            return self.value.datatype_name
        else:
            return utils.get_element_type(self.value)

    def form_datatype(self) -> str:
        return self.datatype_name()

    def view_as(self, library: str, with_units: bool = False):
        r"""Dummy function, returns the scalar value itself.

        See Also
        --------
        .LGDO.view_as
        """
        return self.value

    def __eq__(self, other: Scalar) -> bool:
        if isinstance(other, Scalar):
            return self.value == other.value and self.attrs == self.attrs
        else:
            return False

    def __str__(self) -> str:
        attrs = self.getattrs()
        return f"{str(self.value)} with attrs={repr(attrs)}"

    def __repr__(self) -> str:
        return (
            self.__class__.__name__
            + f"(value={repr(self.value)}, attrs={repr(self.attrs)})"
        )
