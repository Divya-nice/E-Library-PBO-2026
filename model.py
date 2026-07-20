import sqlite3
import os

# ==========================
# Membuat folder database otomatis
# ==========================
os.makedirs("database", exist_ok=True)

DB_NAME = "database/library.db"


# ==========================
# Koneksi Database
# ==========================
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ==========================
# DASHBOARD
# ==========================
def count_buku():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM buku")
        return cursor.fetchone()[0]

    except sqlite3.Error as e:
        print(e)
        return 0

    finally:
        conn.close()


def count_anggota():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM anggota")
        return cursor.fetchone()[0]

    except sqlite3.Error as e:
        print(e)
        return 0

    finally:
        conn.close()


def count_dipinjam():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM peminjaman
            WHERE status='Dipinjam'
        """)
        return cursor.fetchone()[0]

    except sqlite3.Error as e:
        print(e)
        return 0

    finally:
        conn.close()


def count_terlambat():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM peminjaman
            WHERE status='Terlambat'
        """)
        return cursor.fetchone()[0]

    except sqlite3.Error as e:
        print(e)
        return 0

    finally:
        conn.close()
# ==========================
# Membuat Tabel
# ==========================
def create_tables():
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS buku(
            id_buku INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            penulis TEXT NOT NULL,
            penerbit TEXT NOT NULL,
            tahun_terbit INTEGER,
            kategori TEXT,
            stok INTEGER DEFAULT 0
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS anggota(
            id_anggota INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            alamat TEXT,
            no_hp TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS peminjaman(
            id_pinjam INTEGER PRIMARY KEY AUTOINCREMENT,
            id_buku INTEGER NOT NULL,
            id_anggota INTEGER NOT NULL,
            tanggal_pinjam TEXT NOT NULL,
            batas_kembali TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(id_buku) REFERENCES buku(id_buku),
            FOREIGN KEY(id_anggota) REFERENCES anggota(id_anggota)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pengembalian(
            id_pengembalian INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pinjam INTEGER NOT NULL,
            tanggal_kembali TEXT NOT NULL,
            denda REAL DEFAULT 0,
            FOREIGN KEY(id_pinjam) REFERENCES peminjaman(id_pinjam)
        )
        """)

        conn.commit()
        print("Database berhasil dibuat.")

    except sqlite3.Error as e:
        print("Database Error :", e)

    finally:
        if conn:
            conn.close()


# ==========================
# CRUD BUKU
# ==========================
def create_buku(judul, penulis, penerbit, tahun_terbit, kategori, stok):

    if judul.strip() == "" or penulis.strip() == "":
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO buku
        (judul, penulis, penerbit, tahun_terbit, kategori, stok)
        VALUES (?,?,?,?,?,?)
        """, (
            judul,
            penulis,
            penerbit,
            tahun_terbit,
            kategori,
            stok
        ))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print("Error :", e)
        return False

    finally:
        conn.close()


def get_all_buku():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM buku
        ORDER BY id_buku ASC
        """)

        return cursor.fetchall()

    except sqlite3.Error as e:
        print(e)
        return []

    finally:
        conn.close()
# ==========================
# UPDATE & DELETE BUKU
# ==========================
def update_buku(id_buku, judul, penulis, penerbit, tahun_terbit, kategori, stok):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE buku
        SET judul=?,
            penulis=?,
            penerbit=?,
            tahun_terbit=?,
            kategori=?,
            stok=?
        WHERE id_buku=?
        """, (
            judul,
            penulis,
            penerbit,
            tahun_terbit,
            kategori,
            stok,
            id_buku
        ))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print("Error :", e)
        return False

    finally:
        conn.close()


def delete_buku(id_buku):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM buku WHERE id_buku=?",
            (id_buku,)
        )

        conn.commit()
        return True

    except sqlite3.Error as e:
        print("Error :", e)
        return False

    finally:
        conn.close()


