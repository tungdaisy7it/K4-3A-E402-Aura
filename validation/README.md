# validation/ — vòng cho người ngoài nhóm dùng thử (R6, bonus +8)

> ⚠️ **TRẠNG THÁI: CHƯA CHẠY BUỔI TEST NÀO.**
> Thư mục này hiện chỉ có **khung và script điều phối**. Mọi ô trong
> [`feedback-log.md`](feedback-log.md) đang trống và **phải được điền bằng lời thật của người thật**.
> Nhóm không điền sẵn quote, không đoán trước phản ứng của người thử — rubric ghi rõ *"số liệu bị
> chỉnh sửa hoặc che giấu sẽ không được tính"*, và bịa quote của người có tên còn nặng hơn mất điểm.

## R6 yêu cầu đúng bốn thứ

| | Yêu cầu | Trạng thái |
|---|---|---|
| 1 | **5 người ngoài nhóm** dùng thử, trong đó **2 người đã khai từ CP1** | ⬜ có 2 người đã đồng ý (Khoa, Kiên), thiếu 3 |
| 2 | **Quote nguyên văn** — chép đúng lời họ nói, kể cả viết sai chính tả, kể cả câu chê | ⬜ |
| 3 | **Bảng nhật ký** — ai thử · giao task gì · kẹt ở đâu · quote · quyết định | ⬜ khung đã có, chưa có dữ liệu |
| 4 | **≥1 thay đổi** ghi vào `spec.md` §9 Changelog (giữ nguyên thì nói rõ vì sao) | ⬜ |

**Người dùng chê vẫn được tính đủ điểm.** Mục đích là xem giải pháp có ăn thua không. Phát hiện
sản phẩm chưa ổn rồi sửa còn dễ ăn điểm hơn, vì có chỗ cụ thể để nói. Nếu **mọi phản hồi đều là
lời khen thì phiên test chưa đạt** — giao task khó hơn hoặc đổi người thử.

## Chuẩn bị (5 phút, làm một lần)

```bash
cd codebase
pip install -r requirements.txt
python app.py            # http://127.0.0.1:5050
```

Kiểm trước khi gọi người vào: thanh trên hiện `OpenRouter · openai/gpt-4.1-mini`, bấm thử một câu
thấy chẩn đoán trả về. **Nếu API đang bị chặn (free tier) thì hoãn buổi test** — để người thử ngồi
chờ lỗi kết nối là mất buổi vô ích.

In sẵn 5 bản [`phieu-ghi.md`](phieu-ghi.md), mỗi người một tờ.

## Một phiên 10 phút — 5 nhịp, đi đúng thứ tự

**Hai người điều phối:** một người nói, một người ghi. Người ghi không nói gì trong nhịp 4.

| Nhịp | Thời lượng | Nói gì |
|---|---|---|
| **1 · Comfort** | ~1' | "Tụi mình đang đánh giá sản phẩm, không đánh giá bạn. Không có câu trả lời đúng sai — cứ nói to suy nghĩ của bạn." |
| **2 · Context** | ~1' | "Kể lần gần nhất bạn làm lab mà gặp một câu không chắc — bạn đã làm gì?" *(hỏi chuyện đã xảy ra, chưa mở sản phẩm)* |
| **3 · Task** | ~1' | Giao theo **kết quả**, không theo nút: *"Bạn hãy dùng cái này để học phần Token trong Day 01."* Người thử tự cầm chuột. |
| **4 · Observe** | ~5' | **Im lặng.** Ghi: hành động đầu tiên, chỗ do dự, chỗ hiểu sai, chỗ phải gợi ý. |
| **5 · Hỏi sau** | ~2' | Bốn câu ở dưới, ghi **nguyên văn**. |

### Nhịp 4 — ba câu cứu hộ duy nhất được dùng

- "Cứ nói to suy nghĩ nhé."
- "Bạn sẽ làm gì tiếp?"
- "Bạn nghĩ nó nên hoạt động thế nào?"

