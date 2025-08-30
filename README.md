# WPRelive

A homebrew Windows Phone 7/8 HTTP API server made in Python with [Starlette](https://www.starlette.io/),
used for *Microsoft Tellme* (speech recognition) and *Bing Search* (search API, not implemented yet).

### Why?

Just for fun and giggles and learning reverse engineering.

Since Bing API servers (api.m.bing.net, appserver.m.bing.net) is dead for a very long while,
why just not resurrect the ancient tech?

### What's the goal?

To make Microsoft Tellme (Windows Phone 7/8 speech recognition) work again, even the only thing it can do is
help Tellme/Bing with search query.

### How it works?

Microsoft Tellme uses HTTP server for speech recognition, and Bing Search also uses it for search queries.
Bing Search also uses it to get Today Image as a background image, and for search in Maps app.

### What doesn't work?

- Actual speech recognition (decoding SirenSR, or GSM 6.10 8kHz Mono, and get the text from audio)
- Bing Search API (needs to investigate on `jsonwithnif` JSON responses, and `withnif` responses)
- Perhaps more stuff such as Maps search, etc.

Currently implemented services endpoints are:
- Microsoft Tellme: Voice Recognition (`/speechreco/wp/query`)
- Bing mobile search, but no responses yet (`/SearchService/Search.svc/{withnif,jsonwithnif}/`)
- Bing Today Image (`/BackgroundImageService/TodayImageService.svc/GetTodayImage`)

## Installation

Requirements:
- [Python >= 3.9](https://www.python.org/downloads/)

You need to install dependencies (preferably inside Python virtual environment, `venv`),
you can install either from requirements.txt file or with [Pipenv](https://pipenv.pypa.io/):
- Pip way: `pip install -Ur requirements.txt`
- Pipenv way: `pipenv install`
  - You also can install additional development packages by adding `--dev` key.
  - Optionally add `--deploy` for production environments.

Then you can start Uvicorn ASGI host:
```bash
uvicorn --host 0.0.0.0 --port 80 wprelive.app:app
```

You also need DNS server that will redirect `api.m.bing.net` and `appservice.m.bing.net` hostnames
to your host address.

If you are about to host locally on Windows and have Wi-Fi hotspot, you can use your PC as DNS server.
You need to append text in `%SystemRoot%\System32\drivers\etc\hosts` file:
```
<Your Host IP Address> api.m.bing.net
<Your Host IP Address> appservice.m.bing.net
```
Then turn on Wi-Fi hotspot and connect your Windows Phone to your hotspot network.

## License

WPRelive is licensed under MIT license, see [LICENSE](LICENSE) file for more details.
WPRelive is free and open source software.

This is an unofficial project, it is not made, authorized, endorsed by, or in any way offically connected
with Microsoft Corporation, or any of its subsidiaries or its affiliates.
