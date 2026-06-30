#!/usr/bin/env python3
"""Publish a Hugging Face community post (huggingface.co/posts) with GIF attachment."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "app" / "assets" / "hf_community_post_draft.txt"
GIF = ROOT / "app" / "assets" / "flux_flywheel_demo.gif"
SPACE_GIF_URL = (
    "https://huggingface.co/spaces/kinaar111/kingdom/resolve/main/"
    "app/assets/flux_flywheel_demo.gif"
)


def _token() -> str:
    return subprocess.check_output(["hf", "auth", "token"], text=True).strip()


def _parse_draft(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    title_m = re.search(r"^TITLE:\s*\n(.+)$", text, re.M)
    body_m = re.search(r"BODY \(paste below\):\s*\n\n(.+)$", text, re.S)
    if not title_m or not body_m:
        raise ValueError(f"Could not parse draft at {path}")
    title = title_m.group(1).strip()
    body = body_m.group(1).strip()
    body = body.replace("*(GIF above tours He → Fe → Au → Z=129.)*", "")
    body = f"{body}\n\n![Flux Flywheel demo]({SPACE_GIF_URL})"
    return title, body


def _driver() -> webdriver.Firefox:
    opts = Options()
    opts.add_argument("-headless")
    opts.set_preference("dom.webnotifications.enabled", False)
    opts.set_preference("media.volume_scale", "0.0")
    service = Service("/snap/bin/geckodriver")
    return webdriver.Firefox(service=service, options=opts)


def _api_create(token: str, raw_content: str, gif_path: Path) -> dict | None:
    """Try undocumented internal endpoints via in-page fetch (same-origin session)."""
    import urllib.error
    import urllib.request

    # 1) upload attachment if endpoint exists
    attachment_url = None
    upload_targets = [
        "https://huggingface.co/api/settings/post-attachments",
        "https://huggingface.co/api/post-attachments",
        "https://huggingface.co/api/settings/attachments",
    ]
    boundary = "----KingdomComeBoundary7MA4YWxk"
    gif_bytes = gif_path.read_bytes()
    for upload_url in upload_targets:
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{gif_path.name}"\r\n'
            f"Content-Type: image/gif\r\n\r\n"
        ).encode() + gif_bytes + f"\r\n--{boundary}--\r\n".encode()
        req = urllib.request.Request(
            upload_url,
            data=body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode())
                attachment_url = payload.get("url") or payload.get("fileUrl")
                if attachment_url:
                    break
        except urllib.error.HTTPError:
            continue
        except Exception:
            continue

    payload = {"rawContent": raw_content}
    if attachment_url:
        payload["attachments"] = [{"type": "image", "url": attachment_url}]

    create_targets = [
        "https://huggingface.co/api/posts/publish",
        "https://huggingface.co/api/posts",
        "https://huggingface.co/api/settings/posts",
        "https://huggingface.co/api/users/kinaar111/post",
    ]
    for url in create_targets:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as err:
            if err.code not in (404, 405):
                try:
                    detail = err.read().decode()
                except Exception:
                    detail = str(err)
                print(f"API {url} -> {err.code}: {detail[:300]}", file=sys.stderr)
        except Exception as exc:
            print(f"API {url} failed: {exc}", file=sys.stderr)
    return None


def _browser_create(token: str, raw_content: str, gif_path: Path) -> str:
    driver = _driver()
    wait = WebDriverWait(driver, 25)
    try:
        driver.get("https://huggingface.co/")
        driver.execute_script(
            """
            window.localStorage.setItem('hf_token', arguments[0]);
            window.localStorage.setItem('HF_TOKEN', arguments[0]);
            """,
            token,
        )

        # Authenticated fetch helper in-page
        result = driver.execute_async_script(
            """
            const token = arguments[0];
            const rawContent = arguments[1];
            const done = arguments[arguments.length - 1];
            const headers = {
              'Authorization': 'Bearer ' + token,
              'Content-Type': 'application/json',
            };
            const tries = [
              '/api/posts',
              '/api/posts/publish',
              '/api/settings/posts',
            ];
            (async () => {
              for (const path of tries) {
                try {
                  const res = await fetch(path, {method: 'POST', headers, body: JSON.stringify({rawContent})});
                  const text = await res.text();
                  if (res.ok) {
                    done({ok: true, path, body: text});
                    return;
                  }
                  done({ok: false, path, status: res.status, body: text.slice(0, 500)});
                  return;
                } catch (e) {
                  done({ok: false, path, error: String(e)});
                  return;
                }
              }
            })();
            """,
            token,
            raw_content,
        )
        if isinstance(result, dict) and result.get("ok"):
            body = json.loads(result["body"]) if result.get("body") else {}
            slug = body.get("slug") or body.get("socialPost", {}).get("slug")
            if slug:
                return f"https://huggingface.co/posts/kinaar111/{slug}"

        driver.get("https://huggingface.co/posts")
        time.sleep(2)

        # Look for compose UI controls (Pro users)
        compose_selectors = [
            "button[data-testid='create-post']",
            "a[href*='new-post']",
            "button:contains('Post')",
            "[aria-label='Create post']",
            "textarea",
            "[contenteditable='true']",
        ]
        for sel in compose_selectors:
            try:
                if sel.startswith("button:contains"):
                    els = driver.find_elements(By.XPATH, "//button[contains(., 'Post')]")
                else:
                    els = driver.find_elements(By.CSS_SELECTOR, sel)
                if els:
                    els[0].click()
                    break
            except Exception:
                continue

        # File input for GIF
        file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
        if file_inputs:
            file_inputs[0].send_keys(str(gif_path.resolve()))

        editors = driver.find_elements(By.CSS_SELECTOR, "textarea, [contenteditable='true']")
        if editors:
            editors[0].click()
            editors[0].send_keys(raw_content)
        else:
            raise RuntimeError("Compose editor not found — HF Posts UI may require interactive login.")

        for sel in ["button[type='submit']", "button[data-testid='submit-post']"]:
            buttons = driver.find_elements(By.CSS_SELECTOR, sel)
            if buttons:
                buttons[0].click()
                break
        else:
            buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Publish') or contains(., 'Post')]")
            if not buttons:
                raise RuntimeError("Publish button not found.")
            buttons[-1].click()

        wait.until(lambda d: "/posts/kinaar111/" in d.current_url)
        return driver.current_url
    finally:
        driver.quit()


def main() -> None:
    if not DRAFT.exists():
        raise SystemExit(f"Missing draft: {DRAFT}")
    if not GIF.exists():
        raise SystemExit(f"Missing GIF: {GIF}")

    _title, body = _parse_draft(DRAFT)
    token = _token()

    api_result = _api_create(token, body, GIF)
    if api_result:
        slug = api_result.get("slug") or api_result.get("socialPost", {}).get("slug")
        if slug:
            print(f"Posted via API: https://huggingface.co/posts/kinaar111/{slug}")
            return
        print(json.dumps(api_result, indent=2)[:2000])

    try:
        url = _browser_create(token, body, GIF)
        print(f"Posted via browser: {url}")
    except TimeoutException as exc:
        raise SystemExit(
            "Could not publish HF community post automatically. "
            "HF /posts has no public create API; browser compose requires an interactive web session. "
            f"Last error: {exc}"
        ) from exc


if __name__ == "__main__":
    main()