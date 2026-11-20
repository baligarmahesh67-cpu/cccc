"""Flask application for the Basic Crop Recommendation System."""
from flask import Flask, jsonify, render_template, request
from recommender import InputValidationError, recommend_crops

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024  # Keep the small JSON API request bounded.


@app.after_request
def add_security_headers(response):
    """Add a small set of safe defaults for browser responses."""
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
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
    return jsonify({"error": "Method not allowed."}), 405


if __name__ == "__main__":
    # Local development only. Render uses Gunicorn (see render.yaml).
    app.run(host="127.0.0.1", port=5000, debug=False)
