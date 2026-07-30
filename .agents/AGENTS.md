# Quy tắc Thiết kế Biểu đồ Python (Bắt buộc)

Khi tạo bất kỳ biểu đồ nào bằng Python (matplotlib, seaborn, v.v.), **bắt buộc** tuân thủ các quy tắc sau:

## 1. Palette Màu Chuyên nghiệp
- Dùng Seaborn palette `'muted'` hoặc `'Set2'`, hoặc các mã HEX hiện đại:
  - Navy: `#1b365d`
  - Teal: `#008080`
  - Red: `#d9534f`
- **KHÔNG** dùng màu gốc chói (red, blue, green nguyên bản).

## 2. Tối giản (Data-to-Ink Ratio)
- Luôn xóa 2 đường viền Top và Right:
  ```python
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ```
- Bỏ bớt đường lưới hoặc chỉnh `alpha=0.2` cho gridlines.

## 3. Typography
- Tiêu đề: **in đậm**, `fontsize=14`, nêu rõ kết luận/insight (không chỉ mô tả tên chỉ số).
- Nhãn trục (xlabel, ylabel): `fontsize=10`, màu xám đậm `#333333`.

## 4. Data Labels
- Luôn hiển thị giá trị cụ thể trên đỉnh cột/điểm dữ liệu chính.
- Format rõ ràng: số tiền dùng `$`, phần trăm dùng `%`.

## 5. Kích thước & Độ Phân giải
- `figsize=(10, 5)` hoặc `(12, 6)`
- `dpi=300`
