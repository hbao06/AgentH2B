# Tổng hợp đề thi DataMate - Zalo AI Challenge 2026

Cập nhật: 27/10/2026 (GMT+7). Nguồn: [trang DataMate chính thức](https://challenge.zalo.ai/portal/datamate), các mục Description, Evaluation, Data, Rule và Submission Guidance. Đây là bản tóm tắt cho nhóm; khi có khác biệt, ưu tiên nội dung mới nhất trên portal và tài liệu của ban tổ chức.

## 1. Description - Bài toán

Xây dựng AI agent trả lời câu hỏi tiếng Việt thông thường trên dữ liệu có cấu trúc của một doanh nghiệp. Dữ liệu có thể nằm trong một hoặc nhiều tệp CSV, Excel (`.xlsx`) hoặc SQLite (`.sqlite`). Agent cần trả lời đúng hoặc xác định rằng dữ liệu không đủ để trả lời. Ngữ cảnh dữ liệu tập trung vào doanh nghiệp nhỏ ở Việt Nam, nhưng năng lực cần xây dựng là hỏi đáp tổng quát trên bảng.

Mỗi câu hỏi có:

- Data package cho một doanh nghiệp: các tệp dữ liệu và `README.md` mô tả doanh nghiệp.
- `question`: câu hỏi tiếng Việt.
- `as_of_date`: ngày được coi là "hôm nay" để giải các cụm như "tháng này", "tuần rồi", "cùng kỳ năm ngoái".
- Rulebook và lịch dương-âm dùng chung cho các doanh nghiệp trong cùng split.

Đầu ra là một đáp án có kiểu `number`, `percent`, `string`, `date`, `boolean`, `list`, `table`, `unanswerable` hoặc `abstain`. `unanswerable` nghĩa là dữ liệu không chứa thông tin cần thiết; `abstain` nghĩa là agent chọn không trả lời.

Ví dụ chính thức, một dòng trong `questions.jsonl` và dòng tương ứng trong `submission.jsonl`:

```json
{"id":"q_06de33fa21cc","business_id":"biz_118","question":"sp bán dc nhiều nhất tuần rồi là gì","as_of_date":"2026-03-04"}
```

```json
{"id":"q_06de33fa21cc","type":"string","answer":"Xi măng Hà Tiên PCB40 bao 50kg"}
```

## 2. Evaluation - Chấm điểm

Mỗi câu được chấm đúng, sai hoặc abstain. Đúng khi **cả kiểu đáp án lẫn giá trị** khớp tham chiếu; không có điểm một phần. Thiếu dòng kết quả hoặc trả `abstain` được tính là abstain.

| Kiểu | Quy tắc đối sánh quan trọng |
| --- | --- |
| `number` | Khớp chính xác; giá trị tham chiếu là số nguyên (VND, số lượng) hoặc được làm tròn 2 chữ số thập phân. |
| `percent` | Giá trị tính theo phần trăm, làm tròn 2 chữ số thập phân; dấu âm/dương phải đúng. |
| `string` | Chuẩn hóa Unicode NFC, chữ thường, thay ký tự không phải chữ/số/khoảng trắng bằng khoảng trắng, cắt/gộp khoảng trắng; **không bỏ dấu tiếng Việt**. Tham chiếu chấp nhận các cách viết tên và mã xuất hiện trong dữ liệu doanh nghiệp. |
| `date` | Khớp chính xác `yyyy-mm-dd`; nếu hỏi theo tháng thì `yyyy-mm`. |
| `boolean` | `true` hoặc `false`, khớp chính xác. |
| `list` | Có thứ tự; đối sánh từng vị trí. Thứ tự theo câu hỏi, hoặc theo mặc định rulebook. |
| `table` | Đối sánh tên cột sau chuẩn hóa; nếu tên không khớp thì theo vị trí. Các dòng được so như một tập hợp. Ô tên theo quy tắc `string`, ô số theo `number`. |
| `unanswerable` | Chỉ đúng nếu đáp án tham chiếu cũng là `unanswerable`. |
| `abstain` | Luôn tính là abstain, không phụ thuộc đáp án tham chiếu. |

Penalized Accuracy: `PA = (số câu đúng - số câu sai) / tổng số câu`; abstain đóng góp 0. Trả một giá trị cho câu `unanswerable` được tính là sai. Mọi câu có cùng trọng số. Hòa điểm được phân bằng tổng thời gian inference trong lần chạy lại của ban tổ chức, sau đó thời điểm nộp sớm hơn.

Câu hỏi xếp hạng: dùng tiêu chí nêu trong câu hỏi, nếu không có thì dùng mặc định rulebook; sắp giảm dần trên **đơn hàng hợp lệ**. Giá trị bằng nhau thì sắp theo mã tăng dần. Câu có đồng hạng ở ranh giới top-k (hoặc hạng 1 với câu "nhất") không nằm trong test set. Nếu ít hơn k ứng viên thì trả tất cả.

## 3. Data - Hiện chưa truy cập được

Khi xem mục Data, portal hiện thông báo **"Please complete your registration to view Data."** Vì vậy repo này **chưa xác minh** cấu trúc thư mục, schema, các file train/public test, rulebook, lịch dương-âm, hướng dẫn Docker và format chi tiết của bộ dữ liệu. Không nên suy đoán đường dẫn hoặc thiết kế parser theo tên tệp chưa được công bố.

Việc cần bổ sung sau khi nhóm hoàn tất đăng ký và tải dữ liệu:

- Cây thư mục và schema mẫu của data package; quan hệ giữa các bảng/tệp.
- Cấu trúc chính xác của `questions.jsonl`, rulebook, lịch dương-âm và các trường đáp án.
- Cách mount `/data`, nội dung Docker guideline, quy tắc log và ví dụ submission chính thức.
- Giấy phép và phạm vi sử dụng từng tập dữ liệu.

Không đưa data package, public/private test set, model weights hay submission vào Git.

## 4. Rule - Ràng buộc kỹ thuật

- Cuộc thi có public test, nộp giải pháp cuối cùng, rồi private test. Điểm chung cuộc là điểm ban tổ chức **chạy lại Docker image** trên private test.
- Model dùng lúc inference phải có weights công khai trước **01/10/2026** và giấy phép cho phép sử dụng. Tổng số tham số của **tất cả** model inference (LLM, embedding, reranker, classifier; tính cả MoE) không vượt **15 tỷ**. Được quantize và fine-tune; khai báo model trong README giải pháp.
- Inference hoàn toàn offline trong Docker: không API LLM, không download, không truy cập mạng. Hệ thống tự động, không cần người can thiệp. Cấm hard-code đáp án hoặc logic dựa trên ID câu hỏi/doanh nghiệp.
- Được sinh và chạy code trong container. `/data` được mount read-only; file tạm ghi ở nơi khác.
- Được dùng train data, dữ liệu tự tổng hợp và dữ liệu/model công khai. **Không** dùng public/private test để train hay thu thập đáp án test.
- Máy tham chiếu: **2 x NVIDIA RTX 5090 (32 GB VRAM mỗi GPU), RAM 512 GB**. Phải xử lý hết private test trong **6 giờ**, kể cả load model. Docker guideline sẽ quy định base image/CUDA; trang hiện nêu Blackwell cần CUDA >= 12.8 và build PyTorch/vLLM phù hợp.
- Kết quả cần có tính lặp lại: `|PA(upload) - PA(re-run)| <= 0.03`. Nếu vượt, ban tổ chức có thể kiểm tra log, chạy lại và yêu cầu giải trình; không giải thích được có thể bị loại. Nếu chạy quá 6 giờ hoặc dừng sớm, chỉ các dòng đã ghi vào `/result/submission.jsonl` mới được chấm, phần còn lại tính abstain.
- Tư cách/đội thi theo [thể lệ chung](https://challenge.zalo.ai/regulations); tài liệu này chưa trích chi tiết quy mô đội từ PDF thể lệ chung.

## 5. Submission Guidance - Mốc nộp bài

Tất cả mốc giờ dưới đây là **GMT+7**, năm **2026**.

| Mốc | Yêu cầu |
| --- | --- |
| 26/10-16/11 | Public test: chạy bộ public, upload `submission.jsonl` trên portal. Tối đa **5 lần/ngày**, reset cuối ngày. Bảng xếp hạng public chỉ phục vụ phát triển. |
| 16/11, 23:59 | Nộp giải pháp hoàn chỉnh gồm code train, code inference và data dưới dạng Docker package. Cung cấp checksum và link Google Drive công khai cho ban tổ chức tải. Tối đa **2 lần nộp**, bản cuối cùng được đánh giá. |
| 20/11, 09:00 | Ban tổ chức phát private test. Nhóm chạy giải pháp **đã đóng băng** trên tập này. |
| 23/11, 23:59 | Hạn upload `submission.jsonl` private. Ban tổ chức sau đó chạy lại image, xem code và kiểm tra gian lận. |
| 02/12 | Công bố top 2. |

Theo Rule, ban tổ chức mount test set tại `/data` và lấy `/result/submission.jsonl` từ container. Cần đối chiếu Docker guideline chính thức khi Data mở quyền truy cập.

## Việc nhóm cần chốt sớm

1. Hoàn tất đăng ký, lưu tài liệu Data và Docker guideline; cập nhật mục 3 và xác nhận các mẫu JSON thật.
2. Chia người phụ trách: data/schema và rulebook; agent/truy vấn; evaluation/kiểm thử; Docker/inference. Mỗi phần cần có người review chéo.
3. Dựng baseline đo được PA và thời gian chạy trước khi thử model/phương pháp phức tạp hơn.
