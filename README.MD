# arc-bookmarks

[![GitHub stars](https://img.shields.io/github/stars/Physton/arc-bookmarks?style=flat-square)](https://github.com/Physton/arc-bookmarks/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Physton/arc-bookmarks?style=flat-square)](https://github.com/Physton/arc-bookmarks/network/members)
[![GitHub issues](https://img.shields.io/github/issues/Physton/arc-bookmarks?style=flat-square)](https://github.com/Physton/arc-bookmarks/issues)
[![GitHub issues closed](https://img.shields.io/github/issues-closed/Physton/arc-bookmarks?style=flat-square)](https://github.com/Physton/arc-bookmarks/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub license](https://img.shields.io/github/license/Physton/arc-bookmarks?style=flat-square)](https://github.com/Physton/arc-bookmarks/blob/master/LICENSE.md)
[![GitHub commits](https://img.shields.io/github/last-commit/Physton/arc-bookmarks?style=flat-square)](https://github.com/Physton/arc-bookmarks/commits/main)
[![Downloads total](https://img.shields.io/github/downloads/physton/arc-bookmarks/total?style=flat-square)](https://github.com/Physton/arc-bookmarks/releases)

<div align="center">

### [🇺🇸 English](README.MD) | [🇨🇳 简体中文](README_CN.MD)

</div>

[arc-bookmarks](https://github.com/Physton/arc-bookmarks) is a Python script used to export sidebar data (bookmarks) from [Arc Browser](https://arc.net/) to HTML/JSON files. The HTML file can be imported into other browsers. Only applicable to MacOS.

----

## Development Plan

- [x] Export to HTML bookmark file.
- [x] Export to JSON file.
- [x] Automatically import bookmarks into Chrome browser.
- [x] Automatically import bookmarks into Edge browser.
- [ ] Automatically import bookmarks into Firefox browser.
- [ ] Automatically import bookmarks into Safari browser.

## Usage

### Using the executable file (no Python environment required)

1. Go to [Releases](https://github.com/Physton/arc-bookmarks/releases) and download [arc-bookmarks](https://github.com/Physton/arc-bookmarks/releases/latest/download/arc-bookmarks).
2. Open the system `Terminal` application.
3. Add executable permission to the `arc-bookmarks` file.
    ```bash
    chmod +x ~/Downloads/arc-bookmarks
    ```
4. Execute the `arc-bookmarks` file.
    ```bash
    ~/Downloads/arc-bookmarks --save-html=~/Downloads/bookmark.html
    ```

### Using Python to run
1. Go to [Releases](https://github.com/Physton/arc-bookmarks/releases) and download [arc-bookmarks.zip](https://github.com/Physton/arc-bookmarks/releases/latest/download/arc-bookmarks.zip).
2. Unzip the `arc-bookmarks.zip` file.
3. Open the system `Terminal` application.
4. Enter `cd `, then drag the `arc-bookmarks` folder into the terminal window. Press Enter to execute.
    ```bash
    cd ~/Downloads/arc-bookmarks
    ```
5. Execute the `arc-bookmarks` file.
    ```bash
    python3 main.py --save-html=bookmark.html
    ```

## Parameter Description

| Parameter | Default | Description | Example |
| --- | --- | --- | --- |
| sidebar-file | ~/Library/Application Support/Arc/StorableSidebar.json | The path to the StorableSidebar.json file of Arc Browser. It is the file used to store the sidebar data of Arc Browser. In general, you don't need to specify this parameter. If not specified, the program will use the default path. | --sidebar-file="~/Library/Application Support/Arc/StorableSidebar.json" |
| save-json | | Save bookmarks to a JSON file. | --save-json=bookmark.json |
| save-html | | Save bookmarks to an HTML file. Can be imported into browsers. | --save-html=bookmark.html |
| import-to-chrome | | Import bookmarks into Chrome browser. | --import-to-chrome |
| chrome-bookmarks-file | ~/Library/Application Support/Google/Chrome/Default/Bookmarks | The path to the Bookmarks file of Chrome browser. It is the file used to store the bookmarks of Chrome browser. In general, you don't need to specify this parameter. If not specified, the program will use the default path. | --chrome-bookmarks-file="~/Library/Application Support/Google/Chrome/Default/Bookmarks" |
| chrome-import-node | bookmark_bar | The node to import bookmarks into the Chrome browser. The default is bookmark_bar. Can be imported into the bookmark_bar or other nodes. | --chrome-import-node=bookmark_bar |
| import-to-edge | | Import bookmarks into Edge browser. | --import-to-edge |
| edge-bookmarks-file | ~/Library/Application Support/Microsoft Edge/Default/Bookmarks | The path to the Bookmarks file of Edge browser. It is the file used to store the bookmarks of Edge browser. In general, you don't need to specify this parameter. If not specified, the program will use the default path. | --edge-bookmarks-file="~/Library/Application Support/Microsoft Edge/Default/Bookmarks" |
| edge-import-node | bookmark_bar | The node to import bookmarks into the Edge browser. The default is bookmark_bar. Can be imported into the bookmark_bar or other nodes. | --edge-import-node=bookmark_bar |

## Examples

- Export as an HTML file, and save the exported file to `~/Downloads/bookmark.html`.
    ```bash
    ./arc-bookmarks --save-html=~/Downloads/bookmark.html
    ```

- Export as a JSON file, and save the exported file to `~/Downloads/bookmark.json`.
    ```bash
    ./arc-bookmarks --save-json=~/Downloads/bookmark.json
    ```

- Export as both an HTML file and a JSON file, and save the exported files to `~/Downloads/bookmark.html` and `~/Downloads/bookmark.json` respectively.
    ```bash
    ./arc-bookmarks --save-html=~/Downloads/bookmark.html --save-json=~/Downloads/bookmark.json
    ```

- Import bookmarks into Chrome browser.
    ```bash
    ./arc-bookmarks --import-to-chrome
    ```
    **After the import is successful, you need to restart the Chrome browser to see the imported bookmarks.**

- Import bookmarks into Chrome and Edge browsers.
    ```bash
    ./arc-bookmarks --import-to-chrome --import-to-edge
    ```
    **After the import is successful, you need to restart the Chrome and Edge browsers to see the imported bookmarks.**
