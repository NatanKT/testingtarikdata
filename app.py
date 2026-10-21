# program utama dashboard
from flask import Flask, render_template, request
from connection import baca_mysqlUPA

application = Flask(__name__)

# daftar tabel yang mau ditampilkan, satu kotak per tabel
DAFTAR_TABEL = [
    {
        'judul': 'CPU - Rencana Produksi',
        'tabel': 'query_cpu_upa_2026',
        'kolom': ['tanggal', 'bu', 'kode_pabrik', 'line', 'lhp_est', 'lhp_real'],
    },
    {
        'judul': 'LHP - Produksi Aktual',
        'tabel': 'query_lhp_upa_2026',
        'kolom': ['tanggal', 'bu', 'kode_pabrik', 'line', 'real_ctn'],
    },
    {
        'judul': 'OEE',
        'tabel': 'query_oee_upa_2026',
        'kolom': ['tanggal', 'bu', 'at', 'mpt', 'ao', 'so', 'go', 'target_c_bu'],
    },
]


def ambil_filter():
    # ambil filter dari alamat halaman, contoh: /?mulai=2026-03-01&selesai=2026-03-31&bu=WF
    return {
        'mulai': request.args.get('mulai', ''),
        'selesai': request.args.get('selesai', ''),
        'bu': request.args.get('bu', ''),
    }


def susun_where(f, dipakai):
    # bagian "where ..." hanya dibuat untuk filter yang diisi
    syarat = []
    nilai = []
    if f['mulai'] and 'tanggal' in dipakai:
        syarat.append('tanggal >= %s')
        nilai.append(f['mulai'])
    if f['selesai'] and 'tanggal' in dipakai:
        syarat.append('tanggal <= %s')
        nilai.append(f['selesai'])
    if f['bu'] and 'bu' in dipakai:
        syarat.append('bu = %s')
        nilai.append(f['bu'])
    if syarat:
        return ' where ' + ' and '.join(syarat), tuple(nilai)
    return '', ()


def bersihkan_none(baris):
    # ganti nilai None (kolom kosong di database) dengan '' agar tampilan tidak menulis "None"
    hasil = []
    for nilai in baris:
        if nilai is None:
            hasil.append('')
        else:
            hasil.append(nilai)
    return hasil


@application.route('/')
def index():
    daftar_filter = ambil_filter()
    daftar_bu = []
    data = []
    for info in DAFTAR_TABEL:
        # gabung nama kolom jadi satu kalimat, contoh: "tanggal,bu,line"
        daftar_kolom = ','.join(info['kolom'])
        # hanya kolom tanggal & bu yang bisa difilter (kolom lain tidak pasti ada di tiap tabel)
        kolom_filter = [k for k in info['kolom'] if k in ('tanggal', 'bu')]
        where, nilai = susun_where(daftar_filter, kolom_filter)
        # tidak pakai limit: semua baris ikut ditampilkan, urut dari tanggal terbaru
        sql = f"select {daftar_kolom} from {info['tabel']}{where} order by tanggal desc"

        # baca database; kalau gagal, simpan pesan errornya
        hasil = []
        error = None
        try:
            for baris in baca_mysqlUPA(sql, nilai):
                # tanggal ditulis rapi (2026-03-01), bukan (2026, 3, 1)
                hasil.append(bersihkan_none([str(v) if hasattr(v, 'year') else v for v in baris]))
        except Exception as e:
            print(e)
            error = str(e)

        # isi pilihan dropdown BU: ambil dari tabel pertama yang punya kolom bu
        if not daftar_bu and 'bu' in info['kolom']:
            try:
                daftar_bu = [baris[0] for baris in baca_mysqlUPA(f"select distinct bu from {info['tabel']} order by bu")]
            except Exception as e:
                print(e)

        # kirim ke templates/index.html
        data.append({
            'judul': info['judul'],
            'kolom': info['kolom'],
            'rows': hasil,
            'error': error,
        })

    return render_template('index.html', data=data, f=daftar_filter, daftar_bu=daftar_bu)


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
