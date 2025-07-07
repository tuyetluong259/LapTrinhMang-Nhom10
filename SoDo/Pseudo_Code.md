# Mã Giả (Pseudo Code)

Dưới đây là các thuật toán chính của hệ thống Trắc Nghiệm Online được biểu diễn bằng mã giả.

## 1. Server - Main Process

```
FUNCTION Main():
    Khởi tạo socket server
    Bind vào địa chỉ 0.0.0.0:9999
    Listen với tối đa 5 kết nối chờ

    WHILE true:
        client_socket, address = Accept kết nối mới
        Print "Client {address} connected"
        Khởi tạo thread mới với hàm HandleClient(client_socket, address)
        Bắt đầu thread
    END WHILE
END FUNCTION
```

## 2. Server - Handle Client

```
FUNCTION HandleClient(client_socket, address):
    TRY:
        Gửi thông báo chào mừng tới client
        name = Nhận tên người chơi từ client
        user_id, current_score = GetOrCreateUser(name)

        Gửi thông báo bắt đầu game tới client
        WHILE true:
            start_signal = Nhận tín hiệu bắt đầu từ client
            IF start_signal là "0" THEN
                BREAK
            END IF
            Gửi thông báo yêu cầu nhấn phím 0 tới client
        END WHILE

        questions = GetQuestions()
        score = 0

        FOR i = 0 TO 9:
            question = questions[i]
            question_text = FormatQuestion(i+1, question)
            Gửi câu hỏi tới client
            answer = Nhận đáp án từ client

            IF answer == question['correct_option'] THEN
                Gửi thông báo đáp án đúng tới client
                score += 1
            ELSE
                Gửi thông báo đáp án sai và đáp án đúng tới client
            END IF
        END FOR

        UpdateScore(user_id, score)
        leaderboard = GetLeaderboard()
        Gửi kết quả và bảng xếp hạng tới client

    CATCH Exception e:
        Print "Error with client {address}: {e}"
    FINALLY:
        Đóng kết nối client_socket
    END TRY
END FUNCTION
```

## 3. Server - Database Functions

```
FUNCTION GetOrCreateUser(name):
    TRY:
        Execute SQL: "SELECT id, score FROM users WHERE name = ?"
        result = Fetch one row

        IF result EXISTS THEN
            RETURN result["id"], result["score"]
        ELSE
            Execute SQL: "INSERT INTO users (name, score) VALUES (?, 0)"
            Commit transaction
            RETURN last inserted ID, 0
        END IF
    CATCH Exception:
        RETURN NULL, 0
    END TRY
END FUNCTION

FUNCTION GetQuestions():
    Execute SQL: "SELECT q.id, t.name AS topic, q.question, q.option_a, q.option_b,
                 q.option_c, q.option_d, q.correct_option
                 FROM questions q JOIN topics t ON q.topic_id = t.id
                 ORDER BY RAND() LIMIT 10"
    RETURN fetched questions
END FUNCTION

FUNCTION UpdateScore(user_id, score):
    Execute SQL: "UPDATE users SET score = score + ? WHERE id = ?"
    Commit transaction
END FUNCTION

FUNCTION GetLeaderboard():
    Execute SQL: "SELECT name, score FROM users ORDER BY score DESC LIMIT 5"
    RETURN fetched leaderboard
END FUNCTION
```

## 4. Client - Main Process

```
FUNCTION Main():
    master = Khởi tạo cửa sổ Tkinter với theme "morph"
    Khởi tạo QuizClient(master)
    Bắt đầu main loop Tkinter
END FUNCTION
```

## 5. Client - Initialization

```
FUNCTION QuizClient.__init__(master):
    Lưu tham chiếu master window
    Khởi tạo biến điểm số, thời gian và tên người chơi

    TRY:
        Tạo socket và kết nối tới HOST:PORT
    CATCH Exception:
        Hiển thị thông báo lỗi và thoát
    END TRY

    TRY:
        welcome = Nhận dữ liệu chào mừng từ server

        IF "nhập tên" trong welcome THEN
            name = Hiện dialog yêu cầu nhập tên
            IF name là rỗng THEN
                name = "Khách"
            END IF
            self.player_name = name
            Gửi name tới server

            start_msg = Nhận yêu cầu bắt đầu từ server
            IF "bắt đầu" trong start_msg THEN
                Gửi "0" tới server
            END IF
        END IF
    CATCH Exception:
        Hiển thị thông báo lỗi và thoát
    END TRY

    Khởi tạo các thành phần giao diện
    Khởi tạo buffer dữ liệu và biến trạng thái
    Khởi tạo thread lắng nghe dữ liệu từ server
    Đăng ký hàm xử lý đóng cửa sổ
END FUNCTION
```

## 6. Client - Process Data

```
FUNCTION QuizClient._process_data_from_buffer():
    WHILE true:
        original_buffer_len = Độ dài của buffer

        # Xử lý kết quả cuối cùng
        IF "Trò chơi kết thúc!" trong buffer THEN
            final_start_idx = Vị trí của "Trò chơi kết thúc!" trong buffer
            final_message = Cắt buffer từ final_start_idx
            Gọi hàm show_final_result_overlay với final_message
            Xóa buffer
            RETURN
        END IF

        # Xử lý kết quả đáp án
        IF NOT expecting_question THEN
            IF "Đáp án đúng!" trong buffer THEN
                Xử lý và hiển thị thông báo đúng
                Cập nhật buffer
                expecting_question = true
                Tự động chuyển câu hỏi sau 2.5 giây
                CONTINUE
            ELIF "Đáp án sai!" trong buffer THEN
                Xử lý và hiển thị thông báo sai
                Cập nhật buffer
                expecting_question = true
                Tự động chuyển câu hỏi sau 2.5 giây
                CONTINUE
            END IF
        END IF

        # Xử lý câu hỏi mới
        IF expecting_question THEN
            IF "Câu" trong buffer AND "Nhập đáp án (A/B/C/D):" trong buffer THEN
                Xử lý và hiển thị câu hỏi
                Cập nhật buffer
                expecting_question = false
                CONTINUE
            END IF
        END IF

        # Nếu không xử lý được gì thì thoát vòng lặp
        IF Độ dài buffer == original_buffer_len THEN
            BREAK
        END IF
    END WHILE
END FUNCTION
```

## 7. Client - Timer and Overlay

```
FUNCTION QuizClient.start_timer():
    timer_running = false
    time_remaining = QUESTION_TIME_LIMIT
    timer_running = true
    update_timer()
END FUNCTION

FUNCTION QuizClient.update_timer():
    IF timer_running AND time_remaining > 0 THEN
        Cập nhật nhãn hiển thị thời gian
        time_remaining -= 1
        Đặt lịch gọi lại update_timer sau 1 giây
    ELIF timer_running THEN
        timer_running = false
        time_up()
    END IF
END FUNCTION

FUNCTION QuizClient.show_overlay(message, color, sub_message=""):
    Tạo frame overlay che phủ toàn màn hình với nền màu color
    Hiển thị message với font lớn và màu trắng
    Nếu có sub_message thì hiển thị bên dưới
    Tự động ẩn overlay sau 2.5 giây
END FUNCTION

FUNCTION QuizClient.show_final_result_overlay(final_message):
    Tính toán thống kê điểm số
    Tạo overlay hiển thị kết quả cuối cùng
    Lưu điểm số vào file JSON
    Tự động hiện bảng xếp hạng và đóng app sau 20 giây
END FUNCTION
```
