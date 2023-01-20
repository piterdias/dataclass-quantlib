import QuantLib as ql
from dataclasses import dataclass
from dataclass_quantlib.time import (BusinessDayConvention, Schedule, Calendar,
                                     Period, Date, DayCounter, Frequency,
                                     )
from dataclass_quantlib.interest_rate import Compounding


@dataclass
class FixedRateLeg(tuple):
    legSchedule: Schedule
    legDayCount: DayCounter
    legNominals: list[float]
    legCouponRates: list[float]
    legPaymentAdjustment: BusinessDayConvention
    legFirstPeriodDayCount: DayCounter
    legExCouponPeriod: Period
    legExCouponCalendar: Calendar
    legExCouponConvention: BusinessDayConvention
    legExCouponEndOfMonth: bool
    legPaymentCalendar: Calendar
    legPaymentLag: int
    legCompounding: Compounding
    legFrequency: Frequency

    def __new__(cls,
                legSchedule,
                legDayCount,
                legNominals,
                legCouponRates,
                legPaymentAdjustment,
                legFirstPeriodDayCount,
                legExCouponPeriod,
                legExCouponCalendar,
                legExCouponConvention,
                legExCouponEndOfMonth,
                legPaymentCalendar,
                legPaymentLag,
                legCompounding,
                legFrequency,
                ):
        coupons_ = ql.FixedRateLeg(schedule=legSchedule,
                                   dayCount=legDayCount,
                                   nominals=legNominals,
                                   couponRates=legCouponRates,
                                   paymentAdjustment=legPaymentAdjustment,
                                   firstPeriodDayCount=legFirstPeriodDayCount,
                                   exCouponPeriod=legExCouponPeriod,
                                   exCouponCalendar=legExCouponCalendar,
                                   exCouponConvention=legExCouponConvention,
                                   exCouponEndOfMonth=legExCouponEndOfMonth,
                                   paymentCalendar=legPaymentCalendar,
                                   paymentLag=legPaymentLag,
                                   compounding=legCompounding,
                                   compoundingFrequency=legFrequency
                                   )
        return super().__new__(cls, coupons_,
                               )


@dataclass
class AmortizingFixedRateBond(ql.Bond):
    bondSettlementDays: int
    bondCalendar: Calendar
    bondIssueDate: Date
    bondCashFlows: FixedRateLeg

    def __post_init__(self):
        if self.bondSettlementDays < 0 or not isinstance(self.bondSettlementDays, int):
            f'bondSettlementDays = {self.bondSettlementDays} is invalid because it shall be non-negative int type.'
        super().__init__(
            self.bondSettlementDays,
            self.bondCalendar,
            self.bondIssueDate,
            self.bondCashFlows,
        )

@dataclass
class ZeroCouponBond(ql.ZeroCouponBond):
    bondSettlementDays: int
    bondCalendar: Calendar
    bondFaceAmount: float
    bondMaturityDate: Date
    bondPaymentConvention: BusinessDayConvention
    bondRedemption: float
    bondIssueDate: Date

    def __post_init__(self):
        if self.bondSettlementDays < 0 or not isinstance(self.bondSettlementDays, int):
            f'bondSettlementDays = {self.bondSettlementDays} is invalid because it shall be non-negative int type.'
        super().__init__(
            self.bondSettlementDays,
            self.bondCalendar,
            self.bondFaceAmount,
            self.bondMaturityDate,
            self.bondPaymentConvention,
            self.bondRedemption,
            self.bondIssueDate,
        )
