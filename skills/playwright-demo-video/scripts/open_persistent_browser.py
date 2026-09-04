from __future__ import annotations

import argparse
import os
import re
import time
from pathlib import Path

from playwright.sync_api import Error, sync_playwright


PROFILE_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def parse_args() -> argparse.Namespace:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        raise RuntimeError("LOCALAPPDATA is required on Windows.")

    parser = argparse.ArgumentParser(
        description="Open Chrome or Edge with a dedicated persistent profile."
    )
    parser.add_argument("--profile-name", default="demo-video")
    parser.add_argument("--browser", choices=("chrome", "msedge"), default="chrome")
    parser.add_argument("--url", default="about:blank")
    parser.add_argument(
        "--profile-root",
        type=Path,
        default=Path(local_app_data) / "ms-playwright-demo-video",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not PROFILE_NAME_PATTERN.fullmatch(args.profile_name):
        raise ValueError(
            "Profile names may contain only letters, numbers, dots, underscores, "
            "and hyphens."
        )

    profile_dir = args.profile_root / args.profile_name
    profile_dir.mkdir(parents=True, exist_ok=True)

    print(f"Opening {args.browser} with dedicated profile: {profile_dir}")
    print("Complete SSO in the browser. No credentials are read or logged.")
    print("Close the browser normally when authentication is complete.")

    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            channel=args.browser,
            headless=False,
            viewport={"width": 1440, "height": 900},
            color_scheme="light",
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(args.url, wait_until="domcontentloaded")

        try:
            while context.pages:
                context.pages[0].wait_for_timeout(1_000)
                time.sleep(0)
        except Error:
            pass
        finally:
            try:
                context.close()
            except Error:
                pass


if __name__ == "__main__":
    main()
