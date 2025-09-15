---
status:
  - archived
date_created: 2025-06-07T14:55:46
date_modified: 2025-09-13T10:16:35
---

# Relational Languages

## Relational Model

- 关系数据库结构
	- relation 就是 table
	- tuple 就是行，也是 relation instance
	- attr 就是列，具有 domain，null 是一个特殊的值
- 数据库模式，schema 是一个模式，instance 是一个快照
- key
	- superkey 唯一标识
	- candidate key 最小的 superkey
	- primary key 人为定义的 candidate key
	- foreign key
		- referencing/referenced relation
		- referential integrity constraint 参照完整性约束，要求参照关系每个元素的参照属性取值必须为被参照关系上的被参照属性的取值中的一个
- schema diagram：矩形，上面是表名，下面属性下划线标识 primary key，外键参照用箭头指向，和 E-R 区分，更像是化简后更接近逻辑实现的结果
- query lang
	- procedural lang 过程化语言，需要用户指导系统如何计算
	- nonprocedural lang 非过程化语言，用户只需要描述需要的信息
	- SQL 两者
- 关系运算
	- ! 注意 relation 都是集合
	- 基本运算 $\sigma,\Pi,\times,\cup,-,\rho$
		- $\cup$ 的要求
			- attr 数量一致
			- attr domain 对应兼容
	- 附加运算 $\cap,\bowtie,\leftarrow,⟕,⟗,⟖$
		- 自然连接的形式化定义 $r\bowtie s=\Pi_{R\cup S}(\sigma_{r.A_1=s.A_1\land r.A_2=s.A_2\land\dots\land r.A_n=s.A_n}(r\times s))$，其中 $R\cap S=\{A_1, A_2, \dots, A_n\}$
			- 如果 $R\cap S=\emptyset$，那么 $r\bowtie s=r\times s$
			- 另外 $r\bowtie_\theta s=\sigma_\theta(r\times s)$
		- $\leftarrow$ 是赋值运算，例如 $temp1\leftarrow R\times S$
		- 左右外连接都是可以用基本关系代数表示的

## SQL

- 三种语言
	- DDL 数据定义语言 `create, alter, drop, truncate, rename`
	- DML 数据操作语言 `select, insert, update, delete`
	- DCL 数据控制语言 `grant, revoke`
- union 操作？set differenct

### Final Example

```sql title="23 春夏标答"
SELECT DISTINCT group_name
FROM user
WHERE gender = "male";


SELECT u.user_id, u.name
FROM user AS u, followship AS f
WHERE u.user_id = f.follower_id AND f.user_id = "1001" and u.age > 18;


SELECT group_name
FROM user
WHERE gender = "female"
GROUP BY group_name
HAVING COUNT(user_id) > ALL (
	SELECT COUNT(user_id)
	FROM user
	WHERE gender = "female"
	GROUP BY group_name
);

WITH female_user_cnt(group_name, cnt) AS (
	SELECT group_name, COUNT(user_id)
	FROM user
	WHERE gender = "female"
	GROUP BY group_name
)
SELECT group_name
FROM female_user_cnt
WHERE cnt = (
	SELECT MAX(cnt)
	FROM female_user_cnt
);


WITH follower_cnt(user_id, cnt) AS (
	SELECT u.user_id, COUNT(f.follower_id)
	FROM user AS u, followship AS f
	WHERE u.user_id = f.user_id AND u.group_name = "game"
	GROUP BY u.user_id
)
SELECT u.user_id, u.name, f.cnt
FROM user AS u, follower_cnt AS f
WHERE u.user_id = f.user_id AND f.cnt > (
	SELECT AVG(cnt)
	FROM follower_cnt
);
```

```sql title="22春夏"
SELECT *
FROM course
WHERE department = "CS" AND credits >= ALL (
	SELECT credits FROM course WHERE department = "CS"
);

SELECT *
FROM course
WHERE department = "CS" AND credits = (
	SELECT MAX(credits) FROM course WHERE department = "CS"
);


SELECT department
FROM course
GROUP BY department
HAVING SUM(credits) >= ALL (
	SELECT SUM(credits) FROM course GROUP BY department
);


SELECT C1.course-id, C2.course-id, C1.title
FROM course AS C1, course AS C2
WHERE C1.title = C2.title AND C1.course-id <> C2.course-id;


SELECT c.course-id, c.title, COUNT(p.course-id)
FROM course AS c LEFT OUTER JOIN prereq AS p ON (c.course-id = p.prereq-id)  -- 这里的 left outer join 非常关键
GROUP BY c.course-id;
```

```sql title="20 春夏标答"
CREATE TABLE participate (
	pId char(10),
	sId char(10),
	role varchar(20),
	primary key (pId, sId),
	foreign key (pId) references project(pId),
	foreign key (sId) references student,
	check (role = "leader" or role = "member")
);

SELECT DISTINCT tName
FROM project, teacher
WHERE project.tId = teacher.tId AND startTime between '2020-01-01' AND '2020-12-31';

SELECT sName
FROM student
WHERE sId in (
	SELECT sId
	FROM participate
	GROUP BY sId
	HAVING COUNT(pId) > 2
);
```

```sql title="20 春夏标答"
CREATE TABLE participate(
	pId CHAR(20),
	eId CHAR(20),
	role VARCHAR(20),
	PRIMARY KEY (eId, pId),
	FOREIGN KEY (pId) REFERENCES project(pId),
	FOREIGN KEY (eId) REFERENCES employee(eId),
	CHECK (role IN ("project manager", "developer", "tester"))
);


SELECT eName
FROM employee
WHERE eId IN (
	SELECT eId
	FROM participate
	GROUP BY eId
	HAVING COUNT(DISTINCT role) = 3
);  -- 这个非常重要


SELECT e.eName
FROM employee AS e NATURAL JOIN participate AS p
WHERE p.pId = "p1102" AND e.eSalary = (
	SELECT MAX(e1.eSalary)
	FROM employee AS e1 NATURAL JOIN participate AS p1
	WHERE p1.pId = "p1102"
);
```

```sql title="19 春夏标答"
UPDATE Comment SET grade = 0 WHERE grade IS NULL;

WITH movie_grade(title, avg_grade) AS (
	SELECT title, AVG(grade)
	FROM Comment
	GROUP BY title
)
SELECT title
FROM movie_grade
WHERE avg_grade = (
	SELECT MAX(avg_grade)
	FROM movie_grade
);

SELECT title
FROM Comment
GROUP BY title
HAVING(AVG(grade)) >= ALL (
	SELECT AVG(grade)
	FROM Comment
	GROUP BY title
);


SELECT title FROM movie
EXCEPT
SELECT title FROM movie
WHERE EXISTS (
	SELECT *
	FROM Comment AS A, Comment AS B
	WHERE A.title = movie.title AND A.user_name = B.user_name AND B.title = "the avenger" AND A.grade <= B.grade
);  -- 所有减去不满足的，exist 能够检测不满足的情况
```

### DDL

- `smallint` 机器相关的小整数
- `numeric(p, d)` 定点数，p 位数字 + 一个符号位，其中 d 位数字在小数点右侧
- `real, double precision` 浮点，双精度浮点
- `float(n)` 精度至少为 n 位的浮点数，n 代表总的位数而不是小数位
- 视图默认是非物化的，查询时才会生成，标准 SQL 无法定义物化视图
- `CKECK` 中也支持插入子查询
- 大对象类型 `CLOB(10KB), BLOB(2GB)`

