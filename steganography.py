"""LSB image steganography: hide and extract UTF-8 text in the low bits of PNG pixels.

Encoding changes the least-significant bit of each R/G/B channel to carry one
message bit. A 16-bit terminator (1111111111111110) marks the end of the message.
Lossless formats only (PNG/BMP) — JPEG re-compression destroys the hidden bits.
"""

from __future__ import annotations

import argparse

from PIL import Image

TERMINATOR = "1111111111111110"


def _bits(message: str) -> str:
    data = message.encode("utf-8")
    return "".join(format(byte, "08b") for byte in data) + TERMINATOR


def encode(image_path: str, message: str, output_path: str) -> None:
    img = Image.open(image_path).convert("RGB")
    bits = _bits(message)
    capacity = img.width * img.height * 3
    if len(bits) > capacity:
        raise ValueError(f"message needs {len(bits)} bits but image holds only {capacity}")

    pixels = list(img.getdata())
    out: list[tuple[int, int, int]] = []
    i = 0
    for pixel in pixels:
        channels = list(pixel)
        for c in range(3):
            if i < len(bits):
                channels[c] = (channels[c] & ~1) | int(bits[i])
                i += 1
        out.append(tuple(channels))
    img.putdata(out)
    img.save(output_path)


def decode(image_path: str) -> str:
    img = Image.open(image_path).convert("RGB")
    bits = ""
    for pixel in img.getdata():
        for c in range(3):
            bits += str(pixel[c] & 1)
            if bits.endswith(TERMINATOR):
                payload = bits[: -len(TERMINATOR)]
                by = bytes(int(payload[j : j + 8], 2) for j in range(0, len(payload) - len(payload) % 8, 8))
                return by.decode("utf-8", errors="replace")
    raise ValueError("no hidden message found")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="LSB image steganography")
    sub = ap.add_subparsers(dest="cmd", required=True)
    enc = sub.add_parser("encode", help="hide a message")
    enc.add_argument("image")
    enc.add_argument("message")
    enc.add_argument("-o", "--output", default="encoded.png")
    dec = sub.add_parser("decode", help="extract a message")
    dec.add_argument("image")
    args = ap.parse_args(argv)

    if args.cmd == "encode":
        encode(args.image, args.message, args.output)
        print(f"Message hidden in {args.output}")
    else:
        print(decode(args.image))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
