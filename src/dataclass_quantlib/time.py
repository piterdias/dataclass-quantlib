import QuantLib as ql
from enum import Enum
from dataclasses import dataclass, field
from dataclass_quantlib.engine.enumerations import EnumeratedField


class BusinessDayConventions(Enum):
    Following = ql.Following
    ModifiedFollowing = ql.ModifiedFollowing
    Preceding = ql.Preceding
    ModifiedPreceding = ql.ModifiedPreceding
    Unadjusted = ql.Unadjusted
    HalfMonthModifiedFollowing = ql.HalfMonthModifiedFollowing


@dataclass
class BusinessDayConvention(EnumeratedField):
    def __new__(cls, enumerationValue):
        return super().__new__(cls, enumerationValue, BusinessDayConventions)


@dataclass
class Date(ql.Date):
    date: str

    def __post_init__(self):
        if self.date == "":
            super().__init__()
        else:
            super().__init__(
                self.date,
                "%Y-%m-%d",
            )


class DateGenerations(Enum):
    Backward = ql.DateGeneration.Backward
    Forward = ql.DateGeneration.Forward
    Zero = ql.DateGeneration.Zero
    ThirdWednesday = ql.DateGeneration.ThirdWednesday
    ThirdWednesdayInclusive = ql.DateGeneration.ThirdWednesdayInclusive
    Twentieth = ql.DateGeneration.Twentieth
    TwentiethIMM = ql.DateGeneration.TwentiethIMM
    OldCDS = ql.DateGeneration.OldCDS
    CDS = ql.DateGeneration.CDS
    CDS2015 = ql.DateGeneration.CDS2015


@dataclass
class DateGeneration(EnumeratedField):
    def __new__(cls, enumerationValue):
        return super().__new__(cls, enumerationValue, DateGenerations)


class Frequencies(Enum):
    NoFrequency = ql.NoFrequency
    Once = ql.Once
    Annual = ql.Annual
    Semiannual = ql.Semiannual
    EveryFourthMonth = ql.EveryFourthMonth
    Quarterly = ql.Quarterly
    Bimonthly = ql.Bimonthly
    Monthly = ql.Monthly
    EveryFourthWeek = ql.EveryFourthWeek
    Biweekly = ql.Biweekly
    Weekly = ql.Weekly
    Daily = ql.Daily
    OtherFrequency = ql.OtherFrequency


@dataclass
class Frequency(EnumeratedField):
    def __new__(cls, enumerationValue):
        return super().__new__(cls, enumerationValue, Frequencies)


class TimeUnits(Enum):
    Days = ql.Days
    Weeks = ql.Weeks
    Months = ql.Months
    Years = ql.Years
    Hours = ql.Hours
    Minutes = ql.Minutes
    Seconds = ql.Seconds
    Milliseconds = ql.Milliseconds
    Microseconds = ql.Microseconds


@dataclass
class TimeUnit(EnumeratedField):
    def __new__(cls, enumerationValue):
        return super().__new__(cls, enumerationValue, TimeUnits)


@dataclass
class Period(ql.Period):
    periodTimeUnit: TimeUnit
    periodLength: int

    def __post_init__(self):
        super().__init__(self.periodLength, self.periodTimeUnit)


@dataclass
class Calendar(ql.Calendar):
    calendarName: str
    calendarMarket: str

    def __post_init__(self):
        try:
            calendar_ = getattr(ql, self.calendarName)
        except AttributeError as ae:
            raise ValueError(
                f"{self.calendarName} isn't a QuantLib calendar."
            ) from ae

        if not issubclass(calendar_, ql.Calendar):
            raise ValueError(f"{self.calendarName} isn't a QuantLib calendar.")
        if self.calendarMarket not in ("", None):
            market_ = getattr(calendar_, self.calendarMarket)
            calendar_.__init__(self, market_)
        else:
            calendar_.__init__(self)


@dataclass
class Schedule(ql.Schedule):
    scheduleEffectiveDate: Date
    scheduleTerminationDate: Date
    scheduleConvention: BusinessDayConvention
    scheduleTerminationDateConvention: BusinessDayConvention
    scheduleTenor: Period
    scheduleCalendar: Calendar
    scheduleDateGeneration: DateGeneration
    scheduleEndOfMonth: bool
    scheduleFirstDate: Date = field(default_factory=lambda: Date(date=""))
    scheduleNextToLastDate: Date = field(default_factory=lambda: Date(date=""))

    def __post_init__(self):
        super().__init__(
            self.scheduleEffectiveDate,
            self.scheduleTerminationDate,
            self.scheduleTenor,
            self.scheduleCalendar,
            self.scheduleConvention,
            self.scheduleTerminationDateConvention,
            self.scheduleDateGeneration,
            self.scheduleEndOfMonth,
            self.scheduleFirstDate,
            self.scheduleNextToLastDate,
        )


@dataclass
class DayCounter(ql.DayCounter):
    dayCounterName: str
    dayCounterConvention: str = ""
    dayCounterCalendar: Calendar = field(
        default_factory=lambda: Calendar(
            calendarName="NullCalendar", calendarMarket=""
        )
    )

    def __post_init__(self):
        try:
            dayCounter_ = getattr(ql, self.dayCounterName)
        except AttributeError as ae:
            raise ValueError(
                f"{self.dayCounterName} day counter doesn't exist on QuantLib."
            ) from ae
        if not issubclass(dayCounter_, ql.DayCounter):
            raise ValueError(
                f"{self.dayCounterName} isn't a QuantLib day counter."
            )
        if self.dayCounterConvention and (
            self.dayCounterCalendar.calendarName != "NullCalendar"
        ):
            raise ValueError(
                "Don't set both dayCounterConvention and dayCounterCalendar fields."
            )
        if (
            "" == self.dayCounterConvention
            and self.dayCounterCalendar.calendarName == "NullCalendar"
        ):
            dayCounter_.__init__(self)
        elif self.dayCounterConvention != "":
            dayCounterConvention_ = getattr(
                dayCounter_, self.dayCounterConvention
            )
            dayCounter_.__init__(self, dayCounterConvention_)
        else:
            dayCounter_.__init__(self, self.dayCounterCalendar)
