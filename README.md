# Dataclass Quantlib
Dataclass QuantLib - A QuantLib Serialization Library for Python

Dataclass QuantLib aims to provide a way to serialize and deserialize QuantLib objects by making use of Python data classes and dacite library.

The library will not replace QuantLib in Python or other derivative libraries but provide a (near) standard tool able to build a library of financial instruments.

Dataclass QuantLib development started from a particular idea, build a JSON library of Brazilian fixed rate bonds that would make easier for everyone financial institution to support or study the Brazilian market with fewer costs.

QuantLib was choose because I already contributed to it with some code that helps Brazilian fixed rate bonds modeling possible. QuantLib project is widely recognized in the financial industry.

It is important to mention that dacite plays a very import role in this project because it (as stated in dacite's README.md) simplifies the creation of the data classes with minor coding from our side.

## Disclaimer

Dataclass QuantLib is a separate project which is not a part of QuantLib, and does not have any affiliation with QuantLib. The author would like to make it clear that issues arising due to this library should not be reported on the QuantLib repositories, and instead reported on this repository.


