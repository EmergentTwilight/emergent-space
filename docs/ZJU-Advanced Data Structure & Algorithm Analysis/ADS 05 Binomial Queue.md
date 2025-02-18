---
MkDocs_comments: true
date_created: 2024-09-30 03:07:46
date_modified: 2025-02-16 02:05:59
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
tags:
- Data-Structure/Priority-Queue/Binomial-Queue
- Data-Structure/Priority-Queue/Fibonacci-Heap
---
# 1 Structure

- Not a heap-ordered tree, but rather a **colloction** of heap-ordered trees, **forest**

![[__assets/ADS 05 Binomial Queue/IMG-ADS 05 Binomial Queue-20241028013906675.webp]]

- $B_k$ properties
	- $k$ children, which are $B_0, B_1, B_2, \dots, B_{k-1}$
	- 由两个 $B_{k-1}$ 构成，一个接在另一个的根上
	- 有 $2^k$ 个节点
	- 深度为 $d$ 的节点有 $C^d_k$ 个，*Binomial coefficient*

![[__assets/ADS 05 Binomial Queue/IMG-ADS 05 Binomial Queue-20241028013928477.webp]]

> [!NOTE] 
> A priority queue of *any size* can be uniquely represented by a collection of binomial trees.

## 1.1 Definition

- **Binomial Tree** *(recursive definition)* $B_i$: 两个 $B_{i-1}$，让其中一个是另一个的根节点的孩子
- **Binomial Queue**: $B_i$ 的列表，实际是一个 **forest**

> [!attention] 
> 我们不使用 **binomial heap** 这个词，否则可能指代不清

# 2 Operations

## 2.1 FindMin

- at most $\lceil \log N \rceil$ roots, so $O(\log N)$
- keep record of the min, update whenever the tree is changed, then $O(1)$

## 2.2 Merge

![[__assets/ADS 05 Binomial Queue/IMG-ADS 05 Binomial Queue-20241028013941261.webp]]

- 使用二进制加法得到目标森林的结构
- 直接将同阶的数组合成一颗更大的树，完成合并
- $T(N)=O(\log N)$

> [!NOTE] 
> keep trees in the bq *sorted by height*, so that one traversal is enough

## 2.3 Insert

> 也就是二进制加 1

- 单次插入
	- $T_{worst}=O(\log N)$
	- $T_{avg}=O(1)$
- 均摊开销 $T_{amortized}=\Theta(1)$

## 2.4 DeleteMin

![[__assets/ADS 05 Binomial Queue/IMG-ADS 05 Binomial Queue-20241028013951646.webp]]

1. 找最小 $O(\log N)$ or $\Theta(1)$，取决于是否保存了最小元素的指针
2. 将这棵树拆散放到新的队列中 $O(\log N)$
3. 加法 $O(\log N)$

## 2.5 Conclusion

| Operation      | FindMin     | DeleteMin        | Insert              | DecreaseKey      | Merge              |
| -------------- | ----------- | ---------------- | ------------------- | ---------------- | ------------------ |
| Binary         | $\Theta(1)$ | $\Theta(\log n)$ | BuildHeap in $O(n)$ | $O(\log n)$      | $\Theta(n)$        |
| Leftist Heap   | $\Theta(1)$ | $\Theta(\log n)$ | $\Theta(\log n)$    | $O(\log n)$      | $\Theta(\log n)$   |
| Skew Heap      | $\Theta(1)$ | $\Theta(\log n)$ | $\Theta(\log n)$ \* | $O(\log n)$\*    | $\Theta(\log n)$\* |
| Binomial Queue | $\Theta(1)$ | $\Theta(\log n)$ | $\Theta(1)$\*       | $\Theta(\log n)$ | $O(\log n)$        |
| Skew Binomial  | $\Theta(1)$ | $\Theta(\log n)$ | $\Theta(1)$         | $\Theta(\log n)$ | $O(\log n)$        |

> `*` is amortized time.

> [!NOTE] Skew Binomial Queue
> 第 $k$ 个树的容量为 $2^{k+1}-1$，而不是 $2^k$。这样带来的最大好处就是，每次 insert 一个节点时，最多只需要 carry 一次，能做到 $\Theta(1)$ 的 worst-case insert 时间。
> 
> ![[__assets/ADS 05 Binomial Queue/IMG-ADS 05 Binomial Queue-20241028014012921.webp]]
> 
> For example, 60 is represented as 11200 in skew binary (31 + 15 + 7 + 7), and adding 1 produces 12000 (31 + 15 + 15). Since the next higher digit is guaranteed not to be 2, a carry is performed at most once.[^1]

