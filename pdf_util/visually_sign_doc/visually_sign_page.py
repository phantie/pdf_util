
from pdf_util.visually_sign_doc.params import SignPageParams
from pdf_util.visually_sign_doc._util import derive_text_width
from pdf_util.visually_sign_doc._util import split_full_name
from pdf_util.visually_sign_doc._util import align_to_int
from pdf_util.visually_sign_doc._util import format_datetime
from pdf_util.visually_sign_doc._util import now_utc_plus_2

from functools import partial
from pathlib import Path

import fitz



def visually_sign_page(page: fitz.Page, params: SignPageParams) -> None:
    name = params.signer_name
    x_offset = 0
    y_offset = 0

    date, time = format_datetime(now_utc_plus_2())

    font_path = str(Path(__file__).parent.parent/"assets"/"fonts"/"Roboto-Regular.ttf")
    fontname = "Roboto"

    left_part_font_size = 9 * params.scale
    right_part_font_size = 7 * params.scale
    under_line_part_font_size = 6 * params.scale

    margins = params.margins
    align_horizontal = params.align_horizontal
    align_vertical = params.align_vertical


    page.insert_font(fontfile=font_path, fontname=fontname)


    derive_left_part_text_width = partial(derive_text_width, font_path=font_path, font_size=left_part_font_size)
    derive_right_part_text_width = partial(derive_text_width, font_path=font_path, font_size=right_part_font_size)

    left_box_lines = split_full_name(name)

    right_box_lines = [
        f"{params.locale.digitally_signed_by}",
        f"{name}",
        f"{params.locale.date}{date}",
        f"{time}",
    ]

    lr_gap = derive_left_part_text_width("o")

    left_box_width = max(map(derive_left_part_text_width, left_box_lines))
    right_box_width = max(map(derive_right_part_text_width, right_box_lines))

    left_part_text = "\n".join(left_box_lines)
    right_part_text = "\n".join(right_box_lines)

    left_part_textbox_height=lambda x_offset, y_offset, with_insert: text_with_height_fit(
        page=page,
        text=left_part_text,
        x0=x_offset,
        x1=left_box_width + x_offset,
        y0=y_offset,
        fontname=fontname,
        fontsize=left_part_font_size,
        align=align_to_int(params.left_box_text_align),
        with_insert=with_insert
    )
    left_box_height=left_part_textbox_height(x_offset=x_offset, y_offset=y_offset, with_insert=False)

    right_part_textbox_height=lambda x_offset, y_offset, with_insert: text_with_height_fit(
        page=page,
        text=right_part_text,
        x0=x_offset + left_box_width + lr_gap,
        x1=x_offset + left_box_width + lr_gap + right_box_width,
        y0=y_offset,
        fontname=fontname,
        fontsize=right_part_font_size,
        align=align_to_int("left"),
        with_insert=with_insert
    )
    right_box_height=right_part_textbox_height(x_offset=x_offset, y_offset=y_offset, with_insert=False)

    top_part_height = max(left_box_height, right_box_height)

    def bottom_part_textbox_height(x_offset, y_offset, with_insert) -> float:
        if params.under_text_align == "align_with_right":
            under_part_params = {
                "x0": x_offset + left_box_width + lr_gap,
                "x1": x_offset + left_box_width + lr_gap + right_box_width,
                "align": 0
            }

        elif params.under_text_align == "center":
            under_part_params = {
                "x0": x_offset,
                "x1": x_offset + left_box_width + lr_gap + right_box_width,
                "align": 1
            }

        return text_with_height_fit(
            page=page,
            text=params.locale.signature,
            y0=top_part_height + y_offset,
            fontname=fontname,
            fontsize=under_line_part_font_size,
            with_insert=with_insert,
            **under_part_params
        )

    bottom_part_height=bottom_part_textbox_height(x_offset=x_offset, y_offset=y_offset, with_insert=False)

    signature_bounds = fitz.Rect(
        0,
        0,
        left_box_width + lr_gap + right_box_width,
        top_part_height + bottom_part_height
    )

    if align_horizontal == "right":
        x_offset = page.rect.width - signature_bounds.x1 - margins.right
    if align_horizontal == "center":
        x_offset = (page.rect.width - signature_bounds.x1) / 2
    if align_horizontal == "left":
        x_offset = margins.left

    if align_vertical == "bottom":
        y_offset = page.rect.height - signature_bounds.y1 - margins.bottom
    if align_vertical == "center":
        y_offset = (page.rect.height - signature_bounds.y1) / 2
    if align_vertical == "up":
        y_offset = margins.top

    left_part_textbox_height(x_offset=x_offset,y_offset=y_offset,with_insert=True)
    right_part_textbox_height(x_offset=x_offset,y_offset=y_offset,with_insert=True)
    bottom_part_textbox_height(x_offset=x_offset, y_offset=y_offset, with_insert=True)
    page.draw_line((x_offset, top_part_height + y_offset), (left_box_width + right_box_width + lr_gap + x_offset, top_part_height + y_offset), width=1, color=(0, 0, 0))

    


def text_with_height_fit(
    page: fitz.Page,
    text: str,
    x0,
    x1,
    y0,
    fontname,
    fontsize,
    align,
    with_insert: bool
) -> float:
    """Because the library is a piece of shit you need to first try to insert a text
    what's obviously won't fit and then use a lacking delta on Y axis to derive a precise textbox size"""

    min_y_delta = 1
    rect = fitz.Rect(x0, y0, x1, y0 + min_y_delta)
    lacking_y_delta = page.insert_textbox(rect, text, fontname=fontname, fontsize=fontsize, align=align)
    height = min_y_delta - lacking_y_delta
    rect = fitz.Rect(x0, y0, x1, y0 + height)
    if with_insert:
        page.insert_textbox(rect, text, fontname=fontname, fontsize=fontsize, align=align)
    return height

