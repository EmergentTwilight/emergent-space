---
MkDocs_comments: true
date_created: 2024-12-18 12:23:01
date_modified: 2025-01-25 16:27:26
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
state:
- 待发布
- 归档
tags: Programming-Language/Assembly/80x86
type:
- note
---
# 1 符号扩充指令 (sign extend)

```asm
mov al, 0FEh
cbw  ; 将 AL 做 sign ext 放在 AX 中
```

| `cbw`                | `cwd`                 | `cdq`                  | `movsx al, ax`           | `movzx al, ax`           |
| -------------------- | --------------------- | ---------------------- | ------------------------ | ------------------------ |
| convert byte to word | convert word to dword | convert dword to qword | move with sign extension | move with zero extension |
| AL->AX               | AX->DX:AX             | EAX->EDX:EAX           | 符号扩充                     | 零扩充                      |

> [!attention] 
> `cbw, cwd, cdq` 没有参数，需要记住目标寄存器

## 1.1 扩展符号位

```asm title="cbw 扩展 al 符号位" hl=2
mov al, -2
cbw  ; 如果不使用 cbw，要判断 al 的正负，使用分支结构
mov bl, 2
idiv bl
```

## 1.2 零扩充指令 `movzx`

```asm title="a 寄存器上的零扩充"
movzx ax, al
movzx eax, al
```

> [!tip] Tip
> 可以随意指定源寄存器和目标寄存器

## 1.3 符号扩充指令 `movsx`

> 用于淘汰 `cbw` 指令，方便使用且符合直觉

```asm title
movsx ax, al
```

# 2 `XLAT` 换码指令

> 让 `ds:bx` 指向表，`al` 为数组的下标，执行 `xlat` 后有 `al=ds:[bx+al]`

```c title="查表法 in C"
char t[] = "01234567890ABCDEF";
char i;
i = 10;
i = t[i];  // 好处是，不需要更多的 if else 判断；但是比较消耗空间
```

```asm title="使用查表法实现 16 进制数输出"
.386 ; 表示程序中会用32位的寄存器
data segment use16; use16表示偏移使用16位
t db "0123456789ABCDEF"
x dd 2147483647
data ends

code segment use16
assume cs:code, ds:data
main:
   mov ax, data    ;\
   mov ds, ax      ; / ds:bx->t[0]
   mov bx, offset t;/
   mov ecx, 8
   mov eax, x
next:
   rol eax, 4
   push eax
   and eax, 0Fh
   xlat
   mov ah, 2
   mov dl, al
   int 21h
   pop eax
   sub ecx, 1
   jnz next
   mov ah, 4Ch
   int 21h
code ends
end main
```