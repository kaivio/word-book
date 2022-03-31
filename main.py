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
    parser.add_argument('-v',action='count',help="精准匹配一个单词，-vv 附带扩展内容，-vvv 附带调试信息")
    parser.add_argument('-f',action='store_true',help="模糊查找单词")
    parser.add_argument('-z',action='store_true',help="使用中文查找")
    parser.add_argument('-j',action='count', help='打印日语五十音，-jj 附带浊音 -jjj 附带拗音 如后跟参数，假名/罗马字互转')
    parser.add_argument('--tool',action='store_true')
    parser.add_argument('key',nargs='?',default='', help="主参数")

    opts,args = parser.parse_known_args()
    k = opts.key
    if opts.j:
        if opts.key:
            rom(' '.join([opts.key,*args]))
        else:
            show_gojyuonzu(opts.j)
        return


    if not k:
        parser.print_help()
        return
    con = connect()
    cur = con.cursor()
    if opts.tool:
        return

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

def show_gojyuonzu(n):
    for g in gojyuonzu.strip().split('---'):
        if n < 0:
            return
        for r in g.strip().split('\n\n'):
            l1,l2 = '  ', '  '
            for d in r.strip().split('\n'):
                h,k,i,o = d.split()
                h=h == '.' and '　' or h
                k=k == '.' and '　' or k
                i=i == '.' and ' '  or i
                o=o == '.' and ' '  or o
                l1 += f' \033[34m{i:>3}\033[0m {k:2}'
                l2 += f' {h:>2} \033[35m{o:3}\033[0m'

            print(l1)
            print(l2)
        n -= 1


def rom(text):
    hs = []
    ks = []
    ys = []
    os = []
    for i in gojyuonzu.split('\n'):
        try:
            h,k,y,o = i.split()
        except:
            continue
        if h == '.':
            continue
        hs.append(h)
        ks.append(k)
        ys.append(y)
        if o == '.':
            os.append(y)

    if is_rom(text[0]):
        out = []
        t = hs or ks
        for yu in text.split():
            if not is_rom(yu):
                out.append(yu)
                continue
            try:
                i = ys.index(yu)
            except:
                try:
                    i = os.index(yu)
                except:
                    out.append(yu)
                    continue

            out.append(t[i])
        out = ''.join(out)
        print(out)
        return out

    t = ys
    res = []
    for ch in text:
        brute = Brute()
        brute(hs.index, ch)
        brute(ks.index, ch)
        if brute.ok:
             yu = t[brute.val]
             res.append(yu)
        else:
            res.append(ch)

    res = ' '.join(res)
    print(res)
    return res



class Brute():
    ''' 执行->发生异常->继续
            ->没有异常->终止

    >>> a = [3,5,6]
    >>> brute = Brute()
    >>> brute(a.index, 4)
    >>> brute(a.index, 5)
    >>> brute(a.index, 6)
    >>> brute.val == 1
    '''
    def __init__(self):
        self.val = None
        self.ok = False

    def __call__(self,func,*args,**kwargs):
        if self.ok:
            return self.val
        try:
            self.val = func(*args,**kwargs)
            self.ok = True
            return self.val
        except:
            pass

    def reset(self):
        self.__init__()





def is_rom(ch):
    ch = ch[:1]
    o = ord(ch) >= ord('a') and ord(ch) <= ord('z')
    return o

gojyuonzu = '''
あ ア a .
い イ i .
う ウ u .
え エ e .
お オ o .

か カ ka .
き キ ki .
く ク ku .
け ケ ke .
こ コ ko .

さ サ sa .
し シ shi si
す ス su .
せ セ se .
そ ソ so .

た タ ta .
ち チ chi ti
つ ツ tsu tu
て テ te .
と ト to .

な ナ na .
に ニ ni .
ぬ ヌ nu .
ね ネ ne .
の ノ no .

は ハ ha .
ひ ヒ hi .
ふ フ fu hu
へ ヘ he .
ほ ホ ho .

ま マ ma .
み ミ mi .
む ム mu .
め メ me .
も モ mo .

や ヤ ya .
.  .  .  .
ゆ ユ yu .
.  .  .  .
よ ヨ yo .

ら ラ ra .
り リ ri .
る ル ru .
れ レ re .
ろ ロ ro .

わ ワ wa .
ゐ ヰ wi .
.  .  .  .
ゑ ヱ we .
を ヲ wo .
---
ん ン n .
---
が ガ ga .
ぎ ギ gi .
ぐ グ gu .
げ ゲ ge .
ご ゴ go .

ざ ザ za .
じ ジ ji zi
ず ズ zu .
ぜ ゼ ze .
ぞ ゾ zo .

だ ダ da .
ぢ ヂ zi .
づ ヅ zu .
で デ de .
ど ド do .

ば バ ba .
び ビ bi .
ぶ ブ bu .
べ ベ be .
ぼ ボ bo .

ぱ パ pa .
ぴ ピ pi .
ぷ プ pu .
ぺ ペ pe .
ぽ ポ po .
---
きゃ キャ kya .
きゅ キュ kyu .
きょ キョ kyo .

しゃ シャ sha sya
しゅ シュ shu syu
しょ ショ sho syo

ちゃ チャ cha tya
ちゅ チュ chu tyu
ちょ チョ cho tyo

にゃ ニャ nya .
にゅ ニュ nyu .
にょ ニョ nyo .

ひゃ ヒャ hya .
ひゅ ヒュ hyu .
ひょ ヒョ hyo .

みゃ ミャ mya .
みゅ ミュ myu .
みょ ミョ myo .

りゃ リャ rya .
りゅ リュ ryu .
りょ リョ ryo .

ぎゃ ギャ gya .
ぎゅ ギュ gyu .
ぎょ ギョ gyo .

じゃ ジャ ja zya
じゅ ジュ ju zyu
じょ ジョ jo zyo

ぢゃ ヂャ ja zya
ぢゅ ヂュ ju zyu
ぢょ ヂョ jo zyo

びゃ ビャ bya .
びゅ ビュ byu .
びょ ビョ byo .

ぴゃ ピャ pya .
ぴゅ ピュ pyu .
ぴょ ピョ pyo .

'''

if  __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
    finally:
        colse()
