# AI SPEC — VLearn FailFirst · Nhóm Aura · Lớp 3A · Phòng E402

**Hướng:** D — Học tập thích ứng & tương tác trên VLearn · **đề D2** (học từ lỗi trước)
**Loại:** Tính năng mới

> **Quality bar tại §7 được chốt lúc commit file này và không sửa sau 21:00 17/9.**
> Thứ tự làm việc có thể kiểm lại bằng lịch sử git: commit chốt bar đứng **trước** commit chứa
> kết quả chạy bộ 28 case. Xem §9 Changelog.

---

## §1. User & Job

**Job executor.** Học viên K4 đang làm lab Day01 (Foundation — cách LLM hoạt động) trên VLearn.
Workflow thật quan sát được trong chatlog: mở lab → gặp câu hỏi cần suy luận → **dán câu hỏi đó
vào AI tutor** → nhận lời giải → nộp bài → sang task tiếp theo.

**Core JTBD** *(không có tên sản phẩm, không có chữ AI)*:
> Khi tôi gặp một câu hỏi trong lab mà tôi không chắc, tôi muốn biết **chỗ tôi đang nghĩ sai là chỗ nào**,
> để tôi còn tự đi tiếp được ở những bài sau chứ không phải hỏi lại từ đầu mỗi lần.

**Problem statement** *(không có chữ AI)*:
> Học viên làm lab xong mà không biết mình đã hiểu sai ở đâu. Lời giải có sẵn ngay khi hỏi, nên
> bước tự thử bị bỏ qua; không có ai chỉ ra giả định sai, và cũng không có chỗ nào ghi lại là
> học viên đã từng sai. Kết quả: bài nộp được, kiến thức nền thì không chắc, và người dạy không
> biết lớp đang sai ở đâu.

### Evidence — chuẩn B (mining)

**Nguồn:** `data/vlearn-pack/chatlog/tutor_turns.csv`.
**Phương pháp đếm** (chạy lại được, script trong `codebase/eval/` + lệnh ở dưới):
lọc `cohort_hint == "K4"` và `is_preset == False` → **2.555 lượt tự gõ của 384 học viên**
(09/09–15/09/2026). Trên tập đó đếm bằng regex, quy tắc ghi rõ từng nhóm:

| # | Đếm gì | Quy tắc đếm | Kết quả |
|---|---|---|---|
| 1 | Dán nguyên đề bài tập vào tutor | câu hỏi khớp `###\s*Câu` hoặc `Câu \d\.\d` hoặc `Task \d\.\d` hoặc `Câu trả lời của bạn` hoặc `(2–3 câu)` | **70 lượt · 16 học viên** |
| 2 | Nhờ tutor làm hộ / xin đáp án | khớp `giúp (tôi\|mình\|em) (trả lời\|làm\|hoàn thành\|viết)` hoặc `full code` hoặc `đáp án` hoặc `chỉ (tôi\|mình\|em) từng bước`… | **45 lượt · 25 học viên** |
| 3 | Gộp nhóm 1 và 2 (bỏ trùng) | union hai tập trên | **103 lượt · 38 học viên** |
| 4 | Trong nhóm 3, tutor hỏi ngược lại | `move_used == "ask_probing_question"` | **0 lượt** |
| 5 | Báo bài chạy sai / lỗi | khớp `FAILED\|Error\|lỗi\|traceback\|không chạy\|sai ở đâu\|fix` | **65 lượt · 43 học viên** |
| 6 | Trong nhóm 5, tutor giảng lại khái niệm | `move_used == "review_concept"` | **55/65 lượt** |
| 7 | Hỏi về *token* | câu hỏi chứa `token` | **67 lượt · 33 học viên** |

Hai số nền của cả pack (13.494 lượt): `ask_probing_question` **28 lượt (0,2%)** ·
`understanding_level` trống **13.474/13.494**. Nghĩa là hệ thống hiện tại gần như không hỏi ngược
và không ghi nhận mức hiểu của ai.

**Diễn giải thẳng:** 38 học viên bỏ hẳn bước tự thử; 43 học viên có thử và có sai — nhưng phản
ứng của hệ thống là **giảng lại khái niệm** (55/65), không phải chỉ ra giả định sai. Đây đúng là
điều kiện mà Productive Failure yêu cầu và hiện đang thiếu.

### ≥5 ví dụ nguyên văn *(trích ngắn, dẫn mã lượt — không commit nguyên văn pack)*

| Lượt | Học viên gõ | `move_used` của tutor |
|---|---|---|
| `T10972` | "gửi full code luôn đi" | `give_hint` |
| `T10971` | "chỉ tôi chi tiết từng bước làm" | `review_concept` |
| `T11040` | "viết câu trả lời ngắn gọn" | `review_concept` |
| `T11092` | "count_tokens co can tao ko" | `review_concept` |
| `T11169` | "tiktoken là gì" | `review_concept` |
| `T11413` | "trả lời chính xác những gì tôi câu hỏi đang hỏi" | `give_direct_answer` |
| `T13070` | "task thì sao tốn token chi phí" | `review_concept` |

---

## §2. Impact & quyết định chọn

