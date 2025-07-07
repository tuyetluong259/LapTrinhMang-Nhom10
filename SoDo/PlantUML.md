# Biểu Đồ UML (Mermaid Version)

Bộ sơ đồ dưới đây mô tả hệ thống Trắc Nghiệm Online bằng cú pháp **Mermaid** (thay thế hoàn toàn cho PlantUML cũ). Bạn có thể copy-paste trực tiếp vào bất kỳ công cụ nào hỗ trợ Mermaid để xem.

---

## 1. Class Diagram

```mermaid
classDiagram
direction LR

class Server {
  -HOST: str = "0.0.0.0"
  -PORT: int = 9999
  -DB_CONNECTION: Connection
  +__init__()
  +start_server()
  +handle_client(client_socket, address)
  +close_server()
}

class DatabaseManager {
  -connection: Connection
  +__init__(host, user, password, db)
  +connect()
  +disconnect()
  +get_or_create_user(name) Tuple<int,int>
  +get_questions(limit=10) List<Dict>
  +update_score(user_id, score)
  +get_leaderboard(limit=5) List<Dict>
}

class QuestionHandler {
  +format_question(index, question): str
  +check_answer(answer, correct_answer): bool
  +format_result(user_name, score): str
}

class QuizClient {
  -HOST: str = "127.0.0.1"
  -PORT: int = 9999
  -socket: Socket
  -buffer: str
  -score: int
  -player_name: str
  -time_remaining: int
  -timer_running: bool
  -expecting_question: bool
  +__init__(master)
  +setup_ui()
  +start_listening()
  +send_answer(answer)
  +process_data_from_buffer()
  +show_overlay(message, color, sub_message)
  +start_timer()
  +update_timer()
  +time_up()
  +close_connection()
}

class GUI {
  -master: TkinterRoot
  -frame_main: Frame
  -frame_question: Frame
  -label_question: Label
  -radio_buttons: List<RadioButton>
  -button_submit: Button
  -label_timer: Label
  -label_score: Label
  +__init__(master)
  +create_widgets()
  +set_question(question_text)
  +clear_selection()
  +disable_inputs()
  +enable_inputs()
  +update_score(score)
  +update_timer(time)
}

class ScoreHistory {
  -history_file: str
  +__init__(filename="score_history.json")
  +load_history() List<Dict>
  +save_score(player_name, score)
  +get_statistics() Dict
}

class Users
class Topics
class Questions

Server --> DatabaseManager
Server --> QuestionHandler
QuizClient --> GUI
QuizClient --> ScoreHistory
DatabaseManager --> Users
DatabaseManager --> Questions
DatabaseManager --> Topics
Questions --> Topics
```

---

## 2. Sequence Diagram

```mermaid
sequenceDiagram
actor User
participant Client
participant Server
participant DB as Database

%% Kết nối & xác thực
User ->> Client: Khởi động ứng dụng
Client ->> Server: Kết nối
Server -->> Client: Gửi chào mừng
Client ->> User: Nhập tên
User  ->> Client: Nhập tên xong
Client ->> Server: Gửi tên
Server ->> DB: Kiểm tra/tạo user
DB     -->> Server: Trả kết quả
Server ->> Client: Yêu cầu nhấn 0
Client ->> User: Hiển thị yêu cầu
User   ->> Client: Nhấn 0
Client ->> Server: Gửi tín hiệu bắt đầu

%% Vòng lặp trò chơi
Server ->> DB: Lấy 10 câu hỏi
DB     -->> Server: Danh sách
loop 10 lần
    Server ->> Client: Gửi câu hỏi
    Client ->> User: Hiển thị + đếm ngược
    alt Người dùng chọn đáp án
        User   ->> Client: Chọn A/B/C/D
        Client ->> Server: Gửi đáp án
    else Hết thời gian
        Client ->> Server: Gửi đáp án trống
    end
    Server ->> Server: Kiểm tra đáp án
    alt Đúng
        Server ->> Client: Thông báo đúng
        Client ->> User: Overlay "CHÍNH XÁC!"
    else Sai
        Server ->> Client: Thông báo sai
        Client ->> User: Overlay "SAI RỒI!"
    end
end

%% Kết thúc
Server ->> DB: Cập nhật điểm
Server ->> DB: Lấy BXH
DB     -->> Server: BXH
Server ->> Client: Gửi kết quả cuối
Client ->> User: Hiển thị
Client ->> Client: Lưu JSON
```

---

## 3. Activity Diagram

```mermaid
flowchart TD
    A0([Start]) --> A1[Khởi động Server]
    A1 --> A2[Lắng nghe kết nối]

    subgraph Client
        C1[Client kết nối] --> C2{Kết nối OK?}
        C2 -- Yes --> C3[Nhập tên] --> C4[Gửi tên]
        C2 -- No  --> C5[Hiển thị lỗi] --> C6([Stop])
    end

    subgraph Server
        S1[Chấp nhận kết nối] --> S2[Tạo thread]
        S2 --> S3[Gửi chào & yêu cầu tên]
        S3 --> S4[Nhận tên]
        S4 --> S5[Kiểm tra/tạo user]
        S5 --> S6[Yêu cầu bắt đầu]
    end

    C4 -.-> S4
    S6 -.-> C7[Client gửi '0']
    C7 -.-> S7[Server lấy câu hỏi]

    S7 --> LoopStart

    subgraph GameLoop
        LoopStart --> Q1[Server gửi câu hỏi]
        Q1 --> C8[Client hiển thị]
        C8 --> C9[Đếm ngược]
        C9 --> D1{User trả lời?}
        D1 -- Yes --> C10[Gửi đáp án]
        D1 -- No  --> C11[Hết giờ] --> C10
        C10 --> S8[Kiểm tra]
        S8 --> D2{Đúng?}
        D2 -- Yes --> S9[Gửi đúng] --> C12[Overlay đúng]
        D2 -- No  --> S10[Gửi sai]  --> C13[Overlay sai]
        C12 --> NextQ
        C13 --> NextQ
        NextQ{Còn câu hỏi?} -- Yes --> LoopStart
        NextQ -- No --> Exit
    end

    Exit --> S11[Cập nhật điểm] --> S12[Lấy BXH]
    S12 --> C14[Hiển thị kết quả cuối] --> End([Stop])
```

