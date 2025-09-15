---
status:
  - archived
tags: CS/Language/Assembly/80x86
date_created: 2024-12-18T13:28:42
date_modified: 2025-09-13T10:18:05
---

# 1 堆栈段的定义

## 定义和简单操作

```asm title="example: 段的定义"
data segment
    abc dw 1234h, 5678h
data ends

code segment
assume cs:code, ds:data, ss:stk
main:
	mov ax, data
	mov ds, ax
	push abc[0]  ; 相当于 push 1234h
	pop abc[2]
	mov ah, 4C
	int 21h
code ends
end main

stk segment stack  ; 定义堆栈段，堆栈段只能定义一个
	a db 200h dup('S')  ; 或写成 dw 100h dup(0)，这里设置成 S 方便调试的时候发现
stk ends  ; 程序刚开始运行时，ss = stk，sp = 200h
```

> [!attention]
> 堆栈段的定义必须要加 `stack` 修饰

> [!hint] `push` 操作拆解
> - 假设此时 `ss = 1000h`，`sp=200h`
> - 执行 `sp = sp - 2`，于是 `ss:sp = 1000:1FE`
> - 执行 `word ptr ss:[sp] = abc[0]` 注意小端规则：
> ```
> 1000:1FE 34h  <ss:sp
> 1000:1FE 12h
> 1000:200 ???
> ```

> [!hint] `pop` 操作拆解
> - 假设刚刚执行了上面的 `push`
> - 执行 `abc[2] = word ptr ss:[sp]`
> - 执行 `sp = sp + 2`

> [!example] 补充
> - 无法进行 8 位的栈操作
> - 如果没有定义堆栈段？
> 	- `ds = es = 568D, ss = 569D, sp = 0000`，也就是 **`ss` 的初始值等于首段的段地址**
> 	- 如果有 `push`，那么 `sp = sp - 2 = FFFE`
> - 堆栈只能有一个

> [!note]- dword 的堆栈操作
>
> ```
> ; ss = 1000h, sp = 200h
> mov eax, 12345678h
> push eax
> pop ebx
> ```
>
> > [!hint] 操作拆解
> > - `sp = sp - 4`
> > - `dword ptr ss:[sp] = 12345678h`
> > ```l
> > 1000:1FC  78h  <ss:sp
> > 1000:1FD  56h
> > 1000:1FE  34h
> > 1000:1FF  12h
> >```
> > - `ebx = dword ptr ss:[sp]`
> > - `sp = sp + 4`

## 1.1 如果没有定义堆栈段？

```txt title="进行一次 push 后"
569D:0000           data; len=10h
569D:0010=569E:0000 code; len=20h
569D:0030=56A0:0000 后续段
......
569D:FFFE           <ss:sp
569D:FFFF
......
......
9000:FFFF

A000:0000 ~ A000:FFFF  ; 显卡地址
B000:0000 ~ B000:7FFF  ; 显卡地址
B800:0000 ~ B800:7FFF  ; 显卡地址
C000:0000 ~ F000:FFFF  ; ROM 映射，只读
```

> [!important]
> - DOS 系统是单任务的，所以一整块内存都是可用的，一直到 `9000:FFFF` 都是这个程序可用的空间
> - `A000:0000` 前面一共有 640k，其中包含了 DOS 系统的内存

## 1.2 调试中的表现

```
569D:0000  34 12 00 00 00 00 00 00  <data segment: 569D:0000 - 569D:0004
569D:0008  00 00 00 00 00 00 00 00
568D:0010  B8 9D 56 8E D8 FF 36 00  <code segment: 569E:0000 -
```

此时 `ds 569D` `cs 569E`

> [!question] `data` 段之后应该就是 `code` 段吗？
> **并不是**，只有能够整除 `0010` 的地址才能作为段地址的开始，所以 `569D:0010` 才是 `code` 段的开始

