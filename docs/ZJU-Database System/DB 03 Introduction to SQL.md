---
status:
  - archived
tags: CS/DB/SQL
date_created: 2025-02-25T14:48:26
date_modified: 2025-09-13T10:18:12
---

# Overview

The SQL has several parts:

- DDL
- DML
- integrity
- view definition
- transaction control
- embedded SQL and dynamic SQL
- authorization

# SQL Data Definition

## 可定义项

- 每个 relation 的 schema
- 变量类型
- integrity 约束
- the set of indices to be maintained for each relation
- 每个 relation 的安全和权限管理
- 每个 relation 存储在磁盘上的方式

## Basic Types

> `CHAR, VARCHAR, INT, SMALLINT, NUMERIC(p, d), REAL, DOUBLE PRECISION, FLOAT(n)`

- `numeric(p, d)` p 位十进制实数，d 是小数位的数量
	- e.g. `numeric(3, 1)` 允许 44.5 不允许 4.45 和 0.32
- `float(n)` 表示一个浮点数，精度至少有 n 位数

## Create Table

```sql
CREATE TABLE r
	(A_1 D_1, A_2 D_2, ..., A_n D_n),
		(integrity-constraint_1),
		...,
		(integrity-constraint_k))
```

- A 是 attr name，D 是 data type

### Integrity Constraints

```sql
PRIMARY KEY (A_x, ..., A_y)
FOREIGN KEY (A_m, ..., A_n) REFERENCES r
NOT NULL
```

```sql title="example"
CREATE TABLE instructor(
	ID CHAR(5),
	name VARCHAR(20) NOT NULL,
	dept_name VARCHAR(20),
	salary numeric(8, 2),
	PRIMARY KEY (ID),
	FOREIGN KEY (dept_name) REFERENCES department
);
```

```sql title="example"
CREATE TABLE takes(
	ID VARCHAR(5),
	course_id VARCHAR(8),
	sec_id VARCHAR(8),
	semester VARCHAR(6),
	year numeric(4, 0),
	grade VARCHAR(2),
	PRIMARY KEY (ID, course_id, sec_id, semester, year),
	FOREIGH KEY (ID) REFERENCES student(ID),
	FOREIGN KEY (course_id, sec_id, semester, year) REFERENCES section(course_id, sec_id, semester, year)
	ON DELETE CASCADE RESTRICT | SET NULL | SET DEFAULT
);
```

- `ON DELETE CASCADE` 在 ref 被删除时进行的操作

## Update Tables

- `INSERT INTO instructor VALUES ('10211', 'Smith', 'Biology', 6000);`
- `DELETE FROM student WHERE name = 'Tom';`
- `DROP TABLE r`
- `ALTER TABLE r ADD A D`
- `ALTER TABLE r DROP A`

# Basic Query Structure

```sql
SELECT A_1, A_2, ..., A_n
FROM r_1, r_2, ..., r_m
WHERE P
```

- 查询结果是一个 relation

## Select Clause

- ! names are case insensitive
- ! SQL 允许 relation 中的 duplicate，结果中也都会显示
	- 除非使用 `SELECT DISTINCT dept_name`
	- 而使用 `SELECT ALL dept_name` 表示 dup 都会保留
- `SELECT * FROM instructor` 选择所有的列
- `SELECT '437` 没有 `FROM`，会得到一行一列的有 437 的表格
	- `SELECT '437' AS FOO` 给列重命名
- `SELECT 'A' FROM instructor` 会得到一列 N 行，每一行都是 `A`
- `SELECT` 中可以使用数学表达式，前提是 data type 支持
	- `SELECT ID, name, salary/12`
	- `SELECT ID, name, salary/12 AS monthly_salary`

## Where Clause

- 表示 conditions
- 可以使用算术表达式和逻辑表达式
	- `SELECT name FROM instructor WHERE dept_name = 'Comp. Sci. AND salary > 70000`

## From Clause

