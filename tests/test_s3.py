from pathlib import Path
from unittest.mock import MagicMock

from cloudberry.s3 import generate_presigned_url, push_picture_to_s3


def test_push_picture_to_s3_sets_content_type(tmp_path: Path):
    image = tmp_path / "photo.jpg"
    image.write_text("image", encoding="utf-8")

    client = MagicMock()
    uploaded = push_picture_to_s3(client, "bucket", "prefix/photo.jpg", image)

    assert uploaded is True
    _, kwargs = client.upload_file.call_args
    assert kwargs["ExtraArgs"]["ContentType"] == "image/jpeg"


def test_generate_presigned_url():
    client = MagicMock()
    client.generate_presigned_url.return_value = "https://example.com/photo"

    url = generate_presigned_url(client, "bucket", "prefix/photo.jpg")

    assert url == "https://example.com/photo"
    client.generate_presigned_url.assert_called_once()


def test_push_picture_to_s3_retries_and_succeeds(tmp_path: Path):
    image = tmp_path / "photo.jpg"
    image.write_text("image", encoding="utf-8")

    client = MagicMock()
    client.upload_file.side_effect = [Exception("network"), None]

    uploaded = push_picture_to_s3(
        client,
        "bucket",
        "prefix/photo.jpg",
        image,
        make_public=True,
        max_retries=2,
    )

    assert uploaded is True
    assert client.upload_file.call_count == 2
    _, kwargs = client.upload_file.call_args
    assert kwargs["ExtraArgs"]["ACL"] == "public-read"
    assert kwargs["ExtraArgs"]["ContentType"] == "image/jpeg"
