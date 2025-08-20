import tkinter as tk
from tkinter import filedialog, font, messagebox

class SimpleNotepad(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SimpleNotepad")
        self.geometry("600x400")

        # フォント設定
        self.current_font = font.Font(family="MS Gothic", size=12)

        # テキストボックス
        self.text = tk.Text(self, wrap="none", undo=True, font=self.current_font)
        self.text.pack(fill="both", expand=True)

        # メニュー
        self.create_menu()

        # ステータスバー
        self.status = tk.Label(self, text="", anchor="w")
        self.status.pack(side="bottom", fill="x")

        # イベントバインド
        self.text.bind("<<Modified>>", self.update_status)
        self.text.bind("<KeyRelease>", self.update_status)
        self.text.bind("<ButtonRelease>", self.update_status)

        self.update_status()

    def create_menu(self):
        menubar = tk.Menu(self)

        # ファイル
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="開く", command=self.open_file)
        filemenu.add_command(label="保存", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="終了", command=self.quit)
        menubar.add_cascade(label="ファイル", menu=filemenu)

        # 編集
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="全選択", command=lambda: self.text.tag_add("sel", "1.0", "end"))
        editmenu.add_command(label="切り取り", command=lambda: self.text.event_generate("<<Cut>>"))
        editmenu.add_command(label="コピー", command=lambda: self.text.event_generate("<<Copy>>"))
        editmenu.add_command(label="ペースト", command=lambda: self.text.event_generate("<<Paste>>"))
        editmenu.add_separator()
        editmenu.add_command(label="フォント設定", command=self.change_font)
        menubar.add_cascade(label="編集", menu=editmenu)

        # ヘルプ
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="バージョン情報", command=self.show_version)
        menubar.add_cascade(label="ヘルプ", menu=helpmenu)

        self.config(menu=menubar)

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            with open(filepath, "r", encoding="utf-8") as f:
                self.text.delete("1.0", "end")
                self.text.insert("1.0", f.read())
            self.update_status()

    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", "end-1c"))

    def change_font(self):
        # TkinterにはC#みたいなFontDialogがないので簡易実装
        new_font = font.Font(family="MS Gothic", size=16)  # 固定的に変更する例
        self.current_font = new_font
        self.text.configure(font=self.current_font)
        self.update_status()

    def update_status(self, event=None):
        total_lines = int(self.text.index('end-1c').split('.')[0])
        total_chars = len(self.text.get("1.0", "end-1c"))
        current_index = self.text.index("insert").split(".")
        current_line = current_index[0]
        current_char = current_index[1]

        font_info = f"{self.current_font.actual('family')}, {self.current_font.actual('size')}pt"

        self.status.config(
            text=f"行数: {total_lines} | 選択行: {current_line} | 文字数: {total_chars} | "
                 f"カーソル位置: {current_char} | フォント: {font_info}"
        )

    def show_version(self):
        messagebox.showinfo("バージョン情報",
                            "SimpleNotepad\nVersion: 1.0.0\n作者: 削除くん")

if __name__ == "__main__":
    app = SimpleNotepad()
    app.mainloop()
