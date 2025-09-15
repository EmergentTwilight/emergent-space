---
status:
  - archived
tags: CS/DB/Design
date_created: 2025-03-18T14:42:39
date_modified: 2025-09-13T10:18:12
---

# Overview

- phases
	- initial phase: 需求调研
	- second phase
		- 选择 data model
		- 形成 conceptual schema
	- final phase: moving to implementation
		- logical design
		- physcial design
- alternatives
	- redundancy: 数据的重复，可能导致不一致
	- incompleteness: 一部分设计很难建模出来
	- 如何衡量好的设计有多好？
- approaches
	- ER model
	- Normalization Theory (范式理论 in chap. 7)

# The Entity-Relationship Model

- 3 basic concepts
	- entity sets
	- relationship sets
	- attributes

## Entity Sets

- entity: 某个人、某家企业
- entity set: 具有相同类型的实体的集合
- 一个 entity 具有一些 attr，一个 entity set 具有相同的 attr 类型
- 一个 entity set 的属性的子集形成了 primary key，能够唯一识别 set 中的成员
- 表示
	- 上方有集合名称
	- 下划线是主键

![[IMG-DB 06 Database Design using the E-R Model-20250318151010785.webp|500x221]]

## Relationship Sets

![[IMG-DB 06 Database Design using the E-R Model-20250318151251637.webp|500x264]]

- 一个关系是数个实体之间的联系
- 一个关系集合是一类关系的集合

![[IMG-DB 06 Database Design using the E-R Model-20250318151519050.webp|500x148]]

- 关系集合也可以有属性，例如成为学生的时间

![[IMG-DB 06 Database Design using the E-R Model-20250318151557068.webp|500x163]]

### Roles

> The function that an entity plays in a relationship is called that entity's **role**.
> 角色是实体在关系中的作用

![[IMG-DB 06 Database Design using the E-R Model-20250318151927012.webp|500x233]]

### Degree of a Relationship Set

- 大部分都是二元关系
- 少部分用三元关系表示比较清晰，但是也可以转化为二元关系
	- e.g. *students* work on research *projects* under the guidance of an *instructor*

![[IMG-DB 06 Database Design using the E-R Model-20250318152242234.webp|500x252]]

# Complex Attributes

- attr types
	- simple and composite
		- 复合属性的子属性也可以是复合属性
	- single-valued and multivalued
	- derived(派生), 例如生日和年龄
- **Domain**: 每个属性的 valid 值空间

![[IMG-DB 06 Database Design using the E-R Model-20250325133525452.webp]]

- 使用缩进表示复合关系
- 使用大括号表示多值属性
- 使用小括号表示派生属性*类似函数*

# Mapping Cardinalities

- cardinalities constrs
	- one to one
	- one to many
	- many to one
	- many to many
- total and partial participation
	- 用双线表示全部参与的实体类，例如学生全部有 advisor 关系

![[IMG-DB 06 Database Design using the E-R Model-20250325134152690.webp]]

![[IMG-DB 06 Database Design using the E-R Model-20250325134759655.webp]]

## Expression for More Complex Constraints

![[IMG-DB 06 Database Design using the E-R Model-20250325135055436.webp]]

- 表示的是上下界
- `*` 表示 no limit

## on Ternary Relationship

- 默认**最多只能有一个箭头**，避免多种解释
- 超过一个箭头，会导致多种解释，例如 B C 都有箭头，可以理解为
	- 每个 A 对应唯一的 B 和 C
	- 每个 pair (A, B) 对应唯一的 C，每个 pair (A, C) 对应唯一的 B

# Primary Key

- Primary Key 用来在实体和关系中进行区分，考虑以下集合中的主键
	- entity sets
	- relationship sets
	- weak entity sets

## Entity Sets

- 首先，默认每个实体都是是不同的
	- No two entities in an entity sets are allowed to have exactly the same value for all attrs
- 复习
	- 主键是候选键之一
	- 候选键是*最小*超键
	- 超键能唯一确定元素

## Relationship Sets

- 要区分不同的 relationship，所以也需要 primary key
- 如果实体的属性字段重名，需要重新命名
- 首先，无论 relationship set 是否有自己的属性，其相关实体集合的主键的并集总是 relationship set 的一个超键
- 其次，mapping cardinality 不同，主键的选择也有不同
	- many to many: 实体主键并集
	- many to one: many 那边的主键
	- one to many: many 那边的主键
	- one to one: 任意一边的主键