**Cấm:** thuyết minh màn hình · giải thích icon · hỏi "bạn có thích không?" · chữa cháy khi họ kẹt.
Chỗ họ kẹt chính là dữ liệu — cứu là mất dữ liệu.

### Nhịp 5 — bốn câu hỏi sau khi dùng

1. "Điều gì khó hiểu hoặc khó chịu nhất?"
2. "Kết quả này bạn có tin không — vì sao?"
3. "Bạn có dùng thật không — vì sao / vì sao chưa?"
4. "Nếu từ mai không được dùng cái này nữa, bạn thấy: **rất tiếc / hơi tiếc / không sao**?"

## Đọc log theo thang bằng chứng 4 tầng

Xếp mỗi dòng log vào một tầng, tầng càng cao càng đáng tin:

| Tầng | Loại bằng chứng | Trọng lượng |
|---|---|---|
| 1 | **Hành vi quan sát được** — họ bấm gì, kẹt ở đâu, bỏ giữa chừng | **mạnh nhất** |
| 2 | Lời nói **trong lúc** dùng | mạnh |
| 3 | Giải thích khi được hỏi sau | vừa |
| 4 | Dự đoán tương lai — "mình sẽ dùng" | **yếu nhất, chỉ coi là gợi ý** |

Một hành động thật nặng hơn mười câu nói sẽ-dùng.

## Bốn thứ đặc thù track D phải quan sát

Track D bắt buộc người thử **thực sự học một đoạn**, không phải chỉ bấm thử giao diện. Nên ngoài
nhật ký thường, mỗi phiên phải ghi được bốn thứ này:

| # | Ghi gì | Vì sao |
|---|---|---|
| 1 | Họ **đoán số mấy** và **lý do họ viết** | Đây là input thật cho bộ nhãn lỗi — nếu lý do không khớp `M1`–`M5` thì bank của nhóm còn thiếu |
| 2 | Hệ thống gán **nhãn gì**, và nhãn đó **có đúng** với điều họ đang nghĩ không | Đo trực tiếp chiều "chẩn đoán đúng" bằng người, không bằng máy |
| 3 | Họ **có tự sửa được** sau gợi ý bậc 1, hay phải lên bậc 2, bậc 3 | Đo "dẫn giải tối thiểu" |
| 4 | Ở bước chốt hiểu, họ **giải thích lại đúng cơ chế** hay chỉ nhắc lại kết quả | **Đây là chỉ số học** — điều kiện 4 của quality bar `spec.md` §7 |

Hai người trong nhóm chấm độc lập mục 4 rồi so. Lệch từ 2/5 người trở lên thì định nghĩa
"giải thích lại đúng" chưa đủ rõ, phải viết lại — theo guide §2.6 bước 4.

## Sau buổi test — ba việc, làm ngay trong ngày

1. **Điền `feedback-log.md`** — đủ 5 dòng, quote nguyên văn, không sửa chính tả của họ.
2. **Tổng hợp 4 dòng** ở cuối file đó: chủ đề lặp nhiều nhất · 1–2 thay đổi làm trước demo ·
   giữ nguyên có lý do · đưa vào backlog.
3. **Ghi ≥1 dòng vào `spec.md` §9 Changelog.** Mẫu dòng:

   ```
   | 18/9 sau validation | <đổi gì cụ thể> | <người thử nào, quote nào dẫn tới thay đổi này> |
   ```

   Nếu quyết định **không sửa**, vẫn phải ghi một dòng nói rõ vì sao giữ nguyên — R6 cho điểm cả
   hai hướng, miễn là có căn cứ.

## Ghi chú nguồn

Script phiên test theo Product Discovery Group / Stanford CS177 (Jim Morris, CC-BY-SA);
câu Disappointment theo Sean Ellis; thang bằng chứng 4 tầng theo bài giảng Day 18 khoá AI20k.
Tóm lược trong `02-guide.md` §4.2 của repo đề bài.
