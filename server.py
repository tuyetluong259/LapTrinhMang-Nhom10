# server.py
import socket
import threading

HOST = '127.0.0.1'
PORT = 54312

correct_answer_index = 0  # 0 = Điệp âm

def handle_client(conn, addr):
    print(f"[KẾT NỐI] {addr} đã kết nối.")
    try:
        question = "QUESTION:Ở câu \"her hardest hue to hold\" trong bài thơ của Frost, biện pháp âm điệu nào được sử dụng?|Điệp âm|Lặp lại|Trùng âm|Từ tượng thanh"
        conn.sendall(question.encode())

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            if data.startswith("ANSWER:"):
                answer = int(data.split(":")[1])
                print(f"[CLIENT {addr}] chọn: {answer}")
                if answer == correct_answer_index:
                    result = f"RESULT:✅ Chính xác! Đáp án đúng là {chr(65 + answer)}."
                else:
                    result = f"RESULT:❌ Sai rồi! Đáp án đúng là {chr(65 + correct_answer_index)}."
                conn.sendall(result.encode())
    except:
        print(f"[NGẮT KẾT NỐI] {addr}")
    finally:
        conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER] Đang lắng nghe tại {HOST}:{PORT}...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
