---
status:
  - archived
date_created: 2024-12-17T09:59:57
date_modified: 2025-09-12T13:16:26
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
---

> [!note] Note
> 1. 并不是最终使用的版本
> 2. ***与其抄很多知识点，不如抄点例题！***

# 1 Chapter 1

## 1.1 performance

- elapse time 总时间
- cpu time 除去 I/O 等其他因素的时间
- clock cycle time 时钟周期
- clock rate 时钟频率
- 同样的代码，如果 ISA 相同，则 \#inst 相同
- power of cpu $P=C\times V^2 \times F$
- amdahl's law $T_{\text{improved}}=\frac{T_{\text{affected}}}{\text{improvement factor}}+T_{\text{unaffected}}$
- MIPS: 每秒钟百万指令数

## 1.2 great ideas

- design for moore's law
- use abstraction to simplify design
- make the common case fast
- performance via parallelism
- performance via pipelining
- performance via prediction
- hierarchy of memories
- dependability via redundancy

# 2 Chapter 2 Instructions

## 2.1 指令表

![[references/CO-InstTypes.webp]]

![[references/CO-Insts.webp]]

> 这张图不用抄，如果考到了相关指令会给其作用的解释，但是可以记一下每一种指令是什么 type
> 或者记录一下简单的 opcode？

- `lr.d/lr.w` load reserved `lr.d rd, (rs1)`
	- 从 `(rs1)` 加载到 `rd`
	- 并在硬件上保留一个 `reservation` 标记
- `sc.d/sc.w` store conditional `sc.d rd, rs2, (rs1)`
	- 检查 `reservation` 标记是否有效，如果有效才将 `rs2` 的值写入 `(rs1)`，并标记 `rd=0`

```asm title="atomic swap"
again:
	lr.d x10, (x20)
	sc.d x11, (x20), x23
	bne x11, x0, again  # branch again if store failed
	addi x23, x10, 0
```

```asm title="lock"
	addi x12, x0, 1
again:
	lr.d x10, (x20)  # read lock
	bne x10, x0, again  # 设置了一个锁，解锁条件为 sd x0, 0(x20) 被执行，使得跳转条件不满足
	sc.d x11, (x20), x12  # attempt to store
	bne x11, x0, again
```

### 2.1.1 加载 32-bit 立即数

