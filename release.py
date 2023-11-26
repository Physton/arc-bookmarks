import os
import sys
import json
import shutil
import requests
from github import Github
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('GITHUB_TOKEN')
REPO = 'Physton/arc-bookmarks'
GITHUB = f'https://github.com/{REPO}'
GITHUB_AUTH = f'https://{TOKEN}:{TOKEN}@github.com/{REPO}'

main_path = os.path.dirname(__file__)
release_path = os.path.join(main_path, 'release')

# 删除release目录
if os.path.exists(release_path):
    shutil.rmtree(release_path)

# git clone
os.system(f'git clone {GITHUB} {release_path}')

# 读取 main.py 中的 VERSION = 'v0.0.1'
with open(os.path.join(release_path, 'main.py'), 'r') as f:
    for line in f.readlines():
        if 'VERSION' in line:
            version = line.split('=')[1].strip().strip("'")
            break

if not version:
    print('Version not found.')
    sys.exit(1)

# 创建GitHub API客户端
g = Github(TOKEN)

# 获取仓库对象
repo = g.get_repo(REPO)

try:
    # 创建标签
    tag_name = f'{version}'
    commit_sha = repo.get_commits()[0].sha  # 替换为要标记的提交的SHA
    tag_message = 'Release {version}'
    repo.create_git_tag(tag_name, tag_message, commit_sha, 'commit')

    # 创建引用（引用标签）
    ref_name = f'refs/tags/{tag_name}'
    ref_sha = repo.get_git_ref('heads/main').object.sha
    repo.create_git_ref(ref_name, ref_sha)

    # 创建发布
    release_title = f'{version}'  # 发布标题
    release_body = ''  # 发布正文
    release = repo.create_git_release(tag_name, release_title, release_body)

    # 上传文件到发布
    file_name = 'arc-bookmarks'
    file_path = os.path.join(main_path, 'dist', file_name)
    file_path = os.path.abspath(file_path)
    release.upload_asset(file_path, content_type='application/octet-stream', label=file_name)

    # 打包 repo 目录
    file_name = 'arc-bookmarks.zip'
    file_path = os.path.join(release_path, file_name)
    os.system(f'cd {release_path} && zip -r {file_name} ./*')
    release.upload_asset(file_path, content_type='application/octet-stream', label=file_name)

    # 删除 repo 目录
    shutil.rmtree(release_path)
except Exception as e:
    # 删除 tag 和 release
    repo.get_git_ref(f'tags/{tag_name}').delete()
    repo.get_release(tag_name).delete_release()
    # 抛出异常
    raise e
