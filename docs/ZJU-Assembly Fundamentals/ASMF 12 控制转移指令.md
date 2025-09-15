---
status:
  - archived
tags: CS/Language/Assembly/80x86
date_created: 2024-12-10T19:13:46
date_modified: 2025-09-13T10:18:06
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
---

# 1 无条件跳转指令 `jmp`

|     | 短跳转          | 近跳转              | 远跳转                      |
| --- | ------------ | ---------------- | ------------------------ |
| 机器码 | `EB`         | `E9`             | `EA`                     |
| 范围  | `[80h, 7Fh]` | `[8000h, 7FFFh]` | `[0000:0000, FFFF:FFFF]` |
| 备注  | 相对偏移         | 相对偏移，小端规则        | 远指针                      |

## 1.1 短跳转

```asm
1000:0100  EB06  jmp 0108h  ; 保存的是相对地址
1000:0102
1000:0104
1000:0106
```

> [!question] 为什么是 `EB06`
> 计算 `0108h - 0102h = 06` 用目标地址减去下一条指令地址即可
>
> 如果是下面这种情况：
>
> ```asm
> 1D3E:00F0  ...
> 1D3E:0100  EB??  jmp 00F0h
> ```
> 此时计算 `00F0h - 0102h = FFEEh` 可以进行符号截断，得到 `EE`

> [!note] Note
> 短跳转的范围为 `[-128, 127]`

> [!tip] Tip
> 好处在于，如果代码被整段复制，跳转的机器码不需要修改

### 1.1.1 代码移动

```asm
code segment
assume cs:code, ds:code, es:code
main:
   push cs
   pop ds; DS=CS
   push cs
   pop es; ES=CS
   cld
   mov ah, 2
   mov dl, 'A'
   int 21h
   mov si, offset begin_flag  ; 起始指令地址
   mov di, 1000h  ; 目标地址
   mov cx, offset end_flag - offset begin_flag  ; 得到这段代码机器语言的总长度
   rep movsb
   mov cx, offset end_flag - offset main  ; 本段代码的总长度
   mov di, offset main
   mov bx, 1000h
   jmp bx
begin_flag:
   jmp next
next:
   mov al, 0
   rep stosb
   mov ah, 2
   mov dl, 'B'
   int 21h
   mov ah, 4Ch
   int 21h
end_flag:
code ends
end main
```

> [!tip] Tip
> - 将 `begin_flag` 后面的内容移动到新的位置
> - 在新的位置，有 `jmp` 短跳转的机器码不变，相对偏移仍然正确
> - 在新的位置执行接下来的程序，将原来位置的代码抹除
> - 输出字符 `B`

```c title="C 中的代码移动"
extern int printf();
int f(int a, int b)
{
   return a+b;
}
void zzz(void)
{
}
main()
{
   char buf[100];
   char *p = (char *)printf;
   char *q = (char *)f;
   int n = (char *)zzz - (char *)f;
   int y;
   memcpy(buf, p, n);
   memcpy(p, q, n);
   y = printf(10, 20);
   memcpy(p, buf, n);
   printf("y=%d\n", y);
}
```

> [!tip] Tip
> - 这里的 `zzz` 只是为了确定 `f` 的长度，相当于 label
> - **首先备份原本的 `printf`**
> - 然后替换，调用
> - 最后恢复原来的 `printf`

## 1.2 近跳转

```asm title="近跳转的三种格式"
jmp 1000h  ; 偏移地址或者标号
jmp bx  ; 16 位寄存器
jmp word ptr [addr]  ; 16 位变量
```

```asm
1D3E:0100  E9FD1E  jmp 2000h
1D3E:0103
....
1D3E:2000
```

> [!question] 为什么是 `FD1E`
> `2000h - 0103h = 1EFD`，并使用小端格式表示成 `FD1E`

> [!note] Note
> 近跳转的范围为 `[8000h, 7FFFh]`

## 1.3 远跳转

```asm
code segment
assume cs:code
main:
	; jmp far ptr 0FFFFh:0000h 直接用这个编译不会通过
	db 0EAh;  jmp far ptr 的机器语言指令
	dw 0
	dw 0FFFFh
code ends
end main
```

> [!note] Note
> 上面的 `jmp 0FFFFh:0000h` 相当于重启，这是 ROM 映射的地址，是开机执行的第一条指令

```asm
data segment
	addr dw 0000h, 0FFFFh
	; 或 addr dd 0000FFFFh
data ends

code segment
assume cs:code, ds:data
main:
	mov ax, data
	mov ds, ax
	jmp dword ptr [addr]
code ends
end main
```

## 1.4 总结

```asm
code segment
assume cs:code
main:
	jmp next  ; 没有必要写成 jmp short next，因为编译器会自动辨别是短跳还是近跳
exit:
	mov ah, 4Ch
	mov dl, 'A'
	int 21h
	jmp abc  ; jmp neat ptr abc
	db 200h dup(0)  ; 专门用来阻碍短跳
abc:
	jmp far ptr away
code ends

fff segment
assume cs:fff
away:
	mov ah, 2
	mov dl, 'F'
	int 21h
	jmp far ptr exit  ; jmp far ptr exit
fff ends
end main
```

> [!note] Note
> 编译的时候，其实会产生这样的结果
> ```asm
>jmp next
>nop
>... 
>```
> 这是 forward reference，编译器还不知道 `next` 在哪里，可能需要 3 byte 的短跳，所以先空出 3 byte，发现为短跳之后再改成 `nop`

# 2 循环指令 `loop`

```asm
	mov ax, 0
	mov cx, 3
	; jcxz done
next:
	add ax, cx
	loop next  ; cx = 2, 1, 0
			   ; dec cx
			   ; jnz next
done:
```

> [!warning] Warning
> 如果 `cx = 0`，并不是 0 次循环，因为 `cx--` 会先执行，所以会执行 `10000h` 次
> 如果不希望发生这种情况，可以在循环外面进行一个判断 `jcxz done`

> [!NOTE]
> 另有 `loopz, loopnz` 指令，可以根据比较的结果来决定是否进行循环
> ```asm
> mov ax, 8000h
> mov bx, 8
> mov cx, 10h
> again:
> 	rol ax 1
> 	test bx, ax
> 	loopz again
>```

# 3 子程序调用与返回指令
