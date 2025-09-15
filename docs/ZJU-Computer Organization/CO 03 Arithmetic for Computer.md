---
status:
  - archived
tags: CS/Hardware/Arithmetic
attachment:
  - "[[slides/CO_Ch3.pdf|CO_Ch3]]"
date_created: 2024-11-10T12:07:50
date_modified: 2025-09-12T13:12:41
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
---

# 1 Introduction

- 约定 word 是 32bits
- double word 是 64bits
- program counter `PC + 4`，指令都是 32 位的

# 2 Signed and Unsigned Numbers

![[./__assets/CO 03 Arithmetic for Computer/IMG-CO 03 Arithmetic for Computer-20250315140541538.webp]]

- unsigned
- signed
	- sign magnitude
	- 2's complement
- *移码*，例如加上 -128 的 bias 来表示负数..

# 3 Addition, subtranction and ALU

- 加法需要注意 carry
- 减就是加上补码

## 3.1 Overflow

- 什么时候发生
	- 负数相加得正数
	- 正数相加得负数
- **设计逻辑电路可以进行溢出判断**
- 如何处理？
	- 可以 ignore，或者在编译的时候避免
	- OS 来处理
		- 将 PC 设置成 OS 处理溢出的指令地址
		- 可以修正然后 return
		- 也可以 exit 并报错
- ! 发生的时候寄存器写入失效

## 3.2 ALU

- ALU 支持的操作没有定义，一个加法器也可以叫做 ALU
	- 模块化设计，不同指令需要的部分是不一样的
	- MUX 输出选择

![[./__assets/CO 03 Arithmetic for Computer/IMG-CO 03 Arithmetic for Computer-20250315140612385.webp]]

> [!tip] Tip
> - 设计 1-bit 并扩展
> - 设计不同功能并选择

# 4 Multiplication

![[./__assets/CO 03 Arithmetic for Computer/IMG-CO 03 Arithmetic for Computer-20250315140619535.webp]]

- multiplier 先保存在 `product[63:0]`
- 如果 `product[0] == 1` ，那么 `product[127:64]` 加上 multiplicand，然后右移
- 129 bit 是为了保证过程中加法可能算出的最高位
- 一共需要移动 64 次，这是因为原本 `product[63:0]` 是 multiplier

![[./__assets/CO 03 Arithmetic for Computer/IMG-CO 03 Arithmetic for Computer-20250315140627136.webp]]

## 4.1 Booth's Algorithm

> [!tip]- Tip
> ![[./__assets/CO 03 Arithmetic for Computer/IMG-CO 03 Arithmetic for Computer-20250315140637714.webp]]
> ![[./__assets/CO 03 Arithmetic for Computer/IMG-CO 03 Arithmetic for Computer-20250315140645713.webp]]

- 将连续的 `1111` 变成 `10000 - 1`

# 5 Division

![[./__assets/CO 03 Arithmetic for Computer/IMG-CO 03 Arithmetic for Computer-20250315140652685.webp]]

![[./__assets/CO 03 Arithmetic for Computer/IMG-CO 03 Arithmetic for Computer-20250315140700161.webp]]

- Dividend 初始加载到 `remainder[63:0]`，并左移一位
- 将 `remainder[127:64]` 减去 divisor，结果保存在 `remainder[127:64]`
	- 如果结果大于 0，那么 `remainder` 左移，并使 `remainder[0] = 1`
	- 如果结果小于 0，那么将 `remainder[127:63]` 加上 divisor 复原，`remainder` 左移，`remainder[0] = 0`
	- 上述执行 64 次
- 最终，因为多左移了一次，需要 `remainder` 右移一位，`remainder[127:64]` 是余数，`remainder[63:0]` 是商

> [!question]- 为什么同时需要 shift left/right
> - dividend 初始放在寄存器的右侧，肯定需要左移
> - 最后的 remainder 在左半边，总的左移次数是 65 次，所以要右移一位
> - ![[./__assets/CO 03 Arithmetic for Computer/IMG-CO 03 Arithmetic for Computer-20250315140709116.webp]]

## 5.1 Signed Division

- 余数的符号与被除数的符号一致
- 其他的部分用 unsigned 就好
- ! 除以 0，引发 overflow

# 6 Floating Point Numbers

- `sign`， 1 表示负数
- `exp`，具有 bias，fp32 是 -127，fp64 是 -1023
- `frac`，舍掉最左侧的 1

![[./__assets/CO 03 Arithmetic for Computer/IMG-CO 03 Arithmetic for Computer-20250315140726651.webp]]

- ! 注意保留了一些 exp 的取值，以表示溢出

![[./__assets/CO 03 Arithmetic for Computer/IMG-CO 03 Arithmetic for Computer-20250315140737206.webp]]

## 6.1 FP Add

![[./__assets/CO 03 Arithmetic for Computer/IMG-CO 03 Arithmetic for Computer-20250315140744040.webp]]

## 6.2 Rounding

- methods
	- always round up (to $+\infty$)
	- always round down (to $-\infty$)
	- truncate 直接截断
	- round to nearest even
		- 四舍五入
		- 0.5 要看前面 bit 的奇偶
- `guard (frac[-1]) | round (frac[-2]) | sticky (frac[-3])`
	- sticky 表示 round 后面是否还有 1，如果有 1 那么 sticky 就是 1
	- round to nearest even 精度是 0.5ulp

![[./__assets/CO 03 Arithmetic for Computer/IMG-CO 03 Arithmetic for Computer-20250315140752297.webp]]
