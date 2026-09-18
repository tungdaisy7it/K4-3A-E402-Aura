# Chi tiết nhật ký 5 phiên Validation (Khối R6)

## Phiên 1: Bùi Đăng Khoa (Willing user từ CP1)
- **Mã học viên:** 2A202601123
- **Thời gian:** 17/9/2026 · 16:30
- **Nhiệm vụ:** Làm bài dự đoán token đoạn văn tiếng Việt 99 tiếng.
- **Câu trả lời nhập vào:** "99 token, vì đoạn văn có 99 từ tiếng Việt."
- **Nhãn hệ thống gán:** `M1` (token = từ/tiếng).
- **Hành vi học viên:** Đọc gợi ý Bậc 1 có mã `[T04-049]`, tự gõ lại giải thích: *"Tokenizer cắt theo cụm ký tự hay gặp, không cắt theo từ. Tiếng Việt có dấu nên 1 tiếng thường tốn hơn 1 token."*
- **Người chấm 1 (Hằng):** Đạt.
- **Người chấm 2 (Thạch):** Đạt.
- **Quote nguyên văn:** *"Mới đầu mình tưởng 1 tiếng tiếng Việt tính là 1 token như từ tiếng Anh. Nhìn AI gợi ý mã [T04-049] mới nhớ ra tokenizer cắt theo cụm ký tự hay gặp, tiếng Việt có dấu nên bị chẻ nhỏ hơn."*

---

## Phiên 2: Nguyễn Trung Kiên (Willing user từ CP1)
- **Mã học viên:** 2A202601456
- **Thời gian:** 17/9/2026 · 16:45
- **Nhiệm vụ:** Làm bài dự đoán token đoạn văn tiếng Việt 99 tiếng.
- **Câu trả lời nhập vào:** "Tầm 120 token cho mọi model LLM vì tiếng Việt tốn hơn tiếng Anh 20%."
- **Nhãn hệ thống gán:** `M3` (coi tỉ lệ token cố định ở mọi model).
- **Hành vi học viên:** Hệ thống đưa gợi ý nhắc về sự khác biệt giữa `o200k_base` và `cl100k_base`. Học viên tự sửa thành công.
- **Người chấm 1 (Hằng):** Đạt.
- **Người chấm 2 (Thạch):** Đạt.
- **Quote nguyên văn:** *"Mình cứ nghĩ model nào cũng đếm token như nhau. Lúc AI chẩn đoán bảo o200k_base với cl100k_base chênh nhau gần 2 lần mới giật mình."*

---

## Phiên 3: Trần Đức Anh
- **Mã học viên:** 2A202601789
- **Thời gian:** 17/9/2026 · 17:10
- **Nhiệm vụ:** Dự đoán token.
- **Câu trả lời nhập vào:** "450 token vì 1 chữ cái là 1 token."
- **Nhãn hệ thống gán:** `M2` (token = ký tự).
- **Hành vi học viên:** Bấm "Tôi sửa lại", nhập giải thích đúng cơ chế byte-pair encoding.
- **Người chấm 1 (Hằng):** Đạt.
- **Người chấm 2 (Thạch):** Đạt.
- **Quote nguyên văn:** *"Mình thấy giao diện có nút 'Chẩn đoán sai rồi' rất hay, đỡ bị ép nhãn lung tung nếu gõ nhầm."*

---

## Phiên 4: Hoàng Thị Mai
- **Mã học viên:** 2A202602112
- **Thời gian:** 17/9/2026 · 17:25
- **Nhiệm vụ:** Dự đoán token.
- **Câu trả lời nhập vào:** "ko biết"
- **Nhãn hệ thống gán:** `LOW` (không ép nhãn lỗi).
- **Hành vi học viên:** Nhận câu hỏi thu hẹp ở Bậc 1, kẹt nhẹ nên sang Bậc 2 xem gợi ý cơ chế rồi giải thích lại đúng.
- **Người chấm 1 (Hằng):** Đạt (ở Bậc 2).
- **Người chấm 2 (Thạch):** Đạt (ở Bậc 2).
- **Quote nguyên văn:** *"Giao diện bước mở khoá nên highlight rõ từng mảnh token cắt ra sao để người không chuyên nhìn là hiểu liền."*

---

## Phiên 5: Phạm Minh Đức
- **Mã học viên:** 2A202602334
- **Thời gian:** 17/9/2026 · 17:40
- **Nhiệm vụ:** Dự đoán token.
- **Câu trả lời nhập vào:** "100 token"
- **Nhãn hệ thống gán:** `M1`.
- **Hành vi học viên:** Sửa ngay sau Bậc 1.
- **Người chấm 1 (Hằng):** Đạt.
- **Người chấm 2 (Thạch):** Đạt.
- **Quote nguyên văn:** *"Bài tập bắt đoán trước thế này vui hơn hẳn là nhảy vào xem video giảng luôn. Đúng kiểu bắt não phải suy nghĩ."*
