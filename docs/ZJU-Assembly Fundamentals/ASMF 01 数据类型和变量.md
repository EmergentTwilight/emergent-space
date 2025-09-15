---
status:
  - archived
tags: CS/Language/Assembly/80x86
date_created: 2024-12-17T20:39:11
date_modified: 2025-09-13T10:18:05
---

# 1 汇编语言中的数据类型

| type   | db     | dw (word)   | dd (double words) | dq (quadruple words)          | dt (ten bytes) |
| ------ | ------ | ----------- | ----------------- | ----------------------------- | -------------- |
| bits   | 8      | 16          | 32                | 64                            | 80             |
| c type | `char` | `short int` | `long int, float` | `long long (__int64), double` | `long double`  |
| printf |        |             |                   | `%lld, %llx`                  | `%Lf`          |

> [!NOTE]
> - 8086 中的 word 指的是 **2 bytes, 16 bits**
> - RISC-V 中的 word 一般指的是 **4bytes, 32bits**

```asm title="进行几个变量声明"
x dd 12345678h
y dd 3.14159
a dq 1234567887654321h
b dq 3.14159265
```

# 2 例程：变量的操作

```asm title="变量的简单操作" hl=2
.386  ; 告诉编译器将使用 32 位的CPU，允许使用 32 位寄存器
data segment use16  ; 表示段内变量的偏移地址仍旧是 16 位，因为 dos 环境只允许使用 16 位的偏移地址
	s db 01h, 02h, 03h, 04h  ; s 是一个数组，相当于 char s[4] = {1,2,3,4}，汇编语言中当初始值超过 1 就是数组
	t dw 89ABh, CDEFh  ; t 是一个数组，但是第一项是 t[0]，第二项却是 t[2]
	abc dw 1234h
	xyz dw 5678h
	ddd dd 12345678h
	eee dd 0
data ends

code segment use16
assume cs:code, ds:data
main:
	mov ax, seg abc
	mov ds, ax

	mov ax, t[2]  ; 或写成 mov ax, [t+2]
	mov abc, ax

	; mov eax, abc  ; 不等宽 32 != 16
	mov eax, dword ptr abc
	
	; add abc, xyz  ; ERROR: 不可以两个都是变量
	add abc, 5678h  ; 正确的写法
	mov ax, xyz  ; 或者先放到寄存器里
	add abc, ax  ; 正确的写法
	
	mov eax, ddd
	mov eee, eax
	
	; mov al, ddd  ; 编译报错，因为两个参数不等宽
	mov al, byte ptr ddd  ; byte ptr 相当于强制类型转化 (char*)
	
	; mov ax, s  ; 编译语法错误，不等宽
	mov ax, word ptr s  ; ax = {s[1],s[0]}
	mov abc, ax
	
	mov ah, 4Ch
	mov al, 0  ; 返回码
	int 21h  ;  exit()

code ends
end main
```

## 2.1 ERROR 和正确写法的区别？

- 一条指令中的两个参数，**最多只能有一个是内存变量**
- 另一个可以是寄存器或者**常数**
- 无法实现两个内存变量直接运算可能是因为硬件限制

## 2.2 变量的地址表示

- `段地址:[偏移地址]` 用来表示某个地址指向的量，等价于 C 语言中的 `a[3]` 或 `*(a+3)`
- 可以在 td 中看到类似 `mov    eax [0004]` 的代码，其实这里**省略了 `ds:`**

## 2.3 Little Endian 规则

8086 使用小端规则，所以在 td 中会发现 `12345678h` 变成了 `78563412`，也就是 LSD 78 被放在了内存地址最小的位置。

举例来说，假定 `a` 的地址是 1000，则 `a` 的值以以下格式存放：

| Addr  | Little Endian | Big Endian |
| ----- | ------------- | ---------- |
| +1000 | `0x78`        | `0x12`     |
| +1001 | `0x56`        | `0x34`     |
| +1002 | `0x34`        | `0x56`     |
| +1003 | `0x12`        | `0x78`     |

> [!hint] 为什么小端更好
> 如果只要取 `a` 的最低字节，那么只需要访问 `a` 原本的地址，方便编译

注意，数据窗口中显示的是 `78563412h`，但是寄存器窗口中会是正常的 `12345678h`。

## 2.4 编程中的变量对齐

- 在进行 `mov eax, ddd` 时，由于 `eax` 是 32 位的，所以 CPU 也会从 `ddd` 的地址处开始读 4 个 byte
	- 但这**要求 `ddd` 确实是 `dq` 类型**，否则编译器会报错
- 使用**强制类型转换**可以允许非对齐
	- `mov al, byte ptr ddd` 相当于 `al = *(char *)(ds:0004)`

| 3 种 ptr 修饰 | byte ptr | word ptr | dword ptr |
| ---------- | -------- | -------- | --------- |
| bytes      | 1        | 2        | 4         |

> [!attention]
> - ptr 宽度修饰不能用于常数
> - 变量在定义的时候已经声明了类型，编译器会自动加上修饰，所以不用加
> 但如果不是通过变量引用的方式来引用变量（即代码中没有出现变量名），还是需要加上修饰

## 2.5 数组和元素合并

```asm
s db 01h, 02h, 03h, 04h  ; char s[4] = {1, 2, 3, 4}
```

此时，`s` 是一个数组，其大小为 4 字节。可以用 `word ptr` 来读取 `s`，但要**注意 Little Endian**，读出的 word 是 **`0201h`**。这样读取，相当于进行了合并。

同样的，如果进行 `mov eax, dword ptr abc`，实际上读取了内存中**连续的** `{xyz, abc}`。

### 2.5.1 特殊情况

```asm
t dw 89ABh, CDEFh
```

把 `t` 中各个元素逐字节按小端展开：

```txt
t+0 AB
t+1 89
t+2 EF
t+3 CD
```

所以，为了取第二个元素，实际上需要取 `t[2]`

> [!attention] 指针偏移操作与 C 语言的不同
> - C 语言中 `ptr+1`，不一定真的是 `+1`，而是位移了一个数组元素的大小
> - 汇编中 `ptr+1`，就是位移一个字节

# 3 符号扩充

> 将一个宽度较小的变量赋值给一个宽度较大的变量时，会发生扩充

- 零扩充：将空位用 0 补全
- 符号扩充：将空位用最高位 sign extend 补全

# 4 HW：思考题

C 语言中是否有可能将数组某个元素的后一半和下一个的前一半结合在一起

```c title="Reassembling data"
#include <stdio.h>

int main() {
	short int a[3] = {0x1234, 0x5678, 0xabcd}, y;
	     			  // 34, 12, 78, 56, cd, ab
	y = *(short int *)((char*)&a[0] + 1);  // 相当于按照字节寻址
	print("%x", y);
}
```

```txt title="output"
7812
```