# 3 Implementation

> Binomial queue = **array** of binomial trees

> [!hint] 从需求侧入手
> - DeleteMin 要拆树，需要能快速找到所有子树 -> 使用 First-child-next-sibling
> - Merge 需要孩子按照 size 大小进行排序 -> 按照 **decreasing order** 存储子树
> - 为什么不用数组？占用空间较大，而且不好扩容

![[__assets/ADS 05 Binomial Queue/IMG-ADS 05 Binomial Queue-20241028014033907.webp]]

```c title="Data Structure of Binomial Queue"
typedef struct BinNode *Position;
typedef struct Collection *BinQueue;
tyepdef struct BinNode *BenTree;

struct BinNode
{
	ElementType Element;
	Position LeftChild;
	Position NextSibling;
};

struct Collection
{
	int CurrentSize;  // total number of nodes
	BinTree TheTrees[ MaxTrees ];
}
```

## 3.1 Combine 2 Trees/Merge %% fold %% 

```c title="Combine 2 Trees"
BinTree CombineTrees( BinTree T1, BinTree T2 )
{
	if (T1->Element > T2->Element)
		return CombineTrees(T2, T1);  // attach the larger one to the smaller one
	// insert T2 to be the leftmost child of T1
	T2->NextSibling = T1->LeftChild;
	T1->LeftChild = T2;
	return T1;
}
```

> [!hint] 
> 从这里就能发现为什么 `LeftChild` 是最大的孩子了，这样方便树的合并操作；在合并时将根节点较大的一棵树直接当作 `LeftChild`，就不需要遍历所有 children。

```c title="Binomial Queue Merge"
BinQueue Merge( BinQueue H1, BinQueue H2 )
{
	BinTree T1, T2, Carry = NULL;
	int i, j;
	
	if (H1->CurrentSize + H2->CurrentSize > Capacity) ErrorMessage();
	H1->CurrentSize += H2->CurrentSize;
	
	for (i = 0, j = 1; j <= H1->CurrentSize; i++, j *= 2) {
		T1 = H1->TheTrees[i];
		T2 = H2->TheTrees[i];
		if (Carry == NULL) {
			if (T2 == NULL)  // do nothing
			else {
				if (T1 == NULL) {
					H1->TheTrees[i] = T2;
					H2->TheTrees[i] = NULL;
				} else {
					Carry = CombineTrees(T1, T2);
					H1->TheTrees[i] = H2->TheTrees[i] = NULL;
				}
			}
		} else {
			if (T2 == NULL) {
				if (T1 == NULL) {
					H1->TheTrees[i] = Carry;
					Carry = NULL;
				} else {
					Carry = CombineTrees(T1, Carry);
					H1->TheTrees[i] = NULL
				}
			} else {
				if (T1 == NULL) {
					Carry = CombineTrees(T2, Carry);
					H2->TheTrees[i] = NULL;
				} else {
					H1->TheTrees[i] = Carry;
					Carry = CombineTrees(T1, T2);
					H2->TheTrees[i] = NULL;
				}
			}
		}
	}

	return H1;
}
```

## 3.2 DeleteMin

```c title="DeleteMin"
void DeleteMin( BinQueue H )
{
	BinQueue DeletedQueue;
	Position DeletedTree, OldRoot;
	ElementType MinItem = Infinity;  // the min item to be returned
	int i, j, MinTree;
	
	if (IsEmpty(H)) { PrintErrorMessage(); return -Infinity; }

	/* Step 1: find the minimum item */
	for (i = 0; i < MaxTrees; i++) {
		if(H->TheTrees[i] && H->TheTrees[i]->Element < MinItem) {
			MinItem = H->TheTrees[i]->Element;
			MinTree = i;
		}
	}  // this can be optimized by maintaining a ptr to minterm in queue
	DeletedTree = H->TheTrees[MinTree];
	
	/* Step 2: remove MinTree from H, creating H' */
	H->TheTrees[MinTree] = NULL;
	
	/* Step 3.1: remove the root */
	OldRoot = DeletedTree;
	DeletedTree = DeletedTree->LeftChild;
	free(OldRoot);
	
	/* Step 3.2: create H'' */
	DeletedQueue = IntializeBinQueue();
	DeletedQueue->CurrentSize = (1<<MinTree) - 1;
	for (j = MinTree - 1; j >= 0; j--) {
		DeletedQueue->TheTrees[j] = DeletedTree;
		DeletedTree = DeletedTree->NextSibling;
		DeletedQueue->TheTrees[j]->NextSibling = NULL;
	}
	H->CurrentSize -= DeletedQueue->CurrentSize + 1;
	
	/* Step 4: merge H' and H'' */
	H = merge(H, DeletedQueue);
	
	return MinItem;
}
```