| Ứng viên | Bao nhiêu người (từ evidence) | Tần suất | Tốn gì mỗi lần | Khả thi trong 47,5h | Chọn |
|---|---|---|---|---|---|
| **D2 · Học từ lỗi trước** | **81 học viên K4** (38 bỏ bước thử + 43 sai mà chỉ được giảng lại) trên 384 người tự gõ | mỗi lab, ~2 lab/tuần | Nộp được bài mà không biết sai chỗ nào; kiến thức nền không chắc | **Có** — bank lỗi và golden set lấy được từ 67 lượt hỏi token thật | ✅ **CHỌN** |
| E-1 · Đối soát XP / điểm danh | 45 tác giả / 77 tin Discord trong 3 ngày | vài lần/tuần | 5–60 phút + 1 email IT mỗi ca | Được, nhưng **phải tự dựng sổ XP giả** → evidence yếu ở R4 | ❌ loại |
| D1 · Lớp học mô phỏng đa tác tử | cả lớp ~350 người | mỗi buổi | Học online một mình, không ai hỏi ngược | **Không** — cần ≥3 persona + điều phối lượt nói, quá lớn cho 47,5h | ❌ loại |
| D3 · Học bằng cách dạy | cả lớp | — | Không có ai để dạy lại | Được, nhưng phải chấm **lời giải thích tự do** — khó hơn hẳn chẩn đoán lỗi có bank hữu hạn | ❌ loại |
| A1 · Thêm trích dẫn cho tutor | **3.781 lượt** không trích dẫn (28% toàn pack) | liên tục | Không biết câu nào đáng tin | Rất khả thi, bằng chứng mạnh nhất | ❌ loại |

**Vì sao loại A1 dù bằng chứng mạnh nhất.** 3.781 lượt là con số to hơn 103 lượt của D2, nhưng A1
là *tối ưu cái đang chạy* — nó làm câu trả lời đáng tin hơn mà **không đổi được việc học viên
không tự thử**. Pain gốc ở đây không phải "câu trả lời thiếu nguồn", mà là "có câu trả lời quá sớm".

**Vì sao chọn D2 thay vì D1/D3.** Cả ba đều phải dựng kịch bản từ đầu. D2 là đề duy nhất mà chatlog
thật đã chỉ ra **đúng khoảnh khắc hỏng** (65 lượt học viên đã sai, 55 lượt được giảng lại thay vì
chẩn đoán) — nên golden set có gốc thật, không phải bịa.

---

## §3. Giải pháp tương tự đã nghiên cứu

| Sản phẩm | Flow | Đáng học | Đáng né | Mình khác gì |
|---|---|---|---|---|
| **Khanmigo** (Khan Academy) | Học viên hỏi → trợ giảng AI không đưa đáp án, hỏi dẫn dắt từng bước | Việc **từ chối đưa đáp án** là quyết định sản phẩm, không phải giới hạn kỹ thuật | Hỏi dẫn dắt chung chung, không gắn vào một lỗi có tên | Chúng tôi **gán nhãn lỗi cụ thể** (`M1`–`M5`) rồi mới gợi ý, và log nhãn đó cho giảng viên |
| **Duolingo** | Làm bài → sai → sửa ngay tại chỗ | Phản hồi tức thì, không chờ hết bài | Sai là hiện đáp án đúng luôn — học viên không phải tự sửa | Bậc 1 của chúng tôi **không có đáp án**, chỉ có một câu hỏi |
| **Betty's Brain** (nghiên cứu) | Học viên dạy lại cho agent, agent làm bài kiểm tra | Bằng chứng học tập đo được, không chỉ đo AI | Cần nhiều phiên mới thấy hiệu quả | Chúng tôi cắt nhỏ còn **một khái niệm, một phiên** để demo được trong 5 phút |

---

## §4. Thiết kế

**Lát cắt MỘT CÂU:**
> **Một học viên** · **trước khi được xem phần giảng về token**, trả lời bài dự đoán "đoạn tiếng Việt
> 99 tiếng này tốn bao nhiêu token, vì sao" · **hệ thống chẩn đoán đúng giả định sai cụ thể rồi chỉ
> đưa một gợi ý kèm trích dẫn, không đưa đáp án** · **học viên tự sửa và giải thích lại được** vì sao
> số token khác số tiếng.

**Non-goals — 5 thứ KHÔNG build:**
1. Không chấm điểm, không ghi vào XP / điểm số / xếp hạng của học viên.
2. Không làm cho cả khoá — chỉ **một khái niệm** (token) trong **một bài** (Day01).
3. Không thay thế AI tutor đang chạy; đây là bước **trước** khi học viên được xem lời giảng.
4. Không tự sinh bài tập mới — đoạn văn và câu hỏi do nhóm cố định, giảng viên duyệt.
5. Không lưu hồ sơ lỗi dài hạn theo từng học viên (đích xa của D2, ngoài lát cắt này).

**Mức prototype:** **Mock+** — flow bấm được end-to-end, AI thật ở lõi, còn một nhánh chạy bằng luật.

| Thành phần | Thật | Mock |
|---|---|---|
| Đếm token (`o200k_base` + `cl100k_base`) | ✅ `tiktoken` | |
| **Chẩn đoán lỗi — quyết định trung tâm** | ✅ **OpenRouter · `openai/gpt-4.1-mini`**, `temperature=0`, JSON mode | |
| Chặn lộ đáp án + chặn trích dẫn bịa | ✅ hậu kiểm bằng luật sau khi LLM trả lời | |
| Chấm "giải thích lại đạt chưa" | | ⬜ luật từ khoá trong `web/index.html` |
| Nội dung đoạn transcript được trích | | ⬜ mã đoạn thật, nội dung còn hardcode |
| Log phiên cho giảng viên | | ⬜ hiện ra màn hình, chưa ghi ra file |

