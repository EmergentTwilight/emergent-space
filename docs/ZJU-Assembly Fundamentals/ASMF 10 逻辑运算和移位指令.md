---
status:
  - archived
tags: CS/Language/Assembly/80x86
date_created: 2024-12-17T20:39:11
date_modified: 2025-09-13T10:18:06
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
---

# 1 逻辑运算

| 指令   | `and` | `or` | `xor` | `not` | `test`       |
| ---- | ----- | ---- | ----- | ----- | ------------ |
| C 算符 | `&`   | `\|` | `^`   | `~`   |              |
| 解释   |       |      |       |       | 不保留结果的 `and` |

## 1.1 `test` 运算

> [!note] Note
> - 相当于进行一个 `AND` 运算，结果不会保留但会影响 flag
> - `test` 与 `and` 的关系相当于 `cmp` 和 `sub` 的关系

```asm title="test"
mov ax, 1234h
test ax, 8000h  ; ZF = 0, AX = 1234h
```

# 2 移位运算

| 指令   | `shl` | `shr` | `rol`     | `ror`     | `sal` | `sar` | `rcl`    | `rcr`    |
| ---- | ----- | ----- | --------- | --------- | ----- | ----- | -------- | -------- |
| C 算符 | `<<`  | `>>`  | `_rotl()` | `_rotr()` |       |       |          |          |
| 解释   |       |       | 循环左移      | 循环右移      | 算数左移  | 算数右移  | 带进位的逻辑左移 | 带进位的逻辑右移 |

## 2.1 循环移位指令 `rol, ror`

> [!note] 移位与 `CF` 的关系
> > [!warning] Warning
> > `CF` 里保留的一定是**最后移出去的一位**，不论是什么移位指令
>
> ```asm title="shift - CF"
> mov ah, 0EFh  ; 1110 1111, CF = ?
> ror ah, 1  ;    1111 0111, CF = 1
> ```

```asm title="printf()" hl=15,29
.386
data segment use16
abc dd 2147483647
data ends

code segment use16
assume cs:code, ds:data
main:
	mov ax, seg abc
	mov ds, ax
	mov eax, abc  ; 复习：编译后编程 mov eax, ds:[0]，所以前面要先赋值
	mov cx, 8
again:
	rol eax, 4
	push eax  ; 为了暂时保护 eax 的值，保存到栈中
	and eax, 0Fh  ; 这时 and 运算清除了 eax 前面部分的内容
	cmp al, 10
	jb is_digit
is_alpha:  // 16进制中的字母也可以打印
	sub al, 10
	add al, 'A'
	jmp finish_4bits
is_digit:
	add al, '0'
finish_4bits:
	mov ah, 2
	mov dl, al
	int 21h
	pop eax  ; 表示从栈中恢复上次 push 时 eax 的值
	sub cx, 1
	jnz again  ; jump if not zero
	mov ah, 4Ch
	int 21h
code ends
end main
```

> 使用 `rol` 指令，将 32-bit 数输出成 16 进制的格式

## 2.2 算数移位指令 `sal, sar`

- `sal` 算数左移，其实等价于 `shl`
- `sar` 算数右移，**不等于** `shr`，因为有符号问题

```asm title="arithmetic shift"
mov ah, 0FEh  ; 1111 1110 = -2
sar ah, 1  ;    1111 1111 = -1

mov ah, 0FEh  ; 1111 1110 = 254
shr ah, 1  ;    0111 1111 = 124
```

## 2.3 进位循环位移指令 `rcl, rcr`

- `rcl` 带进位循环左移
- `rcr` 带进位循环右移
- 每次移入 `CF`，移出的到 `CF`

```asm title="shift 1234ABCDh left 3 bit without 32-bit reg"
; method 1
mov ax, 0ABCDh
mov dx, 1234h
shl dx, 3
mov bx, ax
shl ax, 3
shr bx, 13
or dx, bx

; method 2 with rcl
mov ax, 0ABCDh
mov dx, 1234h
mov cx, 3
next:
	shl ax, 1  ; 移到 CF
	rcl dx, 1  ; CF 会补 DX 右侧的空洞
	dec cx
	jnq next
```
