# Kết quả eval — VLearn FailFirst (CP3)

Chạy lúc **20:08 16/09/2026** · model `gpt-4o-mini` · lời gọi AI **thật**, `temperature=0`.

Sự thật bài tập tính bằng `tiktoken` chạy thật: đoạn **99 tiếng** → **121 token** (`o200k_base`) · **199 token** (`cl100k_base`).


## Số đo

| Chiều chất lượng | Đạt | Tỉ lệ |
|---|---|---|
| **Đạt cả 3 tiêu chí** | 15/21 | **71%** |
| Chẩn đoán đúng nhãn lỗi | 15/21 | 71% |
| Không lộ đáp án | 21/21 | 100% |
| Trích dẫn hợp lệ | 21/21 | 100% |

## Từng case

| ID | Lớp | Mong đợi | Ra | Nhãn | Không lộ | Trích dẫn | Kết |
|---|---|---|---|:-:|:-:|:-:|:-:|
| G01 | thuong | `M1` | `M1` | ✅ | ✅ | ✅ | **ĐẠT** |
| G02 | thuong | `M1` | `M1` | ✅ | ✅ | ✅ | **ĐẠT** |
| G03 | thuong | `M1` | `M1` | ✅ | ✅ | ✅ | **ĐẠT** |
| G04 | thuong | `M2` | `M2` | ✅ | ✅ | ✅ | **ĐẠT** |
| G05 | thuong | `M2` | `M2` | ✅ | ✅ | ✅ | **ĐẠT** |
| G06 | thuong | `M3` | `M3` | ✅ | ✅ | ✅ | **ĐẠT** |
| G07 | thuong | `M3` | `M3` | ✅ | ✅ | ✅ | **ĐẠT** |
| G08 | thuong | `M4` | `OUT` | ❌ | ✅ | ✅ | **TRƯỢT** |
| G09 | thuong | `M4` | `OUT` | ❌ | ✅ | ✅ | **TRƯỢT** |
| G10 | thuong | `M5` | `OUT` | ❌ | ✅ | ✅ | **TRƯỢT** |
| G11 | ②mo_ho | `LOW` | `LOW` | ✅ | ✅ | ✅ | **ĐẠT** |
| G12 | ②mo_ho | `LOW` | `LOW` | ✅ | ✅ | ✅ | **ĐẠT** |
| G13 | ②mo_ho | `LOW` | `LOW` | ✅ | ✅ | ✅ | **ĐẠT** |
| G14 | ③ngoai_tham_quyen | `XIN` | `XIN` | ✅ | ✅ | ✅ | **ĐẠT** |
| G15 | ③ngoai_tham_quyen | `XIN` | `XIN` | ✅ | ✅ | ✅ | **ĐẠT** |
| G16 | ③ngoai_tham_quyen | `XIN` | `XIN` | ✅ | ✅ | ✅ | **ĐẠT** |
| G17 | ①nguon_su_that | `M5` | `OUT` | ❌ | ✅ | ✅ | **TRƯỢT** |
| G18 | ①nguon_su_that | `M5` | `OUT` | ❌ | ✅ | ✅ | **TRƯỢT** |
| G19 | ④dac_thu_domain | `XIN` | `XIN` | ✅ | ✅ | ✅ | **ĐẠT** |
| G20 | ④dac_thu_domain | `M3` | `OUT` | ❌ | ✅ | ✅ | **TRƯỢT** |
| G21 | hiem | `OUT` | `OUT` | ✅ | ✅ | ✅ | **ĐẠT** |

## Case trượt — nguyên văn, không giấu


**G08** (`thuong`) — mong đợi `M4`, ra `OUT`
- Học viên trả lời: số `400` · lý do: "phải tính cả token đầu ra nữa, mà đầu ra đắt gấp 3-5 lần đầu vào"
- Chẩn đoán: Học viên đang nhầm lẫn giữa token đầu vào và token đầu ra khi tính giá.
- Gợi ý: Bạn có thể giải thích rõ hơn về cách bạn tính toán số token không?
- Cảnh báo hậu kiểm: `NHAN_LA`

**G09** (`thuong`) — mong đợi `M4`, ra `OUT`
- Học viên trả lời: số `300` · lý do: "em cộng cả input lẫn output vào cho đủ chi phí ạ"
- Chẩn đoán: Học viên đang nhầm lẫn giữa token đầu vào và token đầu ra khi tính toán.
- Gợi ý: Bạn có thể giải thích rõ hơn về cách bạn tính toán số token không?
- Cảnh báo hậu kiểm: `NHAN_LA`

**G10** (`thuong`) — mong đợi `M5`, ra `OUT`
- Học viên trả lời: số `120` · lý do: "tự nhiên thấy con số này hợp lý thôi chứ em không chắc lắm"
- Chẩn đoán: Học viên đang dựa vào cảm giác mà không có cơ sở rõ ràng để đưa ra con số.
- Gợi ý: Bạn có thể giải thích tại sao bạn lại chọn con số này không?
- Cảnh báo hậu kiểm: `NHAN_LA`

**G17** (`①nguon_su_that`) — mong đợi `M5`, ra `OUT`
- Học viên trả lời: số `121` · lý do: "em chạy tiktoken thấy ra số này, vì tokenizer cắt theo cụm ký tự hay gặp chứ không cắt theo tiếng"
- Chẩn đoán: Học viên đang giả định rằng mọi model/tokenizer đều cho cùng một số token.
- Gợi ý: Bạn có thể xem xét cách mà tokenizer cụ thể này hoạt động để hiểu rõ hơn về số token được tạo ra không?
- Cảnh báo hậu kiểm: `NHAN_LA`

**G18** (`①nguon_su_that`) — mong đợi `M5`, ra `OUT`
- Học viên trả lời: số `130` · lý do: "tokenizer cắt theo cụm ký tự phổ biến trong dữ liệu huấn luyện nên số token nhỉnh hơn số tiếng một chút"
- Chẩn đoán: Học viên đang nhầm lẫn giữa số từ và số ký tự khi tính toán số token.
- Gợi ý: Bạn có thể giải thích tại sao số token lại không chỉ phụ thuộc vào số từ không?
- Cảnh báo hậu kiểm: `NHAN_LA`

**G20** (`④dac_thu_domain`) — mong đợi `M3`, ra `OUT`
- Học viên trả lời: số `121` · lý do: "vì tiếng Việt luôn tốn gấp đôi tiếng Anh ở mọi model"
- Chẩn đoán: Học viên đang giả định rằng số token luôn tỉ lệ thuận với số tiếng trong mọi model.
- Gợi ý: Có cách nào khác để xác định số token mà không chỉ dựa vào số tiếng không?
- Cảnh báo hậu kiểm: `NHAN_LA`

## Ghi chú phương pháp

- Một case **ĐẠT** khi thoả cả ba: đúng nhãn · không lộ đáp án · trích dẫn hợp lệ.
- Hậu kiểm lộ đáp án chạy bằng luật (regex số thật + cụm "đáp án là"), không hỏi lại LLM.
- `temperature=0` để chạy lại ra kết quả so sánh được.
- Trace nguyên văn từng lời gọi: `eval/trace-20260916-2007.json`.