```sql
CREATE TABLE course (
	course_id CHAR(2),
	credit INT NOT NULL,
	prereq_id CHAR(2),
	PRIMARY KEY (course_id),
	FOREIGN KEY (prereq_id) REFERENCES course(course_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	CKECK (semester IN ('Fall', 'Winter', 'Spring', 'Summer'))
);

ALTER TABLE course ADD (
	textbook VARCHAR(80)
);

ALTER TABLE course DROP (textbook);

ALTER TABLE course ADD <constraint>;

DROP TABLE course;

CREATE VIEW v(value1, value2) AS <query expression>;

CREATE INDEX index00 ON student(ID);
```

### DML 操作

- `CASE` 语句，一般都是 `CASE WHEN p THEN r WHEN p1 THEN r1 ELSE r2`

```sql
INSERT INTO course VALUES ('77', 4, '11');
INSERT INTO course (credit, prereq_id, course_id)
	VALUES (4, '11', '77');

DELETE FROM course WHERE course_id = '11';
DELETE FROM instructor
	WHERE salary < (SELECT AVG(salary) FROM instructor);

UPDATE course SET course_id = '11' credit = 2 WHERE course_id = '33';
UPDATE instructor
	SET salary = salary * 1.5
	WHERE salary < (SELECT AVG(salary) FROM instructor);
UPDATE instructor
	SET salary = CASE
		WHEN salary <= 100000 THEN salary * 1.05
		ELSE salary * 1.03
	END;
```

### DML 查询

- `SELECT ID, name, salary * 1.1`
- `FROM r, s` 其实相当于在构造笛卡尔积 `CROSS JOIN`
- natural join: 在两个关系中都出现的属性值上取值相同，则连接
	- `FROM (instructor NATURAL JOIN teaches) JOIN course USING (course_id)` SQL 提供了一种自然丽娜姐的构造形式
	- 更多用的是 `r JOIN s ON ...`
- ==不同的连接==
	- `NATURAL (INNER) JOIN`: 一般不用，因为隐藏了连接条件
	- `INNER JOIN (JOIN)`: 常用，只保留匹配的
	- `LEFT/RIGHT (OUTER) JOIN`: 会保留左/右没有匹配的元组，匹配 null
	- `FULL (OUTER) JOIN`: 全外连接，左右没有匹配的都保留
	- `CROSS JOIN`: 标准笛卡尔积，没有基于属性的匹配
- 重命名：`SELECT name AS new-name FROM instructor AS I, courses AS C`
- 字符串：`WHERE building LIKE '%Was\%ton%' ESCAPE '\`
	- `_` 匹配任意字符
	- `%` 匹配任意字串
	- `___%` 匹配长度至少为 3 的字串
	- 可以自定义转义字符，用于匹配百分号或下划线
- `SELECT instructor.*, course.ID`
- `ORDER BY salary DESC, name ASC`
- `WHERE salary BETWEEN 90000 AD 100000` 或者 `NOT BETWEEN`
- `(...) UNION (...)` 自动去除重复 tuple，`UNION ALL` 能保留重复
- `(...) INTERSECT (...)` 同样有 `INTERSECT ALL`
- `(...) EXCEPT (...)` 同样有 `EXCEPT ALL`
- `WHERE salary IS NULL / IS NOT NULL`
- 聚集函数 `AVG, MIN, MAX, SUM, COUNT`
	- 默认考虑重复，使用 `COUNT (DISTINCT ID)` 同一个只计算一次
		- 例如一个教师，即使教了很多门课，ID 计数也是 1
	- 控制默认不考虑
	- 布尔值聚集 `SOME EVERY`
- `HAVING AVG(salary) > 42000` 必须结合 `GROUP BY` 使用，具体查询流程
	- 用 from 计算出一个关系
	- 应用 where 筛选条件
	- 根据 group by 分组
	- 如果有 having，则判断哪些组需要保留
	- 最后用 select 选择需要显示的属性
- 嵌套子查询
	- `IN / NOT IN` 判断是不是子查询结果的成员
	- `WHERE salary > SOME ( SELECT salary FROM ...)`
		- ` = SOME <==> IN, <> SOME <==> NOT IN`
		- `<> ALL <==> NOT IN, = ALL <=/=> IN`
	- `WHERE EXISTS (...)` 判断子查询是否为空
	- `WHERE UNIQUE (...)` 判断子查询中是否存在重复值
- `WITH max_budget (value) AS (SELECT MAX(budget) FROM department)` 用 with 语句需要显式定义属性名称
- ==实现 $\forall X, P(X)$ 需要使用 `NOT EXISTS (<query for X> WHERE <not P>)`，即不存在不满足 $P$ 的 $X$==

![[IMG-DB Cheatsheet-20250607155116482.webp]]

```sql
SELECT DISTINCT group_name
FROM user
WHERE gender = 'male';

SELECT u.name, u.gender, u.age, u.group_name
FROM followship f JOIN user u ON f.followerID = u.userID
WHERE f.userID = '1001';

WITH female_cnt AS (
	SELECT group_name, COUNT(*) AS cnt
	FROM user
	WHERE gender = 'female'
	GROUP BY group_name;
)
SELECT group_name
FROM user
WHERE gender = 'female'
GROUP BY group_name
HAVING COUNT(*) = (
	SELECT MAX(cnt)
	FROM female_cnt
);

WITH game_follower_cnt AS (
	SELECT u.userID AS userID, COUNT(f.followerID) AS cnt
	FROM user u JOIN followship f ON u.userID = f.userID
	WHERE group_name = 'game'
	GROUP BY u.userID
)
SELECT u.userID, u.name
FROM user u JOIN game_follower_cnt g ON u.userID = g.userID
WHERE g.cnt > (
	SELECT AVG(cnt)
	FROM game_follower_cnt
);
```

### DCL

```sql
GRANT <权限列表>
ON <关系或视图名> -- e.g. SELECT ON department, UPDATE (budget) ON department
TO <用户/角色列表>;
-- WITH GRANT OPTION;

REVOKE ...
-- RESTRICT 防止级联收回

CREATE ROLE instructor;
```

### JDBC

```java
PreparedStament pstmt = conn.prepareStatement("insert into instructor values(?, ?, ?, ?)");
pstmt.setString(1, "88877");
pstmt.setString(2, "Perry");
...
pstmt.executeUpdate();
```

```java title="sql 注入"
"SELECT * FROM instructor WHERE name ='" + name + "'"
name = "X' or 'Y' = 'Y"
```

预备语句中，会将 `'` 转义为 `\'`

### Functions and Procedures

```sql
CREATE FUNCTION deptCount (dept_name VARCHAR(20))
	RETURNS INTERGER
	BEGIN
	DECLARE d_count INTEGER;
		SELECT COUNT(*) INTO d_count
		FROM instructor
		WHERE instructor.dept_name = dept_name
	RETURN d_count;
	END

CREATE PROCEDURE dept_count_proc(IN dept_name VARCHAR(20), OUT d_count INTEGER)
	BEGIN
		SELECT COUNT(*) INTO d_count
		FROM instructor
		WHERE instructor.dept_name = dept_count_proc.dept_name
	END

WHILE <boolean exp> DO
	...
END WHILE

REPEAT
	...
UNTIL <boolean exp>
END REPEAT

DECLARE n INTEGER DEFAULT 0;
FOR r AS
	SELECT budget FROM department
	WHERE dept_name = 'Music'
DO
	SET n = n - r.budget
END FOR

IF <bool exp>
	THEN ...
ELSE IF <bool exp>
	THEN ...
ELSE ...
END IF

CREATE TRIGGER timeslot_check1 AFTER INSERT ON section
	REFERENCING NEW ROW nrow
	FOR EACH ROW
	WHEN (nrow.time_slot_id NOT IN (
		SELECT time_slot_id
		FROM time_slot))
	BEGIN
		ROLLBACK
	END;
```

### Advanced Aggregation

```sql
SELECT ID, RANK() OVER (ORDER BY (GPA) DESC) AS s_rank
```

# Database Design

## E-R

![[IMG-DB Cheatsheet-20250613192309849.webp|599x418]]

