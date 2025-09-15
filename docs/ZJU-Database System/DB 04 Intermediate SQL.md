---
status:
  - archived
tags: CS/DB/SQL
date_created: 2025-03-04T15:29:51
date_modified: 2025-09-13T10:18:12
---

# Join Expressions

| join types        | join conditions     |
| ----------------- | ------------------- |
| join (inner join) | `NATURAL`           |
| left outer        | `ON <predicate>`    |
| right outer       | `USING(A1, A2,...)` |
| full outer        |                     |
| **定义了不匹配键的处理方式**  | **定义了用于匹配的键**       |

## Join Conditions

### Natural

> 相同的属性，只留下一个

```sql
SELECT name, course_id
FROM student, takes
WHERE student.ID = takes.ID;

SELECT name, course_id
FROM student NATURAL JOIN takes;
```

![[IMG-DB 04 Intermediate SQL-20250304154053434.webp|400]]

> 如上图，只保留了一列 ID 属性

> [!warning] Warning
> 使用 `{sql}NATURAL JOIN` 的话，会自动将命名相同的属性匹配，但是可能这些属性的含义并不一样
> e.g. 学生的学院和学生上课的开课学院

```sql title="使用 using 来声明连接属性"
SELECT name, title
FROM (student NATURAL JOIN takes) join course USING (coutse_id);
```

### Others

- `ON` 会保留多个属性
- `USING(A1, A2,...)` 会将声明的同名属性合并

## Join Types

- `JOIN` 默认使用 `INNER JOIN`，不会保留有 `NULL` 的 tuple

### Outer Join

> [!note] Note
> 如果 A 中的一个元素无法在 B 中找到匹配，也保留并补充空值
> e.g. 一个没有修任何课程的学生，也希望在 `{sql}student JOIN takes` 中

- left outer join: 保留左边的全部信息
- right outer join: 保留右边
- full outer join: 保留两边

# Views

- 用于向部分用户仅展示部分信息 *hide certain data from the view of certain users*
- Any relation that is not of the conceptual model but is made visible to a user as a *virtual relation* is called a **view**

## Definition

```sql
CREATE VIEW v AS
< query exp >;
```

- view definition 和使用 query 创建新的 relation 不同
	- view definition 导致了 **the saving of an expression**，存储了查询表达式

```sql title="example"
CREATE VIEW faculty AS
	SELECT ID, name, dept_name
	FROM instructor;

CREATE VIEW dept_total_salary(dept_name, total_salary) AS
	SELECT dept_name, SUM(salary)
	FROM instructor
	GROUP BY dept_name;
```

### by using other views

- 一个视图的定义可能依靠其他视图
- v1 is said to **depend directly** on v2，如果 v2 出现在了 v1 的定义中
- v1 is said to **depend on** v2，如果直接依赖、或者存在到 v2 的依赖路径
- v 可以是 **recursive** 的，如果依赖自己定义

```sql title="example"
CREATE VIEW physics_fall_2017 AS
	SELECT course, course_id, sec_id, building, room_number
	FROM course, section
	WHERE course.course_id = section.course_id
		AND course.dept_name = 'Physics'
		AND section.semester = 'Fall'
		AND section.year = '2017';

CREATE VIEW physics_fall_2017_watson ON
	SELECT course_id, room_number
	FROM physics_fall_2017
	WHERE building = 'Waston';
```

## Expansion

```sql
CREATE VIEW physics_fall_2017_watson ON
	SELECT course_id, room_number
	FROM physics_fall_2017
	WHERE building = 'Waston';

# expand to:

CREATE VIEW physics_fall_2017_watson ON
	SELECT course_id, room_number
	FROM (
		SELECT course, course_id, sec_id, building, room_number
		FROM course, section
		WHERE course.course_id = section.course_id
			AND course.dept_name = 'Physics'
			AND section.semester = 'Fall'
			AND section.year = '2017'
	)
	WHERE building = 'Waston';
```

- 只要不是 recursive，总会得到展开结果

## Materialized Views

- 一些 DBMS 允许 view 能被物理存储
	- 在定义时 copy
- 如果 relation 中的数据有更新，materialized view 需要维护

