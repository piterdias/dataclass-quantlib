import QuantLib as ql
from enum import Enum
from dataclasses import dataclass
from dataclass_quantlib.engine.enumerations import EnumeratedField
from dataclass_quantlib.time import DayCounter, Frequency


class Compoundings(Enum):
    Simple = ql.Simple
    Compounded = ql.Compounded
    Continuous = ql.Continuous
    SimpleThenCompounded = ql.SimpleThenCompounded
    CompoundedThenSimple = ql.CompoundedThenSimple


@dataclass
class Compounding(EnumeratedField):
    def __new__(cls, enumerationValue):
        return super().__new__(cls, enumerationValue, Compoundings)


@dataclass
class InterestRate(ql.InterestRate):
    interestRate: float
    interestRateDayCounter: DayCounter
    interestRateCompounding: Compounding
    interestRateFrequency: Frequency

    def __post_init__(self):
        super().__init__(
            self.interestRate,
            self.interestRateDayCounter,
            self.interestRateCompounding,
            self.interestRateFrequency,
        )
