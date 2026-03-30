import time
import os

# THUẬT TOÁN AES-128
SBOX = [
    0x63,
    0x7C,
    0x77,
    0x7B,
    0xF2,
    0x6B,
    0x6F,
    0xC5,
    0x30,
    0x01,
    0x67,
    0x2B,
    0xFE,
    0xD7,
    0xAB,
    0x76,
    0xCA,
    0x82,
    0xC9,
    0x7D,
    0xFA,
    0x59,
    0x47,
    0xF0,
    0xAD,
    0xD4,
    0xA2,
    0xAF,
    0x9C,
    0xA4,
    0x72,
    0xC0,
    0xB7,
    0xFD,
    0x93,
    0x26,
    0x36,
    0x3F,
    0xF7,
    0xCC,
    0x34,
    0xA5,
    0xE5,
    0xF1,
    0x71,
    0xD8,
    0x31,
    0x15,
    0x04,
    0xC7,
    0x23,
    0xC3,
    0x18,
    0x96,
    0x05,
    0x9A,
    0x07,
    0x12,
    0x80,
    0xE2,
    0xEB,
    0x27,
    0xB2,
    0x75,
    0x09,
    0x83,
    0x2C,
    0x1A,
    0x1B,
    0x6E,
    0x5A,
    0xA0,
    0x52,
    0x3B,
    0xD6,
    0xB3,
    0x29,
    0xE3,
    0x2F,
    0x84,
    0x53,
    0xD1,
    0x00,
    0xED,
    0x20,
    0xFC,
    0xB1,
    0x5B,
    0x6A,
    0xCB,
    0xBE,
    0x39,
    0x4A,
    0x4C,
    0x58,
    0xCF,
    0xD0,
    0xEF,
    0xAA,
    0xFB,
    0x43,
    0x4D,
    0x33,
    0x85,
    0x45,
    0xF9,
    0x02,
    0x7F,
    0x50,
    0x3C,
    0x9F,
    0xA8,
    0x51,
    0xA3,
    0x40,
    0x8F,
    0x92,
    0x9D,
    0x38,
    0xF5,
    0xBC,
    0xB6,
    0xDA,
    0x21,
    0x10,
    0xFF,
    0xF3,
    0xD2,
    0xCD,
    0x0C,
    0x13,
    0xEC,
    0x5F,
    0x97,
    0x44,
    0x17,
    0xC4,
    0xA7,
    0x7E,
    0x3D,
    0x64,
    0x5D,
    0x19,
    0x73,
    0x60,
    0x81,
    0x4F,
    0xDC,
    0x22,
    0x2A,
    0x90,
    0x88,
    0x46,
    0xEE,
    0xB8,
    0x14,
    0xDE,
    0x5E,
    0x0B,
    0xDB,
    0xE0,
    0x32,
    0x3A,
    0x0A,
    0x49,
    0x06,
    0x24,
    0x5C,
    0xC2,
    0xD3,
    0xAC,
    0x62,
    0x91,
    0x95,
    0xE4,
    0x79,
    0xE7,
    0xC8,
    0x37,
    0x6D,
    0x8D,
    0xD5,
    0x4E,
    0xA9,
    0x6C,
    0x56,
    0xF4,
    0xEA,
    0x65,
    0x7A,
    0xAE,
    0x08,
    0xBA,
    0x78,
    0x25,
    0x2E,
    0x1C,
    0xA6,
    0xB4,
    0xC6,
    0xE8,
    0xDD,
    0x74,
    0x1F,
    0x4B,
    0xBD,
    0x8B,
    0x8A,
    0x70,
    0x3E,
    0xB5,
    0x66,
    0x48,
    0x03,
    0xF6,
    0x0E,
    0x61,
    0x35,
    0x57,
    0xB9,
    0x86,
    0xC1,
    0x1D,
    0x9E,
    0xE1,
    0xF8,
    0x98,
    0x11,
    0x69,
    0xD9,
    0x8E,
    0x94,
    0x9B,
    0x1E,
    0x87,
    0xE9,
    0xCE,
    0x55,
    0x28,
    0xDF,
    0x8C,
    0xA1,
    0x89,
    0x0D,
    0xBF,
    0xE6,
    0x42,
    0x68,
    0x41,
    0x99,
    0x2D,
    0x0F,
    0xB0,
    0x54,
    0xBB,
    0x16,
]
INV_SBOX = [0] * 256
for i, val in enumerate(SBOX):
    INV_SBOX[val] = i
RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]


def xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else (a << 1) & 0xFF


def mul_gf(a, b):
    res = 0
    for _ in range(8):
        if b & 1:
            res ^= a
        a = xtime(a)
        b >>= 1
    return res


def key_expansion(key):
    w = list(key)
    for i in range(4, 44):
        temp = w[(i - 1) * 4 : i * 4]
        if i % 4 == 0:
            temp = [SBOX[b] for b in temp[1:] + temp[:1]]
            temp[0] ^= RCON[i // 4]
        for j in range(4):
            w.append(w[(i - 4) * 4 + j] ^ temp[j])
    return [w[i * 16 : (i + 1) * 16] for i in range(11)]


def mix_columns(s, inv=False):
    for i in range(0, 16, 4):
        c = s[i : i + 4]
        if not inv:
            s[i] = xtime(c[0]) ^ (xtime(c[1]) ^ c[1]) ^ c[2] ^ c[3]
            s[i + 1] = c[0] ^ xtime(c[1]) ^ (xtime(c[2]) ^ c[2]) ^ c[3]
            s[i + 2] = c[0] ^ c[1] ^ xtime(c[2]) ^ (xtime(c[3]) ^ c[3])
            s[i + 3] = (xtime(c[0]) ^ c[0]) ^ c[1] ^ c[2] ^ xtime(c[3])
        else:
            s[i] = (
                mul_gf(c[0], 0x0E)
                ^ mul_gf(c[1], 0x0B)
                ^ mul_gf(c[2], 0x0D)
                ^ mul_gf(c[3], 0x09)
            )
            s[i + 1] = (
                mul_gf(c[0], 0x09)
                ^ mul_gf(c[1], 0x0E)
                ^ mul_gf(c[2], 0x0B)
                ^ mul_gf(c[3], 0x0D)
            )
            s[i + 2] = (
                mul_gf(c[0], 0x0D)
                ^ mul_gf(c[1], 0x09)
                ^ mul_gf(c[2], 0x0E)
                ^ mul_gf(c[3], 0x0B)
            )
            s[i + 3] = (
                mul_gf(c[0], 0x0B)
                ^ mul_gf(c[1], 0x0D)
                ^ mul_gf(c[2], 0x09)
                ^ mul_gf(c[3], 0x0E)
            )


def aes_main(block, round_keys, mode="encrypt"):
    state = list(block)
    if mode == "encrypt":
        # AddRoundKey
        for i in range(16):
            state[i] ^= round_keys[0][i]
        for r in range(1, 10):
            # SubBytes
            for i in range(16):
                state[i] = SBOX[state[i]]
            # ShiftRows.
            state[1], state[5], state[9], state[13] = (
                state[5],
                state[9],
                state[13],
                state[1],
            )
            state[2], state[6], state[10], state[14] = (
                state[10],
                state[14],
                state[2],
                state[6],
            )
            state[3], state[7], state[11], state[15] = (
                state[15],
                state[3],
                state[7],
                state[11],
            )
            # MixColumns
            mix_columns(state)
            # AddRoundKey
            for i in range(16):
                state[i] ^= round_keys[r][i]

        # SubBytes
        for i in range(16):
            state[i] = SBOX[state[i]]
        # ShiftRows.
        state[1], state[5], state[9], state[13] = (
            state[5],
            state[9],
            state[13],
            state[1],
        )
        state[2], state[6], state[10], state[14] = (
            state[10],
            state[14],
            state[2],
            state[6],
        )
        state[3], state[7], state[11], state[15] = (
            state[15],
            state[3],
            state[7],
            state[11],
        )
        # AddRoundKey
        for i in range(16):
            state[i] ^= round_keys[10][i]
    else:
        for i in range(16):
            state[i] ^= round_keys[10][i]
        for r in range(9, 0, -1):
            # InvShiftRows
            state[1], state[5], state[9], state[13] = (
                state[13],
                state[1],
                state[5],
                state[9],
            )
            state[2], state[6], state[10], state[14] = (
                state[10],
                state[14],
                state[2],
                state[6],
            )
            state[3], state[7], state[11], state[15] = (
                state[7],
                state[11],
                state[15],
                state[3],
            )
            # InvSubBytes
            for i in range(16):
                state[i] = INV_SBOX[state[i]]
            # AddRoundKey
            for i in range(16):
                state[i] ^= round_keys[r][i]
            # InvMixColumns
            mix_columns(state, inv=True)

        # InvShiftRows
        state[1], state[5], state[9], state[13] = (
            state[13],
            state[1],
            state[5],
            state[9],
        )
        state[2], state[6], state[10], state[14] = (
            state[10],
            state[14],
            state[2],
            state[6],
        )
        state[3], state[7], state[11], state[15] = (
            state[7],
            state[11],
            state[15],
            state[3],
        )
        # InvSubBytes
        for i in range(16):
            state[i] = INV_SBOX[state[i]]
        # AddRoundKey
        for i in range(16):
            state[i] ^= round_keys[0][i]

    return bytes(state)


# XỬ LÝ ĐỌC/GHI FILE VÀ GIAO DIỆN
def main():
    print("======================================================")
    print(" BÀI TẬP NHÓM 18: MÃ HÓA VÀ GIẢI MÃ FILE BẰNG AES-128")
    print("======================================================")

    # 1. Nhập thông tin Khóa và File
    key_in = input("[?] Nhập khóa mã hóa (tối đa 16 ký tự): ")
    key_str = key_in.encode("utf-8").ljust(16, b"\0")[:16]  # Đảm bảo đúng 16 byte

    input_file = input("[?] Nhập tên file cần mã hóa (VD: input.txt): ")

    if not os.path.exists(input_file):
        print(f"[!] Lỗi: Không tìm thấy file '{input_file}' trong thư mục hiện tại.")
        print("[!] Vui lòng tạo một file .txt và chạy lại chương trình.")
        return

    # Đọc dữ liệu từ file
    with open(input_file, "rb") as f:
        raw_data = f.read()
    print(f"\n[+] Đã tải file '{input_file}' ({len(raw_data)} bytes).")

    # Mở rộng khóa
    r_keys = key_expansion(key_str)

    # 2. THỰC HIỆN MÃ HÓA
    print("[*] Đang tiến hành MÃ HÓA...")
    # Padding PKCS#7 cho file gốc
    pad_len = 16 - (len(raw_data) % 16)
    data_to_encrypt = raw_data + bytes([pad_len] * pad_len)

    start_e = time.perf_counter()
    encrypted = b"".join(
        [
            aes_main(data_to_encrypt[i : i + 16], r_keys, "encrypt")
            for i in range(0, len(data_to_encrypt), 16)
        ]
    )
    end_e = time.perf_counter()
    time_encrypt = end_e - start_e

    enc_filename = "encrypted_file.bin"
    with open(enc_filename, "wb") as f:
        f.write(encrypted)

    # 3. THỰC HIỆN GIẢI MÃ
    print("[*] Đang tiến hành GIẢI MÃ...")

    start_d = time.perf_counter()
    decrypted_raw = b"".join(
        [
            aes_main(encrypted[i : i + 16], r_keys, "decrypt")
            for i in range(0, len(encrypted), 16)
        ]
    )

    # Gỡ Padding
    pad_len = decrypted_raw[-1]
    if 0 < pad_len <= 16:
        final_data = decrypted_raw[:-pad_len]
    else:
        final_data = decrypted_raw
    end_d = time.perf_counter()
    time_decrypt = end_d - start_d

    dec_filename = "decrypted_" + input_file
    with open(dec_filename, "wb") as f:
        f.write(final_data)

    # 4. TỔNG KẾT BÁO CÁO
    print("\n================ TỔNG KẾT KẾT QUẢ ================")
    print(f"1. File gốc:      {input_file}")
    print(f"2. File mã hóa:   {enc_filename}")
    print(f"3. File giải mã:  {dec_filename}")
    print("-" * 50)
    print(f"[THỜI GIAN MÃ HÓA]:  {time_encrypt:.6f} giây")
    print(f"[THỜI GIAN GIẢI MÃ]: {time_decrypt:.6f} giây")
    print("======================================================")


if __name__ == "__main__":
    main()