## Update of a View

- 多数 SQL 都只支持简单视图的更新
	- `FROM` 只有一张表
	- `SELECT` 只有字段名，没有表达式，aggregates 或者 `DISTINCT`
	- 所有没有放在 `SELECT` 中的字段名允许 `NULL`
	- 没有 `GROUP BY` 或者 `HAVING` 语句

### examples

```sql title="example"
INSERT INTO faculty VALUES ('30756', 'Green', 'Music');
```

`faculty` 是 `instructor` 的视图，没有插入 `salary` 字段，有两种解决方法

- 拒绝插入
- 插入 null

```sql title="some updates cannot be translated uniquely"
CREATE VIEW instructor_info AS
	SELECT ID, name, building
	FROM instructor, department
	WHERE instructor.dept_name = department.dept_name;

INSERT INTO instructor_info VALUES ('67890', 'White', 'Taylor');
```

- 如果 `Taylor` 有多个 department，是哪个？
- 如果 `Taylor` 没有 department 怎么办？

```sql title="simple view outlier"
CREATE VIEW history_instructors AS
	SELECT *
	FROM instructor
	WHERE dept_name = 'History';

INSERT INTO history_instructors VALUES ('124554', 'Brown', 'Biology', 100000);  # 无法插入
```

# Index

- 一张表上的 index 是一种**数据结构**，使得数据库系统能够快速查找一些类型的 tuple

```sql tilte="create index command"
CREATE INDEX <name> ON <relation-name> (attr);

CREATE INDEX stuID_index on student(ID);

SELECT *
FROM student
WHERE ID = '12345';  # 能直接使用已有的 index 来查询
```

# Transactions

- A **transaction** consists of a sequence of query and/or update statements and is a "unit" of work.
- transaction 一定以下面一种声明结束
	- **Commit work**: 提交 transaction 中的所有操作（永久化）
	- **Rollback work**: undone transaction 中的所有操作
- Atomic transaction: 只能完全执行或者 rollback

# Integrity Constraints

- `{sql}NOT NULL` 不允许字段为空
- `{sql}UNIQUE (A1, A2, ..., An)` 声明 `(A1, A2, ..., An)` 是一个 **super key**
	- 和主键不同，candidate keys 允许为 null
- `{sql}CHECK (P)`
	- `{sql}CHECK (semester in ('Fall', 'Winter', 'Spring', 'Summer')`
	- check 的条件可以非常复杂，可以嵌套 query

## Referential Integrity

- 保证一张表中出现的一些值能够对应到其他一些表上的一些值（foreign key）
	- `{sql}FOREIGN KEY (dept_name) REFERENCES department` 默认 ref 对应表的 primary key
	- `{sql}FOREIGN KEY (dept_name) REFERENCES department (dept_name)` 也可以自定义

```sql
CREATE TABLE person (
	ID CHAR(10),
	name CHAR(40),
	mother CHAR(10),
	father CHAR(10),
	PRIMARY KEY ID,
	FOREIGN KEY father REFERENCES person,
	FOREIGN KEY mother REFERENCES person
)
```

那么在插入的时候，要么先将 `father, mother` 设置为 `null`，要么取消 `FOREIGN KEY` 约束

## Cascading Actions

```sql title="example"
CREATE TABLE course (
	...,
	dept_name VARCHAR(20),
	FOREIGN KEY (dept_name) REFERNECES department
		ON DELETE CASCADE
		ON UPDATE CASCADE
	...
)
```

也可以用 `{sql}ON DELETE SET NULL / ON UPDATE SET DEFAULT`

## Assertions

- 表述 db 需要 **always to satisfy** 的条件
- `{sql}CREATE ASSERTION <assertion-name> CHECK (<predicate>);`

# Triggers

- 系统根据数据库的修改自动执行的语句
- **ECA** rule
	- E: event
	- C: condition
	- A: action
- introduced in SQL 1999

```sql title="example"
CREATE TRIGGER setnull_trigger BEFORE UPDATE OF takes ON grade
REFERENCING NEW ROW AS nrow
FOR EACH ROW
	WHEN (nrow.grade = '')
	BEGIN ATOMIC
		SET nrow.grade = NULL;
end;
```

