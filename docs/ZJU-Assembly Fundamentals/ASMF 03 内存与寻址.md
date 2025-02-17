---
MkDocs_comments: true
date_created: 2024-12-18 13:13:18
date_modified: 2025-02-04 14:53:08
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
state:
- 待发布
- 归档
tags: Programming-Language/Assembly/80x86
type:
- note
---
# 1 内存

- DOS 系统在实模式下，能够访问 `[00000h, 0FFFFFh]` 共 1MB 的内存空间，这里的 `12345h` 称为物理地址，寄存器放不下，所以需要**段地址**和**偏移地址**
- 一个段的最大长度位 `0FFFFh`，也就是 64kB

# 2 段地址、偏移地址

- 段地址的 16 进制个位必须是 0
- 段的长度为 `2233Fh-12340h+1=10000h=64k`
- 一个物理地址可以表示为多个逻辑地址
	- `12398h`
	- `1230:0098`
	- `1239:0008`
	- `1234:0058`
	- $ 总之就是段地址只管到十位，偏移地址能更深入一位
	- $ 段地址 `+1` 等效于偏移地址 `+10h`

## 2.1 直接寻址和间接寻址

### 2.1.1 直接寻址：使用常数来表示偏移地址

> [!attention] 
> 段地址只能用寄存器来表示

```asm title="间接寻址"
mov al, ds:[2000h]
mov al, byte ptr ds:[2000h]  ; 声明类型是字节指针
							 ; 但其实可以省略，因为 al 就是一个字节
```

上面的操作等价于：

```c title="间接寻址"
typedef unsigned char byte
al = *(byte *)(ds:2000h);
```

## 2.2 间接寻址: 使用寄存器或寄存器 + 常数来表示偏移地址

> [!attention] 
> 用于间接寻址的寄存器**仅限** `bx, bp, si, di`，而且一定是 `bx, bp` 中的一个能和 `si, di` 中的一个相加

```asm title="间接寻址"
mov bx, 2000h
mov al, ds:[bx]
mov al, byte ptr ds:[bx]

mov ds:[bx], 1  ; 语法错误！！
mov bypt ptr ds:[bx], 1
mov word ptr ds:[bx], 1
mov dword ptr ds:[bx], 1
```

> [!warning] Warning
> 当源操作数是**常数**，目标操作数是**变量**时，无法确定宽度，必须指定 ptr

# 3 段缺省和段覆盖

```asm title="引用数组元素"
mov ah, [abc]  ; 直接操作 abc 地址指向的对象
			   ; 默认指定了 byte ptr
			   ; 默认段地址就是 ds
; 其完整形式为
mov ah, byte ptr ds:[abc]
```

## 3.1 段缺省的三个原则

1. 直接寻址，则缺省 `ds`
2. 间接寻址，含有 `bp` 时，缺省 `ss`
3. 间接寻址，不含 `bp` 时，缺省 `ds`

## 3.2 段覆盖

- 强制使用类似 `cs:[1000h]` 的形式覆盖段缺省的默认值

## 3.3 Assume 的作用

帮助编译器建立寄存器与段的关联，当源程序引用了某个段内的变量时，编译器会自动将段地址替换为关联的段地址寄存器

# 4 1M 内存空间的划分

| 地址范围                     | 用途              | 大小   |
| ------------------------ | --------------- | ---- |
| `[0000:0000, 9000:0000]` | 操作系统和用户程序       | 640K |
| `[A000:0000, A000:FFFF]` | 映射显卡内存 **图形模式** | 64K  |
| `[B000:0000, B000:7FFF]` | 映射显卡内存          | 32K  |
| `[B800:0000, B800:7FFF]` | 映射显卡内存 **文本模式** | 32K  |
| `[C000:0000, F000:FFFF]` | 映射 ROM          | 320K |

# 5 寄存器总结

## 5.1 16 位 CPU 中共有 14 个寄存器

- `ax, bx, cx, dx, sp, bp, si, di`
	- `bx, bp, si, di` 用来表示**偏移地址**，可以放在 `[]` 内
	- `ax, bx, cx, dx` 称为**通用寄存器**，常用于算数、逻辑运算