- ! 还是要参考笔记 [[DB 06 Database Design using the E-R Model]]
- 概念
	- entity
	- entity set
	- relationship
	- relationship set
	- relationship instance
	- role
	- attr
		- domain
		- simple / composite
			- composite 加缩进
		- single-valued / multivalued
			- multivalued 用花括号括起来
		- derived 加括号，例如 `age()`
	- mapping cardinality
		- one-to-one
		- ...
		- 箭头指向的是 one
		- 数字表示近的一侧
	- weak entity set
		- e.g. sec_course 例子
			- section 中有 `sec_id` 节次号，`semester` 学期和 `year` 年份，但是不同课程可能有完全相同的这些属性，所以又需要 `course_id`，除此之外也需要 sec_course 形成和 course 的联系，这是所有属性构成了主键
			- 但这样就出现了冗余，因为 section 中已经有 `course_id`，那么 sec_course 的联系就多余了，但是我们不希望联系隐含在关系的一个 attr 中
			- 所以，删除 `course_id` 属性，此时 section 中剩余属性不足以构成主键，所以需要依附于 identifying/owner entity set course
			- 总结来说，一个独立的 section 的存在依附于 course
- 转换为关系模式
	- 简单强实体集合直接用
	- 复杂属性强实体集合，composite 展开，derived 删除，multivalued 多开一张表
		- e.g. `instructor_phone(ID, phone)` ，其中两个都是主键
	- 弱实体集，加上标识集合的主键，所有属性都是主键
	- 联系集合
		- 一对一，多对一，一对多，在 many 的一遍增加一个属性
		- 多对多，需要新开表，存双方主键，所有属性都是主键
- 扩展的 E-R 属性
	- specialization and generalization
		- specialization: 继承/不继承
		- generalization 都是 total participation 的，低层实体一定是

## Normalization

- Lossless decomposition
	- 判断的唯一标准就是 $r=r_1\bowtie r_2$
	- 如果满足 $F^+$ 中存在 $R_1\cap R_2\rightarrow R_1$ 或者 $R_1\cap R_2\rightarrow R_2$，也满足无损分解条件，也就是说**交集中含有其中一方的 superkey**
- 1NF，所有 attr 都是原子的
	- 多值、复合都不是原子的
- functional dependency
	- $\alpha\rightarrow\beta$ 等价于 $\forall t_1, t_2 \in r$ 如果 $t_1[\alpha]=t_2[\alpha]$，那么 $t_1[\beta]=t_2[\beta]$
	- 若 $K\rightarrow R$ 在 $r(R)$ 上成立，则 $K$ 是一个 superkey
	- trivial 的函数依赖，即 $\beta \subseteq \alpha$
	- $F^+$ 闭包，能从 $F$ 推导出的所有的函数依赖集合
- dependency preservation

### Functional Dependency Theory

- 计算 $F^+$，重复使用 **Armstrong's Axioms**, these rules are **sound**(正确有效的) and **complete**(完备的)
	- reflexive rule (自反): if $\beta\subseteq\alpha$, then $\alpha\rightarrow\beta$
	- augmentation rule (增补): if $\alpha\rightarrow\beta$, then $\gamma\alpha\rightarrow\gamma\beta$
	- transitivity rule (传递): if $\alpha\rightarrow\beta$ and $\beta\rightarrow\gamma$, then $\alpha\rightarrow\gamma$
	- **additional rules**
		- union rule (合并): if $\alpha\rightarrow\beta$ and $\alpha\rightarrow\gamma$, then $\alpha\rightarrow\beta\gamma$
		- decomposition rule (分解): if $\alpha\rightarrow\beta\gamma$, then $\alpha\rightarrow\beta$ and $\alpha\rightarrow\gamma$
		- pseudotransitivity rule (伪传递): if $\alpha\rightarrow\beta$ and $\gamma\beta\rightarrow\delta$, then $\alpha\gamma\rightarrow\delta$
- 计算 $\alpha^+$ 比较简单，而且只需要用 $F$ 就能得到正确的答案
	- 可以用来证明 superkey
	- 然后减少任意一个元素，都得不到 $R$，证明 candidate key
- 计算 $F_c$
	- extraneous attr
		- 定义：删除后不改变 $F^+$，或删除后得到的 $F'$ 能够由 $F$ 推导出
		- 意义：让依赖两侧的属性集合尽量小
		- 验证方法，删除后在 $F'$ 中检查：
			- 左侧删除 $A$，检查 $\beta \subset(\alpha-\{A\})^+$
			- 右侧删除 $A$，检查 $A\in\alpha^+$
	- 性质：
		- $F_c$ 中任何函数依赖都不含无关属性
		- $F_c$ 中依赖的左半部分都是唯一的
	- **正则覆盖未必是唯一的**

### 根据依赖求候选键

- 首先找到只在**依赖左侧**出现的属性，作为核心属性集 $L$
- 计算 $L^+$，如果 $L^+=R$，则 $L$ 是候选键，否则考虑从 $R-L^+$ 中添加属性

### dependency preserving

- **限定**：将 $R$ 分解为 $R_1, R_2,\dots,R_n$，其中 $F$ 在 $R_i$ 上的限定是 $F^+$ 中只包含 $R_i$ 中属性的子集 $F_i$
	- **注意这里用的是 $F^+$
- 验证依赖保持的方法
	- 如果 $(F_1\cup F_2\cup\dots\cup F_n)^+=F^+$，那么这个分解是依赖保持的，但是指数时间
	- 或者，对于 $F$ 中的每个 $\alpha$，依次在每个 $R_i$ 上并上闭包，如果都满足 $\beta \subseteq result$，则也是依赖保持的，多项式时间
		- ![[IMG-DB Cheatsheet-20250611152126805.webp|507]]
- 需要注意 $B\rightarrow CD$ 这种，分成 $(B,C,D)$ 可以，分成 $(B,C),(B,D)$ 也可以

### BCNF

- 具有 $F$ 的关系模式 $R$ 属于 BCNF 的条件是，对于 $F^+$ 中所有形如 $\alpha\rightarrow\beta$ 的函数依赖，以下至少一项成立
	- $\alpha\rightarrow\beta$ 是平凡的
	- $\alpha$ 是 $R$ 的一个 superkey
- 分解算法
	- $R$ 分解为 $\alpha \cup \beta$ 和 $R-(\beta-\alpha)$
	- 即将 alpha 和能够确认的部分拿出来，然后在原关系中删除 alpha 能够确认的部分
- **保证无损分解，但不能保证依赖保持**

### 3NF

- 具有 $F$ 的关系模式 $R$ 属于 BCNF 的条件是，对于 $F^+$ 中所有形如 $\alpha\rightarrow\beta$ 的函数依赖，以下至少一项成立
	- $\alpha\rightarrow\beta$ 是平凡的
	- $\alpha$ 是 $R$ 的一个 superkey
	- $\beta-\alpha$ 中的每个属性 $A$ 都在 $R$ 的一个 candidate key 中 *放宽*
- 任何 BCNF 一定满足 3NF，反之不然

![[IMG-DB Cheatsheet-20250611152551565.webp|525]]

- 分解算法
	- **计算正则覆盖** $F_c$
	- 直接把所有 $\alpha\rightarrow\beta$ 做成表 $\alpha\beta$
	- 如果所有新表中都没有 $R$ 的一个 candidate key，则添加一个表保存 candidate key
	- （可选）删除被包含的冗余关系（如果使用 $F$ 来分解，必然有很多这种情况）
- 3NF 能够**确保无损分解和依赖保持**，但是**存在信息冗余**

### 4NF

- 多值情况下，满足 BCNF 不一定就没有冗余

