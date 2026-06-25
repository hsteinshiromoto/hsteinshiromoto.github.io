from __future__ import annotations

import argparse
import base64
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.append(str(PROJECT_ROOT))


def save(output_path: Path, object: Any):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.is_dir():
        output_path.rmdir()

    print(f"Saved: {output_path}")

    object.write(str(output_path), xml_declaration=True, encoding="unicode")


def embed_logo(qr_path: Path, logo_path: Path, output_path: Path, logo_size_pct=0.25):
    # Parse QR SVG
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree = ET.parse(str(qr_path))
    root = tree.getroot()
    ns = "http://www.w3.org/2000/svg"

    # Get QR dimensions from viewBox (coordinate space) if available, else from width/height
    if "viewBox" in root.attrib:
        _, _, width, height = map(float, root.attrib["viewBox"].split())
    else:
        width = float(re.sub(r"[^\d.]", "", root.attrib["width"]))
        height = float(re.sub(r"[^\d.]", "", root.attrib["height"]))

    # Logo dimensions (centered)
    logo_w = width * logo_size_pct
    logo_h = height * logo_size_pct
    x = (width - logo_w) / 2
    y = (height - logo_h) / 2

    if logo_path.suffix == ".svg":
        # Inline SVG logo via <image> with base64
        with logo_path.open("rb") as f:
            data = base64.b64encode(f.read()).decode()
        mime = "image/svg+xml"
    else:
        # Raster fallback (PNG/JPG)
        with logo_path.open("rb") as f:
            data = base64.b64encode(f.read()).decode()
        mime = "image/png"

    # Add white background square behind logo
    rect = ET.SubElement(root, f"{{{ns}}}rect")
    rect.attrib = {
        "x": str(x),
        "y": str(y),
        "width": str(logo_w),
        "height": str(logo_h),
        "fill": "white",
    }

    # Embed logo
    img = ET.SubElement(root, f"{{{ns}}}image")
    img.attrib = {
        "href": f"data:{mime};base64,{data}",
        "x": str(x),
        "y": str(y),
        "width": str(logo_w),
        "height": str(logo_h),
    }

    save(output_path=output_path, object=tree)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command Line Interface")
    parser.add_argument(
        "--qrcode_path",
        type=Path,
        default=PROJECT_ROOT / "assets" / "images" / "qr.svg",
        help="Path to qrcode image file. Usage `--qrcode_path='path/to/qrcode.svg`",
    )
    parser.add_argument(
        "--logo_path",
        type=Path,
        default=PROJECT_ROOT / "assets" / "images" / "logo.svg",
        help="Path to logo image file. Usage `--logo_path='path/to/logo.svg`",
    )
    parser.add_argument(
        "--output_path",
        type=Path,
        default=PROJECT_ROOT / "assets" / "images" / "qr_logo.svg",
        help="Path to logo image file. Usage `--output_path='path/to/logo.svg`",
    )

    args = parser.parse_args()

    embed_logo(
        qr_path=args.qrcode_path, logo_path=args.logo_path, output_path=args.output_path
    )
