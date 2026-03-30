import tkinter as tk
from tkinter import filedialog, messagebox
import time
import os

# Import các hàm thuật toán từ file AES.py của bạn
import AES


class AESInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("AES-128 Encryptor/Decryptor - Nhóm 18")
        self.root.geometry("1000x750")  # Tăng kích thước để chứa bảng Terminal Log

        self.filepath = ""
        self.file_ext = ""
        self.file_name_only = ""
        self.current_action = ""

        self.input_data = b""
        self.output_data = b""

        # --- KHU VỰC ĐIỀU KHIỂN ---
        control_frame = tk.Frame(root, pady=10)
        control_frame.pack(fill="x")

        # Khóa
        key_frame = tk.Frame(control_frame)
        key_frame.pack(pady=5)
        tk.Label(
            key_frame, text="Khóa Bí Mật (Tối đa 16 ký tự):", font=("Arial", 10, "bold")
        ).pack(side="left")

        self.key_entry = tk.Entry(key_frame, width=30, show="*", font=("Arial", 10))
        self.key_entry.pack(side="left", padx=5)
        self.btn_show_pwd = tk.Button(
            key_frame,
            text="👁",
            command=self.toggle_password,
            font=("Arial", 10),
            cursor="hand2",
        )
        self.btn_show_pwd.pack(side="left")

        # Chọn File
        file_frame = tk.Frame(control_frame)
        file_frame.pack(pady=5)
        self.lbl_filename = tk.Label(
            file_frame,
            text="Chưa chọn file...",
            width=40,
            anchor="w",
            fg="gray",
            bg="white",
            relief="sunken",
        )
        self.lbl_filename.pack(side="left", padx=5)
        tk.Button(
            file_frame, text="Chọn File Gốc", command=self.select_file, cursor="hand2"
        ).pack(side="left")

        # Nút chức năng
        btn_frame = tk.Frame(control_frame)
        btn_frame.pack(pady=10)
        tk.Button(
            btn_frame,
            text="Mã Hóa File",
            command=self.encrypt_action,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15,
            cursor="hand2",
        ).pack(side="left", padx=10)
        tk.Button(
            btn_frame,
            text="Giải Mã File",
            command=self.decrypt_action,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15,
            cursor="hand2",
        ).pack(side="left", padx=10)

        self.btn_export = tk.Button(
            btn_frame,
            text="💾 Xuất File (Lưu)",
            command=self.export_file,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15,
            cursor="hand2",
            state="disabled",
        )
        self.btn_export.pack(side="left", padx=10)

        # --- KHU VỰC TERMINAL LOG BÁO CÁO (Phía dưới cùng) ---
        log_frame = tk.Frame(root, padx=10, pady=5)
        log_frame.pack(side="bottom", fill="x")
        tk.Label(
            log_frame,
            text="TERMINAL LOG (Báo cáo quá trình):",
            font=("Arial", 10, "bold"),
        ).pack(anchor="w")
        self.txt_log = tk.Text(
            log_frame, height=6, bg="black", fg="#00FF00", font=("Consolas", 10)
        )
        self.txt_log.pack(fill="x")
        self.print_log("======================================================")
        self.print_log(" BÀI TẬP NHÓM 18: MÃ HÓA VÀ GIẢI MÃ FILE BẰNG AES-128")
        self.print_log("======================================================")

        # --- KHU VỰC HIỂN THỊ NỘI DUNG (Ở giữa) ---
        content_frame = tk.Frame(root, padx=10, pady=10)
        content_frame.pack(fill="both", expand=True)

        self.mode_left = tk.StringVar(value="Text")
        self.mode_right = tk.StringVar(value="Hex")

        # Nửa Trái
        left_frame = tk.Frame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        left_header = tk.Frame(left_frame)
        left_header.pack(fill="x", pady=2)
        tk.Label(left_header, text="NỘI DUNG GỐC", font=("Arial", 10, "bold")).pack(
            side="left"
        )
        tk.Radiobutton(
            left_header,
            text="Text",
            variable=self.mode_left,
            value="Text",
            command=self.refresh_left,
        ).pack(side="right")
        tk.Radiobutton(
            left_header,
            text="Hex",
            variable=self.mode_left,
            value="Hex",
            command=self.refresh_left,
        ).pack(side="right")
        tk.Radiobutton(
            left_header,
            text="Binary",
            variable=self.mode_left,
            value="Binary",
            command=self.refresh_left,
        ).pack(side="right")
        self.txt_left = tk.Text(left_frame, wrap="word", font=("Consolas", 10))
        self.txt_left.pack(fill="both", expand=True)

        # Nửa Phải
        right_frame = tk.Frame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        right_header = tk.Frame(right_frame)
        right_header.pack(fill="x", pady=2)
        tk.Label(
            right_header, text="KẾT QUẢ XỬ LÝ", font=("Arial", 10, "bold"), fg="#d32f2f"
        ).pack(side="left")
        tk.Radiobutton(
            right_header,
            text="Text",
            variable=self.mode_right,
            value="Text",
            command=self.refresh_right,
        ).pack(side="right")
        tk.Radiobutton(
            right_header,
            text="Hex",
            variable=self.mode_right,
            value="Hex",
            command=self.refresh_right,
        ).pack(side="right")
        tk.Radiobutton(
            right_header,
            text="Binary",
            variable=self.mode_right,
            value="Binary",
            command=self.refresh_right,
        ).pack(side="right")
        self.txt_right = tk.Text(
            right_frame, wrap="word", font=("Consolas", 10), bg="#f4f4f4"
        )
        self.txt_right.pack(fill="both", expand=True)

    # --- HÀM TIỆN ÍCH ---
    def print_log(self, message):
        """In thông báo ra khung Terminal nền đen"""
        self.txt_log.insert(tk.END, message + "\n")
        self.txt_log.see(tk.END)  # Cuộn xuống dòng mới nhất

    def toggle_password(self):
        if self.key_entry.cget("show") == "*":
            self.key_entry.config(show="")
            self.btn_show_pwd.config(text="🙈")
        else:
            self.key_entry.config(show="*")
            self.btn_show_pwd.config(text="👁")

    def format_data(self, data, mode):
        if not data:
            return ""
        limit = 5000
        slice_data = data[:2000]
        res = ""

        if mode == "Text":
            try:
                res = data.decode("utf-8")
                if len(res) > limit:
                    res = res[:limit] + "\n\n... [CÒN TIẾP] ..."
            except UnicodeDecodeError:
                res = "[DỮ LIỆU KHÔNG THỂ ĐỌC DƯỚI DẠNG VĂN BẢN (NON-TEXT)]\n\n Không đọc được nội dung file dạng text."
        elif mode == "Hex":
            hex_str = slice_data.hex().upper()
            res = " ".join(hex_str[i : i + 2] for i in range(0, len(hex_str), 2))
            if len(data) > 2000:
                res += "\n\n... [CÒN TIẾP] ..."
        elif mode == "Binary":
            res = " ".join(f"{b:08b}" for b in slice_data[:500])
            if len(data) > 500:
                res += "\n\n... [CÒN TIẾP] ..."

        return res

    def refresh_left(self):
        self.txt_left.delete(1.0, tk.END)
        self.txt_left.insert(
            tk.END, self.format_data(self.input_data, self.mode_left.get())
        )

    def refresh_right(self):
        self.txt_right.config(state="normal")
        self.txt_right.delete(1.0, tk.END)
        self.txt_right.insert(
            tk.END, self.format_data(self.output_data, self.mode_right.get())
        )

    # --- HÀM XỬ LÝ CHÍNH ---
    def select_file(self):
        path = filedialog.askopenfilename(title="Chọn file")
        if path:
            self.filepath = path
            self.file_name_only = os.path.splitext(os.path.basename(path))[0]
            self.file_ext = os.path.splitext(path)[1]  # Lấy đuôi file

            self.lbl_filename.config(text=os.path.basename(path), fg="black")

            with open(path, "rb") as f:
                self.input_data = f.read()

            self.output_data = b""
            self.btn_export.config(state="disabled")
            self.mode_left.set("Text")
            self.refresh_left()
            self.refresh_right()
            self.print_log(
                f"\n[+] Đã tải file '{os.path.basename(path)}' ({len(self.input_data)} bytes)."
            )

    def get_key(self):
        key_in = self.key_entry.get()
        if not key_in:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập khóa bí mật!")
            return None
        return key_in.encode("utf-8").ljust(16, b"\0")[:16]

    def encrypt_action(self):
        if not self.input_data:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file gốc!")
            return

        key_str = self.get_key()
        if not key_str:
            return

        try:
            self.print_log("[*] Đang tiến hành MÃ HÓA...")
            self.root.update()

            r_keys = AES.key_expansion(key_str)
            pad_len = 16 - (len(self.input_data) % 16)
            data_to_encrypt = self.input_data + bytes([pad_len] * pad_len)

            start_time = time.perf_counter()
            self.output_data = b"".join(
                [
                    AES.aes_main(data_to_encrypt[i : i + 16], r_keys, "encrypt")
                    for i in range(0, len(data_to_encrypt), 16)
                ]
            )
            end_time = time.perf_counter()
            time_encrypt = end_time - start_time

            self.current_action = "enc"
            self.mode_right.set("Hex")
            self.refresh_right()
            self.btn_export.config(state="normal")

            self.print_log(f"[THỜI GIAN MÃ HÓA]: {time_encrypt:.6f} giây")
            self.print_log(f"-> Sẵn sàng xuất file mã hóa (.bin)")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi:\n{str(e)}")

    def decrypt_action(self):
        if not self.input_data:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file gốc để giải mã!")
            return
        if len(self.input_data) % 16 != 0:
            messagebox.showerror(
                "Lỗi Dữ Liệu",
                "File đầu vào không hợp lệ! Kích thước file giải mã phải chia hết cho 16. Bạn có chắc đây là file đã được mã hóa bằng AES-128 không?",
            )
            return

        key_str = self.get_key()
        if not key_str:
            return

        try:
            self.print_log("[*] Đang tiến hành GIẢI MÃ...")
            self.root.update()

            r_keys = AES.key_expansion(key_str)

            start_time = time.perf_counter()
            decrypted_raw = b"".join(
                [
                    AES.aes_main(self.input_data[i : i + 16], r_keys, "decrypt")
                    for i in range(0, len(self.input_data), 16)
                ]
            )

            # Gỡ Padding (Tuyệt đối an toàn giống AES.py)
            pad_len = decrypted_raw[-1]
            if 0 < pad_len <= 16:
                self.output_data = decrypted_raw[:-pad_len]
            else:
                self.output_data = decrypted_raw
            end_time = time.perf_counter()
            time_decrypt = end_time - start_time

            self.current_action = "dec"
            self.mode_left.set("Hex")
            self.refresh_left()
            self.mode_right.set("Text")
            self.refresh_right()
            self.btn_export.config(state="normal")

            self.print_log(f"[THỜI GIAN GIẢI MÃ]: {time_decrypt:.6f} giây")
            self.print_log(f"-> Sẵn sàng xuất file giải mã.")

        except Exception as e:
            messagebox.showerror(
                "Lỗi", f"Giải mã thất bại. Sai khóa hoặc file hỏng!\nChi tiết: {str(e)}"
            )

    def export_file(self):
        if not self.output_data:
            return

        # --- ÉP CHUẨN ĐỊNH DẠNG FILE ---
        if self.current_action == "enc":
            # Nếu đang MÃ HÓA, ép phải lưu ra file .bin để không bị hỏng dữ liệu
            suggested_name = f"encrypted_{self.file_name_only}.bin"
            filepath = filedialog.asksaveasfilename(
                title="Lưu file Mã Hóa",
                initialfile=suggested_name,
                defaultextension=".bin",
                filetypes=[("Binary Encrypted File", "*.bin")],
            )
        else:
            # Nếu đang GIẢI MÃ, gợi ý lại đuôi file text (nếu có)
            suggested_name = f"decrypted_{self.file_name_only}.txt"
            filepath = filedialog.asksaveasfilename(
                title="Lưu file Giải Mã",
                initialfile=suggested_name,
                defaultextension=".txt",
                filetypes=[("Text File", "*.txt"), ("All Files", "*.*")],
            )

        if filepath:
            try:
                with open(filepath, "wb") as f:
                    f.write(self.output_data)

                self.print_log("-" * 50)
                self.print_log(f"Đã lưu thành công: {os.path.basename(filepath)}")
                messagebox.showinfo("Thành công", f"Đã xuất file tại:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Lỗi lưu file", f"Không thể lưu file:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AESInterface(root)
    root.mainloop()