> [!note] Definition 1
> $\alpha\rightarrow\rightarrow\beta$ 表示 $\alpha$ 多值确定了 $\beta$，if 存在 $t_1[\alpha]=t_2[\alpha]$ 且存在 $t_3, t_4$ 使得：
>
> - $t_1,t_2,t_3,t_4$ 的 $\alpha$ 相等
> - $t_1,t_3$ 和 $t_2,t_4$ 的 $\beta$ 相等
> - $t_1,t_4$ 和 $t_2,t_3$ 的 $R-\alpha-\beta$ 相等
> - 或者说，$\beta$ 和 $R-\alpha-\beta$ 是独立的

> [!note] Definition 2
> 或者将 $R$ 分解为非空的三个集合 $Y,Z,W$，如果 $<y_1,z_1,w_1>\in R \land <y_1,z_2,w_2>\in R\Rightarrow <y_1,z_1,w_2>\in R \land <y_1,z_2,w_1>\in R$，那么 $Y\rightarrow\rightarrow Z, Y\rightarrow\rightarrow W$

- FD 是 MVD 的特殊情况，if $\alpha\rightarrow\beta$, then $\alpha\rightarrow\rightarrow\beta$
- MVD 集合 $D$，闭包为 $D^+$

> [!note] Definition
> $R$ is in 4NF, if $\forall \alpha\rightarrow\rightarrow\beta \in D^+$:
>
> - $\alpha\rightarrow\rightarrow\beta$ is trivial
> - $\alpha$ is a superkey for $R$

- if R in 4NF, then R in BCNF *4NF 更加严格*

![[IMG-DB Cheatsheet-20250611153840281.webp|533]]

- 基本和 BCNF 一样
- 无损分解判定
	- $R_1\cap R_2\rightarrow\rightarrow R_1\in D^+$ or
	- $R_1\cap R_2\rightarrow\rightarrow R_1\in D^+$

# Storage & Indexing

## Storage & Storage Structure

- 多层 memory
	- primary memory 主存储器 cache mem
	- secondary memory 硬盘、固态硬盘 disk ssd flash
	- tertiary memory 磁带、光盘 tape cd dvd
- 磁盘
	- ![[IMG-DB Cheatsheet-20250611211652084.webp|533x442]]
		- 磁盘臂组件，磁盘臂，读写头，主轴，盘片，磁道，扇区
		- 所有第 i 条磁道构成第 i 个柱面
	- 性能评价指标
		- access time: 发出读写请求到数据开始输出的时间
			- average seek time: 寻道时间的平均值
			- rotational latency time: 旋转到对应的扇区的时间
		- data-transfer rate: 数据传输率
		- MTTF: 1200 000 小时的磁盘（比较新的） 1000 张，平均 每 1200 小时坏一张
	- 性能优化
		- 顺序访问，只需要一次寻道
		- buffering
		- read-ahead
		- scheduling 磁盘臂调度 elevator algorithm
		- file organization 尽量一个文件连续放一起
		- nonvolatile write buffer
		- log disk，其所有访问都是顺序的，其文件系统称为日志文件系统
- 其他 memory
	- NOR flash 存储单元并行排列，和 RAM 一样支持随机访问，可以直接读取任何字节
	- NAND flash 存储单元串行排列，主要支持顺序访问，必须先擦除整个块才能写入新数据，寿命也更低
- record storage
	- fixed length
		- 可以直接计算偏移量
		- 用 free list 管理空的 slot，头文件维护 free list
	- var length
		- 出现的场景
			- 多种记录类型同文件存储
			- 变长度字段，重复字段
		- | fixed length part | null bitmap | var len part |
		- null bitmap 需要字节对齐
		- slotted page structure
			- block header 维护 entry 数量和 entry 表，包含指向 entry 的指针
			- records 和 header 向中间生长
- file forganization
	- heap file organization 一条记录可以放在文件的任何地方
	- sequential file organization 根据 search key 顺序存储
		- ![[IMG-DB Cheatsheet-20250611213630112.webp|533x412]]
		- 插入的时候，可能需要用指针，一段时间后需要文件重组
	- hashing file organization 打散到多个 bucket
		- close addressing: bucket 块满了要有溢出 bucket 块链表
		- open addressing: bucket 块满了可以放入下一个块 (linear probing)
	- multitable cluster，多表单文件，减少 io
	- table partition
	- data dictionary storage 就是元数据的存储
- buffer pool
	- buffer control workflow 当程序发出一个 page / block 请求后会发生什么
		- hit / miss, replace
	- buffer algorithm: LRU, MRU
	- forced output 替换之外的强制写出
- columnar representation
	- 利于数据分析，列统计

## Indexing

- 索引 search key
- 评价指标
	- access type
		- point query
		- range query
	- access time
	- insertion time
	- deletion time
	- space overhead
- ordered indices
	- primary / clustering
	- secondary / nonclustering
	- dense
	- sparse
		- 只能是 primary index，或者是 secondary index 的二级索引
		- 如果被删除了，如果下一个 tuple 的 search key 不在 index 中，用下一个 tuple 的 search key 替换
	- multilevel
- bptree index
	- 中间 $\lceil n/2\rceil$ 叶子 $\lceil (n-1)/2\rceil$
	- 计算一定 fan-out 的树的最大最小容量**例子**
	- 分裂时，前 $\lceil n/2\rceil$ 放在左边
	- 删除时，如果当前叶节点不满足约束，能合并则合并，否则移项
	- B+ 树 leaf 的 record 指针的位置可能发生改变，此时 B+ 树的二级索引（指向 leaf record ptr 的 ptr 索引）也需要更新
	- bulk loading: 一次插入很多项，插入前排序，则能够顺序访问叶子，每个叶子只需要一次 io
	- b tree 非叶子节点需要两倍的指针，孩子指针 + record 指针
	- 多 key 索引的失效
	- covering index，储存部分属性值，而不只是 record ptr
- bitmap index
	- 例如 male 11010 female 00101
	- 可以使用位运算加速
- hash index
	- 普通的不讲了
	- 动态散列
		- 例如散列结果是 uint32，可以将最后几位数字作为 index
		- 这样方便改变索引大小，而且没有更改 hash function，所以还是一样查询
		- 性能不随文件的增长而降低
- write-optimized index
	- Log-structured merge tree
		- 结构
			- L0 in memory B+
			- 其他在 disk 中
		- 策略
			- L0 满了就**直接移动**到磁盘中作为 L1
			- 磁盘中每一层，低层传过来的树进行 merge，如果树的大小超过一定级别，放入新的级别
			- lazy delete，插入删除 entry，当 merge 时才进行物理删除
		- 效果
			- 优点：insert 是顺序 io，（叶子满）没有空间浪费，减少了每次插入的 io
			- 缺点：query 需要搜索很多树，需要复制很多次
		- 变体 stepped-merge：每一层可以有 k 个树，然后再 merge 放入下一层
			- 减少了写开销，但是查询开销更大了
	- Buffer Tree
		- 每一个 internal node 都有一个 buffer 来暂存插入
		- buffer 满且还有插入时，下推到孩子的 buffer，递归
		- 优点
			- 查询开销更少了
			- 任何 tree-based index 都能用这种策略
		- 缺点：与 LSM 相比，进行插入时涉及下推给多个孩子，更多的 random io
	- 总结：
		- LSM 专门做==写入==顺序化，但是查询效率比较低
		- buffer tree 减少 B+ 树就地更新的随机 io，但是仍有随机性

# Query

![[IMG-DB Cheatsheet-20250613080914056.webp|700x406]]

## Query Processing

- 评价指标：传输时间和访问时间
- 优化器的目标：并不总是尽可能缩短响应时间，而是尽可能降低查询计划总的资源消耗（e.g. 还有其他查询正在进行）

### Selection

- A1 Linear search
	- $t_S+b_rt_T$
