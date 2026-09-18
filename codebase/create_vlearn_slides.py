# -*- coding: utf-8 -*-
"""
Script tạo Slide thuyết trình PowerPoint (.pptx) lồng lộn, siêu đẹp mắt cho VLearn.
Thiết kế Dark Mode Glassmorphism cao cấp với hiệu ứng nổi bật chuẩn Pitch Deck 2026.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Ultra-Premium Dark Color Palette
    COLOR_BG_DARK = RGBColor(11, 15, 25)       # #0B0F19 (Deep Rich Midnight Dark)
    COLOR_CARD_DARK = RGBColor(17, 24, 39)     # #111827 (Dark Glass Card)
    COLOR_CARD_BORDER = RGBColor(31, 41, 55)   # #1F2937
    COLOR_BLUE_GLOW = RGBColor(56, 189, 248)   # #38BDF8 (Neon Sky Cyan)
    COLOR_RED_BRAND = RGBColor(239, 68, 68)    # #EF4444 (Vivid Crimson)
    COLOR_GREEN_GLOW = RGBColor(16, 185, 129)  # #10B981 (Emerald Glow)
    COLOR_AMBER_GLOW = RGBColor(245, 158, 11)  # #F59E0B (Radiant Amber)
    COLOR_TEXT_MAIN = RGBColor(249, 250, 251)  # #F9FAFB (Pure Bright White)
    COLOR_TEXT_DIM = RGBColor(156, 163, 175)   # #9CA3AF (Secondary Dimmed Text)
    COLOR_CARD_GREEN_BG = RGBColor(6, 44, 34)  # Soft Emerald Card Background

    blank_layout = prs.slide_layouts[6]

    def add_dark_bg(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = COLOR_BG_DARK

    def add_header(slide, title_text, category_text="VLEARN FAILFIRST AI"):
        # Header category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = "⚡ " + category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_RED_BRAND
        p_cat.font.name = "Segoe UI"

        # Main Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TEXT_MAIN
        p_title.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 1: HERO COVER SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    add_dark_bg(slide1)

    # Decorative Top Accent Bar
    accent_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = COLOR_RED_BRAND
    accent_bar.line.fill.background()

    # Brand Title
    brand_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(1.2))
    tf1 = brand_box.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "VLearn FailFirst AI"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_BLUE_GLOW
    p1.font.name = "Segoe UI"

    # Subtitle
    sub_box = slide1.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(11.3), Inches(1.5))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    
    p_sub1 = tf_sub.paragraphs[0]
    p_sub1.text = "NỀN TẢNG HỌC TỪ LỖI SAI (PRODUCTIVE FAILURE) & AI TUTOR CHẨN ĐOÁN THÔNG MINH"
    p_sub1.font.size = Pt(20)
    p_sub1.font.bold = True
    p_sub1.font.color.rgb = COLOR_TEXT_MAIN
    p_sub1.font.name = "Segoe UI"

    p_sub2 = tf_sub.add_paragraph()
    p_sub2.text = "Chuyển dịch trải nghiệm từ Học thụ động sang Chẩn đoán chủ động và Khai phá tri thức cùng AI."
    p_sub2.font.size = Pt(14)
    p_sub2.font.color.rgb = COLOR_TEXT_DIM
    p_sub2.font.name = "Segoe UI"
    p_sub2.space_before = Pt(10)

    # 3 Pill Cards on Hero Slide
    hero_cards = [
        ("⚡ FailFirst Paradigm", "Tự suy đoán & vấp ngã trước giúp tăng 3.5x khả năng ghi nhớ chủ động."),
        ("🤖 Multi-tier AI Tutor", "Chẩn đoán đúng mã giả định sai (M1..M5) & giải thích định hướng đa tầng."),
        ("🎯 Selective Unblur UI", "Mở mờ riêng từng đoạn văn đối chiếu nguồn [T04-049] sau khi tự sửa đúng.")
    ]

    card_w = Inches(3.6)
    card_gap = Inches(0.26)
    for idx, (htitle, hdesc) in enumerate(hero_cards):
        hx = Inches(1.0) + idx * (card_w + card_gap)
        card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, hx, Inches(4.5), card_w, Inches(1.8))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_DARK
        card.line.color.rgb = COLOR_BLUE_GLOW if idx == 0 else (COLOR_RED_BRAND if idx == 1 else COLOR_GREEN_GLOW)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.2)
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = htitle
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MAIN

        p_body = tf.add_paragraph()
        p_body.text = hdesc
        p_body.font.size = Pt(11)
        p_body.font.color.rgb = COLOR_TEXT_DIM
        p_body.space_before = Pt(6)

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_dark_bg(slide2)
    add_header(slide2, "1. VẤN NẠN HỌC THỤ ĐỘNG & ẢO TƯỞNG NẮM VỮNG KIẾN THỨC", "THỰC TRẠNG & NỖI ĐAU HỌC VIÊN")

    prob_cards = [
        ("📖 90% Kiến Thức Bốc Hơi", "Khi chỉ đọc slide hoặc xem video thụ động, não bộ không kích hoạt liên kết sâu. Hơn 90% kiến thức biến mất sau 24h."),
        ("🧠 Ảo Tưởng Hiểu Bài (Illusion)", "Người học cảm thấy 'hiểu bài' khi đọc qua chữ. Nhưng khi áp dụng thực chiến thì bộc lộ vô số giả định sai lệch."),
        ("❌ LMS Truyền Thống Bất Lực", "Các hệ thống LMS hiện tại chỉ chấm Đúng/Sai vô hồn, không thể chẩn đoán bản chất lỗ hổng tư duy của học viên.")
    ]

    for idx, (title, desc) in enumerate(prob_cards):
        cx = Inches(0.8) + idx * (Inches(3.6) + Inches(0.3))
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.8), Inches(3.6), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_DARK
        card.line.color.rgb = COLOR_RED_BRAND

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.3)
        tf.margin_left = Inches(0.3)
        tf.margin_right = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = COLOR_RED_BRAND

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(13)
        p_desc.font.color.rgb = COLOR_TEXT_DIM
        p_desc.space_before = Pt(14)

    # =========================================================================
    # SLIDE 3: SOLUTION COMPARISON
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_dark_bg(slide3)
    add_header(slide3, "2. GIẢI PHÁP VLEARN: PHƯƠNG PHÁP HỌC FAILFIRST", "MÔ HÌNH ĐỔI MỚI GIẢNG DẠY")

    # Left Card: Traditional
    card_l = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    card_l.fill.solid()
    card_l.fill.fore_color.rgb = COLOR_CARD_DARK
    card_l.line.color.rgb = COLOR_RED_BRAND

    tf_l = card_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_top = Inches(0.3)
    tf_l.margin_left = Inches(0.3)

    p = tf_l.paragraphs[0]
    p.text = "❌ MÔ HÌNH CỦA LMS TRUYỀN THỐNG"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED_BRAND

    p_b = tf_l.add_paragraph()
    p_b.text = "Đọc Bài Giảng -> Nghe Giảng -> Làm Quiz\n\n• Học viên tiếp thu hoàn toàn thụ động.\n• Não bộ không có kích thích vấp ngã tư duy.\n• Dễ chán nản và quên sạch kiến thức sau khi xong."
    p_b.font.size = Pt(13)
    p_b.font.color.rgb = COLOR_TEXT_DIM
    p_b.space_before = Pt(14)

    # Right Card: VLearn
    card_r = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = COLOR_CARD_GREEN_BG
    card_r.line.color.rgb = COLOR_GREEN_GLOW

    tf_r = card_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_top = Inches(0.3)
    tf_r.margin_left = Inches(0.3)

    p = tf_r.paragraphs[0]
    p.text = "✨ MÔ HÌNH VLEARN FAILFIRST AI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN_GLOW

    p_b = tf_r.add_paragraph()
    p_b.text = "Tự Thử -> AI Chẩn Đoán -> Mở Khóa Nguồn\n\n• Bắt buộc suy đoán & đưa lý do trước khi đọc.\n• AI Tutor phân loại đúng giả định sai (M1..M5).\n• Tự sửa đúng mới mở mờ đoạn văn trích dẫn nguồn."
    p_b.font.size = Pt(13)
    p_b.font.color.rgb = COLOR_TEXT_MAIN
    p_b.space_before = Pt(14)

    # =========================================================================
    # SLIDE 4: DIAGNOSTIC LOOP
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_dark_bg(slide4)
    add_header(slide4, "3. AI TUTOR CHẨN ĐOÁN DẠNG TƯƠNG TÁC ĐA TẦNG", "LUỒNG TƯƠNG TÁC HỌC VIÊN")

    steps_data = [
        ("01. Làm bài", "Nhập suy đoán & lý do (Hỗ trợ linh hoạt gõ cả Chữ và Số)."),
        ("02. AI Chẩn đoán", "AI trả nhãn sai M1..M5 & Gợi ý định hướng Tier 1."),
        ("03. Chọn tương tác", "Chọn 'Tôi đã hiểu' HOẶC 'Giải thích thêm (Tier 2)'."),
        ("04. Mở khóa Nguồn", "Nhập lại đúng bản chất -> Xác nhận thành công & mở khóa nguồn!")
    ]

    sw = Inches(2.7)
    sgap = Inches(0.3)
    for idx, (stitle, sdesc) in enumerate(steps_data):
        sx = Inches(0.8) + idx * (sw + sgap)
        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, Inches(1.8), sw, Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_GREEN_BG if idx == 3 else COLOR_CARD_DARK
        card.line.color.rgb = COLOR_GREEN_GLOW if idx == 3 else COLOR_BLUE_GLOW

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.3)
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = stitle
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = COLOR_GREEN_GLOW if idx == 3 else COLOR_BLUE_GLOW

        p2 = tf.add_paragraph()
        p2.text = sdesc
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_TEXT_DIM
        p2.space_before = Pt(12)

    # =========================================================================
    # SLIDE 5: SELECTIVE UNBLUR
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_dark_bg(slide5)
    add_header(slide5, "4. TÍNH NĂNG ĐỘC BẢN: SELECTIVE PARAGRAPH UNBLURRING", "TRẢI NGHIỆM MỞ MỜ CÓ ĐIỀU KIỆN")

    card1 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    card1.fill.solid()
    card1.fill.fore_color.rgb = COLOR_CARD_DARK
    card1.line.color.rgb = COLOR_RED_BRAND

    tf1 = card1.text_frame
    tf1.word_wrap = True
    tf1.margin_top = Inches(0.3)
    tf1.margin_left = Inches(0.3)

    p = tf1.paragraphs[0]
    p.text = "🔒 Lớp Mờ 5.5px Chống Đọc Thụ Động"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED_BRAND

    p_body = tf1.add_paragraph()
    p_body.text = "• Ở chế độ Tự học, toàn bộ bài giảng được tạm đóng che mờ.\n\n• Nhấp vào thẻ [Txx-NNN] khi chưa làm xong chỉ hiện Khung xem trước (Preview), không mở mờ bừa bãi tràn lan.\n\n• Buộc học viên tập trung tư duy vấp ngã."
    p_body.font.size = Pt(13)
    p_body.font.color.rgb = COLOR_TEXT_DIM
    p_body.space_before = Pt(12)

    card2 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    card2.fill.solid()
    card2.fill.fore_color.rgb = COLOR_CARD_GREEN_BG
    card2.line.color.rgb = COLOR_GREEN_GLOW

    tf2 = card2.text_frame
    tf2.word_wrap = True
    tf2.margin_top = Inches(0.3)
    tf2.margin_left = Inches(0.3)

    p = tf2.paragraphs[0]
    p.text = "🎯 Mở Mờ Riêng Đoạn Nguồn [T04-049]"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN_GLOW

    p_body = tf2.add_paragraph()
    p_body.text = "• Làm xong Câu 1/3, CHỈ MỞ MỜ DUY NHẤT đoạn văn trích dẫn nguồn tương ứng [T04-049].\n\n• Các đoạn khác tiếp tục che mờ cho tới khi làm xong cả 3 câu hỏi.\n\n• Đảm bảo tính liền mạch giữa Chẩn đoán và Bài đọc."
    p_body.font.size = Pt(13)
    p_body.font.color.rgb = COLOR_TEXT_MAIN
    p_body.space_before = Pt(12)

    # =========================================================================
    # SLIDE 6: PRODUCT IMPACT & TECH
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_dark_bg(slide6)
    add_header(slide6, "5. HIỆU QUẢ GIẢNG DẠY & CÔNG NGHỆ NỀN TẢNG", "GIÁ TRỊ SẢN PHẨM & KỸ THUẬT")

    tech_items = [
        ("📈 Tăng 3.5x Khả Năng Ghi Nhớ", "Kích hoạt tư duy chủ động (Active Recall) qua Productive Failure thay vì đọc thụ động."),
        ("⚡ Tiktoken Real-time Đếm Thật", "Tích hợp thuật toán nén mã hóa o200k_base (GPT-4o) tính toán chính xác 100% số token."),
        ("📚 6 Bài Học vlearn-pack", "Tích hợp toàn bộ dữ liệu transcript sạch từ Bài 1 đến Bài 6 phân theo 3 Module."),
        ("🎨 Thiết Kế Chuẩn VLearn UI", "Giao diện hiện đại, mượt mà, tối ưu trải nghiệm học tập tự nhiên chuẩn SaaS 2026.")
    ]

    for idx, (title, desc) in enumerate(tech_items):
        bx = Inches(0.8) if idx % 2 == 0 else Inches(6.9)
        by = Inches(1.8) if idx < 2 else Inches(4.35)

        card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, Inches(5.6), Inches(2.25))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_DARK
        card.line.color.rgb = COLOR_BLUE_GLOW

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.2)
        tf.margin_left = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = COLOR_BLUE_GLOW

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = COLOR_TEXT_DIM
        p_desc.space_before = Pt(6)

    # =========================================================================
    # SLIDE 7: GRAND OUTRO & CALL TO ACTION
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_dark_bg(slide7)

    # Outro Title
    tbox7 = slide7.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.33), Inches(1.5))
    tf7 = tbox7.text_frame
    tf7.word_wrap = True
    
    p = tf7.paragraphs[0]
    p.text = "VLearn — ĐỔI MỚI HỌC TẬP CÙNG AI TUTOR"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MAIN
    p.font.name = "Segoe UI"

    p2 = tf7.add_paragraph()
    p2.text = "Cảm ơn quý thầy cô và các bạn đã lắng nghe bài thuyết trình!"
    p2.font.size = Pt(18)
    p2.font.color.rgb = COLOR_BLUE_GLOW
    p2.space_before = Pt(10)

    # CTA Card
    cta_card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.8), Inches(11.33), Inches(2.6))
    cta_card.fill.solid()
    cta_card.fill.fore_color.rgb = COLOR_CARD_GREEN_BG
    cta_card.line.color.rgb = COLOR_GREEN_GLOW

    tf_cta = cta_card.text_frame
    tf_cta.word_wrap = True
    tf_cta.margin_top = Inches(0.4)
    tf_cta.margin_left = Inches(0.5)

    p_c1 = tf_cta.paragraphs[0]
    p_c1.text = "🚀 TRẢI NGHIỆM SẢN PHẨM DEMO TRỰC TIẾP:"
    p_c1.font.size = Pt(18)
    p_c1.font.bold = True
    p_c1.font.color.rgb = COLOR_GREEN_GLOW

    p_c2 = tf_cta.add_paragraph()
    p_c2.text = "• Link Demo Server: http://127.0.0.1:5050\n• Web Slide Preview: http://127.0.0.1:5050/slide\n• GitHub Repository: https://github.com/tungdaisy7it/K4-3A-E402-Aura"
    p_c2.font.size = Pt(15)
    p_c2.font.bold = True
    p_c2.font.color.rgb = COLOR_TEXT_MAIN
    p_c2.space_before = Pt(12)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "VLearn_Pitch_Deck.pptx")
    prs.save(output_path)
    print("-> Done generating PPTX slide deck at: " + output_path)

if __name__ == "__main__":
    create_presentation()
