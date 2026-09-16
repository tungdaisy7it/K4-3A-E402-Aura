# CP3 — Video thao tác + số đo · VLearn FailFirst (D2)

## 1 · Số đo

**Thử 21 case, 20 case đạt (95%).** Một case trượt: `G18`.

Chạy `python eval/run_eval.py` — mỗi case là **một lời gọi AI thật** tới `gpt-4o-mini`, `temperature=0`.
Kết quả đầy đủ kèm nguyên văn case trượt: [`codebase/eval/`](../codebase/eval/) · trace từng lời gọi trong `trace-*.json`.

### Một case tính là ĐẠT khi thoả cả ba

| # | Tiêu chí | Vì sao tách riêng |
|---|---|---|
| 1 | Chẩn đoán đúng nhãn lỗi | Gán sai nhãn → học viên đi sửa nhầm chỗ |
| 2 | Không lộ đáp án | Lộ số là bài tập mất sạch ý nghĩa, dù nhãn đúng |
| 3 | Trích dẫn nằm trong danh sách hợp lệ | Bịa mã đoạn transcript = bịa nguồn |

Tiêu chí 2 và 3 kiểm bằng **luật** (regex số thật `121`/`199`, cụm "đáp án là"; so mã trích dẫn với danh sách), không hỏi lại LLM — nên người ngoài nhóm chấm lại ra cùng kết quả.

### Kết quả hai lượt chạy

| Lượt | Đạt cả 3 | Đúng nhãn | Không lộ đáp án | Trích dẫn hợp lệ |
|---|---|---|---|---|
| **v1** — bản đầu | **15/21 · 71%** | 15/21 | 21/21 | 21/21 |
| **v2** — sau khi sửa | **20/21 · 95%** | 20/21 | 21/21 | 21/21 |

File gốc cả hai lượt đều giữ trong repo: `results-v1-truoc-khi-sua.md` và `results-20260916-2010.md`.

### 6 case trượt ở v1 — nguyên nhân và cách sửa

Cả 6 đều cùng một kiểu: **model trả `OUT` (lỗi ngoài bank) thay vì gán nhãn cụ thể**. Hai nguyên nhân khác hẳn nhau:

**(a) Lỗi ở prompt — 4 case (`G08` `G09` `G10` `G20`).**
Luật số 4 trong system prompt viết *"thà trả LOW hoặc OUT còn hơn gán nhãn sai"*, khiến model chọn `OUT` làm mặc định cho mọi ca hơi khó. `G08` nói thẳng "phải tính cả token đầu ra" — đúng định nghĩa `M4` — mà vẫn bị đẩy ra `OUT`.
→ Sửa: đổi luật 4 thành *"OUT là lối thoát cuối, không phải mặc định"*, và thêm mục "cách nhận M3 và M4 (hay bị bỏ sót)".

**(b) Lỗi ở chính golden set — 2 case (`G17` `G18`).**
Hai case này là câu trả lời **đúng cả số lẫn cơ chế**, nhưng nhóm lại đặt nhãn mong đợi là `M5` (đoán bừa). Model trả `OUT` mới là phản ứng hợp lý — bank không có chỗ nào cho "học viên trả lời đúng".
→ Sửa: thêm nhãn `DUNG` vào bank, đổi nhãn mong đợi của G17/G18. **Đây là lỗi thiết kế của nhóm, không phải lỗi của AI** — và chỉ lộ ra khi chạy eval thật.

### Case còn trượt ở v2

`G18` — học viên đoán **130** (số thật 121) kèm lý do đúng cơ chế. Nhóm đặt mong đợi `DUNG`, model trả `OUT`.
Đây là ca **thật sự ở ranh giới**: lý do đúng nhưng số lệch 7%. Nhóm chưa định nghĩa được "số hợp lý" là sai lệch bao nhiêu phần trăm. Phải chốt ngưỡng đó trong `spec.md` trước 21:00 17/9 — chưa chốt thì case này vẫn sẽ trượt.

### Hai điểm yếu của số đo này, nói trước khi bị hỏi

1. **21 case do nhóm tự viết, cùng người viết prompt** — nên bộ case dễ hơn học viên thật. Số 95% sẽ tụt khi gặp câu trả lời thật. Việc tiếp theo: dựng lại case từ 67 lượt hỏi *token* có thật trong chatlog K4 (33 học viên), dẫn `turn_id`.
2. **Chưa đo được cái quan trọng nhất của track D: học viên có HỌC được không.** 95% mới chỉ nói AI chẩn đoán đúng. Chỉ số học (≥3/5 người giải thích lại đúng sau khi sai) phải đo ở buổi validation với 5 người thật.

## 2 · Video thao tác — kịch bản 30 giây

Chạy trước: `cd codebase && pip install -r requirements.txt && python app.py` → mở http://127.0.0.1:5050

| Giây | Bấm gì | Phải thấy gì trên màn hình |
|---|---|---|
| 0–5 | Mở trang | Ô lời giảng **đang khoá** 🔒, thanh xanh "AI THẬT" |
| 5–10 | Gõ `99` + lý do "mỗi tiếng là một token" | |
| 10–17 | Bấm **Nộp dự đoán** | Spinner → nhãn **M1**, chẩn đoán, gợi ý **không có số đáp án**, trích dẫn `[T06-134]`, dòng meta `gpt-4o-mini · …ms` |
| 17–22 | Bấm **Cho đáp án luôn đi** | Hệ thống **từ chối** nhưng đưa câu hỏi thu hẹp |
| 22–30 | Bấm **Tôi sửa lại** → gõ giải thích có chữ "cắt theo cụm" → **Gửi** | Mở khoá + bảng **121 token (o200k) vs 199 token (cl100k)** do tiktoken đếm thật |

Dòng meta `gpt-4o-mini · 1722ms` ở cuối khối chẩn đoán chính là bằng chứng AI chạy thật — **đừng cắt mất khỏi khung hình**.

## 3 · Cái gì thật, cái gì còn mock

| Thành phần | Trạng thái |
|---|---|
| Đếm token | **Thật** — `tiktoken`, cả `o200k_base` lẫn `cl100k_base` |
| Chẩn đoán lỗi (quyết định trung tâm) | **Thật** — `gpt-4o-mini`, `temperature=0`, JSON mode |
| Chặn lộ đáp án | **Thật** — hậu kiểm bằng luật sau khi LLM trả lời |
| Chấm "giải thích lại đạt chưa" | **Còn mock** — luật từ khoá trong `web/index.html`, chưa gọi AI |
| Trích dẫn transcript | **Bán thật** — mã đoạn có thật và được kiểm, nhưng nội dung trích còn hardcode |

Mức prototype tự khai: **Mock+** — flow bấm được, AI thật ở lõi, còn một nhánh chấm hiểu chạy bằng luật.

## 4 · Chi phí

`gpt-4o-mini`, prompt ~700 token vào / ~120 token ra mỗi lời gọi. Chạy trọn 21 case hai lượt ≈ 0,01 USD. Không phải lo ngân sách ở quy mô hackathon.
