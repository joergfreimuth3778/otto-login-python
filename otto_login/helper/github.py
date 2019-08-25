import os
import requests
import subprocess

from otto_login import settings


def clone_github_repos():
    threads = []
    all_threads = []

    repos = get_all_repos()

    for repo in repos:
        repo_path = path(repo)

        if os.path.exists(repo_path):
            thread = pull_repo(repo_path)
        else:
            thread = clone_repo(repo_path, repo)

        threads.append(thread)
        all_threads.append(thread)

        if len(threads) % 30 == 0:
            threads = handle_threads(threads)
            print(f'  finished {len(all_threads)} from {len(repos)}')

    handle_threads(threads)
    print(f'  finished {len(all_threads)} from {len(repos)}')

    check_result(all_threads)


def check_result(threads):
    for thread in threads:
        if thread.returncode is None or thread.returncode > 0:
            print(f'  ERROR running {" ".join(thread.args)}')


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
        ['git', '-C', local_path, 'pull', '-q', '-r'],
        stderr=subprocess.DEVNULL
    )


def clone_repo(local_path, repo):
    return subprocess.Popen(
        ['git', 'clone', f'git@{settings.github_base}:{settings.github_org}/{repo}', local_path],
        stderr=subprocess.DEVNULL
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
        f'access_token={token()}&'
        f'per_page={page_size}&'
        f'page={page}'
    )
    if result.status_code == 200:
        return {r['name'] for r in result.json()}
    else:
        print(f'ERROR fetching git repos ({result.status_code})')
        exit(1)


def token():
    try:
        process = subprocess.run(settings.github_token.split(),
                                 check=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL,
                                 universal_newlines=True)

        return process.stdout.strip()
    except:
        return settings.github_token
