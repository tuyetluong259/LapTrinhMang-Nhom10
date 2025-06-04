import socket
import threading
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

HOST = '127.0.0.1'
PORT = 54312

class QuizClient:
    def __init__(self, master):
        self.master = master
        self.master.title("🎮 Trắc Nghiệm Online")
        self.master.geometry("600x500")
        self.master.resizable(False, False)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối đến server: {e}")
            self.master.destroy()
            return

        # ===== GIAO DIỆN =====
        self.frame_main = ttk.Frame(master, padding=20)
        self.frame_main.pack(fill="both", expand=True)

        self.title_label = ttk.Label(self.frame_main, text="🧠 Trắc Nghiệm Online", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=10)

        self.question_label = ttk.Label(self.frame_main, text="Đang tải câu hỏi...", wraplength=550, font=("Helvetica", 14))
        self.question_label.pack(pady=10)

        # Khung đáp án
        self.answer_var = tk.StringVar()
        self.answer_container = ttk.Frame(self.frame_main)
        self.answer_container.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            btn = ttk.Button(self.answer_container, text=f"Đáp án {i+1}", bootstyle="danger-solid", width=25)
            btn.pack(fill="x", padx=10, pady=5)
            self.option_buttons.append(btn)
            btn.bind("<Button-1>", self.select_answer)

        self.drop_area = ttk.Label(self.frame_main, text="⬇️ Kéo đáp án vào đây", font=("Helvetica", 14), bootstyle="warning", width=30, padding=10)
        self.drop_area.pack(pady=20)

        self.submit_btn = ttk.Button(self.frame_main, text="🚀 Gửi Đáp Án", command=self.send_answer, bootstyle="success-solid")
        self.submit_btn.pack(pady=15)

        self.response_label = ttk.Label(self.frame_main, text="", font=("Helvetica", 12), foreground="green", wraplength=500)
        self.response_label.pack()

        self.listen_thread = threading.Thread(target=self.receive_data, daemon=True)
        self.listen_thread.start()

        self.selected_answer = ""

        # Khi đóng cửa sổ, tắt kết nối
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def select_answer(self, event):
        self.selected_answer = event.widget.cget("text")
        self.drop_area.config(text=f"✅ {self.selected_answer}")

    def receive_data(self):
        while True:
            try:
                data = self.client_socket.recv(4096).decode()
                if not data:
                    break
                if data.startswith("QUESTION:"):
                    self.show_question(data[9:])
                elif data.startswith("RESULT:"):
                    self.response_label.config(text=data[7:], foreground="green")
            except Exception as e:
                print("Lỗi khi nhận dữ liệu:", e)
                break

    def show_question(self, question_data):
        parts = question_data.split("|")
        if len(parts) == 5:
            self.question_label.config(text=parts[0])
            for i in range(4):
                self.option_buttons[i].config(text=parts[i + 1])
            self.selected_answer = ""  # reset lựa chọn
            self.drop_area.config(text="⬇️ Kéo đáp án vào đây")  # reset hộp kéo thả
            self.response_label.config(text="")  # xóa kết quả cũ

    def send_answer(self):
        if not self.selected_answer:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một đáp án!")
            return
        try:
            answer_index = self.option_buttons.index(next(btn for btn in self.option_buttons if btn.cget("text") == self.selected_answer))
            self.client_socket.sendall(f"ANSWER:{answer_index}".encode())
        except Exception as e:
            messagebox.showerror("Lỗi", f"Gửi dữ liệu thất bại: {e}")

    def on_close(self):
        try:
            self.client_socket.close()
        except:
            pass
        self.master.destroy()

if __name__ == "__main__":
    app = ttk.Window(themename="morph")  # Chọn theme hiện đại hơn
    QuizClient(app)
    app.mainloop()
