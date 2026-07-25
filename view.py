import tkinter as tk
from tkinter import ttk

# Widget kalender (klik tanggal/bulan/tahun). Tetap bisa diketik manual.
# Jika tkcalendar belum terpasang, otomatis memakai input teks biasa
# supaya aplikasi tetap bisa dijalankan.
try:
    from tkcalendar import DateEntry
    HAS_TKCALENDAR = True
except Exception:
    DateEntry = None
    HAS_TKCALENDAR = False


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

    def get(self):
        return self.combo.get()

    def set(self, value):
        self.combo.set(value)

    def set_values(self, values):
        self.combo["values"] = values


class LabeledDateEntry(tk.Frame):
    """Label + input tanggal berkalender.

    Pengguna bisa memilih tanggal/bulan/tahun lewat kalender ATAU
    mengetik manual dengan format DD-MM-YYYY. Menyediakan get()/set()
    dan atribut .entry supaya kompatibel dengan Controller (main.py).
    """

    def __init__(self, parent, label_text, width=25):
        super().__init__(parent, bg=Style.BG)
        tk.Label(self, text=label_text, font=Style.FONT_NORMAL,
                 bg=Style.BG, fg=Style.TEXT, width=14, anchor="w").pack(side="left")
        if HAS_TKCALENDAR:
            self.entry = DateEntry(self, width=width - 2,
                                   date_pattern="dd-mm-yyyy",
                                   state="normal")
        else:
            self.entry = ttk.Entry(self, width=width)
        self.entry.pack(side="left", padx=5)

    def get(self):
        return self.entry.get()

    def set(self, value):
        if value in (None, ""):
            try:
                self.entry.delete(0, tk.END)
            except Exception:
                pass
            return
        # Untuk DateEntry, set_date menyinkronkan kalender internal.
        if HAS_TKCALENDAR:
            try:
                self.entry.set_date(value)
                return
            except Exception:
                pass
        try:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, value)
        except Exception:
            pass


