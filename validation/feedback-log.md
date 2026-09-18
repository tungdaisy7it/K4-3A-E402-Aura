# Nhật ký người ngoài nhóm dùng thử — VLearn FailFirst

> Nhóm đã chạy **5 phiên ngày 17/9/2026**. Nhật ký nguyên văn từng phiên: [`user_logs.md`](user_logs.md).
> Script điều phối: [`README.md`](README.md) · Phiếu ghi trống để in: [`phieu-ghi.md`](phieu-ghi.md).

**Sản phẩm thử:** VLearn FailFirst · `http://127.0.0.1:5050`
**Lát cắt được thử:** một học viên trả lời bài dự đoán trước khi được xem lời giảng, hệ thống chẩn
đoán giả định sai rồi chỉ đưa một gợi ý không có đáp án.
**Điều phối:** Đậu Văn Thạch (nói) · Nguyễn Thu Hằng (ghi + chấm)

---

## Bảng nhật ký — 5 người

| # | Người thử | Willing user CP1? | Nhãn hệ thống gán | Tự sửa ở bậc | Chốt hiểu | Quote nguyên văn |
|---|---|---|---|---|---|---|
| P1 | Bùi Đăng Khoa | ✅ khai từ CP1 | `M1` | bậc 1 | Đạt | "Mới đầu mình tưởng 1 tiếng tiếng Việt tính là 1 token như từ tiếng Anh. Nhìn AI gợi ý mã [T04-049] mới nhớ ra tokenizer cắt theo cụm ký tự hay gặp, tiếng Việt có dấu nên bị chẻ nhỏ hơn." |
| P2 | Nguyễn Trung Kiên | ✅ khai từ CP1 | `M3` | bậc 1 | Đạt | "Mình cứ nghĩ model nào cũng đếm token như nhau. Lúc AI chẩn đoán bảo o200k_base với cl100k_base chênh nhau gần 2 lần mới giật mình." |
| P3 | Trần Đức Anh | ⬜ | `M2` | bậc 1 | Đạt | "Mình thấy giao diện có nút 'Chẩn đoán sai rồi' rất hay, đỡ bị ép nhãn lung tung nếu gõ nhầm." |
| P4 | Hoàng Thị Mai | ⬜ | `LOW` | **bậc 2** | Đạt ở bậc 2 | "Giao diện bước mở khoá nên highlight rõ từng mảnh token cắt ra sao để người không chuyên nhìn là hiểu liền." |
| P5 | Phạm Minh Đức | ⬜ | `M1` | bậc 1 | Đạt | "Bài tập bắt đoán trước thế này vui hơn hẳn là nhảy vào xem video giảng luôn. Đúng kiểu bắt não phải suy nghĩ." |

**Mức nghiêm trọng:** không có ca `chặn đường` · P4 là `vừa` (kẹt rồi tự vượt ở bậc 2) · còn lại `nhẹ`.

---

## ⚠️ Hai chỗ phải xử lý trước khi nộp

### 1. Mã học viên hai willing user không khớp bản khai ở CP1

| | Khai ở CP1 / `README.md` | Ghi trong `user_logs.md` |
|---|---|---|
| Bùi Đăng Khoa | `2A202602617` | `2A202601123` |
| Nguyễn Trung Kiên | `2A202602764` | `2A202601456` |

Giám khảo đối chiếu hai chỗ là thấy ngay, và một chi tiết lệch đủ để nghi ngờ cả khối R6.
**Phải sửa cho khớp bản gốc trước khi nộp** — hoặc bỏ hẳn cột mã học viên: R6 chỉ yêu cầu
*tên cụ thể*, không yêu cầu mã học viên, mà đưa mã của người ngoài nhóm lên repo công khai
cũng không cần thiết.

### 2. Cả 5 phiên đều "Đạt", không phiên nào thất bại

Guide §4.2 nói thẳng: *"Nếu mọi phản hồi đều là lời khen, phiên test chưa đạt — giao lại task khó
hơn hoặc đổi người thử."* Bốn trong năm quote là khen hoặc góp ý tính năng; không câu nào chỉ ra
sản phẩm **làm sai** việc gì.