- event: `BEFORE/AFTER INSERT/DELETE/UPDATE OF <relation>`
	- 可以细化到 attr `... ON <attr>`
- `REFERENCING OLD/NEW ROW AS`

```sql title="trigger to maintain credits_earned value"
CREATE TRIGGER credits_earned AFTER UPDATE OF takes ON (grade)
REFERENCING NEW ROW AS nrow
REFERENCING OLD ROW AS orow
FOR EACH ROW
WHEN nrow.grade <> 'F' AND nrow.grade IS NOT NULL
	AND (orow.grade = 'F' OR orow.grade IS NULL)
BEGIN ATOMIC
	UPDATE student
	SET tot_cred = tot_cred + (
		SELECT credits
		FROM course
		WHERE course.course_id = nrow.course_id
	)
	WHERE student.id = nrow.id;
END;
```

## when not to use

- 现在有更好的方法（materialized view）
- 可以封装方法，在更新的时候同时执行，而不是使用触发器
- risk of unintended execution
	- 从 backup 中加载数据
	- 将更新传递到远程数据库
	- tip: 执行这些操作时可以 disable 触发器

# Data Types

## Built-in Data Types in SQL

- date: `DATE '2005-7-27'`
- time: `TIME '09:00:30'`, `TIME '09:00:30.75'`
- timestamp: `TIMESTAMP '2005-7-27 09:00:30.75'`
- interval: `INTERVAL '1' DAY`

## Large-Object Types

- `BLOB`: binary large object
- `CLOB`: character alrge object

```sql title="example"
book_review CLOB(10kB),
image BLOB(10MB),
movie BLOB(2GB)
```

- query 返回的不是大文件本身，而是一个 **pointer**(定位器)

## User-Defined Types

```sql title="example"
CREATE TYPE Dollars AS NUMBERIC (12, 2) FINAL;

CREATE TABLE department (
	dept_name VARCHAR(20),
	building VARCHAR(15),
	budget Dollars
);
```

## Domains

- 和 types 相似，但是可以有 constraints

```sql
CREATE DOMAIN person_name CHAR(20) NOT NULL;

CREATE DOMAIN degree_level VARCHAR(10)
	CONSTRAINT degree_level_test
		CHECK (VALUE IN ('Bachelors', 'Masters', 'Doctorate'));
```

# Authorization

## Grant

```sql
GRANT <privilege_list> ON <relation or view> TO <user_list>
```

- `<user_list>`
	- a user-id
	- `PUBLIC` 所有合法用户
	- a role (more on this later)
- 给视图权限不意味着给依赖的 relation 的权限
- 给权限的人 (grantor) 一定有这个权限

## Privileges

- select
- insert
- update
- delete
- all privileges

## Revoke

```sql
REVOKE <privilege_list> ON <relation or view> FORM <user_list>
```

- ! 如果一个用户的一个权限被不同用户赋予了两次，可能仍然会拥有这个权限
- 所有依赖于这个用户的权限的权限都会被 revoke *级联删除*

## Roles

```sql
CREATE ROLE <name>
GRANT <role> TO <users>

CREATE ROLE dean;
GRANT instructor TO dean;
GRANT dean TO Satoshi;
```

## Authorization on Views

```sql
CREATE VIEW geo_instructor AS
(
	SELECT *
	FROM instructor
	WHERE dept_name = 'Geology'
);

GRANT SELECT ON geo_instructor TO geo_staff;
```

- view creator 需要有 `instructor` 的 `SELECT` 权限才能创建 view
- geo_staff 可以没有 `instructor` 的任何权限？

## Other Features

### References 权限

- 有了才能去另一个 relation 引用 Foreign key
- `{sql}GRANT REFERENCE (dept_name) ON department TO Mariano;`

### Transfer of privileges

```sql title="example"
GRANT SELECT ON department TO Amit WITH GRANT OPTION;
REVOKE SELECT ON department FROM Amit, Satoshi CASCADE;
REVOKE SELECT ON department FROM Amit, Satoshi RESTRICT;
```
