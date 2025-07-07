# Biểu Đồ Luồng (Flow Chart)

Các biểu đồ dưới đây mô tả luồng hoạt động của các thành phần chính trong hệ thống Trắc Nghiệm Online.

## 1. Luồng hoạt động tổng quát của hệ thống

```mermaid
flowchart TD
    Start([Bắt đầu]) --> S1[Khởi động Server]
    Start --> C1[Khởi động Client]

    S1 --> S2[Lắng nghe kết nối]
    C1 --> C2[Kết nối tới Server]

    C2 --> C3{Kết nối\nthành công?}
    C3 -->|Không| C4[Hiển thị lỗi và thoát]
    C3 -->|Có| C5[Nhập tên người chơi]

    S2 --> S3[Chấp nhận kết nối]
    S3 --> S4[Tạo thread xử lý client mới]
    S4 --> S5[Gửi lời chào và yêu cầu tên]

    C5 --> C6[Gửi tên tới server]
    S5 --> S6[Nhận tên người chơi]

    S6 --> S7[Kiểm tra/tạo người chơi trong DB]
    S7 --> S8[Yêu cầu tín hiệu bắt đầu]

    S8 --> C7[Nhận yêu cầu bắt đầu]
    C7 --> C8[Gửi tín hiệu bắt đầu]

    C8 --> S9[Nhận tín hiệu bắt đầu]
    S9 --> S10[Lấy câu hỏi từ database]
    S10 --> GameLoop[Vòng lặp game]

    GameLoop --> End([Kết thúc])
```

## 2. Vòng lặp trò chơi (Game Loop)

```mermaid
flowchart TD
    Start([Bắt đầu vòng lặp]) --> S1[Server lấy câu hỏi]
    S1 --> S2[Server gửi câu hỏi]
    S2 --> C1[Client nhận và hiển thị câu hỏi]
    C1 --> C2[Client bắt đầu đếm ngược]

    C2 --> C3{Người dùng\nchọn đáp án?}
    C3 -->|Có| C4[Gửi đáp án tới server]
    C3 -->|Không| C5{Hết thời gian?}
    C5 -->|Không| C3
    C5 -->|Có| C6[Hiển thị thông báo hết giờ]
    C6 --> S5

    C4 --> S3[Server kiểm tra đáp án]
    S3 -->|Đúng| S4A[Tăng điểm]
    S3 -->|Sai| S4B[Giữ nguyên điểm]

    S4A --> S5[Server gửi kết quả]
    S4B --> S5

    S5 --> C7[Client hiển thị kết quả]
    C7 --> S6{Còn câu hỏi?}

    S6 -->|Có| S1
    S6 -->|Không| FinalProcess[Xử lý kết thúc]

    FinalProcess --> S7[Server cập nhật điểm vào DB]
    S7 --> S8[Server lấy bảng xếp hạng]
    S8 --> S9[Server gửi kết quả cuối cùng]

    S9 --> C8[Client hiển thị kết quả cuối]
    C8 --> C9[Client lưu điểm vào file JSON]
    C9 --> C10[Client hiển thị bảng xếp hạng]

    C10 --> End([Kết thúc vòng lặp])
```

## 3. Xử lý dữ liệu của Client

```mermaid
flowchart TD
    Start([Bắt đầu]) --> R1[Nhận dữ liệu từ socket]
    R1 --> R2[Thêm vào buffer]
    R2 --> P1{Có 'Trò chơi\nkết thúc!' trong\nbuffer?}

    P1 -->|Có| P2[Hiển thị kết quả cuối]
    P2 --> P3[Lưu điểm số]
    P3 --> P4[Xóa buffer]
    P4 --> End1([Kết thúc])

    P1 -->|Không| P5{Đang đợi\nkết quả đáp án?}

    P5 -->|Có| P6{Có 'Đáp án đúng!'\ntrong buffer?}
    P6 -->|Có| P7[Hiển thị thông báo đúng]
    P7 --> P8[Cập nhật điểm số]
    P8 --> P9[Đánh dấu đợi câu hỏi mới]
    P9 --> P10[Hẹn giờ chuyển câu hỏi]
    P10 --> End2([Tiếp tục])

    P6 -->|Không| P11{Có 'Đáp án sai!'\ntrong buffer?}
    P11 -->|Có| P12[Hiển thị thông báo sai]
    P12 --> P9
    P11 -->|Không| End3([Tiếp tục])

    P5 -->|Không| P13{Đang đợi\ncâu hỏi?}
    P13 -->|Có| P14{Có câu hỏi\nmới trong buffer?}

    P14 -->|Có| P15[Phân tích và hiển thị câu hỏi]
    P15 --> P16[Bắt đầu đếm ngược]
    P16 --> P17[Đánh dấu đang đợi đáp án]
    P17 --> End4([Tiếp tục])

    P14 -->|Không| End5([Tiếp tục])
    P13 -->|Không| End6([Tiếp tục])
```