- `cs, ds, es, ss` 用来表示**段地址**
	- `cs:ip` 指向当前将要执行的指令，`ip` 是指令指针（instruction pointer），`cs` 是代码段寄存器
	- `ss:sp` 指向堆栈顶端，其中 `sp` 是堆栈指针（stack pointer），`ss` 是堆栈段寄存器
	- `es` 附加段寄存器，和 `ds` 一样，可以表示一个数据段的地址
- `ip, fl`

## 5.2 堆栈的简单操作

```asm title="push and pop"
stk segment stack
db 100h dup(0)
stk ends

code segment
assume cs:code
main:
	mov ax, 1234h
	mov bx, 5678h
	push ax
	push bx
	mov ax, 0
	mov bx, 0
	pop bx
	pop ax
code ends
end main
```

# 6 远指针、近指针

## 6.1 `lea` 加载偏移地址

> 加载偏移地址，load effective address

```asm
lea dx, ds:[bx]  ; 相当于 mov dx, bx，并没有简化
lea dx, ds:[bx+si+3]  ; 相当于一次计算了两个加法，其他指令无法做到，有用
lea eax, [eax+eax*4]  ; EAX=EAX*5，用 lea 作乘法
```

## 6.2 远指针 (Far Ptr)

- 16 位汇编，`xxxx:xxxx`，即 **16** 位段地址 + **16** 位偏移地址，`dword ptr`
- 32 位汇编，`xxxx:xxxxx`，即 **16** 位段地址 + **32** 位偏移地址，`fword ptr`

```txt
; &p = 1234:5678
1000:0000  78
1000:0001  56
1000:0002  34
1000:0003  12
```

> [!attention] 
> - 小端规则
> - 远指针和 int 无法区分，需要由使用者定义

## 6.3 `les`, `lds` 加载段地址

> 将段地址加载到 `es` 或者 `ds` 中，将偏移地址加载到指定寄存器中，Load segment address to Extra Segment reg / Data Segment reg

```asm title="取用远指针"
; bx=0, ds=1000h
mov di: ds:[bx]  ; di=5678h
mov es, ds:[bx+2]  ; es=1234h

lds bx, ds:[bx]  ; ds=1234h, bx=5678h

les di, ds:[bx]  ; es=[31:16]=1234h, di=[15:0]=5678h
```

> [!warning] Warning
> 常用 `les`，因为 `ds` 寄存器代表代码段，一般不修改

```asm title="Example: 使用变量保存远指针"
data segment
video_addr dw 0000h, 0B800h, 160, 0B800h  ; 上述定义也可以写成:
										  ; video_addr dd 0B8000000h, 0B80000A0h
										  ; video_addr db 00, 00, 00, 0B8h, 0A0h, 00, 00, 00, 0B8h
data ends

code segment
assume cs:code, ds:data
main:
   mov ax, data
   mov ds, ax
   mov bx, 0
   mov cx, 2
next:
   les di, dword ptr video_addr[bx]  ; es:di=B800:[0000]
   mov word ptr es:[di], 1741h
   add bx, 4
   sub cx, 1
   jnz next
   mov ah, 1
   int 21h
   mov ah, 4Ch
   int 21h
code ends
end main
```

# 7 补充：32 位寻址方式

- `[寄存器 + 寄存器*n + 常数]`
	- `n=1,2,4,8`
	- 寄存器为 `eax, ebx, ecx, edx, esi, edi, esp, ebp` 从中任选一个，可以同名 *限制更少了*

```asm title="遍历数组"
; long int a[3]={10,20,30};
; assume ds=seg a, ebx=offset a, esi=0

mov ecx, 3
again:
	mov eax, ds:[ebx+esi*4]
	add [sum], eax
	add esi, 1
	sub ecx, 1
	jnz again
```

# 8 显卡地址映射

## 8.1 文本模式：操作文本内容和颜色

- 屏幕的左上角为原点，横向为 $x$ 轴，纵向为 $y$ 轴，右下角的坐标为 $(79, 24)$，也就是 80 格宽，25 格高
- `offset = (y * 80 + x) * 2`
- 可以指定字符输出的位置和颜色

### 8.1.1 数据格式

- 每 2 byte 决定屏幕上的一个字符，分别对应 `[ASCII Code, Color]`，颜色的高 4 位是背景色，低 4 位是前景色
- 颜色对照表如下，红绿蓝可以合成其他颜色