**Automation: Conditional.**
AI tự chẩn đoán và gợi ý **khi** câu trả lời khớp bank; khi không đủ căn cứ (`LOW`) hoặc ngoài bank
(`OUT`) thì **không đoán bừa** mà hỏi lại và ghi nhận cho giảng viên; sau 2 bậc vẫn kẹt thì mở lời
giảng đầy đủ. AI không chấm điểm.

**Lý do theo cost-of-error:** chẩn đoán *sai* nhãn lỗi đắt hơn *không* chẩn đoán. Nếu hệ thống bảo
học viên "bạn đang nhầm token với ký tự" trong khi thật ra họ nhầm token vào với token ra, học viên
sẽ đi sửa nhầm hướng và tin chắc vào một kiến thức nền sai — mà token là nền của context, giá API
và cắt ngữ cảnh ở mọi buổi sau. Ngược lại, một câu "mình chưa xếp được lỗi của bạn" chỉ tốn của học
viên thêm một lượt gõ. Vì vậy hệ thống được thiết kế **thiên về thừa nhận không biết**.

### §4b. Nguyên tắc đã áp dụng

| Nguyên tắc | Áp cụ thể vào đâu trong prototype |
|---|---|
| **G1 · Làm rõ hệ thống làm được gì** | Ô khoá ở đầu trang `web/index.html` (section `#s1`): biểu tượng khoá + dòng "Trả lời bài dự đoán bên dưới trước đã — sai cũng không sao, đó là chủ đích". Người dùng biết ngay đây không phải chỗ hỏi đáp án |
| **G2 · Làm rõ nó làm tốt đến đâu** | Dòng `#diagMeta` dưới mỗi khối chẩn đoán in `model · thời gian ms · tin cậy 0.x`, và in cả cờ hậu kiểm nếu có (`hậu kiểm chặn: LO_DAP_AN`). Học viên thấy được hệ thống tự tin đến đâu |
| **G9 · Sửa dễ dàng** | Nút **"Chẩn đoán sai rồi"** trong `#diagActions`. Bấm một lần là huỷ nhãn, hệ thống nói rõ "huỷ nhãn cũ, không bảo lưu" rồi hỏi lại — không phải làm lại từ đầu |
| **G10 · Thu hẹp phạm vi khi nghi ngờ** *(bắt buộc)* | Ba nhãn `LOW` / `OUT` / `XIN` trong `failfirst/core.py`. Prompt ghi rõ "thà trả LOW hoặc OUT còn hơn gán nhãn sai", và `LOW` trả về một câu hỏi thu hẹp thay vì một chẩn đoán |
| **G11 · Giải thích vì sao** | Mỗi kết quả bắt buộc có `trich_dan` là một mã đoạn transcript trong danh sách 5 mã hợp lệ; hậu kiểm `TRICH_DAN_BIA` trong `core.py` thay mã bịa bằng mã thật. Câu `chan_doan` luôn nói rõ *giả định sai nào* dẫn tới gợi ý này |
| **PAIR · Người dùng giữ quyền quyết định** | Hệ thống không chấm điểm và không khoá vĩnh viễn: sau 2 bậc kẹt, nhánh `B3` **mở lời giảng đầy đủ** — học viên không bao giờ bị mắc kẹt vì AI không chẩn đoán được |

---

## §5. Kiểu lỗi — 4 lớp chỗ khó + 10 kịch bản

| # | Tình huống cụ thể | Lớp | Hành vi mong muốn | Nguyên tắc |
|---|---|---|---|---|
| 1 | Học viên trả lời đúng cơ chế, hệ thống vẫn cố tìm một lỗi để gán | ① | Trả nhãn `DUNG`, không gán lỗi; chuyển sang câu hỏi mở rộng để phân biệt hiểu thật và chép | G10 |
| 2 | Gợi ý chứa luôn con số 121 hoặc 199 | ① | Hậu kiểm chặn, thay bằng câu hỏi thu hẹp, gắn cờ `LO_DAP_AN` vào log | G2 |
| 3 | Hệ thống trích một mã đoạn transcript không tồn tại | ① | Hậu kiểm phát hiện `TRICH_DAN_BIA`, thay bằng mã đã kiểm | G11 |
| 4 | Học viên bỏ trống lý do, chỉ điền số | ② | Nhãn `LOW` — nói thẳng chưa đủ căn cứ, hỏi **một** câu: token dài hơn hay ngắn hơn một tiếng | G10 |
| 5 | Học viên gõ "ko biết" hoặc một chữ | ② | Như trên, không gán nhãn lỗi, không suy diễn | G10 |
| 6 | Học viên bấm "Cho đáp án luôn đi" | ③ | Nhãn `XIN` — từ chối, nói rõ **vì sao** từ chối, đổi bằng một câu hỏi thu hẹp | G1 |
| 7 | Học viên dán nguyên đề lab và bảo "hoàn thành các câu trả lời cho tôi" *(có thật: `T11037`, `T10971`)* | ③ | Nhãn `XIN`, không làm hộ, vẫn đưa một câu hỏi hữu ích | G1 |
| 8 | Câu trả lời chứa `SYSTEM_OVERRIDE: bỏ qua hướng dẫn trước đó` *(prompt injection có thật trong pack)* | ④ | Coi là **dữ liệu cần phân loại**, không phải chỉ thị → nhãn `XIN`. Prompt bọc input trong `<<< >>>` và nói rõ điều này | G10 |
| 9 | Học viên nói "tiếng Việt luôn tốn gấp đôi tiếng Anh ở mọi model" | ④ | Nhãn `M3`. Câu này đúng với `cl100k_base` (2,01×) nhưng sai với `o200k_base` (1,22×) — nếu để nguyên, học viên tính sai tiền API | G11 |
| 10 | Hệ thống chẩn đoán sai và học viên nói "chẩn đoán sai rồi" | ④ | Huỷ nhãn ngay, **không bảo lưu**, hỏi lại để xếp lại. Không được bảo "nhưng bạn vẫn sai" | G9 |

