---
status:
  - archived
tags:
  - CS/CG-CV/Concept/Color-Science
  - CS/CG-CV/Task/Colorization
  - CS/CG-CV/Task/Deblurring
date_created: 2025-08-03T22:28:03
date_modified: 2025-09-12T15:23:21
---

# High Dynamic Range Imaging (HDR)

## Exposure

$$
\text{Exposure}=\text{Gain}\times\text{Irradiance}\times\text{Time}
$$

- gain 和 iso 有关
- irradiance 与光圈有关
- time 受快门速度影响

单反相机没有快门延迟，因为不需要将传感器的电荷清零。

## Dynamic Range

> the ratio between the largest and smallest values of a certain quantity (e.g., birghtness)

使用包围曝光得到高动态范围图片。

## Image Formation Model

![[IMG-CV 12 Computational Photography-20250803224542965.webp|500]]

1. 舍弃太亮和太暗的像素
2. 对于剩下的像素，按照曝光时间的倒数加权平均
3. 得到新的像素点

## Tone Mapping (Gamma Compression)

> 将高动态范围的图像映射到低动态范围空间

![[IMG-CV 12 Computational Photography-20250803225222263.webp|500]]

不同的相机可能会用不同的 gamma 曲线，所以需要保留 raw 文件。

# Deblurring

- motion blur: 物体或相机移动
- ps 有去运动模糊的功能

## Modeling Image Blur

- 焦外模糊，每个点都变成光斑，即高斯模糊，相当于清晰图像经过高斯核卷积
	- 形状取决于光圈的形状
- 运动模糊，也可以是卷积，每个点都变成一条线，相当于清晰图像经过这个模糊核卷积
	- 形状取决于曝光时间内相机视角的移动

![[IMG-CV 12 Computational Photography-20250803230041729.webp|500]]

所以要去卷积（deconvolution）。

### Non-Blind Image Deconvolution

根据卷积定理，时域上的卷积 = 频域上的乘积，若 $G$ 为模糊图像，$F$ 为清晰图像，$H$ 为模糊核，则：

$$
\text{FFT}(G)=\text{FFT}(F*H)=\text{FFT}(F)\times\text{FFT}(H)\quad\Rightarrow\quad F=\text{IFFT}(\text{FFT}(G)\div\text{FFT}(H))
$$

![[IMG-CV 12 Computational Photography-20250803230707507.webp|500]]

![[IMG-CV 12 Computational Photography-20250803231018656.webp|500]]

图像太模糊的时候，这种方法效果非常差，这是因为：模糊核比较大的时候，其傅里叶变换（也是一个高斯分布）会变小，0 的部分变多，而距离原点比较远的高频信息除以 0 被放大很多倍。

> [!question] Question
> 如何尽量不放大高频噪声？

![[IMG-CV 12 Computational Photography-20250803231126228.webp|600]]

重新设计**模糊核的傅里叶变换的倒数**：

$$
W=\frac{H}{|H|^2+K}
$$

这被称为**维纳滤波器**。

> [!note] Application
> - 高速路上，模糊核基本已知，可以恢复车辆的运动模糊
> - 哈勃望远镜的镜片有偏移，用滤波修复

#### Optimization Method

模糊图像的生成过程：

$$
G=F*H+N
$$

优化目标为 $N\rightarrow 0$，即：

$$
\text{MSE}=||G-F*H||_2^2=\sum_{ij}(G_{ij}-[F*H]_{ij})^2
$$

但是这个方程的解不唯一，有多种 $F$ 和可以满足条件。

加入约束条件：图像的大部分都是光滑的（梯度是稀疏的），做一个梯度的 L1，变为：

$$
\min_F ||G-F*H||_2^2+\lambda||\nabla F||_1
$$

### Blind image Deconvolution

卷积核也要纳入优化，而且增加先验：卷积核也是稀疏的（是线组成的）：

$$
\min_F ||G-F*H||_2^2+\lambda_1||\nabla F||_1+\lambda||H||_1\quad s.t. H\geq 0
$$

# Colorization

> 将黑白的图像变成彩色的

## Sample-Based Colorization

> use sample image

![[IMG-CV 12 Computational Photography-20250803232732086.webp|500]]

- 对于每个像素，匹配到 sample image
- 将匹配到的像素颜色赋值过来

## Interactive Colorization

![[IMG-CV 12 Computational Photography-20250803232926167.webp|500]]

对于两个相邻的像素，如果亮度接近，颜色也应当接近：

$$
J(U)=\sum_r\left(U(r)-\sum_{s\in N(r)} w_{rs}U(s)\right)^2
$$

- 另外约束用户已经输入的像素颜色不变
- $w_{rs}$ 衡量了 $r,s$ 之间的相似度

> [!question] 对视频上色？
> 打关键帧，一小段内用相同的先验来优化

## CNN

- 输入黑白图，输出彩色图
- 同样的输入有不同的 gt，例如不同颜色的猫，所以直接用 MSE 会造成崩溃

> [!note] GAN
> 将损失函数定义为一个神经网络

![[IMG-CV 12 Computational Photography-20250803234118328.webp|500]]

GAN 的优化方案：

$$
\arg\min_G\max_D \mathbf{E}_{\mathbf{x},\mathbf{y}}[\log D(G(\mathbf{X}))+\log(1-D(\mathbf{y}))]
$$

可以迭代优化，固定一个训练另一个。

> [!question] Question
> minimax 问题训练时非常容易发散

> [!question] Question
> 如果仍然需要保留用户输入的部分控制，可以加入一个 mask 输入，是用户的 brush 图层

# More Image Synthesis Tasks

## Super-Resolution

![[IMG-CV 12 Computational Photography-20250803234932907.webp|800]]

loss 分为两部分，一部分与原图保持一致，另一部分是 GAN。

## Image to Image Translation

![[IMG-CV 12 Computational Photography-20250803235201117.webp|500]]

- 风格转换、草图生成、去雾

## Pose and Garment Transfer

![[IMG-CV 12 Computational Photography-20250803235440902.webp|600]]

1. 拟合人的参数模型，只是没有完整的纹理图
2. mask 得到纹理图
3. 纹理图过网络得到特征（高维纹理图）
4. 纹理图特征和目标姿态参数得到特征图像
5. 特征图像过网络得到最终生成图像

> [!note] Note
> 现在的方法大致逻辑仍然一样，但大多使用了更高级的网络，例如 difussion

## Head Re-Enactment

> 人脸表情迁移，deepfake

## AIGC

> 主要得益于 diffussion model 的发展

- idea: 图像合成是在学习图像的概率分布，学习如何将高斯噪声逐渐减噪声为有意义的图像
- pros: 方便训练，分辨率较高
