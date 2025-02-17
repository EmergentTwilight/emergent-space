---
MkDocs_comments: true
date_created: 2024-12-18 13:31:23
date_modified: 2025-01-25 16:26:59
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
state:
- 待发布
- 归档
tags: Programming-Language/Assembly/80x86
type:
- note
---
# 1 总结

> 8086 一共有 14 个寄存器，分别为：

- 通用寄存器：`AX, BX, CX, DX`
- 段地址寄存器：`CS, DS, ES, SS`
- 偏移地址寄存器：`IP, SP, BP, SI, DI`
- 标志寄存器：`FL`

> 80386 中除了段地址寄存器仍然是 16 位，其余均扩展到 32 位

# 2 通用寄存器

> 用于算数、逻辑、移位运算

| 名称  | `AX`        | `BX` | `CX`  | `DX` |
| --- | ----------- | ---- | ----- | ---- |
| 助记  | accumulator | base | count | data |

# 3 段地址寄存器

| 名称            | `CS`                                      | `DS`                                  | `ES`                                  | `SS`                                  |
| ------------- | ----------------------------------------- | ------------------------------------- | ------------------------------------- | ------------------------------------- |
| 助记            | code segment                              | data segment                          | extra segment                         | stack segment                         |
| 是否能用 `mov` 赋值 | **不能**<br>只能用 `jmp, call, ret, int` 等间接改变 | **可以**<br>但是 `SRC` 必须是寄存器或变量而不是 `imm` | **可以**<br>但是 `SRC` 必须是寄存器或变量而不是 `imm` | **可以**<br>但是 `SRC` 必须是寄存器或变量而不是 `imm` |
| 可用的源寄存器       | 无                                         | `AX, BX, CX, DX, SP, BP, SI, DI`      | `AX, BX, CX, DX, SP, BP, SI, DI`      | `AX, BX, CX, DX, SP, BP, SI, DI`      |

```asm title="间接赋值"
; method 1
mov ax, 1000h
mov ds, ax

; method 2
mov word ptr ds:[bx], 1000h
mov es, ds:[bx]
```

## 3.1 寄存器内容初始化

