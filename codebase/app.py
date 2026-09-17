# -*- coding: utf-8 -*-
"""
VLearn FailFirst — server chạy thật cho CP3.

    cd codebase
    pip install -r requirements.txt
    python app.py
    -> mở http://127.0.0.1:5050

Khác bản mock CP2: bước chẩn đoán là LỜI GỌI AI THẬT, số token do tiktoken đếm thật.
"""
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from failfirst.core import DOAN_VAN, dem_token, chan_doan, su_that  # noqa: E402

app = Flask(__name__, static_folder=None)  # tat static catch-all de khong nuot /api/*


@app.get("/")
def index():
    return send_from_directory("web", "index.html")


@app.get("/api/health")
def health():
    """Cho header hiển thị đang chạy model nào, qua nhà cung cấp nào."""
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    return jsonify({
        "model": os.environ.get("OPENAI_MODEL", "?"),
        "provider": "OpenRouter" if "openrouter" in base else "OpenAI",
        "co_key": bool(os.environ.get("OPENAI_API_KEY")),
    })


@app.get("/api/bai-tap")
def bai_tap():
    st = su_that()
    return jsonify({"doan_van": DOAN_VAN, "n_tieng": st["n_tieng"]})


@app.post("/api/chan-doan")
def api_chan_doan():
    d = request.get_json(force=True) or {}
    out = chan_doan(d.get("so"), d.get("ly_do", ""))
    return jsonify(out)


@app.post("/api/mo-khoa")
def api_mo_khoa():
    """Chỉ gọi khi học viên đã qua bước chẩn đoán — lúc này mới được thấy sự thật."""
    st = su_that()
    st["ti_le_o200k"] = round(st["o200k_base"] / st["n_tieng"], 2)
    st["ti_le_cl100k"] = round(st["cl100k_base"] / st["n_tieng"], 2)
    return jsonify(st)


@app.post("/api/dem")
def api_dem():
    """Cho học viên tự thử đếm token đoạn văn bất kỳ sau khi mở khoá."""
    d = request.get_json(force=True) or {}
    t = d.get("text", "")
    return jsonify({
        "n_tieng": len(t.split()),
        "o200k_base": dem_token(t, "o200k_base"),
        "cl100k_base": dem_token(t, "cl100k_base"),
    })


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Thiếu OPENAI_API_KEY — copy .env.example thành .env rồi điền key.")
    port = int(os.environ.get("PORT", 5050))
    print("-> http://127.0.0.1:%d" % port)
    app.run(host="127.0.0.1", port=port, debug=False)
