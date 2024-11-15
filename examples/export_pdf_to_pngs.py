"""

Install:
    cd experiments/pdf_util
    poetry install
    poetry shell

Run:
    python examples/export_pdf_to_pngs.py --pdf path/to/file --out-dir output/dir/
"""

import argparse
import pdf_util
import fitz
import os.path

parser = argparse.ArgumentParser()
parser.add_argument('--pdf', required=True, type=str, help="Pdf path")
parser.add_argument('--out-dir', type=str, required=True, help="Output dir")
args = parser.parse_args()
pdf_path = args.pdf
out_dir = args.out_dir

assert pdf_path is not None
assert out_dir is not None

print(f"{pdf_path=} {out_dir=}")

images = pdf_util.doc_to_images(fitz.Document(pdf_path))

for (i, image) in enumerate(images):
    image.save(os.path.join(out_dir, f"{i}.png"), format="png")


