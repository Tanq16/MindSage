# MindSage

<h1 align="center">
  <br>
  <img src=".github/logo.png" alt="MS" width="425"></a>
  <br>MindSage<br>
</h1>

MindSage is a simplistic and limited clone of [Fabric](https://github.com/danielmiessler/fabric/tree/main) by Daniel Miessler.

This project is meant to provide a Docker image that sets up a limited-version of Fabric's API server on a home network. The provided `client.py` can be used to connect to the server from various machines in the same network. Additionally, the accepted arguments have been modified to be simplistic so the API can be called from Siri shortcuts as well.

## Usage

The intended usage is by deploying as a Docker container like so &rarr;

```bash
docker run -p 5000:5000 -e "OPENAI_API_KEY=sk-proj-XXXX" --rm -it tanq16/mindsage:latest
```

> Keep in mind the above image is for x86-64 only. You need to build one for ARM64.

A better method is to deploy using Docker compose or a deployment manager like [Dockge](https://github.com/louislam/dockge), where the environment variables can be specified separately to not expose the key within shell history.

The accepted JSON data for interacting with a `curl` request is as follows &rarr;

```json
{
  "model":"gpt3.5",
  "link":1,
  "input":"https://youtube.com/watch?v=abcdefghijk"
}
```

Only 2 models (gpt3.5 and gpt4) are supported. The `link` variable tells it whether to accept a link or text, and the `input` variable is either the link or the text. The `client` checks for the presence of `youtu` in the link and automatically pulls the transcript if it does, i.e., only `youtube.*` and `youtu.be*` links will work (copy pasting the URL from a browser will alwaya work).

## Local Usage

If you still want to use the project locally, ensure `python3.10+` is installed and then follow these steps &rarr;

```bash
# Clone the repo
git clone https://github.com/tanq16/MindSage --depth=1 && cd MindSage
# Create Venv
python3 -m venv msenv && source msenv/bin/activate
# Install deps (yes, i didn't provide a requirements.txt)
pip install requests flask openai youtube_transcript_api
# Run the server
python server.py
```

## Add Your Flare

The current project is setup to be used in a containerized fashion with a limited number of patterns I found useful. If you want to add additional patterns in the image, add the relevant Fabric links to the `patternlist` file. Additionally, make sure to add the relevant options to the list within `client.py`. Then build using the following &rarr;

```bash
docker build -t mindsage .
```

Then, run like so &rarr;

```bash
docker run -p 5000:5000 -e "OPENAI_API_KEY=sk-proj-XXXX" --rm -it mindsage
```
