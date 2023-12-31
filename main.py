import os
import json
import sys
import time
import requests

VERSION = 'v0.0.4'
REPO = 'Physton/arc-bookmarks'
GITHUB = f'https://github.com/{REPO}'

def init_bookmark(id, title = '', url = '', date_added = '', date_last_used='', children = []):
    return {
        'id': id,
        'title': title,
        'url': url,
        'date_added': date_added,
        'date_last_used': date_last_used,
        'children': children,
    }

def toptem2bookmark(item):
    bookmark = init_bookmark(item['value']['id'])
    bookmark['title'] = get_value(item, 'value.data.tab.savedTitle', '')
    bookmark['url'] = get_value(item, 'value.data.tab.savedURL', '')
    bookmark['date_last_used'] = get_value(item, 'value.data.tab.timeLastActiveAt', '')
    bookmark['date_added'] = item['value']['createdAt']
    return bookmark

def item2bookmark(item, items):
    if 'childrenIds' in item['value'] and len(item['value']['childrenIds']) > 0:
        # 这是一个文件夹
        bookmark = init_bookmark(item['value']['id'])
        bookmark['title'] = item['value']['title']
        bookmark['date_added'] = item['value']['createdAt']
        children = []
        for childId in item['value']['childrenIds']:
            subItem = items.get(childId, None)
            if subItem:
                subBookmark = item2bookmark(subItem, items).copy()
                children.append(subBookmark)
        bookmark['children'] = children
        return bookmark
    else:
        # 这是一个书签
        return toptem2bookmark(item).copy()

def print_json(json_data):
    print(json.dumps(json_data, indent=4, ensure_ascii=False))

def print_error(message):
    print(f'\033[31m{message}\033[0m')
    sys.exit()

def print_success(message):
    print(f'\033[32m{message}\033[0m')

def print_warning(message):
    print(f'\033[33m{message}\033[0m')

def get_space_index(spaces, space_id):
    for index, space in enumerate(spaces):
        if space['id'] == space_id:
            return index
    return -1

def get_value(data, keys, default=None):
    if "." in keys:
        key, rest = keys.split(".", 1)
        if key in data:
            return get_value(data[key], rest, default)
        else:
            return default
    else:
        return data.get(keys, default)

def get_bookmarks(SidebarFile):
    SidebarFile = os.path.expanduser(SidebarFile)
    if not os.path.exists(SidebarFile):
        print(f'SidebarFile not exists: {SidebarFile}')
        sys.exit()

    with open(SidebarFile, 'r', encoding='utf-8') as f:
        SidebarJson = json.load(f)

    sidebarSyncState = SidebarJson['sidebarSyncState']

    items = {}
    for item in sidebarSyncState['items']:
        if isinstance(item, str):
            continue
        items[item['value']['id']] = item

    topAppsContainers = []

    topAppsContainerID = get_value(sidebarSyncState, 'container.value.topAppsContainerID', None)
    if topAppsContainerID:
        topAppsContainer = items.get(topAppsContainerID, None)
        if topAppsContainer:
            for childId in topAppsContainer['value']['childrenIds']:
                item = items.get(childId, None)
                if not item:
                    continue
                topAppsContainers.append(toptem2bookmark(item))

    spaces = []
    for orderedSpaceID in sidebarSyncState['container']['value']['orderedSpaceIDs']:
        spaces.append({
            'id': orderedSpaceID,
            'title': '',
            'pinnedId': '',
            'unpinnedId': '',
            'pinneds': [],
            'unpinneds': [],
        })

    for item in sidebarSyncState['spaceModels']:
        if isinstance(item, str):
            continue

        space_index = get_space_index(spaces, item['value']['id'])
        if space_index == -1:
            continue

        emoji = get_value(item, 'value.customInfo.iconType.emoji_v2', '')
        spaces[space_index]['title'] = emoji + item['value']['title']

        for index, childId in enumerate(item['value']['containerIDs']):
            if childId == 'pinned':
                spaces[space_index]['pinnedId'] = item['value']['containerIDs'][index + 1]
            elif childId == 'unpinned':
                spaces[space_index]['unpinnedId'] = item['value']['containerIDs'][index + 1]

        item = items.get(spaces[space_index]['pinnedId'], None)
        if item:
            for childId in item['value']['childrenIds']:
                subItem = items.get(childId, None)
                if subItem:
                    bookmark = item2bookmark(subItem, items)
                    spaces[space_index]['pinneds'].append(bookmark)

    bookmarks = []
    bookmarks.extend(topAppsContainers)
    for space in spaces:
        bookmark = init_bookmark(space['id'])
        bookmark['title'] = space['title']
        bookmark['children'] = space['pinneds']
        bookmarks.append(bookmark)

    return bookmarks