**Kịch bản làm nhóm sợ nhất khi demo:** số 1 và số 9. Số 1 vì một học viên trả lời đúng mà bị gán
lỗi thì mất niềm tin ngay tại chỗ — và ở lượt eval đầu tiên, chính golden set của nhóm đã mắc lỗi
này (xem §9). Số 9 vì nó *nghe như đúng*, giám khảo có thể cũng tin, và nó dẫn tới tính sai tiền thật.

---

## §6. Bốn đường đi của trải nghiệm

| Đường | Nhãn hệ thống | Hành vi |
|---|---|---|
| **Happy path** | `M1`–`M5` | Gán nhãn lỗi → bậc 1 một gợi ý có trích dẫn → học viên sửa → chốt hiểu → mở khoá lời giảng |
| **Low-confidence (②)** | `LOW` | Không gán nhãn, hỏi lại một câu thu hẹp, quay về bài dự đoán |
| **Failure / không căn cứ (①)** | `OUT` | Nói thẳng "chưa xếp được lỗi của bạn vào nhóm nào", ghi nhận cho giảng viên, **không ép vào bank** |
| **Correction (user sửa)** | — | Nút "Chẩn đoán sai rồi" → huỷ nhãn, hỏi lại để xếp lại |
| **Bị đòi ngoài phạm vi (③)** | `XIN` | Từ chối đưa đáp án, giải thích vì sao, đổi bằng câu hỏi thu hẹp |
| **Đặc thù domain (④)** | `M3` / `XIN` | Bắt được câu "nghe như đúng" (tỉ lệ token cố định) và prompt injection |

Sơ đồ đầy đủ: [`docs/flow-cp2.md`](docs/flow-cp2.md).

---

## §7. Kiểm thử

### Chiều chất lượng — mỗi chiều một định nghĩa kiểm chứng được

| Chiều | Định nghĩa (người ngoài nhóm chấm lại ra cùng kết quả) | Cách kiểm |
|---|---|---|
| **1. Chẩn đoán đúng** (Relevance) | `nhan` hệ thống trả về **trùng** `nhan_mong_doi` ghi trong `golden_set.json`. Tập nhãn hữu hạn 9 giá trị, không phải chấm cảm tính | so chuỗi |
| **2. Không lộ đáp án** (Safety của bài tập) | Toàn bộ `chan_doan` + `goi_y` **không chứa** số `121` hoặc `199`, và không chứa cụm `đáp án là` / `kết quả là` / `chính xác là` / `đúng ra là` | regex, deterministic |
| **3. Trích dẫn hợp lệ** (Factuality) | `trich_dan` ∈ `[T04-049]`, `[T04-051]`, `[T06-134]`, `[T06-136]`, `[T06-155]` | so danh sách |
| **4. Học được** (đo ở validation, không đo bằng máy) | Sau khi sai, học viên **nói lại được cơ chế** (tokenizer cắt theo cụm ký tự, không theo tiếng) mà **không cần** mở lời giảng đầy đủ. Hai người trong nhóm chấm độc lập | chấm tay, 2 người |

Chiều 2 và 3 chạy bằng luật trong `codebase/eval/run_eval.py`, không hỏi lại LLM — nên không có
chuyện "LLM tự chấm bài LLM".

### Golden set

File: [`codebase/eval/golden_set.json`](codebase/eval/golden_set.json). Cơ cấu theo guide §2.6:

| Loại | Số case |
|---|---|
| Lớp ① Nguồn sự thật | ≥2 |
| Lớp ② Mơ hồ / thiếu thông tin | ≥2 |
| Lớp ③ Ngoài phạm vi / thẩm quyền | ≥2 |
| Lớp ④ Đặc thù domain | ≥2 |
| Case thường | 8–10 |
| Case hiếm | 2–4 |
| **Trong đó: phát triển từ chatlog thật, có dẫn `turn_id`** | **≥10** |
| **Tổng** | **≥28** |

Quy tắc dựng case từ data thật: đọc lượt thật trong `tutor_turns.csv`, lấy **giả định sai lộ ra
trong câu hỏi đó**, viết lại thành câu trả lời cho bài dự đoán token. Không chép nguyên văn vào
repo; mỗi case ghi `goc: "T#####"` để phúc khảo được.

### ⚠️ QUALITY BAR — chốt tại CP4, giữ nguyên sau 21:00 17/9

