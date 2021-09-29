import json
from json import JSONDecodeError

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
    repo.create_issue(title=title, body=body, labels=['new_posting', 'bot'])


def upload_github_push(repo, message, content, path, branch):
    """
    해당 repo에 새롭게 추가된 post 정보가 저장된 Json file을 push하는 함수
    :param repo: repo 이름
    :param message: push message
    :param content: push content
    :param branch:  대상 파일을 push 할 branch 위치
    :return: None
    """
    author = InputGitAuthor(
        'taxijjang',
        'gw9122@naver.com'
    )
    try:
        # update old file to new file
        contents = repo.get_contents(path, branch)
        data = json.loads(contents.decoded_content.decode('utf-8'))
        data.update(content)
        data = dict(sorted(data.items()))
        data = json.dumps(data, ensure_ascii=False, indent="\t")
        repo.update_file(contents.path, message, data, contents.sha, branch=branch)
    except JSONDecodeError:
        data = dict(sorted(content.itmes()))
        data = json.dumps(data, ensure_ascii=False, indent="\t")
        repo.update_file(contents.path, message, data, contents.sha, branch=branch)
    except UnknownObjectException:
        # if old file is not exists make new file
        data = json.dumps(content, ensure_ascii=False, indent="\t")
        repo.create_file(path, message, data, branch=branch)
