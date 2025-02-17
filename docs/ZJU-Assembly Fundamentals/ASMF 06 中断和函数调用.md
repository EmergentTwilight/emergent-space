---
MkDocs_comments: true
date_created: 2024-12-03 20:03:56
date_modified: 2025-02-04 14:55:02
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
state:
- 待发布
- 归档
tags: Programming-Language/Assembly/80x86
type:
- note
---
# 1 中断

```asm title="div00"
code segment
assume code:cs
main:
	mov ax, 123h
	mov bl, 1
	div bl
	mov ah, 4Ch
	int 21h
code ends
end main
```

> [!note] Note
> - 上述代码会造成 `al` 溢出，操作系统输出 `Divide overflow`，如果使用调试器，会得到 `Divide by zero` 报错
> - 两次的输出不一样，是因为中断是可以定义的

## 1.1 修改中断

> 试图修改中断，实现溢出时自定义输出内容，并强制执行剩余指令

```asm title="DIV0" hl=42
data segment
old_00h dw 0, 0
data ends

code segment
assume cs:code, ds:data
main:
	mov ax, data
	mov ds, ax
	xor ax, ax
	mov es, ax  ; es=0
	mov ax, es:[0]
	mov dx, es:[2]
	mov old_00h[0], ax
	mov old_00h[2], dx  ; 保存旧的 00h
	
	mov word ptr es:[0], offset my_00h
	mov word ptr es:[2], cs  ; 修改中断向量为 cs:offset my_00h
	
	mov ax, 1234h
	mov bl, 00h
	; 运行到 divide，CPU 插入 int 00h，具体操作如下：
	; pushf
	; push cs  ; 下一条指令的段地址
	; push offset divide  ; 下一条指令的偏移地址
	; jmp dword ptr 0:[0]  ; far ptr 跳转
divide:
	div bl
next:
	mov ax, old_00h[0]
	mov dx, old_00h[2]
	mov es:[0], ax
	mov es:[2], dx  ; 恢复 int 00h
	
	mov ah, 4Ch
	int 21h

my_00h:
	;;;;; 修改下一条指令地址以跳过 div 指令 ;;;;;
	push bp  ; 保护 bp
	mov bp, sp  ; 因为 sp 不能出现在方括号内，要用 bp 替代
	add word ptr [bp+2], 2  ; 方括号里有 bp，默认是段地址是 ss
							; bp+2，跳过刚才 push 的 bp，修改下一条指令的偏移地址（offset divide）
						    ; +2 后相当于跳过了 div bl 这个 2 字节的指令，直接执行后面的指令
	
	pop bp
	
	;;;;; 自定义一种输出样式 ;;;;;
	push ax  ; 保护
	push dx  ; 保护
	mov ah, 2
	mov dl, 'D'
	int 21h  ; 屏幕上输出一个字母 D
	pop dx
	pop ax
	iret  ; 中断返回
		  ; CPU 执行 iret 时执行以下命令，而执行 ret 只会 pop ip
		  ; pop ip  ; 载入了修改后的指令地址
		  ; pop cs
		  ; popf
code ends
end main
```

假设 `div` 指令发生时，`ss=1000h, sp=2000h`，那么在执行 `add word ptr [bp+2], 2` 时堆栈中的状态如下：

```txt
ss:1FF8    old bp <- bp (ss)
ss:1FFA    offset divide (ip)
ss:1FFC    CS
ss:2000    FL
```

> [!attention]
> 一定要保证**堆栈平衡**！

## 1.2 

```asm
mov ah, 1
int 21h  ; pushf
		 ; push cs
		 ; push offset next  ; 将下一个 cs:ip 入栈
		 ; IF = 0  ; 进入 int 21h 函数后，禁止中断
		 ; TF = 0  ; 进入 int 21h 函数后，临时恢复正常模式
		 ; jmp dword ptr 0:[84h]  ; 中断向量，0:[4*n]
```

> [!note] Note
> - 因为是远跳转，所以需要 `push cs:(next ip)`
> - `pushf` 方便返回之后恢复原样

```asm

```

# 2 函数调用

- 当 `call` 执行时，CPU 会 `push` 下一条指令的地址，即
	- `push offset next`
	- `jmp f`
- 当 `ret` 执行时，CPU 会 `pop` 得到返回地址，即
	- `pop ip`

> [!NOTE] 函数返回与中断调用与返回的不同之处
> - 调用
> 	- 函数使用 `call f`
> 		- 根据 label 寻址
> 		- 只 `push` 返回地址
> 		- `push next_ip; jmp f`
> 	- 中断使用 `int n`
> 		- 根据内存中中断函数地址寻址
> 		- `push` 了 `FL, CS` 和返回地址
> 		- `pushf; push cs; push next_ip; jmp dword ptr 0:[4*n]`
> - 返回
> 	- 函数使用 `ret`
> 		- `pop ip` 然后自动就回到了原本应当执行的下一条指令
> 	- 中断使用 `iret`
> 		- `pop ip; pop cs; popf` 因为是一起执行的，所以不用考虑 `ip` 被 `pop` 之后就无法执行后面两个 `pop`

