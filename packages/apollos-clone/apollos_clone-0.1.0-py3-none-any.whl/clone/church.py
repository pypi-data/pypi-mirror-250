import os
from dataclasses import dataclass
from functools import cached_property

import requests


@dataclass
class Church:
    slug: str

    @cached_property
    def configs(self):
        api_key = os.getenv("APOLLOS_API_KEY")
        if not api_key:
            raise ValueError("APOLLOS_API_KEY environment variable must be set")
        response = requests.get(
            f"https://apollos-cluster-production.herokuapp.com/api/config/{self.slug}",
            headers={"x-api-key": api_key},
        )
        response.raise_for_status()
        return response.json()

    icon_bg = property(
        lambda self: self.configs["APP.THEME"]["value"]["colors"]["primary"]
    )
    icon_url = property(lambda self: self.configs["APP.ICON_URL"]["value"])
    wordmark_url = property(lambda self: self.configs["APP.WORDMARK_URL"]["value"])
