---
type: 
status: 
tags: 
aliases: 
created: 2024-05-07T02:17:59
updated: 2024-07-07T10:48:11
---
# HW

## HW 8

1. If a directed graph G=(V, E) is weakly connected, then there must be at least |V| edges in G. **F**
	1. weak / strong connection
		1. 弱连接指的是存在一条路径，经过两点
		2. 强连接指的是，从 A 出发可以到 B，从 B 出发也可以到 A
	2. 应该是 |V|-1，只要有 undirected path 就行
2. Given the adjacency list of a directed graph as shown by the figure. There is(are) __ strongly connected component(s).
	1. 注意单个 vertex 也算是子图
	2. 首先看哪些节点没有入或者没有出的，一定是单节点的子图

### 函数题：Is Topological Order

#### idea 1

- 遍历，建立 `cntIndegree[num]` 保存入度，**记得初始化为**
- 遍历输入，对于每个输入，如果对应 `cntIndegree` 是 0，则正确
	- 并将 successor 的入度减一
- 如果入度还不是 0 的节点被 visit，则不正确，退出 false

##### test

- 错误了，因为**AdjV 里的节点编号也是从 0 开始的**
- 修改之后就正确了

### 编程题：Hamiltonian Cycle

#### idea 1

- 建立图，adjmat/adjlist?
	- 边界为 200 vertices，40000 个 int，预计占用 2^18 byte，空间足够，使用完全 adjmat
- 对于每一个输入 query
	- 首先数量需要是 Nv+1 以上
	- 然后首尾相同
	- 其次需要包含所有数字
	- 再次检查是否都可以连通

> [!attention] 关于循环控制语句
> C 语言中没有能够直接 `break` 或者 `continue` 上层循环的用法，需要用一个 `flag` 来传递循环控制操作！

## HW 9

- In a weighted undirected graph, if the length of the shortest path from `b` to `a` is 12, and there exists an edge of weight 2 between `c` and `b`, then the length of the shortest path from `c` to `a` must be no less than 10.
	- **T**
	- 如果 less than 10 的话，`b` to `a` 的最短就比 12 还小了

## HW 10

### 7-1 Universal Travel Sites

- **就是最大网络流问题**，但是加上了字符串，最好有字典，或者使用 python
- 思路
	- 读图
		- 边里直接存节点名称，全部使用 strcmp，可以避免字典，*这里用 python 来实现*
		- 每个边同时存储 $G_r, G_f$
	- unweighted 路径搜索，返回路径 *直到搜不到 break*
	- 根据路径更新 $G_r, G_f$

**总之，灵活切换 python 来实现是正确的选择**

### Uniqueness of MST

- 具有相同**拓扑结构**的 MST 就是相同的
	- 任何一棵树都可以 **reroot**，但是**边集不变**
	- 只要**边集相同**，就认为 MST 相同

> [!NOTE] 如果能够建立最小生成树，如何判断是否唯一？
> 如果出现了相同权重的

#### idea

- 对 edge 按照 weight 升序排列
- 使用并查集，路径压缩，遍历 edge
	- 对于路径长度 d
		- 首先对所有的长度为 d 的路径进行分析，是否能够加入图中 *是否成环*，并进行记录
		- 然后进行逐个加入
- 最后看看**如果存在可能加入 MST 但是实际上没有加入**的路径，那么 MST 不唯一

##### 注意

- 需要使用快速排序，不然超时
- 实现过于麻烦

## HW 11

- Apply DFS to a directed acyclic graph, and output the vertex before the end of each recursion. The output sequence will be: **reversely topologically sorted**
	- 因为是在返回的时候打印的，而 DFS 的顺序是顺着拓扑排序深入的
	- *注意* 有向无环图就是树，这就是树的 DFS
- Use simple insertion sort to sort 10 numbers from non-decreasing to non-increasing, the possible numbers of comparisons and movements are:
	- 一共有 45 个逆序对，所以交换的次数不会大于 45
	- 选 D. 45, 44

### 函数题：Strongly Connected Components

- 注意不是连通是 **digraph 强连通**，所以不是简单的 [[Blog/mkdocs-blog-project/emergent-space-obmd/Fundamentals of Data Structure/Ch.09 Graph Algorithms#Undirected Graphs]]

#### Idea

> [!hint] 如何找到某个顶点所在的 SCC ?
> - 首先，一个 SCC 的定义是，内部所有两个顶点之间都存在双向路径
> 	- 那么 V 可以找到其他所有节点，其他所有节点也可以找到 V
> 	- 满足上面这个条件，其他节点**就可以相互找到**，*使用 V 作为跳板*
> - 所以得到了 SCC 的 **充要条件**

- for all V in G
	- if not visited
		- find the SCC it is in `getStronglyConnectedComponent()`
		- print(\n)
- `getSCC(Graph G, Vertex V)`
	- V 出发能找到的节点构成集合 From
	- 能找到 V 的节点构成集合 To
	- 取交集，加上 V 本身，就是 V 所在的最大 SCC
- **使用 `adj_mat` 利用 Warshall 算法可以更加方便地解决**
	- 对于 `adj_mat` 使用 Warshall 算法，得到目标矩阵
	- 对于每个 unvisited 的顶点 V
		- **取矩阵里第 V 行和第 V 列的 AND**
			- 这个结果就是 V 所在的 SCC
		- visit SCC 内所有的顶点 *打印，标记*