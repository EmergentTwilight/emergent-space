---
status:
  - archived
tags: CS/Language/Assembly/80x86
date_created: 2024-12-18T13:48:47
date_modified: 2025-09-13T10:18:06
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
---

# 1 字符串复制指令

```c title="copy"
memcpy(void *t, void *s, int n);
memmove(void *t, void *s, int n);
strcpy(char *t, char *s);
strncpy(char *t, char *s, int n);  // n 表示最多复制的字符数
```

## 1.1 `rep movsb`

> 从 `ds:si` 开始复制到 `es:di`，向前向后由 `DF` 决定，次数由 `CX` 决定

```pseudo title="movsb"
again:
	if (xc == 0)
		goto done;
	byte ptr es:[di] = byte ptr ds:[si]
	if (df == 0)
		{ si++, di++; }
	else
		{ si-- ; di--; }
	cx--
	goto again
done:
```

### 1.1.1 Example

```txt title="example: 从左边复制到右边"
1000:0000  "A"   2000:0000  "A"
1000:1001  "B"   2000:0001  "B"
1000:1002  "C"   2000:0002  "C"
1001:1003   0    2000:0003   0
```

```asm title="example"
mov ax, 1000h
mov ds, ax
mov si, 0  ; mov si, 3
mov ax, 2000h
mov es, ax
mov di, 0  ; mov di, 3
mov cx, 4
cld        ; std
rep movsb
```

> [!warning] Attention
> - `si, di` 一定会超出复制范围 1
> - 如果 `cld`，那么最终 `si=di=4`
> - 如果 `std`，那么最终 `si=di=FFFF`

## 1.2 `rep movsw`

> 一次复制一个 word

```pseudo
again:
	if (cx == 0)
		goto done;
	word ptr es:[di] = word ptr ds:[si]
	if (df == 0)
		{ si+=2; di+=2; }
	else
		{ si-=2; di-=2; }
	goto again
done:
```

## 1.3 `rep movsd`

> 同理，只是一次复制 4 个 byte

## 1.4 如果一次不是 4 个 byte

在 32 位系统下，如果要复制的字节数 `ecx` 不是 4 的倍数，可以做下面这样的处理，相当于处理了最后几个

```asm
push ecx
shr ecx, 2
rep movsd
pop ecx
and ecx, 3  ; 相当于 ecx = ecx % 4
rep movsb
```

# 2 字符串比较指令

## 2.1 `cmpsb`

```pseudo
cmp byte ptr ds:[si] and byte ptr es:[di]
if df == 0:
	si++
	di++
else:
	si--
	di--
```

## 2.2 `repe cmpsb`

> 若本次相等则继续比较下一个，repeat if equal

```pseudo
again:
	if (cx == 0)
		goto done
	compare byte ptr ds:[si] and byte ptr es:[di]
	if (df == 0)
		{ si++; di++; }
	else
		{ si--; di--; }
	cx--
	if (本次比较相等)
		goto again
done:
```

> [!warning] Attention
> - 这里的 `cx` 的作用是确定一个最大比较位数
> - 每次比较，无论是否相等，`si, di` 都会变化，所以要注意边界

## 2.3 `repne cmpsb`

> 如果本次比较不相等则继续比较下一个，repeat if not equal

## 2.4 实现 `strcmp`

```asm title="strcmp"
	repe cmpsb
	je equal
	dec si
	dec di
equal:
```

- 如果最后一次比较相等，说明从 `CX==0` 处退出，两个字符串全等，`di, si` 正好停在字符串外面一位
- 如果最后一次不相等，说明从 `if (本次比较相等)` 退出，不全等，`di, si` 停在第一个不同位置的*后面一位*，所以需要 `dec` 一次来找到第一个不相等的字符

# 3 字符串扫描指令

## 3.1 `scasb`

> 将 `al` 与字符进行比较，scan string by byte

```pseudo
cmp al, es:[di]
if (df == 0)
	di++;
else
	di--;
```

## 3.2 `repne scasb`

> 如果本次比较不相等则继续比较下一个

```pseudo
next:
	if (cx == 0) goto done
	cmp al, es:[di]
	if (df == 0) di++;
	else di--;
	cx--
	je done
	goto next
done:
```

### 3.2.1 应用：实现 `strlen`

```asm
mov ax, 1000h
mov es, ax
mov di, 2000h  ; es:di 就是目标字符串
mov cx, 0FFFFh  ; 最多查找 FFFF 次
mov al, 0  ; 待查找的字符
cld  ; 使用正方向
repne scasb
not cx  ; 相当于 FFFF-cx
dec cx
```

- 由于扫描到 `\0` 时仍然会 `cx--`，所以 `not cx` 是包括 `\0` 的
- 由于字符串长度不包括 `\0`，所以需要 `dec`

## 3.3 `repe scasb`

> 如果本次比较相等则继续比较下一个

### 3.3.1 应用：实现删除字符串前面的字符

> [!question] Question
> 加入 `1000:0000` 存有 `###ABC`，要求跳过前面的 `#`，将剩余部分复制到 `2000:0000`

```pseudo
assume that es=1000h, di=0, cx=7
mov al, '#'
cld
repe scasb
dec di  ; ES:DI->"ABC"
inc cx  ; CX=4
push es
pop ds  ; DS=ES
push di
pop si  ; SI=DI
mov ax, 2000h
mov es, ax
rep movsb
```

# 4 读取字符串指令 `lodsb/w/d`

> 加载 `ds:si` 指向的内容并移动指针

```pseudo
AL/AX/EAX = DS:[SI];
SI++;
```

### 4.1.1 `rep lodsb`

> 实现用 `CX` 控制的读取给定长度内存

# 5 字符串写入指令 `stosb/w/d`

## 5.1 `stosb/w/d` 填充指令

> 进行一次填充，移动 `di`

```pseudo
es:[di] = al
if (df == 0)
	di++
else
	di--
```

### 5.1.1 `rep stosb`

> 循环 `cx` 次 `stosb`

```pseudo
again:
	if (cx == 0) goto done
	es:[di] = al / ax / eax
	if (df == 0)
		di++ / di+=2 / di+=4
	else
		di-- / di-=2 / di-=4
	cx--
	goto again
done:
```

### 5.1.2 用处：内存初始化

```asm title="将 1000:10A0 开始共 100h 个字节都清零"
mov ax, 1000h
mov es, ax
mov di, 10A0h
mov cx, 100h
cld
xor al, al
rep stosb
```

或者使用 double word 填充，能够更快

```asm title="将 1000:10A0 开始共 100h 个字节都清零"
mov ax, 1000h
mov es, ax
mov di, 10A0h
mov cx, 40h
cld
xor eax, eax
rep stosd
```

### 5.1.3 Example: 过滤字符

> `ds:si -> "##AB#12#XY"`，`es:di` 指向空数组，`cx=11` 过滤字符串并放到空数组中

```asm
	cld
again:
	lodsb
	cmp al, '#'
	je next
	stosb
next:
	dec cx
	jnz again
```
