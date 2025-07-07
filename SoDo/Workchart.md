# Biểu Đồ Quy Trình (Workflow Chart)

Các biểu đồ dưới đây mô tả các quy trình hoạt động chính của hệ thống Trắc Nghiệm Online.

## 1. Quy trình phát triển hệ thống

```mermaid
graph TD
    Start([Bắt đầu]) --> A1[Phân tích yêu cầu]
    A1 --> A2[Thiết kế hệ thống]
    A2 --> A3[Thiết kế cơ sở dữ liệu]
    A3 --> A4[Phát triển Server]
    A3 --> A5[Phát triển Client]

    A4 --> A6[Kết nối database]
    A5 --> A7[Thiết kế UI]
    A6 --> A8[Kiểm thử Server]
    A7 --> A9[Kiểm thử Client]

    A8 --> A10[Tích hợp hệ thống]
    A9 --> A10
    A10 --> A11[Kiểm thử toàn bộ hệ thống]
    A11 --> A12[Triển khai]
    A12 --> End([Kết thúc])

    style A1 fill:#f9d77e,stroke:#ff9900
    style A2 fill:#f9d77e,stroke:#ff9900
    style A3 fill:#f9d77e,stroke:#ff9900
    style A4 fill:#a2c4c9,stroke:#0066cc
    style A5 fill:#d4a6c8,stroke:#660066
    style A6 fill:#a2c4c9,stroke:#0066cc
    style A7 fill:#d4a6c8,stroke:#660066
    style A8 fill:#a2c4c9,stroke:#0066cc
    style A9 fill:#d4a6c8,stroke:#660066
    style A10 fill:#c9e1bd,stroke:#009900
    style A11 fill:#c9e1bd,stroke:#009900
    style A12 fill:#c9e1bd,stroke:#009900
```

## 2. Quy trình đăng ký và xác thực người dùng

```mermaid
graph TD
    Start([Người dùng mới]) --> C1[Khởi động ứng dụng]
    C1 --> C2[Nhập tên người dùng]

    C2 --> S1[Server nhận tên người dùng]
    S1 --> S2{Tên đã tồn tại\ntrong DB?}

    S2 -->|Có| S3[Lấy thông tin điểm số hiện tại]
    S2 -->|Không| S4[Tạo người dùng mới với điểm = 0]

    S3 --> S5[Lưu thông tin người dùng hiện tại]
    S4 --> S5

    S5 --> S6[Yêu cầu xác nhận bắt đầu game]
    S6 --> C3[Người dùng nhấn '0' để bắt đầu]
    C3 --> S7[Server bắt đầu trò chơi]

    S7 --> EndSuccess([Bắt đầu trò chơi])
```

## 3. Quy trình lưu trữ và truy xuất câu hỏi

```mermaid
graph TD
    Start([Bắt đầu]) --> A1[Quản trị viên thêm câu hỏi vào DB]
    A1 --> A2[Câu hỏi được phân loại theo chủ đề]
    A2 --> A3[Lưu trữ trong bảng questions]

    B1[Người dùng bắt đầu trò chơi] --> B2[Server truy vấn DB]
    B2 --> B3[Lấy ngẫu nhiên 10 câu hỏi]
    B3 --> B4[Phân tích câu hỏi]
    B4 --> B5[Định dạng câu hỏi để gửi tới client]
    B5 --> B6[Gửi từng câu hỏi theo trình tự]

    B6 --> End([Kết thúc])

    style A1 fill:#ffcccc,stroke:#ff6666
    style A2 fill:#ffcccc,stroke:#ff6666
    style A3 fill:#ffcccc,stroke:#ff6666
    style B1 fill:#ccccff,stroke:#6666ff
    style B2 fill:#ccccff,stroke:#6666ff
    style B3 fill:#ccccff,stroke:#6666ff
    style B4 fill:#ccccff,stroke:#6666ff
    style B5 fill:#ccccff,stroke:#6666ff
    style B6 fill:#ccccff,stroke:#6666ff
```

## 4. Quy trình tính điểm và cập nhật bảng xếp hạng

