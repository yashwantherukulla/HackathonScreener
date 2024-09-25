import pygit2
from typing import List
import logging
import os
import shutil
class GitHandler:
    base_path = "./data"

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def clone_repository(self, url: str, team_name: str, base_path="./data") -> pygit2.Repository:
        path = os.path.join(base_path, team_name, "repo")
        try:
            if os.path.exists(path):
                if os.path.exists(os.path.join(path, '.git')):
                    self.logger.info(f"Repository already exists at path: {path}")
                    return pygit2.Repository(path)
                else:
                    self.logger.warning(f"Directory exists but is not a Git repository: {path}")
                    shutil.rmtree(path)
            
            self.logger.info(f"Cloning repository to: {path}")
            pygit2.clone_repository(url, path)
        except pygit2.GitError as e:
            self.logger.error(f"Error while cloning repository: {e}")
            raise e
        except ValueError as e:
            self.logger.error(f"ValueError: {e}")
            if "exists and is not an empty directory" in str(e):
                self.logger.info(f"Removing non-empty directory: {path}")
                shutil.rmtree(path)
                self.logger.info(f"Retrying to clone repository to: {path}")
                pygit2.clone_repository(url, path)
            else:
                raise e
        
    def get_latest_commit(self, repo: pygit2.Repository) -> pygit2.Commit:
        try:
            return repo.head.peel(pygit2.Commit)
        except pygit2.GitError as e:
            self.logger.error(f"Error while getting latest commit: {e}")
            raise e

    def get_file_content(self, repo: pygit2.Repository, file_path: str) -> str:
        try:
            file = repo[file_path]
            return file.data.decode("utf-8")
        except pygit2.GitError as e:
            self.logger.error(f"Error while getting file content: {e}")
            raise e
        

# if __name__ == "__main__":
#     url = "https://github.com/woaitsAryan/regit"
#     base_path = "./cloned_repos"
#     git_handler = GitHandler()
#     repo = git_handler.clone_repository(url, base_path)