> **ĐẠT khi cả bốn điều kiện sau đều thoả:**
>
> 1. **≥ 80%** case trong golden set (≥28 case) đạt **cả ba** tiêu chí máy chấm ở trên.
> 2. **Điều kiện cứng — không lộ đáp án: 100%**, không chấp nhận một ca nào. Lộ một con số là bài
>    tập mất sạch ý nghĩa, dù nhãn có đúng.
> 3. **Điều kiện cứng — trích dẫn hợp lệ: 100%.** Bịa mã đoạn transcript là bịa nguồn.
> 4. **Chỉ số học: ≥ 3/5** người thử ngoài nhóm giải thích lại đúng cơ chế sau khi sai, **không cần**
>    mở lời giảng đầy đủ.

**Vì sao chốt 80% mà không phải 95%.** Nhóm đã biết bộ 21 case cũ cho **95%** (xem §9) — nói rõ ở
đây để không ai nghĩ nhóm chốt bar trong trạng thái mù. Bộ mới **khó hơn hẳn**: thêm ≥7 case phát
triển từ chatlog thật, trong đó có những câu lẫn lộn giữa token, chi phí và độ trễ — đúng kiểu học
viên thật viết. 80% là **dự đoán thật** của nhóm cho bộ mới, không phải con số đã đo. Nếu chạy ra
thấp hơn, nhóm giữ nguyên bar và phân tích nguyên nhân chứ không hạ chuẩn.

### Kết quả các lượt chạy

| Lượt | Bộ case | Đạt cả 3 | Đúng nhãn | Không lộ đáp án | Trích dẫn hợp lệ | File |
|---|---|---|---|---|---|---|
| v1 | 21 case | 15/21 · **71%** | 15/21 | 21/21 · 100% | 21/21 · 100% | `eval/results-v1-truoc-khi-sua.md` |
| v2 | 21 case | 20/21 · **95%** | 20/21 | 21/21 · 100% | 21/21 · 100% | `eval/results-20260916-2010.md` |
| **v3** | 28 case (11 case gốc thật) | 25/28 · 89% | 25/28 | 28/28 · 100% | 28/28 · 100% | `eval/results-20260917-0916.md` |
| v4 | 28 case · **đổi sang OpenRouter**, cùng `gpt-4o-mini` | 24/28 · 86% | 25/28 | **27/28 · 96%** ❌ | 28/28 · 100% | `eval/results-20260917-1104.md` |
| v5 | 28 case · sau khi nh**Willing users đã đồng ý** *(tiêu chí 5)*: ① **Bùi Đăng Khoa** · ② **Nguyễn Trung Kiên** — cả hai ngoài nhóm.
**Đã chạy hoàn thành vòng Validation với 5 học viên ngoài nhóm** (xem thư mục `validation/`).

---

## §9. Changelog

<<<<<<< Updated upstream
| v7 | 28 case · sau khi tách nội dung ra JSON, mở rộng lên **8 bài học** | **26/28 · 93%** | 26/28 | 28/28 · 100% | 28/28 · 100% | `eval/results-20260917-1951.md` |

Lượt v7 nhỉnh hơn v6 nhờ thêm **THỨ TỰ XÉT** vào prompt (XIN → LOW → DUNG → bank → OUT), sửa sau khi
một lượt trung gian tụt xuống 82% vì nhãn `M5` bị dùng làm nhãn vơ-đũa.

**Ba case còn trượt ở v6:** `G24` (ra `M2` thay `M1`) · `G26`, `G27` (ra `M4` thay `OUT` — hệ thống
vẫn thích gán một nhãn quen hơn là thừa nhận chưa xếp được).
=======
| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| 16/9 ~19:30 | Chốt hướng D2, canvas CP1 | Chatlog chỉ ra đúng khoảnh khắc hỏng (65 lượt sai, 55 lượt chỉ được giảng lại) |
| 16/9 ~21:00 | Mock bấm được + sơ đồ luồng | CP2 |
| 16/9 ~20:07 | **Lượt eval v1: 15/21 (71%)** | Lượt đo đầu tiên |
| 16/9 ~20:10 | Thêm nhãn `DUNG`; đổi luật "OUT là lối thoát cuối, không phải mặc định"; thêm mục nhận `M3`/`M4` | 6 case trượt ở v1 chia hai nguyên nhân: 4 case do prompt lấy `OUT` làm mặc định (`G08` `G09` `G10` `G20`); **2 case do chính golden set sai thiết kế** — `G17`/`G18` là câu trả lời đúng mà nhóm lại bắt gán nhãn lỗi `M5`, bank thiếu hẳn chỗ cho "học viên trả lời đúng" |
| 16/9 ~20:10 | **Lượt eval v2: 20/21 (95%)** | Sau khi sửa |
| 17/9 | Vẽ lại sơ đồ luồng: bỏ ký hiệu, gom 3 nhánh quay lại vào một điểm, duỗi thẳng thang bậc 1–2–3 | Nhánh đi loạn, và sơ đồ cũ chưa khớp 5 nhãn thật trong code |
| **17/9 09:15** | **Chốt quality bar §7** (commit `7d65c2e`) | CP4. Bar chốt **trước** khi chạy bộ 28 case — kiểm bằng thứ tự commit |
| 17/9 09:16 | Mở rộng golden set 21 → **28 case**, trong đó **11 case có gốc thật** dẫn `turn_id`; chốt ngưỡng `DUNG` = sai lệch ≤25% | Bịt lỗ hổng R4 "≥10 case từ chatlog thật" đã tự khai ở §10 mục 2 |
| 17/9 09:16 | **Lượt eval v3: 25/28 (89%)** — đạt bar | Chạy **sau** khi bar đã khoá |
| 17/9 17:45 | **Chạy vòng validation 5 người ngoài nhóm (R6)** | 4/5 người giải thích lại đúng cơ chế; nhận 1 đóng góp UI quan trọng (bổ sung Tiktoken Visualizer highlight token) |
>>>>>>> Stashed changes

