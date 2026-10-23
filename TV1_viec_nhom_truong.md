# Việc của nhóm trưởng (TV1) – Project 3

## Lịch việc theo ngày

| Ngày | Việc | Xong |
|---|---|---|
| 1 | Tạo nhóm chat, upload thư mục `Project3/` này lên Drive chung, bỏ đề + `daylilies.jpg` vào `00_DeBai/` | ☐ |
| 1 | Gửi **tin nhắn 1** (mở nhóm). Không cần xin phép dùng Python: đề ưu tiên Python | ☐ |
| 1 | Overleaf: New Project → Upload Project → `bao_cao.zip`, mời 6 bạn, gửi link vào nhóm | ☐ |
| 1 | Chủ trì họp 15 phút: chốt quy ước code, giờ báo cáo 21h | ☐ |
| 2–4 | `01_Parts/part1.py` đã viết xong (Task 1–2) → đánh dấu **Xong** | ☐ |
| 2 | Khi TV2 gửi phần đầu file chung: so với phần đầu trong `part1.py`, nếu khác thì dán bản của TV2 vào | ☐ |
| 5 | Tải 7 file `partX.py` về `01_Parts/`, chạy `python ghep_file.py --run` | ☐ |
| 5 | Gửi **tin nhắn 3** kèm `lab03_v1.py` và danh sách lỗi script in ra | ☐ |
| 6–7 | Nhận đoạn sửa → thay vào `partX.py` tương ứng → chạy lại `python ghep_file.py --run` (ra v2, v3…) | ☐ |
| 6 | Họp chốt Q5, Q6; đọc lướt toàn bộ câu trả lời Q1–Q6 | ☐ |
| 7 | `python ghep_file.py --final` → gửi `lab03_final.py` cho TV6 chạy lại & ký checklist | ☐ |
| 7 | Chép `lab03_final.py` thành `bao_cao/code/lab03.py`, chạy `python vi_du_them.py`, tải `code/` và `figures/` lên Overleaf; viết mục 3 (Code) | ☐ |
| 8 | `python ghep_file.py --nop` → nộp `04_Nop/lab03.py` + báo cáo PDF (tải từ Overleaf) → gửi **tin nhắn 4** + ảnh chụp xác nhận | ☐ |

**Nguyên tắc:** chỉ mình TV1 sửa file ghép. Ai báo lỗi thì người phụ trách sửa trong `partX.py` của họ rồi gửi lại – không sửa tay vào `lab03_vN.py`, nếu không lần ghép sau sẽ mất.

## Báo cáo (bắt buộc, LaTeX trên Overleaf)

| Phần | Người viết | File | Hạn nháp |
|---|---|---|---|
| 1. Problem statement | TV5 | `sections/01_problem.tex` | N6 |
| 2.1 Color arrays, linear filters | TV2 | `sections/02_theory.tex` | N6 |
| 2.2 Determinant, inverse | TV7 | `sections/02_theory.tex` | N6 |
| 2.3 Eigenvalues, conditioning | TV3 | `sections/02_theory.tex` | N6 |
| 3. Code | TV1 | `sections/03_code.tex` | N7 |
| 4.1 Ví dụ daylilies | TV4 | `sections/04_examples.tex` | N6 |
| 4.2 Dữ liệu thêm | TV6 | `sections/04_examples.tex` | N6 |
| 5. Comments | TV7 | `sections/05_comments.tex` | N6 |
| 6. References | TV5 | `refs.bib` | N7 |
| Xuất PDF báo cáo | TV1 | Overleaf → Download PDF | N8 |

Mỗi file có sẵn gợi ý nội dung (dòng `%`) và ô `[TODO]` đỏ. Phần lý thuyết **tự viết**, không chép lời giải trong file lộ trình. Trước khi nộp: bỏ dấu `%` ở dòng `\renewcommand{\todo}...` trong `main.tex` để ẩn TODO và tên người viết. Comment trong `lab03.py` viết tiếng Anh, vì code được in vào phụ lục.

