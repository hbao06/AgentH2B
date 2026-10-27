# AgentH2B - DataMate | Zalo AI Challenge 2026

Repo làm việc nhóm cho bài thi DataMate: xây dựng agent trả lời câu hỏi tiếng Việt trên dữ liệu có cấu trúc, chạy offline và xuất kết quả đúng định dạng của ban tổ chức.

## Bắt đầu

- Đọc [tóm tắt đề thi](docs/competition.md) trước khi thiết kế giải pháp.
- Đọc [quy ước làm việc nhóm](CONTRIBUTING.md) trước khi tạo nhánh hoặc pull request.
- Mã Python đặt trong `src/datamate/`; kiểm thử trong `tests/`.
- Dữ liệu, model weights, kết quả chạy và file nộp bài chỉ lưu cục bộ; xem `.gitignore`.

## Trạng thái

Repo mới được khởi tạo. Đã có baseline wiring và Docker skeleton; chưa có bộ dữ liệu chính thức hoặc planner/model inference. Bước tiếp theo là lấy Data, rulebook và Docker guideline sau khi đăng ký; sau đó chốt planner/executor và tạo baseline có đáp án.

## Baseline hiện tại

Repo đã có lớp ingest dùng lại ý tưởng Region/preview từ pipeline Excel cũ, hỗ trợ CSV, XLSX và SQLite; evaluator PA; chuẩn hóa kiểu đáp án; Docker skeleton; và CLI end-to-end. Baseline hiện chỉ phát `abstain` sau khi đọc/preview dữ liệu để kiểm tra wiring an toàn. Nhóm sẽ thay planner/executor ở bước tiếp theo, sau khi có schema thật.

Chạy kiểm thử:

```bash
pip install -e ".[dev]"
pytest
```

Chạy baseline cục bộ với dữ liệu thật:

```bash
PYTHONPATH=src python -m datamate --questions /data/questions.jsonl --data /data --output /result/submission.jsonl
```

Nguồn chính: [DataMate overview](https://challenge.zalo.ai/portal/datamate).

