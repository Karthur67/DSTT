"""
ghep_file.py - công cụ của nhóm trưởng (TV1), Project 3 Đại số tuyến tính.

Đặt file này trong thư mục Project3/ (cùng cấp với 01_Parts/, 03_BanGhep/...).

  python ghep_file.py              Ngày 5-7: ghép part1..part7 -> 03_BanGhep/lab03_vN.py
  python ghep_file.py --run        Ghép rồi chạy thử luôn, đối chiếu số liệu mẫu, lưu ảnh
  python ghep_file.py --final      Tối ngày 7: ghép thành 03_BanGhep/lab03_final.py (kèm chạy thử)
  python ghep_file.py --nop        Ngày 8: chép lab03_final.py -> 04_Nop/lab03.py

Script làm gì:
  * Lấy phần đầu file (import + hàm chung) MỘT lần, từ part1.py.
  * Cắt mỗi partX.py theo dấu "# %% Task N", xếp lại đúng thứ tự Task 1 -> 14.
  * Bỏ các dòng plt.show() lẻ trong từng phần, thêm đúng 1 plt.show() ở cuối.
  * Báo lỗi: thiếu task, trùng task, lỗi cú pháp, thiếu biến đề yêu cầu,
    thiếu Q1-Q6 / A1-A6, dùng .astype(np.uint8) trực tiếp.
"""
import argparse
import ast
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS_DIR = ROOT / "01_Parts"
OUT_DIR = ROOT / "03_BanGhep"
SUBMIT_DIR = ROOT / "04_Nop"
IMAGE_CANDIDATES = [ROOT / "00_DeBai" / "daylilies.jpg", ROOT / "daylilies.jpg"]

# Ai phụ trách task nào (theo ma trận phân công, trang 3)
TASK_OWNER = {1: 1, 2: 1, 3: 4, 4: 2, 5: 3, 6: 4, 7: 5,
              8: 7, 9: 6, 10: 6, 11: 2, 12: 7, 13: 3, 14: 5}
REQUIRED_VARS = {
    1: ["ImJPG"], 2: ["m", "n", "l"],
    3: ["redChannel", "greenChannel", "blueChannel"],
    4: ["ImJPG_Gray"], 5: ["ImJPG_Sepia"], 6: ["ImJPG_Red"],
    7: ["ImJPG_Permute", "ImJPG_HueRotate"], 8: ["ImJPG_DeleteGreen"],
    9: ["ImJPG_Invert"], 10: ["ImJPG_Saturate"], 11: ["ImJPG_User"],
    12: ["ImJPG_UserInv", "ImJPG_Inv"], 13: ["ImJPG_SepiaInv"],
    14: ["ImJPG_Gamma1", "ImJPG_Gamma2"],
}
QUESTION_OWNER = {1: 2, 2: 4, 3: 6, 4: 2, 5: 7, 6: 3}
# Nhóm thống nhất: mọi task lọc bằng ma trận dùng vòng lặp từng pixel như đề (Task 4)
LOOP_TASKS = {4, 5, 6, 7, 8, 10, 11, 12, 13}

MARKER = re.compile(r"^#\s*%%\s*Task\s+(\d+)\b", re.IGNORECASE)
SHOW_LINE = re.compile(r"^plt\.show\(\)\s*(#.*)?$")


def tv(task):
    return f"@TV{TASK_OWNER.get(task, '?')}"