# 4 Amortized Analysis

> $Claim$: A binomial queue of $N$ elements can be built by $N$ successive insertions in $O(N)$ time.

## 4.1 Aggregate Method

![[__assets/ADS 05 Binomial Queue/IMG-ADS 05 Binomial Queue-20241028014045974.webp]]

### 4.1.1 推导方式 1

- 进行二进制 counting 时，进位操作发生的频率为 $\frac{1}{2^i}$，每次进位都算一次操作，*包括创建 $B_{0}$*
- 进行求和 $N\left( 1+\frac{1}{2}+\frac{1}{4}+\dots+\frac{1}{2^{\log N}} \right) \leq 2N=O(N)$

### 4.1.2 推导方式 2

- 如上图，`link=1` 每 4 次发生，`link=2` 每 8 次发生，......，`link=i` 每 $2^{i+1}$ 次发生
- 进行求和 $N+N\left( \frac{1}{4}+2\times \frac{1}{8} +3\times \frac{1}{16} + \dots\right) \leq 2N=O(N)$

## 4.2 Potential Method

根据上面的例子已经能够看出，势能函数可以定义为 $\Phi(H)=$ \# of binomial trees。

一次插入，如果开销为 $c$，那么 # of binomial trees 会增加 $2-c$，因此，每次操作的均摊开销 $\hat{c_{i}}=c_{i}+(\Phi_{i}-\Phi_{i-1})=2$。

$$
\sum_{i=1}^{\hat{N}}c_{i}+\Phi_{N}-\Phi_{0}=2N \Rightarrow \sum_{i=1}^N c_{i}=2N-\Phi_{N}\leq{2}N=O(N)
$$

Thus, $T_{worst}=O(\log N)$, but $T_{amortized}=2$

# 5 More about heaps/Extened reading %% fold %% 

