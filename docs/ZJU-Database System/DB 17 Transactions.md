---
status:
  - archived
tags: CS/DB/ACID
date_created: 2025-05-20T13:35:56
date_modified: 2025-09-13T10:18:12
---

# Concepts

- **transaction**: 程序执行的单元
- (Atomic) 原子性要求：要么没有执行，要么执行完成，确保由于外部故障导致部分执行的操作不会对 db 产生影响
- (Durability) 持久性要求：事务执行完成后，外部故障不会导致 db 中的更新受到影响
- (Consistency) 一致性要求：例如转账前后，两个账户总余额相等
- (Isolation) 隔离性要求：各个事物相互之间无法感知，就像事务在串行处理一样

# Concurrent Executions

- 并发执行的优点
	- 增加了处理器和硬盘的利用率
	- 降低平均响应时间

## Anomalies in Concurrent Executions

![[IMG-DB 17 Transactions-20250520140439702.webp|400]]

- Lost Update: 同时修改同一位置数据，只保留了最后一个写入

![[IMG-DB 17 Transactions-20250520140554484.webp|400]]

- Dirty Read: 一个事务修改了 A，但还没提交，此时另一个事务读到了 A 的新值

![[IMG-DB 17 Transactions-20250520140734588.webp|500x371]]

- Unrepeatable Read: 不可重复读，由于另一个事务的执行，同一个事务中不同位置读同一数据值不同

![[IMG-DB 17 Transactions-20250520140917318.webp|500x247]]

> [!note] Note
> 隔离性越高，并发程度越低

# Serializability

- **schedule**: 一组并发事务的所有指令执行的顺序
	- 包含这些事务的所有指令
	- 必须使执行顺序能够实现这些事务独立执行
- Serializability: 一个 schedule 如果等价于 serial 执行，那么具有 serializability，有两种 equivalence
	- Conflict serializability
	- View serializability
- view: 只用关注 read & write 就好，其他操作可以忽略

## Conflict Serializability

### Conflicting Inst.

![[IMG-DB 17 Transactions-20250520142756794.webp|500x135]]

- 只要有 write，就不能交换顺序

- 如果 S 能通过一系列 **non-conflicting** inst 交换，得到 S'，则二者 conflict equivalent
- 如果 S 与一个 serial schedule 是 conflict equivalent 的，则其是 conflict serializable

![[IMG-DB 17 Transactions-20250520143247852.webp|500x278]]

![[IMG-DB 17 Transactions-20250520143304201.webp|500x141]]

# View Serializability

- S 和 S' 是 view equivalent 如果对于所有数据 Q
	1. S 中读 Q 初始值的 T 在 S' 中也读初始值
	2. S 中读 $T_i$ 产生的 Q 的值的 $T_j$ 在 S' 中也如此
	3. S 中最后写 Q 的 T 在 S' 中也写最后的 Q 值
- 如果 S 和一个 serial schedule 是 view equivalent 的，则称为 view serializable

## Other Serializability

![[IMG-DB 17 Transactions-20250520143855543.webp|500x283]]

# Testing for Serializability

## Precedence Graph (for Conflict Serializability)

- 前驱图，存在边 $(T_i, T_j)$ 如果二者 conflict，且 conflict 指令对中 $T_1$ 执行的早
- 如果前驱图存在还，则不可串行化
- 否则，按照拓扑排序进行串行化

## Testing for View Serializability

- NP-Complete

# Recoverability

- recoverable schedule: $T_j$ 读取了先前另一个 $T_i$ 写的数据，则 $T_i$ 必须先 commit

## Cascading Rollbacks

![[IMG-DB 17 Transactions-20250520144934745.webp|500x241]]

### Cascadeless Schedules

- cascadeless schedules: 不能发生 cascading rollbacks
- 存在数据依赖时，先 commit 再读，例如上图中，$T_{10}$ 应当在 $T_{11}$ 读之前就 commit

## Concurrency Control

> 试图找到一个机制，能够生成可串行化 schedule，并且能够测试其可串行化性

**concurrency control protocols** in ch.18

## Weak Levels of Consistency

> 为了性能，可以牺牲一些一致性，schedule 不一定都是可串行化的

- **Repeatable read**
- **Read committed**
- **Read uncommitted**

# Implementation of Isolation

- Locking
- Timestamps
- Multiple versions of each data item
