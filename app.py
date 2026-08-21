import os
import json
import uuid
import mimetypes
from datetime import datetime
from flask import (
    Flask, request, jsonify, render_template, redirect,
    url_for, send_from_directory, abort, Response
)
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DB_FILE = os.path.join(BASE_DIR, "files_db.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB per upload

# ---------------------------------------------------------------------------
# Categories this hosting service supports. Each has its own allowed
# extensions so the frontend can show clear, labelled upload options.
# ---------------------------------------------------------------------------
CATEGORIES = {
    "web": {
        "label": "HTML / CSS / JavaScript files",
        "ext": {"html", "htm", "css", "js", "mjs", "json"},
    },
    "code": {
        "label": "Direct HTML code (paste & host)",
        "ext": {"html"},
    },
    "image": {
        "label": "Images",
        "ext": {"png", "jpg", "jpeg", "gif", "webp", "svg", "bmp", "ico"},
    },
    "audio": {
        "label": "Audio / Songs",
        "ext": {"mp3", "wav", "ogg", "m4a", "flac"},
    },
    "video": {
        "label": "Videos",
        "ext": {"mp4", "webm", "mov", "mkv", "avi"},
    },
    "file": {
        "label": "Any other file",
        "ext": None,  # any extension allowed
    },
}

ALL_ALLOWED_EXT = set()
for c in CATEGORIES.values():
    if c["ext"]:
        ALL_ALLOWED_EXT |= c["ext"]


# ---------------------------------------------------------------------------
# Tiny JSON "database" of everything that has been hosted so far.
# ---------------------------------------------------------------------------
def load_db():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_record(record):
    data = load_db()
    data.insert(0, record)
    save_db(data)


def guess_category(ext):
    ext = ext.lower()
    for key, meta in CATEGORIES.items():
        if key == "code" or key == "file":
            continue
        if meta["ext"] and ext in meta["ext"]:
            return key
    return "file"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    files = load_db()[:12]
    return render_template("index.html", categories=CATEGORIES, files=files)


@app.route("/projects")
def projects():
    files = [f for f in load_db() if f["category"] in ("web", "code")]
    return render_template("list.html", title="Projects", files=files)


@app.route("/portfolio")
def portfolio():
    files = load_db()
    return render_template("list.html", title="Portfolio", files=files)


@app.route("/api/files")
def api_files():
    return jsonify(load_db())


@app.route("/upload", methods=["POST"])
def upload():
    """Handles file uploads for every category (web/image/audio/video/file)."""
    if "file" not in request.files:
        return jsonify({"ok": False, "error": "No file received."}), 400

    f = request.files["file"]
    if f.filename == "":
        return jsonify({"ok": False, "error": "No file selected."}), 400

    original_name = secure_filename(f.filename)
    if "." not in original_name:
        return jsonify({"ok": False, "error": "File needs an extension."}), 400

    ext = original_name.rsplit(".", 1)[1].lower()
    category = guess_category(ext)

    slug = uuid.uuid4().hex[:10]
    stored_name = f"{slug}.{ext}"
    f.save(os.path.join(UPLOAD_DIR, stored_name))

    record = {
        "id": slug,
        "name": original_name,
        "stored_name": stored_name,
        "category": category,
        "ext": ext,
        "size": os.path.getsize(os.path.join(UPLOAD_DIR, stored_name)),
        "uploaded_at": datetime.utcnow().isoformat() + "Z",
        "url": url_for("serve_file", stored_name=stored_name, _external=False),
    }
    add_record(record)
    return jsonify({"ok": True, "file": record})


@app.route("/host-html", methods=["POST"])
def host_html():
    """Hosts raw pasted HTML code as a live page."""
    payload = request.get_json(silent=True) or request.form
    code = (payload.get("code") or "").strip()
    title = secure_filename(payload.get("title") or "page") or "page"

    if not code:
        return jsonify({"ok": False, "error": "No HTML code received."}), 400

    slug = uuid.uuid4().hex[:10]
    stored_name = f"{slug}.html"
    with open(os.path.join(UPLOAD_DIR, stored_name), "w", encoding="utf-8") as fh:
        fh.write(code)

    record = {
        "id": slug,
        "name": f"{title}.html",
        "stored_name": stored_name,
        "category": "code",
        "ext": "html",
        "size": os.path.getsize(os.path.join(UPLOAD_DIR, stored_name)),
        "uploaded_at": datetime.utcnow().isoformat() + "Z",
        "url": url_for("serve_file", stored_name=stored_name, _external=False),
    }
    add_record(record)
    return jsonify({"ok": True, "file": record})


@app.route("/uploads/<path:stored_name>")
def serve_file(stored_name):
    """
    Serves every hosted file with a correct content type.
    HTML/CSS/JS render live (like a mini GitHub Pages); images, audio and
    video stream / display directly; everything else downloads.
    """
    safe_name = secure_filename(stored_name)
    full_path = os.path.join(UPLOAD_DIR, safe_name)
    if not os.path.isfile(full_path):
        abort(404)

    mime, _ = mimetypes.guess_type(full_path)
    mime = mime or "application/octet-stream"

    if safe_name.lower().endswith((".html", ".htm")):
        with open(full_path, "r", encoding="utf-8", errors="replace") as fh:
            return Response(fh.read(), mimetype="text/html")

    return send_from_directory(UPLOAD_DIR, safe_name, mimetype=mime)


@app.route("/delete/<file_id>", methods=["POST"])
def delete_file(file_id):
    data = load_db()
    target = next((r for r in data if r["id"] == file_id), None)
    if not target:
        abort(404)
    try:
        os.remove(os.path.join(UPLOAD_DIR, target["stored_name"]))
    except OSError:
        pass
    data = [r for r in data if r["id"] != file_id]
    save_db(data)
    return jsonify({"ok": True})


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
