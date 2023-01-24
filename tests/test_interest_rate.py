#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 19:33:59 2023

@author: piterdias
"""

import pytest

from dacite import from_dict
from dataclass_quantlib.interest_rate import InterestRate


@pytest.fixture
def interest_rate():
    object_description = {
        "interestRate": 0.1,
        "interestRateDayCounter": {
            "dayCounterName": "Business252",
            "dayCounterConvention": "",
            "dayCounterCalendar": {
                "calendarName": "Brazil",
                "calendarMarket": "Settlement",
            },
        },
        "interestRateCompounding": {"enumerationValue": "Compounded"},
        "interestRateFrequency": {"enumerationValue": "Annual"},
    }
    return object_description


def test_interest_rate_instantiation(interest_rate):
    bond = from_dict(data_class=InterestRate, data=interest_rate)
    assert isinstance(bond, InterestRate)