def bookmarks2html(bookmarks):
    html = '''
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
        It will be read and overwritten.
        DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
'''
    def _bookmarks2html(bookmarks):
        html = ''
        for bookmark in bookmarks:
            if bookmark['url'] == '':
                html += f'<DT><H3>{bookmark["title"]}</H3>\n<DL><p>\n'
                html += _bookmarks2html(bookmark['children'])
                html += '</DL><p>\n'
            else:
                html += f'<DT><A HREF="{bookmark["url"]}">{bookmark["title"]}</A>\n'
        return html
    html += _bookmarks2html(bookmarks)
    html += '</DL><p>\n'
    return html

def bookmarks2chrome(bookmarks):
    chromeBookmarks = {
        'children': [],
        'date_added': '0',
        'date_last_used': '0',
        'date_modified': '0',
        'guid': '',
        'id': '1',
        'name': 'Bookmarks bar',
        'type': 'folder',
    }
    def _bookmarks2chrome(bookmarks, id = 0):
        chromeBookmarks = []
        for bookmark in bookmarks:
            id += 1
            chromeBookmarkItem = {
                'date_added': '0',
                'date_last_used': '0',
                'date_modified': '0',
                'guid': bookmark['id'],
                'id': id,
                'name': bookmark['title'],
                'type': 'folder',
            }
            if bookmark['children'] and len(bookmark['children']) > 0:
                chromeBookmarkItem['children'] = _bookmarks2chrome(bookmark['children'], id)
                chromeBookmarkItem['type'] = 'folder'
            else:
                chromeBookmarkItem['type'] = 'url'
                chromeBookmarkItem['url'] = bookmark['url']
            chromeBookmarks.append(chromeBookmarkItem)
        return chromeBookmarks
    chromeBookmarks['children'] = _bookmarks2chrome(bookmarks, 1)
    return chromeBookmarks