# ============================================================
#  HALAMAN 1 : DASHBOARD
# ============================================================
class DashboardPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent, title="Dashboard E-Library")

        tk.Label(self, text="Ringkasan Data Perpustakaan Digital", font=Style.FONT_NORMAL, bg=Style.BG, fg="#7f8c8d").pack(anchor="w", padx=20, pady=(10, 20))

        card_area = tk.Frame(self, bg=Style.BG)
        card_area.pack(fill="x", padx=20)

        # Label angka dashboard
        self.lbl_total_buku = self._create_card(card_area, "Total Buku", "#3498db", 0)
        self.lbl_total_anggota = self._create_card(card_area, "Total Anggota", "#2ecc71", 1)
        self.lbl_buku_dipinjam = self._create_card(card_area, "Buku Dipinjam", "#e67e22", 2)
        self.lbl_buku_terlambat = self._create_card(card_area, "Buku Terlambat", "#e74c3c", 3)

        for i in range(4):
            card_area.grid_columnconfigure(i, weight=1)

    def _create_card(self, parent, title, color, col):
        card = tk.Frame(parent, bg=Style.CARD)
        card.grid(row=0, column=col, padx=10, pady=10, sticky="nsew", ipadx=10, ipady=15)

        tk.Frame(card, bg=color, height=5).pack(fill="x")

        lbl = tk.Label(card, text="0", font=Style.FONT_CARD_NUM, bg=Style.CARD, fg=color)
        lbl.pack(pady=(15, 5))

        tk.Label(card, text=title, font=Style.FONT_NORMAL, bg=Style.CARD, fg=Style.TEXT).pack(pady=(0, 15))

        return lbl


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
        self.btn_tambah = tk.Button(btn_area, text="Tambah", bg="#2ecc71",
                                    fg=Style.WHITE, font=Style.FONT_NORMAL,
                                    width=12, relief="flat", cursor="hand2")
        self.btn_tambah.pack(side="left", padx=5)

        self.btn_update = tk.Button(btn_area, text="Update", bg="#3498db",
                                    fg=Style.WHITE, font=Style.FONT_NORMAL,
                                    width=12, relief="flat", cursor="hand2")
        self.btn_update.pack(side="left", padx=5)

        self.btn_hapus = tk.Button(btn_area, text="Hapus", bg="#e74c3c",
                                   fg=Style.WHITE, font=Style.FONT_NORMAL,
                                   width=12, relief="flat", cursor="hand2")
        self.btn_hapus.pack(side="left", padx=5)

        self.btn_reset = tk.Button(btn_area, text="Reset", bg="#95a5a6",
                                   fg=Style.WHITE, font=Style.FONT_NORMAL,
                                   width=12, relief="flat", cursor="hand2")
        self.btn_reset.pack(side="left", padx=5)

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
        self.btn_tambah = tk.Button(btn_area, text="Tambah", bg="#2ecc71",
                                    fg=Style.WHITE, font=Style.FONT_NORMAL,
                                    width=12, relief="flat", cursor="hand2")
        self.btn_tambah.pack(side="left", padx=5)

        self.btn_update = tk.Button(btn_area, text="Update", bg="#3498db",
                                    fg=Style.WHITE, font=Style.FONT_NORMAL,
                                    width=12, relief="flat", cursor="hand2")
        self.btn_update.pack(side="left", padx=5)

        self.btn_hapus = tk.Button(btn_area, text="Hapus", bg="#e74c3c",
                                   fg=Style.WHITE, font=Style.FONT_NORMAL,
                                   width=12, relief="flat", cursor="hand2")
        self.btn_hapus.pack(side="left", padx=5)

        self.btn_reset = tk.Button(btn_area, text="Reset", bg="#95a5a6",
                                   fg=Style.WHITE, font=Style.FONT_NORMAL,
                                   width=12, relief="flat", cursor="hand2")
        self.btn_reset.pack(side="left", padx=5)

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
        self.f_tgl_pinjam = LabeledDateEntry(form, "Tanggal Pinjam")
        self.f_batas = LabeledDateEntry(form, "Batas Kembali")

        for w in (self.f_id, self.f_anggota, self.f_buku,
                  self.f_tgl_pinjam, self.f_batas):
            w.pack(anchor="w", pady=4)

        btn_area = tk.Frame(container, bg=Style.BG)
        btn_area.pack(fill="x", pady=10)
        self.btn_tambah = tk.Button(btn_area, text="Tambah", bg="#2ecc71",
                                    fg=Style.WHITE, font=Style.FONT_NORMAL,
                                    width=12, relief="flat", cursor="hand2")
        self.btn_tambah.pack(side="left", padx=5)

        self.btn_update = tk.Button(btn_area, text="Update", bg="#3498db",
                                    fg=Style.WHITE, font=Style.FONT_NORMAL,
                                    width=12, relief="flat", cursor="hand2")
        self.btn_update.pack(side="left", padx=5)

        self.btn_hapus = tk.Button(btn_area, text="Hapus", bg="#e74c3c",
                                   fg=Style.WHITE, font=Style.FONT_NORMAL,
                                   width=12, relief="flat", cursor="hand2")
        self.btn_hapus.pack(side="left", padx=5)

        self.btn_reset = tk.Button(btn_area, text="Reset", bg="#95a5a6",
                                   fg=Style.WHITE, font=Style.FONT_NORMAL,
                                   width=12, relief="flat", cursor="hand2")
        self.btn_reset.pack(side="left", padx=5)

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

        form = tk.LabelFrame(container, text="Data Pengembalian Buku", bg=Style.BG, fg=Style.TEXT, font=Style.FONT_SUBTITLE, padx=15, pady=15)
        form.pack(fill="x")

        self.f_pinjam = LabeledCombobox(form, "Peminjaman", values=[], width=45)
        self.f_tgl_kembali = LabeledDateEntry(form, "Tanggal Kembali", width=45)
        self.f_denda = LabeledEntry(form, "Denda", width=45)
        self.f_denda.entry.config(state="readonly")

        for w in (self.f_pinjam, self.f_tgl_kembali, self.f_denda):
            w.pack(fill="x", pady=4)

        # Keterangan batas maksimal pengembalian (diisi otomatis oleh Controller)
        self.lbl_info = tk.Label(
            form,
            text="\u2139\ufe0f  Pilih data peminjaman untuk melihat batas pengembalian.",
            font=Style.FONT_NORMAL, bg=Style.BG, fg="#e67e22",
            anchor="w", justify="left", wraplength=700
        )
        self.lbl_info.pack(fill="x", pady=(8, 0))

        btn_area = tk.Frame(container, bg=Style.BG)
        btn_area.pack(fill="x", pady=10)

        self.btn_proses = tk.Button(btn_area, text="Kembalikan Buku", bg="#2ecc71",
                                    fg=Style.WHITE, font=Style.FONT_NORMAL,
                                    width=20, relief="flat", cursor="hand2")
        self.btn_proses.pack(side="left", padx=5)

        cols = ("ID", "Anggota", "Buku", "Batas Kembali", "Tanggal Kembali", "Denda")
        self.tree = ttk.Treeview(container, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=(10, 0))