## Weak Entity Sets

![[IMG-DB 06 Database Design using the E-R Model-20250325143140222.webp]]

- 例如 section 实体由 `course_id, semester, year, sec_id` 唯一确定，如果再建立 sec_course 来连接 section 和 course，则信息是有冗余的
- A **weak entity set** is one whose existence is dependent on another entity, called its **identifying entity**(标志性实体)
	- 没有主键，弱实体集自身没有足够属性来形成主键，必须依赖强实体集
	- 具有部分键 (partial key)，部分键是能在**同一个强实体**范围内唯一标识弱实体的属性
		- e.g. 一个公寓单元的单元号是部分键，在不同建筑中可能重复，所以需要依赖建筑这个强实体集
- ER 图中，弱实体集使用双矩形表示，**识别关系**使用双菱形表示

# Removing Reduntant Attrs

![[IMG-DB 06 Database Design using the E-R Model-20250325144520222.webp]]

- e.g. student 中有 dept_name，department 中也有 dept_name，student 中的 dept_name 是*冗余的*，需要移除
- 但是当转换成表格时，一些情况下，被移除的属性又会被重新加入，*仅仅是在 ER 图阶段是冗余的*

![[IMG-DB 06 Database Design using the E-R Model-20250325144543392.webp]]

# E-R Diagram to Relational Schemas

- 强实体集合直接转换成 relation，并设置主键
- 弱实体结合会**重新引入依赖的强实体集合的主键**，例如 `section: sec_id, ... -> section: course_id, sec_id, ...`
- 复合属性会被 flatten，例如 `name_first_name, name_last_name`
- 忽略多值属性，可以单独再创建表来保存
- 忽略派生属性

## Redundancy of Schemas

![[IMG-DB 06 Database Design using the E-R Model-20250325145205072.webp]]

- 多对多的关系需要转化成表
- 一对多、多对一，只需要在多的一遍增加对侧主键
- 一对一，任选一边增加对侧主键

# Extended E-R Features

![[IMG-DB 06 Database Design using the E-R Model-20250325145628210.webp]]

- 箭头表示 *is a* 关系
- 重叠 (overlapping) 特化表示，同时可以具有两种身份，可以同时是学生和员工
- 不重叠 (disjoint) 特化表示，不可以同时具有两种身份，不可同时是导师和秘书

## Specialization

- 从上往下看是特化，可以继承或不继承
- 不继承，节省空间，但是查询时需要多表查询，效率低 ![[IMG-DB 06 Database Design using the E-R Model-20250325150143202.webp]]
- 继承，redundant，消耗空间，但是查询更快，不用多表连接 ![[IMG-DB 06 Database Design using the E-R Model-20250325150132073.webp]]

## Generalization

- 从下往上看是概化
- 概化一般都是 total participation

> [!note] Completeness Constratint
> - total: 高级实体全部需要参与低级实体集合的一个
> - partial: 高级实体不一定需要属于低级实体集合

## Aggregation

![[IMG-DB 06 Database Design using the E-R Model-20250325151030535.webp]]

- 将三元关系聚合成**抽象实体**(Abstract Entity)
	- e.g. 项目评估时，将 project, student, instructor 聚合为一个**抽象实体**
- 转化为 schema 时，会发现 eval_for 和 proj_guide 是冗余的

## 3-relationship to 2-relationship

![[IMG-DB 06 Database Design using the E-R Model-20250325152030965.webp]]

## E-R Symbols

![[IMG-DB 06 Database Design using the E-R Model-20250325152401931.webp]]

![[IMG-DB 06 Database Design using the E-R Model-20250325152420764.webp]]

# Alternative Notations for Modeling Data

![[IMG-DB 06 Database Design using the E-R Model-20250409134642973.webp]]

## UML

- Unified Modeling Language
- 关系框被省略，直接画线连接，关系名写线上

# Other Aspects of Database Design

- functional requirements
	- interfaces
	- authroization
- data flow, workflow
	- store the workflow data
	- need a series of daa queries and updates
- schema evolution
	- consider the future demand
	- minimize the modification
