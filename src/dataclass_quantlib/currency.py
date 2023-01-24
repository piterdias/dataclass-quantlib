#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 22:43:35 2023

@author: piterdias
"""

import QuantLib as ql
from dataclasses import dataclass


@dataclass
class Currency(ql.Currency):
    currencyAlphabeticCode: str

    def __post_init__(self):
        try:
            currency_ = getattr(ql, f"{self.currencyAlphabeticCode}Currency")
        except AttributeError as ae:
            raise ValueError(
                f"{self.currencyAlphabeticCode} isn't a valid QuantLib currency."
            ) from ae

        if not issubclass(currency_, ql.Currency):
            raise ValueError(
                f"{self.currencyAlphabeticCode} isn't a valid QuantLib currency."
            )
        currency_.__init__(self)