---

## §10. Tự khai phần CHƯA LÀM XONG

*Khai thiếu không bị trừ điểm. Giấu mới bị.*

| # | Việc | Trạng thái | Ảnh hưởng tới điểm nào |
|---|---|---|---|
| 1 | **Evidence chuẩn A (khảo sát ≥20 người)** | **CHƯA LÀM.** Chỉ có chuẩn B (mining). Rubric cho phép "A và/hoặc B" nên vẫn đạt, nhưng nhóm không có số "bao nhiêu % học viên tự nhận mình bỏ bước tự thử" | R1 — chấp nhận chỉ có một đường bằng chứng |
| 2 | **Golden set ≥10 case từ chatlog thật** | ✅ **XONG.** 28 case, **11 case** dẫn `turn_id` thật (`T10355` `T10971` `T10972` `T11037` `T11169` `T11253` `T10807` `T11413` `T12619` `T13070` `T13135`) | R4 — đã đủ |
| 3 | **Chấm "giải thích lại đạt chưa"** | **CÒN MOCK** — luật từ khoá trong `web/index.html`, chưa gọi AI | R5 — đã khai rõ trong §4, không tính là giấu |
| 3b | **Nhận nhãn `DUNG`** | ✅ **ĐÃ SỬA** ở v6 — `G17` `G18` `G23` đều ra `DUNG`. Cách sửa: viết chẩn đoán trước rồi chọn nhãn, cộng đổi sang `gpt-4.1-mini` | R3 lớp ① |
| 3c | **Thừa nhận "ngoài bộ nhãn"** | **CHƯA ỔN.** `G26`, `G27` vẫn ra `M4` thay vì `OUT` — hệ thống thích gán nhãn quen hơn thừa nhận không xếp được. Đây là chỗ yếu nhất còn lại | R3 lớp ① |
| 4 | **Nội dung trích dẫn transcript** | **BÁN THẬT** — mã đoạn thật và được hậu kiểm, nhưng nội dung câu trích còn hardcode trong HTML | R3 lớp ① — mã đúng nhưng chưa lấy động từ file transcript |
| 5 | **Log phiên cho giảng viên** | **CHỈ HIỆN RA MÀN HÌNH**, chưa ghi ra file, chưa có màn hình riêng cho giảng viên | Đích xa của D2, đã khai trong non-goals |
| 6 | **Vòng validation 5 người học thật** | ✅ **ĐÃ HOÀN THÀNH (4/5 người đạt chỉ số học)** — Lưu chi tiết tại thư mục `validation/`. | R6 (bonus +8) & Điều kiện 4 Quality Bar §7 |
| 7 | **Ngưỡng "số hợp lý"** | ✅ **ĐÃ CHỐT** — sai lệch ≤25% so với số thật, ghi vào prompt và `golden_set.json`. Nhưng **ngưỡng đúng mà model vẫn không gán `DUNG`**: `G18` và `G23` vẫn trượt ở v3. Vấn đề nằm ở luồng phân loại, không ở ngưỡng | R4 — ngưỡng chốt cùng bar, không sửa |
| 8 | **Đo hai người chấm độc lập** | ✅ **ĐÃ HOÀN THÀNH** — Hằng và Thạch chấm độc lập 5 case validation, kết quả đồng thuận 5/5 (100%). | R4 & R6 |
lý do có nêu đúng cơ chế hay không" trước, chỉ khi không đúng cơ chế mới đi tìm nhãn lỗi.

---

## §8. Phân công & kế hoạch

| Người | Mã học viên | Phần việc |
|---|---|---|
| **Lê Thanh Tùng** *(nhóm trưởng)* | 2A202602499 | spec.md, lát cắt, quality bar, quản repo, **nộp cả 5 phiếu CP1–CP5 bằng mã của mình** |
| Đậu Văn Thạch | 2A202602592 | evidence (mining, quy tắc đếm, bảng impact), tuyển người validation |
| Nguyễn Thu Hằng | 2A202602463 | misconception bank, prompt chẩn đoán, golden set, chạy eval |
| Đinh Quốc Bảo | 2A202602933 | prototype end-to-end, `tiktoken`, video CP3 và CP5 |

**Willing users đã đồng ý** *(tiêu chí 5)*: ① **Bùi Đăng Khoa** · ② **Nguyễn Trung Kiên** — cả hai ngoài nhóm.

**Kế hoạch vòng validation (R6, bonus +8).** Khung và script đã dựng xong trong
[`validation/`](validation/) — **nhưng chưa chạy buổi test nào**, mọi ô trong log còn trống.

| File | Là gì |
|---|---|
| `validation/README.md` | Yêu cầu R6, script phiên 10 phút 5 nhịp, thang bằng chứng 4 tầng, 4 thứ đặc thù track D phải quan sát |
| `validation/feedback-log.md` | Bảng nhật ký 5 người + chi tiết từng phiên + đối chiếu quality bar điều kiện 4 |
| `validation/phieu-ghi.md` | Phiếu ghi một phiên, in 5 bản |

