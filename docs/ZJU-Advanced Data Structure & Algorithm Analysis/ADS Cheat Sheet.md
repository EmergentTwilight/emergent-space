---
MkDocs_comments: true
date_created: 2024-11-03 20:31:58
date_modified: 2025-01-31 19:26:17
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
---


# 1 Data Structures

## 1.1 Balanced BST

### 1.1.1 AVL Trees

- $n_{h}=F_{h+3}-1$，**假如空树高度是 -1，或者说边才能提供高度？**
- $BF$ balance factor 可以是 1, -1, 0
- LL, RR 都是单次旋转，LR, RL 都要转两次
- Trouble maker 是产生不平衡时插入的节点，Trouble finder 是插入操作后 $BF$ 发生不平衡的节点
- 记录 height 而不是 bf 能够减少更新次数
- 删除操作
	- 找到要删的节点
		- 如果是叶子，删除
		- 如果是 2 度，试图删除前驱或后继
		- 如果是 1 度，删除并提升子节点
	- bottom-up 回去进行高度更新和旋转平衡调整

| Insert                | Find        | Delete      |
| --------------------- | ----------- | ----------- |
| $O(\log N)$           | $O(\log N)$ | $O(\log N)$ |
| 先插入 BST，在递归中完成局部检查和调整 |             | 递归删除并检查调整   |

### 1.1.2 Splay Trees

- zig, zig-zig 都算 single rotation，zig-zag 才算 double
	- 在 AVL 中，zig-zig 也算两次
- 优点是存储空间小
- 删除的时候，splay 到根，删根，左子树 splay max，然后让右子树成为左子树的右孩子
- **roughly halves the depth of most nodes on the path**
- 势能函数 $\Phi(T)=\sum_{i \in T}\log S(i)$，其中 $S(i)$ 表示节点 $i$ 为根的子树的节点数量，约等于 height
	- 可以证明单次 rotate 的均摊开销是常数的，
	- The amortized time to splay a tree with root $T$ at node $X$ is at most $3(R(T)-R(X))+1=O(\log N)$

| Insert               | Find         | Delete                          | 势能函数                              |
| -------------------- | ------------ | ------------------------------- | --------------------------------- |
| $O(\log N)$*         | $O(\log N)$* | $O(\log N)$*                    | $\Phi(T)=\sum_{i \in T}\log S(i)$ |
| 先插入 BST，再 splay 到根节点 | 找到并 Splay    | 找到，splay，删除，左子树 splay max，右子树接上 |                                   |

### 1.1.3 Red-Black Trees

- 定义
	- 根是黑色
	- `NIL` 是共享叶子，是黑色，除了 nil 都是 internal node
	- 没有连续的红色节点
	- **每个**节点的黑高相同
		- black height 不算自己，算 `NIL` *类比 2-3-4 tree*
	- ! 红色一度节点出现就非法
- 平衡性证明
	- $bh(x)\geq h(x)/2$ 因为没有红色连续
	- $sizeof(x)\geq 2^{bh(x)}-1$ 递推
	- $h\leq 2\ln(N+1)$ 平衡性 **记住这个式子**
- 插入的情况
	- bottom-up
		- 叔叔红色则染色
		- 叔叔黑色保证红色同侧，并换色旋转
	- top-down
		- 向下遍历的时候，将有两个红色孩子的黑色节点染红，其孩子染黑
		- 这样就保证父亲为红色时，叔叔不可能是红色，直接进入最后情况
