import argparse

from clone.church import Church
from clone.graphics import generate_play_store_assets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("church", help="Church slug")
    parser.add_argument("--android", action="store_true")
    args = parser.parse_args()

    church = Church(args.church)
    if args.android:
        generate_play_store_assets(
            icon_bg=church.icon_bg,
            icon_url=church.icon_url,
            wordmark_url=church.wordmark_url,
        )


if __name__ == "__main__":
    main()