## 2.1 三种参数传递形式

### 2.1.1 寄存器传递

```asm title="寄存器传递"
f:
	add ax, ax
	ret
main:
	mov ax, 3
	call f
next:
	mov ah, 4Ch
	int 21h
```

### 2.1.2 变量传递

```asm title="变量传递"
f:
	mov ax, var
	add ax, ax
	ret
main:
	mov var, 3
	call f
```

- con: 无法支持多线程

### 2.1.3 堆栈传递

```asm title="堆栈传递"
f:
	push bp
	mov bp, sp
	mov ax, [bp+4]
	add ax, ax
	pop bp
	ret
main:
	mov ax, 3
	push ax
	call f
	add sp, 2
```

### 2.1.4 Example: 实现加法函数

```asm title="func add"
func_add:
	push bp  ; 保护 bp
	mov bp, sp  ; 因为 sp 不能放在方括号里面
	mov ax, [bp+4]  ; 这是因为，需要越过刚才 push 的 bp 和 call 压入的返回地址
	add ax, [bp+6]
	pop bp
	ret
main:
	mov ax, 3
	push ax
	mov ax, 2
	push ax
	call f
	add sp, 4  ; 维持堆栈平衡
```

## 2.2 `call, ret` 指令和函数调用操作

> [!note] 复习参数传递
> - 寄存器传递 （复习计组，RISC-V 首选寄存器传递，放不下才用栈）
> - 全局变量传递
> - 堆栈传递

> [!note] 参数的顺序
> 形如 `f(2, 3)`，参数的代入顺序是从右到左的，先 3 后 2 连续 `push` 两次

```asm title="function add"
f:  ; 假设栈顶两个 word 是输入
	push bp  ; 用前保护
	mov bp, sp  ; 这是因为，方括号内只能用 bp
	mov ax, [bp+4]  ; ax = a
	add ax, [bp+6]  ; ax += b
	pop bp  ; 恢复 bp
	ret
main:
	mov ax, 3
	push ax
	mov ax, 2
	push ax
	; 16 位不能直接 push 3, push 2
	; 32 位才能这样用
	call f
here:
	add sp, 4  ; 堆栈平衡，当然可以用 pop，但是需要拿一个寄存器来做垃圾桶，不如直接恢复栈指针方便
```

> [!note] `call` 与 `jmp` 的不同之处
> 在上述代码中，`call f` 同时会 `push offset here`

> [!note] 返回值传递
> 一般会把 16 位函数返回值放在 `ax` 中，如果 32 位用 `eax` 最简单

```txt title="stack"
ss:1FF8  old bp
ss:1FFA  here
ss:1FFC  2
ss:1FFE  3
ss:2000
```

> [!question] 为什么不用 `int f(static int para)` ？
> 一般来说 `static int` 都是定义在 `data` 段内的，例如 `static int c ==> c dw`，不在堆栈里，但函数的参数使用堆栈传递
> - **静态变量**和**全局变量**都相当于在 `data` 段内定义的变量，其地址是固定不变的
> - **动态变量**（包括**形式参数**）一定存在于**堆栈**中，是动态诞生和死亡的，地址可能发生变化

> [!note] 其他调用方式
> - Pascal 语言
> 	- `push` 顺序：从左到右
> 	- 参数由 callee 释放，`ret 4` 相当于同时执行了 `pop ip; add sp, 4`
> - stdcall: windows api
> 	- `push` 顺序：从右到左
> 	- 参数由 caller 释放

## 2.3 补充：C 语言中函数的参数

### 2.3.1 参数未定函数

> `int printf(char *format, ...)` 参数的数量和类型都是未指定的

```c
double f(char *s, ...) {
	double y = 0;
	char *p;
	p = (char*)&s;
	p += sizeof(s);  // 这样就到了第一个未定参数
	while (*s != 0) {
		if (*s == 'i') {  // 表明是 int 类型变量
			y += *(int *)p;
			p += sizeof(int);  // 跳过了第一个未定参数
		} else if (*s == 'l') {
			y += *(long *)p;
			p += sizeof(long);
		} else if (*s == 'd') {
			y += *(double*) p;
			p += sizeof(32)
		}
	}
	return y;
}

void main() {
	double y;
	y = f("ild", 100, 200L, 3.0)
here:
}
```

```txt title="stack"
old bp
here
&"ild"[0]
100
200L
3,0
```

### 2.3.2 局部动态变量

```c
int f(int a, int b)
{
	int c;
	c = a + b;
	return c;
}
```

```asm
f:
	push bp
	mov bp, sp
	sub sp, 2  ; 相当于空的 push 行为，挖了一个坑给 c
	mov ax, [bp+4]
	add ax, [bp+6]
	mov [bp-2], ax  ; 计算 c 的值
	mov ax, [bp-2]
	mov sp, bp  ; 变量 c 死亡
	pop bp
	ret
```