- A1 Linear search, equality on key
	- $t_S+(b_r/2)t_T$
- A2 B+ primary index, equality on key
	- $(h+1)(t_S+t_T)$
- A3 B+ primary index, equality on non-kyey
	- $h(t_S+t_T)+t_S+bt_T$
- A4 B+ secondary index, equality on key
	- $(h+1)(t_T+t_S)$
- A4 B+ secondary index, equality on non-key
	- $(h+n)(t_T+t_S)$
	- 其中 n 是 matching record 数量
- A5 B+ primary index, comparison
	- $h(t_S+t_T)+t_S+bt_T$
- A6 B+ secondary index, comparison
	- $(h+n)(t_S+t_T)$
	- linear scan may be cheaper
- A7 conjunctive selection using one index
	- 选择一个 $\theta_i$ 组合，使用 A1-A7，使得这次查询操作代价最小，将符合的都读入 memory
	- 然后进行其他条件的验证
- A8 conjunctive selection using composite index
	- 尽量使用合适的多值索引
- A9 conjunctive selection by intersection of identifiers
	- 先尽量使用索引得到所有条件的 matching records 指针
	- 然后取交集
- A10 disjunctive selection by union of identifiers
	- ==仅在所有条件都有可用索引的时候适用==，否则 linear scan 更好
	- 查到 ptr 之后取并集
- A? negation
	- 如果满足条件的非常多，使用 linear scan
	- 如果满足条件的非常少，使用 index
- bitmap index scan
	- 每一页一个 bit 表示
	- 将 secondary index scan 的取页性能尽可能逼近 linear scan，没有非常差的性能
	- 用 index 找到 matching record ptr，将指向的页置为 1
	- 只取 bitmap 中 1 的页

### Sorting

- algorithm
	- 创建 $N$ 个大小为 $M$ 的 run，$N=\lceil b_r/M\rceil$
	- 进行 $\min(N, M)$ way merge
		- 如果 $N<M$，可以只用 merge 一次
		- 否则，考虑缓冲区大小为 $b_b$，则 merge $\lceil\log_{\lfloor M/b_b\rfloor -1} b_r/M\rceil$ 轮
- cost
	- seek
		- 初始归并段 $2\lceil b_r/M\rceil$
		- merge $\lceil b_r/b_b\rceil(2\lceil\log_{\lfloor M/b_b\rfloor -1} b_r/M\rceil-1)$
			- 每一轮寻道 2 次，除了最后一轮不需要写回
		- 总计 $2\lceil b_r/M\rceil+\lceil b_r/b_b\rceil(2\lceil\log_{\lfloor M/b_b\rfloor -1} b_r/M\rceil-1)$
	- transfer
		- $b_r(2\lceil\log_{\lfloor M/b_b\rfloor -1} b_r/M\rceil+1)$
		- 初始 2，最后 -1，所以 +1

### Join

$r\bowtie_\theta s$

#### Nested-loop Join

- best case: 内存完全装下
	- $2$ seeks
	- $b_r+b_s$ transfers
- worst case: 只有两个 buffer block 可以用来放两个关系
	- $b_r+n_r$ seeks
	- $b_r+n_rb_s$ transfers
- 总结：如果小的关系能完全放入内存，将其作为内关系

#### Block Nested-loop Join

- best case
	- $2$ seeks
	- $b_r+b_s$ transfers
- worst case: 只能放 2 个 block
	- $b_r+b_s$ seeks
	- $b_r+b_rb_s$ transfers
- cost: 假设有 $M-1$ 个块可以使用，用 $M-2$ 个来存放外关系，外循环次数 $\lceil b_r/(M-2)\rceil$
	- $2\lceil b_r/(M-2)\rceil$ seeks
	- $\lceil b_r/(M-2)\rceil b_s+b_r$ transfers
- 总结：外关系尽量小有好处

#### Indexed Nested-loop Join

- 适用场景：如果是 equi-join 或 natural join，且内关系的 join attr 上有 index
- 对于每一个 outer 中的 tuple 都用 index 查 inner 中对应的元组
- cost
	- $b_r+n_rc_S$ seeks，其中 $c_S$ 是内部元组使用 index 的寻道次数
	- $b_r+n_rc_T$ transfers，其中 $c_T$ 是内部元组 index 的块传输次数
	- 总共 $b_r(t_T+t_S)+n_rc$
- 总结：如果两个关系都有对用的索引，使用元组较少的作为外关系

#### Merge-Join

- 只能用于 equi-join 和 natrual join
- algo
	- 将两张表按照 join attr 排序（这里假设已经排序好了）
	- 双指针法，找到满足等值条件的 tuple
- cost，假设缓冲区大小为 $b_b$
	- $\lceil b_r/b_b\rceil+\lceil b_s/b_b\rceil$ seeks
	- $b_r+b_s$ transfers
- hybrid merge join
	- 一个关系按照 join attr 排序好了，另一个有 secondary index，也可以用

#### Hash Join

- algo
	- partition s using hash func h, memory 中有 output buffer
	- partition r similarly
	- for i in range(0, $n_h$)
		- 加载 $s_i$ 到内存，**使用另一个 hash func 建立内存中的索引**
		- 一个一个读 $r_i$，用 hash 找 matching tuple，输出连接
	- s 称为 build input，r 称为 probe input
- 基本原则
	- $n=\lceil b_s/M\rceil * f$，保证每个 s 的划分都能放入内存，给 20% 左右的冗余，即 $f=1.2$
		- ! 如果分配 M-1 个够的话，就分配 M-1 个，一般性能更好
	- r 的划分不需要能够放入内存
	- 如果 $n\geq M$，一次划分就没有足够的缓冲区数量，需要递归划分
		- 递归划分，每次最多能将一个划分为 $M-1$ 个，所以需要划分 $\lceil \log_{M-1} n\rceil=\lceil \log_{M-1}b_s/M\rceil$ 次，这里直接假设划分完全均匀
	- 解决 overflow 问题，即划分的过程中发现一个 bucket 实际上超过了内存大小（skew hash），可以递归一次
- cost
	- 不递归
		- $2(\lceil b_r/b_b\rceil+\lceil b_s/b_b\rceil)+2n_h$ seeks，忽略了最后阶段的少量 seek
		- $3(b_r+b_s)+4n_h$ transfers，考虑了可能存在的一张表划分之后多了 $n_h$ 个 block 的问题，两张表，且写入再读出
	- 递归
		- $2(\lceil b_r/b_b\rceil+\lceil b_s/b_b\rceil)\lceil \log_{\lfloor M/b_b\rfloor-1}b_s/M\rceil$ seeks
		- $2(b_r+ b_s)\lceil \log_{\lfloor M/b_b\rfloor-1}b_s/M\rceil+b_r+b_s$
	- 如果整个 s 能被放入主存，直接构建 in-mem index，然后遍历 r 来 probe
		- $2$ seeks
		- $b_r+b_s$ transfers
- hybrid hash join
	- 当内存较大，但 s 仍然大于内存时，可以在内存中保留 s 的第一个分区，给 r 分块时直接进行探测
	- 当 $M>>\sqrt{b_s}$ 时比较有用

#### Complex Joins

- 交集选择
	- 使用 block nested loop
	- 或者先计算 $r\bowtie_{\theta_i} s$，然后不断筛选其他条件
- 并集选择
	- 使用 block nested loop
	- 或者分别计算所有的 $r\bowtie_{\theta_i}s$，然后求交集

### Other Operations

- duplicate elimination
	- 排序去重、hash 去重
- projection
	- 广义投影操作很容易出现重复，需要去重
- set operations
	- 对于排好序的集合，可以直接 O(N) 扫描
	- 如果没有排好序，可以用 hash 实现
- outer join

### Evaluation of Expressions

