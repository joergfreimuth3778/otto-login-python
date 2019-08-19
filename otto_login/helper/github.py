import os
import requests
import subprocess

from otto_login import settings


def clone_github_repos():
    i = 0
    threads = []

    for repo in get_all_repos():
        repo_path = path(repo)

        if os.path.exists(repo_path):
            threads.append(pull_repo(repo_path))
        else:
            threads.append(clone_repo(repo_path, repo))

        i += 1

        if i % 30 == 0:
            threads = handle_threads(threads)

    handle_threads(threads)


def handle_threads(threads):
    for thread in threads:
        try:
            thread.wait(5)
        except subprocess.TimeoutExpired:
            thread.kill()
        except:
            raise

    return []


def path(repo):
    return f'{settings.local_repo_path}/{str(repo)[len(settings.github_repo_prefix):]}'


def pull_repo(local_path):
    return subprocess.Popen(
        ['git', '-C', local_path, 'pull', '-r']
    )


def clone_repo(local_path, repo):
    return subprocess.Popen(
        ['git', 'clone', f'git@{settings.github_base}/{settings.github_org}/{repo}', local_path]
    )


def get_all_repos():
    page = 1
    all_repos = set()

    repos = get_repos(page)

    while len(repos) > 0:
        all_repos.update(repos)
        page += 1
        repos = get_repos(page)

    return all_repos


def get_repos(page):
    page_size = 100

    result = requests.get(
        f'{settings.github_api}'
        f'/teams/'
        f'{settings.github_team_id}/'
        f'repos?'
        f'access_token={settings.github_token}&'
        f'per_page={page_size}&'
        f'page={page}'
    )

    return {r['name'] for r in result.json()}
