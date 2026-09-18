# -*- coding: utf-8 -*-
"""
Chạy trọn bộ golden set qua lời gọi AI thật, xuất bảng kết quả + trace.

    python eval/run_eval.py

Sinh ra:
    eval/results-<timestamp>.md    bảng kết quả, đủ mọi case kể cả case trượt
    eval/trace-<timestamp>.json    log nguyên văn từng lời gọi, để phúc khảo
"""
import io
import json
import os
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

from failfirst.core import TRICH_DAN_HOP_LE, chan_doan, su_that  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def cham(case, out, st):
    """Ba tiêu chí, phải đạt cả ba."""
    dung_nhan = out.get("nhan") == case["nhan_mong_doi"]
    khong_lo = "LO_DAP_AN" not in out.get("canh_bao", [])
    trich_ok = out.get("trich_dan") in TRICH_DAN_HOP_LE and "TRICH_DAN_BIA" not in out.get("canh_bao", [])
    return {
        "dung_nhan": dung_nhan,
        "khong_lo_dap_an": khong_lo,
        "trich_dan_hop_le": trich_ok,
        "dat": dung_nhan and khong_lo and trich_ok,
    }


def main():
    gs = json.load(open(os.path.join(HERE, "golden_set.json"), encoding="utf-8"))
    st = su_that()
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    rows, trace = [], []

    print("Su that bai tap: %d tieng | o200k=%d | cl100k=%d\n"
          % (st["n_tieng"], st["o200k_base"], st["cl100k_base"]))

    for c in gs["cases"]:
        # Nhà cung cấp free tier chặn theo số request đang bay -> thử lại có giãn cách.
        # Lỗi hạ tầng KHÔNG phải lỗi chất lượng, nên tách ra đếm riêng ở phần tổng kết.
        out, loi = None, None
        for lan in range(4):
            try:
                out = chan_doan(c.get("so"), c.get("ly_do", ""))
                loi = None
                break
            except Exception as e:
                loi = str(e)[:200]
                time.sleep(2 + lan * 4)
        if out is None:
            out = {"nhan": "ERROR", "chan_doan": loi, "goi_y": "", "trich_dan": "",
                   "canh_bao": ["LOI_HA_TANG"]}
        k = cham(c, out, st)
        rows.append((c, out, k))
        trace.append({"case": c, "ket_qua": out, "cham": k})
        print("%-4s %-22s mong doi %-4s -> %-4s  %s"
              % (c["id"], c["lop"], c["nhan_mong_doi"], out.get("nhan"),
                 "DAT" if k["dat"] else "TRUOT"))
        time.sleep(1.2)

    n = len(rows)
    n_loi = sum(1 for _, o, _ in rows if o.get("nhan") == "ERROR")
    dat = sum(1 for _, _, k in rows if k["dat"])
    dung_nhan = sum(1 for _, _, k in rows if k["dung_nhan"])
    khong_lo = sum(1 for _, _, k in rows if k["khong_lo_dap_an"])
    trich_ok = sum(1 for _, _, k in rows if k["trich_dan_hop_le"])

    md = []
    md.append("# Kết quả eval — VLearn FailFirst (CP3)\n")
    md.append("Chạy lúc **%s** · model `%s` · lời gọi AI **thật**, `temperature=0`.\n"
              % (datetime.now().strftime("%H:%M %d/%m/%Y"), os.environ.get("OPENAI_MODEL")))
    md.append("Sự thật bài tập tính bằng `tiktoken` chạy thật: đoạn **%d tiếng** → "
              "**%d token** (`o200k_base`) · **%d token** (`cl100k_base`).\n"
              % (st["n_tieng"], st["o200k_base"], st["cl100k_base"]))
    md.append("\n## Số đo\n")
    md.append("| Chiều chất lượng | Đạt | Tỉ lệ |")
    md.append("|---|---|---|")
    n_do = n - n_loi
    md.append("| **Đạt cả 3 tiêu chí — trên TOÀN BỘ bộ** | %d/%d | **%.0f%%** |" % (dat, n, dat / n * 100))
    if n_loi:
        md.append("| ⚠️ Không đo được — gọi API thất bại sau 4 lần thử | %d/%d | %.0f%% |"
                  % (n_loi, n, n_loi / n * 100))
        md.append("| Đạt cả 3 tiêu chí — trên %d case ĐO ĐƯỢC | %d/%d | **%.0f%%** |"
                  % (n_do, dat, n_do, dat / n_do * 100 if n_do else 0))
    md.append("| Chẩn đoán đúng nhãn lỗi | %d/%d | %.0f%% |" % (dung_nhan, n, dung_nhan / n * 100))
    md.append("| Không lộ đáp án | %d/%d | %.0f%% |" % (khong_lo, n, khong_lo / n * 100))
    md.append("| Trích dẫn hợp lệ | %d/%d | %.0f%% |" % (trich_ok, n, trich_ok / n * 100))

    md.append("\n## Từng case\n")
    md.append("| ID | Lớp | Mong đợi | Ra | Nhãn | Không lộ | Trích dẫn | Kết |")
    md.append("|---|---|---|---|:-:|:-:|:-:|:-:|")
    tick = lambda b: "✅" if b else "❌"
    for c, out, k in rows:
        md.append("| %s | %s | `%s` | `%s` | %s | %s | %s | **%s** |"
                  % (c["id"], c["lop"], c["nhan_mong_doi"], out.get("nhan"),
                     tick(k["dung_nhan"]), tick(k["khong_lo_dap_an"]),
                     tick(k["trich_dan_hop_le"]), "ĐẠT" if k["dat"] else "TRƯỢT"))

    truot = [(c, out, k) for c, out, k in rows if not k["dat"]]
    md.append("\n## Case trượt — nguyên văn, không giấu\n")
    if not truot:
        md.append("_Không có case nào trượt._")
    for c, out, k in truot:
        md.append("\n**%s** (`%s`) — mong đợi `%s`, ra `%s`" % (c["id"], c["lop"], c["nhan_mong_doi"], out.get("nhan")))
        md.append("- Học viên trả lời: số `%s` · lý do: \"%s\"" % (c.get("so"), c.get("ly_do")))
        md.append("- Chẩn đoán: %s" % out.get("chan_doan"))
        md.append("- Gợi ý: %s" % out.get("goi_y"))
        if out.get("canh_bao"):
            md.append("- Cảnh báo hậu kiểm: `%s`" % ", ".join(out["canh_bao"]))

    md.append("\n## Ghi chú phương pháp\n")
    md.append("- Một case **ĐẠT** khi thoả cả ba: đúng nhãn · không lộ đáp án · trích dẫn hợp lệ.")
    md.append("- Hậu kiểm lộ đáp án chạy bằng luật (regex số thật + cụm \"đáp án là\"), không hỏi lại LLM.")
    md.append("- `temperature=0` để chạy lại ra kết quả so sánh được.")
    md.append("- Trace nguyên văn từng lời gọi: `eval/trace-%s.json`." % stamp)
    if n_loi:
        md.append("- ⚠️ **%d case không đo được** vì nhà cung cấp chặn theo số request đang bay "
                  "(free tier trả HTTP 402 sau 4 lần thử lại). Đây là lỗi hạ tầng, **không phải "
                  "lỗi chất lượng** — các case đó bị tính là TRƯỢT ở dòng \"toàn bộ bộ\" để "
                  "không làm số đẹp lên, và được tách riêng ở dòng \"case đo được\"." % n_loi)

    p_md = os.path.join(HERE, "results-%s.md" % stamp)
    p_js = os.path.join(HERE, "trace-%s.json" % stamp)
    io.open(p_md, "w", encoding="utf-8").write("\n".join(md) + "\n")
    json.dump(trace, io.open(p_js, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("\n=== %d/%d DAT (%.0f%%) ===" % (dat, n, dat / n * 100))
    print("dung nhan %d/%d | khong lo dap an %d/%d | trich dan %d/%d"
          % (dung_nhan, n, khong_lo, n, trich_ok, n))
    print("->", p_md)


if __name__ == "__main__":
    main()
