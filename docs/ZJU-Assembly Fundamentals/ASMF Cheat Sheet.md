---
MkDocs_comments: true
attachment:
- https://mem.ac/course/fasm/
date_created: 2024-12-17 18:24:38
date_modified: 2025-02-04 14:55:13
state:
- 待发布
- 归档
tags: Programming-Language/Assembly/80x86
type:
- note
---
# 编程 tips

- `add dl, '0'` 转字符格式
- `add dl, 20h` 大写转小写
- `sub dl, 20h` 小写转大写
- 32 位整数转 16 进制输出
	- 每次 `rol -> push -> and 0Fh -> ... -> pop` 实现从高到低，每次取四位
	- 逻辑判断 `cmp al, 10`，选择输出一个数字或者字母
- 二进制变量转十进制输出
	- 每次进行 `64 / 32 -> 32` 除法运算防止溢出
	- 使用栈进行反向输出，让个位最后输出
	- 需要统计 push 的次数
- 删除字符串前面的字符
	- 使用 `repe scasb` 来跳过等于 `al` 的字符
- `strcmp`
	- `repe cmpsb`
		- 如果最后一次相等，则全等，且过完了整个字符串
		- 否则，不全等，停在了第一个不相等字符串的后面
- 内存清零
	- `rep stosb` 来进行批量置零
- 过滤字符串字符
	- 首先设置好 `cld`，确认 `di, si` 地址正确，然后每一个字符都 `lodsb ... stosb` 来实现

# 指令表

- 数据传送指令
	- 通用数据传送指令 `mov,push,pop,xchg`
		- `mov dest, src`
			- 不能给 `cs` 赋值
			- 不影响标志位
			- 两个操作数不能都是内存变量
			- 等宽修饰！！
			- 不能将常数赋值给段寄存器
			- 不能引用 `ip, fl` 寄存器
		- `push op` 将 `src` 压入堆栈并更新 `sp`
			- 不影响标志位
			- 不支持 8 位操作数
		- `pop op` 弹出给 `op`，注意事项和 `push` 一样
		- `xchg src1, src2` 交换两个操作数的值
			- 不影响标志位
			- 不能有段寄存器
	- 输入输出指令 `in, out` 用于端口操作
		- `in al, port` 从端口读取到 `al`
			- `port` < 0FFh 的时候才能用常数，否则要用 dx 寄存器，`in al, dx`
		- `out port, al` 将 `al` 写入到端口，和 `in` 一样注意事项
	- 地址传送指令 `lea, lds, les`
		- `lea dest, src` load effective address 加载偏移地址
		- `lds dest, src` 将 `src` 偏移地址放到 `dest`，段地址放在 `ds`
		- `les dest, src` 将 `src` 偏移地址放到 `dest`，段地址放在 `es`
	- 标志寄存器传送指令 `lahf, sahf, pushf, popf`
		- `lahf` 将 `fl` 低 8 位赋值给 `ah` (load AH with Flags)
		- `sahf` 将 `ah` 赋值给 `fl` 低 8 位 (Store AH in Flags)
		- `pushf(d)` 加 d 是 `efl`
		- `popf(d)` 加 d 是 `efl`
- 转换指令
	- 扩充指令
		- `cbw` `al->ax`
		- `cwd` `ax->dx:ax`
		- `cdq` `eax->edx:eax`
		- `movsx dest, src` 将 `src` 符号扩充放到 `dest`
		- `movzx dest, src` 将 `src` 零扩充放到 `dest`
		- `xlat` 把 `byte ptr ds:[bx+al]` 赋值给 `al`
			- 先构造 `ds:bx->array`
			- 然后在 `al` 中写入字节下标，使用 `xlat` 取这个字节