```txt title="stack"
ss:1FF6  c       <-- sp
ss:1FF8  old bp
ss:1FFA  here
ss:1FFC  2
ss:1FFE  3
ss:2000
```

## 2.4 函数框架

```asm title="函数框架与寄存器保护"
f:
	push bp
	mov bp, sp  ; 创建堆栈框架
	sub sp, n  ; 分配动态变量的空间为 n 个字节
	push bx
	push si
	push di
	...
	pop di
	pop si
	pop bx
	mov sp, bp
	pop bp
	ret
```

> [!note] Note
> **Callee** 一定需要保护 `bp, bx, si, di` 四个可以段缺省的偏移地址寄存器

## 2.5 递归

> 注意堆栈的操作，特别是每次调用的 `bp` 值

```asm title="递归求和"
code segment
assume cs:code
;Input: n=[bp+4]
;Output: AX=1+2+3+...+n
f proc near
   push bp       ; (3)(6)(9)
   mov bp, sp
   mov ax, [bp+2]
   cmp ax, 1
   je done
   dec ax
   push ax       ; (4)(7)
   call f        ; (5)(8)
there:
   add sp, 2     ; (12)(15)
   add ax, [bp+2]
done:
   pop bp        ; (10)(13)(16)
   ret           ; (11)(14)(17)
f endp

main:
   mov ax, 3
   push ax       ; (1)
   call f        ; (2)
here:            ; f(3)的返回值在AX中, 值为6
   add sp, 2     ; (18)
   mov ah, 4Ch
   int 21h
code ends
end main
```

```txt title="stack"
ss:1FEE  bp2    (9)  <-- bp
ss:1FF0  there  (8)
ss:1FF2  ax=1   (7)
ss:1FF4  bp1=1FF(6)  <-- bp2
ss:1FF6  there  (5)
ss:1FF8  ax=2   (4)
ss:1FFA  old bp (3)  <-- bp1
ss:1FFC  here   (2)
ss:1FFE  ax=3   (1)
ss:2000
```

# 3 混合语言编程

> c + asm

## 3.1 TC

```c title="TC"
main() {
	int x=10, y=20, z;
	asm mov ax, [x]
	asm add ax, [y]
	asm mov [z], ax
	printf("z = %d",z);
}
```

> [!NOTE] 编译
> - TC 不能编译含有内嵌汇编指令的程序，要使用 `tcc` 编译器，在命令行界面进行操作
> ```shell
> d:
> cd \tc
> tcc -v tcasm.c
> td tcasm
> ```

```c title="支持标号"
main() {
	int i;
	{
		again:
		asm mov ah, 2
		asm mov dl, 'A'
		asm ...
	}
}
```

## 3.2 VC

> 使用 `__asm{}` 包裹

```c title="汇编代码段"
#include <stdio.h>
#include <math.h>
int main() {
	int x=-1, y=-2, z;
	__asm
	{
		mov eax, [x]
		add eax, [y]
		mov [z], eax
		push [z]
		call abs  // 可以调用其他函数
		add esp 4
		mov [z], eax
	}
	printf("%d", z);
	return 0;
}
```

```c title="纯汇编函数"
__declspec(naked) int f(int a, int b)  // 告诉编译器不需要为函数插入函数框架
{
	__asm
	{
		push ebp
		mov ebp, esp
		...	
	}
}
```

## 3.3 TC 调用汇编语言模块

```c
// int f(int x, int y, int *p){
//	  return (*p = x - y);
// }

extern int f(int x, int y, int *p);  // extern 让编译器在编译时不会报错

void main() {
	int x=1000, y=1001, z=0;
	f(x, y, *z);
	printf("z=%d", z);
}
```

```asm
public _f  ; 表示 f 是全局的，可以提供给外部函数调用，如果不写的话只能被本文件中的其他函数调用
_TEXT segment byte public 'CODE'  ; _TEXT 是因为 C 语言代码段也是这样命名
assume cs:_TEXT
;int f(int x, int y, int *p)
_f proc near  ; procedure 过程即函数，这里的下划线是因为 c 在编译的时候所有函数名前都会加上下划线
push bp
mov bp, sp
push bx
mov ax, [bp+4]; AX = x
sub ax, [bp+6]; AX = x - y
mov bx, [bp+8]; BX = p
mov [bx], ax  ; *p = x - y
mov ax, [bp+4]
add ax, [bp+6]; return AX
pop bx
pop bp
ret
_f endp
_TEXT ends
end  ; 这个模块没有 main，所以不需要 end main
```

```shell title="编译方法"
masm /Ml called.asm;  # 为了将所有标号的大小写保留 -> called.obj
copy called.asm /tc
cd /tc
tcc callasm.c called.obj  # 进行联合编译，先生成 callasm.obj，然后链接
```

```shell title="调试方法"
tcc -v callasm.c called.obj  # 包含源码调试信息
td called.exe  # 然后可以打开指令窗口，看到汇编代码
```