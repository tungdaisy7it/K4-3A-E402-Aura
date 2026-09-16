# CP1 Canvas — VLearn FailFirst (Sai trước · Giảng sau)

**Track D · Đề D2 — Học từ lỗi trước: làm bài rồi mới được giảng**

| Mục | Nội dung |
|---|---|
| **Hướng** | D — Học tập thích ứng & tương tác trên VLearn · đề **D2** |
| **Job executor** | Học viên K4 sắp học phần "token" của Day01 Foundation — mở lab ra, muốn xong bài, chưa thử tự nghĩ |
| **Pain 1 câu** | Học viên đang làm lab Day01 **dán thẳng đề bài vào tutor để lấy đáp án** (103 lượt · 38 học viên); tutor trả lời luôn và **không hỏi ngược lần nào** (0/103), nên học viên nộp được bài mà chưa từng tự thử — chỗ hiểu sai không ai phát hiện, kể cả chính học viên lẫn giảng viên (`understanding_level` trống 13.474/13.494) |
| **Evidence ban đầu** | Mining `tutor_turns.csv`, lọc `cohort_hint=K4` + `is_preset=False` (2.555 lượt, 384 học viên): ① **103 lượt / 38 học viên** dán nguyên đề hoặc nhờ làm hộ — tutor hỏi ngược **0 lần**; ② **65 lượt / 43 học viên** báo bài chạy sai, tutor chọn `review_concept` 55/65 (giảng lại khái niệm thay vì chẩn đoán lỗi); ③ **67 lượt / 33 học viên** hỏi về *token* — cụm kẹt lớn nhất Day01. Nguồn giảng để trích: `[T04-049]`, `[T06-134]`, `[T06-136]`, `[T06-155]`. *(Repo chỉ dẫn `turn_id` + mã đoạn, không commit nguyên văn pack.)* |
| **Lát cắt 1 câu** | **Một học viên** · **trước khi được xem phần giảng về token**, trả lời bài dự đoán "đoạn tiếng Việt ~100 từ này tốn bao nhiêu token — nhiều hay ít hơn số từ, vì sao" · **AI chẩn đoán đúng giả định sai cụ thể** rồi chỉ đưa **một** gợi ý kèm trích dẫn transcript, **không đưa đáp án** · **học viên tự sửa và giải thích lại được** vì sao số token lệch số từ |
| **Automation** | **Conditional** — AI tự chẩn đoán + gợi ý khi lỗi khớp misconception bank; lỗi lạ / câu trả lời bỏ trống / gõ bừa → **không đoán bừa**, hỏi lại một câu; sau 2 vòng vẫn kẹt → mở lời giảng đầy đủ. AI **không chấm điểm**, giảng viên duyệt bank + lời dẫn giải. *Lý do (cost-of-error):* chẩn đoán sai lỗi khiến học viên sửa nhầm và đóng đinh kiến thức nền sai — đắt hơn hẳn việc không chẩn đoán |
| **Willing users dự kiến** | ≥5 bạn ngoài nhóm **thực sự học một đoạn** bằng prototype (ràng buộc riêng của track D), 2 người khai ngay tại CP1: ①____ ②____ ③____ ④____ ⑤____ |
| **Phân công** | Châu: spec + lát cắt · TV2: evidence (mining + log) · TV3: prompt chẩn đoán lỗi + misconception bank · TV4: golden set + eval · TV5: dựng phiên học + validation/demo |

---

## Ý tưởng đầy đủ

### Vì sao chọn D2 chứ không phải D1/D3

Cả ba đề D đều cần dựng kịch bản từ đầu. D2 là đề duy nhất mà **chatlog thật đã chỉ ra đúng khoảnh khắc hỏng**: học viên có làm bài, có sai, có báo lỗi — nhưng hệ thống hiện tại phản ứng bằng cách giảng lại khái niệm (`review_concept` 55/65) thay vì chỉ ra giả định sai. Nghĩa là misconception bank và golden set có thể lấy thẳng từ data thật, không phải bịa — đúng yêu cầu R4 ("≥10 case từ chatlog thật").

