# Import
import tkinter as tk
from tkinter import messagebox

import model
from view import ELibraryView
from datetime import datetime

# Class Controller
class Controller:

#1. Inisialisasi
    def __init__(self):
        # Membuat database
        model.create_tables()

        # Membuat tampilan
        self.app = ELibraryView()

        # Hubungkan event
        self.bind_events()

        # Tampilkan data awal
        self.load_dashboard()
        self.load_buku()
        self.load_combo_buku()
        self.load_anggota()
        self.load_combo_anggota()
        self.load_pengembalian()
        self.load_combo_pengembalian()
        self.load_peminjaman()

    def bind_events(self):
        # Data Buku
        self.app.buku_page.btn_tambah.config(command=self.tambah_buku)
        self.app.buku_page.btn_update.config(command=self.update_buku)
        self.app.buku_page.btn_hapus.config(command=self.hapus_buku)
        self.app.buku_page.btn_reset.config(command=self.reset_buku)
        
        self.app.buku_page.tree.bind("<<TreeviewSelect>>", self.pilih_buku)

        # Data Anggota
        self.app.anggota_page.btn_tambah.config(command=self.tambah_anggota)
        self.app.anggota_page.btn_update.config(command=self.update_anggota)
        self.app.anggota_page.btn_hapus.config(command=self.hapus_anggota)
        self.app.anggota_page.btn_reset.config(command=self.reset_anggota)

        self.app.anggota_page.tree.bind("<<TreeviewSelect>>", self.pilih_anggota)

        # Data Peminjaman
        self.app.peminjaman_page.btn_tambah.config(command=self.tambah_peminjaman)
        self.app.peminjaman_page.btn_update.config(command=self.update_peminjaman)
        self.app.peminjaman_page.btn_hapus.config(command=self.hapus_peminjaman)
        self.app.peminjaman_page.btn_reset.config(command=self.reset_peminjaman)

        self.app.peminjaman_page.tree.bind("<<TreeviewSelect>>", self.pilih_peminjaman)

        # Data Pengembalian
        self.app.pengembalian_page.btn_proses.config(command=self.proses_pengembalian)
        self.app.pengembalian_page.f_tgl_kembali.entry.bind("<FocusOut>", self.hitung_denda_otomatis)
    
# 2. Load data
    # Menampilkan data di dashboard
    def load_dashboard(self):
        page = self.app.dashboard_page

        total_buku = model.count_buku()
        total_anggota = model.count_anggota()
        dipinjam = model.count_dipinjam()
        terlambat = model.count_terlambat()

        print("Dashboard")
        print("Buku :", total_buku)
        print("Anggota :", total_anggota)
        print("Dipinjam :", dipinjam)
        print("Terlambat :", terlambat)

        page.lbl_total_buku.config(text=str(total_buku))
        page.lbl_total_anggota.config(text=str(total_anggota))
        page.lbl_buku_dipinjam.config(text=str(dipinjam))
        page.lbl_buku_terlambat.config(text=str(terlambat))

    def load_combobox(self):
        page = self.app.peminjaman_page
        buku = model.get_all_buku()
        anggota = model.get_all_anggota()

        page.f_buku.combo["values"] = [
            f"{row[0]} - {row[1]}"
            for row in buku
        ]

        page.f_anggota.combo["values"] = [
            f"{row[0]} - {row[1]}"
            for row in anggota
        ]

