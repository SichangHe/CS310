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


def define_schema():
    """implement and run the required DDL commands, also considering all the
    potential constraints."""


def insert_data():
    """offer and perform a series of data insertion queries, adding at least 10
    courses and 3 departments."""


def list_cs310():
    """list the department names and campuses, teaching 'COMPSCI 310' as a
    course ID, allowing at least 10 students to enroll. The results should be
    sorted with respect to campus in alphabetical order."""


def list_dept_credit():
    """return the department names alongside the total number of course credits
    offered."""


def list_allowed_student():
    """show the total number of students allowed to take courses by each campus
    where the results are sorted in descending order with respect to the total
    number of students."""


def list_courses_offered():
    """return the course IDs for the courses offered by at least 2 departments,
    accepting 30 students or more."""


def list_dept_on_quota():
    """list the names of departments that offer one or more courses allowing at
    least 3 times of the student quota for another course given by the same
    department."""


def main():
    """Run all of the above."""


main() if __name__ == "__main__" else None
