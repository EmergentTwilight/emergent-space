---
created: 2024-07-01T10:22:37
updated: 2024-07-11T08:39:45
---
# 简单教程

## 初步上手

MkDocs 需要 python 环境，先创建一个 python 虚拟环境，然后进行如下配置：

```bash
pip install mkdocs
pip install mkdocs-material
pip install mkdocs-callouts
pip install mkdocs-include
pip install mkdocs-statistics-plugin
```

下面是有用的 MkDocs 命令：

```bash
mkdocs new . # 进行初始化
mkdocs serve # 本地演示
mkdocs build # 完成编辑之后，建立静态页面
mkdocs gh-deploy # 进行部署
```

使用 git 将库 push 到 github：

```bash
git init # 初始化 git

git config --global user.name <yourname>
git config --global user.email <youremail>

git add . # 将所有文件添加到缓存
git commit -m "info"
git remote add origin <repo_url>
git push origin master # 将本地分支推送到远端仓库

git config --global http.proxy 127.0.0.1:7890
git config --global https.proxy 127.0.0.1:7890  # 修复代理设置的问题
```

## 基础设置

参考 MkDocs 官方的 [Setup](https://squidfunk.github.io/mkdocs-material/setup/) 文档对网页进行设置。

## Useful links

-  [解决Git连接失败：Failed to connect to github.com port 443 after 21090 ms: Couldn‘t connect to server ‍-腾讯云开发者社区-腾讯云 (tencent.com)](https://cloud.tencent.com/developer/article/2405656)
- [尝试修改 mkdocs-material 网页的字体的过程记录 - My Pamphlet Blog (ronaldln.github.io)](https://ronaldln.github.io/MyPamphlet-Blog/2023/10/23/mkdocs-material/)
- [添加 mkdocs-material 网页字数统计功能记录 - My Pamphlet Blog (ronaldln.github.io)](https://ronaldln.github.io/MyPamphlet-Blog/2023/10/24/mkdocs-material/)

# TODO

## 界面设计

- [x] CSS 不渲染问题
- [x] 更好的 css 样式
	- [x] 更多切换选择
		- [x] 浅色黑白
		- [x] 深色高亮
- [x] 字体适配
- [x] github 链接
- [ ] 标题图标绘制
- [ ] homepage 设计

## 功能

- [x] obsidian 2 mkdocs push
- [x] 附件抓取
- [ ] 完整的导航
- [x] pdf 链接测试
- [x] markdown 链接
	- [x] BFS 实现
	- [x] 测试
- [ ] 评论区
- [ ] 访问量统计？

# Python Scripts

- 实现 wikilink 转换为 markdown link
- 实现敏感内容标记和自动删除
- 实现附件自动抓取和链接更新