> [!question] 段首地址的偏移地址不应该是 `0000` 吗
> 可以让 `code` 的首地址偏移为 `0000`，只需要让 `cs = 569E` 即可，这就相当于 `569D:0010 == 569E:0000`，这样

```
ds:0220 53 53 53 53 53 53 53 53
ds:0228 53 53 53 53 53 53 00 00
ds:0230 ?? ?? ?? ?? ?? ?? ?? ??  <ss:sp = 56A0:01FE = 569D:0230 = ds:0230 = 56A0:
```

> [!question] 为什么最后面有的 `S` 被覆盖掉了？
> - td 在载入的时候可能会调用程序里定义的堆栈，于是就会出现乱码
> - 不仅如此，如果程序里使用了 `pop`，调试的时候也可能被同时使用同一个堆栈的其他程序覆盖掉（如调试器），**堆栈指针前方的内容是不安全的**

# 3 寄存器初始化赋值和 `psp` 段

程序载入内存时，dos 会对以下寄存器做初始化赋值

| `ss:sp`           | `cs:ip`                   | `ds`     | `es`     |
| ----------------- | ------------------------- | -------- | -------- |
| `ss=stk, sp=堆栈长度` | `cs=code, ip=offset main` | `ds=psp` | `es=psp` |

> [!NOTE] `psp`
> - `psp` 是程序段前缀 (program segment prefix)，是一块长度为 100h 字节的内存，并且一定位于程序首段的前方
> - `psp` 是操作系统定义的，储存了与当前进程相关的一些信息，例如命令行参数
> - 初始都赋值成 `psp`，方便访问 `psp` 里的内容
> ```text
>mov ax, data
>mov ds, ax
>; 等价于
>mov ax, ds
>add ax, 10h
>mov ax, ds 
>```

> [!attention]
> `ip` 的位置由 `end X` 决定，`ip` 会被赋值成 `X` label 的位移地址，所以 `end` 其实指定了程序的入口

## 3.1 调试观察 `psp` 段表现

```shell
ss 123 456 abc
```

```
ds:0080  0C 20 31 32 33 20 34 35  ? 123 45
ds:0088  36 20 61 62 63 0D 00 FF  6 abc???
```

> [!note] 内容解读
> 第一个 `0C` 是参数长度，也就是 12，即字符串 `" 123 456 abc"`

```asm
data1 segment
abc db 1, 2, 3
end data1

data2 segment
xyz db 4, 5, 6
end data2

code segment
assume cs:code, ds:data1, es:data2
main:
	mov ax, data1
	mov ds, ax
	mov ax, data2
	mov ds, ax
	mov ah, abc[1]  ; -> mov ah, ds:[abc+1] -> mov ah, ds:[0+1] -> mov ah, ds:[1]
	mov xyz[1], ah
```

`ds = 569D, es = 569E, cs = 569F`

```txt title="memory"
ds:0000  01 02 03 00 00 00 00 00  <ds
ds:0008  00 00 00 00 00 00 00 00
ds:0010  04 05 06 00 00 00 00 00  <es
```

# 4 段地址的隐含和覆盖

## 4.1 段地址的隐含

```asm title="段地址的隐含"
; 隐含了 ds:
mov ax, [bx]
mov ax, [si]
mov ax, [di+2]
mov ax, [bx+di+2]
mov ax, [1000h]

; 隐含了 ss:
; 只要 [] 中有 bp，默认的段地址就是 ss
mov ax, [bp]
mov ax, [bp+2]
mov ax, [bp+si+2]
```

> [!attention] 堆栈段的引用
> - `ss:[sp]` 是语法错误的，因为 `sp` 不能放在方括号里
> - 使用 `bp` 来进行直接的堆栈段的引用

## 4.2 段覆盖

> 就是在操作数前添加一个段前缀来改变默认的 `ds`

```asm title="segment override"
mov bx, sp
mov ax, ss:[bx]
```
