"""
vi_du_them.py - tạo hình và bảng số liệu cho Phần 4 (Illustrative example) của báo cáo.

  python vi_du_them.py

Đầu vào:
  * 00_DeBai/daylilies.jpg          ảnh của đề (ví dụ trong tài liệu)
  * 05_DuLieuThem/*.jpg|*.png       ảnh nhóm tự tìm / tự chụp (TV4, TV6 bỏ vào)
  * bảng màu tổng hợp               script tự tạo: dải màu thuần + dải xám

Đầu ra (vào bao_cao/figures/, LaTeX tự dùng):
  * bang_mau.png                    ảnh tổng hợp do nhóm tự xây
  * luoi_<ten_anh>.png              11 bộ lọc áp lên từng ảnh
  * khoi_phuc_<ten_anh>.png         gốc / lọc User / khôi phục / lọc Sepia / khôi phục
  * bang_ma_tran.tex                det, cond, khả nghịch? của mọi ma trận lọc
  * bang_khoi_phuc.tex              sai lệch khôi phục + % giá trị bị cắt, cho từng ảnh
  * so_lieu.csv                     cùng số liệu, để kiểm tra
"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
EXTRA_DIR = ROOT / "05_DuLieuThem"
OUT = ROOT / "bao_cao" / "figures"
MAX_SIDE = 600            # thu nhỏ ảnh lớn cho nhanh và nhẹ báo cáo


# ---------- cùng hàm với lab03.py ----------
def to_uint8(x):
    x = np.sign(x) * np.floor(np.abs(x) + 0.5)
    return np.clip(x, 0, 255).astype(np.uint8)


def apply_filter(img, M):
    return to_uint8(img.astype(np.float64) @ M.T)


# ---------- các ma trận trong đề ----------
theta = np.pi / 2
HUE = (np.array([[0.213, 0.715, 0.072]] * 3)
       + np.cos(theta) * np.array([[0.787, -0.715, -0.072], [-0.213, 0.285, -0.072], [-0.213, -0.715, 0.928]])
       + np.sin(theta) * np.array([[-0.213, -0.715, 0.928], [0.143, 0.140, -0.283], [-0.787, 0.715, 0.072]]))
MATRICES = {
    "Gray": np.full((3, 3), 1 / 3),
    "Sepia": np.array([[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]),
    "Red": np.diag([1.0, 0, 0]),
    "Permute": np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]], dtype=float),
    "HueRotate": HUE,
    "DeleteGreen": np.diag([1.0, 0, 1]),
    "Saturate": np.diag([1.2, 0.75, 2]),
    "User": np.array([[0.7, 0.15, 0.15], [0.15, 0.7, 0.15], [0.15, 0.15, 0.7]]),
}


def all_outputs(img):
    out = {name: apply_filter(img, M) for name, M in MATRICES.items()}
    out["Invert"] = 255 - img
    out["Gamma1"] = to_uint8(to_uint8(img.astype(float) ** 0.9).astype(float) + 30)
    out["Gamma2"] = to_uint8(to_uint8(img.astype(float) ** 1.1).astype(float) - 50)
    return out


def color_chart(h=240, w=480):
    """Ảnh tổng hợp: 6 hàng sắc độ thuần (đỏ→tím) từ tối đến sáng + 1 dải xám."""
    hues = np.array([[255, 0, 0], [255, 255, 0], [0, 255, 0],
                     [0, 255, 255], [0, 0, 255], [255, 0, 255]], dtype=float)
    rows = []
    t = np.linspace(0.15, 1, w)[:, None]
    for c in hues:
        rows.append(np.repeat((t * c)[None], h // 7, axis=0))
    gray = np.repeat(np.linspace(0, 255, w)[:, None], 3, axis=1)
    rows.append(np.repeat(gray[None], h - 6 * (h // 7), axis=0))
    return to_uint8(np.concatenate(rows, axis=0))


def load(path):
    im = Image.open(path).convert("RGB")
    if max(im.size) > MAX_SIDE:
        im.thumbnail((MAX_SIDE, MAX_SIDE))
    return np.array(im)


def clipped_fraction(img, M):
    raw = img.astype(np.float64) @ M.T
    return float(np.mean((raw < -0.5) | (raw > 255.5)))


def save_grid(name, img, outs):
    keys = ["Gray", "Sepia", "Red", "Permute", "HueRotate", "DeleteGreen",
            "Invert", "Saturate", "User", "Gamma1", "Gamma2"]
    fig, axes = plt.subplots(3, 4, figsize=(12, 8.5))
    for ax, (title, im) in zip(axes.flat, [("Original", img)] + [(k, outs[k]) for k in keys]):
        ax.imshow(im)
        ax.set_title(title, fontsize=10)
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(OUT / f"luoi_{name}.png", dpi=110)
    plt.close(fig)


def restore_experiment(name, img, outs):
    user_inv = apply_filter(outs["User"], np.linalg.inv(MATRICES["User"]))
    sepia_inv = apply_filter(outs["Sepia"], np.linalg.inv(MATRICES["Sepia"]))
    fig, axes = plt.subplots(1, 5, figsize=(15, 3.4))
    panels = [("Original", img), ("User filter", outs["User"]), ("User restored", user_inv),
              ("Sepia filter", outs["Sepia"]), ("Sepia restored", sepia_inv)]
    for ax, (t, im) in zip(axes, panels):
        ax.imshow(im); ax.set_title(t, fontsize=10); ax.axis("off")
    fig.tight_layout()
    fig.savefig(OUT / f"khoi_phuc_{name}.png", dpi=110)
    plt.close(fig)
    err = lambda a: np.abs(a.astype(int) - img.astype(int))
    return {
        "user_max": int(err(user_inv).max()), "user_mean": float(err(user_inv).mean()),
        "sepia_max": int(err(sepia_inv).max()), "sepia_mean": float(err(sepia_inv).mean()),
        "clip_sepia": clipped_fraction(img, MATRICES["Sepia"]),
        "clip_saturate": clipped_fraction(img, MATRICES["Saturate"]),
        "clip_userinv": clipped_fraction(img, np.linalg.inv(MATRICES["User"])),
    }


def tex_escape(s):
    return s.replace("_", r"\_")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(exist_ok=True)

    images = {}
    chart = color_chart()
    Image.fromarray(chart).save(OUT / "bang_mau.png")
    images["bang_mau"] = chart
    for p in [ROOT / "00_DeBai" / "daylilies.jpg"] + sorted(
            q for q in EXTRA_DIR.iterdir() if q.suffix.lower() in (".jpg", ".jpeg", ".png")):
        if p.exists():
            images[p.stem] = load(p)
    if "daylilies" not in images:
        print("! Chưa thấy 00_DeBai/daylilies.jpg - chỉ chạy với ảnh khác.")

    # Bảng 1: tính chất các ma trận
    lines = [r"\begin{tabular}{lrrl}", r"\toprule",
             r"Filter & $\det M$ & $\operatorname{cond}(M)$ & Invertible? \\", r"\midrule"]
    print(f"{'Ma trận':<12}{'det':>12}{'cond':>14}")
    for name, M in MATRICES.items():
        det = np.linalg.det(M)
        cond = np.linalg.cond(M)
        if abs(det) < 1e-12:
            verdict, cond_s = "no (singular)", r"$\infty$"
        elif cond > 1e3:
            verdict, cond_s = "in theory only", f"{cond:,.0f}".replace(",", r"\,")
        else:
            verdict, cond_s = "yes", f"{cond:.2f}"
        det_s = f"{det:.3g}" if abs(det) >= 1e-12 else "0"
        lines.append(f"{name} & {det_s} & {cond_s} & {verdict} \\\\")
        print(f"{name:<12}{det:>12.4g}{cond:>14.4g}")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (OUT / "bang_ma_tran.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Bảng 2: thí nghiệm khôi phục trên từng ảnh
    rows = []
    for name, img in images.items():
        outs = all_outputs(img)
        save_grid(name, img, outs)
        r = restore_experiment(name, img, outs)
        r.update(image=name, size=f"{img.shape[0]}x{img.shape[1]}")
        rows.append(r)
        print(f"  {name:<14} {r['size']:<9} User: max {r['user_max']:>3}   "
              f"Sepia: max {r['sepia_max']:>3}, TB {r['sepia_mean']:6.1f}")

    with open(OUT / "so_lieu.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    t = [r"\begin{tabular}{lrrrrrr}", r"\toprule",
         r" & \multicolumn{2}{c}{User $\to$ inverse} & \multicolumn{2}{c}{Sepia $\to$ inverse} "
         r"& \multicolumn{2}{c}{Clipped values} \\",
         r"\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}",
         r"Image & max err & mean err & max err & mean err & Sepia & inv(User) \\", r"\midrule"]
    for r in rows:
        t.append(f"\\texttt{{{tex_escape(r['image'])}}} & {r['user_max']} & {r['user_mean']:.2f} & "
                 f"{r['sepia_max']} & {r['sepia_mean']:.1f} & {100*r['clip_sepia']:.1f}\\% & "
                 f"{100*r['clip_userinv']:.1f}\\% \\\\")
    t += [r"\bottomrule", r"\end{tabular}"]
    (OUT / "bang_khoi_phuc.tex").write_text("\n".join(t) + "\n", encoding="utf-8")

    # danh sách ảnh để main.tex tự chèn
    figs = []
    for name in images:
        if name == "daylilies":
            continue
        n = tex_escape(name)
        figs.append(
            "\\begin{figure}[H]\\centering\n"
            f"\\includegraphics[width=\\textwidth]{{figures/luoi_{name}.png}}\n"
            f"\\caption{{All filters applied to \\texttt{{{n}}}.}}\\label{{fig:grid-{name}}}\n"
            "\\end{figure}\n"
            "\\begin{figure}[H]\\centering\n"
            f"\\includegraphics[width=\\textwidth]{{figures/khoi_phuc_{name}.png}}\n"
            f"\\caption{{Inverse experiment on \\texttt{{{n}}}.}}\\label{{fig:restore-{name}}}\n"
            "\\end{figure}\n")
    (OUT / "hinh_du_lieu_them.tex").write_text("\n".join(figs), encoding="utf-8")
    print(f"\nĐã lưu hình và bảng vào {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
