# CS310 Class Note

WDR 2106

course project: use DB to make app

information: data with meaning

knowledge: actionable information

exploratory data analysis (EDA)

relation ≈ table

data definition language (DDL): for schema

data manipulation language (DML): for query and CRUD

DML & DDL both in SQL

data model (DM): entity, attribute, relationship, constraint

entity relationship diagram (E-R diagram) (ER diagram)

unified modeling language (UML): for OODM

relation schema $R=(A_1,…)$

relation instance $r(R)$

- element $t$

attribute usually atomic

superkey $K$: subset of row tuple, bijection with row

- superset of $K$ is also superkey

candidate key = minimal superkey

union compatibility/ type compatibility

data control language (DCL) & transaction control language (TCL): management

`like`: any substring `%`, any char `_`

for where clause filter: like, between, some, all

for where clause standalone: exists, unique

union, intersect, except (all)

```sql
select x, fn(y) from _ group by x having …
```

boolean type: true, false, unknown

```sql
select _ from _ where x in y;
-- lateral clause:
select _ from x, lateral (/* access outside variables */) …;
-- with clause:
with alias_name as (…) select …;
delete from _ where _;
insert into table_name (attributes, …) values (…,), (…,), …
update table_name set attributes = value where …;
-- join using
select _ from relation1 join relation2 using (attr1, …);
-- view/ materialized view
create view view_name as select …;
create materialized view view_name as select …;
```

domain constraint on single relation: `not null`, `unique`, `check (…)`

referential integrity: `foreign key (attr1) references table_name on delete …`

named constraint: `attr1 type, constraint constr_name check (…)`

- drop named constraint: `alter table table_name drop constraint constr_name;`
- deferrable constraint: check at end of transaction

assertion

```sql
create assertion assert_name check (…);
```

function call

- `coalesce(attr1, default_value_in_place_of_null)`
- `cast(attr1 as type)`
- `data_format(value, 'format string')`
    - `if(predicate, value_when_true, value_when_false)` or `decode` in Oracle

user-defined type (UDT): distinct type/ structured data type

```sql
create type type_name as …;
create domain domain_name as …;
```

create table extension

```sql
create table table2 like table1;
create table table1 as (select …) with data;
```

stored function/ stored procedure:

```sql
delimiter $$
create function fn_name(arg1 type1, …) returns type_out begin
    -- declare local variable, set to NULL by default
    declare local_var var_type default default_val;
    -- mutate local variable
    set local_var = …;
    select _ into local_var from …;
    return …;
end $$
-- `type_out` can be a `table (…)`—table function

create procedure proc_name(
    in arg_input type1, out arg_output type2, inout arg_mutate type3, …
) begin
    -- …
end $$
-- no returning for procedure

delimiter ;

-- call procedure
call proc_name(args…, @outside_var);
```

stored function: deterministic/ non-deterministic (default)

procedural SQL:

```sql
-- expression with pattern matching
case -- optionally with value here
    when _ then _
    …
    else _
end;

-- loop
label1: loop
    iterate; -- continue
    leave; -- break
end loop;
while predicate1 do
    -- …
end while;
repeat
    -- …
until predicate1 end repeat;
for each_row as table_value1 do
    -- …
end for;
```

trigger:

```sql
create trigger trigger_name after insert on table_name -- or `before`, `delete`
referencing new row as row_name for each row when ( -- or `old row`.
-- or without renaming `new` or `old`.
    -- …
)
begin -- compound statement
    rollback
end;

-- multiple trigger
create trigger trigger_name before update on table_name
for each row follows another_trigger_name begin
    -- …
end, $$
```

error handling:

```sql
declare continue handle for sqlstate 'err_no' begin -- or for `not found`
    -- …
end; -- or `set _ = …`
```

cursor:

```sql
declare cur_name for select _ from _;
open cur_name;
fetch cur_name into var1, …;
close cur_name;
```
