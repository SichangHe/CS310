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
-- expression with pattern matching
case
    when _ then _
    …
    else _
end;
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
