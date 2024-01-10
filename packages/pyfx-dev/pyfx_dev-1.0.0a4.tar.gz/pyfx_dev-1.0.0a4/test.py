import numpy as np
from numpy.typing import DTypeLike
from pydantic import BaseModel


class PyFxComponent(BaseModel):
    """Generic component use to create PyFx classes"""

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    modified: bool = True


class TestClass(PyFxComponent):
    name: str
    knobs: dict[str, int]
    data_type: np.float32

    def __init__(self, **data):
        super().__init__(**data)
        self.x = 1


a = TestClass(name="Test", knobs={"test": 2}, data_type=np.float32)
