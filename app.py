from flask import Flask, render_template
from connection import baca_mysqlUPA

application = Flask(__name__)

judul = ('CPU - Rencana Produksi', 'LHP - Produksi Aktual', 'OEE')
tabel = ('query_cpu_upa_2026', 'query_lhp_upa_2026', 'query_oee_upa_2026')
kolom = (
    ('tanggal', 'bu', 'kode_pabrik', 'line', 'lhp_est', 'lhp_real'),
    ('tanggal', 'bu', 'kode_pabrik', 'line', 'real_ctn'),
    ('tanggal', 'bu', 'at', 'mpt', 'ao', 'so', 'go', 'target_c_bu'),
)

@application.route('/')
def index():
    data = []
    for i in range(0, 3):
        sql = "select %s from %s order by tanggal desc limit 10" % (','.join(kolom[i]), tabel[i])
        try:
            hasil = [list(baris) for baris in baca_mysqlUPA(sql)]
            err = None
        except Exception as e:
            print(e)
            hasil, err = [], str(e)
        data.append({'judul': judul[i], 'kolom': kolom[i], 'rows': hasil, 'error': err})
    return render_template('index.html', data=data)

application.run(host='0.0.0.0', debug=True)