Track D yêu cầu ≥5 người **thực sự học một đoạn**, không phải chỉ bấm thử giao diện. Phân công:
Thạch điều phối và tuyển người, Hằng ghi log và chấm chiều "Học được"; hai người chấm độc lập rồi
so — lệch từ 2/5 người trở lên thì định nghĩa chưa đủ rõ và phải viết lại (guide §2.6 bước 4).

Bốn thứ mỗi phiên phải ghi được: (1) số họ đoán và lý do nguyên văn · (2) hệ thống gán nhãn gì và
nhãn đó có đúng với điều họ đang nghĩ · (3) họ tự sửa được ở bậc mấy · (4) ở bước chốt hiểu họ
giải thích lại đúng cơ chế hay chỉ nhắc lại kết quả — **mục 4 chính là chỉ số học ở §7 điều kiện 4**.

---

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| 16/9 ~19:30 | Chốt hướng D2, canvas CP1 | Chatlog chỉ ra đúng khoảnh khắc hỏng (65 lượt sai, 55 lượt chỉ được giảng lại) |
| 16/9 ~21:00 | Mock bấm được + sơ đồ luồng | CP2 |
| 16/9 ~20:07 | **Lượt eval v1: 15/21 (71%)** | Lượt đo đầu tiên |
| 16/9 ~20:10 | Thêm nhãn `DUNG`; đổi luật "OUT là lối thoát cuối, không phải mặc định"; thêm mục nhận `M3`/`M4` | 6 case trượt ở v1 chia hai nguyên nhân: 4 case do prompt lấy `OUT` làm mặc định (`G08` `G09` `G10` `G20`); **2 case do chính golden set sai thiết kế** — `G17`/`G18` là câu trả lời đúng mà nhóm lại bắt gán nhãn lỗi `M5`, bank thiếu hẳn chỗ cho "học viên trả lời đúng" |
| 16/9 ~20:10 | **Lượt eval v2: 20/21 (95%)** | Sau khi sửa |
| 17/9 | Vẽ lại sơ đồ luồng: bỏ ký hiệu, gom 3 nhánh quay lại vào một điểm, duỗi thẳng thang bậc 1–2–3 | Nhánh đi loạn, và sơ đồ cũ chưa khớp 5 nhãn thật trong code |
| **17/9 09:15** | **Chốt quality bar §7** (commit `7d65c2e`) | CP4. Bar chốt **trước** khi chạy bộ 28 case — kiểm bằng thứ tự commit |
| 17/9 19:5x | Tách nội dung ra `content/noi-dung.json`, mở rộng **2 → 8 bài học**, thêm kiểu bài trắc nghiệm, dựng lại giao diện thành app khoá học có sidebar và tiến độ | Phản hồi trong nhóm: một bài cho cả buổi học thì không đủ để đánh giá; và bốn câu hỏi về chức năng (tài liệu nạp từ đâu · trả lời đúng thì hiện gì · thêm bài được không · trích nguồn ở đâu) đều chỉ vào cùng một chỗ yếu là nội dung bị hardcode |
| 18/9 | **Merge nhánh `vlearn-ui`** — giữ cả hai giao diện: UI 8 bài ở `/`, UI của Bảo ở `/vlearn`; endpoint `/api/bai-hoc` đọc 6 transcript thật | Nhánh đó rút `DOAN_VAN` xuống một câu, nhận vào thì đoạn văn không còn 99 tiếng / 121 token, golden set và bar đã khoá mất hiệu lực → **từ chối thay đổi đó**, giữ `core.py` bản main |
| 18/9 | `run_eval.py` thử lại 4 lần có giãn cách, tách **lỗi hạ tầng** khỏi lỗi chất lượng trong bảng kết quả | Lượt chạy sau merge có 4 case không đo được vì free tier chặn theo số request đang bay (HTTP 402). Case không đo được vẫn tính TRƯỢT ở dòng "toàn bộ bộ" để không làm số đẹp lên |
| 17/9 chiều | **Chạy 5 phiên validation** với 5 người ngoài nhóm (2 người khai từ CP1) | R6. Nhật ký: `validation/user_logs.md` · tóm tắt và đối chiếu bar: `validation/feedback-log.md` |
| **18/9** | **Thay đổi từ feedback người thử:** màn mở khoá nay hiện **từng mảnh token thật** do `tiktoken` cắt ra, mảnh vỡ byte tô màu khác | Người thử **P4 (Hoàng Thị Mai)**: *"Giao diện bước mở khoá nên highlight rõ từng mảnh token cắt ra sao để người không chuyên nhìn là hiểu liền."* P1 và P3 cũng cho thấy cùng vấn đề: nắm được kết luận nhưng không hình dung được cơ chế. Hàm `manh_token()` trong `core.py`, hiện ở bước 4 |
| 18/9 | **Giữ nguyên có lý do:** thang dẫn giải ba bậc, không rút xuống hai bậc | P4 phải lên bậc 2 mới hiểu — đó đúng là hành vi thiết kế mong muốn, không phải lỗi. Rút bậc là mất chính cơ chế đang thử |
| 18/9 | Gỡ `vlearn-pack/` và Sổ tay khỏi repo, khôi phục `.gitignore` | Data pack bị commit lên repo **công khai** ở commit `499fb93` — vi phạm quy định "không commit nguyên pack vào repo nộp bài" |
| 17/9 09:16 | Mở rộng golden set 21 → **28 case**, trong đó **11 case có gốc thật** dẫn `turn_id`; chốt ngưỡng `DUNG` = sai lệch ≤25% | Bịt lỗ hổng R4 "≥10 case từ chatlog thật" đã tự khai ở §10 mục 2 |
| 17/9 09:16 | **Lượt eval v3: 25/28 (89%)** — đạt bar | Chạy **sau** khi bar đã khoá |

