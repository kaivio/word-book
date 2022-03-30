
class Word():
    id:str
    book_id:str

    word:str
    phone:str = ''
    usphone:str = ''
    ukphone:str = ''
    zh: str = ''
    en: str = ''

    rel:str = ''
    phrase:str = ''
    syno:str = ''

    rem:str = ''
    sentence:str = ''

def load(row:'sqlite3.Row') -> Word:
    w = Word()
    for k in row.keys():
        setattr(w,k,row[k])
    return w
def dump(w:Word) -> tuple:
    return (

    w.id,
    w.book_id,

    w.word,
    w.phone,
    w.usphone,
    w.ukphone,
    w.zh,
    w.en,

    w.rel,
    w.phrase,
    w.syno,

    w.rem,
    w.sentence,

            )
class Style():
    clear = '\033[0m'
    h1 = '\033[1;33m'
    h2 = '\033[36m'
    timid = '\033[2;3m'
    grey = '\033[90m'
    italic = '\033[3m'

_style = Style()
_nostyle = Style()
for _i in dir(_nostyle):
    if not _i.startswith('__'):
        setattr(_nostyle,_i,'')

def view_word(w:Word, styling=False, level=0):
    style = _style
    if not styling:
        style = _nostyle
    def other_words(items):
        view = ''
        for i in items.split('\n'):
            if not i:
                continue
            w,t = i.split(':',1)
            s,t = t.split('.',1)
            w,s,t = [_.strip() for _ in (w,s,t)]
            t = t.replace('；',f'{style.grey}; {style.clear}')
            v = w.split('/')
            if len(v) > 1:
                view += '  '+f" {style.grey}/{style.clear} ".join(v)+'\n    '
            else:
                view += f'  {w}{style.grey}:{style.clear} '
            if s == '?':
                view += t+'\n'
            else:
                view += f'{style.timid}{s}.{style.clear} {t}\n'


        return view

    view = ''
    view += f'  {style.h1}{w.word}'
    view += style.clear
    if level > 0:
        view += f'  {style.grey}/{w.phone}/'
        view += f'{w.ukphone}/'
        view += f'{w.usphone}/'
        view += style.clear+'\n'

    for i in w.zh.split('\n'):
        if not i:
            continue
        s,t = i.split('.',1)
        t = t.strip()
        view += f'  {style.timid}{s}.{style.clear}\t{t}\n'
    if level < 1:
        return ' '.join(view.strip().split())
    if level == 1:
        return view

    if w.rem:
        view += f'  {style.h2}－ 记 忆 －{style.clear}  \n'
        view += f'  {w.rem}\n'
    if level == 2:
        return view

    if w.rel:
        view += f'  {style.h2}－ 同 根 －{style.clear}  \n'
        view += other_words(w.rel)
    if level == 3:
        return view

    if w.syno:
        view += f'  {style.h2}－ 同 近 －{style.clear}  \n'
        view += other_words(w.syno)
    if level == 4:
        return view

    if w.phrase:
        view += f'  {style.h2}－ 短 语 －{style.clear}  \n'
        view += other_words(w.phrase)
    if level == 5:
        return view

    if w.sentence:
        view += f'  {style.h2}－ 例 句  －{style.clear}  \n'
        for s in w.sentence.split('\n'):
            if not s:
                continue
            en,zh = s.split('----')
            en = en.strip()
            zh = zh.strip()
            view += f'  {style.grey}ℓ {style.clear}{en}\n'
            view += f'  {style.grey}√ {style.clear}{zh}\n'
    if level == 6:
        return view

    if w.en:
        view += f'  {style.h2}－ 英 释 －{style.clear}  \n'
        for i in w.en.split('\n'):
            if not i:
                continue
            s,t = i.split('.',1)
            t = t.strip()
            view += f'  {style.timid}{s}.{style.clear}\t{t}\n'

    if level < 99:
        return view

    view += f'  {style.timid}-----------\n  {w.book_id}{style.clear}'

    return view
    # https://dict.youdao.com/dictvoice?audio&type=<1|2>

def print_word(w,level=5):
    print(view_word(w,True,level).rstrip())


