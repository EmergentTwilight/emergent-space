---
status:
  - archived
tags: CS/Language/Assembly/80x86
date_created: 2024-12-17T21:31:05
date_modified: 2025-09-13T10:18:06
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
---

# 1 算术运算指令格式（以加法为例）

```asm title="add 语句的几种用法"
add ax, bx                       ; reg, reg 
add ax, 2                        ; reg, constant
add ax, ds:[1000h]               ; reg, variable
add byte ptr ds:[1000h], 1       ; varible, constant
add ds:[1000h], ah               ; varible, reg
```

## 1.1 `add reg, reg`

> 寄存器必须等宽！

```asm
add ax, bh  ; wrong
add ah, bx  ; wrong
```

上面的加法中，使用的寄存器有 8 位和 16 位的，所以不能直接相加。

> [!example] Solution
> 如果一定要相加，则必须将较短的进行扩展：
> ```asm
> mov bl, bh  ; let bh = 12h, then bl = 12h
> mov bh, 0  ; bx = 0012h
> add ax, bx
> ```

> [!hint] 寄存器的关系
> `mov eax, 12345678h`
> 则 `ax=5678h`，`ah=56h`，`al=78h`，也就是

## 1.2 `add var, constant`

> 必须手动声明变量宽度！

```asm
add byte ptr ds:[1000h], 1
```

> [!attention]
> 汇编语言中**常数没有宽度**。上面的例子中，编译器无法自动确定变量宽度，**必须手动确定变量宽度**为 `byte ptr`

设 `ds=2000h`，且从地址 `2000h:1000h` 起存放了下面四个字节：

```txt
2000:1000 0FFh
2000:1001 0FFh
2000:1002 0FFh
2000:1003 0FFh
```

> [!attention]
> 汇编语言中，由于使用后缀 `h` 来声明 16 进制数，当这个 16 进制数开头恰好是字母时，编译器无法识别这是一个变量还是一个数。<br>
> 所以，**增加一个前缀 `0`** 来说明这是一个数而不是一个变量。

```asm title="同一个地址可以指向宽度不同的对象"
add byte ptr ds:[1000h], 1
; 此时指的是 0FFh，进行加一后变成了 00h

add word ptr ds:[1000h], 1
; 此时是 0FFFFh + 1 = 0000h

add dword ptr ds:[1000h], 1
; 此时是 0FFFFFFFFh + 1 = 00000000h
```

## 1.3 不存在 `add var, var`

> [!hint]
> 由于 Intel CPU 的硬件限制，一个 step 中只能访问一个地址的内存，因此无法直接将两个 var 相加

```asm title="错误和对应的修正"
; wrong
add byte ptr ds:[1000h], byte ptr ds:[2000h]

; correct
mov ah, ds:[2000h]
add ds:[1000h], ah
```

### 1.3.1 编译器如何处理变量相加

```c
a += b;
```

```asm title="visual c++ 无优化"
00401028    mov        eax, [00424a30]
0040102D    add        eax, dword ptr [00424a34]
00401033    mov        [00424a30], eax
```

> [!NOTE]
> - 上述的汇编语言其实可以压缩到两步
> - `[00424a30]` 这里相当于省略了 `ds:`

# 2 加法和减法

| 加法指令 | `add` | `inc`    | `adc` |         |           |
| ---- | ----- | -------- | ----- | ------- | --------- |
| 含义   | 加法    | 自增       | 带进位加法 |         |           |
| 备注   |       | 不影响 `CF` |       |         |           |
| 减法指令 | `sub` | `dec`    | `sbb` | `neg`   | `cmp`     |
| 含义   | 减法    | 自减       | 带借位减法 | 符号相反数   | 减法比较      |
| 备注   |       | 不影响 `CF` |       | 相当于普通减法 | 不保存计算结果结果 |

> 乘除法的语法比较复杂，本次课不会涉及

## 2.1 `inc` 自增

- 比 `add ax, 1` 机器码更短，执行速度更快
- **不会导致 `CF` 的改变**，但是会影响别的标志位

```asm title="更短的代码" hl=10,11
again:
	add ax, cx
	jc done
	add cx, 1
	jmp again
done:

again:
	add ax, cx
	inc cx
	jnc again
done:
```

- 上面的代码中，先使用 `inc cx` 对下一次循环做准备，然后再进行跳转判断，减少了跳转语句

> `dec` 同理

## 2.2 `adc` 带进位加法

```asm title="不使用 32 位寄存器完成大数加法 12345678h+5678FFFFh"
mov dx, 1234h
mov ax, 5678h  ; dx:ax
add ax, 0FFFFh  ; CF=1
adc dx, 5678h  ; dx + 5678h + CF
```

> `adc a, b ==> a = a + b + CF`

### 2.2.1 用 `adc` 实现更大的加法

```asm title="使用数组表示的大数加法"
x db 100 dup(88h)
y db 100 dup(89h)
z db 101 dup(0)

main:
	mov cx, 100
	mov si, offset x
	mov di, offset y
	mov bx, offset z
	clc
again:
	mov al, [si]
	adc al, [di]
	mov [bx], al
	inc si
	inc di
	inc bx
	dec cx
	jnz again
```

