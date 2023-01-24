#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 22:53:35 2023

@author: piterdias
"""

import QuantLib as ql
from dataclasses import dataclass


@dataclass
class Region(ql.CustomRegion):
    regionName: str
    regionCode: str

    def __post_init__(self):
        super().__init__(
            self.regionName,
            self.regionCode,
        )