- `SELECT * FROM instructor, teaches` 进行笛卡尔积

# Additional Basic Operations

## Rename Operation

- `old-name AS new-name`

```sql
SELECT DISTINCT T.name
FROM instructor AS T, instructor AS S
WHERE T.salary > S.salary AND S.dept_name = 'Comp. Sci.'
```

> [!question] Question
> - 如果使用 `DISTINCT`，可能有重名的无法都显示
> - 如果不适用 `DISTINCT`，工资高的会出现很多次

![[IMG-DB 03 Introduction to SQL-20250225154808709.webp|400]]

## String Operations

- `%` 匹配所有 substring
- `_` 匹配所有 char

```sql
SELECT name
FROM instructor
WHERE name LIKE '%dar%'
```

## Order by

```sql
SELECT DISTINCT name
FROM instructor
OEDER BY name ASC/DESC  # 升序降序
ORDER BY dept_name, name  # multiple attr
```

## Set Op

```sql
(SELECT course_id FROM section WHERE sem = 'Fall' AND year = 2017)
UNION/INTERSECT/EXCEPT
(...)
```

> [!note] Note
> 集合默认不重复，除非使用 `{sql}UNION/INTERSECT/EXCEPT ALL`

## Null

- null signifies
	- unknown
	- not exist
- 任何表达式含有 null，则结果是 null
	- e.g. `{sql}5 + null = null`
- predicate: `{sql}IS NULL / IS NOT NULL`
- 任何比较含有 null，则结果是 unknown
	- e.g. `{sql}5 < NULL / NULL <> NULL / NULL = NULL`
- 布尔运算定义扩展，返回肯定对的结果
	- and: `{sql}(true and unknown) = unknown, (false and unknown) = false, (unknown and unknown) = unknown`
	- or: `{sql}(unknown or true) = true, (unknown or false) = unknown, (unknown or unknown) = unknown`
	- ! 如果结果是 unknown，predicate 在 `{sql}WHERE` 语句中被当成 false

## Aggregate Functions

- 这些函数在 multiset 多重集上计算，允许重复元素
	- avg, min, max, sum, count

```sql
SELECT AVG(salary)
FROM instructor
WHERE dept_name = 'Comp. Sci.';

SELECT COUNT(DISTINCT ID)  # 一位老师可能开多门课
FROM teaches
WHERE semester = 'Spring' AND year = 2018;

SELECT COUNT(*)
FROM course;
```

### `GROUP BY`

```sql title="find the avg salary of instructors in each dept"
/* SELECT dept_name, ID, AVG(salary) error，分组和显示 ID 矛盾 */
SELECT dept_name, AVG(salary) AS avg_salary
FROM instructor
GROUP BY dept_name;
```

### `HAVING`

```sql
SELECT dept_name, AVG(salary) AS avg_salary
FROM instructor
GROUP BY dept_name
HAVING AVG(salary) > 42000;
```

## Nested Subqueries

### Set Membership

```sql
WHERE course_id IN / NOT IN (SELECT coutse_id FROM section WHERE semester = 'Sprint'AND year = 2018)
WHERE name NOT IN ('Mozard', 'Einstein')
WHERE (course_id, sec_id, semester, year) IN (SELECT course_id, sec_id, semester, year FROM teaches WHERE teaches.ID = 10101)
```

### Set Comparison

#### `SOME`

```sql title="Find names of instructors with salary greater than that of some (at least one) instructor in the Biology department."
SELECT DISTINCT T.name
FROM instructor AS T, instructor AS S
WHERE T.salary > S.salary AND S.dept_name = 'Biology';

SELECT name  /* 注意这里不需要使用 DISTINCT，因为没有笛卡尔积 */
FROM instructor
WHERE salary > SOME(
	SELECT salary
	FROM instructor
	WHERE dept_name = 'Biology'
);
```

> `{sql}= SOME(...)` 相当于 `IN`，但是 `{sql}!= SOME(...)` 不等于 `NOT IN`

