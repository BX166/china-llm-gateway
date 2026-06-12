# -*- coding: utf-8 -*-
"""Kling AI video generation API wrapper.
JWT HS256 auth, auto-refresh every 30 min.
Pricing: ¥0.49/sec (std), ¥0.98/sec (pro)
"""
import time
import hmac
import hashlib
import json
import requests

API_BASE = "https://api-beijing.klingai.com"
AK = "AhBdGfbDeR9FrbpGaBanH3npmg4GHL4f"
SK = "FYyTLrYbmtNMFYbATeeLyTkDMB8kThrt"


class KlingAPI:
    def __init__(self):
        self._token = None
        self._token_expiry = 0

    def _get_token(self):
        """Generate JWT token, valid 30 min."""
        now = int(time.time())
        if self._token and now < self._token_expiry - 60:
            return self._token

        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "iss": AK,
            "exp": now + 1800,
            "nbf": now,
            "iat": now,
        }

        def b64(s):
            import base64
            return base64.urlsafe_b64encode(
                s.encode() if isinstance(s, str) else s
            ).rstrip(b"=").decode()

        h = b64(json.dumps(header, separators=(",", ":")))
        p = b64(json.dumps(payload, separators=(",", ":")))
        sig = b64(hmac.new(SK.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest())

        self._token = f"{h}.{p}.{sig}"
        self._token_expiry = now + 1800
        return self._token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/json",
        }

    def text2video(
        self,
        prompt,
        model="kling-v1-6",
        duration="5",
        mode="pro",
        aspect_ratio="16:9",
        cfg_scale=0.5,
        negative_prompt="",
    ):
        """Submit a text-to-video generation task."""
        body = {
            "model_name": model,
            "prompt": prompt,
            "duration": str(duration),
            "mode": mode,
            "aspect_ratio": aspect_ratio,
            "cfg_scale": cfg_scale,
        }
        if negative_prompt:
            body["negative_prompt"] = negative_prompt

        r = requests.post(
            f"{API_BASE}/v1/videos/text2video",
            headers=self._headers(),
            json=body,
            timeout=30,
        )
        return r.json()

    def image2video(
        self,
        image_url,
        prompt="",
        model="kling-v1-6",
        duration="5",
        mode="pro",
        cfg_scale=0.5,
    ):
        """Submit an image-to-video generation task."""
        body = {
            "model_name": model,
            "image": image_url,
            "prompt": prompt,
            "duration": str(duration),
            "mode": mode,
            "cfg_scale": cfg_scale,
        }
        r = requests.post(
            f"{API_BASE}/v1/videos/image2video",
            headers=self._headers(),
            json=body,
            timeout=30,
        )
        return r.json()

    def query_task(self, task_id):
        """Query a text2video task status."""
        r = requests.get(
            f"{API_BASE}/v1/videos/text2video/{task_id}",
            headers=self._headers(),
            timeout=15,
        )
        return r.json()

    def query_image2video_task(self, task_id):
        """Query an image2video task status."""
        r = requests.get(
            f"{API_BASE}/v1/videos/image2video/{task_id}",
            headers=self._headers(),
            timeout=15,
        )
        return r.json()

    def poll(self, task_id, interval=10, timeout=900, is_image2video=False):
        """Poll a task until completion or timeout."""
        started = time.time()
        while True:
            if is_image2video:
                r = self.query_image2video_task(task_id)
            else:
                r = self.query_task(task_id)

            data = r.get("data", {})
            status = data.get("task_status", "unknown")
            elapsed = int(time.time() - started)

            print(f"  {status.upper()}... ({elapsed}s elapsed)")

            if status == "succeed":
                return r
            elif status == "failed":
                raise RuntimeError(
                    f"Task failed: {json.dumps(r, ensure_ascii=False)}"
                )

            if elapsed > timeout:
                raise TimeoutError(f"Task {task_id} timed out after {timeout}s")

            time.sleep(interval)

    def download_video(self, url, output_path):
        """Download video from URL to local path."""
        r = requests.get(url, timeout=120, stream=True)
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return output_path