|        | 背景  |     |     |     |     | 前景  |     |     |     |
| ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 位      | 7   | 6   | 5   | 4   |     | 3   | 2   | 1   | 0   |
| 对应颜色元素 | 闪烁  | 红   | 绿   | 蓝   |     | 高亮  | 红   | 绿   | 蓝   |

### 8.1.2 Example

```asm title="左上角显示红色的 A 和绿色的 B"
mov ax, 0B800h
mov ds, ax
mov byte ptr ds:[0], 'A'
mov byte ptr ds:[1], 74h
mov byte ptr ds:[2], 'B'
mov byte ptr ds:[3], 72h
```

> [!hint] 
> - `0B800h` 可以认为是显卡的地址，往显卡写入字符就可以显示在屏幕上
> - `74h` 中，`7` 表示背景色是白色，`4` 用来表示前景色是红色

```asm title="文本模式下用 * 显示汉字“我”"
data segment
hz db 04h,80h,0Eh,0A0h,78h,90h,08h,90h
   db 08h,84h,0FFh,0FEh,08h,80h,08h,90h
   db 0Ah,90h,0Ch,60h,18h,40h,68h,0A0h
   db 09h,20h,0Ah,14h,28h,14h,10h,0Ch
data ends
code segment
assume cs:code, ds:data
main:
   mov ax, data
   mov ds, ax
   mov ax, 0B800h
   mov es, ax
   mov ax, 0003h
   int 10h
   mov di, 0
   mov dx, 16
   mov si, 0
next_row:
   mov ah, hz[si]
   mov al, hz[si+1]
   add si, 2
   mov cx, 16
check_next_dot:
   shl ax, 1
   jnc no_dot
is_dot:
   mov byte ptr es:[di], '*'
   mov byte ptr es:[di+1], 0Ch
no_dot:
   add di, 2
   sub cx, 1
   jnz check_next_dot
   sub di, 32
   add di, 160
   sub dx, 1
   jnz next_row
   mov ah, 1
   int 21h
   mov ah, 4Ch
   int 21h
code ends
end main
```

## 8.2 图形模式：操作像素点

调用 `int 10h` 中断，将显卡切换到 320\*200，256 色的图形模式

```asm
mov ah, 0  ; 调用 int 10h 的 0 号子功能
mov al, 13h  ; 代表图形模式编号
int 10h
```

### 8.2.1 坐标转换

`(x, y) -> y*320+x`

### 8.2.2 数据格式

- 显卡内存中一个字节表示一个点

| 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 黑   | 蓝   | 绿   | 青   | 红   | 洋红  | 棕   | 白   |
| 8   | 9   | A   | B   | C   | D   | E   | F   |
| 灰   | 亮蓝  | 亮绿  | 亮青  | 亮红  | 紫   | 黄   | 亮白  |

```asm title="进入图形模式并显示红色方块" hl=
code segment
assume cs:code; cs不需要赋值会自动等于code
main:
   jmp begin
i  dw 0
begin:
   mov ax, 0013h
   int 10h
   mov ax, 0A000h
   mov es, ax
   ;(320/2, 200/2)
   mov di, (100-20)*320+(160-20); (160-20,100-20)
   ;mov cx, 41; rows=41
   mov i, 41
next_row:
   ;push cx
   push di
   mov al, 4; color=red
   mov cx, 41; dots=41
next_dot:
   mov es:[di], al
   add di, 1
   sub cx, 1
   jnz next_dot
   pop di; 左上角(x,y)对应的地址
   ;pop cx; cx=41
   add di, 320; 下一行的起点的地址
   ;sub cx, 1; 行数-1
   sub i, 1
   jnz next_row
   mov ah,0
   int 16h;bios键盘输入,类似int 21h的01h功能
   mov ax, 0003h
   int 10h; 切换到80*25文本模式
   mov ah, 4Ch
   int 21h
code ends
end main
```

