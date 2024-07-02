---
type: 
status: 
tags: 
aliases: 
created: 2024-05-07T02:17:59
updated: 2024-05-22T11:38:31
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

> [!tip]- Code
> ```c
> bool IsTopSeq( LGraph Graph, Vertex Seq[] )
> {
>     int cntIndegree[Graph->Nv];
>     for(int i = 0; i < Graph->Nv; i++) cntIndegree[i] = 0;        // init
> 
>     for(int i = 0; i < Graph->Nv; i++){     // complete cntIndegree
>         PtrToAdjVNode p = Graph->G[i].FirstEdge;
>         for(; p != NULL; p = p->Next){
>             cntIndegree[p->AdjV]++;
>         }
>     }
> 
>     for(int i = 0; i < Graph->Nv; i++){     // read seq and judge
>         Vertex thisVertex = Seq[i]-1;
>         // check if its indegree is zero, if not, invalid, exit
>         if(cntIndegree[thisVertex]) return false;
>         // deduct the indegree of its successors
>         PtrToAdjVNode p = Graph->G[thisVertex].FirstEdge;
>         for(; p != NULL; p = p->Next){
>             cntIndegree[p->AdjV]--;
>         }
>     }
> 
>     return true;
> }
> ```
> 

### 编程题：Hamiltonian Cycle

#### idea 1

- 建立图，adjmat/adjlist?
	- 边界为 200 vertices，40000 个 int，预计占用 2^18 byte，空间足够，使用完全 adjmat
- 对于每一个输入 query
	- 首先数量需要是 Nv+1 以上
	- 然后首尾相同
	- 其次需要包含所有数字
	- 再次检查是否都可以连通

> [!tip]-  Code
> 
> ```c
> #include<stdio.h>
> #include<stdlib.h>
> 
> int main(void)
> {
>     int N, M, K;
>     scanf("%d %d", &N, &M);
>     int** adj_mat = (int**)calloc(N, sizeof(int*));     // init adjmat
>     for(int i = 0; i < N; i++) adj_mat[i] = (int*)calloc(N, sizeof(int));
> 
>     // read graph
>     for(int i = 0; i < M; i++){
>         int v 1, v 2;
>         scanf("%d %d", &v 1, &v 2);
>         adj_mat[v 1-1][v 2-1] = 1;
>         adj_mat[v 2-1][v 1-1] = 1;        // symmetric
>     }
> 
>     // main loop for query
>     scanf("%d", &K);
>     for(int i = 0; i < K; i++){
>         // read n and seq
>         int n; scanf("%d", &n);
>         int* seq = (int*)calloc(n, sizeof(int));
>         for(int j = 0; j < n; j++) scanf("%d", &seq[j]);
>         // if n is not equal to N + 1 OR head != tail, invalid
>         if(n != N + 1 || seq[0] != seq[n-1]) { printf("NO\n"); free(seq); continue; }
>         // if not all the vertices is included, invalid
>         int* map = (int*)calloc(N, sizeof(int));
>         for(int j = 0; j < n; j++) map[seq[j]-1]++;       // mark all the vertices included
>         int flag = 1;
>         for(int j = 0; j < N; j++) if(map[j] == 0) flag = 0;
>         free(map);
>         if(flag == 0) { printf("NO\n"); free(seq); continue; }
>         // else, check if all the path is valid
>         flag = 1;
>         for(int j = 0; j < n - 1; j++) if(adj_mat[seq[j]-1][seq[j+1]-1] == 0) flag = 0;
>         if(flag == 0) { printf("NO\n"); free(seq); continue; }
>         // finally, valid
>         printf("YES\n"); free(seq);
>     }
> 
>     for(int i = 0; i < N; i++) free(adj_mat[i]);
>     free(adj_mat);
>     return 0;
> }
> ```
> 

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

> [!tip]- Python code by Kimi
> ```python
> from collections import defaultdict
> 
> def bfs(graph, source, sink, parent):
>     visited = set()
>     queue = [source]
>     visited.add(source)
>     while queue:
>         node = queue.pop(0)
>         for next_node, (cap, flow) in graph[node].items():
>             if cap > 0 and next_node not in visited:
>                 parent[next_node] = node
>                 queue.append(next_node)
>                 visited.add(next_node)
>     return sink in visited
> 
> def dinic(graph, source, sink):
>     max_flow = 0
>     while True:
>         parent = {v: None for v in graph}
>         if not bfs(graph, source, sink, parent):
>             break
>         path_flow = float('inf')
>         node = sink
>         while node != source:
>             parent_node = parent[node]
>             path_flow = min(path_flow, graph[parent_node][node][0])
>             node = parent_node
>         max_flow += path_flow
>         node = sink
>         while node != source:
>             parent_node = parent[node]
>             graph[parent_node][node][0] -= path_flow  # 更新正向边的容量
>             if graph[node][parent_node]:  # 确保反向边存在
>                 graph[node][parent_node][0] += path_flow  # 更新反向边的容量
>             else:
>                 graph[node][parent_node] = [path_flow, 0]  # 添加反向边
>             node = parent_node
>     return max_flow
> 
> def main():
>     (source, sink, N) = input().split()
>     N = int(N)
>     graph = defaultdict(dict)
>     for _ in range(N):
>         (u, v, cap) = input().split()
>         cap = int(cap)
>         graph[u][v] = [cap, 0]
>         # 确保反向边存在，如果没有则初始化容量为 0
>         if not graph[v].get(u, False):
>             graph[v][u] = [0, cap]
>     print(dinic(graph, source, sink))
> 
> main()
> ```

