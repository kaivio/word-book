import argparse
import sqlite3
import sys
from pathlib import Path
import sql
import word

_connection = None
def connect(file=f'{Path(__file__).parent}/book.db') -> sqlite3.Connection:
    global _connection
    if _connection:
        return _connection
    _connection = sqlite3.connect(file)
    _connection.row_factory = sqlite3.Row
    return  _connection
def cursor():
    return connect().cursor()
def colse():
    if _connection:
        _connection.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v',action='count')
    parser.add_argument('-f',action='store_true')
    parser.add_argument('-z',action='store_true')
    parser.add_argument('--tool',action='store_true')
    parser.add_argument('key',default='')

    opts,args = parser.parse_known_args()
    k = opts.key
    if True:
        pass
    con = connect()
    cur = con.cursor()
    if opts.tool:
        pass

    elif opts.z:
        sql.find_by_zh(cur, f'*{k}*')
        rows = cur.fetchall()
        show_list(rows)

    elif opts.v:
        if opts.v == 1:
            level = 5
        elif opts.v == 2:
            level = 7
        elif opts.v == 3:
            level = 100

        row = get(k)
        if row:
            w = word.load(row)
            word.print_word(w,level)
        else:
            print('(空)')

    elif opts.f:
        rows = find(k)
        show_list(rows)

    else:
        row = get(k)
        if row:
            w = word.load(row)
            word.print_word(w,4)
        else:
            rows = find(k)
            show_list(rows)

def show_list(rows):
    print(f'找到 {len(rows)} 条结果')
    for row in rows:
        w = word.load(row)
        word.print_word(w,0)


def get(k):
    cur = cursor()
    sql.index(cur, k)
    index = cur.fetchone()
    row = None
    if index:
        iw = index['word']
        sql.get(cur,iw)
        row = cur.fetchone()

    return row

def find(k):
    cur = cursor()
    sql.indexs(cur, k+'*')
    indexs = cur.fetchall()
    if not indexs:
        sql.indexs(cur, '*'+k+'*')
        indexs = cur.fetchall()

    rows = []
    iws = set()
    if indexs:
        print(len(indexs))
        for iw,  in  indexs:
            if iw in iws:
                continue
            iws.add(iw)
            sql.get(cur,iw)
            row = cur.fetchone()
            rows.append(row)

    return rows


if  __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
    finally:
        colse()