- 算数运算指令
	- 加法指令
		- `add dest, src`
		- `inc op` **不影响 CF**
		- `adc dest, src` `dest = dest + src + CF`
	- 减法指令
		- `sub dest, src`
		- `sbb dest, src` `dest = dest - src - CF`
			- **计算借位减法也应该从低位算到高位**
		- `dec op` **不影响 CF**
		- `neg op`
		- `cmp op1, op2` `temp = op1 - op2`
			- 影响标志位，但是并不保存结果
			- 后面常伴随条件跳转指令
	- 乘法指令
		- `mul src` 无符号数乘法
			- `src` 8 位，`ax = al * src`
			- `src` 16 位，`dx:ax = ax * src`
			- `src` 32 位，`edx:eax = eax * src`
		- `imul` 有符号数乘法
			- `imul src` 和 `mul src` 用法相同
			- `imul src1, src2` `src1 = src1 * src2`
			- `imul src1, src2, imm` `src1 = src1 * src2 * imm`
	- 除法指令
		- `div op` 无符号数除法
			- 8-bit, `ax / op = al...ah`
			- 16-bit, `dx:ax / op = ax...dx`
			- 32-bit, `edx:eax / op = eax...edx`
			- **溢出**
				- 除数为 0，或者商过大导致商寄存器无法容纳
				- CPU 会在除法前面插入 `int 00h` 打印 overflow 并停止程序
				- 可以调整 `dx:[0]` 的 `int 00h` 中断矢量来改变行为
		- `idiv op` 有符号数除法，和 `div` 一样
	- 浮点运算指令
		- fp 寄存器都是 80-bit，一共有 `st(0), ..., st(7)` 八个
		- `fld op` (float load) 将一个浮点数压入堆栈
		- `fild op` (float int load) 将一个整数转换为浮点数压入堆栈
		- `fst dest` (float store) 将 `st(0)` 保存到一个浮点类型变量**或小数寄存器**
		- `fstp dest` (float store and pop) 一样的操作，只是多了一个 pop 的步骤
			- `fstp st` 一般用来当 pop 用
- 十进制调整指令
	- 压缩 BCD 码调整指令
		- `daa` (decimal adjust after addition) 将 `al` 在加法之后重新调整为 BCD 码
		- `das` (decimal adjust after substraction) 将 `al` 在剑法之后重新调整为 BCD 码
	- & 非压缩 BCD 码调整指令
		- `aaa` (ASCII adjust after addition) 非压缩 BCD 码加法调整
		- `aas` (ASCII adjust after substraction) 减法调整
		- `aam` (ASCII adjust after mul) 乘法调整
		- `aad` (ASCII adjust after div)
- 逻辑运算和移位指令
	- 逻辑运算指令
		- `and dest, src`
		- `or dest, src`
		- `xor dest, src`
		- `not op`
		- `test dest, src` 进行 and 运算但是不保留结果
	- 移位指令 **最后移出的一位永远放到 CF**
		- `shl dest, count` 逻辑左移
			- 没有 `.386` 的话，只能是 `shl reg, 1`
		- `shr dest, count` 逻辑右移
		- `sal dest, count` 算数左移，**和 SHL 完全一样**
		- `srl dest, count` 算数右移，左边补符号位
		- `rol dest, count` 循环左移，**最后移出又移入的数还是放在 CF**
		- `ror dest, count` 循环右移
		- `rcl dest, count` 带进位循环左移，右边补 CF，左边移到 CF，**相当于 CF 作为多余的一位参与循环移位了**
		- `rcr dest, count` 带进位循环右移
- 字符串操作指令
	- 字符串复制指令 `rep movsb/w/d` (mov string in byte)
		- `movsb` 先复制再移动 SI DI
			1. `byte ptr es:[di] = byte ptr ds:[si]` *分别是 data segment:source index 和 extra segment:destination index*
			2. `if (!DF) { di++; si++; } else { di--; si--; }` *w d 分别为 2 4*
		- `rep`
			1. 先判断 CX 是不是 0，如果是就结束
			2. 进行一次操作，然后 CX--
		- `rep movsb` 将 `ds:[si]` 指向的字符串复制到 `es:[di]`，CX 指定复制字符数量，DF 制定复制方向
	- 字符串比较指令 `repe/ne cmpsb/w/d`
		- `cmpsb` 先比较再移动 SI DI
			1. `cmp byte ptr ds:[si], byte ptr es:[di]`，状态保存在 FL
			2. `if (!DF) { di++; si++; } else { di--; si--; }`
		- `repe/ne` repeat if equal/not equal
			1. 先判断 CX 是不是 0，如果是就结束
			2. 进行指令操作
			3. CX-- *不影响标志位*
			4. 判断 ZF 是否为 0，再决定是终止还是继续
		- `strcmp: repe cmpsb`
			- 初始化 CX 为字符串长度
			- `repe cmpsb`
			- 如果最后一次是 equal，那么遇到 `\0` 退出，字符串全等
			- 否则，找到不相等的字符，由于 `cmpsb` 比较之后一定会移动 DI SI，所以 `dec si, dec di` 才能找到第一个不同的字符位置
	- 搜索字符串指令 `repe/ne scasb/w/d`
		- `scasb` **只和 `es:[di]` 有关了**，其实就是 cmpsb 里的源字符串变成了 al/ax/eax
			1. `cmp al, byte ptr es:[di]`
			2. `if (!DF) di++; else di--;`
		- `strlen: repne scasb` 可以用来求字符串长度
			- `al = 0`
			- 初始化 CX=0FFFFh，表示最大搜索长度
			- 搜到 0 的时候，根据 repne 的流程，还会进行 CX--
			- 使用 `not cx` 得到搜索过的字符数量，还需要 `dec cx` 得到没有 `\0` 的字符数量
	- 写入字符串指令 `rep stosb/w/d`
		- `stosb` 将 al/ax/eax 写入 `es:[di]`
			1. `byte ptr es:[di] = al`
			2. `if (!DF) di++; else di--;`
		- 可以用于数组清零 `cx=len; al=0; rep stosb`
			- 同时使用 `stosb/d`
				- `cx=len; push cx; shr cx, 2`
				- `rep stosd`
				- `pop cx; and cx, 3`
				- `rep stosb`
	- 读取字符串指令 `lodsb/w/d`
		- 从 `ds:[si]` 读取一个字符到 al/ax/eax，并按照 DF 指示移动 SI
		- 简化了数组遍历过程，可以用于**过滤字符**
