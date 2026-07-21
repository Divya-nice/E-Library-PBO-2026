import tkinter as tk
from tkinter import messagebox

import model
from view import ELibraryView

class Controller:

    def __init__(self):

        # membuat database
        model.create_tables()

        # membuat tampilan
        self.app = ELibraryView()

        # hubungkan event
        self.bind_events()

        # tampilkan data awal
        self.load_dashboard()
        self.load_buku()
        self.load_anggota()
        self.load_combobox()
        self.load_combo_buku()
        self.load_combo_anggota()
        self.load_combo_pengembalian()
        self.load_peminjaman()
        self.load_pengembalian()

    def bind_events(self):
        # =====================
        # DATA BUKU
        # =====================
        self.app.buku_page.btn_tambah.config(command=self.tambah_buku)
        self.app.buku_page.btn_update.config(command=self.update_buku)
        self.app.buku_page.btn_hapus.config(command=self.hapus_buku)
        self.app.buku_page.btn_reset.config(command=self.reset_buku)
        
        self.app.buku_page.tree.bind(
            "<<TreeviewSelect>>",
            self.pilih_buku
        )

        # =====================
        # DATA ANGGOTA
        # =====================
        self.app.anggota_page.btn_tambah.config(command=self.tambah_anggota)
        self.app.anggota_page.btn_update.config(command=self.update_anggota)
        self.app.anggota_page.btn_hapus.config(command=self.hapus_anggota)
        self.app.anggota_page.btn_reset.config(command=self.reset_anggota)

        self.app.anggota_page.tree.bind(
            "<<TreeviewSelect>>",
            self.pilih_anggota
        )

        # =====================
        # PEMINJAMAN
        # =====================
        self.app.peminjaman_page.btn_tambah.config(command=self.tambah_peminjaman)
        self.app.peminjaman_page.btn_update.config(command=self.update_peminjaman)
        self.app.peminjaman_page.btn_hapus.config(command=self.hapus_peminjaman)
        self.app.peminjaman_page.btn_reset.config(command=self.reset_peminjaman)

        self.app.peminjaman_page.tree.bind(
            "<<TreeviewSelect>>",
        self.pilih_peminjaman
        )

        # =====================
        # PENGEMBALIAN
        # =====================

        self.app.pengembalian_page.btn_proses.config(
            command=self.proses_pengembalian
        )

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
    
    def reset_peminjaman(self):

        page = self.app.peminjaman_page

        page.f_id.entry.config(state="normal")

        page.f_id.set("")
        page.f_id.entry.config(state="readonly")

        page.f_anggota.combo.set("")
        page.f_buku.combo.set("")
        page.f_tgl_pinjam.set("")
        page.f_batas.set("")
    
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

    def load_combo_buku(self):

        data = model.get_all_buku()

        self.daftar_buku = {}

        nama_buku = []

        for row in data:
            self.daftar_buku[row[1]] = row[0]
            nama_buku.append(row[1])

        self.app.peminjaman_page.f_buku.combo["values"] = nama_buku

    def load_combo_anggota(self):

        data = model.get_all_anggota()

        self.daftar_anggota = {}

        nama_anggota = []

        for row in data:
            self.daftar_anggota[row[1]] = row[0]
            nama_anggota.append(row[1])

        self.app.peminjaman_page.f_anggota.combo["values"] = nama_anggota

    def load_dashboard(self):
        pass

    def load_buku(self):
        page = self.app.buku_page

        # kosongkan treeview
        for item in page.tree.get_children():
            page.tree.delete(item)

        # ambil data dari database
        data = model.get_all_buku()

        # tampilkan
        for row in data:
            page.tree.insert("", "end", values=row)
    
    def load_combo_pengembalian(self):

        data = model.get_all_peminjaman()

        self.daftar_pinjam = {}

        daftar = []

        for row in data:
            # row = (id_pinjam, nama, judul, tanggal, batas, status)

            if row[5] == "Dipinjam":
                teks = f"{row[0]} - {row[1]} - {row[2]}"

                self.daftar_pinjam[teks] = row[0]
                daftar.append(teks)

        self.app.pengembalian_page.f_pinjam.combo["values"] = daftar
    
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
            messagebox.showinfo(
                "Berhasil",
                "Data buku berhasil ditambahkan."
            )

            self.reset_buku()
            self.load_buku()
            self.load_dashboard()

        else:
            messagebox.showerror(
                "Gagal",
                "Data buku tidak dapat disimpan."
            )

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
            messagebox.showinfo(
                "Berhasil",
                "Data buku berhasil diupdate."
            )

            self.reset_buku()
            self.load_buku()

        else:
            messagebox.showerror(
                "Gagal",
                "Update data gagal."
        )
    
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
            messagebox.showinfo(
                "Berhasil",
                "Data berhasil dihapus."
            )

            self.reset_buku()
            self.load_buku()

        else:
            messagebox.showerror(
                "Gagal",
                "Data gagal dihapus."
        )

    def load_anggota(self):

        page = self.app.anggota_page

        for item in page.tree.get_children():
            page.tree.delete(item)

        data = model.get_all_anggota()

        for row in data:
            page.tree.insert("", "end", values=row)
    
    def reset_anggota(self):

        page = self.app.anggota_page

        page.f_id.set("")
        page.f_nama.set("")
        page.f_alamat.set("")
        page.f_hp.set("")

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

    def tambah_anggota(self):

        page = self.app.anggota_page

        berhasil = model.create_anggota(

            page.f_nama.get(),
            page.f_alamat.get(),
            page.f_hp.get()

        )

        if berhasil:

            messagebox.showinfo(
                "Berhasil",
                "Data anggota berhasil ditambahkan."
            )

            self.reset_anggota()
            self.load_anggota()
            self.load_dashboard()

        else:

            messagebox.showerror(
                "Gagal",
                "Data anggota gagal disimpan."
            )
    
    def update_anggota(self):

        page = self.app.anggota_page

        berhasil = model.update_anggota(

            page.f_id.get(),
            page.f_nama.get(),
            page.f_alamat.get(),
            page.f_hp.get()

        )

        if berhasil:

            messagebox.showinfo(
                "Berhasil",
                "Data berhasil diupdate."
            )

            self.reset_anggota()
            self.load_anggota()

        else:

            messagebox.showerror(
                "Gagal",
                "Update gagal."
            )
    
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

            messagebox.showinfo(
                "Berhasil",
                "Data berhasil dihapus."
            )

            self.reset_anggota()
            self.load_anggota()

        else:

            messagebox.showerror(
                "Gagal",
                "Data gagal dihapus."
            )

    def load_peminjaman(self):

        page = self.app.peminjaman_page

        # kosongkan treeview
        for item in page.tree.get_children():
            page.tree.delete(item)

        # ambil data
        data = model.get_all_peminjaman()

        # tampilkan
        for row in data:
            page.tree.insert("", "end", values=row)

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

        berhasil = model.create_peminjaman(
            id_buku,
            id_anggota,
            page.f_tgl_pinjam.get(),
            page.f_batas.get(),
            "Dipinjam"
        )

        if berhasil:
            messagebox.showinfo(
                "Berhasil",
                "Data peminjaman berhasil ditambahkan."
            )

            self.load_peminjaman()
            self.load_combo_pengembalian()
            self.reset_peminjaman()
            self.load_dashboard()

        else:
            messagebox.showerror(
                "Gagal",
                "Data gagal disimpan."
            )

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
            messagebox.showinfo(
                "Berhasil",
                "Data berhasil diupdate."
            )

            self.reset_peminjaman()
            self.load_peminjaman()
            self.load_combo_pengembalian()

        else:
            messagebox.showerror(
                "Gagal",
                "Update data gagal."
            )

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

            messagebox.showinfo(
                "Berhasil",
                "Data berhasil dihapus."
            )

            self.reset_peminjaman()
            self.load_peminjaman()
            self.load_combo_pengembalian()
            self.load_dashboard()

        else:

            messagebox.showerror(
                "Gagal",
                "Data gagal dihapus."
            )
    
    def proses_pengembalian(self):

        page = self.app.pengembalian_page

        if page.f_pinjam.combo.get() == "":
            messagebox.showwarning(
                "Peringatan",
                "Pilih data peminjaman terlebih dahulu."
            )

            return

        id_pinjam = page.f_pinjam.combo.get().split(" - ")[0]

        berhasil = model.create_pengembalian(
            id_pinjam,
            page.f_tgl_kembali.get(),
            page.f_denda.get()
        )

        if berhasil:

            model.selesai_peminjaman(id_pinjam)

            messagebox.showinfo(
                "Berhasil",
                "Pengembalian berhasil diproses."
            )

            self.load_pengembalian()
            self.load_peminjaman()
            self.load_combo_pengembalian()
            self.load_dashboard()

            page.f_pinjam.combo.set("")
            page.f_tgl_kembali.set("")
            page.f_denda.set("")

        else:

            messagebox.showerror(
                "Gagal",
                "Pengembalian gagal diproses."
            )

    def load_pengembalian(self):
        page = self.app.pengembalian_page

        for item in page.tree.get_children():
            page.tree.delete(item)

        data = model.get_all_pengembalian()

        for row in data:
            page.tree.insert("", "end", values=row)

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    controller = Controller()
    controller.run()