# 3. Fitur Buku  
    # Menampilkan data buku
    def load_buku(self):
        page = self.app.buku_page

        for item in page.tree.get_children():
            page.tree.delete(item)

        data = model.get_all_buku()

        for row in data:
            page.tree.insert("", "end", values=row)
    
    # Menambahkan buku
    def tambah_buku(self):
        page = self.app.buku_page

        berhasil = model.create_buku(
            page.f_judul.get(),
            page.f_penulis.get(),
            page.f_penerbit.get(),
            page.f_tahun.get(),
            page.f_kategori.get(),
            page.f_stok.get()
        )

        if berhasil:
            self.load_buku()
            self.load_combo_buku()
            self.reset_buku()
            self.load_dashboard()

            messagebox.showinfo(
                "Berhasil",
                "Data buku berhasil ditambahkan."
            )

        else:
            messagebox.showerror(
                "Gagal",
                "Data buku tidak dapat disimpan."
            )
    
    # Memilih data buku
    def pilih_buku(self, event):
        page = self.app.buku_page
        selected = page.tree.focus()

        if not selected:
            return
        values = page.tree.item(selected)["values"]

        page.f_id.entry.config(state="normal")
        page.f_id.set(values[0])
        page.f_id.entry.config(state="readonly")
        page.f_judul.set(values[1])
        page.f_penulis.set(values[2])
        page.f_penerbit.set(values[3])
        page.f_tahun.set(values[4])
        page.f_kategori.set(values[5])
        page.f_stok.set(values[6])
    
    # Mengupdate data buku
    def update_buku(self):
        page = self.app.buku_page
        berhasil = model.update_buku(
            page.f_id.get(),
            page.f_judul.get(),
            page.f_penulis.get(),
            page.f_penerbit.get(),
            page.f_tahun.get(),
            page.f_kategori.get(),
            page.f_stok.get()
        )

        if berhasil:
            self.load_buku()
            self.load_combo_buku()
            self.reset_buku()
            messagebox.showinfo(
                "Berhasil",
                "Data buku berhasil diupdate."
            )

        else:
            messagebox.showerror(
                "Gagal",
                "Update data gagal."
        )
            
    # Menghapus data buku
    def hapus_buku(self):
        page = self.app.buku_page

        if page.f_id.get() == "":
            messagebox.showwarning(
                "Peringatan",
                "Pilih data terlebih dahulu."
            )
            return

        jawab = messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus data?"
        )

        if not jawab:
            return

        berhasil = model.delete_buku(
            page.f_id.get()
        )

        if berhasil:            
            self.load_buku()
            self.load_combo_buku()
            self.reset_buku()
            messagebox.showinfo(
                "Berhasil",
                "Data berhasil dihapus."
            )

        else:
            messagebox.showerror(
                "Gagal",
                "Data gagal dihapus."
        )

    # Merefresh form data buku
    def reset_buku(self):
        page = self.app.buku_page

        page.f_id.entry.config(state="readonly")
        page.f_id.set("")
        page.f_judul.set("")
        page.f_penulis.set("")
        page.f_penerbit.set("")
        page.f_tahun.set("")
        page.f_kategori.set("")
        page.f_stok.set("")
    
    # Combo buku
    def load_combo_buku(self):
        data = model.get_all_buku()
        self.daftar_buku = {}
        nama_buku = []

        for row in data:
            self.daftar_buku[row[1]] = row[0]
            nama_buku.append(row[1])

        self.app.peminjaman_page.f_buku.combo["values"] = nama_buku

# 4. Fitur Anggota
    # Menampilkan data anggota
    def load_anggota(self):
        page = self.app.anggota_page

        for item in page.tree.get_children():
            page.tree.delete(item)

        data = model.get_all_anggota()

        for row in data:
            page.tree.insert("", "end", values=row)
    
    # Menambahkan data anggota
    def tambah_anggota(self):
        page = self.app.anggota_page
        berhasil = model.create_anggota(
            page.f_nama.get(),
            page.f_alamat.get(),
            page.f_hp.get()
        )

        if berhasil:
            self.load_anggota()
            self.load_combo_anggota()
            self.reset_anggota()
            self.load_dashboard()
            messagebox.showinfo(
                "Berhasil",
                "Data anggota berhasil ditambahkan."
            )

        else:
            messagebox.showerror(
                "Gagal",
                "Data anggota gagal disimpan."
            )
    
    # Memilih data aggota
    def pilih_anggota(self, event):
        page = self.app.anggota_page
        selected = page.tree.focus()

        if not selected:
            return

        values = page.tree.item(selected)["values"]
        page.f_id.entry.config(state="normal")
        page.f_id.set(values[0])
        page.f_nama.set(values[1])
        page.f_alamat.set(values[2])
        page.f_hp.set(values[3])
        page.f_id.entry.config(state="readonly")
    
    # Mengupdate data anggota
    def update_anggota(self):
        page = self.app.anggota_page
        berhasil = model.update_anggota(
            page.f_id.get(),
            page.f_nama.get(),
            page.f_alamat.get(),
            page.f_hp.get()
        )

        if berhasil:
            self.load_anggota()
            self.load_combo_anggota()
            self.reset_anggota()
            messagebox.showinfo(
                "Berhasil",
                "Data berhasil diupdate."
            )

        else:
            messagebox.showerror(
                "Gagal",
                "Update gagal."
            )
    
    # Menghapus data anggota
    def hapus_anggota(self):
        page = self.app.anggota_page

        if page.f_id.get() == "":
            messagebox.showwarning(
                "Peringatan",
                "Pilih data terlebih dahulu."
            )
            return

        jawab = messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus data?"
        )

        if not jawab:
            return

        berhasil = model.delete_anggota(
            page.f_id.get()
        )

        if berhasil:
            self.load_anggota()
            self.load_combo_anggota()
            self.reset_anggota()
            messagebox.showinfo(
                "Berhasil",
                "Data berhasil dihapus."
            )

        else:
            messagebox.showerror(
                "Gagal",
                "Data gagal dihapus."
            )
    
    # Merefresh form data anggota
    def reset_anggota(self):
        page = self.app.anggota_page
        page.f_id.set("")
        page.f_nama.set("")
        page.f_alamat.set("")
        page.f_hp.set("")
    
    # Combo data anggota
    def load_combo_anggota(self):
        data = model.get_all_anggota()
        self.daftar_anggota = {}
        nama_anggota = []

        for row in data:
            self.daftar_anggota[row[1]] = row[0]
            nama_anggota.append(row[1])

        self.app.peminjaman_page.f_anggota.combo["values"] = nama_anggota


