from typing import NamedTuple

import pytest

from pyfx.exceptions import KnobRangeError
from pyfx.knob import PyFxKnob


class NormalTestInfo(NamedTuple):
    test_id: str
    test_data: dict


class ErrorTestInfo(NamedTuple):
    test_id: str
    test_data: dict
    error: Exception
    error_msg: str = None


"""PyFxKnob.__init__ Normal Tests"""
pyfx_knob_init_normal_test_info = [
    NormalTestInfo(
        test_id="PyFxKnob.__init__: Normal - Default Values",
        test_data={
            "name": "Volume",
        },
    ),
    NormalTestInfo(
        test_id="PyFxKnob.__init__: Normal - Initial Values",
        test_data={
            "name": "Balance",
            "minimum_value": -10,
            "maximum_value": 10,
            "default_value": 5,
            "precision": 1,
            "sensitivity": 0.5,
            "mode": "logarithmic",
            "display_enabled": True,
            "value": 0,
        },
    ),
]


@pytest.mark.parametrize(
    "test_id, test_data",
    pyfx_knob_init_normal_test_info,
    ids=[test_info.test_id for test_info in pyfx_knob_init_normal_test_info],
)
def test_pyfx_knob_init_normal_cases(test_id: str, test_data: dict):
    default_minimum_value = 0
    default_maximum_value = 1
    default_default_value = 0.5
    default_precision = 0.01
    default_sensitivity = 1
    default_mode = "linear"
    default_display_enabled = False
    default_value = 0.5

    expected_minimum_value = test_data.get("minimum_value", default_minimum_value)
    expected_maximum_value = test_data.get("maximum_value", default_maximum_value)
    expected_default_value = test_data.get("default_value", default_default_value)
    expected_precision = test_data.get("precision", default_precision)
    expected_sensitivity = test_data.get("sensitivity", default_sensitivity)
    expected_mode = test_data.get("mode", default_mode)
    expected_display_enabled = test_data.get("display_enabled", default_display_enabled)
    expected_value = test_data.get("value", default_value)

    knob = PyFxKnob(**test_data)

    assert knob.name == test_data["name"]
    assert knob.minimum_value == expected_minimum_value
    assert knob.maximum_value == expected_maximum_value
    assert knob.default_value == expected_default_value
    assert knob.precision == expected_precision
    assert knob.sensitivity == expected_sensitivity
    assert knob.mode == expected_mode
    assert knob.display_enabled == expected_display_enabled
    assert knob.value == expected_value


"""PyFxKnob.__init__ Error Tests"""
pyfx_knob_init_error_test_info = [
    ErrorTestInfo(
        test_id="PyFxKnob.__init__: Error - Min > Max",
        test_data={
            "name": "Volume",
            "minimum_value": 1,
            "maximum_value": 0,
        },
        error=KnobRangeError,
        error_msg="Minimum value must be less than maximum value",
    ),
    ErrorTestInfo(
        test_id="PyFxKnob.__init__: Error - Default outside of Min-Max",
        test_data={
            "name": "Volume",
            "minimum_value": 0,
            "maximum_value": 1,
            "default_value": 2,
        },
        error=KnobRangeError,
        error_msg="Default value must be within the minimum and maximum values",
    ),
]


@pytest.mark.parametrize(
    "test_id, test_data, error, error_msg",
    pyfx_knob_init_error_test_info,
    ids=[test_info.test_id for test_info in pyfx_knob_init_error_test_info],
)
def test_pyfx_knob_init_error_cases(test_id: str, test_data: dict, error: Exception, error_msg: str):
    # Act / Assert
    with pytest.raises(error) as exc_info:
        PyFxKnob(**test_data)

    if error_msg is not None:
        assert str(exc_info.value) == error_msg
