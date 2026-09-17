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

from failfirst.core import (NGUON, chan_doan, danh_sach_bai_tap,  # noqa: E402
                            dem_token, lay_bai, su_that)

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
    """Danh sách bài + nội dung một bài. Không kèm đáp án."""
    b = lay_bai(request.args.get("id"))
    return jsonify({
        "danh_sach": danh_sach_bai_tap(),
        "bai": {
            "id": b["id"], "khai_niem": b["khai_niem"], "phan": b["phan"],
            "tieu_de": b["tieu_de"], "doan_van": b["doan_van"],
            "cau_hoi_so": b["cau_hoi_so"], "cau_hoi_ly_do": b["cau_hoi_ly_do"],
            "cau_chot_hieu": b["cau_chot_hieu"], "tu_khoa_chot_hieu": b["tu_khoa_chot_hieu"],
            "n_tieng": len(b["doan_van"].split()), "kieu": b["kieu"],
        },
    })


@app.post("/api/chan-doan")
def api_chan_doan():
    d = request.get_json(force=True) or {}
    return jsonify(chan_doan(d.get("so"), d.get("ly_do", ""), bai_tap_id=d.get("bai_tap")))


@app.post("/api/mo-khoa")
def api_mo_khoa():
    """Chỉ gọi sau khi học viên đã qua bước chẩn đoán — lúc này mới được thấy sự thật."""
    d = request.get_json(force=True) or {}
    b = lay_bai(d.get("bai_tap"))
    st = su_that(b["id"])
    if st["kieu"] == "dem_token":
        st["ti_le_o200k"] = round(st["o200k_base"] / st["n_tieng"], 2)
        st["ti_le_cl100k"] = round(st["cl100k_base"] / st["n_tieng"], 2)
    st["nguon"] = [{"ma": m, "noi_dung": NGUON.get(m, "")} for m in b["nguon_mo_khoa"]]
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