1. [[1403.0252] A Back-to-Basics Empirical Study of Priority Queues (arxiv.org)](https://arxiv.org/abs/1403.0252) 这篇论文的测试方法、数学推导和分析都非常值得学习
2. [Fibonacci heaps 斐波那契堆_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1x54y1w7Y6/) Fibonacci Heaps 融合了很多数据结构的思想

## 5.1 Fibonacci Heap



```cpp title="a possible implementation"
#ifndef FIBONACCI_HEAP_H
#define FIBONACCI_HEAP_H

#include "Heap.hpp"
#include <cmath>
#include <list>
#include <unordered_map>
#include <vector>

using namespace std;

template <typename ValueType>
class FibonacciHeap : public Heap<ValueType>
{
private:
    // Node structure for the Fibonacci heap
    struct Node
    {
        ValueType value;
        int key;
        int degree;
        bool mark;
        Node *parent;
        list<Node *> children;

        // Constructor for the Node structure
        Node(ValueType value, int key)
            : value(value), key(key), degree(0), mark(false), parent(nullptr) {}
    };

    // Pointer to the minimum node in the heap
    Node *min_node;
    // List of root nodes in the heap
    list<Node *> root_list;
    unordered_map<ValueType, Node *> value_to_node;
    int node_count;

    // Consolidate the trees of the same degree
    void consolidate()
    {
        int max_degree = static_cast<int>(log2(node_count)) + 1;
        vector<Node *> degree_table(max_degree, nullptr);

        // iterate root list to consolidate trees of the same degree
        for (auto it = root_list.begin(); it != root_list.end(); it++)
        {
            Node *x = *it;
            int degree = x->degree;

            while (degree_table[degree] != nullptr)
            {
                Node *y = degree_table[degree];
                if (y->key < x->key)
                    swap(x, y);
                attach(y, x); // attach y to x
                degree_table[degree] = nullptr;
                degree++;
            }

            degree_table[degree] = x;
        }

        // rebuild root list
        min_node = nullptr;
        root_list.clear();
        for (Node *node : degree_table)
        {
            if (node)
            {
                root_list.push_back(node);
                if (!min_node || node->key < min_node->key)
                    min_node = node;
            }
        }
    }

    // Attach a child node to a parent node
    void attach(Node *target_child, Node *target_parent)
    {
        root_list.remove(target_child);
        target_parent->children.push_back(target_child);
        target_child->parent = target_parent;
        target_parent->mark = false;
        target_parent->degree++;
    }

    // Cut a child node from its parent node
    void cut(Node *child, Node *parent)
    {
        parent->children.remove(child);
        parent->degree--;
        root_list.push_back(child);
        child->parent = nullptr;
        child->mark = false;
    }

    // Perform cascading cut on a node
    void cascadingCut(Node *node)
    {
        Node *parent = node->parent;
        if (parent)
        {
            if (!parent->mark)
                parent->mark = true;
            else
            {
                cut(node, parent);
                cascadingCut(parent);
            }
        }
    }

public:
    // Constructor for the Fibonacci heap
    FibonacciHeap() : min_node(nullptr), node_count(0) {}

    // Insert a new node into the heap
    void insert(ValueType value, int key) override
    {
        Node *new_node = new Node(value, key);
        root_list.push_back(new_node); // lazy insertion
        if (!min_node || key < min_node->key)
            min_node = new_node;
        value_to_node[value] = new_node;
        ++node_count;
    }

    // Extract the minimum node from the heap
    pair<ValueType, int> extractMin() override
    {
        if (!min_node)
            throw "Heap is empty";

        Node *old_min_node = min_node;
        pair<ValueType, int> result = {old_min_node->value, old_min_node->key};

        // add children of the minimun node to root list
        for (auto child : old_min_node->children)
        {
            child->parent = nullptr;
            root_list.push_back(child);
        }

        // remove the min node
        root_list.remove(old_min_node);
        value_to_node.erase(old_min_node->value);
        delete old_min_node;

        if (root_list.empty())
            min_node = nullptr;
        else
        {
            min_node = *root_list.begin();
            consolidate();
        }

        --node_count;
        return result;
    }

    // Decrease the key of a node
    void decreaseKey(ValueType value, int new_key) override
    {
        if (value_to_node.find(value) == value_to_node.end())
            throw "Value not found in heap";

        Node *node = value_to_node[value];
        if (new_key > node->key)
            throw "New key is greater than current key";

        node->key = new_key;
        Node *parent = node->parent;

        if (parent && node->key < parent->key)
        {
            cut(node, parent);
            cascadingCut(parent);
        }

        if (node->key < min_node->key)
            min_node = node;
    }

    // Check if the heap is empty
    bool isEmpty() override
    {
        return root_list.empty();
    }
};

#endif // FIBONACCI_HEAP_H
```

### 5.1.1 Data Structure

- `root_list` 所有树的根节点列表
- `min_node*` 维护一个指向最小 key 节点的指针
- 每一棵树用 `list` 存孩子，每个节点存父节点指针，方便快捷访问

> [!NOTE] Data Structure
> ![[__assets/ADS 05 Binomial Queue/IMG-ADS 05 Binomial Queue-20241028014738550.webp]]
> ![[__assets/ADS 05 Binomial Queue/IMG-ADS 05 Binomial Queue-20241028014756607.webp]]

### 5.1.2 GetMin

维护指针 `Node* min_node`，所以 $O(1)$

### 5.1.3 Insert

- 直接添加到 `root_list` 作为一个根节点，所以 $O(1)$
- 均摊分析，每次会在 `ExtractMin` 的时候进行树的合并操作，$O(N)$，其中 $N$ 是插入节点的数量，所以单次插入的均摊时间为 $T_{amortized}=O(1)$

### 5.1.4 DecreaseKey

1. 根据 `unordered_map` 访问位置，$O(1)$
2. 进行 `cut` 和 `cascadingCut` 操作，可能有递归 $O(d)$，期中 $d$ 是节点的深度

### 5.1.5 ExtractMin

1. 找到 `min_node`，$O(1)$
2. 进行 `attach`，保证没有两棵树的 degree 相等，和 Binomial Queue 的二进制进位操作类似，$O(T)$，其中 $T$ 是树的数量

# 6 Questions

## 6.1 Q5

### 6.1.1 DeleteMin 时间复杂度

For a binomial queue, delete-min takes a constant time on average. (T/F)

> [!hint]- Answer
> **F** 是 $\Theta(\log n)$

### 6.1.2 Children order

To implement a binomial queue, the subtrees of a binomial tree are linked in increasing sizes. (T/F)

> [!hint]- Answer
> 为了使得合并时能快速找到根节点较大的一棵树的插入位置，应该从大到小保存孩子链表，使用**头插法**避免遍历链表

## 6.2 Ex5

### 6.2.1 Node count at odd/even depth

In a binomial queue, the total number of the nodes at even depth is always ___ than that of the nodes at odd depth (the root is defined to be at the depth 0).

> [!hint]- Answer
> $\geq$ 注意根节点深度是 0，所以 even 的更大

[^1]: Example taken from [Skew binomial heap - Wikipedia](https://en.wikipedia.org/wiki/Skew_binomial_heap)