# ==========================
# CRUD ANGGOTA
# ==========================
def create_anggota(nama, alamat, no_hp):

    if nama.strip() == "":
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO anggota
        (nama, alamat, no_hp)
        VALUES (?,?,?)
        """, (
            nama,
            alamat,
            no_hp
        ))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print("Error :", e)
        return False

    finally:
        conn.close()


def get_all_anggota():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM anggota
        ORDER BY id_anggota ASC
        """)

        return cursor.fetchall()

    except sqlite3.Error as e:
        print("Error :", e)
        return []

    finally:
        conn.close()


def update_anggota(id_anggota, nama, alamat, no_hp):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE anggota
        SET nama=?,
            alamat=?,
            no_hp=?
        WHERE id_anggota=?
        """, (
            nama,
            alamat,
            no_hp,
            id_anggota
        ))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print("Error :", e)
        return False

    finally:
        conn.close()


def delete_anggota(id_anggota):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM anggota WHERE id_anggota=?",
            (id_anggota,)
        )

        conn.commit()
        return True

    except sqlite3.Error as e:
        print("Error :", e)
        return False

    finally:
        conn.close()
# ==========================
# CRUD PEMINJAMAN
# ==========================
def create_peminjaman(id_buku, id_anggota, tanggal_pinjam, batas_kembali, status):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO peminjaman
        (id_buku, id_anggota, tanggal_pinjam, batas_kembali, status)
        VALUES (?,?,?,?,?)
        """, (
            id_buku,
            id_anggota,
            tanggal_pinjam,
            batas_kembali,
            status
        ))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print("Error :", e)
        return False

    finally:
        conn.close()


def get_all_peminjaman():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.id_pinjam,
                a.nama,
                b.judul,
                p.tanggal_pinjam,
                p.batas_kembali,
                p.status
            FROM peminjaman p
            JOIN anggota a
                ON p.id_anggota = a.id_anggota
            JOIN buku b
                ON p.id_buku = b.id_buku
            ORDER BY p.id_pinjam
        """)

        return cursor.fetchall()

    except sqlite3.Error as e:
        print(e)
        return []

    finally:
        conn.close()

def update_peminjaman(id_pinjam, id_buku, id_anggota, tanggal_pinjam, batas_kembali, status):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE peminjaman
        SET id_buku=?,
            id_anggota=?,
            tanggal_pinjam=?,
            batas_kembali=?,
            status=?
        WHERE id_pinjam=?
        """, (
            id_buku,
            id_anggota,
            tanggal_pinjam,
            batas_kembali,
            status,
            id_pinjam
        ))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print("Error :", e)
        return False

    finally:
        conn.close()


def delete_peminjaman(id_pinjam):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM peminjaman WHERE id_pinjam=?",
            (id_pinjam,)
        )

        conn.commit()
        return True

    except sqlite3.Error as e:
        print("Error :", e)
        return False

    finally:
        conn.close()


# ==========================
# CRUD PENGEMBALIAN
# ==========================
def create_pengembalian(id_pinjam, tanggal_kembali, denda):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO pengembalian
        (id_pinjam, tanggal_kembali, denda)
        VALUES (?,?,?)
        """, (
            id_pinjam,
            tanggal_kembali,
            denda
        ))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print("Error :", e)
        return False

    finally:
        conn.close()


def get_all_pengembalian():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                pengembalian.id_pengembalian,
                anggota.nama,
                buku.judul,
                pengembalian.tanggal_kembali,
                pengembalian.denda
            FROM pengembalian
            INNER JOIN peminjaman
                ON pengembalian.id_pinjam = peminjaman.id_pinjam
            INNER JOIN anggota
                ON peminjaman.id_anggota = anggota.id_anggota
            INNER JOIN buku
                ON peminjaman.id_buku = buku.id_buku
            ORDER BY pengembalian.id_pengembalian ASC
        """)

        return cursor.fetchall()

    except sqlite3.Error as e:
        print("Error :", e)
        return []

    finally:
        conn.close()


# ==========================
# Jalankan Program
# ==========================
if __name__ == "_main_":

    create_tables()

    print("Database berhasil dibuat.")
    print("Lokasi database :", DB_NAME)