# 5. Fitur Peminjaman
    # Menampilkan data peminjaman
    def load_peminjaman(self):
        page = self.app.peminjaman_page

        for item in page.tree.get_children():
            page.tree.delete(item)

        data = model.get_all_peminjaman()

        for row in data:
            page.tree.insert("", "end", values=row)

    # Menambahkan data peminjaman
    def tambah_peminjaman(self):
        page = self.app.peminjaman_page

        if page.f_buku.combo.get() == "" or page.f_anggota.combo.get() == "":
            messagebox.showwarning(
                "Peringatan",
                "Lengkapi data terlebih dahulu."
            )
            return

        id_buku = self.daftar_buku[page.f_buku.combo.get()]
        id_anggota = self.daftar_anggota[page.f_anggota.combo.get()]

        stok = model.get_stok_buku(id_buku)

        if stok <= 0:
            messagebox.showwarning(
            "Stok Habis",
            "Buku yang dipilih sedang tidak tersedia."
            )
            return

        berhasil = model.create_peminjaman(
            id_buku,
            id_anggota,
            page.f_tgl_pinjam.get(),
            page.f_batas.get(),
            "Dipinjam"
        )

        if berhasil : 
            model.update_stok_buku(id_buku, -1)
            self.load_peminjaman()
            self.load_combo_pengembalian()
            self.load_buku()
            self.reset_peminjaman()
            self.load_dashboard()
            messagebox.showinfo(
                "Berhasil",
                "Data peminjaman berhasil ditambahkan."
            )

        else:
            messagebox.showerror(
                "Gagal",
                "Data gagal disimpan."
            )
    
    # Memilih data peminjaman
    def pilih_peminjaman(self, event):
        page = self.app.peminjaman_page
        selected = page.tree.focus()

        if not selected:
            return
        values = page.tree.item(selected)["values"]

        page.f_id.entry.config(state="normal")
        page.f_id.set(values[0])
        page.f_id.entry.config(state="readonly")
        page.f_anggota.combo.set(values[1])
        page.f_buku.combo.set(values[2])
        page.f_tgl_pinjam.set(values[3])
        page.f_batas.set(values[4])
    
    # Mengupdate data peminjaman
    def update_peminjaman(self):
        page = self.app.peminjaman_page

        if page.f_id.get() == "":
            messagebox.showwarning(
                "Peringatan",
                "Pilih data terlebih dahulu."
            )
            return

        id_buku = self.daftar_buku[page.f_buku.combo.get()]
        id_anggota = self.daftar_anggota[page.f_anggota.combo.get()]

        berhasil = model.update_peminjaman(
            page.f_id.get(),
            id_buku,
            id_anggota,
            page.f_tgl_pinjam.get(),
            page.f_batas.get(),
            "Dipinjam"
        )

        if berhasil:
            self.reset_peminjaman()
            self.load_peminjaman()
            self.load_combo_pengembalian()
            self.load_pengembalian()
            self.load_buku()
            self.load_dashboard()
            messagebox.showinfo(
                "Berhasil",
                "Data berhasil diupdate."
            )

        else:
            messagebox.showerror(
                "Gagal",
                "Update data gagal."
            )

    # Menghapus data peminjaman
    def hapus_peminjaman(self):
        page = self.app.peminjaman_page

        if page.f_id.get() == "":
            messagebox.showwarning(
                "Peringatan",
                "Pilih data terlebih dahulu."
            )
            return

        jawab = messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus data peminjaman?"
        )

        if not jawab:
            return

        berhasil = model.delete_peminjaman(
            page.f_id.get()
        )

        if berhasil:
            self.reset_peminjaman()
            self.load_peminjaman()
            self.load_combo_pengembalian()
            self.load_dashboard()
            messagebox.showinfo(
                "Berhasil",
                "Data berhasil dihapus."
            )

        else:
            messagebox.showerror(
                "Gagal",
                "Data gagal dihapus."
            )

    # Merefresh data peminjaman
    def reset_peminjaman(self):
        page = self.app.peminjaman_page
        page.f_id.entry.config(state="normal")
        page.f_id.set("")
        page.f_id.entry.config(state="readonly")
        page.f_anggota.combo.set("")
        page.f_buku.combo.set("")
        page.f_tgl_pinjam.set("")
        page.f_batas.set("")

