---
MkDocs_comments: true
date_created: 2024-06-26 01:41:07
date_modified: 2025-01-31 17:58:26
is_published: true
state:
- 待发布
- 归档
type:
- note
---
# Mistakes

## True of False

1.  If a queue is implemented by a circularly linked list, then the insertion and deletion opetations can be performed with one pointer **rear** insetad of **rear** and **front** ***T***

# Cheat Sheet

## Tricky points

- 树的类型
	- full
	- complete
	- perfect
	- balanced

在二叉树中，有几个常见的类型需要区分：完全二叉树（complete binary tree）、满二叉树（full binary tree）、完美二叉树（perfect binary tree）和平衡二叉树（balanced binary tree）。下面是每种类型的详细解释：

> [!NOTE]- 不同的二叉树
> 1. **完全二叉树（Complete Binary Tree）**：
>    - 定义：完全二叉树是一棵二叉树，其中所有层（除了可能的最后一层）都是满的，且所有节点尽可能地靠左排列。
>    - 特点：在完全二叉树中，每一层的节点都是从左到右填满的，但最后一层的节点不一定填满。
>    - 例子：
>      ```
>            1
>          /   \
>         2     3
>        / \   /
>       4   5 6
>      ```
> 
> 2. **满二叉树（Full Binary Tree）**：
>    - 定义：满二叉树是一棵二叉树，其中每个节点要么有两个子节点，要么没有子节点。
>    - 特点：每个节点要么是叶子节点，要么有两个子节点。
>    - 例子：
>      ```
>            1
>          /   \
>         2     3
>        / \   / \
>       4   5 6   7
>      ```
> 
> 3. **完美二叉树（Perfect Binary Tree）**：
>    - 定义：完美二叉树是一棵二叉树，其中所有内节点都有两个子节点，且所有叶子节点都在同一层。
>    - 特点：完美二叉树既是满二叉树又是完全二叉树。它的所有叶子节点在同一层，并且所有内节点都有两个子节点。
>    - 例子：
>      ```
>            1
>          /   \
>         2     3
>        / \   / \
>       4   5 6   7
>      ```
> 
> 4. **平衡二叉树（Balanced Binary Tree）**：
>    - 定义：平衡二叉树是一棵二叉树，其中任何节点的两个子树的高度差不超过 1。
>    - 特点：为了保证查询操作的效率，树的高度尽量保持在最低水平。常见的平衡二叉树有 AVL 树和红黑树。
>    - 例子：
>      ```
>            3
>          /   \
>         2     4
>        /       \
>       1         5
>      ```
> 
> ### 总结
> - **完全二叉树**：从左到右逐层填满，可能最后一层不完全。
> - **满二叉树**：每个节点要么有两个子节点，要么没有子节点。
> - **完美二叉树**：所有内节点都有两个子节点，所有叶子节点在同一层。
> - **平衡二叉树**：任何节点的两个子树高度差不超过 1。

## [[Ch.02 Algorithm Analysis]]

- $T(N)=O(f(N))$ 上界，小于等于
- $T(N)=\Omega(g(N))$ 下界，大于等于
- $T(N)=\Theta(h(N))$ 确界，表示上下界同阶
- $T(N)=o(p(N))$ **严格渐进上界**，严格小于

## [[Ch.03 List]]

