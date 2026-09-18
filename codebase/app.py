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


@app.get("/slide")
def slide_preview():
    return send_from_directory(".", "VLearn_Pitch_Deck_Preview.html")


@app.get("/download-slide")
def download_slide():
    return send_from_directory(".", "VLearn_Pitch_Deck.pptx", as_attachment=True)


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


# ------------------------------------------------------------- vlearn-pack integration
LESSONS_MAP = {
    1: {
        "title": "Bài 1: Foundation · Cách LLM hoạt động & Tokenization",
        "file": "transcript-04-clean.md",
        "module": "MODULE 1: AI FOUNDATIONS",
        "questions": [
            "📌 ĐOẠN VĂN THỰC HÀNH (16 tiếng):\n\"Mô hình AI cắt văn bản thành các token để xử lý dữ liệu ngôn ngữ.\"\n\n👉 Theo bạn, đoạn văn 16 tiếng trên đếm ra bao nhiêu token trong encoding o200k_base (Model: GPT-4o)?",
            "Vì sao 1 từ tiếng Việt có dấu thường bị tokenizer cl100k_base (GPT-4) cắt thành nhiều mảnh token hơn tiếng Anh?",
            "Theo bài giảng, sự khác biệt lớn nhất giữa tokenizer o200k_base (GPT-4o) và cl100k_base (GPT-4) là gì?"
        ]
    },
    2: {
        "title": "Bài 2: Xác định bài toán kinh doanh cho AI",
        "file": "transcript-01-clean.md",
        "module": "MODULE 2: BÀI TOÁN AI DOANH NGHIỆP",
        "questions": [
            "Theo bài giảng, 70% sự thành công khi đưa AI vào doanh nghiệp đến từ đâu?",
            "Khi sếp đưa yêu cầu mơ hồ 'làm AI support', kỹ năng quan trọng nhất của Product Manager là gì?",
            "Tại sao văn hóa làm sản phẩm AI cần lấy người dùng làm trung tâm (User-centered)?"
        ]
    },
    3: {
        "title": "Bài 3: Chỉ số thành công & Mức tự động hóa",
        "file": "transcript-02-clean.md",
        "module": "MODULE 2: BÀI TOÁN AI DOANH NGHIỆP",
        "questions": [
            "Sự khác biệt cốt lõi giữa Product Manager và Project Manager trong dự án AI là gì?",
            "Khi đo lường mức độ tự động hóa, tại sao không nên kỳ vọng AI thay thế 100% con người ngay lập tức?",
            "Chỉ số thành công (North Star Metric) của một trợ lý AI support nên đo lường bằng yếu tố nào?"
        ]
    },
    4: {
        "title": "Bài 4: Soi bài toán nhóm & Ràng buộc AI",
        "file": "transcript-03-clean.md",
        "module": "MODULE 2: BÀI TOÁN AI DOANH NGHIỆP",
        "questions": [
            "Vì sao sản phẩm AI cần thiết kế theo hướng giảm thiểu rủi ro xác suất?",
            "Khi mô hình AI trả lời sai (hallucination), giải pháp thiết kế UX tốt nhất là gì?",
            "Cách thiết kế rào chắn rủi ro (Safety Guardrails) trước khi cho user sử dụng AI?"
        ]
    },
    5: {
        "title": "Bài 5: Đánh giá bài toán, dữ liệu & Quy trình làm AI",
        "file": "transcript-05-clean.md",
        "module": "MODULE 3: CHUYÊN SÂU & DỮ LIỆU",
        "questions": [
            "Làm thế nào để đo lường ROI của một giải pháp AI trước khi triển khai?",
            "Bước làm sạch dữ liệu đóng vai trò gì trong việc tăng độ chính xác của AI?",
            "Tại sao dữ liệu phản hồi thật của học viên lại quan trọng hơn bộ dữ liệu tổng hợp?"
        ]
    },
    6: {
        "title": "Bài 6: Deep Dive · Transformer & Attention Architecture",
        "file": "transcript-06-clean.md",
        "module": "MODULE 3: CHUYÊN SÂU & DỮ LIỆU",
        "questions": [
            "Cơ chế Attention trong Transformer giúp mô hình giải quyết vấn đề gì?",
            "Sự khác biệt giữa Self-Attention và Cross-Attention trong kiến trúc Encoder-Decoder?",
            "Tại sao Positional Encoding lại cần thiết khi xử lý chuỗi văn bản không thứ tự?"
        ]
    }
}


@app.route("/api/bai-hoc", methods=["GET"])
def danh_sach_bai_hoc():
    """Trả về danh sách 6 bài học từ vlearn-pack kèm phân loại module."""
    out = []
    for lid, info in LESSONS_MAP.items():
        out.append({
            "id": lid,
            "title": info["title"],
            "module": info.get("module", "MODULE CHUNG")
        })
    return jsonify(out)


@app.route("/api/bai-hoc/<int:lid>", methods=["GET"])
def chi_tiet_bai_hoc(lid):
    """Trả về nội dung transcript sạch bài học từ vlearn-pack."""
    info = LESSONS_MAP.get(lid, LESSONS_MAP[1])
    pack_dir = os.path.join(os.path.dirname(__file__), "..", "vlearn-pack", "transcript")
    fpath = os.path.join(pack_dir, info["file"])
    content = ""
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
    
    return jsonify({
        "id": lid,
        "title": info["title"],
        "module": info.get("module", "MODULE CHUNG"),
        "questions": info.get("questions", ["Câu hỏi chẩn đoán?"]),
        "content": content
    })


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Thiếu OPENAI_API_KEY — copy .env.example thành .env rồi điền key.")
    port = int(os.environ.get("PORT", 5050))
    print("-> http://127.0.0.1:%d" % port)
    app.run(host="127.0.0.1", port=port, debug=False)