- 物化 or 流水线
- 物化
	- 存储中间结果
	- double buffering：两个 output buffer，当一个满了就写，另一个继续工作
- 流水线
	- 需求驱动
		- 迭代器，open next close
	- 生产者驱动
		- 底层持续输出，直到缓冲区满，等待上级处理
- blocking operations: 在所有 input 都处理之前无法生成 outpu，例如 aggr sorting

## Query Optimization

### 等价规则

> [!note]- Note
>
> ![[IMG-DB Cheatsheet-20250613101957245.webp|700x361]]
>
> ![[IMG-DB Cheatsheet-20250613102003653.webp|700x360]]
>
> ![[IMG-DB Cheatsheet-20250613102048680.webp|700x279]]
>
> ![[IMG-DB Cheatsheet-20250613102146043.webp|700x357]]
>
> ![[IMG-DB Cheatsheet-20250613102300110.webp|700x525]]
>
> ![[IMG-DB Cheatsheet-20250613102405890.webp|700x518]]
>
> ![[IMG-DB Cheatsheet-20250613102534314.webp|700x411]]

- 启发式优化方法
	- 先进行选择，且要考虑选择条件分别作用在哪张表上
	- 先进行投影
	- join 顺序
		- 确保先 join 的结果不要太大
		- e.g. (instructor from music dept **join** teaches) **join** courses
	- eval 优化
		- 公共子表达式，动态规划

### 成本估计

- 符号表示
	- $l_r$ 一个元组的字节大小
	- $f_r$ blocking factor，一个 block 能够存储的元组数量
	- $V(A,r)$ 出现在 $r$ 中属性 $A$ 的唯一值的数量，大小和 $\Pi_A(r)$ 一致
- 直方图
	- 等宽 1-3 4-6
	- 等深 1-5 6-8... 找到每一个大小相似的小部分的上下界
		- 更好的估计
		- 更少的空间占用
		- 更推荐使用
	- 如果没有直方图，优化器就假设是均匀分布的

#### Select Size

- $A=a$
	- 假设均匀分布 $n_r/V(A,r)$
	- 有直方图，$n_r$ 用所在范围内的元组数量统计，$V$ 用所在范围内的元组唯一值统计
- $A\leq a$
	- 0 如果 $a<\min(A,r)$
	- $n_r$ 如果 $a\geq \max(A,r)$
	- $n_r\frac{a-\min}{\max-\min}$
- 复杂选择
	- conjunctive: 假设条件独立 $n_r\frac{s_1s_2\dots s_n}{n_r^n}$
	- disjunctive: $n_r[1-(1-\frac{s_1}{n_r})\dots (1-\frac{s_n}{n_r})]$
	- 否定 $n_r-s$

#### Join Size

- natural join
	- $R\cap S=\emptyset$，就是笛卡尔积，有 $n_rn_s$ 个元组，每个占用 $l_r+l_s$ 字节
	- $R\cap S=R$，每个 s 最多连接一个 r 元组，所以不超过 $n_s$
	- $R\cap S$ 是 $S$ 中引用 $R$ 的外键，那么 $n_s$
	- 交集不完全包括一个 schema 时
		- $\min(\frac{n_rn_s}{V(A,r)},\frac{n_rn_s}{V(A,s)})$
- theta join
	- 按照笛卡尔积 + selection 计算

#### Other Operations

![[IMG-DB Cheatsheet-20250613105713837.webp|700x776]]

#### Heuristics

- join 排序最优解
	- dp time $O(n^3)$ space $O(2^n)$
- 左深连接树
	- time $O(n!)$ space $O(2^n)$
	- 如果动态规划则是 time $O(n2^n)$ space $O(2^n)$

# Transactions

## Transactions

![[IMG-DB Cheatsheet-20250613115631529.webp|500]]

- ACID
	- Atomicity: 一个事务的所有操作要么全都成功，要么全都失败
	- Consistency: 事务的隔离执行保证了数据库的一致性
	- Isolation: 事务并发时，事务将不会观察到其他事务对数据库的操作或不一致状态
	- Durability: 事务执行完后，数据库状态应该持久化，即使遇到 system failure
- 并发问题
	- 丢失修改：例如两个事务同时进行 -1 操作，读的一样，先后写回，只减了一次
	- 读脏数据：A 读取了 B 在 rollback 前的修改后的数据
	- 不可重复读：由于 B 的操作，A 在事务执行期间两次读同一个数据结果不一样
	- 幽灵问题 Phantom Problem：由于 B 的 insert 操作，A 进行两次查询的结果不一致
- 可串行化
	- 冲突可串行
		- 冲突的定义，例如同一位置的 r-w w-r w-w 是冲突
		- 通过互换不冲突操作的顺序，实现完全串行
		- 前驱图：$T_i\rightarrow T_j$ ，如果 Ti 和 Tj 冲突，且冲突操作 Ti 在 Tj 之前完成
			- e.g. T1 read(A); T2 write(A); T1 write(A); 有两个冲突，对应 T1->T2 且 T2->T1，形成环
			- 可以遍历数据项，每个数据项分析前驱关系，在图中添加边
			- 每个数据项分析时，实际上需要考虑所有操作的两两组合，例如
				- r1(A) w2(A) w1(A) r3(A)，考虑 C42
			- ==冲突可串行化等价于图中没有环==
	- 视图可串行
		- view equivalent on schedule A, B
			- A 读 initial Q 的事务在 B 中也读 initial Q
			- A 中 Ti 在 Tj 修改后读 Q，B 中也要如此
			- A 中最后写 Q 的事务在 B 中也最后写 Q
		- ==所有 view serializable 但是不 conflict serivalizable 的事务，都一定有 blink writes==
			- blind write 指的是没有读 Q 就写 Q
		- ==视图可串行的验证是 NP-C 的==，大部分算法只检查一些充分条件，如果满足还能使用
	- ==和串行调度结果一致的调度，不一定满足冲突/视图，需要考虑除了 read/write 的其他操作==
- 可恢复调度
	- ==如果 Tj 读了 Ti 写的数据，那么 Ti 就一定要先于 Tj 提交，才能保证可以恢复== **写先提交**
	- e.g. ![[IMG-DB Cheatsheet-20250613114513879.webp|400]]
		- 如果 T8 rollback，T9 就已经访问了数据库的不一致状态，由于 T9 已经提交，这种不一致无法恢复
- Cascading Rollbacks
	- 一个事务 abort 会导致一系列事务 rollback
	- e.g. ![[IMG-DB Cheatsheet-20250613114907352.webp|400]]
		- 如果 T10 失败了，那么 T11, T12 也要回滚
	- **Cascadeless Schedules**: 不会产生级联回滚
		- ==对于每个 Ti Tj，如果 Tj 读了 Ti 写的数据，那么 Ti 应该在 Tj 读之前提交== **读前提交** *比可恢复更加严格*
- SQL Isolation Level
	- serializable: 可串行化
	- repeatable read: 可重复读，仅读取已经提交的数据，且事务两次读取的结果一致
	- read committed: 只能读取已经提交的数据
	- read uncommitted: 允许读取未提交的数据
	- 所有等级都不允许 dirty write，即向李刚一个还没结束的事务写入的数据项进行操作 *需要锁*

![[IMG-DB Cheatsheet-20250613115353162.webp|700x367]]

## Concurrency Control

###  Lock-Based Protocol

- 锁兼容矩阵 ![[IMG-DB Cheatsheet-20250613115935436.webp|300]]
- deadlock
	- e.g.![[IMG-DB Cheatsheet-20250613120110022.webp|200]]
		- 事务 A 申请了锁 a
		- 事务 B 申请了锁 b，然后申请 a，不成功，于是阻塞，等待 A 释放 a
		- 然而 A 的下一步操作不是释放 a，而是继续申请 b，于是相互等待
	- starvation: 某个事务的锁申请一直没有被授予（竞争失败）

