---
status:
  - archived
tags:
  - CS/CG-CV/Concept/Camera
  - CS/CG-CV/Light-Field
date_created: 2025-02-11T01:35:25
date_modified: 2025-09-13T10:18:02
---

# Concepts in Photography

# Lense

## Thin Lens

- 没有厚度
- 焦距可调
- 完美聚焦

## Circle of Confusion (CoC)

> 弥散圆

![[./__assets/GAMES101 10 Cameras, Lenses and Light Fields/IMG-GAMES101 10 Cameras, Lenses and Light Fields-20250211015441228.webp|500x304]]

> [!note] Note
> 焦外模糊程度与光圈大小相关

## F-Stop

> F 数等于焦距除以光圈直径 $N=f/D$

## in rendering

![[./__assets/GAMES101 10 Cameras, Lenses and Light Fields/IMG-GAMES101 10 Cameras, Lenses and Light Fields-20250211020028208.webp|500x206]]

1. 根据物象位置确定像距，摆放 sensor
2. 进行光线追踪

![[./__assets/GAMES101 10 Cameras, Lenses and Light Fields/IMG-GAMES101 10 Cameras, Lenses and Light Fields-20250211020158662.webp|500x284]]

> [!note] Depth of field 景深
> - 成像后 CoC 足够小的部分，也就是成像清晰的一段范围
> - 光圈越小，景深越大
> - 焦距越大，景深越小

# Light Field / Lumigraph

> [!note] 全光函数
>
> $$
> P(\theta,\phi,\lambda,t,V_x,V_y,V_z)
> $$
>
> 方位角、波长、时间、空间坐标

> [!note] 光线
>
> $$
> P(\theta,\phi,V_x,V_y,V_z)
> $$
>
> 同时，两点也可以定义一条光线

![[./__assets/GAMES101 10 Cameras, Lenses and Light Fields/IMG-GAMES101 10 Cameras, Lenses and Light Fields-20250211021412140.webp|500x400]]

> [!note] 光场
> 记录了所有方向看物体的所有光的信息

## Defining a Light Field

![[./__assets/GAMES101 10 Cameras, Lenses and Light Fields/IMG-GAMES101 10 Cameras, Lenses and Light Fields-20250211021824948.webp|500x342]]

![[./__assets/GAMES101 10 Cameras, Lenses and Light Fields/IMG-GAMES101 10 Cameras, Lenses and Light Fields-20250211021908370.webp|500x309]]

## Light Field Camera

![[./__assets/GAMES101 10 Cameras, Lenses and Light Fields/IMG-GAMES101 10 Cameras, Lenses and Light Fields-20250211022246748.webp|500x596]]

> [!note] Note
> - 每个像素记录的不是 irradiance 而是 radiance
> - 每个像素都是微透镜
> - 可以后期调整焦距、光圈等

![[./__assets/GAMES101 10 Cameras, Lenses and Light Fields/IMG-GAMES101 10 Cameras, Lenses and Light Fields-20250211022454852.webp|213x415]]
