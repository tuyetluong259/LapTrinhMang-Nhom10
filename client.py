import socket
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import time # Dùng cho độ trễ trong auto_advance_question

HOST = '127.0.0.1'
PORT = 9999

class QuizClient:
    def __init__(self, master):
        self.master = master
        self.master.title("🎮 Trắc Nghiệm Online")
        self.master.geometry("600x600")
        self.master.resizable(False, False)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
            print("[Client Init] Kết nối thành công tới server.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối đến server: {e}")
            self.master.destroy()
            return

        # ---- Gửi tên người chơi và tín hiệu bắt đầu ----
        try:
            welcome = self.client_socket.recv(1024).decode()
            print(f"[Client Init] Nhận từ server (Chào mừng): '{welcome.strip()}'")
            
            # Nếu server yêu cầu tên
            if "nhập tên" in welcome.lower():
                name = simpledialog.askstring("Nhập tên", "Nhập tên người chơi của bạn:")
                if not name:
                    name = "Khách" # Mặc định nếu người dùng không nhập hoặc đóng
                self.client_socket.sendall(name.encode())
                print(f"[Client Init] Đã gửi tên: '{name}'")

                # Nhận yêu cầu bắt đầu game (nhấn 0)
                start_msg = self.client_socket.recv(1024).decode()
                print(f"[Client Init] Nhận từ server (Yêu cầu bắt đầu): '{start_msg.strip()}'")
                if "bắt đầu" in start_msg.lower():
                    self.client_socket.sendall(b"0")
                    print("[Client Init] Đã gửi tín hiệu bắt đầu (0).")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khởi tạo hoặc gửi tên/bắt đầu game: {e}")
            self.master.destroy()
            return

        # ---- Cấu hình giao diện ----
        self.frame_main = ttk.Frame(master, padding=20)
        self.frame_main.pack(fill="both", expand=True)

        self.title_label = ttk.Label(self.frame_main, text="🧠 Trắc Nghiệm Online", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=10)

        self.question_label = ttk.Label(self.frame_main, text="Đang tải câu hỏi...", wraplength=550, font=("Helvetica", 14))
        self.question_label.pack(pady=10)

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
        
        # Nhãn hiển thị kết quả đúng/sai
        self.response_label = ttk.Label(self.frame_main, text="", font=("Helvetica", 16, "bold"), foreground="blue", wraplength=500) # Tăng font size, làm đậm và đổi màu cho dễ thấy
        self.response_label.pack(pady=10)

        # ---- Biến trạng thái và Buffer dữ liệu ----
        self.data_buffer = "" # Nơi lưu trữ dữ liệu nhận được từ server
        self.expecting_question = True # True: đang đợi câu hỏi; False: đang đợi kết quả
        self.selected_answer = ""
        
        # Đăng ký sự kiện tự động chuyển câu hỏi
        self.master.bind("<<ContinueNextQuestion>>", self.auto_advance_question)

        # Khởi động luồng nhận dữ liệu từ server
        self.listen_thread = threading.Thread(target=self.receive_data, daemon=True)
        self.listen_thread.start()

        # Xử lý khi đóng cửa sổ
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def select_answer(self, event):
        """Xử lý khi người dùng chọn một đáp án."""
        self.selected_answer = event.widget.cget("text")
        self.drop_area.config(text=f"✅ {self.selected_answer}")
        print(f"[UI] Đã chọn đáp án: '{self.selected_answer}'")

    def receive_data(self):
        """Luồng riêng biệt để nhận dữ liệu từ server."""
        while True:
            try:
                chunk = self.client_socket.recv(4096).decode()
                if not chunk:
                    print("[Receive] Server đã đóng kết nối. Thoát luồng nhận dữ liệu.")
                    break
                self.data_buffer += chunk
                print(f"\n[Receive] Nhận được chunk ({len(chunk)} bytes):\n---BEGIN CHUNK---\n{chunk.strip()}\n---END CHUNK---\n")
                print(f"[Receive] Buffer hiện tại ({len(self.data_buffer)} bytes):\n---BEGIN BUFFER---\n{self.data_buffer.strip()[:500]}...\n---END BUFFER---\n")
                
                # Gọi hàm xử lý buffer trên luồng chính của Tkinter để tránh lỗi luồng
                self.master.after_idle(self._process_data_from_buffer)

            except Exception as e:
                print(f"[Receive ERROR] Lỗi khi nhận dữ liệu: {e}")
                break
        
        # Xử lý phần còn lại của buffer khi kết nối đóng (nếu có)
        if self.data_buffer:
            print("[Receive] Xử lý buffer còn lại khi kết nối đóng.")
            self.master.after_idle(self._process_data_from_buffer)

    def _process_data_from_buffer(self):
        """
        Hàm này được gọi liên tục trên luồng chính của Tkinter để phân tích
        và xử lý dữ liệu trong self.data_buffer.
        """
        print(f"\n[Process Buffer] Bắt đầu xử lý. Buffer ban đầu ({len(self.data_buffer)} bytes): {self.data_buffer.strip()[:200]}...")
        
        # Vòng lặp để xử lý nhiều thông điệp trong cùng một buffer (nếu có)
        while True:
            original_buffer_len_in_loop = len(self.data_buffer) # Kích thước buffer trước khi xử lý trong vòng lặp này

            # 1. Ưu tiên tìm kết quả cuối cùng (kết thúc game)
            if "Trò chơi kết thúc!" in self.data_buffer:
                final_start_idx = self.data_buffer.find("Trò chơi kết thúc!")
                final_message = self.data_buffer[final_start_idx:].strip()
                self.master.after(0, lambda: messagebox.showinfo("Kết thúc", final_message))
                self.master.after(0, self.master.destroy)
                print(f"[Process Buffer] Đã xử lý thông báo kết thúc game. Thoát.")
                self.data_buffer = "" # Xóa buffer
                return # Thoát khỏi hàm và vòng lặp

            # 2. Xử lý kết quả đáp án (chỉ khi đang đợi kết quả, tức là vừa gửi đáp án)
            if not self.expecting_question:
                print(f"[Process Buffer] Đang tìm kết quả đáp án. Buffer: {self.data_buffer.strip()[:100]}...")
                if "Đáp án đúng!" in self.data_buffer:
                    idx = self.data_buffer.find("Đáp án đúng!")
                    # Tìm điểm kết thúc của thông báo (thường là \n\n)
                    end_idx = self.data_buffer.find("\n\n", idx)
                    if end_idx == -1: # Trường hợp thông báo bị cắt
                        end_idx = len(self.data_buffer)
                    
                    message = self.data_buffer[idx:end_idx].strip()
                    self.master.after(0, self.show_answer_result, message)
                    self.master.after(0, self.disable_answer_submission) # Vô hiệu hóa nút gửi
                    self.data_buffer = self.data_buffer[end_idx:].strip() # Cắt bỏ phần đã xử lý
                    self.expecting_question = True # Sau khi hiển thị kết quả, chuyển sang đợi câu hỏi mới
                    print(f"[Process Buffer] Đã xử lý 'Đáp án đúng!'. Buffer còn lại: {self.data_buffer.strip()[:100]}...")
                    # Kích hoạt sự kiện để tự động chuyển câu hỏi sau một khoảng thời gian
                    self.master.after(2000, self.master.event_generate, "<<ContinueNextQuestion>>") # 2 giây
                    continue # Quay lại đầu vòng lặp để kiểm tra xem có câu hỏi tiếp theo ngay lập tức trong buffer không

                elif "Đáp án sai!" in self.data_buffer:
                    idx = self.data_buffer.find("Đáp án sai!")
                    end_idx = self.data_buffer.find("\n\n", idx)
                    if end_idx == -1:
                        end_idx = len(self.data_buffer)
                    
                    message = self.data_buffer[idx:end_idx].strip()
                    self.master.after(0, self.show_answer_result, message)
                    self.master.after(0, self.disable_answer_submission) # Vô hiệu hóa nút gửi
                    self.data_buffer = self.data_buffer[end_idx:].strip() # Cắt bỏ phần đã xử lý
                    self.expecting_question = True # Sau khi hiển thị kết quả, chuyển sang đợi câu hỏi mới
                    print(f"[Process Buffer] Đã xử lý 'Đáp án sai!'. Buffer còn lại: {self.data_buffer.strip()[:100]}...")
                    self.master.after(2000, self.master.event_generate, "<<ContinueNextQuestion>>") # 2 giây
                    continue # Quay lại đầu vòng lặp

            # 3. Xử lý câu hỏi (chỉ khi đang đợi câu hỏi)
            if self.expecting_question:
                print(f"[Process Buffer] Đang tìm câu hỏi. Buffer: {self.data_buffer.strip()[:100]}...")
                if "Câu" in self.data_buffer and "Nhập đáp án (A/B/C/D):" in self.data_buffer:
                    question_start_idx = self.data_buffer.find("Câu")
                    question_end_idx = self.data_buffer.find("Nhập đáp án (A/B/C/D):") + len("Nhập đáp án (A/B/C/D):")
                    
                    if question_start_idx != -1 and question_end_idx != -1 and question_end_idx > question_start_idx:
                        question_block = self.data_buffer[question_start_idx:question_end_idx].strip()
                        self.master.after(0, self.parse_and_show_question, question_block)
                        # self.master.after(0, self.enable_answer_submission) # Sẽ được gọi trong auto_advance_question sau khi hiển thị câu hỏi
                        self.data_buffer = self.data_buffer[question_end_idx:].strip() # Cắt bỏ phần câu hỏi đã xử lý
                        self.expecting_question = False # Đã nhận câu hỏi, giờ đợi đáp án
                        print(f"[Process Buffer] Đã xử lý câu hỏi. Buffer còn lại: {self.data_buffer.strip()[:100]}...")
                        continue # Quay lại đầu vòng lặp để kiểm tra xem có kết quả hoặc thông báo khác ngay sau câu hỏi không
            
            # Nếu không có gì được xử lý trong vòng lặp này, thoát ra để chờ thêm dữ liệu
            if len(self.data_buffer) == original_buffer_len_in_loop:
                print(f"[Process Buffer] Không tìm thấy mẫu nào để xử lý trong vòng lặp này. Kích thước buffer: {len(self.data_buffer)}")
                break # Không có gì mới để xử lý trong buffer hiện tại

        print(f"[Process Buffer] Kết thúc xử lý buffer. Buffer cuối: {self.data_buffer.strip()[:100]}...")

    def parse_and_show_question(self, data):
        """Cập nhật giao diện với câu hỏi mới và các lựa chọn."""
        print(f"[UI Update] Cập nhật câu hỏi: {data[:50]}...")
        lines = data.strip().split("\n")
        
        question_text_lines = []
        options = []
        
        # Tách câu hỏi và các lựa chọn
        for line in lines:
            line_strip = line.strip()
            if line_strip.startswith(("A.", "B.", "C.", "D.")):
                options.append(line_strip)
            else:
                # Đảm bảo chỉ thêm các dòng có nội dung vào phần câu hỏi
                if line_strip: # Không thêm dòng trống
                    question_text_lines.append(line_strip)

        self.question_label.config(text="\n".join(question_text_lines))

        # Cập nhật nút đáp án
        for i in range(4):
            if i < len(options):
                self.option_buttons[i].config(text=options[i], state=NORMAL)
            else:
                self.option_buttons[i].config(text=f"Đáp án {chr(65+i)}. (Trống)", state=DISABLED) # Vô hiệu hóa nút thừa

        self.selected_answer = ""
        self.drop_area.config(text="⬇️ Kéo đáp án vào đây")
        # KHÔNG XÓA self.response_label ở đây. Nó sẽ được xóa khi auto_advance_question gọi (sau độ trễ).
        print("[UI Update] Giao diện đã cập nhật với câu hỏi mới.")

    def show_answer_result(self, message):
        """Hiển thị thông báo đúng/sai trên giao diện."""
        print(f"[UI Update] HIỂN THỊ KẾT QUẢ TRÊN GUI: '{message}'")
        # Đặt màu sắc và font cho nhãn kết quả
        if "sai" in message.lower() or "incorrect" in message.lower():
            self.response_label.config(text=message, foreground="red")
        else:
            self.response_label.config(text=message, foreground="green")
        
        # Buộc Tkinter cập nhật ngay lập tức để đảm bảo thông báo hiển thị
        self.response_label.update_idletasks() 
        
    def send_answer(self):
        """Gửi đáp án đã chọn đến server."""
        if not self.selected_answer:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một đáp án trước khi gửi!")
            return
        
        try:
            # Lấy ký tự đáp án (A, B, C, D) từ chuỗi đầy đủ (ví dụ "A. 3" -> "A")
            answer_letter = self.selected_answer[0].upper() 
            
            self.client_socket.sendall(f"{answer_letter}\n".encode()) # Thêm \n để server dễ đọc
            print(f"[Send Answer] Đã gửi đáp án: '{answer_letter}'")
            
            self.expecting_question = False # Đã gửi đáp án, giờ đợi kết quả từ server
            self.disable_answer_submission() # Vô hiệu hóa nút gửi và lựa chọn ngay lập tức

        except Exception as e:
            messagebox.showerror("Lỗi", f"Gửi dữ liệu thất bại: {e}")
            print(f"[Send Answer ERROR] Lỗi khi gửi đáp án: {e}")

    def auto_advance_question(self, event=None):
        """
        Hàm này được gọi bởi sự kiện <<ContinueNextQuestion>> sau khi hiển thị kết quả và chờ.
        Nó sẽ kích hoạt lại quá trình xử lý buffer để hiển thị câu hỏi tiếp theo.
        """
        print("\n[Auto Advance] Tự động chuyển câu hỏi được kích hoạt.")
        # Dọn dẹp trạng thái UI và kích hoạt lại khả năng gửi đáp án
        self.response_label.config(text="") # Xóa thông báo kết quả cũ sau độ trễ
        self.enable_answer_submission() # Kích hoạt lại các nút và ô nhập liệu
        self.expecting_question = True # Đặt lại trạng thái để _process_data_from_buffer tìm câu hỏi
        self._process_data_from_buffer() # Kích hoạt lại việc xử lý buffer để tìm câu hỏi mới (nếu đã có trong buffer)
        print("[Auto Advance] Đã kích hoạt xử lý buffer để tìm câu hỏi mới.")

    def disable_answer_submission(self):
        """Vô hiệu hóa nút gửi đáp án và các lựa chọn."""
        self.submit_btn.config(state=DISABLED)
        for btn in self.option_buttons:
            btn.config(state=DISABLED)
        print("[UI State] Đã vô hiệu hóa gửi đáp án.")

    def enable_answer_submission(self):
        """Kích hoạt lại nút gửi đáp án và các lựa chọn."""
        self.submit_btn.config(state=NORMAL)
        for btn in self.option_buttons:
            btn.config(state=NORMAL)
        print("[UI State] Đã kích hoạt gửi đáp án.")

    def on_close(self):
        """Xử lý khi cửa sổ client đóng."""
        try:
            self.client_socket.close()
            print("[Client Exit] Socket client đã đóng.")
        except Exception as e:
            print(f"[Client Exit ERROR] Lỗi khi đóng socket: {e}")
        self.master.destroy()
        print("[Client Exit] Ứng dụng client đã đóng.")

if __name__ == "__main__":
    app = ttk.Window(themename="morph")
    QuizClient(app)
    app.mainloop()
