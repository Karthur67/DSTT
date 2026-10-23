"""
theo_doi.py - theo dõi tiến độ Project 3 hoàn toàn bằng Python (thay cho file Excel).

Đặt cùng thư mục với ghep_file.py. Dữ liệu lưu trong theo_doi.json (tự tạo lần đầu).
Chỉ cần Python 3; lệnh `excel` cần thêm openpyxl (pip install openpyxl).

LỆNH THƯỜNG DÙNG
  python theo_doi.py                         Xem bảng tổng quan
  python theo_doi.py bat-dau 2026-10-22      Đặt ngày nhận đề (N1)
  python theo_doi.py ten TV2 "Trần Thị B"    Điền họ tên thành viên
  python theo_doi.py xong T5 Q6              Đánh dấu Xong   (T1-T14, Q1-Q6, R1-R9 báo cáo, B1-B29 lộ trình)
  python theo_doi.py dang T13                Đánh dấu Đang làm
  python theo_doi.py chua T13                Trả về Chưa làm
  python theo_doi.py quet                    Tự quét 01_Parts/: task nào có code đúng biến -> Xong
  python theo_doi.py ds [TV3]                Danh sách việc (của cả nhóm hoặc 1 người)
  python theo_doi.py lo-trinh                24 bước của lộ trình 8 ngày
  python theo_doi.py checkin TV1 TV2 ...     Ghi nhận ai đã báo cáo 21h hôm nay
  python theo_doi.py loi them 8 "sai tên biến ImJPG_Deletegreen" [--dong 112]
  python theo_doi.py loi sua 1               Đóng lỗi số 1
  python theo_doi.py loi                     Xem danh sách lỗi
  python theo_doi.py checklist [C3 TV6]      Xem checklist / ký 1 mục (TV4, TV6, TV1)
  python theo_doi.py bao-cao                 In tin nhắn tiến độ để dán vào nhóm chat 21h
  python theo_doi.py excel                   Xuất Theo_doi_Project3.xlsx từ dữ liệu hiện tại
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "theo_doi.json"
TODAY = dt.date.today()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROLES = {"TV1": "Nhóm trưởng · ghép file, nộp bài", "TV2": "Hàm lọc chung",
         "TV3": "Review TV6", "TV4": "Chạy thử bản đầu (N5)",
         "TV5": "Tiến độ, khung báo cáo", "TV6": "Chạy lại bản cuối (N7)", "TV7": "Review TV2"}
TASKS = [(1, "Đọc và hiển thị ảnh", "ImJPG", "TV1"),
         (2, "Kích thước mảng", "m, n, l", "TV1"),
         (3, "Tách 3 kênh màu", "redChannel, greenChannel, blueChannel", "TV4"),
         (4, "Ảnh xám (GrayMatrix)", "ImJPG_Gray", "TV2"),
         (5, "Lọc sepia", "ImJPG_Sepia", "TV3"),
         (6, "Chỉ giữ kênh đỏ", "ImJPG_Red", "TV4"),
         (7, "Hoán vị màu + HueRotate", "ImJPG_Permute, ImJPG_HueRotate", "TV5"),
         (8, "Xóa màu xanh lá", "ImJPG_DeleteGreen", "TV7"),
         (9, "Đảo màu", "ImJPG_Invert", "TV6"),
         (10, "Tăng/giảm từng kênh", "ImJPG_Saturate", "TV6"),
         (11, "Bộ lọc UserMatrix (gửi TV7 trong N2)", "ImJPG_User", "TV2"),
         (12, "Nghịch đảo UserMatrix", "ImJPG_UserInv, ImJPG_Inv", "TV7"),
         (13, "Sepia có khả nghịch?", "ImJPG_SepiaInv", "TV3"),
         (14, "Biến đổi Gamma", "ImJPG_Gamma1, ImJPG_Gamma2", "TV5")]
QUESTIONS = [(1, "uint8 và double / float", "TV2", "TV7"), (2, "RedMatrix làm gì", "TV4", "TV5"),
             (3, "SaturateMatrix làm gì", "TV6", "TV3"), (4, "UserMatrix làm gì", "TV2", "TV7"),
             (5, "Nghịch đảo làm gì với màu", "TV7", "TV2"),
             (6, "Vì sao không khôi phục được ảnh sepia", "TV3", "TV6")]
STEPS = [(1, "Tạo nhóm chat, thư mục chung, tải đề + daylilies.jpg lên 00_DeBai/", "TV1"),
         (1, "Tạo project Overleaf từ bao_cao.zip, mời cả nhóm", "TV1"),
         (1, "Đọc đề + yêu cầu báo cáo, nhắn xác nhận phần mình nhận", "Cả nhóm"),
         (1, "Cài Python 3 + numpy matplotlib pillow, mở thử daylilies.jpg", "Cả nhóm"),
         (1, "Họp online 15 phút: thống nhất quy ước code, giờ báo cáo", "Cả nhóm"),
         (2, "Gửi phần đầu file chung (apply_filter, to_uint8, show) - sáng N2", "TV2"),
         (2, "Gửi code Task 11 cho TV7 - cuối N2", "TV2"),
         (3, "Check-in giữa kỳ tối N3 (15 phút)", "TV5"),
         (4, "Tìm/chụp 2-3 ảnh thêm vào 05_DuLieuThem/ (ghi nguồn)", "TV4 · TV6"),
         (4, "Trao đổi np.linalg.inv, det, cond cho Task 12-13", "TV3 · TV7"),
         (4, "Viết partX.py, lưu ảnh vào 02_Anh/, nháp câu trả lời", "Cả nhóm"),
         (4, "◆ HẠN CHÓT: nộp partX.py vào 01_Parts/", "Cả nhóm"),
         (5, "Ghép 7 phần (python ghep_file.py --run)", "TV1"),
         (5, "Lưu 03_BanGhep/lab03_v1.py, báo nhóm", "TV1"),
         (5, "Chạy bản ghép trong thư mục sạch, đối chiếu Fig. 5, Fig. 6", "TV4"),
         (5, "Ghi từng lỗi (python theo_doi.py loi them ...)", "TV4"),
         (5, "Chạy vi_du_them.py, đưa bao_cao/figures/ lên Overleaf", "TV6"),
         (6, "Sửa lỗi trong partX.py của mình, gửi lại", "Người phụ trách"),
         (6, "Review chéo câu trả lời và phần báo cáo theo cặp", "Cả nhóm"),
         (6, "Họp tối N6 (20 phút): chốt Q5, Q6", "Cả nhóm"),
         (6, "◆ Nháp đủ các phần báo cáo trên Overleaf", "Cả nhóm"),
         (7, "Cập nhật bản ghép v2, v3… (chỉ TV1 sửa)", "TV1"),
         (7, "◆ Chốt lab03_final.py (python ghep_file.py --final)", "TV1"),
         (7, "Chạy lại bản cuối, đi hết checklist và ký", "TV6"),
         (7, "Chép lab03.py vào bao_cao/code/, chạy lại vi_du_them.py", "TV1"),
         (7, "Gom tài liệu tham khảo", "TV5"),
         (8, "Xuất báo cáo PDF từ Overleaf (python ghep_file.py --nop cho code)", "TV1"),
         (8, "◆ Nộp lab03.py + báo cáo PDF (+ nguồn LaTeX), lưu 04_Nop/", "TV1"),
         (8, "Chụp xác nhận đã nộp gửi nhóm chat", "TV1")]
REPORT = [(1, "BC 1. Problem statement", "TV5", 6),
          (2, "BC 2.1 Color arrays, linear filters", "TV2", 6),
          (3, "BC 2.2 Determinant, inverse", "TV7", 6),
          (4, "BC 2.3 Eigenvalues, conditioning", "TV3", 6),
          (5, "BC 3. Code", "TV1", 7),
          (6, "BC 4.1 Example: daylilies", "TV4", 6),
          (7, "BC 4.2 Additional data", "TV6", 6),
          (8, "BC 5. Comments", "TV7", 6),
          (9, "BC 6. References (gom nguồn)", "TV5", 7)]
CHECKLIST = ["lab03.py chạy hết không lỗi, chỉ cần daylilies.jpg",
             "Đủ 14 task và tất cả biến đề yêu cầu",
             "Đủ câu trả lời Q1-Q6 (# Q1: / # A1:)",
             "Ảnh Task 3 và Task 7 giống Fig. 5, Fig. 6",
             "Task 12: khôi phục ImJPG_User sai lệch ≤ 1",
             "Task 13: ảnh khôi phục sepia là nhiễu, có giải thích Q6",
             "Số liệu khớp: 308,322,3 · det(User)=0.3025 · cond(Sepia)≈16659",
             "Không lặp phần đầu file; cuối file có plt.show()",
             "Báo cáo đủ 6 phần, mỗi người đã xóa TODO phần mình",
             "Cả nhóm đã đọc lại bản cuối",
             "Lý thuyết tự viết, có trích dẫn; ảnh thêm có ghi nguồn"]
SIGNERS = ["TV4", "TV6", "TV1"]
STATUS = {"chua": "Chưa làm", "dang": "Đang làm", "xong": "Xong"}


# ------------------------------------------------------------------ dữ liệu
def new_data():
    items = {}
    for n, name, vars_, who in TASKS:
        items[f"T{n}"] = {"loai": "Task", "ten": name, "bien": vars_, "tv": who,
                          "review": "", "han": 2 if n == 11 else 4,
                          "trang_thai": "Chưa làm", "ngay_xong": ""}
    for n, name, who, rv in QUESTIONS:
        items[f"Q{n}"] = {"loai": "Câu hỏi", "ten": name, "bien": f"# Q{n}: / # A{n}:",
                          "tv": who, "review": rv, "han": 6,
                          "trang_thai": "Chưa làm", "ngay_xong": ""}
    for n, name, tv, due in REPORT:
        items[f"R{n}"] = {"loai": "Báo cáo", "ten": name, "bien": f"bao_cao/sections", "tv": tv,
                          "review": "", "han": due, "trang_thai": "Chưa làm", "ngay_xong": ""}
    for i, (d, name, who) in enumerate(STEPS, 1):
        items[f"B{i}"] = {"loai": "Bước", "ten": name, "bien": "", "tv": who,
                          "review": "", "han": d, "trang_thai": "Chưa làm", "ngay_xong": ""}
    return {"phien_ban": 3, "ngay_nhan_de": "", "thanh_vien": {k: "" for k in ROLES},
            "viec": items, "loi": [], "checkin": {},
            "checklist": {f"C{i}": {s: False for s in SIGNERS} for i in range(1, len(CHECKLIST) + 1)}}


def migrate(d):
    """Dữ liệu bản cũ (chưa có báo cáo): giữ task/câu hỏi/tên/lỗi, làm mới lộ trình."""
    fresh = new_data()
    for k, it in d["viec"].items():
        if k[0] in "TQ":
            fresh["viec"][k] = it
        elif k[0] == "R" and k in fresh["viec"]:      # giữ trạng thái, cập nhật người viết
            for f in ("trang_thai", "ngay_xong"):
                fresh["viec"][k][f] = it[f]
    for k in ("ngay_nhan_de", "thanh_vien", "loi", "checkin"):
        fresh[k] = d[k]
    for k, v in d["checklist"].items():
        if k in fresh["checklist"] and (k != "C9" or d.get("phien_ban", 1) >= 2):
            fresh["checklist"][k] = v
    save(fresh)
    print("(Đã cập nhật phân công mới; trạng thái task, câu hỏi, báo cáo được giữ, lộ trình làm lại.)\n")
    return fresh


def load():
    if DATA.exists():
        d = json.loads(DATA.read_text(encoding="utf-8"))
        return d if d.get("phien_ban", 1) >= 3 else migrate(d)
    d = new_data()
    save(d)
    print(f"(Đã tạo {DATA.name}. Đặt ngày nhận đề: python theo_doi.py bat-dau YYYY-MM-DD)\n")
    return d


def save(d):
    DATA.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def start(d):
    return dt.date.fromisoformat(d["ngay_nhan_de"]) if d["ngay_nhan_de"] else None


def due_date(d, n):
    s = start(d)
    return s + dt.timedelta(days=n - 1) if s else None


def day_label(d):
    s = start(d)
    if not s:
        return "chưa đặt ngày nhận đề"
    k = (TODAY - s).days + 1
    return "chưa bắt đầu" if k < 1 else ("đã quá N8" if k > 8 else f"N{k}")


def who(d, tv):
    name = d["thanh_vien"].get(tv, "")
    return f"{tv} · {name}" if name else tv


def warn(d, it):
    if it["trang_thai"] == "Xong":
        due = due_date(d, it["han"])
        if due and it["ngay_xong"] and dt.date.fromisoformat(it["ngay_xong"]) > due:
            return "xong trễ"
        return ""
    due = due_date(d, it["han"])
    if not due:
        return ""
    if TODAY > due:
        return "QUÁ HẠN"
    if (due - TODAY).days <= 1:
        return "sắp đến hạn"
    return ""


def set_status(d, key, status, quiet=False):
    key = key.upper()
    if key not in d["viec"]:
        print(f"  Không có mã {key} (dùng T1-T14, Q1-Q6, R1-R9, B1-B{len(STEPS)})")
        return False
    it = d["viec"][key]
    it["trang_thai"] = status
    it["ngay_xong"] = TODAY.isoformat() if status == "Xong" else ""
    if not quiet:
        print(f"  {key} {it['ten']} -> {status}")
    return True


def bar(frac, width=20):
    full = round(frac * width)
    return "█" * full + "░" * (width - full) + f" {frac:4.0%}"


# ------------------------------------------------------------------ lệnh
def cmd_overview(d, _a):
    v = d["viec"]
    tq = [k for k in v if k[0] in "TQR"]
    steps = [k for k in v if k[0] == "B"]
    done = lambda ks: sum(v[k]["trang_thai"] == "Xong" for k in ks)
    s = start(d)
    print("=" * 64)
    print(" PROJECT 3 · ĐẠI SỐ TUYẾN TÍNH - TỔNG QUAN")
    print("=" * 64)
    print(f" Hôm nay      : {TODAY:%d/%m/%Y} ({day_label(d)})")
    if s:
        left = (s + dt.timedelta(days=7) - TODAY).days
        print(f" Hạn nộp (N8) : {s + dt.timedelta(days=7):%d/%m/%Y} - còn {left} ngày")
    print(f" Task         : {done([k for k in tq if k[0] == 'T'])}/14     "
          f"Câu hỏi: {done([k for k in tq if k[0] == 'Q'])}/6")
    rp = [k for k in v if k[0] == "R"]
    print(f" Báo cáo      : {done(rp)}/{len(rp)} phần")
    print(f" Code + báo cáo {bar(done(tq) / len(tq))}")
    print(f" Lộ trình       {bar(done(steps) / len(steps))}")
    open_bugs = [b for b in d["loi"] if b["trang_thai"] != "Đã sửa"]
    print(f" Lỗi còn mở   : {len(open_bugs)}")
    ok = sum(all(c.values()) for c in d["checklist"].values())
    print(f" Checklist nộp: {ok}/{len(CHECKLIST)}{'  -> SẴN SÀNG NỘP' if ok == len(CHECKLIST) else ''}")

    print("\n TIẾN ĐỘ TỪNG NGƯỜI (task + câu hỏi + báo cáo)")
    for tv in ROLES:
        ks = [k for k in tq if v[k]["tv"] == tv]
        n_done = done(ks)
        late = sum(warn(d, v[k]) == "QUÁ HẠN" for k in ks)
        flag = f"  ⚠ {late} quá hạn" if late else ""
        print(f"  {who(d, tv):<26} {bar(n_done / len(ks) if ks else 0, 14)}  {n_done}/{len(ks)}{flag}")

    alerts = [(k, it) for k, it in v.items() if warn(d, it) in ("QUÁ HẠN", "sắp đến hạn")]
    if alerts:
        print("\n CẦN CHÚ Ý")
        for k, it in sorted(alerts, key=lambda x: (x[1]["han"], x[0][0], int(x[0][1:]))):
            print(f"  [{warn(d, it):^11}] {k:<4} {it['ten'][:40]:<40} {who(d, it['tv'])}")
    if s:
        print("\n MỐC SẮP TỚI")
        for n, txt in [(2, "TV2 gửi phần đầu file + Task 11 cho TV7"), (4, "◆ Nộp đủ 7 partX.py"),
                       (5, "Ghép lab03_v1 · TV4 chạy thử"), (6, "◆ Nháp đủ báo cáo · họp chốt Q5, Q6"),
                       (7, "◆ Chốt lab03_final · TV6 ký checklist"), (8, "◆ Nộp code + báo cáo PDF")]:
            dd = due_date(d, n)
            if dd >= TODAY:
                print(f"  N{n} {dd:%d/%m}  {txt}  (còn {(dd - TODAY).days} ngày)")
    print()


def cmd_list(d, a):
    tv = a.tv.upper() if a.tv else None
    print(f"{'Mã':<4} {'Việc':<38} {'Phụ trách':<24} {'Hạn':<9} {'Trạng thái':<10} Cảnh báo")
    print("-" * 100)
    for k, it in d["viec"].items():
        if k[0] == "B" or (tv and it["tv"] != tv):
            continue
        due = due_date(d, it["han"])
        dtxt = f"N{it['han']} {due:%d/%m}" if due else f"N{it['han']}"
        print(f"{k:<4} {it['ten'][:38]:<38} {who(d, it['tv'])[:24]:<24} {dtxt:<9} "
              f"{it['trang_thai']:<10} {warn(d, it)}")


def cmd_steps(d, _a):
    cur = None
    for k, it in d["viec"].items():
        if k[0] != "B":
            continue
        if it["han"] != cur:
            cur = it["han"]
            due = due_date(d, cur)
            print(f"\n── N{cur}" + (f" ({due:%d/%m})" if due else ""))
        mark = {"Xong": "✔", "Đang làm": "…"}.get(it["trang_thai"], " ")
        print(f"  [{mark}] {k:<4} {it['ten']:<62} {it['tv']:<14} {warn(d, it)}")


def cmd_status(status):
    def run(d, a):
        for key in a.ma:
            set_status(d, key, status)
        save(d)
    return run


def cmd_scan(d, _a):
    """Quét 01_Parts/*.py: task có marker + đủ biến + không lỗi cú pháp -> Xong."""
    import ast
    import re
    try:
        from ghep_file import split_part, REQUIRED_VARS
    except ImportError:
        sys.exit("Cần file ghep_file.py nằm cùng thư mục.")
    parts = sorted((ROOT / "01_Parts").glob("part*.py"))
    if not parts:
        print("Chưa có file nào trong 01_Parts/.")
        return
    found, text_all = {}, ""
    for p in parts:
        _, blocks, _ = split_part(p)
        for t, blk in blocks.items():
            found[t] = (p.name, "\n".join(blk))
        text_all += p.read_text(encoding="utf-8") + "\n"
    print(f"Đã quét {len(parts)} file: {', '.join(p.name for p in parts)}\n")
    for t in range(1, 15):
        key, it = f"T{t}", d["viec"][f"T{t}"]
        if t not in found:
            print(f"  T{t:<3} chưa có code                         ({who(d, it['tv'])})")
            continue
        fname, code = found[t]
        try:
            assigned = {n.id for n in ast.walk(ast.parse(code))
                        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
        except SyntaxError as e:
            print(f"  T{t:<3} LỖI CÚ PHÁP dòng {e.lineno} trong {fname}")
            if it["trang_thai"] == "Xong":
                set_status(d, key, "Đang làm", quiet=True)
            continue
        missing = [x for x in REQUIRED_VARS[t] if x not in assigned]
        if missing:
            print(f"  T{t:<3} thiếu biến {', '.join(missing)}  ({fname})")
            if it["trang_thai"] != "Xong":
                set_status(d, key, "Đang làm", quiet=True)
        else:
            if it["trang_thai"] != "Xong":
                set_status(d, key, "Xong", quiet=True)
                print(f"  T{t:<3} ✔ -> Xong  ({fname})")
            else:
                print(f"  T{t:<3} ✔")
    for q in range(1, 7):
        key = f"Q{q}"
        has = re.search(rf"^#\s*A{q}\s*[:.]\s*\S", text_all, re.M)
        it = d["viec"][key]
        if has and it["trang_thai"] == "Chưa làm":
            set_status(d, key, "Đang làm", quiet=True)
            print(f"  {key:<4} có nháp câu trả lời -> Đang làm (chốt Xong sau họp/review)")
        elif not has:
            print(f"  {key:<4} chưa có # A{q}:")
    save(d)


def cmd_rename(d, a):
    tv = a.tv.upper()
    if tv not in ROLES:
        sys.exit("Mã phải là TV1 ... TV7")
    d["thanh_vien"][tv] = a.ho_ten
    save(d)
    print(f"  {tv} = {a.ho_ten}")


def cmd_start(d, a):
    dt.date.fromisoformat(a.ngay)
    d["ngay_nhan_de"] = a.ngay
    save(d)
    print(f"  Ngày nhận đề (N1) = {a.ngay}. Hạn nộp N8 = {due_date(d, 8):%d/%m/%Y}")


def cmd_checkin(d, a):
    key = TODAY.isoformat()
    day = d["checkin"].setdefault(key, [])
    for tv in a.tv:
        tv = tv.upper()
        if tv in ROLES and tv not in day:
            day.append(tv)
    save(d)
    missing = [tv for tv in ROLES if tv not in day]
    print(f"  Check-in {TODAY:%d/%m}: {', '.join(sorted(day))}")
    if missing:
        print(f"  Chưa báo cáo: {', '.join(missing)}")
    if d["checkin"]:
        print("\n  Số tối đã check-in:")
        for tv in ROLES:
            n = sum(tv in v for v in d["checkin"].values())
            print(f"   {who(d, tv):<26} {n}/{len(d['checkin'])}")


def cmd_bug(d, a):
    if a.hanh_dong == "them":
        t = int(a.task)
        owner = d["viec"][f"T{t}"]["tv"] if f"T{t}" in d["viec"] else "?"
        bug = {"so": len(d["loi"]) + 1, "ngay": TODAY.isoformat(), "task": t, "dong": a.dong,
               "mo_ta": a.mo_ta, "tv": owner, "trang_thai": "Mở"}
        d["loi"].append(bug)
        save(d)
        dong = f" - dòng {a.dong}" if a.dong else ""
        print(f"  Dán vào nhóm chat:\n  [Lỗi] Task {t}{dong} - {a.mo_ta} - @{owner} sửa")
    elif a.hanh_dong == "sua":
        for b in d["loi"]:
            if b["so"] == int(a.task):
                b["trang_thai"] = "Đã sửa"
                b["ngay_sua"] = TODAY.isoformat()
                save(d)
                print(f"  Lỗi #{b['so']} đã đóng.")
                return
        print("  Không có lỗi số này.")
    else:
        if not d["loi"]:
            print("  Chưa có lỗi nào.")
        for b in d["loi"]:
            dong = f" dòng {b['dong']}" if b["dong"] else ""
            print(f"  #{b['so']:<3} [{b['trang_thai']:<6}] Task {b['task']}{dong} - {b['mo_ta']} - @{b['tv']}")


def cmd_checklist(d, a):
    if a.ma and a.nguoi:
        key, s = a.ma.upper(), a.nguoi.upper()
        if key not in d["checklist"] or s not in SIGNERS:
            sys.exit("Dùng: checklist C1..C11 TV4|TV6|TV1")
        d["checklist"][key][s] = True
        save(d)
    print(f"  {'Mã':<4} {'Hạng mục':<58} TV4 TV6 TV1")
    for i, text in enumerate(CHECKLIST, 1):
        c = d["checklist"][f"C{i}"]
        marks = "  ".join(" ✔" if c[s] else " ·" for s in SIGNERS)
        print(f"  C{i:<3} {text[:58]:<58} {marks}")


def cmd_report(d, _a):
    v = d["viec"]
    tq = [k for k in v if k[0] in "TQR"]
    done = [k for k in tq if v[k]["trang_thai"] == "Xong"]
    today_done = [k for k in v if v[k]["ngay_xong"] == TODAY.isoformat()]
    late = [k for k in v if warn(d, v[k]) == "QUÁ HẠN"]
    soon = [k for k in v if warn(d, v[k]) == "sắp đến hạn"]
    bugs = [b for b in d["loi"] if b["trang_thai"] != "Đã sửa"]
    print(f"📊 Tiến độ Project 3 - {TODAY:%d/%m} ({day_label(d)})")
    print(f"• Task + câu hỏi + phần báo cáo: {len(done)}/{len(tq)} xong")
    if today_done:
        print(f"• Hôm nay xong: {', '.join(today_done)}")
    if late:
        print("• ⚠ Quá hạn: " + ", ".join(f"{k} (@{v[k]['tv']})" for k in late))
    if soon:
        print("• Sắp đến hạn: " + ", ".join(f"{k} (@{v[k]['tv']})" for k in soon))
    if bugs:
        print("• Lỗi còn mở: " + ", ".join(f"Task {b['task']} (@{b['tv']})" for b in bugs))
    missing = [tv for tv in ROLES if tv not in d["checkin"].get(TODAY.isoformat(), [])]
    if missing and d["checkin"]:
        print(f"• Chưa check-in tối nay: {', '.join(missing)}")
    print("Mọi người nhớ cập nhật trạng thái trước 21h nhé!")


def cmd_excel(d, _a):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
    except ImportError:
        sys.exit("Cần cài: pip install openpyxl")
    wb = Workbook()
    fill = {"Xong": "D1FADF", "Đang làm": "FEF0C7", "Chưa làm": "F2F4F7"}
    hdr = PatternFill("solid", fgColor="1F2A44")
    sheets = [("Công việc", lambda k: k[0] in "TQR"), ("Lộ trình 8 ngày", lambda k: k[0] == "B")]
    for idx, (title, keep) in enumerate(sheets):
        ws = wb.active if idx == 0 else wb.create_sheet()
        ws.title = title
        ws.append(["Mã", "Việc", "Biến / ghi chú", "Phụ trách", "Hạn", "Trạng thái", "Ngày xong", "Cảnh báo"])
        for k, it in d["viec"].items():
            if not keep(k):
                continue
            due = due_date(d, it["han"])
            ws.append([k, it["ten"], it["bien"], who(d, it["tv"]),
                       f"N{it['han']}" + (f" {due:%d/%m}" if due else ""),
                       it["trang_thai"], it["ngay_xong"], warn(d, it)])
            ws.cell(ws.max_row, 6).fill = PatternFill("solid", fgColor=fill[it["trang_thai"]])
            if warn(d, it) == "QUÁ HẠN":
                ws.cell(ws.max_row, 8).font = Font(name="Arial", color="B42318", bold=True)
        for c, w in zip("ABCDEFGH", [6, 44, 34, 24, 12, 12, 12, 14]):
            ws.column_dimensions[c].width = w
    ws = wb.create_sheet("Báo lỗi")
    ws.append(["#", "Ngày", "Task", "Dòng", "Mô tả", "Người sửa", "Trạng thái"])
    for b in d["loi"]:
        ws.append([b["so"], b["ngay"], b["task"], b["dong"], b["mo_ta"], b["tv"], b["trang_thai"]])
    ws.column_dimensions["E"].width = 50
    for ws in wb.worksheets:
        for cell in ws[1]:
            cell.font = Font(name="Arial", bold=True, color="FFFFFF")
            cell.fill = hdr
            cell.alignment = Alignment(horizontal="center")
        ws.freeze_panes = "A2"
    out = ROOT / "Theo_doi_Project3.xlsx"
    wb.save(out)
    print(f"  Đã xuất {out.name}")


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description="Theo dõi tiến độ Project 3",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=__doc__.split("LỆNH THƯỜNG DÙNG")[1])
    sub = ap.add_subparsers(dest="lenh")
    sub.add_parser("tong-quan")
    p = sub.add_parser("ds"); p.add_argument("tv", nargs="?")
    sub.add_parser("lo-trinh")
    for name, st in STATUS.items():
        p = sub.add_parser(name); p.add_argument("ma", nargs="+")
        p.set_defaults(func=cmd_status(st))
    sub.add_parser("quet")
    p = sub.add_parser("ten"); p.add_argument("tv"); p.add_argument("ho_ten")
    p = sub.add_parser("bat-dau"); p.add_argument("ngay", help="YYYY-MM-DD")
    p = sub.add_parser("checkin"); p.add_argument("tv", nargs="+")
    p = sub.add_parser("loi"); p.add_argument("hanh_dong", nargs="?", choices=["them", "sua"])
    p.add_argument("task", nargs="?"); p.add_argument("mo_ta", nargs="?")
    p.add_argument("--dong", type=int)
    p = sub.add_parser("checklist"); p.add_argument("ma", nargs="?"); p.add_argument("nguoi", nargs="?")
    sub.add_parser("bao-cao")
    sub.add_parser("excel")
    a = ap.parse_args()

    d = load()
    table = {None: cmd_overview, "tong-quan": cmd_overview, "ds": cmd_list, "lo-trinh": cmd_steps,
             "quet": cmd_scan, "ten": cmd_rename, "bat-dau": cmd_start, "checkin": cmd_checkin,
             "loi": cmd_bug, "checklist": cmd_checklist, "bao-cao": cmd_report, "excel": cmd_excel}
    func = getattr(a, "func", None) or table[a.lenh]
    if a.lenh == "loi" and a.hanh_dong == "them" and (not a.task or not a.mo_ta):
        sys.exit('Dùng: python theo_doi.py loi them <task> "<mô tả>" [--dong N]')
    func(d, a)


if __name__ == "__main__":
    main()