def split_part(path):
    """Trả về (header_lines, {task: block_lines}, list_trùng)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    header, blocks, dup = [], {}, []
    current = None
    for line in lines:
        mk = MARKER.match(line.strip())
        if mk:
            current = int(mk.group(1))
            if current in blocks:
                dup.append(current)
            blocks[current] = [line]
        elif current is None:
            header.append(line)
        else:
            blocks[current].append(line)
    for t, blk in blocks.items():
        blk = [ln for ln in blk if not SHOW_LINE.match(ln.strip())]
        while blk and not blk[-1].strip():
            blk.pop()
        blocks[t] = blk
    return header, blocks, dup


def header_without_image_load(header_lines):
    """Bỏ 2 dòng đọc ảnh / lấy kích thước nếu có trong phần đầu (Task 1-2 đã làm)."""
    out = []
    for ln in header_lines:
        s = ln.strip()
        if s.startswith("ImJPG =") or s.startswith("m, n, l ="):
            continue
        out.append(ln)
    while out and not out[-1].strip():
        out.pop()
    return out


def defined_functions(src):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return {}
    return {node.name: ast.get_source_segment(src, node)
            for node in tree.body if isinstance(node, ast.FunctionDef)}


def assigned_names(src):
    names = set()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            names.add(node.id)
    return names


def build(out_path):
    errors, warnings = [], []
    parts = sorted(PARTS_DIR.glob("part*.py"),
                   key=lambda p: int(re.sub(r"\D", "", p.stem) or 0))
    if not parts:
        sys.exit(f"Không thấy file part*.py nào trong {PARTS_DIR}")
    names = [p.name for p in parts]
    for i in range(1, 8):
        if f"part{i}.py" not in names:
            errors.append(f"[Thiếu file] part{i}.py chưa có trong 01_Parts/ - @TV{i}")

    canonical_header, all_blocks, extra_defs = None, {}, {}
    for p in parts:
        header, blocks, dup = split_part(p)
        for t in dup:
            errors.append(f"[Lỗi] {p.name} có 2 lần '# %% Task {t}' - {tv(t)} sửa")
        if p.name == "part1.py" or canonical_header is None:
            if p.name == "part1.py":
                canonical_header = header_without_image_load(header)
        for t, blk in blocks.items():
            if t not in TASK_OWNER:
                warnings.append(f"[Cảnh báo] {p.name}: Task {t} không có trong đề, bỏ qua")
                continue
            if t in all_blocks:
                errors.append(f"[Lỗi] Task {t} có ở cả {all_blocks[t][0]} và {p.name}")
                continue
            all_blocks[t] = (p.name, blk)
        # hàm riêng ai đó tự viết thêm ở phần đầu file của họ
        for name, src in defined_functions("\n".join(header)).items():
            extra_defs.setdefault(name, (p.name, src))

    if canonical_header is None:
        sys.exit("Cần có 01_Parts/part1.py (chứa phần đầu file chung).")
    base_funcs = defined_functions("\n".join(canonical_header))
    task_code = "\n".join("\n".join(blk) for _, blk in all_blocks.values())
    # chỉ chép hàm riêng nếu task thật sự gọi tới (tránh hàm thừa trong file nộp)
    extra = {k: v for k, v in extra_defs.items()
             if k not in base_funcs and re.search(rf"\b{k}\s*\(", task_code)}

    out = ['"""',
           "Project 3: Matrix multiplication, inversion, and photo filters  (Python version)",
           "",
           "Requirements:  pip install numpy matplotlib pillow",
           "Run:           python lab03.py        (daylilies.jpg must be in the same folder)",
           "",
           "Variable names follow the MATLAB project (ImJPG, redChannel, ImJPG_Gray, ...).",
           '"""']
    out += [ln for ln in canonical_header
            if not ln.strip().startswith("# =====") and "Thay bằng bản TV2" not in ln]
    for name, (src_file, src) in extra.items():
        users = sorted({tv(t) for t, (_, blk) in all_blocks.items()
                        if re.search(rf"\b{name}\s*\(", "\n".join(blk))})
        warnings.append(f"[Cảnh báo] Có task gọi {name}() nhưng phần đầu chung không có hàm này - "
                        f"đã tạm chép từ {src_file}; nên dùng hàm chung (apply_filter_loop) - {', '.join(users)}")
        out += ["", "", src]
    out += ["", ""]

    for t in range(1, 15):
        if t not in all_blocks:
            errors.append(f"[Thiếu] Task {t} chưa có - {tv(t)}")
            continue
        src_file, blk = all_blocks[t]
        code = "\n".join(blk)
        try:
            names_set = assigned_names(code)
        except SyntaxError as e:
            errors.append(f"[Lỗi cú pháp] Task {t} ({src_file}) dòng {e.lineno} trong khối: "
                          f"{e.msg} - {tv(t)} sửa")
            names_set = set()
        for v in REQUIRED_VARS[t]:
            if names_set and v not in names_set:
                errors.append(f"[Lỗi] Task {t} - thiếu/sai tên biến {v} - {tv(t)} sửa")
        if t in LOOP_TASKS and "apply_filter_loop" not in code:
            warnings.append(f"[Cảnh báo] Task {t} ({src_file}): nhóm thống nhất lọc bằng vòng lặp từng pixel, "
                            f"dùng apply_filter_loop(...) - {tv(t)}")
        for k, ln in enumerate(blk):
            if ".astype(np.uint8)" in ln and not ln.lstrip().startswith("#"):
                warnings.append(f"[Cảnh báo] Task {t} ({src_file}) dòng {k+1} trong khối: "
                                f"dùng .astype(np.uint8) trực tiếp, nên dùng to_uint8() - {tv(t)}")
        out += blk + [""]

    out += ["", "plt.show()", ""]
    text = "\n".join(out)

    for q, owner in QUESTION_OWNER.items():
        if not re.search(rf"^#\s*Q{q}\s*[:.]", text, re.M):
            errors.append(f"[Thiếu] Câu hỏi Q{q} - @TV{owner}")
        if not re.search(rf"^#\s*A{q}\s*[:.]", text, re.M):
            errors.append(f"[Thiếu] Câu trả lời A{q} - @TV{owner}")

    OUT_DIR.mkdir(exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    try:
        ast.parse(text)
    except SyntaxError as e:
        errors.append(f"[Lỗi cú pháp] file ghép dòng {e.lineno}: {e.msg}")
    return errors, warnings


def next_version_path():
    n = 1
    while (OUT_DIR / f"lab03_v{n}.py").exists():
        n += 1
    return OUT_DIR / f"lab03_v{n}.py"


def run_and_check(path):
    """Chạy file ghép (không mở cửa sổ), đối chiếu số liệu mẫu trang 9, lưu ảnh."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import runpy

    img = next((p for p in IMAGE_CANDIDATES if p.exists()), None)
    if img is None:
        return ["[Chạy thử] Không thấy daylilies.jpg trong 00_DeBai/ - bỏ qua bước chạy"]
    work = OUT_DIR / f"_chay_{path.stem}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    shutil.copy(img, work / "daylilies.jpg")
    shutil.copy(path, work / "lab03.py")
    old = os.getcwd()
    os.chdir(work)                       # thư mục sạch: chỉ có lab03.py + ảnh
    problems = []
    try:
        plt.close("all")
        g = runpy.run_path("lab03.py", run_name="__main__")
    except Exception as e:
        os.chdir(old)
        return [f"[Chạy thử] File ghép bị lỗi khi chạy: {type(e).__name__}: {e}"]
    finally:
        os.chdir(old)

    for t, vs in REQUIRED_VARS.items():
        for v in vs:
            if v not in g:
                problems.append(f"[Chạy thử] Không có biến {v} sau khi chạy - {tv(t)}")
    for v in [x for vs in REQUIRED_VARS.values() for x in vs if x.startswith("ImJPG")]:
        if v in g and getattr(g[v], "dtype", None) != np.uint8:
            problems.append(f"[Chạy thử] {v} có kiểu {getattr(g[v], 'dtype', type(g[v]))}, "
                            f"cần uint8")

    def near(name, got, want, rel):
        ok = abs(got - want) <= rel * abs(want)
        mark = "OK " if ok else "SAI"
        print(f"   {mark} {name:<34} = {got:.6g}   (mẫu {want:.6g})")
        if not ok:
            problems.append(f"[Số liệu] {name} = {got:.6g}, mẫu là {want:.6g}")

    print("\n== Đối chiếu số liệu (trang 9 của lộ trình) ==")
    if all(k in g for k in "mnl"):
        print(f"   m, n, l = {g['m']}, {g['n']}, {g['l']}   (mẫu 308, 322, 3)")
        if (g["m"], g["n"], g["l"]) != (308, 322, 3):
            problems.append("[Số liệu] Kích thước ảnh khác 308, 322, 3 - kiểm tra lại daylilies.jpg")
    if "UserMatrix" in g:
        near("det(UserMatrix)", np.linalg.det(g["UserMatrix"]), 0.3025, 1e-3)
        near("inv(UserMatrix) đường chéo", np.linalg.inv(g["UserMatrix"])[0, 0], 1.5455, 1e-3)
    if "ImJPG_UserInv" in g and "ImJPG" in g:
        err = int(np.abs(g["ImJPG_UserInv"].astype(int) - g["ImJPG"].astype(int)).max())
        print(f"   {'OK ' if err <= 1 else 'SAI'} Sai lệch khôi phục ImJPG_User      = {err}   (mẫu tối đa 1)")
        if err > 1:
            problems.append(f"[Số liệu] Sai lệch khôi phục ImJPG_User = {err} (> 1) - @TV7")
    if "SepiaMatrix" in g:
        near("det(SepiaMatrix)", np.linalg.det(g["SepiaMatrix"]), 1.21e-7, 0.05)
        near("cond(SepiaMatrix)", np.linalg.cond(g["SepiaMatrix"]), 16659, 0.02)

    figs_dir = OUT_DIR / f"anh_{path.stem}"
    figs_dir.mkdir(exist_ok=True)
    nums = plt.get_fignums()
    for k in nums:
        fig = plt.figure(k)
        title = fig.axes[0].get_title() if fig.axes else f"fig{k}"
        safe = re.sub(r"[^A-Za-z0-9_-]+", "_", title).strip("_")
        fig.savefig(figs_dir / f"{k:02d}_{safe}.png", dpi=80, bbox_inches="tight")
    plt.close("all")
    print(f"\n   Đã lưu {len(nums)} hình vào {figs_dir.relative_to(ROOT)}/ để TV4/TV6 so với Fig. 5, Fig. 6")
    shutil.rmtree(work, ignore_errors=True)
    return problems


def main():
    ap = argparse.ArgumentParser(description="Ghép partX.py thành lab03 (TV1)")
    ap.add_argument("--run", action="store_true", help="chạy thử bản ghép và đối chiếu số liệu")
    ap.add_argument("--final", action="store_true", help="ghép thành lab03_final.py (tối ngày 7)")
    ap.add_argument("--nop", action="store_true", help="chép lab03_final.py sang 04_Nop/lab03.py")
    a = ap.parse_args()

    if a.nop:
        src = OUT_DIR / "lab03_final.py"
        if not src.exists():
            sys.exit("Chưa có 03_BanGhep/lab03_final.py - chạy 'python ghep_file.py --final' trước.")
        SUBMIT_DIR.mkdir(exist_ok=True)
        shutil.copy(src, SUBMIT_DIR / "lab03.py")
        print("Đã tạo 04_Nop/lab03.py - nộp file này (chỉ cần kèm daylilies.jpg).")
        return

    OUT_DIR.mkdir(exist_ok=True)
    out_path = OUT_DIR / "lab03_final.py" if a.final else next_version_path()
    errors, warnings = build(out_path)
    print(f"Đã ghép: {out_path.relative_to(ROOT)}")
    if a.run or a.final:
        errors += run_and_check(out_path)

    print("\n== Danh sách lỗi (dán thẳng vào nhóm chat) ==")
    if not errors and not warnings:
        print("   Không có lỗi nào. ✔")
    for e in errors + warnings:
        print("  ", e)
    if a.final and errors:
        print("\n!! Bản final còn lỗi - chưa nên nộp.")


if __name__ == "__main__":
    main()
