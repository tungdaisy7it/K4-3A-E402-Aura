# CP2 — Luồng hoạt động · VLearn FailFirst (D2)

> **Mốc CP2 chưa cần AI chạy thật.** Bản mock bấm được: [`codebase/mock/index.html`](../codebase/mock/index.html) — tải về mở bằng trình duyệt, không cần cài gì.
> Ở mock, bước chẩn đoán chạy bằng **luật từ khoá**, không gọi LLM. CP3 mới thay bằng lời gọi AI thật + `tiktoken` thật.

## Lát cắt đang hiện thực

> Một học viên · trước khi được xem phần giảng về token, trả lời bài dự đoán "đoạn tiếng Việt ~100 từ này tốn bao nhiêu token — nhiều hay ít hơn số từ, vì sao" · **AI chẩn đoán đúng giả định sai cụ thể** rồi chỉ đưa **một** gợi ý kèm trích dẫn transcript, không đưa đáp án · học viên tự sửa và giải thích lại được.

## Sơ đồ luồng

```mermaid
flowchart TD
    A["Học viên mở phần 3.2 — Token<br/>Lời giảng đang KHOÁ"] --> B["Bài dự đoán:<br/>số token? + vì sao?"]
    B -->|"bấm 'Cho đáp án luôn'"| X["③ NGOÀI THẨM QUYỀN<br/>Từ chối đưa đáp án<br/>nhưng đưa 1 câu hỏi thu hẹp"]
    X --> B
    B --> C{"Câu trả lời có đủ<br/>để chẩn đoán không?"}

    C -->|"bỏ trống / 'ko biết' / 1 chữ"| D["② LOW-CONFIDENCE<br/>Không gán lỗi bừa —<br/>hỏi lại MỘT câu thu hẹp"]
    D --> B

    C -->|"có lý do nhưng không khớp bank"| E["④ FAILURE<br/>Nói thẳng: chưa xếp được<br/>lỗi vào nhóm nào<br/>→ ghi nhận cho giảng viên"]
    E --> B

    C -->|"khớp bank"| F["① CHẨN ĐOÁN<br/>Gán nhãn lỗi M1–M5"]
    F --> G["BẬC 1 — một gợi ý duy nhất<br/>+ trích dẫn [T06-134]<br/>KHÔNG đưa đáp án"]

    G -->|"'chẩn đoán sai rồi, ý tôi là…'"| H["⑤ CORRECTION<br/>Nhận lại, xếp lại nhãn lỗi,<br/>không bảo lưu"]
    H --> G

    G -->|"học viên sửa lại"| I{"Lần sửa thứ mấy?"}
    I -->|"đúng"| J["CHỐT HIỂU<br/>Giải thích lại bằng lời của bạn"]
    I -->|"vẫn sai, lần 2"| K["BẬC 2 — giải thích<br/>+ trích dẫn"]
    K --> I
    I -->|"vẫn sai, lần 3"| L["BẬC 3 — mở lời giảng đầy đủ<br/>(hết đường tắt)"]

    J --> M{"Giải thích có bám<br/>transcript không?"}
    M -->|"chưa"| N["Hỏi ngược đúng chỗ hổng"]
    N --> J
    M -->|"đạt"| O["✅ MỞ KHOÁ lời giảng<br/>+ log phiên cho giảng viên"]
    L --> O
```

## 4 đường đi trải nghiệm (R3 yêu cầu đủ 4)

| Đường | Kích hoạt khi | Hệ thống làm gì | Bấm thử trong mock |
|---|---|---|---|
| **Happy** | Trả lời sai + nêu được lý do khớp bank | Chẩn đoán đúng nhãn lỗi → bậc 1 một gợi ý → học viên sửa → chốt hiểu → mở lời giảng | Kịch bản `Happy` |
| **Low-confidence** | Bỏ trống lý do, "ko biết", trả lời một chữ | **Không gán lỗi bừa** — hỏi lại một câu thu hẹp | Kịch bản `Low-confidence` |
| **Failure** | Lý do rõ ràng nhưng không khớp M1–M5 | Nói thẳng "chưa xếp được lỗi của bạn", ghi nhận cho giảng viên, không bịa nhãn | Kịch bản `Failure` |
| **Correction** | Học viên bảo "chẩn đoán sai rồi, ý tôi là…" | Nhận lại, xếp lại nhãn, không bảo lưu chẩn đoán cũ | Kịch bản `Correction` |

Cộng thêm đường **③ ngoài thẩm quyền**: bấm "Cho đáp án luôn" → từ chối đưa đáp án nhưng vẫn hữu ích. Đây chính là hành vi đã mining được trong chatlog (103 lượt / 38 học viên dán đề hoặc xin làm hộ).

## Misconception bank dùng trong mock

| Mã | Giả định sai | Dấu hiệu trong câu trả lời |
|---|---|---|
| `M1` | token = từ | "mỗi từ một token", "bằng số từ", đoán đúng 100 |
| `M2` | token = ký tự | "ký tự", "chữ cái" |
| `M3` | tiếng Việt và tiếng Anh tốn token như nhau | "như nhau", "giống tiếng Anh", "không khác" |
| `M4` | nhầm token đầu vào với token đầu ra | "đầu ra", "output", nhắc giá gấp 3–5 lần |
| `M5` | đúng kết quả nhưng đoán | số nằm trong khoảng đúng mà lý do không giải thích được |

Bank này ở CP2 mới là bản nháp 5 nhãn. Trước CP4 phải dựng lại từ **câu hỏi token thật trong chatlog** (67 lượt / 33 học viên) và dẫn `turn_id`.

## Cái gì là mock, cái gì sẽ thật

| Thành phần | CP2 (bây giờ) | CP3 trở đi |
|---|---|---|
| Đếm token | Số cứng `186`, gắn nhãn MOCK | `tiktoken` chạy thật (`o200k_base`) |
| Chẩn đoán lỗi | Luật từ khoá trong `index.html` | **Lời gọi AI thật** — đây là quyết định trung tâm |
| Trích dẫn transcript | Trích cứng `[T06-134]`, `[T04-049]` | Lấy từ transcript có mã đoạn |
| Chấm "giải thích lại đạt chưa" | Luật từ khoá | Lời gọi AI thật, đối chiếu transcript |