### Luồng một phiên học (cái sẽ demo 5 phút)

1. **Chặn đường tắt** — học viên vào phần "token" của Day01, VLearn **chưa mở lời giảng**. Màn hình đưa một bài dự đoán, bắt buộc trả lời kèm lý do.
2. **Học viên trả lời sai** (phần lớn sẽ sai — tiếng Việt tốn token hơn hẳn tiếng Anh, số token > số từ).
3. **AI chẩn đoán** — xếp câu trả lời vào một lỗi cụ thể trong bank, ví dụ:
   - `M1` token = từ
   - `M2` token = ký tự
   - `M3` tiếng Việt và tiếng Anh tốn token như nhau
   - `M4` nhầm token đầu vào với token đầu ra (giá gấp 3–5 lần — `[T06-155]`)
   - `M5` **đúng kết quả nhưng đoán** — không nêu được lý do
4. **Dẫn giải theo bậc** — bậc 1 một gợi ý + trích đoạn transcript; bậc 2 giải thích; bậc 3 mở lời giảng đầy đủ. Không nhảy cóc.
5. **Chốt hiểu** — học viên giải thích lại bằng lời của mình; AI đối chiếu với transcript rồi mới cho đi tiếp.

### 4 lớp chỗ khó (taxonomy bắt buộc)

| Lớp | Cụ thể hoá cho D2 |
|---|---|
| ① Nguồn sự thật | Lời dẫn giải phải trích được `[Txx-NNN]`; con số token phải đến từ `tiktoken` chạy thật, không để LLM tự "đếm" |
| ② Mơ hồ / thiếu thông tin | Học viên gõ "ko biết", bỏ trống, trả lời một chữ → chưa đủ để chẩn đoán lỗi nào, phải hỏi lại chứ không gán bừa |
| ③ Ngoài phạm vi / thẩm quyền | "Cho đáp án luôn đi" / dán nguyên đề lab → từ chối đưa đáp án nhưng vẫn phải hữu ích (đây chính là 103 lượt đã mining được) |
| ④ Đặc thù domain | Chẩn đoán nhầm lỗi → học viên sửa sai hướng và tin chắc vào kiến thức nền sai; sai ở token thì hỏng luôn phần context, giá API, cắt ngữ cảnh về sau |

### Quality bar phải có 1 chỉ số về HỌC (ràng buộc riêng track D)

Không được chỉ đo "AI trả lời đúng". Đề xuất chốt trước 21:00 17/9:
- **Chẩn đoán đúng lỗi** ≥ 70% trên golden set (người ngoài nhóm chấm lại ra cùng kết quả)
- **Không rò đáp án** ở bậc 1: 100% (0 ca vi phạm)
- **Học được**: ≥ 3/5 người thử **giải thích lại đúng** sau khi sai, không cần xem lời giảng đầy đủ

### 3 non-goals (để R2 không mất điểm)

1. Không chấm điểm, không ghi vào XP/điểm số của học viên.
2. Không làm cho cả khoá — chỉ **một** khái niệm (token) trong **một** bài (Day01).
3. Không thay thế tutor đang chạy; đây là bước **trước** khi học viên được xem lời giảng.

### Việc phải làm ngay sau CP1

- Chạy lại script mining, lưu `evidence/` (số đếm + ≥5 ví dụ nguyên văn + quy tắc đếm) — R1 chấm trên file này.
- Rủ đủ **5 người thử thật**, hẹn giờ cụ thể trước buổi 18/9 — track D bắt buộc phải có người *học thật*, không phải "bấm thử giao diện".
- Dựng misconception bank M1–M5 từ chính câu hỏi token trong chatlog, dẫn `turn_id`.
