from dataclasses import dataclass


@dataclass
class EnumeratedField(int):
    enumerationValue: str

    def __new__(cls, enumerationValue, typeObject):
        try:
            value_ = getattr(typeObject, enumerationValue)
        except AttributeError as ae:
            raise ValueError(
                f"{enumerationValue} isn't a value attribute of {typeObject.__name__} enumeration.") from ae
        if not isinstance(value_.value, int):
            raise ValueError(
                f"{enumerationValue} isn't a integer attribute of {typeObject.__name__}.")
        return super().__new__(cls, value_.value)
