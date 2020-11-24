import os
import re
import subprocess
import shutil

import requests

from otto_login import settings


def clone_github_repos():
    threads = []
    all_threads = []

    to_pull_or_clone, archived_repos = repos_to_pull_or_clone()

    for repo in to_pull_or_clone:
        repo_path = path(repo)

        if os.path.exists(repo_path):
            thread = pull_repo(repo_path)
        else:
            thread = clone_repo(repo_path, repo)

        threads.append(thread)
        all_threads.append(thread)

        if len(threads) % 30 == 0:
            threads = handle_threads(threads)
            print(f'  finished {len(all_threads)} from {len(to_pull_or_clone)}')

    handle_threads(threads)
    print(f'  finished {len(all_threads)} from {len(to_pull_or_clone)}')

    check_result(all_threads)

    cleanup(archived_repos)

    link_files(to_pull_or_clone)


def link_files(all_tr_repos):
    for repo in all_tr_repos:
        link_target=path(repo)
        for link_source in settings.files_to_link:
            file_or_directory = os.path.basename(link_source)
            if not os.path.exists(f"{link_target}/{file_or_directory}"):
                if file_or_directory == 'javaagent' and not akkamann(link_target):
                    continue

                os.symlink(link_source, f"{link_target}/{file_or_directory}")


def akkamann(repo_path):
    sbt_file = f'{repo_path}/build.sbt'
    if os.path.isfile(sbt_file):
        with open(sbt_file, 'r') as file:
            data = file.read()

        return re.search('de.otto.tracking.akkamann', data) is not None
    else:
        return False


def repos_to_pull_or_clone():
    all_repos = get_all_repos()
    active_repos = {r['name'] for r in all_repos if not r['archived']}
    archived_repos = set(map(lambda r: r['name'], all_repos)) - active_repos

    return active_repos, archived_repos


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
    return f'{settings.local_repo_path}/{str(repo).replace(settings.github_repo_prefix,"")}'


def cleanup(archived_repos):
    for repo in archived_repos:
        repo_path = path(repo)
        if os.path.exists(repo_path):
            print(f"remove {repo_path}")
            shutil.rmtree(repo_path)


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
    all_repos = []

    repos = get_repos(page)

    while len(repos) > 0:
        all_repos += repos
        page += 1
        repos = get_repos(page)

    return list(filter(lambda r: r['name'].startswith(settings.github_repo_prefix), all_repos))


def get_repos(page):
    page_size = 100

    result = requests.get(
        f'{settings.github_api}'
        f'/teams/'
        f'{settings.github_team_id}/'
        f'repos?'
        f'per_page={page_size}&'
        f'page={page}',
        headers={'Authorization': f'token {token()}'}
    )
    if result.status_code == 200:
        return result.json()
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
