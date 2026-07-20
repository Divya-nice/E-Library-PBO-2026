# view.py
# Branch: feature/view-ui  (Lunny)
# Fokus: UI/Tampilan Tkinter untuk E-Library
# CATATAN: Belum ada SQLite, CRUD, event button, atau controller.
#          Semua widget hanya tampilan dan siap dihubungkan
#          ke Controller/Model oleh tim lain.

import tkinter as tk
from tkinter import ttk


# ============================================================
#  KONFIGURASI WARNA & STYLE
# ============================================================
class Style:
    BG = "#f4f6f9"
    SIDEBAR = "#2c3e50"
    SIDEBAR_ACTIVE = "#1abc9c"
    CARD = "#ffffff"
    PRIMARY = "#3498db"
    TEXT = "#2c3e50"
    WHITE = "#ffffff"

    FONT_TITLE = ("Segoe UI", 20, "bold")
    FONT_SUBTITLE = ("Segoe UI", 14, "bold")
    FONT_NORMAL = ("Segoe UI", 10)
    FONT_CARD_NUM = ("Segoe UI", 26, "bold")


# ============================================================
#  BASE PAGE  (Inheritance: semua halaman turunan dari tk.Frame)
# ============================================================
class BasePage(tk.Frame):
    """Kelas dasar untuk semua halaman. Menerapkan Inheritance."""

    def __init__(self, parent, title=""):
        super().__init__(parent, bg=Style.BG)
        self._build_header(title)

    def _build_header(self, title):
        tk.Label(
            self, text=title, font=Style.FONT_TITLE,
            bg=Style.BG, fg=Style.TEXT, anchor="w"
        ).pack(fill="x", padx=20, pady=(20, 10))
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20)


# ============================================================
#  KOMPONEN FORM (Encapsulation input widgets, reusable)
# ============================================================
class LabeledEntry(tk.Frame):
    """Gabungan Label + Entry supaya rapi dan reusable."""

    def __init__(self, parent, label_text, width=25):
        super().__init__(parent, bg=Style.BG)
        tk.Label(self, text=label_text, font=Style.FONT_NORMAL,
                 bg=Style.BG, fg=Style.TEXT, width=14, anchor="w").pack(side="left")
        self.entry = ttk.Entry(self, width=width)
        self.entry.pack(side="left", padx=5)

    def get(self):
        return self.entry.get()

    def set(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)


class LabeledCombobox(tk.Frame):
    def __init__(self, parent, label_text, values=None, width=23):
        super().__init__(parent, bg=Style.BG)
        tk.Label(self, text=label_text, font=Style.FONT_NORMAL,
                 bg=Style.BG, fg=Style.TEXT, width=14, anchor="w").pack(side="left")
        self.combo = ttk.Combobox(self, values=values or [], width=width, state="readonly")
        self.combo.pack(side="left", padx=5)


# ============================================================
#  HALAMAN 1 : DASHBOARD
# ============================================================
class DashboardPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent, title="Dashboard E-Library")

        tk.Label(self, text="Ringkasan Data Perpustakaan Digital",
                 font=Style.FONT_NORMAL, bg=Style.BG,
                 fg="#7f8c8d").pack(anchor="w", padx=20, pady=(10, 20))

        card_area = tk.Frame(self, bg=Style.BG)
        card_area.pack(fill="x", padx=20)

        cards = [
            ("Total Buku", "0", "#3498db"),
            ("Total Anggota", "0", "#2ecc71"),
            ("Buku Dipinjam", "0", "#e67e22"),
            ("Buku Terlambat", "0", "#e74c3c"),
        ]
        for i, (title, value, color) in enumerate(cards):
            self._create_card(card_area, title, value, color, i)
            card_area.grid_columnconfigure(i, weight=1)

    def _create_card(self, parent, title, value, color, col):
        card = tk.Frame(parent, bg=Style.CARD, bd=0, relief="flat")
        card.grid(row=0, column=col, padx=10, pady=10, sticky="nsew", ipadx=10, ipady=15)
        tk.Frame(card, bg=color, height=5).pack(fill="x")
        tk.Label(card, text=value, font=Style.FONT_CARD_NUM,
                 bg=Style.CARD, fg=color).pack(pady=(15, 5))
        tk.Label(card, text=title, font=Style.FONT_NORMAL,
                 bg=Style.CARD, fg=Style.TEXT).pack(pady=(0, 15))