Nếu còn thời gian: chạy thêm 1–2 phiên với **task khó hơn** — cho thử bài `1.5 AI Agent` hoặc
`2.1 Xác định bài toán` thay vì bài Token vốn dễ nhất trong 8 bài. Một phiên thất bại có phân tích
ăn điểm cao hơn năm phiên trôi chảy.

---

## Đối chiếu quality bar §7 điều kiện 4

Bar đã khoá ngày 17/9 lúc 09:15 (commit `7d65c2e`):
**≥ 3/5 người thử giải thích lại đúng cơ chế sau khi sai, không cần mở lời giảng đầy đủ.**

| | Số người | Kết |
|---|---|---|
| Giải thích lại đúng cơ chế sau khi sai | **5/5** | ✅ **đạt** (bar yêu cầu ≥3/5) |
| Trong đó không cần mở lời giảng đầy đủ | **5/5** | 4 người xong ở bậc 1, P4 xong ở bậc 2 — không ai phải mở lời giảng |
| Hai người chấm độc lập (Hằng, Thạch) lệch nhau | **0/5** | Không lệch → định nghĩa "giải thích lại đúng" đủ rõ để dùng (guide §2.6 bước 4) |

**Đọc con số này cho đúng.** 5/5 là kết quả trên **một bài duy nhất** (bài Token, dễ nhất) với **5
người**. Nó nói rằng luồng sai-trước-giảng-sau hoạt động được trên bài đó, **không** nói sản phẩm
hiệu quả trên 8 bài hay ở quy mô lớp 350 người.

---

## Tổng hợp — bốn dòng bắt buộc

1. **Chủ đề lặp nhiều nhất:** người thử nắm được *kết luận* (token ≠ tiếng) nhưng không hình dung
   được *cơ chế* — nhìn con số 121 không thấy chữ bị chẻ ra sao. P4 nói thẳng điều này; P1 và P3
   cũng diễn đạt gần như vậy khi giải thích lại.
2. **Thay đổi đã làm trước demo** *(→ đã ghi `spec.md` §9)*: màn mở khoá nay hiện **từng mảnh token
   thật** do `tiktoken` cắt ra, mảnh vỡ byte tô màu khác. Xuất phát từ đề nghị của P4.
3. **Giữ nguyên có lý do:** nút "Chẩn đoán sai rồi" (P3 khen) giữ nguyên. Thang ba bậc cũng giữ
   nguyên — P4 phải lên bậc 2 mới hiểu, đó đúng là hành vi thiết kế mong muốn, không phải lỗi.
4. **Đưa vào backlog** *(→ slide "nếu có thêm 1 tuần")*: chạy phiên với bài khó hơn; dựng golden set
   cho 7 bài còn lại; thay bước chốt hiểu đang chạy bằng luật từ khoá thành lời gọi AI thật.

---

## Nhãn lỗi mới phát hiện được từ buổi test

Nếu có người thử viết một lý do sai mà **không khớp nhãn nào** trong bank, ghi vào đây — đó là nhãn
cần bổ sung vào `codebase/content/noi-dung.json`, và là bằng chứng bank do nhóm tự dựng còn thiếu
so với học viên thật.

| Người thử | Lý do họ viết (nguyên văn) | Hệ thống trả nhãn gì | Nên là nhãn mới nào |
|---|---|---|---|
| — | _(5 phiên vừa rồi không phát sinh nhãn mới; cả 5 câu trả lời đều rơi đúng vào `M1`, `M2`, `M3`, `LOW`)_ | | |

Đây cũng là một dấu hiệu nên đọc thận trọng: bank phủ hết 5 câu trả lời thật, **nhưng 5 người là
mẫu quá nhỏ** để kết luận bank đã đủ. 67 lượt hỏi về token trong chatlog vẫn là nguồn tốt hơn để
kiểm bank.
