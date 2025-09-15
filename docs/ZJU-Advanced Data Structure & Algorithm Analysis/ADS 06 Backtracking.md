---
status:
  - archived
tags: CS/Algorithm/Backtracking
date_created: 2024-10-14T13:33:37
date_modified: 2025-09-13T10:18:03
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
---

# 1 Intro

## 1.1 Elements of an Algorithm

- Computational Problem: *P/NP*
- Feasibility
- Solution Space
	- Convex Optimization/Linear Programming: Continuous space
	- Combinatorial Optimization: Discrete & finite space
	- Integer Programming: Discrete & infinite space
- Optimality: tradeoff between optimality vs. complexity

> Backtracking 是一种枚举法，*可带剪枝地*遍历解空间

## 1.2 Main Takeaways

- Problems
	- 8-Queens
	- Turnpike Reconstruction Problem
	- Tic-Tac-Toe
- Definitions
	- Game Tree
	- Value
	- Position
- Algorithm
	- Minimax Strategy
	- Alpha-Beta Pruning

## 1.3 Rationale of the Backtracking Algorithms

- 枚举法
- 剪枝：如果部分解仍然满足条件，那么继续尝试添加新的单元解，条件不被满足时 backtrack，直到获得满足条件的完整解

# 2 Eight Queens

> Backtracking eliminates **infeasible** solutions.

## 2.1 Constrains

$$
\begin{align}
\text{Find}\quad S&=(x_{1},x_{2},\dots,x_{n})\\
s.t.\quad  S_{i}&=\{1,2,3,4,5,6,7,8\} \quad \text{for} \,1\leq i\leq{8}\\
x_{i}&\neq x_{j}\quad \text{if}\,i\neq j \\
\frac{x_{i}-x_{j}}{i-j}&\neq \pm 1
\end{align}
$$

对于 $n$-Queens 问题，解空间大小为 $O(n!)$

## 2.2 Solution

> Step 1: Construct a game tree
> Step 2: DFS to examine all the paths

![[__assets/ADS 06 Backtracking/IMG-ADS 06 Backtracking-20241028014837804.webp]]

# 3 The Turnpike Reconstruction Problem

若 $x$ 轴上存在 $N$ 个点，坐标分别为 $x_1<x_2<\dots<x_{N}$，假设以 $x_1=0$ 为原点，一共有 $\frac{N(N-1)}{2}$ 个距离，现在的问题是，根据这些距离重建所有点的坐标。

## 3.1 Solution

> Step 1: 根据距离的数量得出 $N$ 的值
> Step 2: 找到两个端点 $x_0, x_N$
> Step 3: 从大到小 check 距离，最终找到正确的解

![[__assets/ADS 06 Backtracking/IMG-ADS 06 Backtracking-20241028014852286.webp]]

> [!hint] 为什么从大到小 check 距离？
> 在已经确定的点集 $S_m$ 的基础上，想要新增一个点 $x_{m+1}$，那么新产生的最大的距离一定是 $|x_{m+1}-x_{0}|$ 或 $|x_{m+1}-x_{N}|$

```c title="Reconstuct"
bool Reconstruct ( DistType X[ ], DistSet D, int N, int left, int right )
{ /* X[1]...X[left-1] and X[right+1]...X[N] are solved */
    bool Found = false;
    if ( Is_Empty( D ) )
        return true; /* solved */
    D_max = Find_Max( D );
    
    /* option 1：X[right] = D_max */
    /* check if |D_max-X[i]|ÎD is true for all X[i]’s that have been solved */
    OK = Check( D_max, N, left, right ); /* pruning */
    if ( OK ) { /* add X[right] and update D */
        X[right] = D_max;
        for ( i=1; i<left; i++ )  Delete( |X[right]-X[i]|, D);
        for ( i=right+1; i<=N; i++ )  Delete( |X[right]-X[i]|, D);
        Found = Reconstruct ( X, D, N, left, right-1 );
        if ( !Found ) { /* if does not work, undo */
            for ( i=1; i<left; i++ )  Insert( |X[right]-X[i]|, D);
            for ( i=right+1; i<=N; i++ )  Insert( |X[right]-X[i]|, D);
        }
    }
    /* finish checking option 1 */
    
    if ( !Found ) { /* if option 1 does not work */
        /* option 2: X[left] = X[N]-D_max */
        OK = Check( X[N]-D_max, N, left, right );
        if ( OK ) {
            X[left] = X[N] – D_max;
            for ( i=1; i<left; i++ )  Delete( |X[left]-X[i]|, D);
            for ( i=right+1; i<=N; i++ )  Delete( |X[left]-X[i]|, D);
            Found = Reconstruct (X, D, N, left+1, right );
            if ( !Found ) {
                for ( i=1; i<left; i++ ) Insert( |X[left]-X[i]|, D);
                for ( i=right+1; i<=N; i++ ) Insert( |X[left]-X[i]|, D);
            }
        }
        /* finish checking option 2 */
    } /* finish checking all the options */
    return Found;
}
```

## 3.2 A Template for Backtracking

```c title="A Template for Backtracking"
bool Backtracking ( int i )
{   Found = false;
    if ( i > N )
        return true; /* solved with (x1, …, xN) */
    for ( each xi in Si ) {
        /* check if satisfies the restriction R */
        OK = Check((x1, ..., xi) , R ); /* pruning */
        if ( OK ) {
            Count xi in;
            Found = Backtracking( i+1 );
            if ( !Found )
                Undo( i ); /* recover to (x1, …, xi-1) */
        }
        if ( Found ) break;
    }
    return Found;
}
```

