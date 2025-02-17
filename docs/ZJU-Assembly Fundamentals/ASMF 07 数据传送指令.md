---
MkDocs_comments: true
date_created: 2024-12-18 12:21:22
date_modified: 2025-02-04 14:53:03
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
state:
- 待发布
- 归档
tags: Programming-Language/Assembly/80x86
type:
- note
---
# 1 通用数据传送指令

## 1.1 XCHG: exchange 交换

```asm title"xchg example"
mov ax, 1
mov bx, 2
xchg ax, bx
xchg ax, ds:[bx]
```

> 交换**两个寄存器**的值或**一个寄存器和一个内存地址**的值

# 2 地址传送指令 `lea, lds, les`

![[ASMF 03 内存与寻址#6 远指针、近指针]]

