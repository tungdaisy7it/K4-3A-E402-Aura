# 🎤 Kịch Bản Thuyết Trình 5 Phút (Pitch Script) — VLearn FailFirst

**Dự án:** VLearn FailFirst · **Nhóm:** Aura (Lớp 3A · Phòng E402)  
**Track D2:** Học từ lỗi trước (Productive Failure)  
**Tổng thời lượng:** 5 phút (300 giây) · **File Slide sử dụng:** [`VLearn_Pitch_Deck_v2.pptx`](file:///d:/AI-Lab/K4-3A-E402-Aura/VLearn_Pitch_Deck_v2.pptx) / [`slide_pitch_cp5.html`](file:///d:/AI-Lab/K4-3A-E402-Aura/slide_pitch_cp5.html)

---

## ⏱️ Phân Bổ Thời Gian Tóm Tắt (Time Alignment)

| Slide | Chủ đề Slide | Thời lượng | Mục tiêu cần đạt |
|---|---|---|---|
| **Slide 1** | Cover & Giới thiệu Nhóm | **20 giây** | Gợi mở sự tò mò, khẳng định tên sản phẩm & đề D2 |
| **Slide 2** | Nỗi đau Thực tế & Evidence K4 | **40 giây** | Chứng minh pain point bằng con số thật (2.555 lượt chatlog) |
| **Slide 3** | Khảo sát Học viên (N = 19) | **40 giây** | Đưa ra insight bùng nổ: **84.2%** từ chối đáp án, **100%** đồng ý thử |
| **Slide 4** | Lát cắt Sản phẩm & Quy trình 4 Bước | **35 giây** | Trình bày Lát cắt 1 câu & Luồng UX Socratic |
| **Slide 5** | Kiến trúc Kỹ thuật & 4 Lớp Chỗ Khó | **35 giây** | Khoe Tiktoken thật + OpenRouter GPT-4.1-mini + Guardrails |
| **Slide 6** | Bộ Thước đo Chất lượng (Quality Bar) | **30 giây** | Chốt 4 chỉ số đo lường cứng, 100% Safety & Factuality |
| **Slide 7** | Kết quả Eval Test Case v1 $\rightarrow$ v6 | **35 giây** | Nổi bật kết quả **v6 ĐẠT 89%** & bài học đắt giá từ v5 |
| **Slide 8** | Phân tích 3 Failure Cases & Decoupled Flow | **30 giây** | Minh bạch lỗi sai & giải pháp tách luồng kiểm tra đúng/sai |
| **Slide 9** | Kế hoạch Cải tiến & Mở rộng Tương lai | **25 giây** | Mở rộng ngân hàng lỗi & Instructor Dashboard |
| **Slide 10** | Kết luận & Call to Action Demo | **20 giây** | Chốt 3 lý do thắng & mời BGK xem Demo |

---

## 📝 Script Chi Tiết Cho Từng Slide

---

### 🟢 Slide 1: Cover & Mở Đầu (0:00 - 0:20 · 20 giây)
> **[HÀNH ĐỘNG]:** Bấm bật Slide 1. Giọng nói tự tin, năng lượng cao, mỉm cười chào Ban Giám Khảo.

**🗣️ LỜI THOẠI:**
> "Kính chào Ban Giám Khảo và các bạn học viên Lớp 3A!  
> Tôi là **Lê Thanh Tùng**, đại diện nhóm Aura. Hôm nay nhóm chúng tôi mang tới bài pitch cho sản phẩm **VLearn FailFirst** thuộc Track D2 — *Học từ lỗi trước*.  
> Thông điệp cốt lõi của chúng tôi là: **Biến mỗi lỗi sai thành một cơ hội tư duy sâu**, thay vì để AI cho đáp án quá sớm!"

---

### 🟢 Slide 2: Nỗi Đau Thực Tế & Evidence Chatlog (0:20 - 1:00 · 40 giây)
> **[HÀNH ĐỘNG]:** Bấm chuyển sang Slide 2. Chỉ tay vào con số 2.555 lượt chatlog.

**🗣️ LỜI THOẠI:**
> "Mining từ **2.555 lượt chatlog thực tế** của học viên Khóa 4, nhóm phát hiện một hiện trạng đáng lo ngại:  
> Có **103 lượt** học viên dán nguyên đề bài hoặc đòi *'cho xin full code'*. Và trong **100%** các ca đó, hệ thống AI Tutor cũ **không hề hỏi ngược lại một câu nào** để kích thích tư duy.  
> Nguy hiểm hơn, khi học viên báo code chạy lỗi (65 lượt), hệ thống lập tức giảng lại lý thuyết suông thay vì giúp học viên tìm ra **giả định sai gốc rễ**. Học viên nộp được bài, nhưng kiến thức nền thì hoàn toàn rỗng!"

---

### 🟢 Slide 3: Biểu Đồ Khảo Sát Học Viên N = 19 (1:00 - 1:40 · 40 giây)
> **[HÀNH ĐỘNG]:** Bấm chuyển Slide 3. Giọng nhấn mạnh vào 2 con số nổi bật **84.2%** và **100%**.

**🗣️ LỜI THOẠI:**
> "Khảo sát chuyên sâu trên **19 học viên K4**, chúng tôi thu được những con số biết nói:  
> • **78.9%** thừa nhận có thói quen dán đề vào AI vì muốn tiết kiệm thời gian.  
> • **68.4%** khẳng định điều khó nhất khi code sai là *hiểu tại sao bản thân tư duy sai*.  
> Nhưng đây mới là insight bùng nổ nhất: Có tới **84.2% học viên TỪ CHỐI việc lấy đáp án ngay** — họ thèm được AI chỉ ra giả định sai và đưa gợi ý để tự sửa!  
> Và kết quả là **100% 19/19 học viên hào hứng ĐỒNG Ý THỬ chế độ VLearn FailFirst**!"

---

### 🟢 Slide 4: Lát Cắt Sản Phẩm & Quy Trình 4 Bước (1:40 - 2:15 · 35 giây)
> **[HÀNH ĐỘNG]:** Bấm chuyển Slide 4. Đọc lướt qua Lát cắt 1 câu và chỉ vào 4 ô quy trình.

**🗣️ LỜI THOẠI:**
> "Để giải bài toán này trong 47.5h, nhóm chốt lát cắt 1 câu: *Học viên làm bài dự đoán Token tiếng Việt $\rightarrow$ AI chẩn đoán đúng giả định sai M1–M5 $\rightarrow$ Đưa 1 gợi ý kèm trích dẫn $\rightarrow$ Học viên tự sửa đúng mới được mở bài giảng.*  
> Flow UX gồm 4 bước:  
> 1. **Dự đoán:** Buộc tự thử trước khi đọc slide.  
> 2. **Chẩn đoán:** AI xếp loại lỗi ngầm.  
> 3. **Gợi ý Bậc 1:** Đưa câu hỏi dẫn dắt, **100% không lộ đáp án**.  
> 4. **Tự sửa:** Học viên giải thích lại đúng cơ chế mới được xem bài giảng đầy đủ."

---

### 🟢 Slide 5: Kiến Trúc Kỹ Thuật & 4 Lớp An Toàn (2:15 - 2:50 · 35 giây)
> **[HÀNH ĐỘNG]:** Bấm chuyển Slide 5. Nhấn mạnh vào chữ 'Tiktoken Thật' và 'Guardrails Luật Cứng'.

**🗣️ LỜI THOẠI:**
> "Về kỹ thuật, chúng tôi không dùng LLM để đếm token vì LLM đếm token rất hay sai.  
> Chúng tôi kết hợp **Tiktoken thật** để đếm token chính xác, gọi **OpenRouter GPT-4.1-mini** (temp=0, JSON mode) làm Core Diagnoser, và bọc bên ngoài bằng **Bộ Hậu Kiểm Luật Cứng (Guardrails)**:  
> • Chặn 100% lộ số đáp án (con số 121, 199).  
> • Chặn 100% mã trích dẫn bịa.  
> Đặc biệt, hệ thống được thiết kế theo nguyên tắc G10: **Thà thừa nhận LOW hay OUT chứ nhất định không đoán bừa giả định sai của học viên!**"

---

### 🟢 Slide 6: Bộ Thước Đo Chất Lượng - Quality Bar (2:50 - 3:20 · 30 giây)
> **[HÀNH ĐỘNG]:** Bấm chuyển Slide 6. Đọc rõ 4 tiêu chí đo lường.

**🗣️ LỜI THOẠI:**
> "Chất lượng sản phẩm được nhóm khóa cứng tại CP4 qua **4 chỉ số Quality Bar**:  
> 1. **Relevance:** Chẩn đoán đúng nhãn lỗi trên Golden Set 28 cases (target $\ge 80\%$).  
> 2. **Safety (Điều kiện cứng 100%):** Tuyệt đối không lộ con số đáp án.  
> 3. **Factuality (Điều kiện cứng 100%):** Mã trích dẫn bắt buộc thuộc transcript bài giảng thật.  
> 4. **Learning Impact:** Khảo sát người dùng ngoài nhóm tự giải thích lại đúng cơ chế sau khi tự sửa (target $\ge 3/5$ người)."

---

### 🟢 Slide 7: Kết Quả Eval Test Case v1 $\rightarrow$ v6 (3:20 - 3:55 · 35 giây)
> **[HÀNH ĐỘNG]:** Bấm chuyển Slide 7. Chỉ vào dòng v6 màu xanh nhạt nổi bật.

**🗣️ LỜI THOẠI:**
> "Trải qua 6 lượt thử nghiệm liên tục trên 28 Golden Cases:  
> Lượt v5 nhóm bị tụt xuống 57% vì một lỗi prompt đặt trường `nhan` lên trước phần suy luận. Nhóm đã rút bài học: **Phải để LLM suy luận chẩn đoán trước khi chọn nhãn!**  
> Kết quả tại **lượt v6 chính thức**: Đạt **89% Accuracy (25/28)**, **100% Safety** và **100% Factuality** $\rightarrow$ **VƯỢT QUALITY BAR CP5!**"

---

### 🟢 Slide 8: Phân Tích Ca Trượt & Giải Pháp Tách Luồng (3:55 - 4:25 · 30 giây)
> **[HÀNH ĐỘNG]:** Bấm chuyển Slide 8. Giọng minh bạch, thẳng thắn.

**🗣️ LỜI THOẠI:**
> "Không giấu giếm failure cases, tại v6 nhóm còn **3/28 ca trượt** (G18, G23, G24).  
> Nguyên nhân gốc: Khi học viên trả lời ĐÚNG, LLM có xu hướng đẩy câu trả lời đó ra nhãn `OUT` vì coi nó nằm ngoài ngân hàng chẩn đoán lỗi.  
> **Giải pháp khắc phục:** Nhóm thiết kế luồng **Decoupled Flow** — Tách riêng bước kiểm tra đúng/sai (*Correctness Checker*) ra trước. Chỉ khi bài làm SAI mới đẩy vào Misconception Classifier!"

---

### 🟢 Slide 9: Kế Hoạch Cải Tiến Tương Lai (4:25 - 4:50 · 25 giây)
> **[HÀNH ĐỘNG]:** Bấm chuyển Slide 9. Giới thiệu ngắn gọn 3 ý cải tiến.

**🗣️ LỜI THOẠI:**
> "Nếu có thêm thời gian phát triển, nhóm Aura sẽ triển khai 3 định hướng mở rộng:  
> 1. Mở rộng Misconception Bank cho **toàn bộ 10+ bài lab** (Prompting, RAG, Fine-tuning).  
> 2. Xây dựng **Instructor Heatmap Dashboard** giúp Giảng viên xem bản đồ nhiệt các lỗi cả lớp K4 đang kẹt theo thời gian thực.  
> 3. Tích hợp **Vector RAG** để truy vấn tự động đoạn slide/transcript liên quan."

---

### 🟢 Slide 10: Kết Luận & Call To Action Demo (4:50 - 5:10 · 20 giây)
> **[HÀNH ĐỘNG]:** Bấm chuyển Slide 10. Mỉm cười cúi chào BGK, giọng kết thúc ấn tượng.

**🗣️ LỜI THOẠI:**
> "Tóm lại, **VLearn FailFirst** mang tới một giải pháp AI Giáo dục thực chất: *Bằng chứng thật từ 2.555 chatlogs + 19 survey học viên, Quality Bar đạt 89% và kiến trúc sẵn sàng tích hợp vào VLearn!*  
> Xin chân thành cảm ơn Ban Giám Khảo và các bạn! Sau đây xin mời BGK trải nghiệm sản phẩm trực tiếp qua bản Demo!"

---

## 💡 Mẹo Thuyết Trình Ăn Điểm (Pro Pitching Tips)

1. **Tốc độ nói (Pacing):** Nói vừa phải, khoảng 120 - 130 từ/phút. Không đọc nguyên văn chữ trên slide mà dùng từ ngữ sinh động.
2. **Tương tác ánh mắt (Eye Contact):** Nhìn đều 3 phía Ban Giám Khảo khi nói về phần Evidence (Slide 2-3) và Quality Bar (Slide 6-7).
3. **Chuyển Slide nhịp nhàng:** Bấm chuyển slide ngay khi vừa nói xong câu mở đầu của slide đó.
4. **Sẵn sàng Demo:** Mở sẵn tab `http://127.0.0.1:5050` trên trình duyệt để khi vừa dứt câu Slide 10 là có thể chuyển ngay sang màn hình Demo thao tác thật!
