if __name__ == "__main__":
    def _make():
        import sys, re
        out = ''
        with open(sys.argv[0]) as f:
            out = f.read()
            out,_ = out.split('\n#finish\n',1)
            out += '\n#finish\n'
        with open('def.sql') as f:
            sents = f.read().split('-->')[1:]
            for s in sents:
                head, body = s.split('\n',1)
                name, param = head.split('(',1)
                param = param.strip()
                f = ''
                if param[-1] == '!':
                    param = param[:-1].strip()
                    f = ' '*12
                arg = re.sub(r'[\:\=].*?[,\)]+',',',param)
                arg = arg.strip()[:-1]
                if arg:
                    arg = f',[{arg}]'
                out += f'def {name}(cur, {param}:\n'
                out += f"    cur.execute(\n"
                if f:
                    out += "f"
                out += "'''\n"
                out += body
                out += f"'''{f or arg})\n\n"


        with open(sys.argv[0],'w') as f:
            f.write(out)
    _make()

#finish
def  init_body(cur, ):
    cur.execute(
'''
create table body (
  id text,
  book_id text,
  word text primary key not null,
  phone text,
  usphon text,
  ukphone text,
  zh text,
  en text,

  rel text,
  phrase text,
  syno text,

  rem text,
  sentence text
)

''')

def  init_toc(cur, ):
    cur.execute(
'''
create table toc (
  key text primary key not null,
  word text not null
)
''')

def  add_index(cur, key, word):
    cur.execute(
'''
insert into toc values(  ?, ?);
''',[key, word])

def  index(cur, key):
    cur.execute(
'''
select word from toc where key == ?
''',[key])

def  indexs(cur, patt):
    cur.execute(
'''
select word from toc where key glob ?

''',[patt])

def  insert(cur, *args,):
    cur.execute(
'''
insert into body values(
  ?, ?, ?, ?, ?, ?, ?, ?,
  ?, ?, ?,    ?, ?
);

''',[*args,])

def  all(cur, *field):
    cur.execute(
f'''
select {','.join(field)} from body

'''            )

def  check(cur, field,value):
    cur.execute(
f'''
select {field} from body where {field} == "{value}"

'''            )

def  get(cur, word):
    cur.execute(
'''
select * from body where word == ?

''',[word])

def  find_by_zh(cur, patt):
    cur.execute(
'''
select * from body where zh glob ?

''',[patt])