- 控制转移指令
	- 无条件跳转指令 `jmp`
		- `jmp short dest` `EBXX`
		- `jmp near ptr dest` `E9XXXX`
		- `jmp far ptr dest` `EAXXXXXXXX`
	- 条件跳转指令 `jcc` 跳转距离全都是 1 字节，也就是 short jump
		- `ja = jnbe`
		- `jb = jc = jnae`
		- `jae = jnc = jnb`
		- `jbe = jna`
		- `jg = jnle`
		- `jl = jnge`
		- `jge = jnl`
		- `jle = jng`
		- `jz = je`
		- `jnz = jne`
		- `jp = jpe` 有奇偶校验位则跳转，也就是运算结果低 8 位的 1 有偶数个
		- `jnp = jpo` jump is no parity
		- `jcxz` jump if cx is zero
		- `jecxz` jump if ecx is zero
- 循环指令
	- `loop dest`
		1. CX--
		2. 如果 CX 不为 0，则跳转 dest
		- **loop 循环：循环体，cx--，判断；rep 系列循环：判断，循环体，cx--**
			- ! 这就会导致如果初始 CX=0，实际上会执行 FFFF 次
	- `loopz dest == loope dest`
		1. CX--
		2. 如果 `ZF==1 && CX!=0`，才跳转到 dest
	- `loopnz dest`
- 子程序调用与返回指令
	- `call near ptr dest` `E8 XXXX` 近调用
		- `back_addr = ip + 3`
		- `push back_addr`
		- `id = back_addr + delta`
	- `retn` 近返回
		- 流程
			- `pop back_addr`
			- `ip = back_addr`
		- `retn idata16` 用于堆栈平衡，**将调用函数时压入的参数弹出，这样主程序就不需要管理堆栈平衡了**
			- `pop back_addr`
			- `sp += idata16` `idata16` 是函数参数所占的字节数，不算返回地址的
			- `ip = back_addr`
		- ! 注意
			- 标号定义、`name proc...name endp` 定义和 `name proc near...name endp` 定义的函数中，ret 默认就是 retn
			- `name proc far...name endp` 定义的函数中，ret 默认是 retf，所以 retn 不能简写成 ret
	- `call far ptr dest` `9A XXXX XXXX` 远调用
		- 流程
			- `push cs`
			- `push ip+5` *这样在堆栈里的 far ptr 也满足了小端规则*
			- `ip = dest_l`
			- `cs = dest_h`
		- dest 可以是远标号 `name label far/ name proc far`，也可以是 mem32
			- `call dword ptr es:[di]`
	- `retf idata16` 远返回，并同时参数堆栈平衡
- 中断和中断返回指令
	- `int idata8` `CD XX`
		- `pushf`
		- `push cs`
		- `push ip+2`
		- `ip = word ptr 0000:[idata8 * 4]`
		- `cs = word ptr 0000:[idata8 * 4 + 2]`
	- `int 3` `CC` 软件端点中断
		- `pushf`
		- `push cs`
		- `push ip+1`
		- `ip = word ptr 0000:[000Ch]`
		- `cs = word ptr 0000:[000Eh]`
	- `into` `CE` 溢出中断 interrupt on overflow
		- 先判断 OF 是否为 1，是才接着执行
		- `pushf`
		- `push cs`
		- `push ip+1`
		- `ip = word ptr 0000:[0010h]`
		- `cs = word ptr 0000:[0012h]`
	- `iret` 中断返回
		- `pop ip`
		- `pop cs`
		- `popf`