## 3.3 Conclusion

> [!hint] Catch
> 关键在于从大到小枚举并 check 距离，这能够最大化剪枝效率
> ![[__assets/ADS 06 Backtracking/IMG-ADS 06 Backtracking-20241028014907403.webp]]

# 4 Tic-tac-toe

## 4.1 Minimax Strategy

- Evalution function: $f(p)=W_{Computer}-W_{Human}$, where $W$ is the potential wins at **position** $P$
- The human is trying to **minimize** $f(p)$, while the computer is trying to **maximize** it

![[__assets/ADS 06 Backtracking/IMG-ADS 06 Backtracking-20241028014917981.webp]]

> [!NOTE] ply, re-ply
> - ply 指的是玩家的一步操作
> - re-ply 指的是对手的回应操作

## 4.2 $\alpha-\beta$ Pruning

![[__assets/ADS 06 Backtracking/IMG-ADS 06 Backtracking-20241028014933987.webp]]

![[__assets/ADS 06 Backtracking/IMG-ADS 06 Backtracking-20241028014946224.webp]]

In practice, it limits the searching to only $O(\sqrt{ N })$ nodes, where $N$ is the size of full game tree.

### 4.2.1 Discussion: best-case complexity for $\alpha-\beta$ pruning

> [!question] 试图证明：
> 若分叉数 $b$ 的 Minimax 博弈树的深度为 $d$，且叶子节点都在深度 $d$ 层，则 best case 下使用 $\alpha -\beta$ pruning 后的最优复杂度为：
>
> $$
> O\left( b^\frac{d}{2} \right)
> $$

记 $c_i$ 表示深度为 $i$ 时的最优复杂度，则对于 $d=i$ 的树，至少有一个子树进行了子问题的搜索 $c_{i-1}$，其他 $b-1$ 个子树至少有一个孩子进行了子问题的搜索 $(b-1)c_{i-2}$，因此：

$$
c_{i}=c_{i-1}+(b-1)c_{i-2}
$$

求解特征方程 $x^2-x-(b-1)=0$ 得到 $x=\frac{1\pm \sqrt{ 4b-3 }}{2}$，那么

$$
c_{d}=C_{1}x_{1}^d+C_{2}x_{2}^d = O\left( \left( \frac{1+\sqrt{ 4b-3 }}{2} \right)^d \right)=O(b^{d/2})
$$

证毕。

# 5 Questions

## 5.1 Q6

### 5.1.1 Exhaustive search in finite time?

It is guaranteed that an exhaustive search can always find the solution in finite time. (T/F)

> [!hint]- Answer
> **F** 如果搜索空间是无限的，就无法通过遍历的方式得出

## 5.2 Ex6

## 5.3 HW6

### 5.3.1 Detecting Werewolves %% fold %%

> [!question]- Werewolf
> Werewolf（狼人杀） is a game in which the players are partitioned into two parties: the werewolves and the human beings. Suppose that in a game,
>
> - player #1 said: "Player #2 is a werewolf.";
> - player #2 said: "Player #3 is a human.";
> - player #3 said: "Player #4 is a werewolf.";
> - player #4 said: "Player #5 is a human."; and
> - player #5 said: "Player #4 is a human.".
> 
> Given that there were 2 werewolves among them, at least one but not all the werewolves were lying, and there were exactly 2 liers. Can you point out the werewolves?
>
> Now you are asked to solve a harder vertion of this problem: given that there were N players, with M werewolves among them, at least one but not all the werewolves were lying, and there were exactly L liers. You are supposed to point out the werewolves.
>
> **Input Specification**:
>
> Each input file contains one test case. For each case, the first line gives three positive integer N (5 ≤ N ≤ 100), M and L (2 ≤ M < N, 1 ≤ L < N). Then N lines follow and the i-th line gives the statement of the i-th player (1 ≤ i ≤ N), which is represented by the index of the player with a positive sign for a human and a negative sign for a werewolf.
>
> **Output Specification**:
>
> If a solution exists, print in a line in descending order the indices of the M werewolves. The numbers must be separated by exactly one space with no extra spaces at the beginning or the end of the line. If there are more than one solution, you must output the largest solution sequence -- that is, for two sequences A = { a[1], ..., a[M] } and B = { b[1], ..., b[M] }, if there exists 0 ≤ k < M such that a[i] = b[i] (i ≤ k) and a[k+1]>b[k+1], then A is said to be larger than B. In case there is no solution, simply print `No Solution`.
>
> **Sample Input 1**:
>
> ```in
> 5 2 2
> -2
> +3
> -4
> +5
> +4
> ```
>
> **Sample Output 1**:
>
> ```out
> 4 1
> ```
>
> **Sample Input 2**:
>
> ```in
> 6 2 3
> -2
> +3
> -4
> +5
> +4
> -3
> ```
>
> **Sample Output 2**:
>
> ```out
> 6 4
> ```
>
> **Sample Input 3**:
>
> ```in
> 6 2 5
> -2
> +3
> -4
> +5
> +4
> +6
> ```
>
> **Sample Output 3**:
>
> ```out
> No Solution
> ```

> [!hint]
> - 使用合理的 struct 来方便状态传递
> - 需要高亮部分的 pruning 条件，才能避免超时

> [!note]
> 非常有意思的问题


