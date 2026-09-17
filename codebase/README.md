# VLearn FailFirst — web thật

Prototype dùng Flask, JavaScript thuần, `tiktoken` và OpenAI-compatible API. `mock/index.html` là bản mock độc lập và không được web thật sử dụng.

## Chạy ứng dụng

```powershell
cd codebase
pip install -r requirements.txt
Copy-Item .env.example .env
# Điền OPENAI_API_KEY, giữ OPENAI_BASE_URL và OPENAI_MODEL theo nhà cung cấp
python app.py
```

Mở `http://127.0.0.1:5050`.

Khi sửa code trong lúc server đang chạy, cần dừng tiến trình Flask cũ và chạy lại `python app.py` vì ứng dụng dùng `debug=False`. Console phải in build `rag-multi-exercise-20260917.2`. Giao diện cũng so build ID để cảnh báo nếu trình duyệt đang nói chuyện với backend cũ.

## Cấu trúc nội dung

- `content/lessons/token-foundations.json`: lesson, thứ tự exercise, câu hỏi, nội dung xử lý, cách tính đáp án, nguồn được phép và lỗi kỳ vọng.
- `content/documents/*.md`: nội dung tài liệu Markdown.
- `content/documents/manifest.json`: metadata của từng đoạn có thể retrieval: `document_id`, `document_name`, `lesson_id`, `section/page`, `source_id`, `quote`.
- `failfirst/content.py`: nạp và kiểm tra kho, trả dữ liệu công khai không có đáp án, retrieval trong allowlist nguồn của đúng một exercise.
- `failfirst/core.py`: chẩn đoán, giải thích bậc 2/3, chấm phần giải thích lại và hậu kiểm nguồn/đáp án.

Khi thêm nguồn, `quote` trong manifest phải xuất hiện nguyên văn trong file Markdown. Ứng dụng sẽ từ chối khởi động nếu `source_id` trùng, quote không tồn tại, hoặc exercise tham chiếu nguồn thiếu.

## API

Các API cũ vẫn hoạt động:

- `GET /api/bai-tap`: giữ đúng schema `{doan_van, n_tieng}` của bài mặc định.
- `POST /api/chan-doan`: payload cũ `{so, ly_do}` vẫn dùng bài mặc định. Có thể thêm `exercise_id`.
- `POST /api/mo-khoa`: request cũ không payload vẫn trả bài mặc định. Luồng web mới gửi `exercise_id` và `unlock_token` nhận từ `/api/chot-hieu`.
- `POST /api/dem`: giữ nguyên.

API mới:

- `GET /api/lessons/token-foundations`: lesson và exercise theo thứ tự, không chứa đáp án.
- `GET /api/health`: chỉ báo cấu hình và build hiện tại; không tuyên bố kết nối AI đã thành công.
- `POST /api/health/ai`: gửi một yêu cầu JSON rất ngắn tới đúng model thật để kiểm tra key, quyền model, mạng và JSON mode.
- `POST /api/giai-thich`: giải thích bậc 2 hoặc 3 từ nguồn retrieval của một exercise.
- `POST /api/chot-hieu`: AI kiểm tra phần học viên giải thích lại; chỉ kết quả đạt mới có `unlock_token`.

Lỗi OpenAI được trả dưới dạng JSON có `code`, thông báo tiếng Việt và `request_id` nếu OpenAI đã nhận request. Các mã riêng gồm `OPENAI_AUTH`, `OPENAI_PERMISSION`, `OPENAI_RATE_LIMIT`, `OPENAI_TIMEOUT`, `OPENAI_CONNECTION` và `OPENAI_BAD_REQUEST`. Client đặt timeout 45 giây và retry tối đa một lần để màn hình không treo quá lâu.

Mỗi lời gọi AI chỉ nhận exercise hiện tại và tối đa hai đoạn nguồn liên quan. Server kiểm tra `source_id` trả về phải thuộc chính tập retrieval; nếu model tạo mã lạ, kết quả được gắn cờ và source card bị ẩn thay vì thay bằng một nguồn nhìn có vẻ hợp lệ. Nếu retrieval không có kết quả, response cũng không tạo source card.

## Kiểm thử offline

```powershell
python -m unittest discover -s tests -v
```

Bộ test không gọi API ngoài. Nó kiểm tra schema cũ, dữ liệu công khai không lộ đáp án, khóa mở đáp án, metadata nguồn, giới hạn retrieval, prompt chỉ chứa một exercise và hậu kiểm lộ đáp án/source giả.