# ============================================================
#  HALAMAN 2 : DATA BUKU
# ============================================================
class DataBukuPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent, title="Data Buku")

        container = tk.Frame(self, bg=Style.BG)
        container.pack(fill="both", expand=True, padx=20, pady=15)

        form = tk.LabelFrame(container, text="Form Buku", bg=Style.BG,
                             fg=Style.TEXT, font=Style.FONT_SUBTITLE, padx=15, pady=15)
        form.pack(fill="x")

        self.f_id = LabeledEntry(form, "ID Buku")
        self.f_judul = LabeledEntry(form, "Judul")
        self.f_penulis = LabeledEntry(form, "Penulis")
        self.f_penerbit = LabeledEntry(form, "Penerbit")
        self.f_tahun = LabeledEntry(form, "Tahun Terbit")
        self.f_kategori = LabeledEntry(form, "Kategori")
        self.f_stok = LabeledEntry(form, "Stok")

        for w in (self.f_id, self.f_judul, self.f_penulis, self.f_penerbit,
                  self.f_tahun, self.f_kategori, self.f_stok):
            w.pack(anchor="w", pady=4)

        btn_area = tk.Frame(container, bg=Style.BG)
        btn_area.pack(fill="x", pady=10)
        for text, color in [("Tambah", "#2ecc71"), ("Update", "#3498db"),
                            ("Hapus", "#e74c3c"), ("Reset", "#95a5a6")]:
            tk.Button(btn_area, text=text, bg=color, fg=Style.WHITE,
                      font=Style.FONT_NORMAL, width=12, relief="flat",
                      cursor="hand2").pack(side="left", padx=5)

        cols = ("ID", "Judul", "Penulis", "Penerbit", "Tahun", "Kategori", "Stok")
        self.tree = ttk.Treeview(container, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=110, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=(10, 0))


# ============================================================
#  HALAMAN 3 : DATA ANGGOTA
# ============================================================
class DataAnggotaPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent, title="Data Anggota")

        container = tk.Frame(self, bg=Style.BG)
        container.pack(fill="both", expand=True, padx=20, pady=15)

        form = tk.LabelFrame(container, text="Form Anggota", bg=Style.BG,
                             fg=Style.TEXT, font=Style.FONT_SUBTITLE, padx=15, pady=15)
        form.pack(fill="x")

        self.f_id = LabeledEntry(form, "ID Anggota")
        self.f_nama = LabeledEntry(form, "Nama")
        self.f_alamat = LabeledEntry(form, "Alamat")
        self.f_hp = LabeledEntry(form, "Nomor HP")

        for w in (self.f_id, self.f_nama, self.f_alamat, self.f_hp):
            w.pack(anchor="w", pady=4)

        btn_area = tk.Frame(container, bg=Style.BG)
        btn_area.pack(fill="x", pady=10)
        for text, color in [("Tambah", "#2ecc71"), ("Update", "#3498db"),
                            ("Hapus", "#e74c3c"), ("Reset", "#95a5a6")]:
            tk.Button(btn_area, text=text, bg=color, fg=Style.WHITE,
                      font=Style.FONT_NORMAL, width=12, relief="flat",
                      cursor="hand2").pack(side="left", padx=5)

        cols = ("ID", "Nama", "Alamat", "Nomor HP")
        self.tree = ttk.Treeview(container, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=180, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=(10, 0))


# ============================================================
#  HALAMAN 4 : PEMINJAMAN
# ============================================================
class PeminjamanPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent, title="Peminjaman")

        container = tk.Frame(self, bg=Style.BG)
        container.pack(fill="both", expand=True, padx=20, pady=15)

        form = tk.LabelFrame(container, text="Form Peminjaman", bg=Style.BG,
                             fg=Style.TEXT, font=Style.FONT_SUBTITLE, padx=15, pady=15)
        form.pack(fill="x")

        self.f_id = LabeledEntry(form, "ID Pinjam")
        self.f_anggota = LabeledCombobox(form, "Anggota", values=[])
        self.f_buku = LabeledCombobox(form, "Buku", values=[])
        self.f_tgl_pinjam = LabeledEntry(form, "Tanggal Pinjam")
        self.f_batas = LabeledEntry(form, "Batas Kembali")

        for w in (self.f_id, self.f_anggota, self.f_buku,
                  self.f_tgl_pinjam, self.f_batas):
            w.pack(anchor="w", pady=4)

        btn_area = tk.Frame(container, bg=Style.BG)
        btn_area.pack(fill="x", pady=10)
        for text, color in [("Tambah", "#2ecc71"), ("Update", "#3498db"),
                            ("Hapus", "#e74c3c")]:
            tk.Button(btn_area, text=text, bg=color, fg=Style.WHITE,
                      font=Style.FONT_NORMAL, width=12, relief="flat",
                      cursor="hand2").pack(side="left", padx=5)

        cols = ("ID Pinjam", "Anggota", "Buku", "Tanggal Pinjam",
                "Batas Kembali", "Status")
        self.tree = ttk.Treeview(container, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=(10, 0))