# ============================================================
#  HALAMAN 6 : TENTANG APLIKASI
# ============================================================
class TentangPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent, title="Tentang Aplikasi")

        container = tk.Frame(self, bg=Style.BG)
        container.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(container, text="\U0001F4DA E-Library", font=("Segoe UI", 22, "bold"),
                 bg=Style.BG, fg=Style.SIDEBAR).pack(anchor="w", pady=(0, 5))
        tk.Label(container, text="Sistem Manajemen Perpustakaan Digital berbasis desktop.",
                 font=Style.FONT_NORMAL, bg=Style.BG, fg="#7f8c8d").pack(anchor="w", pady=(0, 15))

        self._baris(container, "Deskripsi",
                    "Aplikasi untuk mengelola data buku, anggota, peminjaman, dan "
                    "pengembalian buku beserta perhitungan denda otomatis.")
        self._baris(container, "Teknologi", "Python, Tkinter, SQLite")
        self._baris(container, "Arsitektur", "MVC (Model - View - Controller)")
        self._baris(container, "Versi", "1.0")

        ttk.Separator(container, orient="horizontal").pack(fill="x", pady=15)

        tk.Label(container, text="Tim Pengembang", font=Style.FONT_SUBTITLE,
                 bg=Style.BG, fg=Style.TEXT).pack(anchor="w", pady=(0, 8))
        self._baris(container, "Divya Harinda Verlita", "241230011 \u2014 Controller")
        self._baris(container, "Merllinsha Lunny", "241230021 \u2014 View (Antarmuka)")
        self._baris(container, "Haliza Zulqa Aulia", "241230002 \u2014 Model (Database)")

        ttk.Separator(container, orient="horizontal").pack(fill="x", pady=15)

        self._baris(container, "Dosen Pengampu", "Rizki Surtiyan Surya, M.Kom.")
        self._baris(container, "Program Studi", "Sistem Informasi")
        self._baris(container, "Universitas", "Universitas Muhammadiyah Pontianak")
        self._baris(container, "Tahun", "2026")

    def _baris(self, parent, judul, isi):
        row = tk.Frame(parent, bg=Style.BG)
        row.pack(fill="x", pady=3, anchor="w")
        tk.Label(row, text=judul, font=("Segoe UI", 10, "bold"), bg=Style.BG,
                 fg=Style.TEXT, width=22, anchor="w").pack(side="left")
        tk.Label(row, text=isi, font=Style.FONT_NORMAL, bg=Style.BG,
                 fg=Style.TEXT, anchor="w", justify="left", wraplength=650).pack(side="left")


# ============================================================
#  MAIN WINDOW  (Sidebar + Container Halaman)
# ============================================================
class ELibraryView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("E-Library - Sistem Manajemen Perpustakaan Digital")
        self.geometry("1100x650")
        self.configure(bg=Style.BG)

        self._build_layout()
        self._build_pages()
        self.show_page("Dashboard")

    # ---------- LAYOUT (Sidebar + Content) ----------
    def _build_layout(self):
        self.sidebar = tk.Frame(self, bg=Style.SIDEBAR, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="\U0001F4DA E-Library", bg=Style.SIDEBAR,
                 fg=Style.WHITE, font=("Segoe UI", 16, "bold")).pack(pady=25)

        self.nav_buttons = {}
        for name in ["Dashboard", "Data Buku", "Data Anggota",
                     "Peminjaman", "Pengembalian", "Tentang Aplikasi"]:
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
            "Tentang Aplikasi": TentangPage(self.content),
        }

        self.dashboard_page = self.pages["Dashboard"]
        self.buku_page = self.pages["Data Buku"]
        self.anggota_page = self.pages["Data Anggota"]
        self.peminjaman_page = self.pages["Peminjaman"]
        self.pengembalian_page = self.pages["Pengembalian"]
        self.tentang_page = self.pages["Tentang Aplikasi"]

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
