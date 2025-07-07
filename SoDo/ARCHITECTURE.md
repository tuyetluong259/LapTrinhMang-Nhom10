# Kiến Trúc Hệ Thống

## Tổng quan

Hệ thống Trắc Nghiệm Online được thiết kế theo mô hình client-server, sử dụng kết nối socket TCP/IP để giao tiếp giữa client và server.

```mermaid
graph TD
    A[Client - GUI] <-->|Socket| B[Server]
    B <-->|MySQL| C[(Database)]
    A -->|JSON| D[score_history.json]

    style A fill:#f9d77e,stroke:#ff9900,stroke-width:2px
    style B fill:#a2c4c9,stroke:#0066cc,stroke-width:2px
    style C fill:#c9e1bd,stroke:#009900,stroke-width:2px
    style D fill:#d4a6c8,stroke:#660066,stroke-width:2px
```

## Luồng dữ liệu

```mermaid
sequenceDiagram
    participant User as Người dùng
    participant Client as Client App
    participant Server as Server
    participant DB as Database

    User->>Client: Khởi động app
    Client->>Server: Kết nối socket
    Server-->>Client: Yêu cầu nhập tên
    User->>Client: Nhập tên người chơi
    Client->>Server: Gửi tên
    Server->>DB: Kiểm tra/tạo user
    Server-->>Client: Yêu cầu bắt đầu game
    User->>Client: Bấm bắt đầu (0)
    Client->>Server: Gửi tín hiệu bắt đầu
    Server->>DB: Lấy 10 câu hỏi ngẫu nhiên

    loop 10 câu hỏi
        Server-->>Client: Gửi câu hỏi
        Client-->>User: Hiển thị câu hỏi + hẹn giờ
        User->>Client: Chọn đáp án
        Client->>Server: Gửi đáp án
        Server-->>Client: Kết quả đúng/sai
        Client-->>User: Hiển thị kết quả
    end

    Server->>DB: Cập nhật điểm người chơi
    Server->>DB: Lấy bảng xếp hạng top 5
    Server-->>Client: Gửi kết quả và bảng xếp hạng
    Client->>User: Hiển thị kết quả cuối
    Client->>Client: Lưu điểm vào score_history.json
```

## Giao tiếp Client-Server

Giao thức giao tiếp giữa client và server là các tin nhắn văn bản qua giao thức TCP, với các định dạng cụ thể:

1. **Bắt đầu kết nối**:

   - Server -> Client: "Chào mừng đến với trò chơi trắc nghiệm!\nXin mời nhập tên của bạn:\n"
   - Client -> Server: "[Tên người chơi]"
   - Server -> Client: "Xin chào [Tên]! Để bắt đầu trò chơi, nhấn phím 0 và Enter:\n"
   - Client -> Server: "0"

2. **Gửi câu hỏi**:

   - Server -> Client:
     ```
     Câu {số thứ tự}:
     Chủ đề: {tên chủ đề}
     {nội dung câu hỏi}
     A. {đáp án A}
     B. {đáp án B}
     C. {đáp án C}
     D. {đáp án D}
     Nhập đáp án (A/B/C/D):
     ```

3. **Nhận đáp án và gửi kết quả**:

   - Client -> Server: "[A/B/C/D]"
   - Server -> Client (đáp án đúng): "Đáp án đúng!\n\n"
   - Server -> Client (đáp án sai): "Đáp án sai! Đáp án đúng là: {đáp án đúng}\n\n"

4. **Kết thúc trò chơi**:

   - Server -> Client:

     ```
     Trò chơi kết thúc! Điểm của bạn: {điểm}/10

     === BẢNG XẾP HẠNG TOP 5 ===
     1. {tên} - {điểm} điểm
     2. {tên} - {điểm} điểm
     ...

     Cảm ơn bạn đã chơi!
     ```

## Xử lý đồng thời

```mermaid
flowchart TD
    subgraph Server
        A[Server]
        A -->|"socket.accept()"| MainThread["Thread Main"]
        A -->|"handle_client"| Client1["Thread Client 1"]
        A -->|"handle_client"| Client2["Thread Client 2"]
        A -->|"handle_client"| ClientN["Thread Client n"]

        MainThread -->|"socket.accept()"| Waiting["Chờ kết nối mới"]
        Client1 -->|"handle_client"| Handle1["Xử lý client 1"]
        Client2 -->|"handle_client"| Handle2["Xử lý client 2"]
        ClientN -->|"handle_client"| HandleN["Xử lý client n"]
    end
```

Phía server sử dụng xử lý đa luồng để hỗ trợ nhiều người chơi cùng lúc. Mỗi kết nối client được xử lý bởi một luồng riêng biệt.

## Luồng dữ liệu phía Client

```mermaid
flowchart TD
    A[Main Thread] -->|GUI Events| B[Xử lý Interface]
    A --> C[Listen Thread]
    C -->|socket.recv| D[Nhận dữ liệu]
    D -->|Gửi tới main thread| E[Xử lý qua _process_data_from_buffer]
    E --> F{Loại dữ liệu}
    F -->|Câu hỏi| G[Hiển thị câu hỏi]
    F -->|Kết quả| H[Hiển thị kết quả]
    F -->|Kết thúc| I[Hiển thị kết quả cuối]
    B -->|select_answer| J[Chọn đáp án]
    B -->|send_answer| K[Gửi đáp án]
    B -->|start_timer| L[Đếm ngược thời gian]
```

Phía client sử dụng hai luồng:

1. **Main Thread**: Xử lý giao diện người dùng và sự kiện
2. **Listen Thread**: Chuyên lắng nghe dữ liệu từ server và gửi tới main thread để xử lý

## Lưu trữ dữ liệu

```mermaid
graph LR
    A[Server] -->|MySQL| B[(Database)]
    A -->|MySQL| C[(Questions)]
    A -->|MySQL| D[(Users)]
    A -->|MySQL| E[(Topics)]

    F[Client] -->|JSON| G[score_history.json]
```

Hệ thống sử dụng hai cơ chế lưu trữ:

1. **MySQL**: Lưu trữ câu hỏi, thông tin người dùng và điểm số phía server
2. **JSON**: Lưu trữ lịch sử điểm số cục bộ phía client
