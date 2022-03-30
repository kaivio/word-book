
--> init_body()
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

--> init_toc()
create table toc (
  key text primary key not null,
  word text not null
)
--> add_index(key, word)
insert into toc values(  ?, ?);
--> index(key)
select word from toc where key == ?
--> indexs(patt)
select word from toc where key glob ?

--> insert(*args,)
insert into body values(
  ?, ?, ?, ?, ?, ?, ?, ?,
  ?, ?, ?,    ?, ?
);

--> all(*field) !
select {','.join(field)} from body

--> check(field,value) !
select {field} from body where {field} == "{value}"

--> get(word)
select * from body where word == ?

--> find_by_zh(patt)
select * from body where zh glob ?

