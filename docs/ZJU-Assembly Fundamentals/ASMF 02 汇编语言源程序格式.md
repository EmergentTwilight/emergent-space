---
MkDocs_comments: true
date_created: 2024-12-17 21:07:15
date_modified: 2025-01-25 16:26:31
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
state:
- 待发布
- 归档
tags: Programming-Language/Assembly/80x86
type:
- note
---
# 1 位汇编语言语法基础

```asm title="1+2+3+4+...+100=?"
.386
.model flat, stdcall
option casemap :none

include include\windows.inc
include include\kernel32.inc
include include\user32.inc

; 操作系统相关函数
includelib lib\kernel32.lib
includelib lib\user32.lib

.data
result db 100 dup(0); dup:duplicate重复
; char result[100]={0};
format db "%d",0; db:define byte字节类型
; char format[3]="%d";
prompt db "The result",0

.code
main:         ; 标号
    mov eax, 0; eax:extended ax
    mov ebx, 1
again: 
    add eax, ebx; eax=0+1+2+3
    add ebx, 1  ; ebx=4
    cmp ebx, 100; cmp:compare
    jbe again   ; jbe:jump if below or equal
    
	invoke wsprintf, offset result, offset format, eax
	invoke MessageBox,0,offset result,offset prompt,0
	    ret
end main; 指定程序的起始执行点
        ; end后面的标号决定了程序刚开始
        ; 运行时的eip的值。
```

## 1.1 标号

- `again:` 是一个标号，标号是名称 + 冒号
- 可以作为跳转指令的目标地址，如 `jbe again`，*有点像 goto*
- 可以作为函数调用 call 的地址

## 1.2 函数调用

> 汇编语言也需要调用函数，不过更多调用的是操作系统 API

```asm
invoke wsprintf, offset result, offset format, eax
```

就是 `wsprintf(&result[0], &format[0], eax);`，这是 windows 的一个函数，对应 c 语言中的 `sprintf(result, "%d", eax);`

```asm
invoke MessageBoxA, 0, offset result, offset prompt, 0
```

也就是 `MessageBoxA(0, &result[0], &prompt[0], 0);`，这是一个 windows 函数，实现了一个系统弹窗
- `var1`: 建的消息框的所有者窗口的句柄
- `result`: 这里是将会显示的消息文本
- `prompt`: 这里是窗口的标题
- `var4`: 这里是对会话框按钮的样式

## 1.3 变量定义

```asm
.data
result db 100 dup(0);  dup: duplicate 重复
; char result[100] = {0};
format db "%d", 0;  db: define byte 字节类型
; char format[3] = "%d";
prompt db "The result", 0
```

> [!attention]
> 1. 汇编 string 不会自带 `\0`，需要自己加上一个 0
> 2. 这里定义的变量相当于 C 的全局变量，能被所有函数调用
> 	- 汇编也能定义局部变量，但是比较麻烦

## 1.4 程序结构

除了上述 `invoke` 的部分，都是直接让 CPU 执行的程序，没有调用操作系统的 API。但如果要实现输入输出，就一定要使用操作系统的函数。

为了获得尽可能大的用户权限，我们使用古老的 DOS 系统来学习汇编语言。

# 2 位汇编语言 Hello, world!

> DOS 的汇编语言是 16 位的
> Windows 和 Linux 的汇编语言是 32 位的

```asm title="16 bit asm hello world"
data segment
hello db "Hello, world!", 0Dh, 0Ah, '$'
data ends

code segment
assume cs:code, ds:data
main:
	mov ax, data
	mov ds, ax
	mov ah, 9
	mov dx, offset hello
	int 21h
	mov ah, 4Ch
	mov al, 0
	int 21h
code ends
end main
```

## 2.1 创建字符串变量

```asm title="创建字符串变量"
data segment
hello db "Hello, world!", 0Dh, 0Ah, '$'
; 0Dh 和 0Ah 是 16 进制常数，h 是 16 进制后缀
; 0Dh 代表回车的 ASCII 码，0Ah 代表换行
; '$' 有表示末尾的含义，在正则表达式中也是这个意思
data ends
```

### 2.1.1 换行 or 回车？

- `0Ah` 也就是 `\n`
	- 在 windows 和 dos 中，一个 enter 会产生两个字符 `0Dh 0Ah`
	- 在 Mac OS 和 Linux 中只有一个字符
- 在 C 语言中，使用 `"r"` 文本文件只读形式打开，`fgetc()` 读到一个 `0Dh` 时，会将后面的 `0Ah` 一起读入并合成 `0Ah`
	- 用 `"rb"` 可以每次只读一个字节
	- linux 中 `"r"` 和 `"rb"` 是完全一样的
- `0Dh` 表示回车 **光标回到行首**
- `0Ah` 表示换行 **光标垂直往下一行**

## 2.2 构建变量指针

```asm title="构建变量指针"
mov ax, data; 或写成 mov ax, seg hello
			; 这里的 seg 表示取 hello 的段地址
mov ds, ax; ds = data
		  ; 为什么不用一句话 mov ds, data 来达到目的？
		  ; 因为 ds 只能接受一个变量或寄存器给它赋值，而 data 刚好是常数
		  ; 凡是 s 结尾的寄存器都有这个问题
		  ; 这里的 data 代表 hello 的段地址
mov dx, offset hello; offset hello 表示取 hello 的偏移地址
					; 完成了对 ds 和 dx 的赋值，这样就构成了 ds:dx -> hello 这个指针
```

> [!NOTE] 
> 构建这个指针是为了满足函数调用的要求

## 2.3 调用操作系统函数

### 2.3.1 printf

```asm
mov ah, 9; ah = 9 用来指定要调用的子函数编号
int 21h; 调用 dos 系统函数集
```

