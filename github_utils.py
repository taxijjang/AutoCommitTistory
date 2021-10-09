import json
from json import JSONDecodeError

from github import Github
from github import UnknownObjectException


class GithubUtil:
    def __init__(self, access_token):
        self._access_token = access_token
        self._repo = None

    def set_github_repo(self, repository_name):
        repository_name = "AutoCommitTistory"
        """
        github repo object를 얻는 함수
        :param repository_name: 해당 repo의 이름
        :return: repo object
        """
        g = Github(self._access_token)
        self._repo = g.get_user().get_repo(repository_name)

    def upload_github_issue(self, title, body, labels=None):
        """
        해당 repo의 issue에 새롭게 작성된 post의 내용을 등록하는 함수
        :param title: 이슈 제목
        :param body: 이슈 내용
        :param labels: 이슈의 labels
        :return: None
        """
        self._repo.create_issue(title=title, body=body, labels=labels)

    def upload_github_push(self, message, content, path, branch):
        """
        해당 repo에 변경된 json file을 push 해주는 함수
        :param message: push message
        :param content: push content
        :param path: push 할 대상의 file 위치
        :param branch: push 할 branch
        :return: None
        """
        try:
            contents = self._repo.get_contents(path, branch)
            data = json.loads(contents.decoded_content.decode('utf-8'))
            data.update(content)
            data = dict(sorted(data.items()))
            data = json.dumps(data, ensure_ascii=False, indent='\t')
            self._repo.update_file(contents.path, message, data, contents.sha, branch=branch)
        except JSONDecodeError:
            data = dict(sorted(content.items()))
            data = json.dumps(data, ensure_ascii=False, indent='\t')
            self._repo.update_file(contents.path, message, data, contents.sha, branch=branch)
        except UnknownObjectException:
            # if old file is not exists make new file
            data = json.dumps(content, ensure_ascii=False, indent='\t')
            self._repo.create_file(path, message, data, branch=branch)
