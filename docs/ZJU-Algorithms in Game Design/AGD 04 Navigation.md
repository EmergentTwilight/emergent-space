---
status:
  - archived
tags: CS/Algorithm/Navigation
attachment:
  - "[[slides/S04_Navigation.pdf|S04_Navigation]]"
date_created: 2024-11-22T09:08:44
date_modified: 2025-09-12T15:23:18
---

# Graph Intro

- maze
- tiles

- Line Drawing
	- Bresenham's Algorithm
	- Linear Interpolation

# Obstacles

- Pure graph: 没有跨越障碍的边
- Tiles: keep a list to track

# Single source, single destination

## Greedy Best First Search

> 比 single source, all destinations 会更快

### Heuristic

> to guide our search

```python title="L1 heuristic"
def heuristic(ax, ay, bx, by):
	# may only make sense in grid graphs
	return abs(ax - bx) + abs(ay - by)
```

![[./__assets/AGD 04 Navigation/IMG-AGD 04 Navigation-20250301194532650.webp]]

> [!warning] Warning
> 比 BFS/Dijkstra 更快，但是结果可能更差
>
> > [!note]- pic
> > ![[./__assets/AGD 04 Navigation/IMG-AGD 04 Navigation-20250301194602350.webp]]

## A*

> #CS/Algorithm/A-Star
> combining Dijkstra's and GBFS

- `{python}priority = cost + heuristic(goal.x, goal.y, neighbor.x, neighbor.y)`
	- 将当前 cell 的 cost 和当前 cell 到目标的 heuristic cost 结合起来
- comments
	- 如果 GBFS 有解，那么 A* 会探索完全相同的区域
	- GBFS 可能会找到更长的路径，但是 A* 不会
	- Dijkstra's 就是 A* 和常数 heuristic
	- heuristic 能够帮助 A* 更快找到最优路径

# Single source, all destinations

## BFS

> #CS/Algorithm/BFS
> unweighted edges

- Queue (FIFO)
- 保存反向指针来构建路径

![[./__assets/AGD 04 Navigation/IMG-AGD 04 Navigation-20250301202226442.webp]]

### early exit

> 找到了目标就提前终止

## Dijkstra's

- priority queue

> [!note]- some pics
> ![[./__assets/AGD 04 Navigation/IMG-AGD 04 Navigation-20250301194827073.webp]]
> ![[./__assets/AGD 04 Navigation/IMG-AGD 04 Navigation-20250301194840285.webp]]

## Bellman-Ford

> cost can be negative

# All sources, all destinations

## Floyd-Warshall Algorithm

## Johnson's Algirithm

> a mixture of Dijkstra's and Bellman-Ford

# Navigation Meshes

- Convex Polygons 凸多边形
	- 在内部可以直接使用直线路径，走完之后仍然在其内部
- Navmesh
	- 将可以使用的区域划分为凸多边形
	- 每个多边形一定是 2d 的，但是整个地图不一定

## algo

1. 如果 goal 和 agent 在同一个 polygon 内部，直线抵达
2. 否则将 polygon 映射成 graph，使用 A*，最后再用 rule \#1

# Funnel Algorithm

> navmesh 过于简化了真实情况，如果有很大的 polygon，可能需要花很多时间到这个 polygon 的中心
> ![[./__assets/AGD 04 Navigation/IMG-AGD 04 Navigation-20250301194915274.webp]]

- 首先根据 A* 算法得到将要经过的 polygons，**接下来关注 polygons 的邻接边**
- 考虑跟踪邻接边的左侧和右侧
	- 当下一步可以从上一个拐点直线连接时，直线连接
	- 如果不能，找最近的新拐点，再直线连接
- 最后一步就是到终点，然后选择 cost 较小的一条

![[./__assets/AGD 04 Navigation/IMG-AGD 04 Navigation-20250301195040864.webp]]