```mermaid
graph TD
    Start([Người chơi hoàn thành trò chơi]) --> A1[Server tính tổng số câu trả lời đúng]
    A1 --> A2[Mỗi câu đúng = 10 điểm]
    A2 --> A3[Tổng điểm = số câu đúng * 10]
    A3 --> A4[Cập nhật điểm vào database]

    A4 --> B1[Truy vấn top 5 người chơi điểm cao nhất]
    B1 --> B2[Gửi bảng xếp hạng tới client]

    B2 --> C1[Client lưu điểm hiện tại vào score_history.json]
    C1 --> C2[Hiển thị bảng xếp hạng tổng hợp]

    C2 --> End([Kết thúc])
```

## 5. Quy trình xử lý đồng thời nhiều người dùng

```mermaid
graph TD
    Start([Khởi động server]) --> A1[Server lắng nghe kết nối]
    A1 --> A2{Có kết nối\nmới?}

    A2 -->|Có| A3[Tạo thread mới xử lý client]
    A3 --> A4[Thread xử lý riêng biệt]
    A4 --> A2

    A2 -->|Không| A5[Server tiếp tục lắng nghe]
    A5 --> A2

    A4 --> B1[Gửi câu hỏi]
    B1 --> B2[Nhận câu trả lời]
    B2 --> B3[Xử lý đáp án]
    B3 --> B4{Còn câu hỏi?}

    B4 -->|Có| B1
    B4 -->|Không| B5[Gửi kết quả cuối]
    B5 --> B6[Cập nhật điểm vào DB]
    B6 --> B7[Đóng kết nối]
```

## 6. Quy trình triển khai hệ thống

```mermaid
graph TD
    Start([Bắt đầu triển khai]) --> A1[Cài đặt MySQL]
    A1 --> A2[Khởi tạo cơ sở dữ liệu]
    A2 --> A3[Chạy script sql_init.sql]

    A3 --> B1[Cài đặt Python và các thư viện]
    B1 --> B2[Cấu hình kết nối database trong server.py]

    B2 --> C1[Khởi động server]
    C1 --> C2[Kiểm tra server hoạt động]

    C2 --> D1[Tạo file thực thi client]
    D1 --> D2[Phân phối tới người dùng]

    D2 --> End([Hệ thống hoạt động])
```

## 7. Quy trình bảo trì hệ thống

```mermaid
graph TD
    Start([Bắt đầu bảo trì]) --> A1[Sao lưu cơ sở dữ liệu]
    A1 --> A2[Kiểm tra log lỗi]

    A2 --> B1{Có lỗi\nphát hiện?}

    B1 -->|Có| B2[Phân tích nguyên nhân]
    B2 --> B3[Khắc phục lỗi]
    B3 --> B4[Kiểm thử lại hệ thống]
    B4 --> C1[Cập nhật phiên bản mới]

    B1 -->|Không| C1

    C1 --> C2[Cập nhật câu hỏi mới]
    C2 --> C3[Làm sạch dữ liệu cũ]

    C3 --> End([Kết thúc bảo trì])
```

## 8. Quy trình mở rộng chức năng

```mermaid
graph TD
    Start([Bắt đầu mở rộng]) --> A1[Xác định chức năng mới]
    A1 --> A2[Phân tích yêu cầu]
    A2 --> A3[Thiết kế giải pháp]

    A3 --> B1[Mở rộng cơ sở dữ liệu]
    A3 --> B2[Phát triển chức năng server]
    A3 --> B3[Phát triển giao diện client]

    B1 --> C1[Tích hợp vào hệ thống]
    B2 --> C1
    B3 --> C1

    C1 --> C2[Kiểm thử chức năng mới]
    C2 --> C3[Triển khai cập nhật]

    C3 --> End([Hoàn thành mở rộng])

    style A1 fill:#ffffcc,stroke:#ffcc00
    style A2 fill:#ffffcc,stroke:#ffcc00
    style A3 fill:#ffffcc,stroke:#ffcc00
    style B1 fill:#ccffcc,stroke:#00cc00
    style B2 fill:#ccffcc,stroke:#00cc00
    style B3 fill:#ccffcc,stroke:#00cc00
    style C1 fill:#ccffff,stroke:#00cccc
    style C2 fill:#ccffff,stroke:#00cccc
    style C3 fill:#ccffff,stroke:#00cccc
```
