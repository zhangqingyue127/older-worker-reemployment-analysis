from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Iterable, List

import requests
from lxml import etree


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


def extract_cid_from_html(html: str) -> int:
    """
    Extract the Bilibili CID from page HTML.

    The crawler reads the `window.__INITIAL_STATE__` object and retrieves
    the `cid` field from the embedded video metadata.
    """
    match = re.search(r"window.__INITIAL_STATE__=(.*?);", html)
    if not match:
        raise ValueError("Could not locate the Bilibili initial-state payload.")
    payload = json.loads(match.group(1))
    return int(payload["videoData"]["cid"])


def fetch_danmaku_lines(session: requests.Session, video_url: str) -> List[str]:
    """
    Download all danmaku lines for a single Bilibili video.
    """
    response = session.get(video_url, timeout=20)
    response.raise_for_status()
    cid = extract_cid_from_html(response.text)

    xml_url = f"https://comment.bilibili.com/{cid}.xml"
    xml_response = session.get(xml_url, timeout=20)
    xml_response.raise_for_status()

    root = etree.fromstring(xml_response.content)
    danmaku_nodes = root.xpath("/i/d")
    return [
        "".join(node.xpath("./text()")).strip()
        for node in danmaku_nodes
        if "".join(node.xpath("./text()")).strip()
    ]


def crawl_bilibili_videos(video_urls: Iterable[str], sleep_seconds: float = 2.0) -> List[str]:
    """
    Crawl multiple Bilibili videos and return a flat list of danmaku lines.
    """
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    all_lines: List[str] = []
    for url in video_urls:
        print(f"Fetching danmaku from: {url}")
        try:
            all_lines.extend(fetch_danmaku_lines(session, url))
        except Exception as exc:  # pragma: no cover
            print(f"Skipped {url} because of: {exc}")
        time.sleep(sleep_seconds)
    return all_lines


def save_lines(lines: Iterable[str], output_path: Path) -> None:
    """
    Save danmaku lines as one line per message.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        for line in lines:
            file.write(line.strip() + "\n")


if __name__ == "__main__":
    video_urls = [
        "https://www.bilibili.com/video/BV1mx421f75S/",
        "https://www.bilibili.com/video/BV19XtPecErH/",
        "https://www.bilibili.com/video/BV19c411z7mm/",
    ]
    lines = crawl_bilibili_videos(video_urls)
    save_lines(lines, Path("data/raw/bilibili_danmaku_crawled.txt"))
    print(f"Saved {len(lines)} danmaku lines.")