#### `ALL`

```sql
SELECT name  /* 注意这里不需要使用 DISTINCT，因为没有笛卡尔积 */
FROM instructor
WHERE salary > ALL(
	SELECT salary
	FROM instructor
	WHERE dept_name = 'Biology'
);
```

> `{sql}!= ALL(...)` 相当于 `NOT IN`，但是 `{sql}= ALL(...)` 不等于 `IN`

#### `EXISTS`

```sql
EXISTS r  /* r is not an empty set */
NOT EXISTS r  /* r is an empty set */
```

```sql title="Find all courses taught in both the Fall 2017 semester and in the Spring 2018 semester"
SELECT course_id
FORM section AS S
WHERE semester = 'Fall' AND year = 2017 AND EXISTS(
	SELECT *
	FROM section AS T
	WHERE semester = 'Spring' AND year = 2018 AND S.course_id = T.course_id
);
```

```sql title="Find all students who have taken all courses offered in the Biology department."
SELECT DISTINCT S.ID, S.name
FROM student AS S
/* where required courses is a subset of taken courses */
WHERE NOT EXISTS(
	(SELECT course_id FROM course WHERE dept_name = 'Biology')
	EXCEPT
	(SELECT course_id FROM takes AS T WHERE S.ID = T.ID)
);
```

- $X-Y=\emptyset\Leftrightarrow X\subseteq Y$

#### `UNIQUE`

- 检查子查询中是否有重复的 tuple

```sql title="find all courses that were offered at most once in 2017"
SELECT T.course_id
FROM course AS T
WHERE UNIQUE(
	SELECT R.course_id
	FROM section AS R
	WHERE T.course_id = R.course_id AND R.year = 2017
);
```

### With Clause

```sql
WITH max_budget(value) AS (
	SELECT MAX(budget)
	FROM department
)
SELECT department.name
FROM department, max_budget
WHERE department.budget = max_budget.value;
```

> 将子查询重命名

### Scalar Subquery

```sql title="list all departments along with the number of instructors"
SELECT dept_name, (SELECT COUNT(*) FROM instructor WHERE department.dept_name = instructor.dept_name) AS num_instructors
FROM department
```

> [!note] Note
> 和 `GROUP BY` 不同，如果有没有 instructor 的 dept，也会显示出来

# Modification

## Deletion

```sql
DELETE FROM instructor
WHERE dept_name = 'Finance'
WHERE salary < (SELECT AVG(salary) FROM instructor);
```

## Insertion

```sql
INSERT INTO course VALUES ('CS-437', 'Database Systems', 'Comp. Sci.', 4);  /* 默认插入所有参数 */
INSERT INTO course(course_id, title, dept_name) VALUES ('CS437', 'Database Systems', 'Comp. Sci.');
```

```sql title="Music dept 的所有学分大于 144 的学生都成为 instructor 且薪资 18000" hl=2
INSERT INTO instructor
	SELECT ID, name, dept_name, 18000
	FROM student
	WHERE dept_name = 'Music' AND total_cred > 144;
```

## Update

> 对表中满足一些条件的 tuple 的值进行更新

```sql title="薪水小于 70000 的涨 5%"
UPDATE instructor
SET salary = salary * 1.05
WHERE salary < (SELECT AVG(salary) FROM instructor)
```

```sql title="用 case 语句解决条件更新顺序问题"
UPDATE instructor
SET salary = CASE
	WHEN salary <= 100000 THEN salary * 1.05
	ELSE salary * 1.03
END
```

```sql title="更新学分"
UPDATE student S
SET tot_cred = (
	SELECT CASE /* 能够覆盖没有修读任何课程的情况 */
		WHEN SUM(credits) IS NOT NULL THEN SUM(credits)
		ELSE 0
	END
	FROM takes T, course C
	WHERE T.course_id = C.course_id AND
		S.ID = T.ID AND
		T.grade <> 'F' AND
		T.grade IS NOT NULL
)
```