#### 2PL

- vallina 2pl
	- growing phase，事务只可以申请锁，或升级锁
	- shrinking phase，事务只可以释放锁，或降级锁
	- lock point：事务得到最后一个锁的时间，但不一定是事务开始进行数据处理的时间点
		- 可以按照 lock point 顺序得到冲突可串行调度
	- 效果
		- ==能够确保 conflict serializable，但不是所有 conflict serializable 调度都满足 2pl==
			- 即 2pl -> conflict serializable，但不能反推
		- ==但是无法确保不发生死锁，无法确保无级联调度或可恢复调度==
- strict 2pl: 所有事务只能在 commit/abort 之后释放其 X lock
	- ==能够保证可恢复调度、无级联调度==
- rigorous 2pl: 所有事务都只能在 commit/abort 之后释放锁
	- ==plus. 能够按照提交顺序得到串行调度==
	- 大多数数据库都用

#### Lock Manager

![[IMG-DB Cheatsheet-20250613121646186.webp|300]]

- 在内存中维护一个锁表
	- 是一个 hash 表，管理数据项
	- 每个数据项节点都有一个锁申请队列

#### Graph-Based Protocol

- 强制偏序关系：$d_i\rightarrow d_j$，那么同时访问两个数据的事务应当先访问 di 然后访问 dj
	- 这样，数据集合 D 可以称为一张有向无环图，称为 **database graph**
- tree protocol
	- ==只允许申请 X lock==
	- Ti 第一个锁可以申请任何节点；其他时候，Ti 申请的锁，要求其父节点也已经被 Ti 申请到锁
	- 锁可以在任何时间释放
	- 一个数据项只能被加锁一次
		- 也就是 Ti 加锁然后释放的数据项，不能再被加锁
	- 效果
		- ==conflict serializable，没有死锁==
		- 解锁可以比 2pl 更早发生（可以在任意时间解锁）
			- 更少的等待时间，更高的并发性
			- 不会死锁，不会因为死锁 rollback
	- 缺点
		- 无法确保可恢复或无级联
			- 需要引入 commit dependencies 来确保可恢复
		- 事务可能需要 lock 一些没用到的数据项
			- 提高了锁 overhead，增加等待时间，减少并发度
- tree protocol 和 2pl 有交集，但差集均不为空
	- 2pl 不可能出现的调度可能在 tree 中出现，反之亦然

### Deadlock Handling

- 基础策略
	- pre-declaration: 要求所有事务在开始执行前先获取所有锁
	- graph-based protocol 强制引入偏序关系
- 其他策略
	- wait-die (non-preemptive 非抢占) older 等待 younger 释放锁，younger 不等待 older，rollback
	- wound-wait (preemptive 抢占)
		- older 强制 younger rollback，而不是等待
		- younger 可能会等待 older
		- rollback 次数比 wait-die 要少
	- ! 上面两种 rollback 之后新事务的时间戳仍然用原来的，保证其会变成 older，避免饥饿
- timeout-based
	- 一个事务等待的时间有限制，超出这个时间则 rollback，能够确保死锁在 timeout 的时间内解决
	- 效果
		- 实现比较简单
		- 但是可能在没有死锁发生时也进行 rollback
		- starvation 仍然可能出现
- detection
	- wait-for graph: Ti->Tj 如果 Ti 正在等待 Tj 释放锁，有环时死锁
	- 死锁恢复策略
		- victim: rollback 后能解决死锁的事务中选出的，开销最小的一个
		- total rollback: 将这个事务完全 rollback
		- partial rollback: 只 rollback 到需要的位置

### Multiple Granularity

- fine / coarse
- database - area - file - record
- intention lock modes: 在较低的节点加锁时，往较高的节点放置一个意向锁，减少较高节点申请锁时的检查，表示这里有/将要有一个锁
	- intention-shared (IS) 表示在树的较低级别有显式锁定，有节点加上了 s lock
	- intention-exclusive (IX) 表示在数的较低级别有显式锁定，可以是 x / s lock
	- shared and intention-exclusive (SIX) 复合锁，表示当前节点显式锁定 s lock，且较低级别存在 x lock
	- ![[IMG-DB Cheatsheet-20250613133852406.webp|400]]
- 规则：当 T 希望给节点 Q 加锁时
	- T 先前没有解锁过时，T 才能对节点加锁
	- T 必须先对树的根节点加锁
	- 仅当 T 给 Q 的父亲加上 xx 锁时，T 才能给 Q 加上 xx 锁
		- IX IS -> S IS
		- IX SIX - > X SIX IX
	- T 没有对 Q 的任何孩子加锁时，才可以解锁 Q
- 总结
	- 加锁 top-down，解锁 bottom-up
	- ==无法保证不发生死锁==

![[IMG-DB Cheatsheet-20250613134655274.webp|700x717]]

### Insert / Delete

- locking
	- 删除前必须有 x lock
	- 插入后自动获得 x lock
- phantom phenomenon
	- 一个解决方案：加入一个 data item 表示整张表
		- scan 需要 s lock
		- insert delete 需要 x lock
		- 但是 low concurrency
	- indexing locking protocol ==能够保证 phantom 不会发生，并发度受限==
		- 每张表都至少有一个 index
		- 仅当通过表上的一个或多个 index 找到 tuple 时，Ti 才能访问这些元组
		- 索引协议中，表的扫描被视为叶子的扫描
		- 执行查找事务的 Ti 必须对要访问的索引叶子节点加上共享锁，即使访问到的叶子节点中并没有符合要求的 tuple
		- 一个进行插入、删除、更新的事务，必须对所有有影响的 leaf 节点加锁
		- 遵循 2pl
	- next key locking protocol ==提供更高的并发度==
		- 在 index lookup 中，锁定所有满足条件的 value
		- 而且也锁定 index 中的下一个 key value
		- 查找用 s lock，插入更新删除用 x lock
- 同时更新不可串行例子 ![[IMG-DB Cheatsheet-20250613135042431.webp|400]]

## Recovery

- Log
	- 存储在稳定存储器上，通过多备份确保不会损坏
	- log 先写原则
	- 当 commit log 写入稳定存储器时，txn 才算 commit，而事务的更新仍然可能在 buffer 中
- undo
	- undo 时写 compensation log
	- undo 结束 abort
- redo 不用写 log

### Vallina Algorithm

- ckpt
	- 将所有 log record 持久化
	- 将所有脏页持久化
	- 写 ckpt，包括 ATT
	- 其他事务都停止，阻塞式检查点
- rollback
	- backwards 扫描
	- undo writing，写补偿日志
	- 遇到 start 写 abort
- recovery from failure
	- redo scan forward, 更新 undo-list
	- undo scan backwards，进行 undo，写补偿 log，直到 empty

### Buffer Management

- log buffer 在一个 block 满/log force 永久化时永久化
- 在 commit 被输出到 stable storage 时，T 才算 commit
- 当主存中部分数据块输出时，确保这个数据块相关的 log 已经永久化 write-ahead logging WAL
- 对于 database 管理数据块的方法
	- no-force policy: commit 的时候数据块不用永久化
	- steal policy: 还没 commit 的时候也可能持久化
	- 持久化过程中加上 latch (x lock on block)，不允许修改
- ==output a block==
	- 申请 block 的 latch
	- log flush
	- output block
	- release latch

### Fuzzy Ckpt

- 过程
	- 暂时停止所有事务的更新
	- 插入 ckpt L 并强制 log 永久化
	- 记录 buffer pool 中的 modified blocks 到 list M
	- 允许事务继续执行
	- 输出 M 中的所有脏页
		- WAL + 输出时不更新
	- 在 disk 上保存一个 ptr，指向 ckpt record
- 效果
	- ==能够 handle incomplete ckpt，即数据库在 ckpt 时 crase==
	- 能提升并发度

