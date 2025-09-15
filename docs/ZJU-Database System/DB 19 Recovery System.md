---
status:
  - archived
tags: CS/DB/ACID
date_created: 2025-05-27T14:34:09
date_modified: 2025-09-13T10:16:34
---

# Failure Classification

- 事务故障
	- 逻辑错误
	- 系统错误
- 系统崩溃
- 硬盘故障

## Recovery Algorithms

1. 在进行事务处理时额外记录的信息
2. 在 failure 出现后恢复数据库内容的 ACID 特性

# Recovery and Atomicity

- log: 对数据库的更改日志
	- 记录在非易失的 stable storage (稳定存储器) 上

# Algorithm

- 找到最近的 checkpoint L，checkpoint 开始前的所有提交/终止的都不用管，设置 undo_list 为 L
- Redo Phase: 从 checkpoint L 开始往后扫描
	- 遇到操作则进行
	- 遇到 <T_i start> 加入 undo_list
	- 遇到 <T_i commit> 或者 <T_i abort>，从 undo-list 中溢出 T_i
- Undo Phase: 从最后一条 log 往回扫描
	- 遇到一条 T_i 执行的 log，而且 T_i 在 undo_list 中，则撤销，写撤销 log
	- 遇到 <T_i start>，从 undo_list 中删除 T_i，写 <T_i abort> log