- 每次都直接使用 `adc`，类似**接力**的方法

## 2.3 `sbb` 带借位减法 (subtract with borrow)

```asm title="sbb: 56781234h-1111FFFFh"
mov ax, 1234h
sub ax, 0FFFFh  ; CF=1
mov dx, 5678h
sbb dx, 1111h  ; DX=5678h-1111h-CF
```

- `sbb a, b ==> a = a - b - CF`
- 运算时应该先算低位产生借位，然后再用 `sbb` 得到高位考虑借位的结果

## 2.4 `neg` 相反数

```asm
neg ax  ; ax = 0 - ax
; neg ax = ~ax + 1
```

> [!attention]
> 应当当作普通的减法指令来看待，**会影响标志位**

## 2.5 `cmp` 减法比较

> `cmp` 和 `sub` 的区别在于，进行了减法，保留了**对标志位的影响**，但是丢弃了结果

- `jg, jl, jge, jle` 是**有符号数**比较相关跳转指令
	- `jg: SF==OF && ZF==0`
	- `jge: SF==OF`
	- `jl: SF!=OF`
	- `jle: SF!=OF || ZF==1`
- `ja, jb, jae, jbe` 是**无符号数**比较相关跳转指令
	- `jb: CF=1` (jump if below)
	- `ja: CF=0 & ZF=0` (jump if above)

> [!example]
>
> ```asm
> mov ah, 0FFh
> mov al, 01h
> cmp ah, al
> ja jump1
> jg jump2
> ```
> - 上述 `ah` 是有符号数 `-1`，所以 `ja` 会跳转而 `jg` 不会跳转

# 3 乘法和除法

| 指令  | `mul` | `imul` |
| --- | ----- | ------ |
| 含义  | 无符号乘法 | 符号数乘法  |
| 指令  | `div` | `idiv` |
| 含义  | 无符号整除 | 符号数除法  |

## 3.1 `mul` 无符号乘法

| 位宽    | `8 * 8 -> 16`     | `16 * 16 -> 32`    | `32 * 32 -> 64`       |
| ----- | ----------------- | ------------------ | --------------------- |
| 指令    | `mul src(r/m[8])` | `mul src(r/m[16])` | `mul src(r/m[32])`    |
| 隐含被乘数 | `AL`              | `AX`               | `EAX`                 |
| 含义    | `AX = AL * SRC`   | `DX:AX = AX * SRC` | `EDX:EAX = EAX * SRC` |

### 3.1.1 8 位乘法

- 另一个乘数一定是 AL
- 乘积一定是 AX

```asm title="8-bit mul example"
mov al, 12h
mov bl, 10h
mul bl;  AX=AL*BL=0120h
```

### 3.1.2 16 位乘法

- 被乘数一定是 AX
- 乘积一定是 DX:AX

```asm title="16-bit mul example"
mov ax, 1234h
mov bx, 100h
mul bx  ; dx=0012h, ax=3400h
```

### 3.1.3 32 位乘法

- 被乘数一定是 EAX
- 乘积一定是 EDX:EAX

`mul ebx  ; edx:eax=eax*ebx`

#### 3.1.3.1 Example: 十进制数字符串转 int32

```asm title="dec2int32"
.386  ; 启用 32 位寄存器
data segment use16  ; 段内偏移地址都是用的 16 位
s db "2147483647", 0  ; 7FFF FFFFh
abc dd 0
data ends

code segment use16
assume cs:code, ds:data
main:
	mov ax, data
	mov ds, ax
	mov eax, 0  ; 答案存放的位置
	mov si, 0  ; index
again:
	cmp s[si], 0
	je done
	mov ebx, 10
	mul ebx  ; eax = eax * 10
	mov edx, 0  ; 保证 edx 清空，只有 dl 有值，避免加法出错
	mov dx, s[si]
	sub dl, '0'
	inc si
	add eax, edx
done:
	mov abc, eax
	mov ah, 4Ch
	int 21h
code ends
end main
```

> 每读出一个字符，转换成数字，将原来的值乘以十加上这个数

## 3.2 `imul` 符号数乘法指令

| 类型    | `imul src(r/m[8/16/32])`                                         | `imul src1(r[16/32]), src2(r/m[16/32])` | `imul src1(r[16]), src2(r/m[16]), constant(imm[16])` |
| ----- | ---------------------------------------------------------------- | --------------------------------------- | ---------------------------------------------------- |
| 隐含被乘数 | `AL/AX/EAX`                                                      | 无                                       | 无                                                    |
| 含义    | `AX = AL * SRC`/<br>`DX:AX = AX * SRC`/<br>`EDX:EAX = EAX * SRC` | `SRC1 = SRC1 * SRC2`                    | `SRC1 = SRC2 * CONSTANT`                             |

```asm title="imul 可以包含 2 个或者 3 个操作数"
imul eax, ebx  ; eax = eax * ebx
imul eax, ebx, 3  ; eax = ebx * 3，这种用法中第三个参数只能是常数
```