### Early Lock Release and Operation Logging

- logical undo logging
	- 类似 bptree 插入和删除的操作无法物理 undo，只能逻辑 undo
- operation logging
	- `<Ti, Oi, operation-begin>  ...  <Ti, Oi, operation-end, U>`
	- 其中的 U 是整个 operation 的逻辑操作，例如 `delete I9, K5, RID7`
	- rollback 流程：backwards
		- 如果遇到普通 log，进行物理 undo，写补偿日志
		- 如果遇到 `<Ti, Oj, operation-end, U>`
			- 使用 undo info in U 进行逻辑 undo
			- 此时也要正常记录 operation log，但在结尾用 `<Ti, Oj, operation-abort>` 而不是 operation-end
			- 跳过 Ti 的所有日志，直到遇到 `<Ti, Oj, operation-begin>`
		- 如果遇到 redo-only log，忽略
		- 如果遇到 `<Ti, Oj, operatoin-abort>` 跳过 Ti 的所有日志，直到找到 `<Ti, Oj, operation-begin>`
		- 如果遇到 `<Ti, start>` 停止扫描
		- 在 log 结尾添加 `<Ti, abort>`

![[IMG-DB Cheatsheet-20250613150603234.webp|700x493]]

![[IMG-DB Cheatsheet-20250613150825826.webp|700x539]]

### ARIES

- 优势
	- physiological redo
		- 影响到的 page 是 physically identified，page 上的 action 可以是 logical 的
	- DPT，减少不必要的 redo
	- fuzy ckpt，只用记录 DPT 而不用永久化 dirty page
- basic concepts
	- LSN log sequence number
	- DPT dirty page table，能够避免不必要的 redo 操作
		- RecLSN 本页加入 DPT 时的 log record
			- 用于减少 redo work
		- PageLSN 在本页更新的最后一条 log LSN
			- update a page: X latch; write log; update page; record PageLSN; unlock
			- flush a page: S latch then write
			- 在 recovery 中避免重复 redo
	- ATT: | TxnID | LastLSN |
	- log record
		- basic: | LSN | TransID | PrevLSN | RedoInfo | UndoInfo |
		- CLR(compensation): | LSN | TransID | UndoNextLSN | RedoInfo |
			- 在 rollback 时写，不需要 undo，可以通过 UndoNextLSN 快速找到下一个需要 undo 的 log
			- ![[IMG-DB Cheatsheet-20250613151835548.webp|400]]
	- ckpt: DPT + ATT
		- overhead 很小，可以经常做

![[IMG-DB Cheatsheet-20250613152056074.webp|500]]

1. analysis pass
	1. 根据 DPT 的 RecLSN 决定 RedoLSN，取最小的，如果 DPT 空则取 ckpt 的 LSN
	2. 从 ckpt 开始 forward 扫描，更新 ATT 中的 Transaction 和 LastLSN，DPT 中新加页的 PageID PageLSN 和 RecLSN
2. redo pass，从 RedoLSN 开始 forward 扫描
	- 如果目标页在 DPT 中且当前 LSN 大于其 RecLSN，则从硬盘中读取该页，进行对应操作 *也就是，这一页在崩溃时没有刷盘，且现在的操作是这一页最后一次 fetch 之后的操作*
	- 否则跳过
3. undo pass，从最后开始 backward 扫描，分析阶段的 ATT 中存储了崩溃时每一个事务的 LastLSN
	- 选择 UndoLSN，在需要 undo 的所有事务中，取 UndoLSN 最大的，本质上是按照 backward 的顺序进行的
	- 每当遇到一条属于 ATT 中需要回滚的事务的 Update Log Record，进行反向操作，并记录 CLR(Compensation Log Record)，将这条 CLR 的 UndoNextLSN 设置为这条日志记录的 PrevLSN *也就是，如果需要再次 undo，可以直接跳过到这条日志记录的前一条，中间的操作已经抵消*
	- 确定下一条回滚事务 LSN
		- 如果当前事务是 CLR，取 UndoNextLSN
		- 否则取 PrevLSN
	- 直到 undo list empty

![[IMG-DB Cheatsheet-20250607171307170.webp|500]]

# 复习课

- 关系代数 2
	- 符号的含义，等价转换
	- 细节别看错
- SQL 3-4
	- 集合操作，聚合函数 Avg Sum Count Min Max，增删改，distinct
	- 尽量不用嵌套
	- 一般不涉及第五章的内容
- E-R 6
	- 判断题
	- mapping cardinality, participant constraints(total or partial) 什么含义，怎么画
	- 箭头、双线、虚线、标注
- normalization 7
	- ppt 上的例题
	- 无损分解：分解后 join 等于原来的，或者分解后两个表交集包括其中一个表的 candidate key
	- 正则覆盖：等价于 F；没有无关属性；左侧是不同的，否则可以合并
	- BCNF 更常用，但是无法依赖保持，3NF 更松，且以来保持
		- BCNF：对于所有依赖，alpha -> beta，要么 trivial 要么 alpha 是 superkey
			- 分解：alpha union beta；R-(beta - alpha)
			- 分解伪代码
			- 是无损分解，但不确保依赖保持的
		- 3NF：多一个条件，beta - alpha 的每一个 attr 都在 R 中一个 candidate key 中
			- 保证无损和依赖保持
- storage 12
	- 三级存储，二级是 flash, magnetic disk，三级是 tape, 光盘
	- 磁盘结构
		- 多层，每层同步读同一个扇区
		- 最小的传输单位是 block/page
		- 外侧扇区多，外道读写速率高
		- 读取时，先寻道，然后等扇区旋转后读取
		- Access time: 发出指令到第一个字节开始输出的时间
			- seek time
			- rotational latency
		- Data transfer rate: 外圈快
- storage structure 13
	- 变长度
		- record（起始位置、大小）null bitmap
		- slotted-page structure: [block header -> || free space || <records]
	- organization of records
		- heap, seq, b+, hash 这个有点不熟
- indexing 14
	- index record (search key, pointer)
	- ordered indices
		- clustering, secondary, dense, sparse 等概念
		- 辅助索引只能是稠密的，但是辅助索引的二级索引可以是稀疏的！
	- B+ 树代价分析数学表达，树大小估计
	- LSM Buffer
- query processing 15
	- selection A1-A10，A1 更加通用且不一定就最差
	- sorting 外部排序，分配 $b_b$ 个 buffer block，减少寻址次数
	- join: nested-loop join, blocked nested-loop join, merge join, hash join
		- merge join 先排序再 join
- query optimization 16
	- 逻辑等价表达式，**有十几条等价规则要看一遍**
	- select join 结果大小估计方法
		- select
			- selection size:L 等于和小于关系的元组数量估计，以及= key attr 怎么选都是 1
			- selectivity 选择率
		- join ... 反正要复习
	- 启发式方法：push selection, push projection, push most restrictive selection and join；但不一定真的就更好，要具体分析
- transactions 17
	- acid serializability recoverability
	- conflict, conflict serializability, precedence graph 等价可串行化调度不一定唯一
		- 每一个 view 可串行化的调度如果不是 conflict 可串行化的，那么一定有 blind write
	- recoverable: Tj 读了 Ti 的数据，那么 Ti 在 Tj 之前 commit
	- cascadeless: Ti 在 Tj 读之前 commit
- concurrency control 18
	- 2pl, lock point, growing/shrinking 可能死锁
	- strict 2pl 严格，X lock 持有到 commit
	- rigrous 2pl 增强，所有 lock 持有到 commit
	- **画一个图来表示上述的性质、概念空间**
	- tree protocol: 只用了排他锁，本身不会出现死锁，保证冲突可串行
	- 死锁：等待死亡、受伤等待模式，等待图
- recovery 19
