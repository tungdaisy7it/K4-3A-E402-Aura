import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # Set slide dimensions to 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6] # Blank layout

    # Colors
    NAVY_DARK = RGBColor(15, 23, 42)
    NAVY_TITLE = RGBColor(30, 58, 138)
    TEXT_MUTED = RGBColor(71, 85, 105)
    BLUE_PRIMARY = RGBColor(2, 132, 199)
    BLUE_BG = RGBColor(224, 242, 254)
    PINK_ACCENT = RGBColor(236, 72, 153)
    PINK_BG = RGBColor(252, 231, 243)
    GREEN_ACCENT = RGBColor(16, 185, 129)
    GREEN_BG = RGBColor(236, 253, 245)
    CARD_BG = RGBColor(255, 255, 255)
    GRAY_BG = RGBColor(248, 250, 252)
    BORDER_COLOR = RGBColor(226, 232, 240)

    def add_header(slide, meta_text, title_text, subtitle_text=""):
        # Meta badge
        meta_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        tf = meta_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = meta_text.upper()
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = BLUE_PRIMARY

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.7))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY_TITLE

        if subtitle_text:
            p_sub = tf_t.add_paragraph()
            p_sub.text = subtitle_text
            p_sub.font.size = Pt(13)
            p_sub.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
        return shape

    def add_footer(slide, current_page, total_pages=10):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.35))
        tf = footer_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"VLearn FailFirst — Pitch Deck CP5 | Nhóm Aura (Lớp 3A · E402)"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED
        
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.RIGHT
        p2.text = f"Trang {current_page} / {total_pages}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MUTED

    # ==================== SLIDE 1: COVER ====================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = GRAY_BG
    bg1.line.color.rgb = GRAY_BG

    card1 = add_card(slide1, 1.0, 1.0, 11.333, 5.5, bg_color=CARD_BG, border_color=BLUE_PRIMARY)
    tf1 = card1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "TRACK D2 — HỌC TỪ LỖI TRƯỚC (FAILFIRST)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_PRIMARY
    
    p = tf1.add_paragraph()
    p.text = "\nVLearn FailFirst"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = NAVY_TITLE

    p = tf1.add_paragraph()
    p.text = "Biến lỗi sai thành cơ hội tư duy — Chẩn đoán giả định sai & Hướng dẫn Socratic\n"
    p.font.size = Pt(18)
    p.font.color.rgb = TEXT_MUTED

    p = tf1.add_paragraph()
    p.text = "------------------------------------------------------------------------------------------------------------------"
    p.font.color.rgb = BORDER_COLOR

    p = tf1.add_paragraph()
    p.text = "\n👥 Nhóm Aura (Lớp 3A · Phòng E402)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    p = tf1.add_paragraph()
    p.text = "• Lê Thanh Tùng (2A202602499) — Leader & Spec & Quality Bar"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    p = tf1.add_paragraph()
    p.text = "• Đậu Văn Thạch (2A202602592) — Evidence Mining & Survey (N=19) & User Validation"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    p = tf1.add_paragraph()
    p.text = "• Nguyễn Thu Hằng (2A202602463) — Misconception Bank & Golden Set & Eval Automation"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    p = tf1.add_paragraph()
    p.text = "• Đinh Quốc Bảo (2A202602933) — Core Prototype & Tiktoken Integration & Flow Demo"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED


    # ==================== SLIDE 2: PAIN & EVIDENCE (SURVEY N=19) ====================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "§1. Nỗi đau Thực tế & Bằng chứng", "Học viên dán đề xin đáp án -> AI cho kết quả quá sớm triệt tiêu tư duy", "Mining 2.555 lượt chatlog K4 + Khảo sát chuyên sâu N = 19 học viên")
    
    # Card 1: Chatlog Mining
    c1 = add_card(slide2, 0.8, 1.8, 5.6, 4.9, bg_color=CARD_BG)
    tf = c1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📊 Chatlog Mining K4 (2.555 lượt)"
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = NAVY_TITLE
    
    items1 = [
        "• 103 lượt (38 học viên) dán nguyên đề hoặc đòi full code / đáp án ngay.",
        "• 0/103 lượt hệ thống cũ hỏi ngược lại để gợi ý tư duy (ask_probing_question = 0).",
        "• 65 lượt báo lỗi code -> 55 lượt hệ thống giảng lại lý thuyết suông thay vì chẩn đoán lỗi sai.",
        "• 13.474 / 13.494 lượt toàn pack hoàn toàn trống chỉ số ghi nhận mức hiểu của học viên."
    ]
    for it in items1:
        p = tf.add_paragraph()
        p.text = "\n" + it
        p.font.size = Pt(12); p.font.color.rgb = NAVY_DARK

    # Card 2: Survey N=19 Highlights
    c2 = add_card(slide2, 6.7, 1.8, 5.8, 4.9, bg_color=BLUE_BG, border_color=BLUE_PRIMARY)
    tf = c2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔥 Kết quả Survey Học viên (N = 19)"
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = NAVY_TITLE

    items2 = [
        "⚡ 78.9% (15/19) có thói quen dán đề lab vào AI Tutor từ thỉnh thoảng đến thường xuyên.",
        "⏱️ 73.7% chọn dán đề vì lý do 'Muốn tiết kiệm thời gian' & 42.1% 'Sợ làm sai / muốn đáp án ngay'.",
        "🧠 68.4% (13/19) khẳng định điều KHÓ NHẤT khi bài sai là 'Hiểu tại sao bản thân nghĩ sai'.",
        "🛑 68.4% bị kẹt vì hỏi AI nhiều lần vẫn KHÔNG hiểu nguyên nhân gốc rễ.",
        "📉 57.9% đánh giá việc AI cho đáp án ngay ảnh hưởng MẠNH (mức 4-5) đến khả năng tự suy nghĩ!"
    ]
    for it in items2:
        p = tf.add_paragraph()
        p.text = "\n" + it
        p.font.size = Pt(12); p.font.color.rgb = NAVY_DARK

    add_footer(slide2, 2)

    # ==================== SLIDE 3: DETAILED SURVEY BREAKDOWN ====================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "§1b. Phân tích Khảo sát Chi tiết", "Nhu cầu thực sự: Học viên muốn AI chỉ ra GIẢ ĐỊNH SAI thay vì cho đáp án!", "Khảo sát N = 19 học viên K4 (Q1 - Q8)")

    # Box 1: Q4 & Q5
    b1 = add_card(slide3, 0.8, 1.8, 3.7, 4.9)
    tf = b1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "❓ Cái khó nhất khi bài sai?"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = NAVY_TITLE
    p = tf.add_paragraph()
    p.text = "\n• 68.4% (13/19 người):\nHiểu tại sao bản thân tư duy/code sai (Root misconception)"
    p.font.size = Pt(12); p.font.color.rgb = NAVY_DARK
    p = tf.add_paragraph()
    p.text = "\n• 31.6% (6/19 người):\nTự sửa lỗi mà không xem đáp án"
    p.font.size = Pt(12); p.font.color.rgb = TEXT_MUTED

    p = tf.add_paragraph()
    p.text = "\n\n⚠️ Tình huống với AI Tutor hiện tại:"
    p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = PINK_ACCENT
    p = tf.add_paragraph()
    p.text = "• 68.4%: Hỏi nhiều lần vẫn không hiểu nguyên nhân gốc."
    p.font.size = Pt(11); p.font.color.rgb = NAVY_DARK
    p = tf.add_paragraph()
    p.text = "• 36.8%: AI cho đáp án quá nhanh -> chỉ chép rồi làm tiếp."
    p.font.size = Pt(11); p.font.color.rgb = NAVY_DARK

    # Box 2: Q8 - Mong muốn
    b2 = add_card(slide3, 4.7, 1.8, 3.8, 4.9, bg_color=PINK_BG, border_color=PINK_ACCENT)
    tf = b2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🎯 Học viên muốn AI làm gì?"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = NAVY_TITLE
    
    p = tf.add_paragraph()
    p.text = "\n84.2% (16/19 người)\nMUỐN AI CHỈ RA CHỖ SAI / GỢI Ý / H HỎI NGƯỢC LẠI!"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = PINK_ACCENT

    p = tf.add_paragraph()
    p.text = "\nChi tiết phân rã mong muốn:"
    p.font.size = Pt(11); p.font.bold = True
    p = tf.add_paragraph()
    p.text = "• 42.1%: Chỉ ra đang hiểu sai khái niệm nào nhưng CHƯA cho đáp án.\n• 31.6%: Hỏi thêm 1 câu để xác định chỗ hiểu sai.\n• 10.5%: Đưa 1 gợi ý ngắn để tự tìm lỗi.\n• Chỉ 15.8% (3 người): Muốn đáp án ngay."
    p.font.size = Pt(11); p.font.color.rgb = NAVY_DARK

    # Box 3: Q8b - Sẵn sàng thử FailFirst
    b3 = add_card(slide3, 8.7, 1.8, 3.8, 4.9, bg_color=GREEN_BG, border_color=GREEN_ACCENT)
    tf = b3.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🚀 Sẵn sàng thử FailFirst?"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = NAVY_TITLE

    p = tf.add_paragraph()
    p.text = "\n100% (19/19 HỌC VIÊN)\nĐỒNG Ý THỬ CHẾ ĐỘ VLEARN FAILFIRST!"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = GREEN_ACCENT

    p = tf.add_paragraph()
    p.text = "\nPhân bố điều kiện sẵn sàng:"
    p.font.size = Pt(11); p.font.bold = True
    p = tf.add_paragraph()
    p.text = "• 47.4% (9 người): Đồng ý nếu chỉ tốn thêm 2-5 phút.\n• 31.6% (6 người): Đồng ý với các bài lab khó.\n• 21.1% (4 người): Hào hứng muốn thử ngay lập tức!"
    p.font.size = Pt(11); p.font.color.rgb = NAVY_DARK

    add_footer(slide3, 3)

    # ==================== SLIDE 4: PRODUCT & SLICE ====================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "§4. Lát cắt Sản phẩm & Giải pháp", "VLearn FailFirst: Buộc tự trả lời trước -> Chẩn đoán lỗi -> Gợi ý Bậc 1 -> Tự sửa", "Lát cắt 1 câu: Khái niệm Token trong Lab Day01 Foundation")

    c_slice = add_card(slide4, 0.8, 1.8, 11.7, 1.3, bg_color=BLUE_BG, border_color=BLUE_PRIMARY)
    tf = c_slice.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📌 LÁT CẮT MỘT CÂU (ONE-SENTENCE SLICE):"
    p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = BLUE_PRIMARY
    p = tf.add_paragraph()
    p.text = "\"Một học viên trước khi xem bài giảng token trả lời bài dự đoán tiếng Việt 99 tiếng -> Hệ thống chẩn đoán đúng giả định sai cụ thể M1-M5 -> Đưa 1 gợi ý kèm trích dẫn transcript -> Học viên tự sửa và giải thích lại được cơ chế mà không cần cho đáp án.\""
    p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = NAVY_TITLE

    # 4 Steps Cards
    step_w = 2.75
    steps = [
        ("1. Dự đoán & Thử", "Học viên làm bài dự đoán token tiếng Việt. Bắt buộc tự thử trước khi xem giảng.", BLUE_BG),
        ("2. Chẩn đoán Lỗi", "LLM chẩn đoán giả định sai M1-M5. Phân biệt rõ DUNG / LOW / OUT / XIN.", PINK_BG),
        ("3. Gợi ý Bậc 1", "Chỉ đưa 1 gợi ý ngắn + mã trích dẫn transcript. KHÔNG LỘ ĐÁP ÁN.", BLUE_BG),
        ("4. Tự sửa & Giảng", "Học viên tự sửa câu trả lời. Giải thích lại đúng mới mở khoá lời giảng.", GREEN_BG)
    ]

    for idx, (stitle, sdesc, sbg) in enumerate(steps):
        sbox = add_card(slide4, 0.8 + idx * 3.0, 3.3, step_w, 3.4, bg_color=sbg)
        tf = sbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stitle
        p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = NAVY_TITLE
        p = tf.add_paragraph()
        p.text = "\n" + sdesc
        p.font.size = Pt(11); p.font.color.rgb = NAVY_DARK

    add_footer(slide4, 4)

    # ==================== SLIDE 5: TECH ARCHITECTURE & 4 CLASSES ====================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "§4-§5. Kiến trúc Kỹ thuật & 4 Lớp Chỗ Khó", "Kết hợp Tiktoken thật + OpenRouter GPT-4.1-mini + Hậu kiểm Luật cứng", "Thiết kế thiên về thừa nhận KHÔNG BIẾT (LOW/OUT) để bảo vệ tư duy học viên")

    # Left Card: Tech Stack
    c_tech = add_card(slide5, 0.8, 1.8, 5.7, 4.9)
    tf = c_tech.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⚙️ Stack Kỹ thuật (Mock+ Level)"
    p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = NAVY_TITLE
    
    titems = [
        "• Tiktoken Thật: Đếm token chính xác (o200k_base vs cl100k_base).",
        "• OpenRouter API: Core LLM Diagnostic với openai/gpt-4.1-mini (temp=0, JSON mode).",
        "• Hậu kiểm bằng luật (Guardrails):",
        "  - Regex Check: Chặn 100% lộ đáp án (121, 199, 'đáp án là').",
        "  - Factuality Check: Chặn 100% mã trích dẫn bịa không có trong transcript.",
        "• Hides answer: Thiên về gán LOW / OUT chứ không đoán bừa."
    ]
    for ti in titems:
        p = tf.add_paragraph()
        p.text = "\n" + ti
        p.font.size = Pt(11); p.font.color.rgb = NAVY_DARK

    # Right Card: 4 Problem Classes
    c_prob = add_card(slide5, 6.7, 1.8, 5.8, 4.9, bg_color=CARD_BG)
    tf = c_prob.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🛡️ 4 Lớp Chỗ Khó & Xử lý An toàn"
    p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = NAVY_TITLE

    pitems = [
        "① Trả lời ĐÚNG / Lộ đáp án: Gán DUNG (chuyển câu hỏi mở rộng) / Hậu kiểm chặn LO_DAP_AN.",
        "② Mơ hồ / Thiếu thông tin: Gán LOW -> Hỏi lại 1 câu thu hẹp phạm vi (G10).",
        "③ Ngoài thẩm quyền / Đòi đáp án: Gán XIN -> Từ chối khéo, giải thích lý do & đưa câu hỏi gợi mở.",
        "④ Đặc thù Domain & Injection: Nhận diện M3 (tỷ lệ token cố định) & bọc prompt trong <<< >>> chống injection."
    ]
    for pi in pitems:
        p = tf.add_paragraph()
        p.text = "\n" + pi
        p.font.size = Pt(11); p.font.color.rgb = NAVY_DARK

    add_footer(slide5, 5)

    # ==================== SLIDE 6: QUALITY BAR METRICS ====================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "§7. Bộ Thước đo Chất lượng (Quality Bar)", "Khóa chuẩn ĐẠT tại CP4 — 4 Tiêu chí Đo lường Khách quan", "Golden Set 28 cases (11 case từ chatlog thật K4 + 17 case nhóm tự thiết kế)")

    q_boxes = [
        ("1. Relevance (Chẩn đoán Đúng)", "Trùng nhãn mong đợi trong golden set (M1-M5, DUNG, LOW, OUT, XIN).\n\n🎯 Target: ≥ 80%", BLUE_BG, BLUE_PRIMARY),
        ("2. Safety (Không lộ đáp án)", "Deterministic Regex Check: Không chứa 121, 199, 'đáp án là'.\n\n🔒 Target: 100% (CỨNG)", PINK_BG, PINK_ACCENT),
        ("3. Factuality (Trích dẫn Đúng)", "Trích dẫn ∈ [T04-049], [T04-051], [T06-134], [T06-136], [T06-155].\n\n📌 Target: 100% (CỨNG)", BLUE_BG, BLUE_PRIMARY),
        ("4. Learning Impact (Chỉ số học)", "Học viên tự giải thích lại đúng cơ chế sau khi tự sửa bài mà không cần mở giảng.\n\n🌱 Target: ≥ 3/5 người", GREEN_BG, GREEN_ACCENT)
    ]

    for idx, (qtitle, qdesc, qbg, qcolor) in enumerate(q_boxes):
        col = idx % 2
        row = idx // 2
        qbox = add_card(slide6, 0.8 + col * 5.9, 1.8 + row * 2.5, 5.7, 2.3, bg_color=qbg, border_color=qcolor)
        tf = qbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = qtitle
        p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = NAVY_TITLE
        p = tf.add_paragraph()
        p.text = "\n" + qdesc
        p.font.size = Pt(11); p.font.color.rgb = NAVY_DARK

    add_footer(slide6, 6)

    # ==================== SLIDE 7: EVAL RESULTS ITERATIONS ====================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "§7. Kết quả Đánh giá Test Case qua các Lượt", "Tiến trình thử nghiệm từ v1 đến v6: Model gpt-4.1-mini ĐẠT Quality Bar!", "Đã đối chiếu công khai trên bộ 28 Golden Cases")

    # Table card
    c_table = add_card(slide7, 0.8, 1.8, 11.7, 4.9)
    tf = c_table.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📊 Bảng Kết quả Chạy Chẩn đoán qua 6 Iteration"
    p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = NAVY_TITLE

    # Add PPT table
    rows, cols = 7, 6
    left, top, width, height = Inches(1.0), Inches(2.3), Inches(11.3), Inches(4.1)
    table_shape = slide7.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(1.1)
    table.columns[1].width = Inches(2.6)
    table.columns[2].width = Inches(1.8)
    table.columns[3].width = Inches(1.8)
    table.columns[4].width = Inches(1.8)
    table.columns[5].width = Inches(2.2)

    headers = ["Lượt", "Bộ Case & Cấu hình", "Đạt cả 3 (%)", "Safety (Không lộ)", "Factuality (Trích)", "Đánh giá Quality Bar"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid(); cell.fill.fore_color.rgb = BLUE_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = RGBColor(255, 255, 255)

    data = [
        ["v1", "21 case · Prompt cơ bản", "71% (15/21)", "100% (21/21)", "100% (21/21)", "❌ Chưa đạt (<80%)"],
        ["v2", "21 case · Tối ưu prompt v2", "95% (20/21)", "100% (21/21)", "100% (21/21)", "✅ Đạt bar cũ"],
        ["v3", "28 case (thêm 11 case thật)", "89% (25/28)", "100% (28/28)", "100% (28/28)", "✅ ĐẠT QUALITY BAR"],
        ["v4", "28 case · OpenRouter gpt-4o-mini", "86% (24/28)", "96% (27/28) ❌", "100% (28/28)", "❌ Lộ 1 case Safety!"],
        ["v5", "28 case · Sửa Schema (đặt nhãn trước)", "57% (16/28) ❌", "100% (28/28)", "89% (25/28) ❌", "❌ Tụt thảm hại vì Prompt!"],
        ["v6", "28 case · OpenRouter gpt-4.1-mini", "89% (25/28)", "100% (28/28) ✅", "100% (28/28) ✅", "🏆 ĐẠT BAR CP5 CHÍNH THỨC"]
    ]

    for row_idx, row_data in enumerate(data):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = text
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if row_idx == 5: # Highlight v6
                cell.fill.solid(); cell.fill.fore_color.rgb = GREEN_BG
                p.font.bold = True; p.font.color.rgb = NAVY_TITLE

    add_footer(slide7, 7)

    # ==================== SLIDE 8: FAILURE CASE ANALYSIS ====================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "§7b. Phân tích Ca Trượt & Phương án Khắc phục", "Phân tích 3/28 ca trượt tại v6 — Minh bạch nguyên nhân & Giải pháp", "Không giấu giếm failure cases — Học trực tiếp từ lỗi để cải tiến")

    f_card1 = add_card(slide8, 0.8, 1.8, 5.7, 4.9, bg_color=PINK_BG, border_color=PINK_ACCENT)
    tf = f_card1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔍 Chi tiết 3 Ca Trượt tại Lượt v6"
    p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = PINK_ACCENT

    fitems = [
        "1. Case G18 (Mong đợi DUNG -> Trả OUT): Học viên đoán 130 token (lệch 7.4% < 25%) & giải thích đúng cơ chế. LLM vẫn đẩy về OUT vì coi trả lời đúng là ngoài bank.",
        "2. Case G23 (Mong đợi DUNG -> Trả OUT - Gốc T11253): Nêu đúng Byte Pair Encoding, đoán 118 token (lệch 2.5%). LLM vẫn ngần ngại không gán DUNG.",
        "3. Case G24 (Mong đợi M1 -> Trả OUT - Gốc T10807): Học viên nhắc tên model o200k_base rồi bảo 'mã hoá mỗi chữ thành 1 token'. LLM bị nhiễu bởi tên model nên đẩy ra OUT."
    ]
    for fi in fitems:
        p = tf.add_paragraph()
        p.text = "\n" + fi
        p.font.size = Pt(10.5); p.font.color.rgb = NAVY_DARK

    f_card2 = add_card(slide8, 6.7, 1.8, 5.8, 4.9, bg_color=BLUE_BG, border_color=BLUE_PRIMARY)
    tf = f_card2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "💡 Nguyên nhân Gốc & Giải pháp Khắc phục"
    p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = NAVY_TITLE

    p = tf.add_paragraph()
    p.text = "\n📌 Nguyên nhân Gốc:"
    p.font.size = Pt(12); p.font.bold = True
    p = tf.add_paragraph()
    p.text = "Cả 3 ca đều rơi về OUT, trong đó 2/3 ca là nhãn DUNG. LLM đang coi 'học viên đúng' là một trường hợp ngoài bank chẩn đoán lỗi nên đẩy ra OUT."
    p.font.size = Pt(11); p.font.color.rgb = NAVY_DARK

    p = tf.add_paragraph()
    p.text = "\n🛠️ Phương án Khắc phục (Tách Luồng):"
    p.font.size = Pt(12); p.font.bold = True
    p = tf.add_paragraph()
    p.text = "Tách nhãn DUNG ra khỏi pipeline so sánh với Misconception Bank:\n1. Bước 1: Kiểm tra câu trả lời có đúng cơ chế/con số không (Correctness Checker).\n2. Bước 2: CHỈ KHI SAI mới đẩy vào Misconception Classifier để gán M1-M5."
    p.font.size = Pt(11); p.font.color.rgb = NAVY_DARK

    add_footer(slide8, 8)

    # ==================== SLIDE 9: FUTURE IMPROVEMENTS ====================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "§8. Kế hoạch Cải tiến & Mở rộng (Future Enhancements)", "Định hướng nâng cấp nếu có thêm thời gian phát triển dự án", "Từ Lát cắt Prototype 1 Khái niệm -> Hệ thống Học tập Thích ứng Toàn diện")

    imp_boxes = [
        ("1. Decoupled Validator", "Tách bước kiểm tra đúng/sai khỏi bước chẩn đoán lỗi. Giảm tỷ lệ gán OUT cho câu trả lời đúng xuống 0%.", BLUE_BG),
        ("2. Multi-Concept Misconception Bank", "Mở rộng Misconception Bank từ 1 khái niệm (Token) sang toàn bộ 10+ bài lab (Prompt, RAG, Agent, Fine-tuning).", PINK_BG),
        ("3. Instructor Heatmap Dashboard", "Xây dựng Dashboard cho Giảng viên theo dõi bản đồ nhiệt các misconceptions lớp đang gặp theo thời gian thực.", GREEN_BG),
        ("4. Longitudinal Misconception Profile", "Lưu trữ hồ sơ tiến trình thay đổi mô hình tư duy (mental model) của từng học viên qua từng tuần học.", BLUE_BG),
        ("5. Dynamic Vector RAG Search", "Truy vấn tự động đoạn slide/transcript bài giảng liên quan nhất bằng Vector DB thay vì 5 mã hardcode.", PINK_BG)
    ]

    for idx, (ititle, idesc, ibg) in enumerate(imp_boxes):
        col = idx % 3
        row = idx // 3
        w = 3.7
        h = 2.3
        ibox = add_card(slide9, 0.8 + col * 3.9, 1.8 + row * 2.5, w, h, bg_color=ibg)
        tf = ibox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = ititle
        p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = NAVY_TITLE
        p = tf.add_paragraph()
        p.text = "\n" + idesc
        p.font.size = Pt(10.5); p.font.color.rgb = NAVY_DARK

    add_footer(slide9, 9)

    # ==================== SLIDE 10: CONCLUSION & DEMO CTA ====================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "§9. Kết luận & Demo Call to Action", "VLearn FailFirst — Giải pháp AI Giáo dục Thực chất", "Bằng chứng thật · Quality Bar ĐẠT 89% · Sẵn sàng tích hợp VLearn")

    c_summary = add_card(slide10, 0.8, 1.8, 11.7, 4.9, bg_color=BLUE_BG, border_color=BLUE_PRIMARY)
    tf = c_summary.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🎯 TỔNG KẾT BÀI PITCH — TẠI SAO CHỌN VLEARN FAILFIRST?"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = NAVY_TITLE

    sitems = [
        "1. BẰNG CHỨNG VÀ NHU CẦU THỰC TẾ ĐÃ ĐƯỢC CHỨNG MINH:",
        "   - Mining 2.555 lượt chatlog K4 + Khảo sát 19 học viên: 100% học viên sẵn sàng thử chế độ FailFirst, 84.2% muốn AI gợi ý/chỉ chỗ sai thay vì đưa đáp án ngay.",
        "",
        "2. CHẤT LƯỢNG KỸ THUẬT ĐÃ ĐƯỢC KIỂM CHỨNG BẰNG CON SỐ (QUALITY BAR):",
        "   - Đạt 89% tổng quan trên bộ 28 Golden Cases (11 case thật K4).",
        "   - ĐẠT 100% Safety (chặn lộ đáp án) & 100% Factuality (trích dẫn chuẩn).",
        "",
        "3. ĐỊNH HƯỚNG TƯƠNG LAI RÕ RÀNG & KHẢ THI:",
        "   - Tách luồng kiểm tra đúng/sai, mở rộng ngân hàng lỗi sang các chủ đề RAG/Agent, dựng Dashboard cho Giảng viên.",
        "",
        "🚀 XIN CHÂN THÀNH CẢM ƠN BAN GIÁM KHẢO & HỌC VIÊN LỚP 3A!"
    ]
    for si in sitems:
        p = tf.add_paragraph()
        p.text = si
        if si.startswith("🚀") or si.startswith("🎯"):
            p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = NAVY_TITLE
        elif si and si[0].isdigit():
            p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = BLUE_PRIMARY
        else:
            p.font.size = Pt(11.5); p.font.color.rgb = NAVY_DARK

    add_footer(slide10, 10)

    # Save presentation
    output_path = r"d:\AI-Lab\K4-3A-E402-Aura\VLearn_Pitch_Deck_v2.pptx"
    prs.save(output_path)
    print(f"Successfully generated PowerPoint presentation at: {output_path}")

if __name__ == "__main__":
    create_deck()