## 4. Đồng bộ hóa giữa các Thread

```mermaid
sequenceDiagram
    participant MT as Main Thread
    participant LT as Listen Thread
    participant S as Server
    participant DB as Database

    MT->>S: Kết nối
    S->>MT: Yêu cầu nhập tên
    MT->>S: Gửi tên người chơi
    S->>DB: Kiểm tra/tạo người chơi
    S->>MT: Yêu cầu bắt đầu
    MT->>S: Gửi tín hiệu bắt đầu
    S->>DB: Lấy câu hỏi

    S->>LT: Gửi câu hỏi
    LT->>LT: Thêm dữ liệu vào buffer
    LT-->>MT: Gửi sự kiện để xử lý buffer
    MT->>MT: Phân tích câu hỏi
    MT->>MT: Hiển thị câu hỏi
    MT->>MT: Bắt đầu đếm ngược

    MT->>S: Gửi đáp án
    S->>LT: Gửi kết quả
    LT->>LT: Thêm kết quả vào buffer
    LT-->>MT: Gửi sự kiện để xử lý buffer
    MT->>MT: Hiển thị kết quả

    Note over MT,LT: Quá trình lặp lại cho các câu hỏi

    S->>LT: Gửi kết quả cuối cùng
    LT->>LT: Thêm kết quả vào buffer
    LT-->>MT: Gửi sự kiện để xử lý buffer
    MT->>MT: Hiển thị kết quả cuối cùng
    MT->>MT: Lưu điểm số vào file JSON
```

## 5. Luồng xử lý timeout

```mermaid
flowchart TD
    Start([Bắt đầu]) --> T1[Hiển thị câu hỏi]
    T1 --> T2[Bắt đầu đồng hồ đếm ngược]

    T2 --> T3{Thời gian > 0?}
    T3 -->|Có| T4[Giảm thời gian 1 giây]
    T4 --> T5[Cập nhật hiển thị thời gian]
    T5 --> T6{Người dùng đã\nchọn đáp án?}

    T6 -->|Có| T7[Dừng đồng hồ]
    T7 --> T8[Xử lý gửi đáp án]
    T8 --> End1([Kết thúc])

    T6 -->|Không| Wait[Chờ 1 giây]
    Wait --> T3

    T3 -->|Không| T9[Hiển thị thông báo hết giờ]
    T9 --> T10[Tự động chuyển câu hỏi tiếp theo]
    T10 --> End2([Kết thúc])
```

## 6. Quá trình xử lý đáp án

```mermaid
flowchart TD
    Start([Bắt đầu]) --> UA1[Người dùng chọn đáp án]
    UA1 --> UA2[Client hiển thị đáp án đã chọn]
    UA2 --> UA3[Người dùng nhấn nút Gửi]

    UA3 --> UA4{Đã chọn\nđáp án?}
    UA4 -->|Không| UA5[Hiển thị thông báo cảnh báo]
    UA5 --> UA1

    UA4 -->|Có| UA6[Gửi đáp án tới server]
    UA6 --> UA7[Vô hiệu hóa nút gửi và lựa chọn]

    UA7 --> SA1[Server nhận đáp án]
    SA1 --> SA2{Đáp án đúng?}

    SA2 -->|Có| SA3[Server gửi 'Đáp án đúng!']
    SA3 --> CA1[Client nhận kết quả]
    CA1 --> CA2[Hiển thị overlay 'CHÍNH XÁC!']
    CA2 --> CA3[Cập nhật điểm số và thống kê]

    SA2 -->|Không| SA4[Server gửi 'Đáp án sai!']
    SA4 --> CA4[Client nhận kết quả]
    CA4 --> CA5[Hiển thị overlay 'SAI RỒI!']
    CA5 --> CA6[Hiển thị đáp án đúng]
    CA6 --> CA7[Cập nhật thống kê]

    CA3 --> CA8[Tự động chuyển câu hỏi sau 2.5 giây]
    CA7 --> CA8

    CA8 --> End([Kết thúc])
```
