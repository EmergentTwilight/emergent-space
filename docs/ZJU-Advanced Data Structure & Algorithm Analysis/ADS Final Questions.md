---
status:
  - archived
tags:
  - CS/Algorithm/Analysis/Approximation
  - CS/Algorithm/Analysis/Complexity
date_created: 2024-12-31T14:51:35
date_modified: 2025-09-13T10:18:05
---



# 15-16 春夏

## Speed Check

- With the same operations,![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231145553245.webp]]
- Bin Queue deletemin 是 O(log N) 的
- neighborhood 里的搜索也可能需要指数时间！
- Max-cut approximation![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231151013535.webp]]
	- A 更新梯度，对的
	- B 是 $2|V|\log W$，错了
- least number of degree 2 node in B+ tree![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231152950538.webp]]
	- 如果全都是三度的，容量是 18 到 27 个，于是就可以满足，不需要任何二度节点
- most number of deg 2 node in B+ tree![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231155403402.webp]]
	- 可以构造尽量多的叶子，然后 bottom up 尽量都用 deg 2 节点建树
- about skew heap![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231154801845.webp]]
	- Skew heap 的最差合并复杂度是 O(N) 的

## Stop and Think

### 普通堆的均摊开销

![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231145826113.webp]]

> [!tip] Tip
> **T**
> - delete 的总次数一定小于 insert 的总次数
> - 无论如何均摊，只要保证 insert 的开销是大于等于 log n 就行，这样就是合理的，delete 的均摊开销甚至可以是 0
> 	- 即均摊后的总和开销一定大于等于真实开销
> - 另一方面，如果说 insert 是 1 而 deletemin 是 0 就是不合理的

### 3-SAT Random

![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231152246129.webp]]

> [!tip] Tip
> B 根据中心极限定理，应该是大约 0.5
> C 一定存在，如果 clause 之间共享的变量不多，那么这种 assignment 显然存在；就算全都共享一样的变量，最差也有 7/8

### Which is true?

![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231154459503.webp]]

> [!tip] Tip
> C 正确的，因为可以执行很多次
> D 不对，可以比最小的一个还要小，比如翻杯子问题，由于豆子已经确定在一个杯子里，总有一种算法只需要执行一次就能检查到

# 16-17 春夏

## Speed Check

- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231155649368.webp]]
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231160000890.webp]]
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231160011705.webp]]
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231160115325.webp]]
	- 考虑长方形，近似比和初始猜测解有很大关系！！
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231160302457.webp]]
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231162414676.webp]]
	- B 没问题，因为近似比的 2 就是这样证明出来的
	- C 应该满足中心极限，接近 1/2

## Stop and Think

### skew heap 的精确复杂度计算

![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231160847808.webp]]

> [!tip] Tip
> - $\Delta \Phi=k_{3}-k_{2}-k_{1}$
> - $c=2+k_{1}+k_{2}+\lfloor \log n_{1} \rfloor+\lfloor \log n_{2} \rfloor$
> - $\hat{c}=c+\Delta \Phi=2+k_{3}+\lfloor \log n_{1} \rfloor+\lfloor \log n_{2} \rfloor\leq 2+\lfloor \log n \rfloor+\lfloor \log n \rfloor+\lfloor \log n \rfloor$？反正大致这样就能推出来 3

# 17-18 春夏

## Speed Check

- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231164010989.webp]]
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231164522585.webp]]
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231200512929.webp]]
	- 需要强调 high probablity
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101003132802.webp]]
	- log N，每次期望删掉一半

## Stop and Think

### Set Cover Problem

![[__assets/ADS Final Questions/IMG-ADS Final Questions-20241231163401441.webp]]

> [!tip] Tip
> $O(\log n)$-factor approx

### Which are true?

![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101002853856.webp]]

> [!tip] Tip
> 这里其实没有一个对的，因为 max-cut 有 1.1382 近似比

# 18-19 春夏

## Speed Check

- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101003359857.webp]]
	- 记住 $log_k N+1$
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101003518792.webp]]
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101004045366.webp]]
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101004104794.webp]]
	- 矩阵分块的复杂度是一样的，除非使用 winograd
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101004643305.webp]]
	- 这是对的，这里说的是整个算法得到的结果是一个局部最优，那么 p 肯定是更加优化的
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101004833452.webp]]
	- A 正确是因为染色一次就多一个黑色节点
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101004948691.webp]]
	- 逆否命题问题
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101005106774.webp]]
	- 最后一个不转

# 19-20 春夏

## Speed Check

- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101105707364.webp]]
	- 纯纯眼高手低，应该是线性而不是平方的
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101111417475.webp]]
	- 这里先入为主了，目标不是减少 pass（那个是 polyphase merge），而是实现并行
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101111503265.webp]]
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101112033542.webp]]
	- 这里 36 其实应该刚好相等？但是就是更快？可能是常数也会更小？

## Stop and Think

### Vertex Cover Greedy

![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101105821894.webp]]

> [!tip] Tip
> 见 [[ADS 09 Greedy Algorithm#6.2.1 Vertex Cover Problem]]

### Build RBT

![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101113545956.webp]]

> [!tip] Tip
> 应该是 O(N) 的，一方面普通建堆也是 O(N) 的，另一方面，考虑第一次有 nlog2/2 第二次 nlog4/4 第三次 nlog8/8，就是 n 乘上一个 1/2+2/4+3/8+4/16... 而这个数列很明显是收敛的，所以是常数

### Minimum Degree Spanning Tree

![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101115501871.webp]]

> [!tip] Tip
> C
> A 除非是近似，不然一定是 1.5 的 lower bound，否则 P=NP
> D 是存在的
> C 一看就觉得不太对，但是资料也查不到）

### MAX-SAT

![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101120003467.webp]]

> [!tip] Tip
> B 是明显错误，应该是 8/7-approx

# 20-21 春夏

## Stop and Think

### Minimum Degree Spanning Tree Potential Func

![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101130028058.webp]]

> [!tip] Answer
> **D**
> A 显然错误，无环图的 degree 总和是 $2|V|-2$
> B 也有问题，进行一次操作后，删除的边 $-(\geq d(w))$，但是增加了一条 $d(u)+1$ 的边（假设 $d(u)>d(v)$），并且还有两条边可能 $+2$，无法保证递减
> C 有问题，对于操作中的 $u,v,w$ 是满足的，实现了 $-1$，但是可能导致其他很多点对的值变大
> D 正确，进行一次操作，考虑 $w$ 减少 $-(\geq 2 \cdot 3^{d(w)-1})$，考虑 $u,v$ 增加 $(2\cdot 3^{d(u)}+2\cdot 3^{d(v)})$。假设 $d(u)\geq d(v)$，存在 $d(w)-1\geq d(u)+1$，所以整体递减，满足题意

### 2 item sizes bin packing

![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101143151021.webp]]

> [!tip] Tip
> 只有 FF 有提升，NF 没有提升
> 期中 NF 没有提升是很好证明的，但是 FF 有提升需要及

# 21-22 春夏

## Speed Check

- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101144038154.webp]]
	- 举例子，例如一个两节点的和一个一节点的，原本 max npl 是 0，但是合并后可以变成 1 **找最简单的例子就行**
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101145129920.webp]]
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101145459652.webp]]
	- 所有边的权重绝对值和
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101145557024.webp]]
	- 不存在，Quick sort 最好也是 nlogn 的
- ![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101145709161.webp]]

## Stop and Think

### $\sqrt{ n }$-paradigm merge sort

![[__assets/ADS Final Questions/IMG-ADS Final Questions-20250101145739631.webp]]

> [!tip] Tip
> 1. 这里的 m 是**所有列表中的总元素个数**，千万要仔细读题！！
> 2. 这样的话，就有 $T(n)=\sqrt{ n }T(\sqrt{ n })+n\log \sqrt{ n }$
> 3. 使用代入检验，就能得到 B

# 22-23 春夏
