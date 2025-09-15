---
status:
  - archived
tags: CS/Hardware/CPU
attachment:
  - "[[slides/CO_Ch4_Pt1.pdf|CO_Ch4_Pt1]]"
date_created: 2024-10-29T09:24:33
date_modified: 2025-09-13T10:18:08
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
---

# 1 Introduction

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315140814181.webp]]

- 在指令进入寄存器模块前，不需要进行解码，因为 RISC-V 中不同指令的 `rd, rs1, rs2` 的相对位置完全一致，*除了立即数，本图缺少了 `ImmGen` 模块*。
- `Contorl` 信号控制所有的 MUX，以及模块的使能信号
- CPUTime 取决于频率和 CPI，Cycle 小可能导致 CPI 增大

# 2 Datapath

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315140821047.webp]]

- Modify PC 是旁路，剩下五个是标准步骤，**明确某种指令对应的最小需要单元**
- Fetch inst mem
- Inst decoding & read operand，执行速度快，同步进行
- Executive Control, ALU operations
- Mem access，不是所有指令都需要访存，`ld/sd`
- Write to reg, R/I

## 2.1 不同指令使用的模块

### 2.1.1 Fetch

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315140827706.webp]]

### 2.1.2 R-Type

- Read two reg operands
- Perform ALU operation, *arithmetic/logical*
- Write result to reg

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315140835203.webp]]

- 注意 RISC-V 中 `ALUop` 是 4 bit 的，因为实现了更多功能
- `reg` 的信号要求
	- `rs1, rs2`
	- `rd` 信号保持
	- `RegWrite = 1'b1`

### 2.1.3 Load/Store

- Read reg operands
- Calculate address, *use ALU, 12-bit offset, sign extened*
- Read/Write reg/mem

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315140841872.webp]]

- 由于内存访问**开销较大**，设计 `MemRead` 来避免不可控的访存
- `ImmGen` 的输入就是 `inst`，要针对不同类型的指令提取/重组立即数，并进行 sign extend

### 2.1.4 Branch

- Read reg operands
- Compare operands
	- ALU zero output
- Calculate target address
	- sign-extend displacement
	- shift left 1
	- add to PC value

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315140851602.webp]]

- offset 左移是在电路里完成的，产生了 offset \* 2 的效果，但是在写代码的时候不需要考虑，编译器会处理好
- `jal` 没有用到 ALU，因为不需要跳转条件，但是也用到了寄存器，因为保存了 `return address`

## 2.2 连线题

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315140900464.webp]]

- ALUC 就是 `ALUControl`，将 `fun7, fun3` 单独解码有利于加快速度
- `ALUop[1:0]`
- ! 图中的 `ALUC` 输出应该是 4-bit

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315140907471.webp]]

- ! 图中 `rs1` 连错了
- ! 图中 Sign extend 应该是 `ImmGen` 模块
- ! 这张图错误太多了

> [!question] 改成 `addi`
> - 将 ALU result 接到 reg write data
> - 让 MemWrite MemRead 都为 0

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315140917083.webp]]

- `RegWrite = MemRead = 0, MemWrite = 1`

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315140924226.webp]]

- ! 图中 Sign extend 应该为 `ImmGen`
- ! 图中右上角的 MUX 第一个输入应该为 `PC+4`

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315140930951.webp]]

- ! 这张图不完整，直接 loop 了，没有保存 `return addres`
- ! 图中的 Sign extend 应该为 `ImmGen`
- ! 应该为 `PC+4`
- 无条件跳转不需要 ALU

## 2.3 Full Datapath

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315140938981.webp]]

- 三个控制信号
	- `ALUSrc` 决定 operand2 是 `rs2` 还是 `imm`
	- `PCSrc` 决定 `PC` 是用 `PC+4` 还是跳转地址
	- `MemtoReg` 决定 reg write 用 mem 还是 `ALUresult`
- 五个步骤
	- inst fetch
	- decode & reg read
	- execute
	- mem
	- write to reg

## 2.4 不同指令的数据通路

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315140945475.webp]]

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315140954467.webp]]

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315141001135.webp]]

- `ALUSrc` 只能取 `Imm`
- `MemtoReg` 这个 MUX 取任何值都可以，反正 `RegWrite = 0`

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315141010300.webp]]

- `PCSrc = Branch & ALU_zero`

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315141017840.webp]]

- `jal` 做了两件事情
	1. 将 `PC+4` 存入 `rd`，需要经过 `MemtoReg`，于是需要换成 2-bit 控制信号
	2. 跳到 `PC+offset`，不用经过 ALU
- `ALUSrc, ALUOperation` 可以随便选，ALU 输入输出没有任何影响

# 3 Control

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315141029502.webp]]

## 3.1 控制信号 7+4

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315141040136.webp]]

- & 7+4 控制信号
	- 7 个单独的信号
	- 4 位 ALU 控制信号
- ! 图中 `ALU_zero` 没有连接 `PCSrc`，当然 `ALU_zero` 也不属于控制信号

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315141046966.webp]]

- ! 和书上不同，`MemtoReg` 应该是两位的
- & 注意二级译码，`ALUop` 信号是 `ALUController` 二级译码产生的信号

## 3.2 完整的 control

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315141056664.webp]]

- & 一定要记住的一张图
- 这里使用了二级译码，`control` 输出的 `ALUOp` 是 2 位的
- 关于 `X` 的情况
	- `sd, bep` 都不写入寄存器，`RegWrite = 0`，所以 `MemtoReg = don't care`
	- `jal` 不需要主 ALU 的任何操作，所以 `ALUSrcB = ALUOp = don't care`
- Instruction memory & Data memory
	- 从处理器的视角，有利于提高吞吐量
	- 但是在实际内存中是共享的，只是缓存映射不一样

### 3.2.1 关于二级译码

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315141104701.webp]]

## 3.3 更多分析题

[[slides/CO_Ch4_Pt1.pdf#page=54&selection=2,0,4,16&color=yellow|CO_Ch4_Pt1, p.54]]

# 4 Conclusion

- &  记住下面两张图

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315141117501.webp]]

![[./__assets/CO 04 The Processor Pt1/IMG-CO 04 The Processor Pt1-20250315141127400.webp]]
