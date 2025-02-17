---
MkDocs_comments: true
date_created: 2025-02-01 14:33:26
date_modified: 2025-02-04 15:02:20
---
# Table of Contents

- [[ASMF 01 数据类型和变量]]
- [[ASMF 02 汇编语言源程序格式]]
- [[ASMF 02 汇编语言源程序格式]]
- [[ASMF 03 内存与寻址]]
- [[ASMF 04 寄存器]]
- [[ASMF 05 段和堆栈]]
- [[ASMF 06 中断和函数调用]]
- [[ASMF 07 数据传送指令]]
- [[ASMF 08 转换指令]]
- [[ASMF 09 算术运算指令]]
- [[ASMF 10 逻辑运算和移位指令]]
- [[ASMF 11 字符串操作指令]]
- [[ASMF 12 控制转移指令]]
- [[ASMF Cheat Sheet]]

# Info

> [!info] 汇编语言程序设计基础
> - 代码：CS1009G
> - 学分：2.0
> - 学期：2024 秋冬
> - 教师：白洪欢
> - 教材：*80x86 汇编语言程序设计基础*

> [!note]- Grading Policy
> - 平时分 **50**
> 	- 主要是作业，感觉没有考勤过
> - 期末考试 **50** *机考、闭卷考试*

# Tips

> [!warning] 这份笔记并不完善 
> - **调试**相关的内容有缺失，可以在教材上找到
> - [[ASMF Cheat Sheet]] 是期末复习手稿，可能有部分错误或表述不清，请以教材为准

> [!tip]
> - 这门课并没有那么困难，只要认真完成作业 & 复习好期末就能拿到不错的分数
> - 建议多尝试一些代码编辑/编译环境，用得顺手很重要

> [!quote] Useful Links
> - [教师主页](https://cc.zju.edu.cn/bhh)
> - [汇编语言程序设计基础 - mem 的小站](https://mem.ac/course/fasm/)

```asm title="hello.asm"
data segment
s db "Hello, world!", 0Dh, 0Ah, '$'
data ends

code segment
assume cs:code, ds:data
main:
	mov ax, data
	mov ds, ax
	mov ah, 9
	mov dx, offset s
	int 21h  ; 进行 printf
	mov ah, 4Ch
	int 21h
code ends
end main
```