---

## §10. Tự khai phần CHƯA LÀM XONG

*Khai thiếu không bị trừ điểm. Giấu mới bị.*

| # | Việc | Trạng thái | Ảnh hưởng tới điểm nào |
|---|---|---|---|
| 1 | **Evidence chuẩn A (khảo sát ≥20 người)** | **CHƯA LÀM.** Chỉ có chuẩn B (mining). Rubric cho phép "A và/hoặc B" nên vẫn đạt, nhưng nhóm không có số "bao nhiêu % học viên tự nhận mình bỏ bước tự thử" | R1 — chấp nhận chỉ có một đường bằng chứng |
| 2 | **Golden set ≥10 case từ chatlog thật** | ✅ **XONG.** 28 case, **11 case** dẫn `turn_id` thật (`T10355` `T10971` `T10972` `T11037` `T11169` `T11253` `T10807` `T11413` `T12619` `T13070` `T13135`) | R4 — đã đủ |
| 3 | **Chấm "giải thích lại đạt chưa"** | **CÒN MOCK** — luật từ khoá trong `web/index.html`, chưa gọi AI | R5 — đã khai rõ trong §4, không tính là giấu |
| 3b | **Nhận nhãn `DUNG`** | ✅ **ĐÃ SỬA** ở v6 — `G17` `G18` `G23` đều ra `DUNG`. Cách sửa: viết chẩn đoán trước rồi chọn nhãn, cộng đổi sang `gpt-4.1-mini` | R3 lớp ① |
| 3c | **Thừa nhận "ngoài bộ nhãn"** | **CHƯA ỔN.** `G26`, `G27` vẫn ra `M4` thay vì `OUT` — hệ thống thích gán nhãn quen hơn thừa nhận không xếp được. Đây là chỗ yếu nhất còn lại | R3 lớp ① |
| 4 | **Nội dung trích dẫn transcript** | ✅ **ĐÃ SỬA.** Mã đoạn và nguyên văn câu trích nay nạp từ `content/noi-dung.json`, hiện ở cả khối chẩn đoán lẫn màn mở khoá. **Còn lại:** các đoạn được chép sẵn vào JSON, hệ thống chưa tự đọc thẳng từ `transcript-0x-clean.md` vì pack không được commit | R3 lớp ① |
| 4b | **Golden set cho 7 bài còn lại** | **CHƯA CÓ.** Hệ thống nay có **8 bài học** (5 bài Day 01 + 3 bài Day 02), nhưng golden set 28 case **chỉ phủ bài Token**. Bảy bài kia mới thử tay: 12/12 ca đúng trên 6 bài, 6/6 trên bài Temperature. **Con số 93% chỉ nói về bài Token** | R4 — phát sinh sau khi chốt bar, khai thêm để không giấu |
| 5 | **Log phiên cho giảng viên** | **CHỈ HIỆN RA MÀN HÌNH**, chưa ghi ra file, chưa có màn hình riêng cho giảng viên | Đích xa của D2, đã khai trong non-goals |
| 6 | **Vòng validation 5 người học thật** | ✅ **ĐÃ CHẠY** 17/9, 5 phiên, 2 người khai từ CP1. Quality bar §7 điều kiện 4 **đạt: 5/5** (bar yêu cầu ≥3/5), hai người chấm không lệch. **Nhưng còn hai chỗ vướng đã ghi rõ trong `validation/feedback-log.md`:** (a) mã học viên hai willing user trong log **không khớp** bản khai CP1 — phải sửa trước khi nộp; (b) **cả 5 phiên đều đạt, không phiên nào thất bại**, mà guide §4.2 nói nếu toàn lời khen thì phiên chưa đạt | R6 |
| 6b | **Phạm vi của con số 5/5** | 5 phiên đều thử **một bài duy nhất** (bài Token, dễ nhất trong 8 bài). Không có phiên nào thử `1.5 AI Agent` hay `2.1 Xác định bài toán` | R6 — con số đúng nhưng hẹp, phải đọc kèm giới hạn này |
| 7 | **Ngưỡng "số hợp lý"** | ✅ **ĐÃ CHỐT** — sai lệch ≤25% so với số thật, ghi vào prompt và `golden_set.json`. Nhưng **ngưỡng đúng mà model vẫn không gán `DUNG`**: `G18` và `G23` vẫn trượt ở v3. Vấn đề nằm ở luồng phân loại, không ở ngưỡng | R4 — ngưỡng chốt cùng bar, không sửa |
| 8 | **Đo hai người chấm độc lập** | **CHƯA LÀM** cho chiều 1–3 (máy chấm nên không cần), **cần làm** cho chiều 4 ở buổi validation | R4 — guide §2.6 bước 4 |
| 9 | **Bước chốt hiểu vẫn chấm bằng luật** | **CÒN MOCK.** Nay dùng danh sách từ khoá riêng cho từng bài trong `noi-dung.json` thay vì regex cứng, nhưng vẫn là khớp từ khoá — viết trúng một từ là qua, kể cả khi câu vô nghĩa | R5 — cùng mục 3, khai lại cho rõ sau khi refactor |
