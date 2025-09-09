import json
import os
from typing import Optional

import redis
from flask import Flask, request, jsonify

from pyfinn import fetch_ad, scrape_ad

app = Flask(__name__)

# Use REDIS_URL from environment so Vercel can point to a managed Redis service.
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
try:
    redis_service: Optional[redis.Redis] = redis.from_url(REDIS_URL)
except Exception:
    redis_service = None

cache_duration = int(os.getenv("CACHE_DURATION_SECONDS", 23 * 60 * 60))


@app.route("/", methods=["GET"])
def ad_detail():
    finnkode = request.args.get("finnkode")
    if not finnkode or not finnkode.isdigit():
        return jsonify(**{"error": "Missing or invalid param finnkode. Try /?finnkode=KODE"})

    cache_key = f"finn-ad-v2:{finnkode}"
    ad = None
    if redis_service:
        try:
            ad = redis_service.get(cache_key)
        except Exception:
            # If Redis is unreachable, proceed without caching
            ad = None

    if not ad:
        url = f"https://www.finn.no/realestate/homes/ad.html?finnkode={finnkode}"
        html = fetch_ad(url)
        ad = scrape_ad(html)
        if redis_service:
            try:
                redis_service.set(cache_key, json.dumps({"url": url} | ad), cache_duration)
            except Exception:
                # best-effort caching
                pass
    else:
        ad = json.loads(ad)

    return jsonify(ad=ad)


if __name__ == "__main__":
    # Local dev run
    app.run(debug=True)