Dữ liệu thêm cho phần 4: TV4, TV6 bỏ 2–3 ảnh vào `05_DuLieuThem/` (ghi nguồn), chạy `python vi_du_them.py`. Script tự tạo thêm một ảnh bảng màu, áp 11 bộ lọc lên mọi ảnh, thử khôi phục bằng nghịch đảo, rồi xuất hình và bảng LaTeX vào `bao_cao/figures/`.

## Theo dõi tiến độ bằng `theo_doi.py`

Thay cho file Excel, mọi thứ chạy bằng Python, dữ liệu lưu trong `theo_doi.json` (để trên Drive chung).

```
python theo_doi.py bat-dau 2026-10-22     # ngày nhận đề, làm 1 lần
python theo_doi.py ten TV2 "Trần Thị B"   # điền tên 7 người
python theo_doi.py                        # bảng tổng quan
python theo_doi.py quet                   # tự đánh dấu task đã có code đúng biến trong 01_Parts/
python theo_doi.py xong T5 Q6 R3 B12      # đánh dấu xong (T task, Q câu hỏi, R phần báo cáo, B bước lộ trình)
python theo_doi.py loi them 8 "sai tên biến" --dong 112
python theo_doi.py bao-cao                # tin nhắn 21h để dán vào nhóm chat
python theo_doi.py excel                  # xuất Excel khi cần gửi ai đó xem
```

## Cách dùng `ghep_file.py`

```
pip install numpy matplotlib pillow
python ghep_file.py            # ghép ra 03_BanGhep/lab03_v1.py, v2, ...
python ghep_file.py --run      # ghép + chạy thử + đối chiếu số liệu trang 9 + lưu ảnh
python ghep_file.py --final    # tối ngày 7: ra lab03_final.py
python ghep_file.py --nop      # ngày 8: chép sang 04_Nop/lab03.py
```

Script tự xếp Task 1 → 14, giữ phần đầu file một lần, bỏ `plt.show()` thừa, và in danh sách lỗi đúng mẫu `[Lỗi] Task 8 – thiếu/sai tên biến ImJPG_DeleteGreen – @TV7 sửa` để dán thẳng vào nhóm. Ảnh kết quả lưu ở `03_BanGhep/anh_lab03_vN/` để TV4 so với Fig. 5, Fig. 6.

---

## Tin nhắn mẫu

### 1. Mở nhóm (ngày 1)

> Chào cả nhóm, mình là TV1 – nhóm trưởng Project 3 ĐSTT. Hạn nộp: **[ngày]**.
> 📁 Thư mục chung: [link]. Đề và ảnh ở `00_DeBai/`, phần ai nấy làm trong `01_Parts/partX.py`.
> 📄 Phân công xem file "Lộ trình & phân công" (trang 3–4).
> Việc hôm nay: (1) đọc đề, nhắn "OK TVx" xác nhận phần mình; (2) `pip install numpy matplotlib pillow`, chạy thử mở được `daylilies.jpg`; (3) họp online 15 phút lúc **[giờ]**.
> Mốc quan trọng: **cuối ngày 4** nộp `partX.py`. Báo trễ trước ít nhất 12 tiếng. Mỗi tối 21h nhắn 1 dòng tiến độ.

### 2. Báo bản ghép (ngày 5)

> Bản ghép đầu tiên: `03_BanGhep/lab03_v1.py`. TV4 chạy thử và đối chiếu Fig. 5, Fig. 6 giúp mình nhé.
> Lỗi script phát hiện (ai bị gắn tên thì sửa trong `partX.py` của mình, gửi lại trước **[giờ] ngày 6**):
> [dán danh sách lỗi]

### 3. Xác nhận đã nộp (ngày 8)

> Đã nộp `lab03.py` lúc [giờ] [ngày], ảnh xác nhận bên dưới. Cảm ơn cả nhóm! 🎉
