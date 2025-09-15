---
status:
  - archived
tags: CS/Algorithm/Maze-Creation
attachment:
  - "[[slides/S03_Mazes.pdf|S03_Mazes]]"
date_created: 2024-11-21T20:39:32
date_modified: 2025-09-12T15:23:19
---

# Intro

## Classification

- Perfect maze: **任意**两个 cell 之间，仅有唯一的路径
	- 也就是说，很多分支，但是没有环路
- Unicursal maze: 没有分支，只有一条路从入口到出口
	- 非常容易解
- Braided maze: 有环，没有死路
- Weave maze: 能从路径的上方、下方穿过

## Algo

- carving a path between cells
- wall adders

# Maze Creation Algos

## Binary Tree

- 每个 cell 都可以连接到其右或上邻居
- **parallel**
- 右侧、上侧都是空的
- **bias**
- **perfect**

## Sidewinder

- 第一行连通，每一行随机分块，块内随机选一个 cell 与上一行连通
- **parallel**
- 第一行是空的
- **bias**
- **perfect**

## Aldous-Broder

### algo

1. 随机选一个 cell 开始
2. 随机选择一个邻居
3. 如果那个邻居没有 visited，连接到那个邻居
4. 移动到那个邻居
5. 如果地图中仍然有 unvisited 的 cell，返回 step 2
6. 结束

### feature

- **no bias**
- **inefficient**，可能有很多 walk 都没有 visit 新的 cell

## Wilson's Random Walk

### algo

1. 随机选一个 cell，标记 visited
2. 随机选另一个 cell 作为起点
3. 进行 **loop-erased random walk**，每一个 step 随机选择邻居，直到选到的邻居是 visited
	1. 标记 walk 上所有 cell visited
	2. 按照历史 step 连通整个 walk
4. 重复 2-4 直到所有 cell 都是 visited

### feature

- **no bias**
	- 产生的迷宫无法和 A-B 算法区分
- **inefficient**
	- 一开始很容易产生循环
	- 最后很快就能找到 visited cell

## Recursive Backtracker

### algo

1. 随机选择一个 cell 作为起点
2. random walk，用 stack 记录递归路径
3. 直到没有 unvisited 邻居，回溯，直到有 unvisited 邻居

### feature

- long, twisted paths with few dead ends
- **bias**
- **memory inefficient**
- explicit stack 更好

# Maze Solution Algos

- Wall Follower: 每个路口都右转/左转
- Dead End Filler: 仅在 perfect maze 中有效
- Recusive Backtracker: 不一定能找到最短路径
- Tremaux Algorithm:
	- 路径: 节点之间的边
	- 从起点进行随机探索，走过一次的路径标记 1
		- 如果遇到岔路
			- 如果岔路有标记，不要走
			- 如果没有标记，可以走
			- 如果所有岔路都有标记，原路返回，将返回时经过的路径标记为 2
	- 到达终点、或所有路径都探索完毕并回到起点

## Dijkstra's Algorithm

### Least-cost path

(omitted)

### Longest path

- 任意选择起点 A，运行 Dijkstra，找到距离 A 最远的 cell B
- 在 B 运行 Dijkstra，找到距离 B 最远的 cell C
- 最长路径就是 B->C
- *定义了图的“直径”*

- 最长路径越长，迷宫就越可能更复杂
