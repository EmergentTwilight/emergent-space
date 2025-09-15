---
status:
  - archived
tags: CS/Language/Python/Numpy
attachment:
  - "[[slides/5_向量化计算.pdf|5_向量化计算]]"
date_created: 2024-07-06T02:00:54
date_modified: 2025-09-12T15:23:19
---

# 什么是向量化计算

- Array Programming
- 编译器的优化

# NumPy

## 什么是向量化

- 未向量化：一堆 for 循环，每次只执行一个运算
- 向量化：张量运算、向量运算表示，并行执行

- 向量化的核心思想
	- 同时多个值参与运算
	- 可以时逻辑上的，也可以是实际执行上的
	- 思维抽象

## NumPy 基础

```python
np.array([1, 2, 3])
```

创建的是 `ndarray` 类型。不同于 python `list` 是树状结构，`ndarray` 更像是 c 中的连续内存地址，由于 CPU 可能有 precache 操作，所以访问速度更快。

### Indexing

```python
array[2:4, -2:, 0]
array[[1, 3, 4]]
```

> [!attention] Title
> 切片获得的数组是一个指向原数组的指针，操作切片数组会改变原来数组的值

```python
any(a > 5 for a in array)
all(a > 5 for a in array)
```

### Axis

```python
any(array, axis = 0)
```

`axis = 0` 指的是 most significant 方向，比如说是**列方向**。

### 运算

```python
A * B  # 按位乘
A @ B  # 矩阵乘法
```

- **广播机制的条件**
	- 两个向量维度相同
	- 某个维度一个向量有，一个无
	- 某个维度一个向量有，一个有但为 1

## 向量化计算

### Q 1

给定一个矩阵，新的矩阵是原有矩阵每个值与它右上、右下的值的和，非法地址的值为 0

```python
def func(A):
	a = A.reshape(3, 3)
	b = np.pad(a[:-1, 1:], ((1, 0), (0, 1)))
	c = np.pad(a[1:, 1:], ((0, 1), (0, 1)))
	return a + b + c
```

# 手写 SIMD 向量化

## SIMD 是什么

- Single Instruction Multiple Data，单指令多数据流
- 在 x86 架构下，SIMD 一般和 SSE 和 AVX 等指令集联系在一起
- SSE 和 AVX 指令集中提供了大量可以单指令操作多个数据单元的指令

## 数据个数!=加速倍数

- SIMD 同时操作两个数据，加速比不一定是 2
- 受到内存带宽使用、解码消耗减小等因素影响
- 如果是整个程序的一部分，那就更复杂了

## 越长越好？

- 可能发热降频
- 可能成本更高
- *AVX 512 甚至可能不如 AVX 2*

## C 向量化 SIMD

- 基本流程
	- Load 到寄存器
	- 进行向量化计算
	- Store 回内存

> [!example] 手写一个循环
>
> ```c
> for(int i = 0; i < MAXN; i++){
> 	c[i] += a[i] * b[i];
> }
> ```
> 然后用 SIMD 手写一遍：
> ```c
> #include <immintrin.h>
> 
> for(int i = 0; i < MAXN; i += 16){  // 因为 AVX512 一次处理16个数据
>     __m512 a_vec = _mm512_load_ps(&a[i]);
>     __m512 b_vec = _mm512_load_ps(&b[i]);
>     __m512 c_vec = _mm512_load_ps(&c[i]);
>     
>     __m512 mul_vec = _mm512_mul_ps(a_vec, b_vec);
>     __m512 c_vec_new = _mm512_add_ps(c_vec, mul_vec);
>     
>     _mm512_store_ps(&c[i], c_vec_new);
> }
> ```

## 常见问题

- 内存对齐
- 循环边界不确定

**多数时候编译器自动向量化就够了，最后再来进行手写 SIMD 优化**
