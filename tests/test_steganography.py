from PIL import Image

from steganography import decode, encode


def test_round_trip(tmp_path):
    src = tmp_path / "src.png"
    out = tmp_path / "out.png"
    Image.new("RGB", (64, 64), (120, 200, 80)).save(src)
    secret = "Hello, World! unicode: café ☕"
    encode(str(src), secret, str(out))
    assert decode(str(out)) == secret


def test_capacity_error(tmp_path):
    src = tmp_path / "tiny.png"
    Image.new("RGB", (2, 2), (0, 0, 0)).save(src)
    import pytest
    with pytest.raises(ValueError):
        encode(str(src), "way too long for four pixels", str(tmp_path / "x.png"))
