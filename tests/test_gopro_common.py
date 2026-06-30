from cloudberry.common import parse_media_page


def test_parse_media_page_extracts_jpg_files():
    content = """<?xml version="1.0" encoding="UTF-8"?>
    <html><body><div><div><table><tbody><tr>
      <td><a>GOPR0001.JPG</a></td><td><span>01-Jan-2024 12:00</span></td>
    </tr><tr>
      <td><a>GOPR0002.JPG</a></td><td><span>02-Jan-2024 13:00</span></td>
    </tr></tbody></table></div></div></body></html>"""

    images = parse_media_page(content)

    assert len(images) == 2
    assert images[0]["name"] == "GOPR0001.JPG"
    assert images[1]["name"] == "GOPR0002.JPG"
