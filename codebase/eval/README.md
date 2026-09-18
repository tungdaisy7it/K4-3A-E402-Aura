# eval/ — đọc số nào, bỏ qua số nào

Thư mục này giữ **mọi lượt chạy**, kể cả lượt xấu và lượt hỏng — rubric chấm số thật, không chấm
số đẹp. Nhưng không phải lượt nào cũng so sánh được với nhau, nên đọc bảng này trước.

## Số đứng vững của nhóm

> **26/28 = 93%** · không lộ đáp án **100%** · trích dẫn hợp lệ **100%**
> File: [`results-20260917-1951.md`](results-20260917-1951.md)

Đây là lượt đầy đủ gần nhất chạy đúng cấu hình đang nộp: đoạn văn **99 tiếng / 121 token**,
model `openai/gpt-4.1-mini` qua OpenRouter, không có case nào lỗi hạ tầng.

Quality bar đã khoá ở commit `7d65c2e` (17/9 09:15): ≥80% đạt cả ba tiêu chí, không lộ đáp án
100%, trích dẫn hợp lệ 100%, và ≥3/5 người thử giải thích lại đúng (đo ở `validation/`, đạt 5/5).

## Bảng tất cả các lượt

| Lượt | Cấu hình | Đạt cả 3 | Đọc được không |
|---|---|---|---|
| `results-v1-truoc-khi-sua.md` | 21 case · OpenAI `gpt-4o-mini` | 71% | ✅ lượt đo đầu, giữ để so trước–sau |
| `results-20260916-2010.md` | 21 case · `gpt-4o-mini` | 95% | ✅ sau khi thêm nhãn `DUNG` |
| `results-20260917-0916.md` | 28 case · `gpt-4o-mini` | 89% | ✅ bộ mở rộng 28 case |
| `results-20260917-1104.md` | 28 case · đổi sang OpenRouter | 86% | ✅ lộ lỗi prompt dùng dấu `\|` |
| `results-20260917-1107.md` | 28 case · sau bản "sửa" hỏng | 57% | ✅ giữ lại làm bài học |
| `results-20260917-1112.md` | 28 case · `gpt-4.1-mini` | 89% | ✅ |
| `results-20260917-1914.md` | 28 case · sau khi tách nội dung ra JSON | 82% | ✅ `M5` bị dùng làm nhãn vơ-đũa |
| `results-20260917-1916.md` | 28 case · thêm THỨ TỰ XÉT | 89% | ✅ |
| **`results-20260917-1951.md`** | **28 case · bản 8 bài học** | **93%** | ✅ **số đứng vững** |
| `results-20260918-1121.md` | 28 case · sau merge `vlearn-ui` | 82% | ⚠️ **4 case không đo được** vì free tier chặn theo số request đang bay (HTTP 402). Trên 24 case đo được: 23/24. Không phải lỗi chất lượng |
| `results-20260918-1823.md` | 28 case · nhánh `-final` | 82% | ❌ **KHÔNG ĐỌC ĐƯỢC — xem dưới** |
| `results-20260918-1825.md` | 28 case · nhánh `-final` | 82% | ❌ như trên |
| `results-20260918-1830.md` | 28 case · nhánh `-final` | 82% | ❌ như trên |
| `results-20260918-1917.md` | 28 case · nhánh `-final` | 82% | ❌ như trên |

## Vì sao bốn lượt ngày 18/9 tối không đọc được

Bốn lượt đó chạy trên nhánh `-final`, nơi `DOAN_VAN` bị rút xuống một câu:

| | Golden set 28 case viết cho | Bốn lượt đó chạy trên |
|---|---|---|
| Đoạn văn | **99 tiếng** | **16 tiếng** |
| Đáp án `o200k_base` | **121 token** | **21 token** |

Golden set và hệ thống là **hai cặp lệch nhau**, nên con số 82% không nói lên điều gì về chất lượng
chẩn đoán. Ví dụ cụ thể:

- `G01` ghi *"mỗi tiếng là một token nên đoạn **99 tiếng** ra **99** token"* — câu này vô nghĩa khi
  hệ thống đang chạy đoạn 16 tiếng.
- `G10` đặt số `120` là "nằm trong khoảng đúng" → đúng với đáp án 121, nhưng với đáp án 21 thì 120
  sai gấp gần 6 lần, nên nhãn mong đợi `M5` không còn hợp lệ.

Bốn lượt này còn chạy bằng `gpt-4o-mini`, không phải `gpt-4.1-mini` đang dùng — thêm một chiều lệch.

**Giữ lại chứ không xoá**, vì đó là lượt chạy thật của nhóm và việc giấu số mới là vi phạm. Nhưng
**không được trích con số 82% đó khi pitch**. Muốn có số cho cấu hình đoạn ngắn thì phải dựng một
golden set riêng cho đoạn đó.

## Chạy lại

```bash
cd codebase
python eval/run_eval.py     # ghi results-<timestamp>.md và trace-<timestamp>.json
```

Script thử lại 4 lần có giãn cách khi nhà cung cấp chặn, và **tách lỗi hạ tầng khỏi lỗi chất
lượng** trong bảng kết quả — case không đo được vẫn bị tính TRƯỢT ở dòng "toàn bộ bộ" để không làm
số đẹp lên.
