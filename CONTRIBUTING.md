# Làm việc nhóm

## Clone và chạy local

```bash
git clone <URL-GITHUB-CUA-NHOM>
cd datamate-2026
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -e ".[dev]"
pytest
```

Khi có dữ liệu chính thức, đặt dữ liệu cục bộ trong `data/` theo hướng dẫn
của ban tổ chức. Thư mục này đã bị Git bỏ qua; không commit dữ liệu cuộc thi.

## Quy trình

1. Tạo issue ngắn gọn cho mỗi việc: mục tiêu, đầu vào, đầu ra và cách kiểm tra.
2. Tạo nhánh từ `main` theo mẫu `feature/<ten-viec>`, `fix/<ten-loi>` hoặc `docs/<ten-viec>`.
3. Mỗi pull request mô tả thay đổi và lệnh/kết quả kiểm tra; ít nhất một thành viên khác review trước khi merge.
4. Giữ `main` luôn chạy được. Không đưa kết quả thử nghiệm chưa kiểm chứng vào code như một quy tắc nghiệp vụ.

## Dữ liệu và tài nguyên

- Không commit data package, câu hỏi test, answer/submission, model weights, checkpoint, log chứa dữ liệu hay credential.
- Ghi nguồn và giấy phép của từng model/dataset công khai trong README của giải pháp trước khi nộp.
- Chỉ dùng train data cho huấn luyện. Theo Rule của cuộc thi, không dùng public/private test data để train hay thu thập đáp án test.
- Khi chia sẻ kết quả, ghi rõ tập đánh giá, commit, cấu hình model, thời gian chạy và cách tính điểm.

## Tiêu chuẩn thay đổi

- Code xử lý dữ liệu cần kiểm tra trường hợp rỗng, sai kiểu, thời gian tương đối và `unanswerable`.
- Thay đổi định dạng đầu ra cần đối chiếu lại [competition.md](docs/competition.md) và ví dụ chính thức.
- Không thêm API online vào đường inference: Docker chấm điểm chạy khi mạng bị vô hiệu hóa.
