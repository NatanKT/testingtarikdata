# modul pembantu: baca data dari database MySQL
import configparser, os
import MySQLdb

# letak folder program ini (dipakai untuk mencari file config.ini)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def baca_mysqlUPA(sql, nilai=()):
    # 1. baca pengaturan koneksi dari config.ini
    cfg = configparser.ConfigParser()
    if not cfg.read(os.path.join(BASE_DIR, 'config.ini'), encoding='utf-8'):
        raise RuntimeError('config.ini tidak ditemukan')
    s = cfg['database']

    # 2. sambungkan ke database lalu jalankan SQL
    basis = MySQLdb.connect(s.get('host'), s.get('user'), s.get('password'), s.get('name'))
    basis.ping(True)
    kursor = basis.cursor()
    # nilai=() dipakai kalau SQL berisi %s, supaya isi filter tidak bisa menyusup ke SQL (anti SQL injection)
    kursor.execute(sql, nilai)
    hasil = kursor.fetchall()

    # 3. tutup koneksi lalu kembalikan hasilnya
    kursor.close()
    basis.close()
    return hasil
