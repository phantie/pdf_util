from __future__ import annotations

from typing import Literal
from typing import TypeVar
from typing import Annotated
from typing import Set
from typing import Self
from typing import Callable
from datetime import datetime

import pydantic



class SignDocParams(pydantic.BaseModel):
    page_params: SignPageParams
    pages_to_sign: Annotated[PagesToSign, pydantic.Field(discriminator="choice", default_factory=lambda: FirstPage())]



class LocaleSignPageParams(pydantic.BaseModel):
    digitally_signed_by: str
    date: str
    signature: str


UK_LOCALE_SIGN_PAGE_PARAMS = LocaleSignPageParams(
    digitally_signed_by="Підписано цифровим підписом:",
    date="Дата: ",
    signature="(підпис)",
)

EN_LOCALE_SIGN_PAGE_PARAMS = LocaleSignPageParams(
    digitally_signed_by="Digitally signed by ",
    date="Date: ",
    signature="(signature)",
)

def default_calculate_datetime() -> datetime:
    from pdf_util.visually_sign_doc._util import now
    from datetime import timedelta
    return now(utc_tz_offset=timedelta(hours=2))


class CalculatedDatetimeSignPageParams(pydantic.BaseModel):
    calculate_datetime: Callable[[], datetime] = default_calculate_datetime

class ScalarDatetimeSignPageParams(pydantic.BaseModel):
    datetime: datetime


class SignPageParams(pydantic.BaseModel):
    signer_name: str
    left_box_text_align: Align = "left"
    under_text_align: Literal["align_with_right", "center"] = "center"
    scale: pydantic.PositiveFloat = 1
    margins: Margins = pydantic.Field(..., default_factory=lambda: Margins.equal(10))
    align_horizontal: Literal["right", "center", "left"] = "right"
    align_vertical: Literal["bottom","center","up"] = "bottom"
    locale: LocaleSignPageParams = EN_LOCALE_SIGN_PAGE_PARAMS
    datetime: CalculatedDatetimeSignPageParams | ScalarDatetimeSignPageParams = pydantic.Field(CalculatedDatetimeSignPageParams())

    model_config = pydantic.ConfigDict(validate_default=True, frozen=True)


class Margins(pydantic.BaseModel):
    left: pydantic.NonNegativeFloat = 0
    right: pydantic.NonNegativeFloat = 0
    top: pydantic.NonNegativeFloat = 0
    bottom: pydantic.NonNegativeFloat = 0

    @classmethod
    def equal(cls, value: pydantic.NonNegativeFloat) -> Self:
        """get equal margins from all sides"""

        return cls(
            left=value,
            right=value,
            top=value,
            bottom=value,
        )


class FirstPage(pydantic.BaseModel):
    choice: Literal["first_page"] = "first_page"

class LastPage(pydantic.BaseModel):
    choice: Literal["last_page"] = "last_page"

class AllPages(pydantic.BaseModel):
    choice: Literal["all_pages"] = "all_pages"

class SomePages(pydantic.BaseModel):
    choice: Literal["some_pages"] = "some_pages"
    pages: Set[pydantic.NonNegativeInt]


PagesToSign = FirstPage | LastPage | AllPages | SomePages


Align = TypeVar("Align", bound=Literal["left", "center", "right"])
