
import requests

from config import API_BASE_URL, API_KEY, validate_config


class CallMissedAPIError(Exception):
    """Raised when the CallMissed API returns an error."""


def _request(method, path, **kwargs):
    validate_config()

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
    }

    if "json" in kwargs:
        headers["Content-Type"] = "application/json"

    try:
        response = requests.request(
            method=method,
            url=f"{API_BASE_URL}{path}",
            headers=headers,
            timeout=(5, 30),
            **kwargs,
        )
    except requests.RequestException:
        raise CallMissedAPIError(
            "Could not connect to CallMissed. Check your connection."
        ) from None

    if not response.ok:
        error_message = "No error details provided."

        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                details = error_data.get("error", error_data.get("message"))

                if isinstance(details, dict):
                    details = details.get("message")

                if isinstance(details, str) and details.strip():
                    error_message = details.strip()[:300]
        except ValueError:
            pass

        raise CallMissedAPIError(
            f"CallMissed returned HTTP {response.status_code}: "
            f"{error_message}"
        )

    try:
        return response.json()
    except ValueError:
        raise CallMissedAPIError(
            "CallMissed returned an unexpected response format."
        ) from None


def get_models():
    return _request("GET", "/models")


def send_chat_message(message, model):
    if not isinstance(message, str) or not message.strip():
        raise ValueError("Message cannot be empty.")

    if not isinstance(model, str) or not model.strip():
        raise ValueError("A model must be selected.")

    return _request(
        "POST",
        "/chat/completions",
        json={
            "model": model,
            "messages": [
                {"role": "user", "content": message.strip()}
            ],
            "max_tokens": 1000,
        },
    )


def extract_chat_text(result):
    """Extract readable text from common chat response formats."""
    if not isinstance(result, dict):
        return None

    choices = result.get("choices", [])

    if not choices or not isinstance(choices[0], dict):
        return None

    message = choices[0].get("message", {})
    if not isinstance(message, dict):
        return None

    content = message.get("content")

    if isinstance(content, str) and content.strip():
        return content.strip()

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])

        text = "\n".join(parts).strip()
        if text:
            return text

    if isinstance(message.get("text"), str):
        text = message["text"].strip()
        if text:
            return text

    return None


def generate_image(prompt):
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Image prompt cannot be empty.")

    if len(prompt) > 1000:
        raise ValueError("Image prompt is too long.")

    return _request(
        "POST",
        "/images/generations",
        json={
            "model": "flux-2-pro",
            "prompt": prompt.strip(),
            "n": 1,
            "size": "1024x1024",
        },
    )


def create_voice_session():
    return _request(
        "POST",
        "/voice/sessions",
        json={
            "system_prompt": (
                "You are a helpful voice assistant. "
                "Keep answers concise and friendly."
            ),
            "greeting": "Hello! Welcome to CallMissed AI Studio. How can I help?",
            "voice": "shubh",
            "language": "en-IN",
            "max_duration_seconds": 60,
            "stt_model": "whisper-large-v3-turbo",
            "stt_model": "saaras:v4",
        },
    )