![[slides/CO_Ch2.pdf#page=80&rect=11,12,723,526|CO_Ch2, p.80]]

## 2.2 寄存器表

![[references/CO-Regs.webp]]

> - `ra` 在进入函数的第一步就要保护
> - `s` 类型寄存器使用前要保护

```asm title="factor"
fact:
	addi sp, sp, -16  # 栈对齐，sp 分配空间的单位为 16 bytes = 128 bits
	sd ra, 8(sp)  # 保护返回地址，每个参数都对齐到 64 位 double word
	sd a0, 0(sp)  # 保护参数，便于递归
	addi t0, a0, -1
	bge t0, zero, L1  # 如果不是叶子，跳到 L1
	addi a0, zero, 1
	addi sp, sp, 16  # 堆栈平衡
	jalr zero, 0(ra)  # 返回
L1:
	addi a0, a0, -1
	jal ra, fact  # 递归调用
	add t1, a0, zero  # a0 为调用返回值
	ld a0, 0(sp)
	ld ra, 8(sp)  # 恢复参数
	add sp, sp, 16  # 堆栈平衡
	mul a0, a0, t1
	jalr zero, 0(ra)  # 返回
```

## 2.3 Memory layout

> [!note]- 简单记一下就行
> ![[slides/CO_Ch2.pdf#page=69&rect=2,57,720,529|CO_Ch2, p.69]]
> ![[slides/CO_Ch2.pdf#page=70&rect=31,66,714,522|CO_Ch2, p.70]]

- little endians: least significant digit 的地址小，例如 `12345678h -> 78 56 34 12`
- fp: 栈帧指针
- sp: 栈顶指针

# 3 Chapter 3 Arithmetics

## 3.1 数制表示

- unsigned
- signed
	- sign-magnitude
	- 2's complement
	- *移码*，例如加 bias = -128

## 3.2 Add, Sub

- 减就是加上补码
- overflow
	- 负数相加得到正数
	- 正数相加得到负数

## 3.3 Mul

> [[CO 03 Arithmetic for Computer#4 Multiplication]]

![[slides/CO_Ch3.pdf#page=51&rect=36,50,688,523|CO_Ch3, p.51]]

## 3.4 Div

> [[CO 03 Arithmetic for Computer#5 Division]]

![[slides/CO_Ch3.pdf#page=68&rect=34,32,633,519|CO_Ch3, p.68]]

## 3.5 Floating point

- IEEE 754 `sign | exp | frac`
	- 32-bit: `sign 1 | exp 8 | frac 23`
	- 64-bit: `sign 1 | exp 11 | frac 52`
	- infinity: `exp = 111...1, frac = 000...0` 无穷也分正负
	- nan: `exp = 111...1, frac != 000...0` illegal or undefined result
- rounding `guard (frac[-1]) | round (frac[-2]) | sticky (frac[-3])`
	- sticky 表示 round 后面是否还有 1，如果有 1 那么 sticky 就是 1
	- round to nearest even 精度是 0.5ulp

![[slides/CO_Ch3.pdf#page=87&rect=78,52,651,457|CO_Ch3, p.87]]

# 4 Chapter 4 CPU

## 4.1 Single cycle cpu

![[slides/CO_Ch4_Pt1.pdf#page=49&rect=25,48,696,513|CO_Ch4_Pt1, p.49]]

> [!note] 题型
> - 信号是什么
> - datapath 流程/需要的 unit
> - 实现一定的指令扩展，信号？datapath？

## 4.2 Pipelined cpu

![[slides/CO_Ch4_Pt2.pdf#page=69&rect=21,43,711,524|CO_Ch4_Pt2, p.69]]

![[slides/CO_Ch4_Pt2.pdf#page=54&rect=25,35,715,515|CO_Ch4_Pt2, p.54]]

- 多/单周期流水线示意图样例

### 4.2.1 Data Hazard

#### 4.2.1.1 EX hazard

```pseudo
if (
	EX/MEM.RegWrite
	and (EX/MEM.Rd != 0)
	and (EX/MEM.Rd == ID/EX.Rs1)
) ForwardA = 10
```

#### 4.2.1.2 Mem hazard *load use*

```pseudo
if (
	MEM/WB.RegWrite
	and (MEM/WB.Rd != 0)  // 有效 WB
	and not (
		EX/MEM.RegWrite
		and (EX/MEM.Rd != 0)  // 上一条指令有效 WB
		and (EX/MEM.Rd == ID/EX.Rs1)
	)  // 下一条指令不需要进行 EX hazard forwarding
	and (MEM/WB.Rd == ID/EX.Rs1)
) ForwardA = 01
```

#### 4.2.1.3 Stall *load use*

```pseudo
if (
	ID/EX.MemRead
	and (
		(ID/EX.Rd == IF/ID.Rs1)
		or (ID/EX.Rd == ID/IF.Rs2)
	)
) stall the pipeline
```

> load use: stall + mem forwarding

### 4.2.2 Branch Hazard

- branch 可以提前到 ID，但是至少仍然产生一个 bubble
- dynamic prediction: 1/2-bit predictor
- branch target buffer，执行到 branch 就根据预测结果跳到 target 执行，不用再计算 pc

### 4.2.3 Exceptions

- `PC -> SPEC (Supervisor Exception Program Counter)`
- `ERROR CODE -> SCAUSE (Supervisor Exception Cause Register)`
- 跳转到 handler
	- `if restartalbe`: 修正错误，并返回到 `SPEC`
	- `else` 终止，向操作系统上报错误
- `PC` 前面需要扩展一个 `MUX` 来进行选择

![[Textbook/Computer Organization and Design [RISC-V Edition].pdf#page=472&rect=138,132,494,449|Computer Organization and Design [RISC-V Edition], p.352]]

# 5 Memory Hierarchy

- 金字塔
- disk access time 计算示例
- 几种表示例
- 几种 cache 结构示例
	- direct mapped
	- fully associative
	- set asso

## 5.1 Write

- write miss 如果目标不在内存里
	- write around: 直接写到 mem
	- write allocate: 先加载到 cache 再执行正常的写
- 正常的写操作 write strategy
	- write through: 总是写入到 mem
		- -> 问题：write stall -> 使用 write buffer 解决
	- write back 需要

## 5.2 Perf

- AMAT =  hit time + miss time = hit time + miss rate \* miss penalty
- CPU Time = CPU exe. clock cycles + mem-stall clock cycles

# 6 IO

- throughput & response time
- (average) disk access time
	- (average) seek time
	- rotational latency 平均转半圈
	- transfer time: 读取和传输一个 sector
	- disk controller: 控制器延迟
