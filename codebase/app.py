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
import secrets
from urllib.parse import urlparse

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from openai import (APIConnectionError, APIStatusError, APITimeoutError,
                    AuthenticationError, BadRequestError,
                    PermissionDeniedError, RateLimitError)

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from failfirst.content import repository  # noqa: E402
from failfirst.core import (  # noqa: E402
    DOAN_VAN, cham_giai_thich, chan_doan, dem_token, giai_thich,
    kiem_tra_ket_noi, su_that,
)

app = Flask(__name__, static_folder=None)  # tat static catch-all de khong nuot /api/*
_unlock_tokens = {}
APP_VERSION = "rag-multi-exercise-20260917.2"


def _openai_error(error):
    """Trả lỗi JSON đủ dùng để sửa cấu hình, không lộ key hay prompt."""
    if isinstance(error, AuthenticationError):
        status, code = 401, "OPENAI_AUTH"
        message = "OpenAI từ chối API key. Hãy kiểm tra OPENAI_API_KEY."
    elif isinstance(error, PermissionDeniedError):
        status, code = 403, "OPENAI_PERMISSION"
        message = "API key không có quyền dùng model đã cấu hình."
    elif isinstance(error, RateLimitError):
        status, code = 429, "OPENAI_RATE_LIMIT"
        message = "OpenAI đang giới hạn tần suất hoặc tài khoản đã hết quota."
    elif isinstance(error, APITimeoutError):
        status, code = 504, "OPENAI_TIMEOUT"
        message = "OpenAI phản hồi quá thời gian chờ 45 giây."
    elif isinstance(error, APIConnectionError):
        status, code = 503, "OPENAI_CONNECTION"
        message = "Server không kết nối được tới OpenAI."
    elif isinstance(error, BadRequestError):
        status, code = 400, "OPENAI_BAD_REQUEST"
        message = "Model hoặc tham số gọi OpenAI không hợp lệ."
    else:
        status, code = 502, "OPENAI_API"
        message = "OpenAI trả về lỗi khi xử lý yêu cầu."
    request_id = getattr(error, "request_id", None)
    return jsonify({"error": {
        "code": code,
        "message": message,
        "request_id": request_id,
        "detail": str(error)[:300],
    }}), status


for _error_type in (AuthenticationError, PermissionDeniedError, RateLimitError,
                    APITimeoutError, APIConnectionError, BadRequestError, APIStatusError):
    app.register_error_handler(_error_type, _openai_error)


@app.errorhandler(KeyError)
def invalid_content_id(error):
    return jsonify({"error": {"code": "CONTENT_NOT_FOUND", "message": str(error)}}), 404


@app.errorhandler(RuntimeError)
def ai_runtime_error(error):
    return jsonify({"error": {
        "code": "AI_RESPONSE_INVALID",
        "message": str(error),
    }}), 502


@app.after_request
def add_build_header(response):
    response.headers["X-VLearn-Version"] = APP_VERSION
    if request.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/")
def index():
    return send_from_directory("web", "index.html")


@app.get("/web/<path:filename>")
def web_asset(filename):
    return send_from_directory("web", filename)


@app.get("/api/health")
def health():
    """Cho biết cấu hình; endpoint này không giả vờ rằng API thật đã được gọi."""
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    configured = bool(os.environ.get("OPENAI_API_KEY"))
    return jsonify({
        "app_version": APP_VERSION,
        "model": os.environ.get("OPENAI_MODEL", "?"),
        "provider": "OpenRouter" if "openrouter" in base else "OpenAI",
        "base_host": urlparse(base).netloc,
        "configured": configured,
        "co_key": configured,  # alias cũ để client CP3 không bị vỡ
        "verified": False,
    })


@app.post("/api/health/ai")
def health_ai():
    """Một lời gọi ngắn tới đúng model để kiểm tra key, model, mạng và JSON mode."""
    out = kiem_tra_ket_noi()
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    return jsonify({
        "app_version": APP_VERSION,
        "provider": "OpenRouter" if "openrouter" in base else "OpenAI",
        "verified": True,
        **out,
    })


@app.get("/api/bai-tap")
def bai_tap():
    """API CP3 cũ: giữ nguyên schema và luôn trả bài token mặc định."""
    st = su_that()
    return jsonify({"doan_van": DOAN_VAN, "n_tieng": st["n_tieng"]})


@app.get("/api/lessons/token-foundations")
def lesson():
    """Lesson cùng danh sách bài công khai; tuyệt đối không chứa answer/source allowlist."""
    return jsonify(repository.public_lesson())


@app.post("/api/chan-doan")
def api_chan_doan():
    d = request.get_json(force=True) or {}
    out = chan_doan(d.get("so"), d.get("ly_do", ""), exercise_id=d.get("exercise_id"))
    return jsonify(out)


@app.post("/api/giai-thich")
def api_giai_thich():
    d = request.get_json(force=True) or {}
    level = 3 if int(d.get("level", 2)) >= 3 else 2
    return jsonify(giai_thich(d.get("exercise_id") or repository.default_exercise_id,
                              d.get("nhan", "OUT"), level))


@app.post("/api/chot-hieu")
def api_chot_hieu():
    d = request.get_json(force=True) or {}
    exercise_id = d.get("exercise_id") or repository.default_exercise_id
    out = cham_giai_thich(
        exercise_id,
        d.get("giai_thich", ""),
    )
    if out.get("dat") is True:
        token = secrets.token_urlsafe(24)
        _unlock_tokens[token] = exercise_id
        out["unlock_token"] = token
    return jsonify(out)


@app.post("/api/mo-khoa")
def api_mo_khoa():
    """Chỉ gọi khi học viên đã qua bước chẩn đoán — lúc này mới được thấy sự thật."""
    d = request.get_json(silent=True) or {}
    exercise_id = d.get("exercise_id") or repository.default_exercise_id
    # Request cũ không có exercise_id vẫn hoạt động. Luồng web nhiều bài phải có proof từ /api/chot-hieu.
    if d.get("exercise_id"):
        token = d.get("unlock_token", "")
        if _unlock_tokens.pop(token, None) != exercise_id:
            return jsonify({"error": "Cần giải thích lại đạt yêu cầu trước khi mở đáp án."}), 403
    exercise = repository.get_exercise(exercise_id)
    st = su_that(exercise_id)
    st["ti_le_o200k"] = round(st["o200k_base"] / st["n_tieng"], 2)
    st["ti_le_cl100k"] = round(st["cl100k_base"] / st["n_tieng"], 2)
    st["question"] = exercise["question"]
    st["sources"] = [repository.source(x) for x in exercise["source_refs"] if repository.source(x)]
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
    print("VLearn build:", APP_VERSION)
    print("-> http://127.0.0.1:%d" % port)
    app.run(host="127.0.0.1", port=port, debug=False)