# 6. Fitur Pengembalian  
    # Menampilkan data pengembalian
    def load_pengembalian(self):
        page = self.app.pengembalian_page

        for item in page.tree.get_children():
            page.tree.delete(item)

        data = model.get_all_pengembalian()

        for row in data:
            row = list(row)
            if row[4] == "" or row[4] is None:
                row[4] = "Rp 0"
            else:
                row[4] = f"Rp {float(row[4]):,.0f}".replace(",", ".")
            page.tree.insert("", "end", values=row)

    # Memproses data pengembalian
    def proses_pengembalian(self):
        page = self.app.pengembalian_page

        if page.f_pinjam.combo.get() == "":
            messagebox.showwarning(
                "Peringatan",
                "Pilih data peminjaman terlebih dahulu."
            )
            return
        
        try:
            datetime.strptime(
            page.f_tgl_kembali.get(),
            "%d-%m-%Y"
            )
        except ValueError:
            messagebox.showerror(
            "Error",
            "Format tanggal harus DD-MM-YYYY"
            )
            return

        if page.f_tgl_kembali.get() == "":
            messagebox.showwarning(
                "Peringatan",
                "Masukkan tanggal kembali."
            )
            return

        id_pinjam = page.f_pinjam.combo.get().split(" - ")[0]

        data = model.get_all_peminjaman()

        id_buku = None
        for row in data:
            if str(row[0]) == str(id_pinjam):
                id_buku = row[3] 
            break

        denda = model.hitung_denda(model.get_batas_kembali(id_pinjam),page.f_tgl_kembali.get())

        page.f_denda.entry.config(state="normal")
        page.f_denda.set(f"Rp {denda:,}".replace(",", "."))
        page.f_denda.entry.config(state="readonly")

        berhasil = model.create_pengembalian(
            id_pinjam,
            page.f_tgl_kembali.get(),
            denda
        )

        if berhasil:
            id_buku = model.get_id_buku_by_pinjam(id_pinjam)

            model.update_stok_buku(id_buku, 1)
            model.selesai_peminjaman(id_pinjam)

            self.load_pengembalian()
            self.load_peminjaman()
            self.load_combo_pengembalian()
            self.load_buku()
            self.load_dashboard()

            messagebox.showinfo(
                "Berhasil",
                "Pengembalian berhasil diproses."
            )

            page.f_pinjam.combo.set("")
            page.f_tgl_kembali.set("")

            page.f_denda.entry.config(state="normal")
            page.f_denda.set("")
            page.f_denda.entry.config(state="readonly")

        else:
            messagebox.showerror(
                "Gagal",
                "Pengembalian gagal diproses."
            )
    
    def hitung_denda_otomatis(self, event=None):
        page = self.app.pengembalian_page

        if page.f_pinjam.combo.get() == "":
            return

        if page.f_tgl_kembali.get() == "":
            return

        id_pinjam = page.f_pinjam.combo.get().split(" - ")[0]

        batas_kembali = model.get_batas_kembali(id_pinjam)

        denda = model.hitung_denda(
            batas_kembali,
            page.f_tgl_kembali.get()
        )

        page.f_denda.entry.config(state="normal")
        page.f_denda.set(f"Rp {denda:,}".replace(",", "."))
        page.f_denda.entry.config(state="readonly")
    
    # Combo data pengembalian
    def load_combo_pengembalian(self):
        data = model.get_all_peminjaman()
        self.daftar_pinjam = {}
        daftar = []

        for row in data:
            if row[5] == "Dipinjam":
                teks = f"{row[0]} - {row[1]} - {row[2]}"
                self.daftar_pinjam[teks] = row[0]
                daftar.append(teks)

        self.app.pengembalian_page.f_pinjam.combo["values"] = daftar

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    controller = Controller()
    controller.run()