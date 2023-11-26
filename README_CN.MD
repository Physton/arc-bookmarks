# arc-bookmarks

[![GitHub stars](https://img.shields.io/github/stars/Physton/arc-bookmarks?style=flat-square)](https://github.com/Physton/arc-bookmarks/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Physton/arc-bookmarks?style=flat-square)](https://github.com/Physton/arc-bookmarks/network/members)
[![GitHub issues](https://img.shields.io/github/issues/Physton/arc-bookmarks?style=flat-square)](https://github.com/Physton/arc-bookmarks/issues)
[![GitHub issues closed](https://img.shields.io/github/issues-closed/Physton/arc-bookmarks?style=flat-square)](https://github.com/Physton/arc-bookmarks/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub license](https://img.shields.io/github/license/Physton/arc-bookmarks?style=flat-square)](https://github.com/Physton/arc-bookmarks/blob/master/LICENSE.md)
[![GitHub commits](https://img.shields.io/github/last-commit/Physton/arc-bookmarks?style=flat-square)](https://github.com/Physton/arc-bookmarks/commits/main)
[![Downloads total](https://img.shields.io/github/downloads/physton/arc-bookmarks/total?style=flat-square)](https://github.com/Physton/arc-bookmarks/releases)
[![Latest release](https://img.shields.io/github/v/release/Physton/arc-bookmarks?style=flat-square)](https://github.com/Physton/arc-bookmarks/releases)

<div align="center">

### [🇺🇸 English](README.MD) | [🇨🇳 简体中文](README_CN.MD)

</div>

[arc-bookmarks](https://github.com/Physton/arc-bookmarks) 是一个 [Python](https://www.python.org/) 脚本，用于导出 [Arc 浏览器](https://arc.net/) 的侧边栏数据（收藏/书签）到 html/json 文件。html 文件可用于导入到其他浏览器。仅适用于 MacOS。

----

## 开发计划

- [x] 导出到 html 书签文件。
- [x] 导出到 json 文件。
- [x] 自动将书签导入到 Chrome 浏览器中。
- [x] 自动将书签导入到 Edge 浏览器中。
- [ ] 自动将书签导入到 Firefox 浏览器中。
- [ ] 自动将书签导入到 Safari 浏览器中。
- [ ] 从其他浏览器导入书签到 Arc 浏览器侧边栏中。

## 使用

### 使用可执行文件（无需 python 环境）

1. 前往 [Releases](https://github.com/Physton/arc-bookmarks/releases)，下载 [arc-bookmarks](https://github.com/Physton/arc-bookmarks/releases/latest/download/arc-bookmarks) 。
2. 打开系统 `终端` 应用程序。
3. 为 `arc-bookmarks` 文件添加可执行权限。
    ```bash
    chmod +x ~/Downloads/arc-bookmarks
    ```
4. 执行 `arc-bookmarks` 文件。
    ```bash
    ~/Downloads/arc-bookmarks --save-html=~/Downloads/bookmark.html
    ```

### 使用 python 运行
1. 前往 [Releases](https://github.com/Physton/arc-bookmarks/releases)，下载 [arc-bookmarks.zip](https://github.com/Physton/arc-bookmarks/releases/latest/download/arc-bookmarks.zip) 。
2. 解压缩 `arc-bookmarks.zip` 文件。
3. 打开系统 `终端` 应用程序。
4. 输入 `cd `，然后将 `arc-bookmarks` 文件夹拖到终端窗口中。回车执行。
    ```bash
    cd ~/Downloads/arc-bookmarks
    ```
5. 执行 `arc-bookmarks` 文件。
    ```bash
    python3 main.py --save-html=bookmark.html
    ```

## 参数说明

- `sidebar-file`
    - 默认值：`~/Library/Application Support/Arc/StorableSidebar.json`
    - 参考值：
    - 示例：`--sidebar-file="~/Library/Application Support/Arc/StorableSidebar.json"`
    - 说明：Arc 浏览器的 `StorableSidebar.json` 文件路径。它是用于存储 Arc 浏览器的侧边栏数据的文件。 一般情况下，不需要指定该参数。如果不指定该参数，程序会使用默认的路径。
- `save-json`
    - 默认值：
    - 参考值：`~/Downloads/bookmark.json`
    - 示例：`--save-json=bookmark.json`
    - 说明：将书签保存到 json 文件中。
- `save-html`
    - 默认值：
    - 参考值：`~/Downloads/bookmark.html`
    - 示例：`--save-html=bookmark.html`
    - 说明：将书签保存到 html 文件中。可用于导入到浏览器中。
- `import-to-chrome`
    - 默认值：
    - 参考值：
    - 示例：`--import-to-chrome`
    - 说明：将书签导入到 Chrome 浏览器中。
    - ⚠️警告：**使用此功能，将会覆盖 Chrome 浏览器中的书签。请自行做好备份。导入成功后，需要重启 Chrome 浏览器才能看到导入的书签。**
        - `chrome-bookmarks-file`
            - 默认值：`~/Library/Application Support/Google/Chrome/Default/Bookmarks`
            - 参考值：
            - 示例：`--chrome-bookmarks-file="~/Library/Application Support/Google/Chrome/Default/Bookmarks"`
            - 说明：Chrome 浏览器的 `Bookmarks` 文件路径。它是用于存储 Chrome 浏览器的书签的文件。 一般情况下，不需要指定该参数。如果不指定该参数，程序会使用默认的路径。
        - `chrome-import-node`
            - 默认值：`bookmark_bar`
            - 参考值：`bookmark_bar`、`other`
            - 示例：`--chrome-import-node=bookmark_bar`
            - 说明：将书签导入到 Chrome 浏览器中的节点。默认为 `bookmark_bar`。
- `import-to-edge`
    - 默认值：
    - 参考值：
    - 示例：`--import-to-edge`
    - 说明：将书签导入到 Edge 浏览器中。
    - ⚠️警告：**使用此功能，将会覆盖 Edge 浏览器中的书签。请自行做好备份。导入成功后，需要重启 Edge 浏览器才能看到导入的书签。**
        - `edge-bookmarks-file`
            - 默认值：`~/Library/Application Support/Microsoft Edge/Default/Bookmarks`
            - 参考值：
            - 示例：`--edge-bookmarks-file="~/Library/Application Support/Microsoft Edge/Default/Bookmarks"`
            - 说明：Edge 浏览器的 `Bookmarks` 文件路径。它是用于存储 Edge 浏览器的书签的文件。 一般情况下，不需要指定该参数。如果不指定该参数，程序会使用默认的路径。
        - `edge-import-node`
            - 默认值：`bookmark_bar`
            - 参考值：`bookmark_bar`、`other`
            - 示例：`--edge-import-node=bookmark_bar`
            - 说明：将书签导入到 Edge 浏览器中的节点。默认为 `bookmark_bar`。

## 示例

- 导出为 html 文件，导出文件保存到 `~/Downloads/bookmark.html` 中。
    ```bash
    ./arc-bookmarks --save-html=~/Downloads/bookmark.html
    ```

- 导出为 json 文件，导出文件保存到 `~/Downloads/bookmark.json` 中。
    ```bash
    ./arc-bookmarks --save-json=~/Downloads/bookmark.json
    ```

- 同时导出为 html 文件和 json 文件，导出文件保存到 `~/Downloads/bookmark.html` 和 `~/Downloads/bookmark.json` 中。
    ```bash
    ./arc-bookmarks --save-html=~/Downloads/bookmark.html --save-json=~/Downloads/bookmark.json
    ```

- 将书签导入到 Chrome 浏览器中。
    ```bash
    ./arc-bookmarks --import-to-chrome
    ```
    **导入成功后，需要重启 Chrome 浏览器才能看到导入的书签。**

- 将书签导入到 Chrome 和 Edge 浏览器中。
    ```bash
    ./arc-bookmarks --import-to-chrome --import-to-edge
    ```
    **导入成功后，需要重启 Chrome 和 Edge 浏览器才能看到导入的书签。**