---

## 4. Component Diagram

```mermaid
graph TD
    subgraph "Server Side"
        server[Server]
        dbManager[DatabaseManager]
        qHandler[QuestionHandler]
        mysql[(MySQL)]
        server --> dbManager
        server --> qHandler
        dbManager --> mysql
    end

    subgraph "Client Side"
        client[QuizClient]
        gui[GUI Components]
        history[Score History]
        socket[Socket Handler]
        client --> gui
        client --> history
        client --> socket
    end

    cloud["TCP/IP Network"]

    server -.-> cloud
    socket -.-> cloud
```

---

## 5. Deployment Diagram

```mermaid
graph TD
    subgraph "Server Machine"
        serverApp["server.py"]
        dbManagerFile["database_manager.py"]
        qHandlerFile["question_handler.py"]
        dbCluster[(MySQL Database)]
        serverApp --> dbManagerFile
        serverApp --> qHandlerFile
        dbManagerFile --> dbCluster
    end

    subgraph "Client Machine"
        clientApp["client.py"]
        guiFile["gui_components.py"]
        historyFile["score_history.json"]
        clientApp --> guiFile
        clientApp --> historyFile
    end

    cloud["TCP/IP"]
    serverApp -.-> cloud
    clientApp -.-> cloud
```

---

## 6. State Diagram

```mermaid
stateDiagram-v2
    [*] --> NotConnected

    NotConnected --> Connecting : Khởi động
    Connecting --> Connected : Thành công
    Connecting --> Failed : Lỗi
    Failed --> [*]

    Connected --> WaitingForUsername : Chào mừng
    WaitingForUsername --> ReadyToStart : Gửi tên
    ReadyToStart --> WaitingForQuestions : Gửi "0"

    state GameLoop {
        WaitingForQuestions --> DisplayingQuestion
        DisplayingQuestion --> WaitingForAnswer
        DisplayingQuestion --> TimerRunning
        TimerRunning --> TimerExpired
        TimerRunning --> WaitingForResult
        TimerExpired --> WaitingForResult
        WaitingForResult --> DisplayingResult
        DisplayingResult --> WaitingForQuestions
    }

    WaitingForQuestions --> GameLoop
    GameLoop --> GameCompleted
    GameCompleted --> ShowingFinalResult
    ShowingFinalResult --> SavingScore
    SavingScore --> ShowingLeaderboard
    ShowingLeaderboard --> Disconnected
    Disconnected --> [*]
```

---

## 7. Use-Case Diagram

```mermaid
graph LR
    actor_Player(["Người chơi"])
    actor_Admin(["Quản trị viên"])

    subgraph "Hệ thống Trắc Nghiệm Online"
        UC1(["Đăng nhập với tên"])
        UC2(["Chơi trò chơi"])
        UC3(["Trả lời câu hỏi"])
        UC4(["Xem kết quả"])
        UC5(["Xem bảng xếp hạng"])
        UC6(["Quản lý người chơi"])
        UC7(["Quản lý câu hỏi"])
        UC8(["Thêm/sửa/xóa câu hỏi"])
        UC9(["Phân loại câu hỏi"])
        UC10(["Sao lưu/phục hồi dữ liệu"])
    end

    actor_Player --> UC1
    actor_Player --> UC2
    UC2 -- include --> UC3
    UC2 -- include --> UC4
    actor_Player --> UC5

    actor_Admin --> UC6
    actor_Admin --> UC7
    UC7 -- include --> UC8
    UC7 -- include --> UC9
    actor_Admin --> UC10
```

---

## 8. Package Diagram

```mermaid
graph TD
    subgraph Server
        subgraph Core
            S_Server[Server]
            ClientHandler
            ThreadManager
        end
        subgraph Database
            DatabaseManager
            QueryBuilder
            ConnectionPool
        end
        subgraph "Game Logic"
            QuestionHandler
            ScoreCalculator
            LeaderboardManager
        end
    end

    subgraph Client
        subgraph Network
            SocketHandler
            DataReceiver
            DataSender
        end
        subgraph UI
            MainWindow
            QuestionUI
            ResultUI
            LeaderboardUI
        end
        subgraph Logic
            GameController
            TimerManager
            ScoreTracker
        end
        subgraph Storage
            LocalStorage
            ScoreHistory
        end
    end

    S_Server --> ClientHandler
    S_Server --> ThreadManager
    ClientHandler --> DatabaseManager
    ClientHandler --> QuestionHandler
    DatabaseManager --> QueryBuilder
    DatabaseManager --> ConnectionPool
    QuestionHandler --> ScoreCalculator
    ScoreCalculator --> LeaderboardManager

    GameController --> SocketHandler
    SocketHandler --> DataReceiver
    SocketHandler --> DataSender
    GameController --> QuestionUI
    GameController --> ResultUI
    GameController --> TimerManager
    GameController --> ScoreTracker
    ScoreTracker --> LocalStorage
    LocalStorage --> ScoreHistory
    GameController --> LeaderboardUI
```
