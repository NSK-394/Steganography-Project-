# Image Steganography (LSB)

![tests](https://github.com/NSK-394/Steganography-Project-/actions/workflows/tests.yml/badge.svg)

Hide and extract UTF-8 text messages inside an image using **Least Significant Bit (LSB)** encoding, built on Pillow.

## How it works
Each pixel has three colour channels (R, G, B), each a byte. Flipping the lowest bit of a channel changes its value by at most 1 — invisible to the eye. The tool writes the message bit-by-bit into those low bits and marks the end with a 16-bit terminator, so the decoder knows exactly where to stop.

**Capacity:** 3 bits per pixel. A 256×256 image holds ~24 KB of text.

## Usage
```bash
python steganography.py encode cover.png "meet at noon" -o secret.png
python steganography.py decode secret.png
# -> meet at noon
```

## Important
- **Lossless formats only** (PNG, BMP). JPEG re-compresses and destroys the hidden bits.
- Raises a clear error if the message is larger than the image can hold, or if no hidden message is found.
- This is **obscurity, not encryption** — anyone who suspects LSB steganography can extract the payload. Encrypt the message first if it's actually sensitive.

## Tests
```bash
pip install pytest pillow && pytest -q
```
The test encodes a unicode message into a generated image and asserts it decodes back byte-for-byte.
