from functools import cache
from io import BytesIO

import requests
from PIL import Image


@cache
def get_network_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))


def create_graphic(width, height, logo_height, bg_color, source_url, dest):
    img = Image.new("RGBA", (width, height), color=bg_color)

    logo = get_network_image(source_url).convert("RGBA")
    scale = logo_height / logo.size[1]
    logo_width = int(logo.size[0] * scale)
    logo = logo.resize((logo_width, logo_height), Image.LANCZOS)

    img.paste(logo, ((width - logo_width) // 2, (height - logo_height) // 2), logo)
    img.save(dest)
    print(f"Created {dest}")


def generate_play_store_assets(icon_bg, icon_url, wordmark_url):
    create_graphic(
        512,
        512,
        450,
        icon_bg,
        icon_url,
        "fastlane/metadata/android/en-US/images/icon.png",
    )
    create_graphic(
        1024,
        500,
        120,
        "#ffffff",
        wordmark_url,
        "fastlane/metadata/android/en-US/images/featureGraphic.png",
    )
