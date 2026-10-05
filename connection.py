import configparser, os
import MySQLdb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def baca_mysqlUPA(sql):
    cfg = configparser.ConfigParser()
    if not cfg.read(os.path.join(BASE_DIR, 'config.ini'), encoding='utf-8'):
        raise RuntimeError('config.ini tidak ditemukan')
    s = cfg['database']
    basis = MySQLdb.connect(s.get('host'), s.get('user'), s.get('password'), s.get('name'))
    basis.ping(True)
    kursor = basis.cursor()
    kursor.execute(sql)
    hasil = kursor.fetchall()
    kursor.close()
    basis.close()
    return hasil
