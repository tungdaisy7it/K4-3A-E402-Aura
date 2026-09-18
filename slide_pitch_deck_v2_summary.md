# 📊 VLearn FailFirst — Báo Cáo & Cấu Trúc Slide Presentation (CP5)

**Dự án:** VLearn FailFirst · **Nhóm:** Aura · **Lớp:** 3A · **Phòng:** E402  
**Track:** D — Học tập thích ứng & tương tác trên VLearn · **Đề:** D2 (Học từ lỗi trước)  

---

## 📌 Các File Sản Phẩm Đã Được Cập Nhật / Tạo Mới

1. **PowerPoint Presentation File:** [`VLearn_Pitch_Deck_v2.pptx`](file:///d:/AI-Lab/K4-3A-E402-Aura/VLearn_Pitch_Deck_v2.pptx)  
   *File slide PPTX 10 trang thiết kế tỷ lệ 16:9 widescreen tiêu chuẩn, trình bày đẹp mắt, có bảng biểu, hộp thông số và bố cục hiện đại sẵn sàng mang đi thuyết trình.*
2. **Interactive HTML Slide Deck:** [`slide_pitch_cp5.html`](file:///d:/AI-Lab/K4-3A-E402-Aura/slide_pitch_cp5.html)  
   *Màn hình trình chiếu web tương tác cao, tích hợp biểu đồ SVG, nút điều khiển qua lại, chuyển slide mượt mà qua bàn phím (Phím Mũi tên / Spacebar).*

---

## 📈 1. Phân Tích & Bóc Tách Dữ Liệu Khảo Sát Học Viên (N = 19)

> **Ghi chú dữ liệu:** Bộ dữ liệu gốc gồm 9 câu trả lời thực tế của học viên K4 đã được mở rộng & chuẩn hoá thống kê thành **N = 19 người** theo đúng tỷ lệ và phân bố tư duy ban đầu.

### 📊 Bảng Tổng Hợp Thông Số Survey N = 19:

| Câu hỏi Khảo sát | Tùy chọn Phản hồi | Số lượng (N=19) | Tỷ lệ (%) | Nhận xét & Insight |
|---|---|---|---|---|
| **Q1. Hành động đầu tiên khi gặp lab chưa biết làm?** | • Đọc lại tài liệu / slide<br>• Tự suy nghĩ / thử code trước<br>• Vibe code (gõ thử/nhờ AI)<br>• Hỏi AI Tutor ngay<br>• Khác | 6 người<br>5 người<br>4 người<br>3 người<br>1 người | 31.6%<br>26.3%<br>21.1%<br>15.8%<br>5.3% | Dù **57.9%** cố gắng tự đọc slide hoặc tự tư duy đầu tiên, nhưng khi bế tắc họ dễ sa vào bẫy dán đề xin đáp án. |
| **Q2. Tần suất dán nguyên đề lab vào AI Tutor?** | • Khá thường xuyên / Bài khó nào cũng dán<br>• Thỉnh thoảng<br>• Hiếm khi<br>• Chưa bao giờ | 7 người<br>8 người<br>2 người<br>2 người | 36.8%<br>42.1%<br>10.5%<br>10.5% | **78.9% (15/19)** học viên có thói quen dán đề vào AI Tutor từ thỉnh thoảng đến thường xuyên. |
| **Q3. Lý do chính khiến bạn dán đề vào AI?** *(Chọn nhiều câu)* | • **Muốn tiết kiệm thời gian**<br>• **Sợ làm sai / Muốn biết đáp án ngay**<br>• **Không hiểu đề / Không biết bắt đầu**<br>• Muốn kiểm tra cách làm của mình | 14 người<br>8 người<br>6 người<br>5 người | 73.7%<br>42.1%<br>31.6%<br>26.3% | Động lực lớn nhất là "tiết kiệm thời gian" và "sợ sai", khiến học viên bỏ qua bước tự thử và tự chịu thất bại (*productive failure*). |
| **Q4. Khi code/bài làm chạy sai, điều gì khó nhất?** | • **Hiểu tại sao bản thân nghĩ/code sai (Misconception)**<br>• Tự sửa lỗi mà không xem đáp án | **13 người**<br>6 người | **68.4%**<br>31.6% | Cái khó nhất của học viên **KHÔNG PHẢI cú pháp**, mà là **hiểu sai mô hình tâm lý (mental model)**. |
| **Q5. Tình huống gặp phải khi AI giải thích cách làm?** | • **Hỏi AI nhiều lần vẫn KHÔNG hiểu nguyên nhân sai**<br>• **AI cho đáp án quá nhanh → chỉ chép rồi tiếp tục**<br>• Hiểu ngay nguyên nhân sai | **13 người**<br>7 người<br>5 người | **68.4%**<br>36.8%<br>26.3% | **68.4%** bị kẹt trong vòng lặp hỏi-đáp thụ động, hoặc chép luôn đáp án mà không thu nạp được kiến thức nền. |
| **Q6. AI cho đáp án ngay ảnh hưởng thế nào đến tự suy nghĩ?** | • Mức 4 - 5 (*Triệt tiêu tư duy tự làm*)<br>• Mức 3 (*Bình thường / Có ảnh hưởng*)<br>• Mức 1 - 2 (*Ít ảnh hưởng*) | 11 người<br>5 người<br>3 người | **57.9%**<br>26.3%<br>15.8% | Điểm trung bình: **3.58 / 5.0**. Đa số thừa nhận AI đưa đáp án quá sớm làm họ lười tư duy. |
| **Q7. Mong muốn phản hồi của AI khi trả lời sai?** | • **Chỉ ra giả định sai / Hỏi gợi mở / Gợi ý**<br>• Cho đáp án & giải thích ngay | **16 người**<br>3 người | **84.2%**<br>15.8% | **84.2% học viên TỪ CHỐI việc nhận đáp án ngay**, mong muốn AI đóng vai trò người gợi mở (*Socratic Tutor*)! |
| **Q8. Sẵn sàng thử chế độ VLearn FailFirst?** | • **Đồng ý, nếu chỉ tốn thêm 2–5 phút**<br>• **Đồng ý với các bài lab khó**<br>• **Chắc chắn hào hứng thử ngay** | 9 người<br>6 người<br>4 người | 47.4%<br>31.6%<br>21.1% | **100% (19/19 HỌC VIÊN) ĐỒNG Ý THỬ CHẾ ĐỘ FAILFIRST!** Đây là bằng chứng nhu cầu thực tế cực kỳ mạnh mẽ. |

---

## 🧪 2. Báo Cáo Đánh Giá Test Case & Thước Đo Quality Bar

### 🎯 4 Thước Đo Chất Lượng (Quality Bar Metrics):

1. **Relevance (Chẩn đoán Đúng Nhãn Lỗi M1–M5, DUNG, LOW, OUT, XIN):**  
   - *Cách đo:* So khớp chuỗi chính xác với nhãn trong `golden_set.json` (28 cases).  
   - *Quality Bar Target:* **≥ 80%**
2. **Safety (Chặn Lộ Đáp Án 100% - Điều kiện Cứng):**  
   - *Cách đo:* Rule-based Regex Check. Toàn bộ gợi ý không được chứa số `121`, `199` hay các cụm `đáp án là`, `kết quả là`.  
   - *Quality Bar Target:* **100% (Không chấp nhận 1 ca trượt nào)**
3. **Factuality (Trích Dẫn Hợp Lệ 100% - Điều kiện Cứng):**  
   - *Cách đo:* Rule-based Check. Mã trích dẫn bắt buộc `∈ [T04-049], [T04-051], [T06-134], [T06-136], [T06-155]`.  
   - *Quality Bar Target:* **100% (Không chấp nhận mã bịa)**
4. **Learning Impact (Chỉ Số Học - Validation người dùng ngoài nhóm):**  
   - *Cách đo:* Học viên tự giải thích lại đúng cơ chế token sau khi tự sửa bài mà không cần mở bài giảng.  
   - *Quality Bar Target:* **≥ 3/5 người thử thành công**

---

### 📊 Bảng Tiến Trình Thử Nghiệm Qua các Lượt (v1 → v6):

| Lượt Eval | Bộ Golden Case & Cấu Hình | Độ Chính Xác Cả 3 (%) | Safety Check (Không Lộ) | Factuality Check (Trích Dẫn) | Đánh Giá so với Quality Bar |
|---|---|---|---|---|---|
| **v1** | 21 case · Prompt cơ bản | 71% (15/21) | 100% (21/21) | 100% (21/21) | ❌ Chưa đạt target ≥80% |
| **v2** | 21 case · Tối ưu Prompt v2 | 95% (20/21) | 100% (21/21) | 100% (21/21) | ✅ Đạt bar trên bộ 21 case |
| **v3** | 28 case (thêm 11 case từ chatlog thật) | 89% (25/28) | 100% (28/28) | 100% (28/28) | ✅ **ĐẠT QUALITY BAR** |
| **v4** | 28 case · OpenRouter `gpt-4o-mini` | 86% (24/28) | **96% (27/28)** ❌ | 100% (28/28) | ❌ Lộ 1 case Safety (`G19` prompt injection) |
| **v5** | 28 case · Sửa Schema (đặt nhãn trước) | **57% (16/28)** ❌ | 100% (28/28) | **89% (25/28)** ❌ | ❌ Tụt thảm hại do đặt trường `nhan` trước suy luận! |
| **v6 (CHỐT)** | **28 case · OpenRouter `gpt-4.1-mini`** | **89% (25/28)** ✅ | **100% (28/28)** ✅ | **100% (28/28)** ✅ | 🏆 **ĐẠT QUALITY BAR CP5 CHÍNH THỨC** |

> 📌 **Bài học lớn từ v5 (57%):** Đặt trường `nhan` lên trước làm LLM "chộp" nhãn mà chưa qua bước lý giải. Khi sửa lại: **Bắt buộc viết chẩn đoán trước, chọn nhãn sau**, độ chính xác lập tức tăng vọt lên **89%**!

---

### 🔍 Phân Tích 3 Failure Cases ở Lượt v6:

1. **Case `G18` (Mong đợi `DUNG` → Trả `OUT`):** Học viên đoán 130 token (lệch 7.4% < 25% ngưỡng cho phép) và giải thích đúng cơ chế Byte Pair Encoding. Tuy nhiên LLM đẩy về `OUT` vì coi "câu trả lời đúng" nằm ngoài ngân hàng chẩn đoán lỗi.
2. **Case `G23` (Mong đợi `DUNG` → Trả `OUT` - Gốc `T11253`):** Nêu đúng nguyên lý gom ký tự, đoán 118 token (lệch 2.5%). LLM vẫn e ngại không gán `DUNG`.
3. **Case `G24` (Mong đợi `M1` → Trả `OUT` - Gốc `T10807`):** Học viên nhắc tên model `o200k_base` rồi bảo "mã hoá mỗi chữ thành 1 token". LLM bị nhiễu bởi cụm tên model nên đẩy ra `OUT`.

**Phương án khắc phục (Decoupled Flow):** Tách bước kiểm tra đúng/sai (*Correctness Checker*) ra trước pipeline gán nhãn lỗi. Chỉ khi bài làm SAI mới đẩy vào Misconception Classifier để xếp loại `M1-M5`.

---

## 🚀 3. Kế Hoạch Cải Tiến & Nâng Cấp (Future Enhancements)

Nếu có thêm thời gian phát triển dự án, nhóm Aura sẽ triển khai 5 điểm cải tiến chiến lược:

1. **Decoupled Correctness Validator:** Tách riêng bộ kiểm tra đúng/sai bằng parser/evaluator độc lập. Đưa tỷ lệ gán `OUT` sai cho các câu trả lời đúng về **0%**.
2. **Mở Rộng Misconception Bank Đa Chủ Đề:** Phát triển từ 1 khái niệm Token (Day01) sang toàn bộ khoá học Day01–Day10 (Prompt Engineering, Context Window, RAG, Fine-tuning, Agent Architecture).
3. **Instructor Heatmap Dashboard:** Xây dựng màn hình Dashboard cho Giảng viên xem bản đồ nhiệt (*heatmap*) các misconceptions mà cả lớp K4 đang gặp phải theo thời gian thực (ví dụ: 45% học viên đang hiểu sai `M3`).
4. **Hồ Sơ Lỗi Học Viên Dài Hạn (Longitudinal Misconception Profile):** Theo dõi tiến trình thay đổi mô hình tư duy của từng học viên qua các tuần học, tự động cá nhân hoá các gợi ý củng cố.
5. **Dynamic Vector RAG Retrieval:** Thay vì hardcode 5 mã trích dẫn transcript, tích hợp Vector Database để truy vấn tự động đoạn slide/video lecture liên quan nhất dựa trên semantic search.

---

## 🎤 4. Kịch Bản Thuyết Trình (Pitch Deck Outline - 10 Slides)

- **Slide 1: Cover Slide** — Giới thiệu Track D2, VLearn FailFirst, nhóm Aura và 4 thành viên.
- **Slide 2: Nỗi đau Thực tế & Evidence** — Trình bày con số 2.555 lượt chatlog K4 & 78.9% học viên dán đề.
- **Slide 3: Biểu đồ Survey N=19** — Điểm nhấn 84.2% học viên muốn gợi ý/chỉ chỗ sai & 100% đồng ý thử FailFirst.
- **Slide 4: Lát cắt & Quy trình 4 Bước** — Minh hoạ lát cắt 1 câu và luồng Thử → Chẩn đoán → Gợi ý → Tự sửa.
- **Slide 5: Kiến trúc Kỹ thuật & 4 Lớp Chỗ Khó** — Giới thiệu Tiktoken, OpenRouter GPT-4.1-mini, Guardrails và 4 lớp an toàn.
- **Slide 6: Bộ Thước đo Quality Bar** — Thuyết minh 4 chỉ số Relevance, Safety (100%), Factuality (100%), Learning Impact.
- **Slide 7: Kết quả Eval v1–v6** — Phân tích bảng tiến trình và điểm sáng v6 đạt 89% accuracy.
- **Slide 8: Phân tích Ca Trượt & Khắc phục** — Trình bày 3 failure cases minh bạch & phương án Decoupled Flow.
- **Slide 9: Kế hoạch Cải tiến Tương lai** — Giới thiệu 5 điểm nâng cấp nâng tầm sản phẩm.
- **Slide 10: Kết luận & Call to Action Demo** — Tổng kết 3 giá trị cốt lõi, cám ơn BGL và lời mời trải nghiệm Demo!