- ADT 的概念
- Sequential List
	- Imp
		- Array
		- Linked List
		- [[Ch.03 List#2.3.3 Cursor Implementation of Linked Lists (no pointer)|Cursor Imp]]
	- App
		- 多项式表示
		- Multilists 矩阵稀疏表示
- **Stack ADT**
	- 链表实现、数组实现、dummy head node
	- 应用
		- Balancing Symbols 符号检查
		- Postfix Evaluation 逆波兰表达式求值
		- Infix to Postfix Conversion *优先级>=当前元素，出栈*，**注意括号**
- **Queue ADT***
	- 循环队列实现
	- `rear` 和 `front` 差 2 是满，差 1 是空
	- 最大容量是 `n-1`
	- `Enqueue` 在 `++rear` 放入元素
	- `Dequeue` 在 `fornt++` 删除元素
	- 需要执行满/空检查

## [[Ch.04 Trees]]

- Preliminaries
	- Degree
	- parent, children sibilings, leaf
	- **Path** 只能是从上往下的
	- Depth, height(The length of the *longest* path from this node to a leaf) *深度就是往根找的长度，高度就是作为根往叶子找的长度*
	- ancestors, descendants
- Imp
	- 可以用线性表表示 *因为内存就是线性的，没有什么数据结构不能线性表示*
	- FirstChild-NextSibiling 表示，所有的树都能等价为 binary tree，但是 *unordered tree 表达可能不唯一*
		- preorder 还是 preorder，但是 **postorder 变成了 inorder**
- **Binary Tree**
	- App
		- Expression Tree (syntax trees)
	- Traversals
		- preorder postorder inorder *levelorder (需要队列)*
			- `iter_inorder` **使用一个栈完成非递归遍历**
		- expression tree 不同的遍历方式就能得到不同的表达式
		- print directory 使用 **preorder**，因为先打印父目录
		- 计算文件夹大小，使用 **postorder**，因为要向父节点返回值
	- 线索二叉树（几乎不考） *如果 `left` 为空，换成中序遍历的前驱，如果 `right` 为空，换成中序遍历的后继，只是方便查找而已*
	- 其他二叉树
		- 斜树 skewed binary tree，退化成线性结构
		- 完全 complete binary tree **除了最后一层，全部填满** *很像堆*
	- properties
		- 叶子节点数比二度节点数多 1 $n_0=n_2+1$
- **The Search Tree ADT**
	- Imp
		- `find` 尾递归优化为循环的例子
		- `insert` 的递归操作需要返回 
		- `Delete`
			- **如果是二度节点，替换为左子树最大或右子树最小**，对被换过来的节点递归进行 `delete`
			- lazy deletion
	- $height(bst)\in[h-1,\lceil\log_2(n+1)\rceil-1]$

## [[Ch.05 Priority Queues (Heaps)]]

- sentinel value 是不可能出现的最小/最大值
- `insert` 放到末尾，`PercolateUp`
- `DeleteMin` 末尾放到开头，`PercolateDown`
- `DecreaseKey` 直接 `PercolateUp`
- `IncreaseKey` 直接 `PercolateDown`
- `Delete` 删除某个位置的元素： `DecreaseKey \infty` 然后进行 `DeleteMin`
- `BuildHeap` 直接放，然后堆每个父节点 `PercolateDown`
	- 也称为 **Linear Algorithm** $T(N)=O(N)$

## [[Ch.06 Sorting]]

- **Insertion Sort** 插入排序 ***stable***
	- best case $O(N)$
- Lower bound for simple sorting algorithm: Any sorting algirithm that sorts by *exchanging adjacent elements* requires $\Omega(N^2)$ *on average*
- **Shellsort** 希尔排序 ***Shellsort is unstable***
	- Naive Shellsort: h 每次除 2
		- worst case $\Theta(N^2)$
	- Hibbard's increments
		- worst case $\Theta(N^{3/2})$
		- *conjucture*: avg $O(N^{5/4})$
	- Sedgewick's best sequence
		- *conjucture*: avg $O(N^{7/6})$, worst $O(N^{4/3})$
- **Heapsort** 堆排序 ***unstable***
	- 平均比较次数 $2N\log N-O(N \log \log N)$
	- 使用不经济，常数比较大
- **Mergesort** 归并排序 ***Mergesort is stable***
	- 递归外部定义 `TmpArray`
		- 如果内部定义 $S=O(N\log N)$
		- 如果外部定义 $S=O(N)$
	- 进行划分
	- 每一次归并，从 `A` 读取，放到 `TmpArray` 中，然后再复写到 `A`
- **Quicksort** 快速排序 ***unstable***
	- 复杂度
		- Time: *best/average case* $O(N\log N)$ *worst case* $O(N^2)$
		- Space: *best* $O(\log N)$ *worst* $O(N)$
	- Strategy
		- `pivot` 使用 `Medium3` 来获取
		- 在 partition 中，如果 `key == pivot` 都停下俩进行 `swap`，这样能够保证 partition 大小相近，时间还是 $O(N\log N)$
	- ***Quicksort is slower than insertion sort for small $N\le 20$***
- **Table Sort**
	- 创建 pointer 来处理大型结构，pointer 就是 key，然后堆
	- Every permutation is made up of disjoint cycles
	- worst case, $\lfloor N/2\rfloor$ cycles and $\lfloor 3N/2\rfloor$ record moves
	- $T=O(mN)$ where $m$ is the size of the structure
- A general lower bound for sorting based on comparisons $O(N\log N)$
- **Bucket Sort** ***stable***
	- 设计所有可能的 `slot`，直接放入
- **Radix Sort** ***stable***
	- 进行多轮排序，每次排一个数位，**Least Significant Digit First**
	- $T=O(P(N+B))$
		- $P$ 是 number of passes，也就是位数
		- $B$ 是 number of buckets
	- MSD Approach: *Parallel sort*
	- LSD Approach: serial sort

## [[Ch.07 Hashing]]

- Identifier density $n/T$
- loading density $n/(sb)$
- collision: $f(key_1)=f(key_2),\,key_1\ne key_2$
- $f(x)=(\sum x[N-i-1]*32^i)\%TableSize$
- **Separate Chaining**: 头插法
- **Open Addressing** $index=(hash(key) + f(i)) \% TableSize$ **注意只有 i 在增加**
	- *Linear Probing*
	- *Quadratic Probing*
		- If quadratic probing is used, and the table size is **prime**, then a new element can always be inserted if the table is **at least half empty**.<br>表的大小为质数，那么如果表至少半空的话，一定可以插入
		- 如果是质数而且可以写成 $4 k+3$，且采用 $f(i)=\pm i^2$，那么只要有空位就行
	- *Double Hashing* $f(i)=i*hash_2(x)$ 第二个哈希函数

## [[Ch.08 Disjoint Set]]

- Basic worst case $\Theta(N^2)$, skewed tree, where 1 = 2, 2 = 3, 3 = 4, ...
- Smart Union Algorithm 都叫做 *Union-by-rank*
	- *Union-by-size* 搭配 *Path-Compression*
	- *Union-by-height*
- $\alpha$ 反 Ackermann 函数，几乎等于常数
- 如果有 $M$ 个 find，$N-1$ 个 unions，$T=O(M\alpha(M,N))$

## [[Ch.09 Graph Algorithms]]

- Definitions
	- complete
	- path
		- simple path
		- cycle
	- connected graph / component
	- tree 连通无环图
	- DAG: 有向无环图
	- Strongly/Weekly connected
- Representation
	- `adj_mat`
	- `adj_lists`
	- `adj_multilists`，每一个节点是一条边，存着起点和终点以及 `mark`，两个出指针指向各自 vertex 连接的下一条边
- **Topological Sort** 拓扑排序
	- 使用一个队列
	- $T=O(|V|+|E|)$
		- 因为要遍历所有边，统计入度
		- 也要遍历所有点，进行删除
- **Shortest Path Algorithms** Dijkstra Algorithm
	- *unweighted*: 使用一个 queue 来记录“探索外延”的 vertex
	- *weighted* **Dijkstra**
		- 每次都遍历，better if graph is dense
			- $T=O(|E|\log |V|)$
		- 建立 MinHeap，better if graph is sparse
			- $T=O(|E|\log|V|)$
			- 但是需要额外的 $S=O(|E|)$，以及需要执行 `deleteMin`
	- *graph with negative costs*: 可能存在解，可能死循环
- **AOE Networks**
	- **EC**: earliest completion ***从头到尾取最大***
	- **LC**: lastest completion ***从尾到头取最小***
	- **Critical Path**: 没有松弛时间的路径
- **Network Flow Problems** 网络流问题
	- Flow Network $G_f$
	- Residual Network $G_r$
	- 每一次，在 $G_r$ 中找到一条通路，那么更新这条通路上瓶颈处的流量到 $G_f$，并且在 $G_r$ 中更新剩余流量和反向流量
	- analysis
		- $T=O(f*|E|)$
- **Minimum Spanning Tree** 最小生成树
	- *Prim* 从一个节点开始，收集边
		- $O(|V|^2)$ 或者使用了更高级的图表示的话 $O(|E|\log|V|)$ or $O(|V|\log|E|)$ 适合 **Dense Graph**
	- *Kruskal* 从森林开始，找最小的边将它们连接起来
		- $T=O(|E|\log|E|)$ 适合在 **Sparse Graph**
- **DFS** *[[Ch.09 Graph Algorithms#6.2.1.1 Use DFS to obtain a spanning tree of G|Use DFS to obtain a apanning tree of G]]*
	- *Biconnectivily* 不存在割点的图
	- **求解 biconnected components**
		1. 使用 DFS 获得一个 spanning tree
			1. 其中有 DFS 编号，也就是 $Num(v_i)$
			2. 其中存在 *back edge*，也就是树里没有但是图里有的边
		2. 找到所有的割点
			1. 什么是割点
				1. *root*，至少有两个孩子
				2. 其他点，至少有一个孩子，而且不能通过后代的 *back edge* 回到祖先
			2. $Low(u)$ 自己的 Num，孩子的 Low，back edge 另一边的 Num 的**总最小值**
		3. 得出结果
			1. 如果是 root，那么至少两个孩子
			2. 或者如果是其他点，至少有一个孩子的 Low 比自己的 Num 大就好
	- **Euler Circuits** $T=O(|E|+|V|)$

# 历年卷

## 15-16 秋冬期末模拟 二叉树检查

- binary search tree 要求每一个根节点大于左子树最大的，小于右子树最小的
- 使用递归，同时进行判断和深度计算 `cbst(BinTree T, int height, int max, int min)`
- 使用全局变量 `int in_seq[1000] = {0}, top = -1, mheight = 0, valid = 1;`
- 使用 `stdlib.h` 中的 `qsort`，可以很方便找到 K 小的元素

> [!hint] `qsort` 使用示例
> ```c
> int cmp(const void *a, const void *b){
>     return *(int*)a - *(int*)b;
> }
> 
> int main(void)
> {
>     int seq[1000];
>     for(int i = 0; i < 1000; i++) seq[i] = rand();
>     qsort(seq, 1000, sizeof(int), cmp);
>     for(int i = 0; i < 1000; i++) printf("%d\n", seq[i]);
>     return 0;
> }
> ```

```c
int cmp(const void* a, const void* b)
{
	return *(int*)a - *(int*)b;
}

qsort(thisSeq, 1000, sizeof(int), cmp);
```

## 16-17 秋冬期末模拟 最小共同祖先问题

- 先确定最小祖先，只需要找到第一个分叉点即可，也就是与子树根节点比较发现一个大一个小，或者出现一个等于的时候
- 然后验证合理性，从这个公共顶点开始搜两个值，如果都搜到了，说明有效，返回公共祖先的 `key`；如果有一个没搜到，都返回 `ERROR`

## 19-20 秋冬期末模拟 Complete Binary Search Tree

- 建立一个 BST
- 判断是否 Complete
- 给出 preorder traversal sequence

> [!hint] 思路
> - 首先，如何表示树的结构？
> 	- 使用数组进行表示，根的下标取 0
> 	- 注意将数组初始化成 `-1` 表示未占用
> - 然后，进行 `insert` 递归操作