- 相当于 C 语言的 `printf(hello)`
- `int 21h` 不是整数类型，而是 interrupt 中断调用，调用了编号为 `21h` 的函数集，而寄存器 `ah=9` 代表调用这个函数集中第 9 号函数

在 [中断大全](http://cc.zju.edu.cn/bhh/rbrown.htm) 中查找这个函数 [Int 21/AH=09h (zju.edu.cn)](http://cc.zju.edu.cn/bhh/intr/rb-2562.htm)

```txt title="调用准备"
AH = 09h
DS:DX -> '$'-terminated string
```

### 2.3.2 return

```asm
mov ah, 4Ch
mov al, 0
int 21h
```

- 参考 [Int 21/AH=4Ch (zju.edu.cn)](http://cc.zju.edu.cn/bhh/intr/rb-2974.htm)
- 相当于 C 语言的 `exit(0);`
- 这三条指令不能换成 `ret` 否则会死机；也不能删除这三条指令，否则 CPU 会继续后续代码（*别的程序遗留的垃圾程序*）导致死机

## 2.4 编译运行

安装好 masm 环境后，用下面的命令编译运行。

```shell title="DOS 命令行界面"
D:\MASM>masm hello
D:\MASM>link hello  // 无视 no stack segment 报错
D:\MASM>dir hello.exe  // 查找是否存在 hello.exe
D:\MASM>hello  // 运行 hello
Hello, world!
				// 有回车，所以输出两行
```

## 2.5 调试

```shell title="DOS 命令行界面"
td hello
```

- td 是 DOS 16 位汇编语言图形界面调试器
- `ctrl+G` 可以找到某个指针位置的内存
- 在 `window/user screen` 中可以回到命令行

# 3 Example: putchar 调用

参考 [Int 21/AH=02h (zju.edu.cn)](http://cc.zju.edu.cn/bhh/intr/rb-2554.htm)

```asm title="16 bit asm putchar"
data segment
a db "ABC"
s db "Hello$world!", 0Dh, 0Ah, 0
data ends

code segment
assume cs:code, ds:data
main:
	mov ax, seg a
	mov ds, ax
	mov bx, 0
next:
	mov dl, s[bx]; 编译后会变成 mov dl, ds:[3+bx]
				 ; 其中 ds 是 s 的段地址
				 ; 3 是 S 的偏移地址，这是因为 data segment 前面有三个字节不属于 s
	cmp dl, 0
	je exit
	mov ah, 2
	int 21h
	add bx, 1
	jmp next
exit:
	mov ah, 4Ch
	mov al, 0
	int 21h
code ends
end main
```

## 3.1 指针位置？

```c title="数组名内移"
#include <stdio.h>

int main() {
	char s[4] = "ABC";
	int i;
	for (i = 0; i < 3; i++) {
		putchar(0[s+i]);
	}
}
```

这里的 `0` 是一个空指针，后面的 `s+i` 也可以构成一个正确的位移

> [!hint] td 使用小贴士
> - 数据窗口 `ctrl+G` 加入地址可以快速找到内存的内容，如 `ds:dx`
> - 代码窗口 `ctrl+O` 可以回到当前执行的命令处
> - `F2` 设置一个断点，然后用 run 快速到达断点
> - window/user screen 或 `Alt+F5` 打开命令行观察
> - `exit` 关闭 dos 命令行窗口

# 4 Example: 实现 `gets()`

- 循环 + [`putchar()`](http://cc.zju.edu.cn/bhh/intr/rb-2552.htm) 实现

```asm title="读取字符串并转化为大写输出"
data segment
    s db 100 dup(0)
data ends

code segment
    assume cs:code, ds:data
    main:
        mov ax, seg s
        mov ds, ax
    ;;;;;;;;;; s = gets(); ;;;;;;;;;;
        mov bx, 0
    input:
        mov ah, 1
        int 21h;  al = getchar()
        cmp al, 0Dh;  if al == '\n'
        je input_done
        mov s[bx], al
        add bx, 1
        jmp input
    input_done:
        mov s[bx], 0;  s[bx] = '\0'

    ;;;;;;;;;; printf("%s", upperCase(s)); ;;;;;;;;;
    output:
        mov bx, 0
        mov dl, s[bx]
        cmp dl, 0
        je output_done
        cmp dl, 'a'
        jl not_lower_case
        cmp dl, 'z'
        jg not_lower_case
    is_lower_case:
        sub dl, 20h
    not_lower_case:
        mov ah, 2
        int 21h;  putchar(dl)
        add bx, 1
        jmp output
    output_done:
        mov ah, 4Ch
        int 21h
code ends
```

> [!hint] 
> 注意上面循环和分支的实现

# 5 HW

```asm title="Reversely putchar"
data segment
sth db 10h dup(0)
s db "abc123", 0
data ends

code segment
assume cs:code ds:data
main:
	mov ax, seg s
	mov ds, ax; 将 s 的段地址存到正确的寄存器中
	mov bx, 0; 这是一个 counter
	mov dx, offset s; 得到 s 的偏移地址并存到寄存器中，ds:dx->s

; find last '\0'
find_max:
	mov dl, s[bx]; 读取 s[bx]
	cmp dl, 0
	je pre_print
	add bx, 1
	jmp find_max

; edge case, s == "\0", so bx == 0, empty string
pre_print:
	mov dl, s[bx]
	mov ah, 2; indicate putchar func
	int 21h; call putchar func
	cmp bx, 0
	je exit
	sub bx, 1
	jmp print

exit:
	mov ah, 4Ch
	mov al, 0; indicate exit(0)
	int 21h; call exit(0)
code ends
endmain
```