"""Flask application for the Basic Crop Recommendation System."""
import os

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge

from recommender import InputValidationError, recommend_crops

app = Flask(__name__)
# Flask 3 stores JSON settings on app.json; JSON_SORT_KEYS is kept for older
# Flask releases but is no longer read by current versions.
app.config["JSON_SORT_KEYS"] = False
app.json.sort_keys = False
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024  # Keep the small JSON API request bounded.


@app.after_request
def add_security_headers(response):
    """Add safe browser defaults to every response."""
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; font-src 'self'; connect-src 'self'; "
        "frame-ancestors 'none'; base-uri 'self'; form-action 'self'",
    )
    if request.path.startswith("/api/"):
        response.headers.setdefault("Cache-Control", "no-store")
    return response


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "basic-crop-recommendation"}), 200


@app.post("/api/recommend")
def api_recommend():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Send the form values as a JSON object."}), 400

    try:
        results = recommend_crops(payload)
    except InputValidationError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({
        "recommendations": results,
        "count": len(results),
        "notice": (
            "Educational screening only. Confirm crop variety, sowing date, soil test, "
            "local weather and district-specific advice with your Krishi Vigyan Kendra "
            "or agriculture department before planting."
        ),
    }), 200


@app.errorhandler(404)
def not_found(_error):
    if request.path.startswith("/api/"):
        return jsonify({"error": "API endpoint not found."}), 404
    return render_template("index.html"), 404


@app.errorhandler(405)
def method_not_allowed(_error):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Method not allowed."}), 405
    return render_template("index.html"), 405


@app.errorhandler(RequestEntityTooLarge)
def request_too_large(_error):
    return jsonify({"error": "Request body is too large. Send only the four form values."}), 413


if __name__ == "__main__":
    # Local development only. Render uses Gunicorn (see render.yaml).
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
