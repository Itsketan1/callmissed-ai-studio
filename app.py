
from flask import Flask, jsonify, render_template, request

from services.callmissed_client import (
    send_chat_message,
    generate_image,
    extract_chat_text,
    create_voice_session,
    CallMissedAPIError,
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

CHAT_MODEL = "sarvam-105b"


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Please enter a message."}), 400

    message = message.strip()

    if len(message) > 4000:
        return jsonify({
            "error": "Message is too long (maximum 4000 characters)."
        }), 400

    try:
        result = send_chat_message(message, CHAT_MODEL)

        if not isinstance(result, dict):
            app.logger.warning("Unexpected chat response type.")
            return jsonify({
                "error": "The AI returned an unexpected response."
            }), 502

        answer = extract_chat_text(result)

        if not answer:
            # Log metadata only, never the full response or API key.
            choices = result.get("choices", [])
            finish_reason = None

            if choices and isinstance(choices[0], dict):
                finish_reason = choices[0].get("finish_reason")

            app.logger.warning(
                "Chat response had no readable text. "
                "Response keys: %s; finish_reason: %s",
                list(result.keys()),
                finish_reason,
            )

            return jsonify({
                "error": (
                    "The model returned no readable text. "
                    "Please try again."
                )
            }), 502

        return jsonify({"reply": answer})

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    except CallMissedAPIError as exc:
        app.logger.warning(
            "CallMissed chat request failed: %s", str(exc)
        )
        return jsonify({
            "error": "The AI service request failed. Please try again."
        }), 502

    except Exception:
        app.logger.exception("Unexpected error in chat endpoint.")
        return jsonify({
            "error": "An unexpected server error occurred."
        }), 500


@app.post("/api/images")
def create_image():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "")

    if not isinstance(prompt, str) or not prompt.strip():
        return jsonify({
            "error": "Please describe the image."
        }), 400

    prompt = prompt.strip()

    if len(prompt) > 1000:
        return jsonify({
            "error": "Prompt must be 1000 characters or fewer."
        }), 400

    try:
        result = generate_image(prompt)

        if not isinstance(result, dict):
            return jsonify({
                "error": "The image service returned an unexpected response."
            }), 502

        images = result.get("data", [])

        if not images or not isinstance(images[0], dict):
            return jsonify({
                "error": "No image was returned."
            }), 502

        image = images[0]
        output = {}

        if isinstance(image.get("url"), str):
            output["url"] = image["url"]

        elif isinstance(image.get("b64_json"), str):
            output["b64_json"] = image["b64_json"]

        else:
            return jsonify({
                "error": "The service returned an unsupported image format."
            }), 502

        return jsonify(output)

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    except CallMissedAPIError as exc:
        app.logger.warning(
            "CallMissed image request failed: %s", str(exc)
        )
        return jsonify({
            "error": "Image generation failed. Please check the server logs."
        }), 502

    except Exception:
        app.logger.exception("Unexpected error in image endpoint.")
        return jsonify({
            "error": "An unexpected server error occurred."
        }), 500



@app.post("/api/voice/session")
def voice_session():
    try:
        result = create_voice_session()

        if not isinstance(result, dict):
            return jsonify({
                "error": "Unexpected voice-session response."
            }), 502

        ws_url = result.get("ws_url")
        token = result.get("token")
        session_id = result.get("id")

        if not all(
            isinstance(value, str) and value
            for value in (ws_url, token)
        ):
            app.logger.warning(
                "Voice-session response missing connection details."
            )
            return jsonify({
                "error": "The voice service returned incomplete session details."
            }), 502

        # The token is returned only to this browser session.
        # Never log it or expose the permanent API key.
        return jsonify({
            "ws_url": ws_url,
            "token": token,
            "session_id": session_id,
        })

    except CallMissedAPIError as exc:
        app.logger.warning("Voice-session request failed: %s", str(exc))
        return jsonify({
            "error": "Could not create a voice session. Check server logs."
        }), 502

    except Exception:
        app.logger.exception("Unexpected voice-session error.")
        return jsonify({
            "error": "An unexpected server error occurred."
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
    )