```asm title="用图像模式显示汉字"我""
data segment
hz db 04h,80h,0Eh,0A0h,78h,90h,08h,90h
   db 08h,84h,0FFh,0FEh,08h,80h,08h,90h
   db 0Ah,90h,0Ch,60h,18h,40h,68h,0A0h
   db 09h,20h,0Ah,14h,28h,14h,10h,0Ch
data ends
code segment
assume cs:code, ds:data
main:
   mov ax, data
   mov ds, ax
   mov ax, 0A000h
   mov es, ax
   mov di, 0
   mov ax, 0013h
   int 10h
   mov dx, 16
   mov si, 0
next_row:
   mov ah, hz[si]
   mov al, hz[si+1]
   add si, 2
   mov cx, 16
check_next_dot:
   shl ax, 1; 刚移出的位会自动进入CF(进位标志)
   jnc no_dot; 若没有进位即CF=0则跳到no_dot
is_dot:
   mov byte ptr es:[di], 0Ch
no_dot:
   add di, 1
   sub cx, 1
   jnz check_next_dot
   sub di, 16
   add di, 320
   sub dx, 1
   jnz next_row
   mov ah, 1
   int 21h
   mov ax, 0003h
   int 10h
   mov ah, 4Ch
   int 21h
code ends
end main
```

# 9 端口

> [!note] Note
> CPU <-> 端口 (port) <-> I/O 设备

端口编号就是端口地址，`[0000h, 0FFFFh]` 一共有 65536 个端口

```asm title="port operation"
in al, 60h  ; 从 60h 端口获得输入
out 60h, al  ; 将 al 的值输出到 60h 端口 
```

## 9.1 Example: 读取键盘输入值

`60h` 端口是键盘的输入端口，通过修改硬件断点 `int 9h` 函数指针，让程序在键盘敲击时读取键盘输入值

### 9.1.1 Code %% fold %% 

```asm title="key"
;---------------------------------------
;PrtSc/SysRq: E0 2A E0 37 E0 B7 E0 AA  ;
;Pause/Break: E1 1D 45 E1 9D C5        ;
;---------------------------------------
data segment
old_9h dw 0, 0
stop   db 0
key    db 0; key=31h
phead  dw 0
key_extend  db 'KeyExtend=', 0
key_up      db 'KeyUp=', 0
key_down    db 'KeyDown=', 0
key_code    db '00h ', 0
hex_tbl     db '0123456789ABCDEF'
cr          db  0Dh, 0Ah, 0
data ends

code segment
assume cs:code, ds:data
main:
   mov ax, data
   mov ds, ax
   xor ax, ax
   mov es, ax
   mov bx, 9*4
   push es:[bx]
   pop old_9h[0]
   push es:[bx+2]
   pop old_9h[2]    ; 保存int 9h的中断向量
   cli
   mov word ptr es:[bx], offset int_9h
   mov es:[bx+2], cs; 修改int 9h的中断向量
   sti
again:
   cmp [stop], 1
   jne again        ; 主程序在此循环等待
   push old_9h[0]
   pop es:[bx]
   push old_9h[2]
   pop es:[bx+2]    ; 恢复int 9h的中断向量
   mov ah, 4Ch
   int 21h

int_9h:
   push ax
   push bx
   push cx
   push ds
   mov ax, data
   mov ds, ax       ; 这里设置DS是因为被中断的不一定是我们自己的程序
   in al, 60h       ; AL=key code
   mov [key], al
   cmp al, 0E0h
   je  extend
   cmp al, 0E1h
   jne up_or_down
extend:
   mov [phead], offset key_extend
   call output
   jmp check_esc
up_or_down:
   test al, 80h     ; 最高位==1时表示key up
   jz down
up:
   mov [phead], offset key_up
   call output
   mov bx, offset cr
   call display     ; 输出回车换行
   jmp check_esc
down:
   mov [phead], offset key_down
   call output
check_esc:   
   cmp [key], 81h   ; Esc键的key up码
   jne int_9h_iret
   mov [stop], 1
int_9h_iret:
   mov al, 20h      ; 发EOI(End Of Interrupt)信号给中断控制器，
   out 20h, al      ; 表示我们已处理当前的硬件中断(硬件中断处理最后都要这2条指令)。
                    ; 因为我们没有跳转到的old_9h，所以必须自己发EOI信号。
                    ; 如果跳到old_9h的话，则old_9h里面有这2条指令，这里就不要写。
   pop ds
   pop cx
   pop bx
   pop ax
   iret             ; 中断返回指令。从堆栈中逐个弹出IP、CS、FL。

output:
   push ax
   push bx
   push cx
   mov bx, offset hex_tbl
   mov cl, 4
   push ax   ; 设AL=31h=0011 0001
   shr al, cl; AL=03h
   xlat      ; AL = DS:[BX+AL] = '3'
   mov key_code[0], al
   pop ax
   and al, 0Fh; AL=01h
   xlat       ; AL='1'
   mov key_code[1], al
   mov bx, [phead]
   call display     ; 输出提示信息
   mov bx, offset key_code
   call display     ; 输出键码
   pop cx
   pop bx
   pop ax
   ret
   
display:
   push ax
   push bx
   push si
   mov si, bx
   mov bx, 0007h    ; BL = color
   cld
display_next:
   mov ah, 0Eh      ; AH=0Eh, BIOS int 10h的子功能，具体请查中断大全
   lodsb
   or al, al
   jz display_done
   int 10h          ; 每次输出一个字符
   jmp display_next
display_done:
   pop si
   pop bx
   pop ax
   ret
code ends
end main
```

