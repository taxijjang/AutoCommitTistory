import json

from github import Github
from github import InputGitAuthor
from github import UnknownObjectException

def get_github_repo(access_token, repository_name):
    """
    github repo object를 얻는 함수
    :param access_token: Github access token
    :param repository_name: repo 이름
    :return repo object
    """
    g = Github(access_token)
    repo = g.get_user().get_repo(repository_name)
    return repo


def upload_github_issue(repo, title, body):
    """
    해당 repo에 title 이름으로 issue를 생성하고, 내용을 body로 채우는 함수
    :param repo: repo 이름
    :param title: issue title
    :param body: issue body
    :return: None
    """
    repo.create_issue(title=title, body=body)


def upload_github_push(repo, message, content, path, branch):
    """
    해당 repo에 새롭게 추가된 post 정보가 저장된 Json file을 push하는 함수
    :param repo: repo 이름
    :param message: push message
    :param content: push content
    :param branch:  대상 파일을 push 할 branch 위치
    :return: None
    """
    source = repo.get_branch(branch)
    update = None
    try:
        # update old file to new file
        file = repo.get_contents(path, branch)
        # repo.update_file(path, message, posts_data,)
        print("ASDF")
        update = True
    except UnknownObjectException:
        # if old file is not exists make new file
        file = ''
        update = False


def push(repo, message, new_data, path, branch, update=False):

    file_path = 'auto_commit_tistory_git_action/posts.json'
    old_file = repo.get_contents(file_path, ref="master")
    old_data = json.loads(old_file.decoded_content.decode("utf-8"))
    update_posts = old_data.update(new_data)
    update_data = json.dumps(update_posts, ensure_ascii=False, indent="\t")


    source = repo.get_branch('master')


    head_sha = repo.get_branch('master').commit.sha

    base_tree = repo.get_git_tree(sha=head_sha)
    tree = repo.create_git_tree()
    # repo.create_git_commit(issue_title)