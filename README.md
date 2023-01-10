# Dataclass Quantlib
Dataclass QuantLib - A QuantLib Serialization Library for Python

Dataclass QuantLib aims to provide a way to serialize and deserialize QuantLib objects by making use of Python data classes and dacite library.

The library will not replace QuantLib in Python or other derivative libraries but provide a (near) standard tool able to build a library of financial instruments.

Dataclass QuantLib development started from a particular idea, build a JSON library of Brazilian fixed rate bonds that would make easier for everyone financial institution to support or study the Brazilian market with fewer costs.

QuantLib was choose because I already contributed to it with some code that helps Brazilian fixed rate bonds modeling possible. QuantLib project is widely recognized in the financial industry.

It is important to mention that dacite plays a very import role in this project because it (as stated in dacite's README.md) simplifies the creation of the data classes with minor coding from our side.

## Disclaimer

Dataclass QuantLib is a separate project which is not a part of QuantLib, and does not have any affiliation with QuantLib. The author would like to make it clear that issues arising due to this library should not be reported on the QuantLib repositories, and instead reported on this repository.

## Short Example

Lets evaluate a Brazilian LTN that matures on 01-Jan-2024, a zero coupon bond that pays R$1,000.00 on 01-Jan-2024. This payment shall be adjusted by the Brazilian Central Bank settlement calendar.

Anbima (www.anbima.com.br) published the following reference data on 06-Jan-2023:

* Price - R$ 883.368164
* Yield - 13.6049%

Given a bond object named *ltn*, someone could calculate the price using

yieldRate = ql.InterestRate(
    0.136049,
    ql.Business252(ql.Brazil(ql.Brazil.Settlement)),
    ql.Compounded,
    ql.Annual,
)

evaluationDate = ql.Date(6, 1, 2023)

print(ql.BondFunctions_cleanPrice(ltn, yieldRate, evaluationDate))

But how to create the *ltn* object?

### 1. Creating the LTN Using QuantLib in Python

import QuantLib as ql

from dataclass_quantlib.time import (
    Date,
    Calendar,
    BusinessDayConvention,
)
from dataclass_quantlib.instruments.bonds import (
    ZeroCouponBond,
)

ltn = ql.ZeroCouponBond(
    0,
    ql.Brazil(ql.Brazil.Settlement),
    1000,
    ql.Date(1,1,2024),
    ql.Following,
    1000,
    ql.Date(3, 1, 2020),
)


### 2. Creating the LTN Programatically Using Dataclass QuantLib

    from dataclass_quantlib.time import (
        Date,
        Calendar,
        BusinessDayConvention,
    )
    from dataclass_quantlib.instruments.bonds import (
        ZeroCouponBond,
    )

    ltn = ZeroCouponBond(
        bondSettlementDays=0,
        bondCalendar=Calendar(calendarName="Brazil", calendarMarket="Settlement"),
        bondFaceAmount=1000,
        bondMaturityDate=Date("2024-01-01"),
        bondPaymentConvention=BusinessDayConvention(enumerationValue="Following"),
        bondRedemption=1000,
        bondIssueDate=Date("2020-01-03"),
    )

### 3. Creating the LTN Using a dict representation

from dacite import from_dict
from dataclass_quantlib.instruments.bonds import (
    ZeroCouponBond,
)

bond_definition = {'bondSettlementDays': 0,
 'bondCalendar': {'calendarName': 'Brazil', 'calendarMarket': 'Settlement'},
 'bondFaceAmount': 1000,
 'bondMaturityDate': {'date': '2024-01-01'},
 'bondPaymentConvention': {'enumerationValue': 'Following'},
 'bondRedemption': 1000,
 'bondIssueDate': {'date': '2020-01-03'}}

ltn = from_dict(data_class=ZeroCouponBond, data=bond_definition)

### What Is The Actual Gain?

People can generate a library of bonds by just formatting the JSON manually or formatting for a data source.

## What are the next steps?

I will intend to make some Pytests and create the (JSON) library of bonds in a separate project in order to understand how this library can grow up.
We have a lot of inflation linked and floating rate bonds in our market that I never tested properly in QuantLib. These cases may (or not) require improvements in QuantLib before proper support using Dataclass QuantLib.
