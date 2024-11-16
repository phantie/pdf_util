from datetime import datetime
from typing import Literal
from typing import TypeVar
from typing import Set
from typing import Optional
from datetime import datetime
from datetime import timedelta
from datetime import timezone

import fitz
import pydantic

from pdf_util.visually_sign_doc.params import PagesToSign
from pdf_util.visually_sign_doc.params import Align


__all__ = [
    "derive_text_width",
    "split_full_name",
    "align_to_int",
    "pages_to_sign_to_indeces",
    "format_datetime",
    "now"
]


def derive_text_width(text: str, font_path: str, font_size: int) -> float:
    font = fitz.Font(fontfile=font_path)
    text_width = font.text_length(text, fontsize=font_size)
    return text_width

def split_full_name(name: str) -> list[str]:
    """Splits full name into 3 parts"""
    parts = name.split()
    assert len(parts) == 3
    return parts


def align_to_int(align: Align) -> Literal[0, 1, 2]:
    match align:
        case "left":
            return 0
        case "center":
            return 1
        case "right":
            return 2


def pages_to_sign_to_indeces(pages_to_sign: PagesToSign, page_count: pydantic.NonNegativeInt) -> Set[pydantic.NonNegativeInt]:
    from pdf_util.visually_sign_doc.params import FirstPage
    from pdf_util.visually_sign_doc.params import LastPage
    from pdf_util.visually_sign_doc.params import AllPages
    from pdf_util.visually_sign_doc.params import SomePages

    assert page_count > 0

    if isinstance(pages_to_sign, FirstPage):
        return {0}

    elif isinstance(pages_to_sign, LastPage):
        return {page_count - 1}

    elif isinstance(pages_to_sign, AllPages):
        return set(range(page_count))
    
    elif isinstance(pages_to_sign, SomePages):
        assert all(page < page_count for page in pages_to_sign.pages)
        return pages_to_sign.pages


def now(*, utc_tz_offset: timedelta) -> datetime:
    tz = timezone(utc_tz_offset)
    return datetime.now(tz)


FormattedDate = TypeVar("FormattedDate", bound=str)
FormattedTime = TypeVar("FormattedTime", bound=str)

def format_datetime(dt: datetime, *, datefmt="%Y.%m.%d", timefmt="%H:%M:%S") -> tuple[FormattedDate, FormattedTime]:
    def format_tz(tz: Optional[timezone]) -> str:
        if tz is None:
            return "+00'00"

        offset = tz.utcoffset(None)
        if offset is None:
            return "+00'00"
        
        total_seconds = int(offset.total_seconds())
        hours, remainder = divmod(abs(total_seconds), 3600)
        minutes, _ = divmod(remainder, 60)
        sign = '+' if total_seconds >= 0 else '-'
        return f"{sign}{hours:02d}'{minutes:02d}"
    
    tz = dt.tzinfo
    formatted_date = dt.strftime(datefmt)
    formatted_time = f"{dt.strftime(timefmt)} {format_tz(tz)}"
    return (formatted_date, formatted_time)

