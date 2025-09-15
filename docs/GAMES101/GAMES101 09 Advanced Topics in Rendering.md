---
status:
  - archived
tags: CS/CG-CV/Rendering
date_created: 2025-02-11T00:12:09
date_modified: 2025-09-13T10:18:02
---

# Advanced Light Transport

## Biased vs. Unbiased Monte Carlo Estimators

> 有偏、渐进无偏和无偏估计

## Bidirectional Path Tracing (BDPT)

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211003445163.webp|500x179]]

> [!note] Note
> 从光源和相机出发，分别形成半路径，然后将半路径连接

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211003601879.webp|500x218]]

> [!note] Note
> - 整个场景应该都被间接光照亮，但是 path tracing 的第一次是 diffuse，只有选到了天花板的位置并反射到光源才是亮度像素
> - 如果使用 BDPT，相当于将天花板亮的区域变成一个大的光源了

## Metropolis Light Transport (MLT)

- 使用 Markov Chain Monte Carlo (MCMC)
- 根据一个有效的采样点，找到旁边采样点的有效路径（局部搜索）

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211004054175.webp|500x191]]

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211004230948.webp|500x261]]

> [!note] Note
> - 只要找到一条到光源的路径，就能找到更多
> - 能够渲染水底光线聚焦形成的光斑！

> [!question] Question
> - 难以分析收敛速度
> - 有的像素收敛快，有的收敛慢，可能图像不均匀，比较脏

## Photon Maping

> [!note] caustics
> ![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211004430745.webp|500x169]]

1. 从光源出发，产生光子，进行反射折射，直到光子到达 diffuse 表面的时候“停在”表面上
2. 从相机出发，对于一个像素，找周围最近的 n 个光子，算出其占据的面积，估计光子密度

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211004700560.webp|500x214]]

> [!bug] problems
> - n 比较小的时候，非常 noisy
> - n 非常大的时候，会 blurry
> 	- biased: 光子无限多的情况下，才有 $\Delta A=\mathrm{d}A$
> 	- 只要 blurry 都叫有偏，但确实是 consistent 的

> [!question] 如果取临近小面积呢？
> 完全有偏估计，因为 $\Delta A$ 不会缩小

## Vertex Connection and Merging (VCM)

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211005228214.webp|500x206]]

- 不浪费 BDPT 中光源发出的光子
- 使用了 PM 来连接到临近光子

## Instant Radiosity (IR)

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211005434916.webp|500x131]]

- 光源出来的 light sub-path 到达的点，作为新的光源 (Virtual Point Lights, VPL)
- ! 不能做 glossy 的物体

# Advanced Appearance Modeling

## Non-Surface Models

### Participating Media

> fog, cloud

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211005903438.webp|574x135]]

被吸收或者散射

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211010443580.webp|500x132]]

Phase Function (相位函数) 定义散射的分布，类似 BRDF

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211010707194.webp|500x160]]

### Hair Appearance

#### Marschner Model

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211010852025.webp|500x361]]

> [!note] Note
> 考虑了三种情况
> - R 直接反射
> - TT 两次折射
> - TRT 入射后反射

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211011057135.webp|500x228]]

> [!note] Note
> 将头发当作玻璃圆柱

> [!bug] problem
> 无法模拟动物的毛发，动物毛发中的 medulla 更大，与光的作用效果不同

#### Double Cylinder Model

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211011437466.webp|551x319]]

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211011523857.webp|500x258]]

### Granular Material

> 颗粒模型

## Surface Models

### Translucent Material

> 类似玉石、皮肤的半透明材质

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211011907429.webp|455x248]]

> [!note] Note
> Subsurface Scattering (次表面散射)

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211012028193.webp|500x290]]

> [!note] BSSRDF
> 考虑不从入射点出射，所以还会对面积积分

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211012148087.webp|500x274]]

> [!note] Dipole Approximation
> 表面上下各一个光源，模拟次表面散射的效果

### Cloth

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211012418031.webp|550x317]]

> [!note] 三种渲染方法
> - 当成物体表面
> - 当成散射介质
> - 暴力计算

### Details

> 现实生活中的车、水壶等表面并非完全光滑，而是会有划痕细节 or 各向异性纹路

![[./__assets/GAMES101 09 Advanced Topics in Rendering/IMG-GAMES101 09 Advanced Topics in Rendering-20250211012908783.webp|500x310]]

> [!note] Note
> - 使用精细的、有噪声的法线贴图来添加细节
> - 解决计算量问题：将一个像素对应到的表面的法线进行平均

## Wave Optics

# Procedural Appearance

> 噪声 ->贴图
