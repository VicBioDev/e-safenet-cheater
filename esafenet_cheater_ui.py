import socket
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import os
import sys
import subprocess
import random
import time

# Define chunk size
chunk_size = 1024


def is_encrypted_powershell(file_path: Path, search_string="Esafenet"):
    encrypted_extensions = [
        ".txt",
        ".csv",
        ".jpg",
        ".gif",
        ".png",
        ".bmp",
        ".jpeg",
        ".tiff",
        ".docx",
        ".xlsx",
        ".pptx",
        ".pdf",
        ".doc",
        ".xls",
        ".ppt",
        ".mp3",
        ".mp4",
        ".avi",
        ".mkv",
        ".mov",
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz",
        ".html",
        ".htm",
        ".xml",
        ".json",
        ".js",
        ".css",
        ".php",
        ".py",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".rb",
        ".go",
        ".rs",
        ".swift",
        ".sh",
        ".bat",
        ".exe",
        ".dll",
        ".iso",
        ".img",
        ".dmg",
    ]
    file_extension = file_path.suffix.lower()
    if file_extension not in encrypted_extensions:
        print(f"Found normal file: {file_path}")
        return False

    ps_script = f"""
        $filePath = "{file_path}"
        $chunkSize = 1024
        $searchString = "{search_string}"

        try {{
            $fileStream = [System.IO.File]::OpenRead($filePath)
            $bytes = New-Object Byte[] $chunkSize
            $numBytesRead = $fileStream.Read($bytes, 0, $chunkSize)
            $fileStream.Close()
            if ($numBytesRead -eq 0) {{
                exit
            }}
            $firstChunkAsString = [System.Text.Encoding]::ASCII.GetString($bytes)
            return $firstChunkAsString.Contains($searchString)
        }} catch {{
            exit
        }}
    """

    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        output = result.stdout.strip()
        is_found = output.lower() == "true"
        if is_found:
            print(f"Found encrypted file: {file_path}")
            return True
        print(f"Found normal file: {file_path}")
        return False
    except subprocess.CalledProcessError:
        print(f"Unknown file: {file_path}")
        return False


def decrypt_file(file_path: Path):
    print(f"Decrypting file: {file_path.absolute()}")
    temp_file_path = file_path.with_suffix(f"{file_path.suffix}.temp")
    with file_path.open("rb") as input_file, temp_file_path.open("wb") as output_file:
        while True:
            chunk = input_file.read(chunk_size)
            if not chunk:
                break
            output_file.write(chunk)

    file_stat = os.stat(file_path)
    create_time = file_stat.st_ctime
    modified_time = file_stat.st_mtime
    encrypted_file_path = file_path.with_suffix(f".encrypted{file_path.suffix}")

    subprocess.run(
        [
            "powershell",
            "Rename-Item",
            f'"{file_path.absolute()}"',
            f'"{encrypted_file_path.absolute()}"',
        ],
        creationflags=subprocess.CREATE_NO_WINDOW,
    )
    os.utime(temp_file_path, (create_time, modified_time))
    time.sleep(random.uniform(0, 1))
    subprocess.run(
        [
            "powershell",
            "Rename-Item",
            f'"{temp_file_path.absolute()}"',
            f'"{file_path.absolute()}"',
        ],
        creationflags=subprocess.CREATE_NO_WINDOW,
    )


def main_ui(paths):
    root = tk.Tk()
    root.title("亿赛通解密")
    root.configure(padx=20, pady=20)

    # Center the window
    root.update_idletasks()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"+{x}+{y}")

    files = []

    # Find encrypted files
    for p in paths:
        if p.exists():
            if p.is_dir():
                for f in p.rglob("*"):
                    if f.is_file() and is_encrypted_powershell(f):
                        files.append(f)
            elif p.is_file() and is_encrypted_powershell(p):
                files.append(p)

    tk.Label(root, text="已找到加密文件:").pack(padx=10, pady=10)
    listbox = tk.Listbox(root, width=60, selectmode="extended")
    for f in files:
        listbox.insert(tk.END, f.name)
    listbox.pack(padx=10, pady=10)

    def select_all(event):
        listbox.select_set(0, tk.END)

    listbox.bind("<Control-a>", select_all)

    def decrypt_selected():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("信息", "未选择任何文件。")
            return
        for idx in sel:
            path_to_decrypt = files[idx]  # Use the files list to get the full path
            if path_to_decrypt.exists():
                decrypt_file(path_to_decrypt)
        # 解密完成后，提示用户是否删除文件
        answer = messagebox.askyesno("确认", "解密完成，是否删除原始文件？")
        if answer:
            for idx in sel:
                file_path = files[idx]
                path_to_delete = file_path.with_suffix(f".encrypted{file_path.suffix}")
                if path_to_delete.exists():
                    os.remove(path_to_delete)
            messagebox.showinfo("信息", "原始文件已删除。")
        else:
            messagebox.showinfo("信息", "已保留原始文件。")
        root.destroy()  # Close the program after decryption

    tk.Button(root, text="解密所选文件", command=decrypt_selected).pack(
        padx=10, pady=10
    )
    # Remove or comment out the delete_selected function and button creation:
    # def delete_selected():
    #     ...
    #
    # tk.Button(root, text="Delete Selected", command=delete_selected).pack()
    root.mainloop()


if __name__ == "__main__":
    print(sys.argv)
    paths = [Path(arg) for arg in sys.argv[1:]]
    print(f"Paths: {paths}")
    if len(paths) == 1 and paths[0].is_file():
        file_path = paths[0]
        if is_encrypted_powershell(file_path):
            decrypt_file(file_path)
            answer = messagebox.askyesno("确认", "解密完成，是否保留原始加密文件？")
            if not answer:
                encrypted_file_path = file_path.with_suffix(
                    f".encrypted{file_path.suffix}"
                )
                if encrypted_file_path.exists():
                    os.remove(encrypted_file_path)
                messagebox.showinfo("信息", "原始加密文件已删除。")
            else:
                messagebox.showinfo("信息", "原始加密文件已保留。")
        else:
            messagebox.showinfo("信息", "此文件未加密")
        sys.exit()
    main_ui(paths)
