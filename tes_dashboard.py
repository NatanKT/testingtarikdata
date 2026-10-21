# tes kecil: pastikan halaman jalan tanpa perlu database sungguhan
import app

jumlah_panggil = 0

def baca_palsu(sql, nilai=()):
    # panggilan pertama pura-pura gagal, sisanya balas 2 baris data
    global jumlah_panggil
    jumlah_panggil += 1
    if jumlah_panggil == 1:
        raise Exception('tes gagal')
    if sql.startswith('select distinct bu'):
        return [('WF',), ('SG',)]
    return [(1, None), (2, 'x')]

app.baca_mysqlUPA = baca_palsu
hasil = app.application.test_client().get('/?mulai=2026-03-01&bu=WF')
html = hasil.data.decode()

assert hasil.status_code == 200
assert 'tes gagal' in html        # pesan error tampil di halaman
assert 'None' not in html         # None sudah diganti kosong
assert '<td>1</td>' in html
assert 'limit 10' not in html
assert 'name="mulai" value="2026-03-01"' in html   # filter tanggal terisi lagi
assert 'selected' in html                          # BU WF tetap terpilih
print('semua tes lulus')
