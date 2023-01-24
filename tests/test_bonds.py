#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 19:33:59 2023

@author: piterdias
"""

import pytest

from dacite import from_dict
from dataclass_quantlib.instruments.bonds import (
    AmortizingFixedRateBond,
    ZeroCouponBond,
)
from math import trunc
import QuantLib as ql

@pytest.fixture
def ntnf():
    bond_description = {
        "bondSettlementDays": 0,
        "bondCalendar": {
            "calendarName": "Brazil",
            "calendarMarket": "Settlement",
        },
        "bondIssueDate": {"date": "2022-01-07"},
        "bondCashFlows": {
            "legSchedule": {
                "scheduleEffectiveDate": {"date": "2022-01-01"},
                "scheduleTerminationDate": {"date": "2033-01-01"},
                "scheduleConvention": {"enumerationValue": "Unadjusted"},
                "scheduleTerminationDateConvention": {
                    "enumerationValue": "Unadjusted"
                },
                "scheduleTenor": {
                    "periodTimeUnit": {"enumerationValue": "Months"},
                    "periodLength": 6,
                },
                "scheduleCalendar": {
                    "calendarName": "Brazil",
                    "calendarMarket": "Settlement",
                },
                "scheduleDateGeneration": {"enumerationValue": "Backward"},
                "scheduleEndOfMonth": False,
                "scheduleFirstDate": {"date": ""},
                "scheduleNextToLastDate": {"date": ""},
            },
            "legDayCount": {
                "dayCounterName": "Thirty360",
                "dayCounterConvention": "BondBasis",
                "dayCounterCalendar": {
                    "calendarName": "NullCalendar",
                    "calendarMarket": "",
                },
            },
            "legNominals": [1000.0],
            "legCouponRates": [0.1],
            "legPaymentAdjustment": {"enumerationValue": "Following"},
            "legFirstPeriodDayCount": {
                "dayCounterName": "Thirty360",
                "dayCounterConvention": "BondBasis",
                "dayCounterCalendar": {
                    "calendarName": "NullCalendar",
                    "calendarMarket": "",
                },
            },
            "legExCouponPeriod": {
                "periodTimeUnit": {"enumerationValue": "Months"},
                "periodLength": 0,
            },
            "legExCouponCalendar": {
                "calendarName": "Brazil",
                "calendarMarket": "Settlement",
            },
            "legExCouponConvention": {"enumerationValue": "Following"},
            "legExCouponEndOfMonth": False,
            "legPaymentCalendar": {
                "calendarName": "Brazil",
                "calendarMarket": "Settlement",
            },
            "legPaymentLag": 0,
            "legCompounding": {"enumerationValue": "Compounded"},
            "legFrequency": {"enumerationValue": "Annual"},
        },
    }
    return bond_description


@pytest.fixture
def ltn():
    bond_description = {
        "bondSettlementDays": 0,
        "bondCalendar": {
            "calendarName": "Brazil",
            "calendarMarket": "Settlement",
        },
        "bondFaceAmount": 1000.0,
        "bondMaturityDate": {"date": "2026-07-01"},
        "bondPaymentConvention": {"enumerationValue": "Following"},
        "bondRedemption": 100.0,
        "bondIssueDate": {"date": "2022-02-11"},
    }
    return bond_description


def test_ltn_instantiation(ltn):
    bond = from_dict(data_class=ZeroCouponBond, data=ltn)
    assert isinstance(bond, ZeroCouponBond)


def test_ltn_price(ltn):
    bond = from_dict(data_class=ZeroCouponBond, data=ltn)
    assert (
        trunc(
            (
                bond.dirtyPrice(
                    0.130776,
                    ql.Business252(ql.Brazil(ql.Brazil.Settlement)),
                    ql.Compounded,
                    ql.Annual,
                    ql.Date(23, 1, 2023),
                )
                * 10
                - 656.457155
            )
            * 1000000
        )
        == 0
    )


def test_ntnf_instantiation(ntnf):
    bond = from_dict(data_class=AmortizingFixedRateBond, data=ntnf)
    assert isinstance(bond, AmortizingFixedRateBond)


def test_ntnf_price(ntnf):
    bond = from_dict(data_class=AmortizingFixedRateBond, data=ntnf)
    assert (
        trunc(
            (
                (
                    bond.dirtyPrice(
                        0.133118,
                        ql.Business252(ql.Brazil(ql.Brazil.Settlement)),
                        ql.Compounded,
                        ql.Annual,
                        ql.Date(23, 1, 2023),
                    )
                    / 100
                    * bond.redemption().amount()
                )
                - 834.873429
            )
            * 10000
        )
        == 0
    )
