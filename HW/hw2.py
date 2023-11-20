"""
Referencing the database schema below with 3 relations, implement a Python
program performing the requested queries. All the Data Description Language
(DDL) commands and Data Manipulation Language (DML) queries should be performed
at the Python level.
```
class(course_ID, department_ID, student_quota)
course(course_ID, course_name, course_type, credit)
department(department ID, department_name, campus)
```
where `course_type` denotes a category among Disciplinary (D), Interdisciplinary
(ID), and Elective (E).
"""

import random
import sqlite3

from pandas import DataFrame


def execute_all(cur: sqlite3.Cursor, sql: str):
    for command in sql.split(";"):
        command = command.strip()
        if command.__len__() > 0:
            cur.execute(command)
    return cur


def print_table(values: list[tuple], columns: list[str]):
    print()
    print(DataFrame(values, columns=columns))
    print("\n")


DDL = """create table if not exists department(
    department_id integer primary key autoincrement,
    department_name text not null,
    campus text not null
);
create table if not exists course(
    course_id text primary key,
    course_name text not null,
    course_type text check(course_type in ('D', 'ID', 'E')),
    credit numerical(2, 1) not null
);
create table if not exists class(
    course_id text not null references course(course_id),
    department_id integer not null references department(department_id),
    student_quota integer,
    primary key (course_id, department_id)
);"""


def define_schema(cur: sqlite3.Cursor):
    """implement and run the required DDL commands, also considering all the
    potential constraints."""
    execute_all(cur, DDL)


CAMPUSES = ["West", "East"]
THE_COURSE = "COMPSCI 310"
COURSE_TYPES = ["D", "ID", "E"]
CREDITS = [0.5, 1, 2, 4]
N_COURSES = 13
DEPTS = "ABCD"
N_DEPT = DEPTS.__len__()
QUOTAS = [12, 18, 40]


def insert_data(cur: sqlite3.Cursor):
    """offer and perform a series of data insertion queries, adding at least 10
    courses and 3 departments."""
    courses = [f"DUMMY {i}" for i in range(N_COURSES - 1)] + [THE_COURSE]
    cur.executemany(
        "insert into course values (?, ?, ?, ?)",
        (
            (c, f"{c} Full Name", random.choice(COURSE_TYPES), random.choice(CREDITS))
            for c in courses
        ),
    )

    cur.executemany(
        "insert into department(department_name, campus) values (?, ?)",
        ((dept, random.choice(CAMPUSES)) for dept in DEPTS),
    )

    classes = set()
    while classes.__len__() < 30:
        classes.add((random.choice(courses), random.choice(range(1, N_DEPT + 1))))
    cur.executemany(
        "insert into class(course_id, department_id, student_quota) values (?, ?, ?)",
        ((*c, random.choice(QUOTAS)) for c in classes),
    )


def list_cs310(cur: sqlite3.Cursor):
    """list the department names and campuses, teaching 'COMPSCI 310' as a
    course ID, allowing at least 10 students to enroll. The results should be
    sorted with respect to campus in alphabetical order."""
    result = cur.execute(
        """select distinct department_name, campus
from department join class using (department_id)
where course_id=? and student_quota>=?
order by campus""",
        (THE_COURSE, 10),
    ).fetchall()
    print_table(result, ["department_name", "campus"])
    return result


def list_dept_credit(cur: sqlite3.Cursor):
    """return the department names alongside the total number of course credits
    offered."""
    result = cur.execute(
        """select department_name, sum(credit)
from department join class using (department_id) join course using (course_id)
group by department_name
"""
    ).fetchall()
    print_table(result, ["department_name", "total_credit"])
    return result


def list_allowed_student(cur: sqlite3.Cursor):
    """show the total number of students allowed to take courses by each campus
    where the results are sorted in descending order with respect to the total
    number of students."""
    result = cur.execute(
        """select campus, sum(student_quota) as total_quota
from department join class using (department_id) join course using (course_id)
group by campus
order by total_quota desc
"""
    ).fetchall()
    print_table(result, ["campus", "total_student_quota"])
    return result


def list_courses_offered(cur: sqlite3.Cursor):
    """return the course IDs for the courses offered by at least 2 departments,
    accepting 30 students or more."""
    result = cur.execute(
        """select course.course_id
from department join class using (department_id) join course using (course_id)
where student_quota>=30
group by course.course_id
having count(department.department_id)>=2
"""
    ).fetchall()
    print_table(result, ["couse_id"])
    return result


def list_dept_on_quota(cur: sqlite3.Cursor):
    """list the names of departments that offer one or more courses allowing at
    least 3 times of the student quota for another course given by the same
    department."""
    result = cur.execute(
        """with quota_map as (
    select department.department_id, department_name, student_quota
    from department join class using (department_id) join course using (course_id)
)
select distinct A.department_name
from quota_map as A, quota_map as B
where A.department_id=B.department_id and A.student_quota >= 3*B.student_quota
"""
    ).fetchall()
    print_table(result, ["department_name"])
    return result


def main():
    """Run all of the above."""
    random.seed(1)
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    for fn in (
        define_schema,
        insert_data,
        list_cs310,
        list_dept_credit,
        list_allowed_student,
        list_courses_offered,
        list_dept_on_quota,
    ):
        print(fn.__doc__)
        fn(cur)


main() if __name__ == "__main__" else None