def check_version():
    try:
        response = requests.get(f'https://api.github.com/repos/{REPO}/releases/latest', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['tag_name'] != VERSION:
                print_warning(f'New version available: {data["tag_name"]}')
    except Exception as e:
        pass

def print_help():
    commander = 'python3 main.py'
    if getattr(sys, 'frozen', False):
        commander = os.path.basename(sys.executable)

    '''
    --import-to-firefox
        Import bookmarks into Firefox browser.
        将书签导入到 Firefox 浏览器中。

    --import-to-safari
        Import bookmarks into Safari browser.
        将书签导入到 Safari 浏览器中。
    '''

    print(f'''Use: {commander} [options]
Options:
    --sidebar-file="~/Library/Application Support/Arc/StorableSidebar.json"
        The path of StorableSidebar.json file of Arc browser. It is a file used to store the sidebar data of Arc browser.
        In general, you don't need to specify this parameter. If you don't specify this parameter, the program will use the default path.
        Arc 浏览器的 StorableSidebar.json 文件路径。它是用于存储 Arc 浏览器的侧边栏数据的文件。
        一般情况下，不需要指定该参数。如果不指定该参数，程序会使用默认的路径。

    --save-json=bookmark.json
        Save bookmarks to json file.
        将书签保存到 json 文件中。

    --save-html=bookmark.html
        Save bookmarks to html file. Can be used to import into the browser.
        将书签保存到 html 文件中。可用于导入到浏览器中。

    --import-to-chrome
        Import bookmarks into Chrome browser.
        将书签导入到 Chrome 浏览器中。

        --chrome-bookmarks-file="~/Library/Application Support/Google/Chrome/Default/Bookmarks"
            The path of Bookmarks file of Chrome browser. It is a file used to store the bookmarks of Chrome browser.
            In general, you don't need to specify this parameter. If you don't specify this parameter, the program will use the default path.
            Chrome 浏览器的 Bookmarks 文件路径。它是用于存储 Chrome 浏览器的书签的文件。
            一般情况下，不需要指定该参数。如果不指定该参数，程序会使用默认的路径。

        --chrome-import-node=bookmark_bar
            The node where the bookmarks are imported into Chrome browser. The default is bookmark_bar.
            Can be imported into bookmark_bar or other nodes.
            将书签导入到 Chrome 浏览器中的节点。默认为 bookmark_bar。
            可以导入到 bookmark_bar 或 other 节点中。

    --import-to-edge
        Import bookmarks into Edge browser.
        将书签导入到 Edge 浏览器中。

        --edge-bookmarks-file="~/Library/Application Support/Microsoft Edge/Default/Bookmarks"
            The path of Favorites file of Edge browser. It is a file used to store the bookmarks of Edge browser.
            In general, you don't need to specify this parameter. If you don't specify this parameter, the program will use the default path.
            Edge 浏览器的 Favorites 文件路径。它是用于存储 Edge 浏览器的书签的文件。
            一般情况下，不需要指定该参数。如果不指定该参数，程序会使用默认的路径。

        --edge-import-node=bookmark_bar
            The node where the bookmarks are imported into Edge browser. The default is bookmark_bar.
            Can be imported into bookmark_bar or other nodes.
            将书签导入到 Edge 浏览器中的节点。默认为 bookmark_bar。
            可以导入到 bookmark_bar 或 other 节点中。

Examples:
    {commander} --save-json=bookmark.json
    {commander} --save-html=bookmark.html
    {commander} --save-json=bookmark.json --save-html=bookmark.html
    {commander} --sidebar-file="~/Library/Application Support/Arc/StorableSidebar.json" --save-json=bookmark.json --save-html=bookmark.html
    {commander} --import-to-chrome
    {commander} --import-to-chrome --import-to-edge
    ''')

if __name__ == '__main__':
    arguments = sys.argv
    arguments.pop(0)

    print(f'arc-bookmarks {VERSION}')
    print(f'Github: {GITHUB}')
    check_version()
    print('')

    if len(arguments) == 0:
        print_help()
        sys.exit()

    SidebarFile = '~/Library/Application Support/Arc/StorableSidebar.json'
    saveJson = False
    saveJsonFile = 'bookmark.json'
    saveHtml = False
    saveHtmlFile = 'bookmark.html'
    importToChrome = False
    importChromeNode = 'bookmark_bar' # bookmark_bar, other
    chromeBookmarksFile = '~/Library/Application Support/Google/Chrome/Default/Bookmarks'
    importToEdge = False
    importEdgeNode = 'bookmark_bar' # bookmark_bar, other
    edgeBookmarksFile = '~/Library/Application Support/Microsoft Edge/Default/Bookmarks'
    importToFirefox = False
    importToSafari = False
    for argument in arguments:
        if argument.startswith('--sidebar-file='):
            SidebarFile = argument.replace('--sidebar-file=', '')
            SidebarFile = os.path.expanduser(SidebarFile)
        elif argument.startswith('--save-json='):
            saveJson = True
            saveJsonFile = argument.replace('--save-json=', '')
            if saveJsonFile == '':
                saveJsonFile = 'bookmark.json'
            saveJsonFile = os.path.expanduser(saveJsonFile)
        elif argument.startswith('--save-html='):
            saveHtml = True
            saveHtmlFile = argument.replace('--save-html=', '')
            if saveHtmlFile == '':
                saveHtmlFile = 'bookmark.html'
            saveHtmlFile = os.path.expanduser(saveHtmlFile)
        elif argument == '--import-to-chrome':
            importToChrome = True
        elif argument.startswith('--chrome-bookmarks-file='):
            chromeBookmarksFile = argument.replace('--chrome-bookmarks-file=', '')
            chromeBookmarksFile = os.path.expanduser(chromeBookmarksFile)
        elif argument.startswith('--chrome-import-node='):
            importChromeNode = argument.replace('--chrome-import-node=', '')
            if importChromeNode not in ['bookmark_bar', 'other']:
                print_error(f'Unknown chrome import node: {importChromeNode}')
                sys.exit()
        elif argument == '--import-to-edge':
            importToEdge = True
        elif argument.startswith('--edge-bookmarks-file='):
            edgeBookmarksFile = argument.replace('--edge-bookmarks-file=', '')
            edgeBookmarksFile = os.path.expanduser(edgeBookmarksFile)
        elif argument.startswith('--edge-import-node='):
            importEdgeNode = argument.replace('--edge-import-node=', '')
            if importEdgeNode not in ['bookmark_bar', 'other']:
                print_error(f'Unknown edge import node: {importEdgeNode}')
                sys.exit()
        elif argument == '--import-to-firefox':
            importToFirefox = True
        elif argument == '--import-to-safari':
            importToSafari = True
        elif argument == '--help':
            print_help()
            sys.exit()
        elif argument == 'main.py':
            pass
        else:
            print_error(f'Unknown argument: {argument}')
            sys.exit()

    bookmarks = get_bookmarks(SidebarFile)
    if saveJson:
        try:
            with open(saveJsonFile, 'w', encoding='utf-8') as f:
                json.dump(bookmarks, f, indent=4, ensure_ascii=False)
                print_success(f'Save json file success: {saveJsonFile}')
        except Exception as e:
            print_error(f'Save json file failed: {e}')

    if saveHtml:
        try:
            with open(saveHtmlFile, 'w', encoding='utf-8') as f:
                f.write(bookmarks2html(bookmarks))
                print_success(f'Save html file success: {saveHtmlFile}')
        except Exception as e:
            print_error(f'Save html file failed: {e}')

    if importToChrome:
        chromeBookmarksFile = os.path.expanduser(chromeBookmarksFile)
        if not os.path.exists(chromeBookmarksFile):
            print_error(f'Chrome bookmarks file not exists: {chromeBookmarksFile}')
        try:
            chromeBookmarks = bookmarks2chrome(bookmarks)
            with open(chromeBookmarksFile, 'r', encoding='utf-8') as f:
                chromeBookmarksJson = json.load(f)
                if importChromeNode == 'bookmark_bar':
                    chromeBookmarksJson['roots']['bookmark_bar']['children'] = chromeBookmarks['children']
                else:
                    chromeBookmarksJson['roots']['other']['children'] = chromeBookmarks['children']
            with open(chromeBookmarksFile, 'w', encoding='utf-8') as f:
                json.dump(chromeBookmarksJson, f, indent=4, ensure_ascii=False)
                print_success(f'Import bookmarks to Chrome success: {chromeBookmarksFile}')
                print_success('Please restart Chrome to take effect.')
        except Exception as e:
            print_error(f'Import bookmarks to Chrome failed: {e}')

    if importToEdge:
        edgeBookmarksFile = os.path.expanduser(edgeBookmarksFile)
        if not os.path.exists(edgeBookmarksFile):
            print_error(f'Edge bookmarks file not exists: {edgeBookmarksFile}')
        try:
            chromeBookmarks = bookmarks2chrome(bookmarks)
            with open(edgeBookmarksFile, 'r', encoding='utf-8') as f:
                edgeBookmarksJson = json.load(f)
                if importEdgeNode == 'bookmark_bar':
                    edgeBookmarksJson['roots']['bookmark_bar']['children'] = chromeBookmarks['children']
                else:
                    edgeBookmarksJson['roots']['other']['children'] = chromeBookmarks['children']
            with open(edgeBookmarksFile, 'w', encoding='utf-8') as f:
                json.dump(edgeBookmarksJson, f, indent=4, ensure_ascii=False)
                print_success(f'Import bookmarks to Edge success: {edgeBookmarksFile}')
                print_success('Please restart Edge to take effect.')
        except Exception as e:
            print_error(f'Import bookmarks to Edge failed: {e}')

    sys.exit()