- 删除的处理
	- 删除黑色叶子的时候才需要进行下面的操作 [[ADS 02 Red-Black Trees and B+ Trees#1.4.1.2 Step 2. 调整 Black Height]]
	- 当成 2-3-4 树来操作

| Number of rotations | AVL         | RBT     |
| ------------------- | ----------- | ------- |
| Insertion           | $\le 2$     | $\le 2$ |
| Deletion            | $O(\log N)$ | $\le 3$ |

| Insert      | Find        | Delete      | FindMax(FindMin) |
| ----------- | ----------- | ----------- | ---------------- |
| $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(\log N)$      |

### 1.1.4 B+ Trees

- 定义
	1. 根是叶子或有 $[2, M]$ 个孩子
	2. 所有非叶子节点（除了根）都有 $[\lceil M/2\rceil, M]$ 个孩子，强调这个 M/2
	3. 所有叶子的**深度相同**
- 复杂度分析
	- $T_{find}=Depth(M,N)\times O(\log M)=O(\lceil \log_{\lceil M/2 \rceil}N \rceil)\times O(\log M)=O(\log N)$
	- $T_{insert}(M,N)=O((M/\log M)\log N)$ 这里考虑的是顺序遍历索引，但其实可以二分查找

## 1.2 Priority Queues

### 1.2.1 Leftist Heaps

- NPL, $Npl(left)\geq Npl(right)$
- property
	- 右路经节点数 $\leq \lfloor \log(N+1) \rfloor$
		- $\leftrightarrow$ 若右路经上有 $r$ 个节点，则 $N\geq 2^r-1$
	- $Npl(root)=r$，那么 $N\geq 2^{r+1}-1$
- Operations
	- merge
		- 如果其中一个堆已经没有左孩子了，那么根据 $Npl$，它一定没有右孩子，这时候为了维护 $Npl$ 只需要将另一个堆当作其左孩子

| Operation    | FindMin     | DeleteMin        | Insert              | DecreaseKey | Merge            |
| ------------ | ----------- | ---------------- | ------------------- | ----------- | ---------------- |
| Binary       | $\Theta(1)$ | $\Theta(\log n)$ | BuildHeap in $O(n)$ | $O(\log n)$ | $\Theta(n)$      |
| Leftist Heap | $\Theta(1)$ | $\Theta(\log n)$ | $\Theta(\log n)$    | $O(\log n)$ | $\Theta(\log n)$ |

### 1.2.2 Skew Heaps

- **Always** swap the left and right children except that the largest of all the nodes on the right paths does not have its children swapped. **始终**交换左子树和右子树，除了在右路径上最大的节点不交换其子节点。
	- 必须完整遍历右路径，即使一个堆已经空了也需要遍历另一个堆余下的右路经，以此保证进行交换
	- 最后一个合并的节点，其**一定没有右孩子**，且**不进行子树交换**
- Amortized Analysis [[ADS 04 Leftist Heaps and Skew Heaps#3.2 Amortized Analysis for Skew Heaps]]
	- $definition$: 某一节点的后代（包括自己）中，其右子树内的大于等于一半，则其为 *heavy node*，反之为 *light*。也就是 $R\geq \frac{L+R+1}{2}$
	- merge 之后，heavy 一定变成 light，light 可能变成 heavy
- 顺序插入 $2^k-1$ 个自然数，形成满树
- right path can be arbitrarily long

| Operation | FindMin     | DeleteMin        | Insert              | DecreaseKey   | Merge              |
| --------- | ----------- | ---------------- | ------------------- | ------------- | ------------------ |
| Binary    | $\Theta(1)$ | $\Theta(\log n)$ | BuildHeap in $O(n)$ | $O(\log n)$   | $\Theta(n)$        |
| Skew Heap | $\Theta(1)$ | $\Theta(\log n)$ | $\Theta(\log n)$ \* | $O(\log n)$\* | $\Theta(\log n)$\* |

### 1.2.3 Binomial Queue

- $\Phi=\text{number of trees}$
- $\hat{c}=2$ for each insertion

### 1.2.4 Fib Heap

- 只有 deletemin 需要进行根链表合并，所以是 $O(\log N)$ 的，其他都是常数

## 1.3 Amortized Analysis

> 只要摊还开销大于总开销，都算是合理的摊还分析

- 势能函数的选择
	- 开始的时候最小 **assume its minimum**
	- 非负的
	- 摊还，也就是*简单操作会导致势能增大，复杂操作会导致势能减小，从而二者的复杂度一致*
	- 初始值可以不是 0

# 2 Algorithm

## 2.1 Inverted File Index

- terms
	- term dict, posting list
	- word stemming
	- stop words
	- distributed indexing
		- term-partitioned index
		- document-partitioned index
	- dynamic indexing
		- auxiliary index = cache
	- compression
		- term dict -> a single str
		- posting list -> 差分存储词首 char 的 index
	- measures
		- relevance measurement
		- precision
		- recall
- 交集查找从 frequency 最小的词开始
- hash 查找更快，但是无法范围查找
- term-partition 也不是没有用的
- thresholding
	- document-thresholding
		- 不方便布尔操作
		- 可能由于截断错过重要文件
	- query 只考虑部分 query

## 2.2 Backtracking

> backtracking 本身就有 eliminate 的含义

- 8-Queens
	- $N!$ solutions
- alpha-beta 剪枝
	- 如果有 N 个节点，可以减少到 $O(\sqrt{ N })$

## 2.3 Divide and Conquer

- method
	- 替代法
	- 递归树
	- 主方法

当 $a\ge 1,b\geq 1, p\geq 0$ 时，对于递推式：

$$T(N)=aT(N/b)+\Theta(N^k \log^p N)$$

1. if $a>b^k$, $T(N)=O(N^{\log_{b}a})$
2. if $a=b^k$, $T(N)=O(N^k \log^{p+1}N)$
3. if $a<b^k$, $T(N)=O(N^k \log^p N)$

## 2.4 Dynamic Programming

![[__assets/ADS Cheat Sheet/IMG-ADS Cheat Sheet-20250102222911289.webp]]

- floyd warshall 算法可以有负权，但是不能有负数圈

## 2.5 Greedy Algorithm

- Elements
	- 做出选择，剩下一个子问题需要解决
	- greedy choice property: 总有一个最优解是贪心选择得到的，参数交换法
	- optimal substructure property: 做出贪心选择后，总能得到最优子结构，即将贪心选择和子问题的最优解组合起来总是全局最优解

# 3 Algorithm Analysis

## 3.1 Complexity Class

- 最难的问题是不可判定问题
- 对于 NTM 来说，不可判定问题还是不可判定
- co-NP: 其补问题是 NP 问题的问题，四种情况中，反正 P 属于 co-NP 和 NP 的交集

| 问题                              | 复杂度类 | 判定含义                      | note                                                                 |
| ------------------------------- | ---- | ------------------------- | -------------------------------------------------------------------- |
| Set Cover                       | NP-C | 判定是否存在大小为 $k$ 的 set cover |                                                                      |
| Circuit-SAT                     | NP-C | 对于一个布尔表达式，判定是否存在一组赋值使其为 1 | 最早被证明是 NP-C 的问题                                                      |
| SAT                             | NP-C |                           |                                                                      |
| Hamiltonian Cycle               | NP-C | 判定一张图是否存在哈密顿回路            | 判定一个图是否**没有**哈密顿回路的问题不是 NP 的                                         |
| Clique                          | NP-C | 判定一张图是否存在大小至少为 k 的团       |                                                                      |
| Knapsack                        | NP-C |                           |                                                                      |
| Bin Packing                     | NP-C |                           |                                                                      |
| Domination Set                  | NP-C |                           |                                                                      |
| DNF-SAT                         | P    | 给定 DNF，判定是否能够满足           | 甚至是线性的复杂度                                                            |
| Longest Distance in Acyclic DAG | P    |                           |                                                                      |
| TSP                             | NP-C | 判定一张图是否存在 cost 不超过 k 的路线  | 要证明 TSP 是 NP-C，需要证明它是 NP，并且可以由哈密顿回路归约得到                              |
| Vertex Cover Problem            | NP-C | 判定一张图是否存在大小至多为 k 的顶点覆盖    | 首先是 NP 的，其次可以由一支 NP-C 的 Clique 问题归约得到<br>这是用补图来证明的，规约算法复杂度为 $O(N^2)$ |
| 3-CNF SAT                       | NP-C |                           |                                                                      |
| Subset Problem                  | NP-C |                           |                                                                      |
| Partition Problem               | NP-C |                           |                                                                      |
| Domination Set                  | NP-C |                           |                                                                      |

## 3.2 Approximation

- FPTAS 就是 n 的指数和 epsilon 无关了
- binpacking
	- NF(2): 1, epsilon, 1, epsilon, 1 epsilon
	- FF(1.7): 如果删掉一个，可能结果会更差

![[__assets/ADS Cheat Sheet/IMG-ADS Cheat Sheet-20250102232014723.webp]]

| 问题              | 优化含义                       | 算法                      | 近似比                                                             | 停止复杂度                                             | note                                                                                              |
| --------------- | -------------------------- | ----------------------- | --------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Bin Packing     | general online             | **online lwb**          | 1.67                                                            |                                                   | 课件给的，存在一种输入，能让所有 online 都无法低于 1.67                                                                |
|                 |                            | FF                      | 2                                                               |                                                   | $O(\|L\|)$                                                                                        |
|                 |                            | NF                      | 1.7                                                             |                                                   |                                                                                                   |
|                 |                            | BF                      | 1.7                                                             |                                                   |                                                                                                   |
|                 |                            | Refined Harmonic        | 1.63597 (asmy)                                                  |                                                   |                                                                                                   |
|                 |                            | Modified Harmonic 2     | 1.61217 (asmy)                                                  |                                                   |                                                                                                   |
|                 |                            | **online asym lwb**     | 1.5407                                                          |                                                   |                                                                                                   |
|                 | general offline            | **lwb**                 | 1.5                                                             |                                                   |                                                                                                   |
|                 |                            | AnyFit                  | 11/9(1.22) ~ 1.25 *asym*                                        |                                                   |                                                                                                   |
|                 |                            | FFD                     | 11/9 OPT + 6/9 (tight) *asym*                                   |                                                   |                                                                                                   |
|                 |                            | NFD                     | 仅仅略微小于 1.7                                                      |                                                   |                                                                                                   |
|                 | 2 item sizes               | FF                      | 2                                                               |                                                   |                                                                                                   |
|                 |                            | NF/BF                   | 1.5 (not tight)                                                 |                                                   |                                                                                                   |
| Knapsack        |                            | EnumerateGreedy<br>贪心枚举 | $1+\varepsilon$<br>$K=\varepsilon \frac{p_{\max}}{n}$           |                                                   | FPTAS                                                                                             |
| K-center        | general                    |                         | $\infty$                                                        |                                                   |                                                                                                   |
|                 | metric distance<br>最小化最大距离 | greedy 第一个点选择最中心的位置     | $\infty$                                                        |                                                   |                                                                                                   |
|                 |                            | greedy 2-r              | ?                                                               |                                                   |                                                                                                   |
|                 |                            | greedy 2-r far away     | 2                                                               |                                                   |                                                                                                   |
|                 |                            | LWB                     | 2                                                               |                                                   | 除非 P=NP，因为小于 2 的近似比可以归约到 dominating set 问题的多项式时间算法；<br>*如果 r(C\*)=1，则 dominating set 有 size K 的解* |
| Max-Cut         |                            | state-slipping          | 2                                                               | **可能无法多项式时间**                                     |                                                                                                   |
|                 |                            |                         | 如果使用 $\frac{2\varepsilon}{\|V\|}w(A,B)$ 梯度更新，就是 $2+\varepsilon$ | $O(\frac{n}{\varepsilon}\log W)$<br>yes! 实现了多项式时间 | W 是所有权重之和<br>这个翻转次数是因为初始最小为 1，每翻转 $n/\varepsilon$ 后权重一定翻倍，最大到 $W$                                 |
|                 |                            | best                    | 1.1382                                                          |                                                   |                                                                                                   |
|                 |                            | P=NP                    | $17/16\approx1.0625$                                            |                                                   |                                                                                                   |
|                 | 只有 1 2 两种边长                |                         | $8/7$                                                           |                                                   |                                                                                                   |
|                 | 最长回路                       | 确定算法                    | $4/3$                                                           |                                                   |                                                                                                   |
|                 |                            | 随机算法                    | $(33+\varepsilon)/25$                                           |                                                   |                                                                                                   |
| Set Cover       | unweighted                 | greedy，每次挑选具有最多未覆盖元素的集合 | $\ln n-\ln \ln n+\Theta(1)$                                     |                                                   |                                                                                                   |
|                 | weighted                   |                         | $O(\log n)$                                                     |                                                   |                                                                                                   |
| Vertex Cover    | 找到最小的顶点覆盖，可以规约到最大独立集       | 每次找一条边，然后删除两个顶点         | $2-\Theta(1/\sqrt{ \log\|V\| })$                                |                                                   |                                                                                                   |
|                 |                            | 每次找最大度数的顶点删除            | $\Omega(\log n)$                                                |                                                   |                                                                                                   |
|                 |                            |                         | $2/(1+\delta)$ in $\delta$-dense graph                          |                                                   |                                                                                                   |
| Independent Set | general                    |                         | 不存在常数近似比                                                        |                                                   |                                                                                                   |
|                 | planar graph               |                         | 任意接近 1 但不等于                                                     |                                                   |                                                                                                   |
|                 | bounded degree             |                         | $(\Delta+2)/3$                                                  |                                                   | $\Delta$ 是最大度数                                                                                    |

## 3.3 Local Search

- metropolis
- simulated annealing
- hopfield neural networks
	- definition
		- good edge: 如果边权重和两个顶点赋值乘积是负数
		- satisfied vertex: 如果这个顶点的 good edge 的总权重大于 bad edge 的总权重
		- stable config: 如果所有的顶点都是 satisfied 的
		- 不一定存在 stable config
		- 找到一个稳定 config，或者是能量足够小的 config
	- state-flipping
		- 随便找一个不满意的点，然后翻转其赋值
		- **最多 $W=\sum_{e}|w_{e}|$ 次迭代**
		- 势能函数 $\Phi(S)=\sum_{e\text{ is good}} |w_{e}|$
			- 每次翻转至少增加 1
			- $0\leq \Phi\leq W$
		- 任何局部最优解都是稳定的 config
- max-cut