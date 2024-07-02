---
created: 2024-07-01T10:22:37
updated: 2024-07-02T10:51:21
---
# 教程

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
mkdocs gh-deploy # 推送完成后，进行云端部署
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

## 工作流

### mkdocs 表现记录

1. 强制每个“文件夹”名称都对应一个文件，默认为文件夹下的第一个文件
2. 默认打开 `docs/index.md` 所以必须要有这个文件

### 1.0 抓取到 attachments 目录

- [x] obsidian 附件抓取脚本
- [x] 使用 `.gitignore`

### 2.0 附件放在每个文件的目录下面

#### markdown 内容 publish 流程

- 在 `mkdocs-blog-project/emergent-space-obmd` 书写，保持所有的 obsidian 特色用法
	- 原有笔记直接复制粘贴到这里
	- 进行原有笔记审核与脱敏处理
	- 写新的，mkdocs 特供 md 笔记
- 覆盖 push 到 `mkdocs-blog-project/emergent-space/docs/markdown` 中，然后执行 `obsidian-attachment-management.py`
	- 对于 `docs` 中的每个文件的 wikilink 进行检查
		- 如果是附件，那么在 ob 中查找这个附件，放到文件所在的**同级目录**；将附件名称中的空格变成 `-`，并更新成 markdown 格式链接
		- 如果是文件，先别动 **还没想好办法**
- **由于 `index.md` 需要作为网站主页使用，所以无法在 `docs/markdown` 文件夹中，只能单独 push**

#### 网页页面管理

- 统一在 `mkdocs.yml` 中进行

#### javascript 扩展

- 直接在项目中编辑
- 就近放置附件
- 在 `mkdocs.yml` 中更新

## 功能