> [!attention] 规范
> - 第二个操作数可以是寄存器或变量
> - 第三个操作数必须是常数

> [!bug]
> - 可能会造成乘法溢出，不像除法溢出那样，CPU 不会中断处理乘法溢出
> - `idiv` 没有类似的使用方法

## 3.3 `div` 无符号数除法

| 位宽    | `16 / 8 -> 8`          | `32 / 16 -> 16`           | `64 / 32 -> 32`               |
| ----- | ---------------------- | ------------------------- | ----------------------------- |
| 指令    | `div src(r/m[8])`      | `div src(r/m[16])`        | `div src(r/m[32])`            |
| 隐含被除数 | `AX`                   | `DX:AX`                   | `EDX:EAX`                     |
| 含义    | `AX / SRC = AL ... AH` | `DX:AX / SRC = AX ... DX` | `EDX:EAX / SRC = EAX ... EDX` |

### 3.3.1 16 位除 8 位得 8 位

`ax / 除数 = al..ah`

```asm title="16/8 example"
mov ax, 123h
mov bh, 10h
div bh  ; AL=12h, AH=03h
```

### 3.3.2 32 位除 16 位得 16 位

`dx:ax / 除数 = ax..dx`

### 3.3.3 64 位除 32 位得 32 位

`edx:eax / 除数 = eax..edx`

### 3.3.4 除法溢出

- 除以 0 会发生溢出，但有时候除以 1 也会导致商太大而无法保存到商寄存器中

```asm
mov ax, 123h
mov bh, 1
; int 00h  ; 会自动插入这一条，停止程序
div bh  ; 商会溢出
```

### 3.3.5 Example: 二进制转十进制输出

```asm
.386
data segment use16
abc dd 7FFFFFFFh
s db 10 dup(' '), 0Dh, 0Ah, '$'
data ends
code segment use16
assume cs:code, ds:data
main:
   mov ax, data
   mov ds, ax
   mov di, 0; 数组s的下标
   mov eax, abc
   mov cx, 0; 统计push的次数
again:
   mov edx, 0; 被除数为EDX:EAX
   mov ebx, 10
   div ebx; EAX=商, EDX=余数
   add dl, '0'
   push dx
   inc cx; 相当于add cx, 1
   cmp eax, 0
   jne again
pop_again:
   pop dx
   mov s[di], dl
   inc di
   dec cx; 相当于sub cx, 1
   jnz pop_again

   mov ah, 9
   mov dx, offset s
   int 21h
   mov ah, 4Ch
   int 21h
code ends
end main
```

> [!attention]
> - 要使用 64 位除 32 位才行，否则会溢出
> - 使用栈先入后出的性质，来将余数按照正确的顺序输出
> - 堆栈只能进行 16 位或 32 位操作，所以即使 `dl` 是需要的 `char`，也要 `push dx`
> - `edx` 在进行除法前必须清零！

## 3.4 `idiv` 符号数除法指令

```asm title="计算 -2/2"
mov ax, -2
mov bl, 2
idiv bl  ; idiv 是有符号数除法指令，AL=0FFh，AH=0
		 ; 使用 div 无符号数除法，会导致溢出，65534/2
```

> [!warning] Attention
> 除法中，如果**除数为零**或者**商寄存器放不下**都会发生**除法溢出**，此时 CPU 会在除法指令上面插入 `int 00h` 中断

# 4 浮点数运算

## 4.1 FP 指令

- `fadd, fsub, fmul, fdiv` 是加减乘除指令
- `fld` 将小数类型变量从内存载入 CPU 中的小数寄存器
- `fild` 将整数类型转化为小数并载入小数寄存器
- `fst` 将小数寄存器 `st(0)` 保存到变量中
- `fstp` 将小数寄存器 `st(0)` 保存到变量中并弹出 `st(0)`

> 最早的 8086 不支持浮点数计算，而是由单独的配套 FPU 8087 进行计算

## 4.2 FP 寄存器

- `st(0), st(1), ..., st(7)` 形成堆栈的形式
	- 在 `fld/fild` 的时候会将 `st(0)` 往后 `push` 到 `st(1)`
- 宽度均为 80-bit 的 `long double` 类型

```asm title="float"
data segment
x dt 3.1415926535897932  ; long double x
y dq 9.3759765625        ; double y
z dd 2.71828             ; float z
i dd 2                   ; long int i
r dt 0                   ; short int r
data ends

code segment
assume cs:code, ds:data
main:
	mov ax, data
	mov ds, ax
	
	fild [i]            ; st(0)=2
	fld [x]             ; st(0)=3.14...., st(1)=2
	fmul st, st(1)      ; st 是 st(0) 的简写
	                    ; 乘法的结果放回 st(0)
	fstp [i]
	mov ah, 4Ch
	int 21h
code ends
end main
```

> [!warning] Attention
> - 编译器会在任何 float 指令前后插入 `wait`，因为 8086 需要等待 8087 计算完成
> - `td` 中观察 FP 寄存器需要打开 `View/Numeric Processor` 窗口
> - 运行完可以在数据窗中看到 `i`，以 IEEE754 格式表示
