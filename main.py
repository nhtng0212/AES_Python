import tkinter as tk
from tkinter import filedialog, messagebox
import time
import os

# Import file thuật toán AES của bạn
import AES


class AESOceanBreezeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AES-128 Ocean Breeze - Nhóm 18")
        self.root.geometry("1100x750")

        # --- BẢNG MÀU SÁNG (WHITE / BLUE / GREEN) ---
        self.BG_MAIN = "#f0f4f8"  # Xanh nhạt siêu sáng (Màu nền app)
        self.BG_CARD = "#ffffff"  # Trắng tinh (Nền các khung Card)
        self.FG_TEXT = "#0f172a"  # Xanh Navy siêu đậm (Chữ chính - chống mờ)
        self.FG_DIM = "#475569"  # Xám tro (Chữ phụ)

        self.COLOR_ENC = "#0284c7"  # Xanh dương đậm (Mã hóa)
        self.COLOR_DEC = "#059669"  # Xanh lá cây (Giải mã)
        self.COLOR_SAV = "#2563eb"  # Xanh dương hoàng gia (Lưu file)
        self.COLOR_ACC = "#0ea5e9"  # Xanh dương lơ (Tab đang chọn)
        self.BORDER = "#cbd5e1"  # Xám viền (Chống mờ lòa giữa các khối)

        self.root.configure(bg=self.BG_MAIN)

        # Biến trạng thái
        self.filepath = ""
        self.file_name_only = ""
        self.input_data = b""
        self.output_data = b""
        self.current_action = ""

        self.show_pwd_var = tk.BooleanVar(value=False)
        self.in_format = tk.StringVar(value="Text")
        self.out_format = tk.StringVar(value="Hex")

        self._build_ui()
        self.write_log("Hệ thống AES-128 Ocean Breeze đã khởi động.")
        self.write_log("Giao diện: Sáng (Light) | Chủ đạo: Trắng - Xanh Dương - Xanh Lá.")

    def _build_ui(self):
        font_title = ("Segoe UI", 16, "bold")
        font_btn = ("Segoe UI", 10, "bold")
        font_text = ("Consolas", 10)
        font_label = ("Segoe UI", 10, "bold")

        # ================= HEADER (KHU VỰC NHẬP LIỆU) =================
        # Dùng viền highlightbackground để tạo cảm giác "Card" nổi lên
        header_frame = tk.Frame(self.root, bg=self.BG_CARD, highlightbackground=self.BORDER, highlightthickness=1)
        header_frame.pack(side="top", fill="x", padx=15, pady=15)

        # Dòng 1: Tên App & Chọn file
        row1 = tk.Frame(header_frame, bg=self.BG_CARD)
        row1.pack(fill="x", padx=20, pady=(15, 5))

        tk.Label(row1, text="🌊 AES-128 STUDIO", font=font_title, bg=self.BG_CARD, fg=self.COLOR_ENC).pack(side="left")

        btn_open = tk.Button(row1, text="📂 TẢI FILE GỐC", bg="#e2e8f0", fg=self.FG_TEXT, font=font_btn, relief="flat",
                             activebackground="#cbd5e1", cursor="hand2", command=self.load_file)
        btn_open.pack(side="left", padx=20, ipadx=10, ipady=3)

        self.lbl_file = tk.Label(row1, text="< Chưa có dữ liệu >", font=("Segoe UI", 10, "italic"), bg=self.BG_CARD,
                                 fg=self.FG_DIM)
        self.lbl_file.pack(side="left")

        # Dòng 2: Nhập khóa bí mật
        row2 = tk.Frame(header_frame, bg=self.BG_CARD)
        row2.pack(fill="x", padx=20, pady=(5, 15))

        tk.Label(row2, text="🔑 Khóa Bí Mật (16 bytes):", font=font_label, bg=self.BG_CARD, fg=self.FG_TEXT).pack(
            side="left")

        # Ô nhập liệu viền xám, chữ xanh navy
        self.entry_key = tk.Entry(row2, show="●", font=font_text, bg="#f8fafc", fg=self.COLOR_ENC,
                                  insertbackground=self.FG_TEXT, relief="flat", highlightbackground=self.BORDER,
                                  highlightthickness=1)
        self.entry_key.pack(side="left", padx=10, ipady=5, ipadx=5, fill="x", expand=True)

        cb_show = tk.Checkbutton(row2, text="Hiển thị khóa", variable=self.show_pwd_var, command=self.toggle_password,
                                 bg=self.BG_CARD, fg=self.FG_TEXT, selectcolor=self.BG_CARD,
                                 activebackground=self.BG_CARD, font=("Segoe UI", 9))
        cb_show.pack(side="left", padx=(0, 10))

        # ================= ACTION BAR (CÁC NÚT MÀU LỚN) =================
        action_frame = tk.Frame(self.root, bg=self.BG_MAIN)
        action_frame.pack(fill="x", padx=15, pady=(0, 15))

        btn_container = tk.Frame(action_frame, bg=self.BG_MAIN)
        btn_container.pack(anchor="center")

        # Nút Mã hóa (Xanh Dương)
        self.btn_encrypt = tk.Button(btn_container, text="🔒 MÃ HÓA (ENCRYPT)", bg=self.COLOR_ENC, fg="white",
                                     font=font_btn, relief="flat", cursor="hand2", command=self.run_encrypt)
        self.btn_encrypt.pack(side="left", padx=10, ipadx=20, ipady=8)

        # Nút Giải mã (Xanh Lá)
        self.btn_decrypt = tk.Button(btn_container, text="🔓 GIẢI MÃ (DECRYPT)", bg=self.COLOR_DEC, fg="white",
                                     font=font_btn, relief="flat", cursor="hand2", command=self.run_decrypt)
        self.btn_decrypt.pack(side="left", padx=10, ipadx=20, ipady=8)

        # Nút Lưu (Chìm khi chưa có data, Xanh hoàng gia khi có data)
        self.btn_save = tk.Button(btn_container, text="💾 XUẤT KẾT QUẢ", bg="#cbd5e1", fg="#64748b", font=font_btn,
                                  relief="flat", state="disabled", command=self.save_file)
        self.btn_save.pack(side="left", padx=10, ipadx=20, ipady=8)

        # ================= MAIN CONTENT (CHIA ĐÔI TRÁI PHẢI) =================
        content_frame = tk.Frame(self.root, bg=self.BG_MAIN)
        content_frame.pack(fill="both", expand=True, padx=15)

        # NỬA TRÁI (INPUT)
        left_panel = tk.Frame(content_frame, bg=self.BG_CARD, highlightbackground=self.BORDER, highlightthickness=1)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))

        left_header = tk.Frame(left_panel, bg="#e0f2fe", pady=8, padx=10)  # Nền xanh lơ nhạt
        left_header.pack(fill="x")
        tk.Label(left_header, text="📥 DỮ LIỆU ĐẦU VÀO", font=font_btn, bg="#e0f2fe", fg=self.COLOR_ENC).pack(
            side="left")

        self.create_toggle_buttons(left_header, self.in_format, "in")

        self.txt_in = tk.Text(left_panel, wrap="word", font=font_text, bg="#f8fafc", fg=self.FG_TEXT, relief="flat",
                              padx=10, pady=10, insertbackground=self.FG_TEXT)
        self.txt_in.pack(fill="both", expand=True, padx=1, pady=1)

        # NỬA PHẢI (OUTPUT)
        right_panel = tk.Frame(content_frame, bg=self.BG_CARD, highlightbackground=self.BORDER, highlightthickness=1)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))

        right_header = tk.Frame(right_panel, bg="#dcfce7", pady=8, padx=10)  # Nền xanh lá nhạt
        right_header.pack(fill="x")
        tk.Label(right_header, text="📤 KẾT QUẢ ĐẦU RA", font=font_btn, bg="#dcfce7", fg=self.COLOR_DEC).pack(
            side="left")

        self.create_toggle_buttons(right_header, self.out_format, "out")

        self.txt_out = tk.Text(right_panel, wrap="word", font=font_text, bg="#ffffff", fg=self.FG_TEXT, relief="flat",
                               padx=10, pady=10)
        self.txt_out.pack(fill="both", expand=True, padx=1, pady=1)

        # ================= TERMINAL LOG (NEUTRAL DARK MÀU NEO) =================
        # Để Log màu đen/xanh navy đậm giúp neo giữ giao diện, tạo độ sâu không bị "lóa"
        log_frame = tk.Frame(self.root, bg=self.BG_MAIN)
        log_frame.pack(side="bottom", fill="x", padx=15, pady=15)

        tk.Label(log_frame, text="NHẬT KÝ HỆ THỐNG", font=("Segoe UI", 9, "bold"), bg=self.BG_MAIN, fg=self.FG_DIM,
                 anchor="w").pack(fill="x")

        self.txt_log = tk.Text(log_frame, height=4, bg="#0f172a", fg="#38bdf8", font=font_text, relief="flat",
                               highlightbackground=self.BORDER, highlightthickness=1, padx=8, pady=8)
        self.txt_log.pack(fill="both")

    def create_toggle_buttons(self, parent, variable, target):
        """Tạo các nút Radio dạng Flat Tab nổi bật trên nền sáng"""
        frame = tk.Frame(parent, bg=parent.cget("bg"))
        frame.pack(side="right")
        modes = ["Text", "Hex", "Binary"]
        for mode in modes:
            rb = tk.Radiobutton(frame, text=mode, variable=variable, value=mode,
                                indicatoron=0, width=6,
                                font=("Segoe UI", 9, "bold"),
                                bg="#f1f5f9", fg=self.FG_DIM,
                                selectcolor=self.COLOR_ACC,
                                activebackground="#cbd5e1", activeforeground="black",
                                relief="flat", borderwidth=1, cursor="hand2",
                                command=lambda t=target: self.refresh_display(t))
            rb.pack(side="left", padx=1)

    # --- HÀM GIAO DIỆN & TIỆN ÍCH ---
    def toggle_password(self):
        if self.show_pwd_var.get():
            self.entry_key.config(show="")
        else:
            self.entry_key.config(show="●")

    def write_log(self, text):
        time_str = time.strftime("%H:%M:%S")
        self.txt_log.insert(tk.END, f"[{time_str}] {text}\n")
        self.txt_log.see(tk.END)

    def process_bytes_to_str(self, data_bytes, mode):
        if not data_bytes: return ""
        preview = data_bytes[:3000]

        if mode == "Text":
            try:
                res = preview.decode("utf-8")
                return res + ("\n\n...[Dữ liệu dài đã được cắt bớt hiển thị]..." if len(data_bytes) > 3000 else "")
            except UnicodeDecodeError:
                return "< Không thể hiển thị nội dung Text. Vui lòng chọn chế độ xem Hex/Binary >"
        elif mode == "Hex":
            h = preview.hex().upper()
            res = " ".join(h[i:i + 2] for i in range(0, len(h), 2))
            return res + ("\n\n...[Dữ liệu dài đã được cắt bớt hiển thị]..." if len(data_bytes) > 3000 else "")
        elif mode == "Binary":
            res = " ".join(f"{b:08b}" for b in preview[:400])
            return res + ("\n\n...[Dữ liệu dài đã được cắt bớt hiển thị]..." if len(data_bytes) > 400 else "")

    def refresh_display(self, target):
        if target == "in":
            self.txt_in.delete(1.0, tk.END)
            self.txt_in.insert(tk.END, self.process_bytes_to_str(self.input_data, self.in_format.get()))
        else:
            self.txt_out.config(state="normal")
            self.txt_out.delete(1.0, tk.END)
            self.txt_out.insert(tk.END, self.process_bytes_to_str(self.output_data, self.out_format.get()))

    def fetch_key(self):
        k = self.entry_key.get()
        if not k:
            messagebox.showwarning("Cảnh báo", "Bạn chưa nhập Khóa Bí Mật!")
            return None
        return k.encode("utf-8").ljust(16, b"\0")[:16]

    # --- HÀM XỬ LÝ LÕI AES ---
    def load_file(self):
        path = filedialog.askopenfilename(title="Chọn file dữ liệu")
        if path:
            self.filepath = path
            self.file_name_only = os.path.splitext(os.path.basename(path))[0]
            self.lbl_file.config(text=os.path.basename(path), fg=self.COLOR_ENC)

            with open(path, "rb") as f:
                self.input_data = f.read()

            self.output_data = b""
            # Vô hiệu hóa nút Save
            self.btn_save.config(state="disabled", bg="#cbd5e1", fg="#64748b", cursor="arrow")

            self.in_format.set("Text")
            self.refresh_display("in")
            self.refresh_display("out")
            self.write_log(f"Đã mở file: {os.path.basename(path)} ({len(self.input_data)} bytes)")

    def run_encrypt(self):
        if not self.input_data:
            messagebox.showinfo("Lỗi", "Vui lòng Mở File Gốc trước!")
            return

        key_bytes = self.fetch_key()
        if not key_bytes: return

        try:
            self.write_log("Đang tiến hành MÃ HÓA AES-128...")
            self.root.update()

            round_keys = AES.key_expansion(key_bytes)
            pad_len = 16 - (len(self.input_data) % 16)
            data_padded = self.input_data + bytes([pad_len] * pad_len)

            start_time = time.perf_counter()
            self.output_data = b"".join([
                AES.aes_main(data_padded[i: i + 16], round_keys, "encrypt")
                for i in range(0, len(data_padded), 16)
            ])
            end_time = time.perf_counter()

            self.current_action = "enc"
            self.out_format.set("Hex")
            self.refresh_display("out")

            # Bật nút Save với màu Xanh Hoàng Gia nổi bật
            self.btn_save.config(state="normal", bg=self.COLOR_SAV, fg="white", cursor="hand2")
            self.write_log(f"Hoàn tất Mã hóa. Thời gian: {end_time - start_time:.5f}s")

        except Exception as e:
            messagebox.showerror("Ngoại lệ", f"Mã hóa thất bại. Chi tiết:\n{e}")

    def run_decrypt(self):
        if not self.input_data:
            messagebox.showinfo("Lỗi", "Vui lòng Mở File Mã Hóa trước!")
            return

        if len(self.input_data) % 16 != 0:
            messagebox.showerror("Lỗi Cấu Trúc",
                                 "Dữ liệu không hợp lệ. File mã hóa AES phải có kích thước chia hết cho 16 bytes.")
            return

        key_bytes = self.fetch_key()
        if not key_bytes: return

        try:
            self.write_log("Đang tiến hành GIẢI MÃ AES-128...")
            self.root.update()

            round_keys = AES.key_expansion(key_bytes)

            start_time = time.perf_counter()
            decrypted_raw = b"".join([
                AES.aes_main(self.input_data[i: i + 16], round_keys, "decrypt")
                for i in range(0, len(self.input_data), 16)
            ])

            pad_val = decrypted_raw[-1]
            if 0 < pad_val <= 16:
                self.output_data = decrypted_raw[:-pad_val]
            else:
                self.output_data = decrypted_raw

            end_time = time.perf_counter()

            self.current_action = "dec"
            self.in_format.set("Hex")
            self.refresh_display("in")
            self.out_format.set("Text")
            self.refresh_display("out")

            self.btn_save.config(state="normal", bg=self.COLOR_SAV, fg="white", cursor="hand2")
            self.write_log(f"Hoàn tất Giải mã. Thời gian: {end_time - start_time:.5f}s")

        except Exception as e:
            messagebox.showerror("Lỗi Giải Mã",
                                 "Giải mã thất bại! Vui lòng kiểm tra lại tính toàn vẹn của file hoặc nhập sai Khóa.")

    def save_file(self):
        if not self.output_data: return

        if self.current_action == "enc":
            def_ext, file_types = ".bin", [("AES Encrypted File", "*.bin")]
            sugg_name = f"Encrypted_{self.file_name_only}.bin"
        else:
            def_ext, file_types = ".txt", [("Text File", "*.txt"), ("All Files", "*.*")]
            sugg_name = f"Decrypted_{self.file_name_only}.txt"

        path = filedialog.asksaveasfilename(title="Lưu dữ liệu", initialfile=sugg_name, defaultextension=def_ext,
                                            filetypes=file_types)

        if path:
            try:
                with open(path, "wb") as f:
                    f.write(self.output_data)
                self.write_log(f"Đã lưu kết quả thành công tại: {path}")
                messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file:\n{os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Lỗi Lưu File", str(e))


if __name__ == "__main__":
    app_root = tk.Tk()
    app = AESOceanBreezeApp(app_root)
    app_root.mainloop()