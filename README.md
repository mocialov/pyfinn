# pyfinn

Fetch real estate listings from finn.no and expose them as JSON. This repository contains a small Flask app and is prepared to run on Vercel as a serverless Python function (requires a hosted Redis instance).

## Quick overview
- Endpoint: `GET /?finnkode=KODE` — returns JSON for the finn.no listing with the given `finnkode`.
- The app uses Redis for caching when `REDIS_URL` is provided. If Redis is unavailable, the app will fetch listings on demand without caching.

## Deploying to Vercel
1. Create (or use) a hosted Redis instance (Upstash, Redis Enterprise, AWS Elasticache etc.).
2. In the Vercel project settings add an Environment Variable:
   - `REDIS_URL` — e.g. `redis://:PASSWORD@HOST:PORT/0` (Upstash gives a full URL you can paste).
3. Set build/install commands in Vercel (Project → Settings → Build & Development Settings):
   - Install Command: `pip install -r requirements.txt`
   - Build Command: leave empty (or `echo "no build"`)
4. `vercel.json` in the repo is configured to route requests to `api/wsgi.py` which exposes the Flask WSGI `app`.

Notes:
- Vercel does not run Docker or background services; you must use a managed Redis.
- The app reads `REDIS_URL` at import; if missing or unreachable, the app works without caching.

## Local development
Recommended: use a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Run the app in development mode (same behavior as `./bin/run`):

```bash
./bin/run
# or
python3 -m pyfinn.api
```

- Test a single request locally (when running the dev server):

```
curl 'http://127.0.0.1:5000/?finnkode=337819107'
```

## Tests
Run the project's tests with pytest:

```bash
pytest -q
```

## Environment variables
- `REDIS_URL` — connection string to Redis (optional for local dev; required on Vercel if you want caching).
- `CACHE_DURATION_SECONDS` — optional integer for cache TTL (defaults to 23*60*60 seconds).

## Troubleshooting
- If the function fails on Vercel with Redis connection errors, double-check the `REDIS_URL` and that the provider allows connections from Vercel. Upstash is a simple provider that works well with serverless platforms.

## Next steps (optional)
- Add a tiny README section with example Upstash steps if you want a step-by-step hosted-Redis walkthrough.
🏠 Fetch real estate listing from finn.no and make available as JSON response.

Requests to finn.no uses a randomized user agent. The response data is cached (with redis).

## Try it out

Hit the button below to create your own. You need a free Heroku account.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/nikolaik/pyfinn)

## Example usage

- [How to use the data in a Google Spreadsheet](https://medium.com/@nikolaik/samle-boligannonser-fra-finn-no-i-et-regneark-med-google-sheets-d0e4fd2ae19f) (in Norwegian)

## Installation

```bash
docker run -d -p 6379:6379 redis
./bin/run
xdg-open http://localhost:5000/
```

## Configuration

- `REDIS_URL` URL to Redis instance. Default: `redis://localhost:6379/0`
- `CACHE_DURATION_SECONDS` How long we cache ad data. Default: `23 * 60 * 60` seconds.

## Terms of use

From finn.no footer (in Norwegian):
> Innholdet er beskyttet etter åndsverksloven. Bruk av automatiserte tjenester (roboter, spidere, indeksering m.m.) samt andre fremgangsmåter for systematisk eller regelmessig bruk er ikke tillatt uten eksplisitt samtykke fra FINN.no.
