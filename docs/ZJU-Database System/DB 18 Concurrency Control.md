---
status:
  - archived
tags: CS/DB/ACID
date_created: 2025-05-20T15:10:17
date_modified: 2025-09-13T10:18:12
---

# Lock-based Protocols

- exclusive
- shared

![[IMG-DB 18 Concurrency Control-20250520151953143.webp|500x307]]

- 两个事务执行互相等待，解决死锁的方式时 rollback 其中一个事务

## Two-Phase Locking Protocol

- 能够保证生成 conflict-serializable schedule
- Growing Phase: 事务只能申请锁/升级锁
- Shrinking Phase: 事务只能释放锁/降级锁
- Lock Points: 事务得到最后一个锁的时间点，进行 serializable 等价的时候，按照 lock point (封锁点) 顺序排序

- **Strict two-phase locking**: 直到 commit/abort 才释放所有 exclusive lock
	- 保证了 recoverability，避免 cascading roll-backs
- **Rigorous two-phase locking**: 直到 commit/abort 才释放所有 lock
	- serialize 等价为 commit 顺序

- 作用
	- 可以保证 conflict serializable 调度
	- 无法避免 dead lock

## Implementation of Locking

![[IMG-DB 18 Concurrency Control-20250527133247658.webp|475x611]]

- Lock Table: 一种内存中的数据结构
	- 使用 hash table 进行 index 映射
	- 每个 index 进行排队
	- 事务提交/终止，删除其在 lock table 中的所有锁
- 也可以维护 a list of locks held by each txn，来加速某个事务所有锁的查询

## Graph-Based Protocol

- 对于所有 data $D$，设置偏序关系 $d_i\rightarrow d_j$，表示任何事务要访问 $d_i, d_j$ 时必须先访问 $d_i$
- $D$ 是一个 dag(有向无环图)，称为 database graph

## Tree Protocol

![[IMG-DB 18 Concurrency Control-20250527134008571.webp|500x366]]

- 只有 exclusive locks
- txn 在申请 B 的锁时，需要先申请 A 的锁
	- 申请到的锁的数量可能大于实际需要的锁的数量
	- 但可以在任意时刻释放
	- 一个 data item 只能申请和释放锁一次
- 作用
	- 保证 conflict serializable
	- 可以避免 dead lock
	- 等待时间相对较短，*相比 2pl 只能在最终释放*
- 缺点
	- 无法保证 recoverability or cascade freedom
	- 申请的锁太多，效率低
- 特点
	- 2pl 中无法生成的 schedule 在 tree protocol 中可能生成，反之亦然

# Deadlock Handling

- 偏序协议（graph tree）可以避免死锁
- 或加入额外的干预条件，例如“所有事务取得所有锁才能开始执行”

## Strategies

- Wait-die(no-preemptive 非抢占): 旧的事务等待，新的事务 rollback
- Wound-wait(preemptive 抢占): 旧的事务强制 rollback，新的事务等待
- rollback 之后需要重新开始，但仍然使用上次执行用的时间戳
- Timeout-Based Schemes
	- 可能导致饥饿
	- 确定好的 time-out 时间非常难

## Detection

![[IMG-DB 18 Concurrency Control-20250527135639058.webp|500x343]]

- 如果有环，说明 dead lock 存在

# Multiple Granularity

![[IMG-DB 18 Concurrency Control-20250527140152665.webp|500x230]]

- 加锁数据的粒度仍然有差别，例如 relation, db, db, file
- 如果一个 txn 给节点 $i$ 枷锁，则也对 $i$ 的所有孩子加共享做锁
- 增加三种锁
	- intention-shared(IS): 对父节点加 IS，可以
	- intention-exclusive(IX)
	- shared and intension exdlusive(SIX)
- 加锁的范围越小，事务并行化空间越大

![[IMG-DB 18 Concurrency Control-20250527140701065.webp|500x295]]

![[IMG-DB 18 Concurrency Control-20250527140752766.webp|500x277]]

# Insert and Delete Operations

## Predicate Reads and Phantom Phenomenon

![[IMG-DB 18 Concurrency Control-20250527142029865.webp|500x158]]

- 无法只用 tuple level 的锁
- One solution:
	- 在 relation 中加入一个 data item 指示器，表示关系包含的元组
	- 进行插入或删除时，需要申请这个 data item 的锁
- Another: index locking
	- 加锁的对象是所操作对象对应的 leaf node
	- 必须保证 2pl
	- 并发性比 data item 好，因为加锁的粒度更细
- Best: Next-Key Locking
	- 对于 leaf node next key 的所有 value 加锁

![[IMG-DB 18 Concurrency Control-20250527143056772.webp|500x109]]

1. 查询，对 8 11 14 18 加共享锁
2. 插入时，15 的 next key 18 不能加排他锁，7 的 next key 8 也不能加排他锁，因此插入等待，不会产生 phantom 现象