# ============================================================
#  HALAMAN 5 : PENGEMBALIAN
# ============================================================
class PengembalianPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent, title="Pengembalian")

        container = tk.Frame(self, bg=Style.BG)
        container.pack(fill="both", expand=True, padx=20, pady=15)

        form = tk.LabelFrame(container, text="Form Pengembalian", bg=Style.BG,
                             fg=Style.TEXT, font=Style.FONT_SUBTITLE, padx=15, pady=15)
        form.pack(fill="x")

        self.f_pinjam = LabeledCombobox(form, "Peminjaman", values=[])
        self.f_tgl_kembali = LabeledEntry(form, "Tanggal Kembali")
        self.f_denda = LabeledEntry(form, "Denda")

        for w in (self.f_pinjam, self.f_tgl_kembali, self.f_denda):
            w.pack(anchor="w", pady=4)

        btn_area = tk.Frame(container, bg=Style.BG)
        btn_area.pack(fill="x", pady=10)
        tk.Button(btn_area, text="Proses Pengembalian", bg="#2ecc71",
                  fg=Style.WHITE, font=Style.FONT_NORMAL, width=20,
                  relief="flat", cursor="hand2").pack(side="left", padx=5)

        cols = ("ID", "Anggota", "Buku", "Tanggal Kembali", "Denda")
        self.tree = ttk.Treeview(container, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=(10, 0))


# ============================================================
#  MAIN WINDOW  (Sidebar + Menu Bar + Container Halaman)
# ============================================================
class ELibraryView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("E-Library - Sistem Manajemen Perpustakaan Digital")
        self.geometry("1100x650")
        self.configure(bg=Style.BG)

        self._build_menubar()
        self._build_layout()
        self._build_pages()
        self.show_page("Dashboard")

    # ---------- MENU BAR ----------
    def _build_menubar(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Keluar", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        master_menu = tk.Menu(menubar, tearoff=0)
        master_menu.add_command(label="Data Buku",
                                command=lambda: self.show_page("Data Buku"))
        master_menu.add_command(label="Data Anggota",
                                command=lambda: self.show_page("Data Anggota"))
        menubar.add_cascade(label="Master Data", menu=master_menu)

        trx_menu = tk.Menu(menubar, tearoff=0)
        trx_menu.add_command(label="Peminjaman",
                             command=lambda: self.show_page("Peminjaman"))
        trx_menu.add_command(label="Pengembalian",
                             command=lambda: self.show_page("Pengembalian"))
        menubar.add_cascade(label="Transaksi", menu=trx_menu)

        menubar.add_command(label="Dashboard",
                            command=lambda: self.show_page("Dashboard"))

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Tentang Aplikasi")
        menubar.add_cascade(label="Bantuan", menu=help_menu)

        self.config(menu=menubar)

    # ---------- LAYOUT (Sidebar + Content) ----------
    def _build_layout(self):
        self.sidebar = tk.Frame(self, bg=Style.SIDEBAR, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="\U0001F4DA E-Library", bg=Style.SIDEBAR,
                 fg=Style.WHITE, font=("Segoe UI", 16, "bold")).pack(pady=25)

        self.nav_buttons = {}
        for name in ["Dashboard", "Data Buku", "Data Anggota",
                     "Peminjaman", "Pengembalian"]:
            btn = tk.Button(self.sidebar, text=name, bg=Style.SIDEBAR,
                            fg=Style.WHITE, font=Style.FONT_NORMAL, bd=0,
                            relief="flat", anchor="w", padx=20, cursor="hand2",
                            activebackground=Style.SIDEBAR_ACTIVE,
                            activeforeground=Style.WHITE,
                            command=lambda n=name: self.show_page(n))
            btn.pack(fill="x", ipady=10)
            self.nav_buttons[name] = btn

        self.content = tk.Frame(self, bg=Style.BG)
        self.content.pack(side="right", fill="both", expand=True)

    # ---------- INISIALISASI HALAMAN ----------
    def _build_pages(self):
        self.pages = {
            "Dashboard": DashboardPage(self.content),
            "Data Buku": DataBukuPage(self.content),
            "Data Anggota": DataAnggotaPage(self.content),
            "Peminjaman": PeminjamanPage(self.content),
            "Pengembalian": PengembalianPage(self.content),
        }
        for page in self.pages.values():
            page.place(x=0, y=0, relwidth=1, relheight=1)

    # ---------- NAVIGASI (Polymorphism: semua page diperlakukan sama) ----------
    def show_page(self, name):
        page = self.pages.get(name)
        if page:
            page.tkraise()
        for n, btn in self.nav_buttons.items():
            btn.configure(bg=Style.SIDEBAR_ACTIVE if n == name else Style.SIDEBAR)


# ============================================================
#  ENTRY POINT (sementara untuk uji tampilan)
#  Nanti aplikasi dijalankan lewat main.py oleh Controller.
# ============================================================
if __name__ == "__main__":
    app = ELibraryView()
    app.mainloop()
