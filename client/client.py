import socket

HOST = '127.0.0.1'  # IP server (chỉnh lại nếu server chạy trên máy khác)
PORT = 9999

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            data = s.recv(4096).decode()
            if not data:
                break
            print(data, end='')

            # Nếu server yêu cầu nhập tên, nhấn 0, hoặc nhập đáp án
            if ("nhập tên" in data.lower() or
                "nhấn phím 0" in data.lower() or
                "nhập đáp án" in data.lower()):
                msg = input(">> ").strip()
                s.sendall(msg.encode())

        print("\nĐã ngắt kết nối với server.")

if __name__ == "__main__":
    main()
