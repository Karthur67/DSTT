# ĐSTT – Project 3: Matrix multiplication, inversion, and photo filters

Kho code chung của nhóm (7 người). Bài nộp: `lab03.py` + báo cáo PDF.

## Cài đặt
```
pip install -r requirements.txt
```

## Thư mục
| Thư mục / file | Dùng để | Ai sửa |
|---|---|---|
| `00_DeBai/` | Đề PDF và `daylilies.jpg` | TV1 |
| `01_Parts/` | `part1.py` … `part7.py` – code của từng người | Mỗi người chỉ file của mình |
| `02_Anh/` | Ảnh kết quả, tên `TVx_TaskY.png` | Mỗi người |
| `03_BanGhep/` | Bản ghép `lab03_v1.py`, `lab03_final.py` | Chỉ TV1 |
| `04_Nop/` | Bài nộp cuối | Chỉ TV1 |
| `05_DuLieuThem/` | Ảnh thêm cho báo cáo, tên `TVx_anh1.jpg`, ghi nguồn | TV4, TV6 |
| `bao_cao/` | Báo cáo LaTeX | TV5 tổng hợp |
| `ghep_file.py` | Ghép 7 phần thành `lab03.py` | TV1 chạy |
| `vi_du_them.py` | Tạo hình, bảng cho Phần 4 báo cáo | TV6 chạy |

## Cách nộp code
1. Vào `01_Parts/` → **Add file → Upload files** → kéo `partX.py` của mình vào.
2. Ghi mô tả, ví dụ `TV7: Task 8, 12` → **Commit changes**.
3. Sửa lỗi: upload lại file cùng tên để ghi đè.

## Quy ước code
- Đầu file dán phần đầu file chung của TV2: chép `01_Parts/part2.py` từ dòng đầu đến hết `m, n, l = ImJPG.shape` (import, `to_uint8`, `apply_filter_loop`, `show`, đọc ảnh). Nhóm chỉ dùng `apply_filter_loop` để lọc.
- Mỗi task mở đầu bằng `# %% Task X`; dùng đúng tên biến trong đề.
- **BẮT BUỘC:** mọi task lọc bằng ma trận (Task 4, 5, 6, 7, 8, 10, 11, 12, 13) **chỉ được dùng `apply_filter_loop(ImJPG, M)`**. **Không** dùng `apply_filter`, **không** tự nhân ma trận cho cả ảnh (`img @ M.T`, `np.dot`). Phần đầu file **không được còn hàm `apply_filter`**. `ghep_file.py` sẽ báo **[Lỗi]** kèm tên người nếu vi phạm. Không dùng `.astype(np.uint8)` trực tiếp.
- Câu trả lời tiếng Anh dạng `# Q1:` / `# A1:` ngay dưới task tương ứng.
