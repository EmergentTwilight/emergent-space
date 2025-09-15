---
status:
  - archived
tags: CS/DB/SQL
date_created: 2025-03-18T13:25:59
date_modified: 2025-09-13T10:18:12
---

# Accessing SQL from a Programming Lang.

- 不是所有 query 都能表达为 SQL 语句
- 非声明式操作，例如交互，不能用 SQL 完成
- 2 approaches
	- **dynamic SQL**: 使用一些函数与 db 进行交流，运行时
		- JDBC, Python Database API, ODBC
	- **embedded SQL**: 将源码中的 SQL 语句在编译时特殊处理，转换为函数调用

## JDBC

- app makes calls to
	- 与数据库服务器建立连接
	- 发送 SQL 命令
	- fetch tuples of result one-by-one into program variables
- JDBC
	- 支持 metadata 查询，例如查询有什么 relation，有什么 attr，attr 的类型

```java
public static void JDBCexample(String dbid, String userid, String passwd)
{
	try (
		Connection conn = DriverManager.getConnection("jdbc:oracle:thin:@db.yale.edu:2000:univdb", userid, passwd);
		Statement stmt = conn.createStatement();
	) {
		// do actual work
	}
	catch (SQLException sqle) {
		System.out.println("SQLException: " + sqle);
	}
	
	// update
	try {
		stme.executeUpdate(
			"insert into instructor values('12344', 'Kem', 'Physics', 80000)"
		);
	}
	catch (SQLException sqle) {
		System.out.println("Could not insert tuple. " + sqle);
	}
	
	// query
	ResultSet rest = stmt.executeQuery(
		"select dept_name, avg(salary)
		from instructor
		group by dept_name"
	);
	while(rset.next()) {
		System.out.println(rset.getString("dept_name") + "" + rset.getFloat(2));
	}
}
```

## Prepared Statement

```java
PreparedStatement pStmt = conn.prepareStatement("insert into instructor values(?, ?, ?, ?)");

pStmt.setString(1, "18930");
pStmt.setString(2, "Perry");
pStmt.setString(3, "Finance");
pStmt.setInt(4, 123445);
pStmt.executeUpdate();
pStmt.setString(1, "18931");
pStmt.executeUpdate();
```

- query 能够一次编译，多次使用不同的参数运行
- 如果需要用户输入，也很方便
- **能够避免 SQL 注入风险**

## Metadata Features

![[IMG-DB 05 Advanced SQL-20250318141526626.webp|500x336]]

## Transaction Control

```java
conn.setAutoCommit(false);
conn.commit();
conn.rollback();
```

## SQLJ

> embedded SQL in Java

```java
#sql iterator deptInfoIter(String dept_name, int avgSal);
deptInfoIter = null;
#sql iter = { select dept_name, avg(salary) from instructor group by dept_name };
while (iter.next()) {
	String deptName = iter.dept_name();
	int avgSal = iter.avgSal();
	System.out.println(deptName + "" + avgSal);
}
iter.close();
```

- host language 宿主语言
- `EXEC SQL` 语句来标记嵌入 SQL `EXEC SQL <embedded SQL statement>`

## Embedded SQL

```
EXEC-SQL connect to server user user-name using password;  // 连接到服务器

EXEC-SQL BEGIN DECLARE SECTION
	int credit_amount;
EXEC SQL END DECLARE SECTION  // 使用 :credit-amount 来引用 host lang 中的变量

EXEC-SQL
	DECLARE c CURSOR FOR
	SELECT ID, name
	FROM student
	WHERE tot_cred > :credit_amount;
END_EXEC
```

*omitted*

# Functions and Procedures

## Functions

```sql title="function"
CREATE FUNCTION deptCount (dept_name VARCHAR(20))
	RETURNS INTEGER
	BEGIN
	DECLARE d_count INTEGER;
		SELECT COUNT(*) INTO d_count
		FROM instructor
		WHERE instructor.dept_name = dept_name
	RETURN d_count;
END

SELECT dept_name, budget
FROM department
WHERE dept_count (dept_name) > 12;
```

- db 支持表函数，返回的是 relation

```sql title="table function"
CREATE FUNCTION instructor_of (dept_name CHAR(20))
	RETURNS TABLE (
		ID VARCHAR(5),
		name VARCHAR(20),
		dept_name VARCHAR(20),
		salary NUMERIC(8, 2)
	)
	RETURN TABLE (
		SELECT ID, name, dept_name, salary
		FROM instructor
		WHERE instructor.dept_name = instructor_of.dept_name
	)

SELECT *
FROM TABLE (instructor_of('Music'))*
```

## Procedures

```sql title="procedure"
CREATE PROCEDURE dept_count_proc (IN dept_name VARCHAR(20), OUT d_count INTEGER)
BEGIN
	SELECT COUNT(*) INTO d_count
	FROM instructor
	WHERE instructor.dept_name = dept_count_proc.dept_name
END

DECLARE d_count INTEGER;
CALL dept_count_proc('Physics', d_count);
```

## Language Constructs

```sql
BEGIN ... END

WHILE <boolean_exp> DO
	...
END WHILE

REPEAT
	...
UNTIL <boolean_exp>
END REPEAT

FOR item AS
	<query>
DO
	...
END FOR

IF <boolean_exp>
	THEN ...
ELSEIF <boolean_exp>
	THEN ...
ELSE ...
END IF
```

```sql title="example"
DECLARE n INTEGER DEFAULT 0;
FOR r AS
	SELECT budget FROM department
	WHERE dept_name = 'Music'
DO
	SET n = n + r.budget
END FOR
```