### 9.1.2 Explain

```txt
KeyDown=1Eh KeyUp=9Eh  # 按下和抬起 A
KeyDown=1Dh KeyUp=9Dh  # left ctrl
KeyExtend=E0h KeyDown=1Dh KeyExtend=E0h KeyUp=9Dh  # right ctrl
```

## 9.2 Example: 读取 CMOS 时钟

`70h, 71h` 与 CMOS 时钟有关，其中的 4, 2, 0 分别表示当前的时分秒，使用 BCD 码

```asm
mov al, 2
out 70h, al  ; 70h 端口收到 2 号地址会将地址 2 和 71h 端口连通
mov al, 10h
out 71h, al  ; 将 10h 写入 2 号地址
in al, 71h  ; 读取 2 号地址的值
```

```asm title="BCD to char"
convert:
	mov ah, al  ; assume ah=al=19h
	and ah, 0Fh  ; ah=9h
	shr al, 4  ; al=1h
	add ah, '0'  ; ah='9'
	add al, '0'  ; al='1'
	ret
```

### 9.2.1 Code %% fold %% 

```asm title="readtime"
data segment
current_time db "00:00:00", 0Dh, 0Ah, '$'
data ends
code segment
assume cs:code, ds:data
main:
   mov ax, data
   mov ds, ax
   mov al, 4
   out 70h,al; index hour
   in al,71h ; AL=hour(e.g. 19h means 19 pm.)
   call convert; AL='1', AH='9'
   ;mov word ptr current_time[0],ax
   mov current_time[0], al
   mov current_time[1], ah
   mov al,2
   out 70h,al; index minute
   in  al,71h; AL=minute
   call convert
   mov word ptr current_time[3],ax;
   ;mov current_time[3], al
   ;mov current_time[4], ah
   mov al,0  ; index second
   out 70h,al
   in  al,71h; AL=second
   call convert
   mov word ptr current_time[6],ax
   mov ah, 9
   mov dx, offset current_time
   int 21h
   mov ah, 4Ch
   int 21h
;---------Convert----------------
;Input:AL=hour or minute or second
;      format:e.g. hour   15h means 3 pm.
;                  second 56h means 56s
;Output: (e.g. AL=56h)
;     AL='5'
;     AH='6'
convert:
    push cx
    mov ah,al ; e.g. assume AL=56h
    and ah,0Fh; AH=06h
    mov cl,4
    shr al,cl ; AL=05h
    ; shr:shift right右移
    add ah, '0'; AH='6'
    add al, '0'; AL='5'
    pop  cx
    ret
;---------End of Convert---------
code ends
end main
```

## 9.3 几种读取键盘方式总结

- `mov ah, 1; int 21h` 相当于 `al = getchar()`，不能读取方向键 **dos 中断调用**
- `mov ah, 0; int 16h` 相当于 `ax = 键盘编码`，可以读取方向键、PgUp 等，但不能读取单独的方向键 **bios (basic I/O system) 调用**
	- bios 封装在 ROM 芯片中，可以在没有操作系统的情况下调用
- `in al, 60h` 可以读取所有按键的编码 **端口操作**
