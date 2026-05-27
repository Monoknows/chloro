import os
import json
import subprocess
import urllib.error
import urllib.request


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
OPENCLAW_CONFIG = os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json")
GATEWAY_URL = os.getenv(
    "OPENCLAW_GATEWAY_URL",
    "http://127.0.0.1:18789/v1/chat/completions",
)
MODEL = os.getenv("CHLORO_MODEL", "openclaw/default")

SYSTEM_PROMPT = """
You are CHLORO, Sir's personal AI assistant.

Style:
- Address the user as Sir.
- Be composed, capable, fast, and practical.
- Be bluntly honest when something is wrong, unsafe, vague, or likely to fail.
- Keep spoken answers short unless the user asks for detail.
- Never claim to be Qwen, ChatGPT, Alibaba, OpenAI, or any other model identity.

Safety:
- Do not generate raw Windows batch, PowerShell, shell, or Python for automatic execution.
- Do not claim you can directly control the computer unless the local CHLORO app has explicitly implemented that action.
- For risky actions such as deleting files, installing software, changing security settings, sending messages, or posting online, say that approval is needed first.
""".strip()

APP_LAUNCHERS = {
    "vscode": ("Visual Studio Code", ["code", PROJECT_ROOT]),
    "vs code": ("Visual Studio Code", ["code", PROJECT_ROOT]),
    "visual studio code": ("Visual Studio Code", ["code", PROJECT_ROOT]),
    "spotify": ("Spotify", "spotify:"),
    "notepad": ("Notepad", ["notepad.exe"]),
    "calculator": ("Calculator", ["calc.exe"]),
    "file explorer": ("File Explorer", ["explorer.exe", PROJECT_ROOT]),
    "explorer": ("File Explorer", ["explorer.exe", PROJECT_ROOT]),
}


def _open_uri(uri):
    os.startfile(uri)


def _launch(command):
    if isinstance(command, str):
        _open_uri(command)
    else:
        subprocess.Popen(command)


def handle_local_action(question):
    normalized = question.strip().lower()
    if not normalized.startswith(("open ", "launch ", "start ")):
        return None

    for app_name, (display_name, command) in APP_LAUNCHERS.items():
        if app_name in normalized:
            try:
                _launch(command)
                return f"Opening {display_name}, Sir."
            except FileNotFoundError:
                return f"I could not find {display_name} on this machine, Sir."
            except OSError as exc:
                return f"I could not open {display_name}, Sir. {exc}"

    return None


def _load_gateway_auth_header():
    token = os.getenv("OPENCLAW_GATEWAY_TOKEN") or os.getenv("OPENCLAW_GATEWAY_PASSWORD")
    if not token and os.path.exists(OPENCLAW_CONFIG):
        try:
            with open(OPENCLAW_CONFIG, "r", encoding="utf-8") as config_file:
                config = json.load(config_file)
            auth_config = config.get("gateway", {}).get("auth", {})
            token = auth_config.get("token") or auth_config.get("password")
        except (OSError, json.JSONDecodeError, TypeError):
            token = None

    if token:
        return {"Authorization": f"Bearer {token}"}

    return {}


def ask_gateway(question):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        "stream": False,
    }

    request = urllib.request.Request(
        GATEWAY_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            **_load_gateway_auth_header(),
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=25) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["choices"][0]["message"]["content"].strip()


def ask_chloro(question):
    local_response = handle_local_action(question)
    if local_response:
        return local_response

    try:
        return ask_gateway(question)
    except (urllib.error.URLError, TimeoutError) as exc:
        return f"I cannot reach the OpenClaw gateway right now, Sir. {exc}"
    except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
        return f"The OpenClaw gateway returned an unexpected response, Sir. {exc}"
