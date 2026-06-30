from cloudberry.s3 import build_object_key


def test_build_object_key_with_prefix():
    assert build_object_key("pi-123", "photo.jpg") == "pi-123/photo.jpg"


def test_build_object_key_without_prefix():
    assert build_object_key("", "photo.jpg") == "photo.jpg"
