---
status:
  - archived
tags: CS/Language/Python/Pygame
attachment:
  - "[[slides/S02_FontSpriteRandom.pdf|S02_FontSpriteRandom]]"
date_created: 2024-11-21T20:20:08
date_modified: 2025-09-12T15:23:18
---

# Font

直接参考 ppt 即可

# Sprite

直接参考 ppt 即可

# Randomness

## Linear Congruential Generator (LCG)

$$
X_{n+1}=(aX_{n}+c) \text{ mod } m
$$

- LCG 一定是循环的，循环的周期一般都 $<m$
- What makes a good Pseudo-Random Number Generator?
	- 更长的重复周期
	- 其他随机来源：例如按键按压的时间等
- `{python}import random` `{python}import secrets`

## Random Distributions

### Roll the dices

> 记住类似 3d4 这样的表达

![[./__assets/AGD 02 Font Sprite Random/IMG-AGD 02 Font Sprite Random-20250301194311927.webp]]

### Asymmetric Distributions

- Drop the lowest roll/dice
- Reroll the lowest
- Critical Hit
	- 在一些概率下，多 roll 一个 ![[./__assets/AGD 02 Font Sprite Random/IMG-AGD 02 Font Sprite Random-20250301194339761.webp]]