> [[ASMF 05 段和堆栈#3 寄存器初始化赋值和 `psp` 段]] 有更多关于 `psp` 段的内容

| `CS:IP`           | `SS:SP`        | `DS`       | `ES`       |
| ----------------- | -------------- | ---------- | ---------- |
| `代码段段地址:首条指令偏移地址` | `堆栈段段地址:堆栈段长度` | `psp 段段地址` | `psp 段段地址` |

这也就是为什么需要先对 `DS` 进行赋值，才能引用 data segment 中的变量

# 4 偏移地址寄存器

| 名称            | `IP`                | `SP`          | `BP`               | `SI`               | `DI`               | (`BX`)             |
| ------------- | ------------------- | ------------- | ------------------ | ------------------ | ------------------ | ------------------ |
| 助记            | instruction pointer | stack pointer |                    |                    |                    | base               |
| 用于 `[]` 间接寻址？ | **不能**              | **不能**        | **能**<br>隐含 `SS` 段 | **能**<br>隐含 `DS` 段 | **能**<br>隐含 `DS` 段 | **能**<br>隐含 `DS` 段 |
| 参与算数、逻辑、移位运算？ | **不能**              | **不能**        | **能**              | **能**              | **能**              | **能**              |

# 5 FL 标志寄存器

- FL 是 16 位的，但是其中只有每一位的布尔值有效，整体没有意义

| 15   | 14     | 13   | 12     |
| ---- | ------ | ---- | ------ |
| x    | x      | x    | x      |
| 0    | 0      | 0    | 0      |
|      |        |      |        |
| 11   | 10     | 9    | 8      |
| OF   | DF     | IF   | TF     |
| 溢出标志 | 复制方向标志 | 中断标志 | 陷阱标志   |
|      |        |      |        |
| 7    | 6      | 5    | 4      |
| SF   | ZF     | x    | AF     |
| 符号标志 | 零标志    | 0    | 辅助进位标志 |
|      |        |      |        |
| 3    | 2      | 1    | 0      |
| x    | PF     | x    | CF     |
| 0    | 奇偶校验标志 | 1    | 进位标志   |

## 5.1 Carry Flag 进位标志

- CF *Carry Flag* 进位标志
	- 加法操作的进位、左移出来的 1，都会存到 CF
	- `jc` 如果有进位则跳转

```asm
code segment
assume cs:codee
main:
	mov ah, 0FFh
	add ah, 1  ; ah = 00h, c = 1
	add ah, 2  ; ah = 02h, c = 0
	sub ah, 3
	mov ah, 4Ch
	int 21h
code ends
end main
```

- 移位操作最后移出去的一位，也会保存到 CF 中

```asm
mov ah, 10110110B
shr ah, 2  ; CF = 1
mov ah, 10110110B
shl ah, 1  ; CF = 1
```

### 5.1.1 与 CF 相关的指令

| `jc`  | `jnc` | `adc` | `clc`    | `stc`    |
| ----- | ----- | ----- | -------- | -------- |
| 有进位跳转 | 无进位跳转 | 带进位加法 | `CF = 0` | `CF = 1` |

`adc ax, bx  ; ax = ax + bx + CF`

```asm title="16 位转二进制输出"
code segment
assume cs:code
main:
	mov ax, 1234h
	mov cx, 16  ; 一般用 cx 来计数
next:
	shl ax, 1
	jc is_1
is_0:
	mov dl, '0'
	jmp output
is_1:
	mov dl, '1'
output:
	mov ah, 2
	int 21h
	sub cx, 1
	jnz next
	mov ah, 4Ch
	int 21h
code ends
end main
```

```asm title="16 位转二进制输出 (advanced)" hl=7,8,9
code segment
assume cs:code
main:
	mov bx, 1234h
	mov cx, 16  ; 一般用 cx 来计数
next:
	shl bx, 1
	mov dl, '0'
	adc dl, 0
output:
	mov ah, 2
	int 1h
	sub cx, 1
	jnz next
	mov ah, 4Ch
	int 21h
code ends
end main
```

> [!warning] Attention
> `mov` 不会改变任何标志，`push` `pop` 也不会改变任何标志

## 5.2 Zero Flag 零标志

```asm
sub ax, ax  ; AX=0, ZF=1, CF=0
add ax, 1  ; AX=1, ZF=0, CF=0
add ax, 0FFFh  ; AX=0, ZF=1, CF=1
jz is_zero  ; 会发生跳转
cmp ax, ax
je next  ; 也会发生跳转
```

- `jz/je` 在 `ZF=1` 的时候跳转，本质上是相同的
- `jnz/jne` 是相反的指令
- 使用 `jz` 还是 `je`，需要在对应的语境下选择

## 5.3 Sign Flag 符号标志

- 每次都保存运算结果的最高位

```asm
mov ah, 7Fh
add ah, 1  ; AH=80h=1000 0000B, SF=1
sub ah, 1  ; AH=7FH=0111 1111B, SF=0
```

- `js` 符号跳转，`SF==1` 则跳转
- `jns` `SF==0` 则跳转

## 5.4 Overflow Flag 溢出标志

> 有符号数加法溢出
> CF 相当于无符号数加法溢出标志

```asm
mov ah, 7Fh
add ah, 1  ; AH=80h, OF=1, ZF=0, CF=0, SF=1
		   ; 127 + 1 = -128, overflow
mov ah, 80h
add ah, 0FFh  ; AH=7Fh, OF=1, ZF=0, CF=1, SF=0
			  ; -128 + -1 = 127，overflow
add ah, 80h
sub ah, 1  ; AH=7Fh, OF=1, ZF=0, CF=0, SF=0
		   ; -128 - 1 = 127, overflow
```

- 正负相加永不溢出
- `jo` 溢出跳转，`jno` 不溢出跳转

## 5.5 Parity Flag 奇偶校验位

```asm
mov ah, 4
add ah, 1  ; AH=00000101B, PF=1 表示有偶数个 1，但只统计结果的低八位
mov ax, 0101h
add ax, 0004h  ; AX=0105h=0000 0001 0000 0101B
			   ; PF 只统计第八位的 1 的个数
```

- `PF=1` 表示结果的**低八位**中有偶数个 1
- `jp/jpe` 如果 parity even 跳转
- `jnp/jpo` 如果 pairty odd 跳转

> [!note] Note
> 标准 ASCII 码只有 7 位，多出的第八位就是奇偶校验位；而扩展 ASCII 码没有

## 5.6 Auxiliary Flag 辅助进位标志

> 第三位向第四位产生进位或借位

```asm
mov ah, 1Fh  ; 0001 1111
add ah, 01h  ; 0000 0001
			 ; ah=20h, AF=1
```

AF 和 BCD 码有关，用 16 进制表示十进制数

```asm
mov al, 29h  ; 分钟 29h=0010 1001
add al, 08h  ; 过了 8 分钟
			 ; 31h
```

- `daa` 指令 (decimal adjust for addition) 加法的十进制调整
	- `if AF == 1 or (AL & 0Fh) > 9: AL += 6`

```asm
mov al, 29h
add al, 02h  ; AL=2Hb, AF=0
daa  ; AL=AL+6=31h
```

## 5.7 Direction Flag

### 5.7.1 字符串复制的方向

| 1000 | 1001 | 1002 | 1003 | 1004 | 1005 | 1006 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| A    | B    | C    | D    | E    |      |      |

| 1000 | 1001 | 1002 | 1003 | 1004 | 1005 | 1006 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| A    | B    | A    | B    | C    | D    | E    |

要将字符串复制到以 1002 位首地址的位置，此时 **源首地址<目标首地址**，复制应该按**反方向**，地址从大到小。否则会导致还没遍历到的原始数据被覆写：

| 1000 | 1001 | 1002 | 1003 | 1004 | 1005 | 1006 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| A    | B    | A    | B    | A    | B    | A    |

- 源首地址<目标首地址：反方向
- 源首地址>目标首地址：正方向

### 5.7.2 Example: 正方向复制

| 1000 | 1001 | 1002 | 1003 | 1004 | 1005 | 1006 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
|      |      | A    | B    | C    | D    | E    |

```asm
; ds, si 表示源指针，构成 ds:si
; es, di 表示目标指针，构成 es:di
; cx 作为字节计数器

; ds=2000h, si=1002h, es=2000h, di=1000h, cx=5
cld  ; DF=0, clear direction flag, 表示正方向
rep movsb  ; 把 ds:si 指向的
```

> [!tip] 细节
> - 首先将 A 复制到 1000
> - 然后 `cx--`, `si++`, `di++`
> - 继续进行，直到 `cx == 0`
> ```c title="rev movsb in C"
>while (cx != 0) {
>	byte ptr es:[di] = byte ptr ds:[si];
>	cx--;
>	if (df == 0) {
>		di++;
>		si++;
>	} else {
>		di--;
>		si--;
>	}
>} 
>```

> [!note] Note
> - `si` source index 源偏移地址
> - `di` destination index 目标偏移地址

### 5.7.3 Example: 反方向复制

| 1000 | 1001 | 1002 | 1003 | 1004 | 1005 | 1006 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| A    | B    | C    | D    | E    |      |      |

```asm
; ds=2000h, si=1004h, es=2000h, di=1006h, cx=5
std  ; DF=1, set direction flag, 表示反方向
rep movsb
```

> [!tip] 细节
> - 这里的 `si, di` 都是从末尾开始的，只要反方向复制，一开始的传入值都应该是末地址
> - 每次都是 `si--, di--, cx--`，其他同理

## 5.8 Interrupt Flag 中断标志

- `IF=1` 允许硬件中断，`cli` 置零
- `IF=0` 禁止硬件中断，`sti` 置一

> [!note] Note
> - `mov ah, 1; int 21h` 是函数调用，软件中断，代码在**显式地**用 `int n` 的形式调用函数集的函数

> [!question] 什么是硬件中断
> ```asm title="example: add 1 to 100"
> mov ax, 0  ; 此时用户敲键盘
> ;; int 9h ;; CPU 插入并执行键盘中断
> mov bx, 1
> next:
> add ax, bx  ; 发生时钟中断
> ;; int 8h ;; CPU 插入并执行时钟中断
> add bx, 1
> cmp bx, 100
> jle next
> ```
> - 键盘中断：假如用户在执行上面程序时敲键盘，此时 CPU 必须暂停并处理本次键盘输入：将键盘输入编码保存到系统中的键盘缓冲区队列，`int 9h` 会返回原来的指令
> - 时钟中断：约每 55 ms 会在下一条指令前插入一个时钟中断 `int 8h`，将操作系统内部的一个计数器 +1

- 软件中断是显式的 *explicit*
- 硬件中断是隐式的 *implicit*

### 5.8.1 example: 修改函数指针时的保护操作

```asm title="IF example"
cli
mov word ptr es:[bx], offset int_9h
mov es:[bx+2], cs
sti
```

这样能保证 `int 9h` 不会在地址改了一半的时候被硬件调用，从而产生错误

## 5.9 Trap Flag 陷阱标志

- `TF=1` 时，CPU 进入单步模式 (single-step mode)，每执行一条指令，就会插入一个 `int 1h` 中断
- `int 1h` 是未定义的，调试器会自定义一个 `int 1h` 的中断函数
	- 调试器 jmp 到被调试程序，被调试程序取得控制权
	- 被调试程序进行一步，调用 `int 1h` 返回调试器
	- *调试器可以观察被调试程序的寄存器状态和当前正在执行的命令等*

```asm title="set TF"
pushf  ; 相当于 push FL，但是 FL 是不能直接引用的
pop ax  ; AX=FL
or ax, 100h  ; 第 8 为置 1，0000 0001 0000 0000
push ax
popf  ; pop FL 即 FL=AX, TF=1
```

```asm title="clear TF"
pushf  ; 相当于 push FL，但是 FL 是不能直接引用的
pop ax  ; AX=FL
and ax, 0FEFFh  ; 第 8 为置 0，1111 1110 1111 1111
				; 或者使用 and ax, not 100h
push ax
popf  ; pop FL 即 FL=AX, TF=0
```

> [!question] 如果我要做一个调试器？
> - 编写断点 `int 1h` 程序
> - 翻译指令，断行并显示汇编代码
> - 等待用户输入

### 5.9.1 `int 1h` 函数的定义

```txt
0:4 78h
0:5 56h
0:6 34h
0:7 12h
```

那么 `int 1h` 的函数首地址（函数指针）为 `1234h:5678h`

> [!tip] Tip
> `int n` 函数的指针，一定保存在 `0:n*4` 处，这是因为每个函数指针都需要占用 4 个字节
> `int 21h` 一定存放在 `0:84h` 处

### 5.9.2 example: antidbg

```asm title="antidbg"
code segment
assume cs:code, ds:code
main:
	jmp begin
old1h dw 0, 0
prev_addr dw offset first, code  ; 前条指令的地址
begin: 
	push cs
	pop ds  ; DS=CS
	xor ax, ax  ; AX=0
	mov es, ax  ; ES=AX=0
	mov bx, 4  ; bx=4
	push es:[bx]  ; 0:[4]
	pop old1h[0]  ;  保存偏移地址
	push es:[bx+2]  ; 0:[6]
	pop old1h[2]  ; 保存段地址
	mov word ptr es:[bx], offset int1h  ; 存入新的偏移地址
	mov word ptr es:[bx+2], cs  ; 存入新的段地址，或者使用 seg int1h
	pushf  ; save old FL
	pushf
	pop ax
	or ax, 100h  ; 1 0000 0000 set TF
	push ax
	popf; TF=1
first:
	nop  ; 当某条指令执行前TF==1,则该条指令执行后会
		; 自动执行int 01h单步中断
single_step_begin:
...
```

> 在执行的时候替换了 `int 1h` 的函数指针，所以更改了单步模式下调用的程序

## 5.10 `pushf, popf`

> 专门执行 `FL` 的堆栈操作

```asm title="设置 TF=1，进入单步运行模式"
pushf
pop ax
or ax, 100h  ; 0000 0001 0000 0000
; and ax, not 100h  ; 清零
push ax
popf
```