> [!tip]- My code
> ```python
> from collections import defaultdict
> 
> # bfs for unweighted graph
> def unweighted(graph, source, sink, path):
>     visited = set()   # use set to store visited nodes
>     queue = [source]   # use queue, init source in queue
>     visited.add(source)   # mark source visited, depth: 0
>     while queue:   # until queue is empty
>         thisNode = queue.pop(0)
>         for nextNode, cap in graph[thisNode].items():   # get all the adjacents
>             if nextNode not in visited and cap > 0:   # find a valid path to nextNode
>                 path[nextNode] = thisNode
>                 queue.append(nextNode)   # enqueue, for next search
>                 visited.add(nextNode)
>     return sink in visited   # true or false, if sink in visited, path is valid
> 
> def maxCapacity(graph, source, sink):
>     cntFlow = 0   # to count total flow
>     while True:
>         # unweighted
>         path = {v: None for v in graph}   # init a dict, to store the paths
>         if not unweighted(graph, source, sink, path):   # path to sink not found, done
>             break
>         # get this path flow
>         thisPathFlow = float("inf")
>         thisNode = sink
>         while thisNode != source:   # trace back
>             lastNode = path[thisNode]
>             if(graph[lastNode][thisNode] < thisPathFlow):   # update this path flow
>                 thisPathFlow = graph[lastNode][thisNode]
>             thisNode = lastNode
>         # update flow
>         cntFlow += thisPathFlow
>         thisNode = sink
>         while thisNode != source:   # trace back
>             lastNode = path[thisNode]
>             graph[lastNode][thisNode] -= thisPathFlow   # update this edge cap
>             graph[thisNode][lastNode] += thisPathFlow   # update inv edge cap
>             thisNode = lastNode
>     return cntFlow   # the solution to the network flow problem is also the answer to this question
> 
> def main():
>     (source, sink, N) = input().split()   # read first line
>     N = int(N)
>     graph = defaultdict(dict)   # return null dict if accessed invalidly
>     for _ in range(N):   # read N lines
>         (v 1, v 2, cap) = input().split()
>         cap = int(cap)
>         graph[v 1][v 2] = cap   # build map with adj_lists
>         if not graph[v 2].get(v 1, False):   # inverse edge not exist
>             graph[v 2][v 1] = 0   # init inverse edge
>     print(maxCapacity(graph, source, sink))
> 
> main()
> ```

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

- 注意不是连通是 **digraph 强连通**，所以不是简单的 [[Blog/mkdocs-blog-project/emergent-space-obmd/ZJU Courses/2024 Spring/Fundamentals of Data Structure/Ch.09 Graph Algorithms#Undirected Graphs]]

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

> [!hint] My Code in C
> ***$O(N^3)$ ***
> ```c
> void StronglyConnectedComponents( Graph G, void (*visit)(Vertex V) )
> {
>     // rebuild to adj_mat
>     // init
>     int adj_mat[G->NumOfVertices][G->NumOfVertices];
>     for(int i = 0; i < G->NumOfVertices; i++) for(int j = 0; j < G->NumOfVertices; j++) adj_mat[i][j] = (i == j)? 1 : 0;   // reflexive!
>     for(int i = 0; i < G->NumOfVertices; i++){
>         for(PtrToVNode thisNode = G->Array[i]; thisNode != NULL; thisNode = thisNode->Next){   // get the first adjV, and traverse every one
>             adj_mat[i][thisNode->Vert] = 1;   // mark a path from i to thisNode
>         }
>     }
> 
>     // Warshall Algorithm
>     for(int i = 0; i < G->NumOfVertices; i++){   // diag index for this algorithm
>         for(int j = 0; j < G->NumOfVertices; j++){   // line index
>             if(i != j && adj_mat[j][i] == 1){   // need to add to this line
>                 for(int k = 0; k < G->NumOfVertices; k++) adj_mat[j][k] |= adj_mat[i][k];
>             }
>         }
>     }
> 
>     // find all the comoponents
>     int visited[G->NumOfVertices];
>     for(int i = 0; i < G->NumOfVertices; i++) visited[i] = 0;
>     for(int i = 0; i < G->NumOfVertices; i++){   // diag index
>         if(!visited[i]){
>             for(int j = 0; j < G->NumOfVertices; j++){   // row/col index
>                 if(adj_mat[i][j] && adj_mat[j][i] && !visited[j]){
>                     visited[j] = 1;
>                     visit(j);
>                 }
>             }
>             printf("\n");   // after finding one component
>         }
>     }
> }
> ```