|      | 短跳转              | 近跳转                 | 远跳转                      |
| ---- | ---------------- | ------------------- | ------------------------ |
| 指令格式 | `jmp short dest` | `jmp near ptr dest` | `jmp far ptr dest`       |
| 机器码  | `EB`             | `E9`                | `EA`                     |
| 示例   | `EB06`           | `E93412`            | `EA78563412`             |
| 范围   | `[80h, 7Fh]`     | `[8000h, 7FFFh]`    | `[0000:0000, FFFF:FFFF]` |
| 相对地址 | `dest-($+2)`     | `dest-($+3)`        | 绝对地址                     |
| 备注   | 相对偏移             | 相对偏移，小端规则           | 远指针，小端规则                 |

| 跳转指令                | 条件               | 解释          |     | 跳转指令           | 条件                | 解释                      |
| ------------------- | ---------------- | ----------- | --- | -------------- | ----------------- | ----------------------- |
| `je`                | `ZF==0`          |             |     | `jne`          | `ZF!=0`           |                         |
| `jae` (above or eq) | `CF==0`          | 没有借位，说明第一个大 |     | `jge`          | `SF==OF`          | 正数且没有溢出/负数且有溢出（实际应该是正数） |
| `ja` (above)        | `CF==0 && ZF==0` | 没有借位，而且不相等  |     | `jg` (greater) | `SF==OF && ZF!=0` | 满足 `jge` 且不相等           |
| `jbe`               | `CF==1`          | 有借位，说明第二个大  |     | `jle`          | `SF!=OF`          | 负数且没有溢出/正数且有溢出（实际应该是负数） |
| `jb`                | `CF==1 && ZF!=0` | 有借位，而且不相等   |     | `jl`           | `SF!=OF && ZF!=0` | 满足 `jle` 且不相等           |

# 寄存器

- `ax, bx, cx, dx, sp, bp, si, di`
	- `bx, bp, si, di` 用来表示**偏移地址**，可以放在 `[]` 内
	- `ax, bx, cx, dx` 称为**通用寄存器**，常用于算数、逻辑运算
- `cs, ds, es, ss` 用来表示**段地址**
	- `cs:ip` 指向当前将要执行的指令，`ip` 是指令指针（instruction pointer），`cs` 是代码段寄存器
	- `ss:sp` 指向堆栈顶端，其中 `sp` 是堆栈指针（stack pointer），`ss` 是堆栈段寄存器
	- `es` 附加段寄存器，和 `ds` 一样，可以表示一个数据段的地址
- `ip` PC 指针
- `fl` 标志寄存器

## 标志寄存器

- `ZF` 零标志
- `SF` 符号标志
- `OF` 溢出标志
- `PF` 奇偶校验标志
- `AF` 辅助进位标志*和 BCD 码的调整有关*
- `DF` 方向标志
	- `std; cld;`
- `IF` 中断标志，IF=0 禁止硬件中断
	- `sti; cli`
- `TF` 陷阱标志，TF=1 进入**单步模式**，每一条指令后面都会跟着一条 `int 01h`
	- 只能使用 `pushf popf` 来操作，例如 `pushf; pop ax; or ax, 100h; push ax; popf`
	- 调试器利用单步模式来获得控制权

# 内存空间

| 地址范围                     | 用途              | 大小   |
| ------------------------ | --------------- | ---- |
| `[0000:0000, 9000:0000]` | 操作系统和用户程序       | 640K |
| `[A000:0000, A000:FFFF]` | 映射显卡内存 **图形模式** | 64K  |
| `[B000:0000, B000:7FFF]` | 映射显卡内存          | 32K  |
| `[B800:0000, B800:7FFF]` | 映射显卡内存 **文本模式** | 32K  |
| `[C000:0000, F000:FFFF]` | 映射 ROM          | 320K |

# 常用中断

- `int 21h`

| AH  | 功能      | 调用参数        | 返回参数    |
| --- | ------- | ----------- | ------- |
| 00  | 程序终止    | CS=程序段前缀    |         |
| 01  | 键盘输入并回显 |             | AL=输入字符 |
| 02  | 显示输出    | DL=输出字符     |         |
| 09  | 显示字符串   | DS:DX=字符串地址 |         |
| 4C  | 带返回码结束  | AL=返回码      |         |

- `int 00h` 除法 overflow 错误中断
- `int 10h`
	- `ah = 0, al = 13h` 显卡切换到 320x200 图形模式
	- 显卡的文本模式直接这样就行 `mov ax, 0B800h; mov es, ax; mov al, 'A'; mov ah, 71h; mov es:[di], ax;`
		- 注意这里高位的内存地址更大，应该是颜色，低位才是字符
- `int 16h`
	- `ah = 0` 从键盘读取一个键的编码，放到 `ax`