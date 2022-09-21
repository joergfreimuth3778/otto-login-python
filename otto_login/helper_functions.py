import subprocess


def run_cmd(cmd):
    try:
        process = subprocess.run(cmd.split(),
                                 check=True,
                                 stdout=subprocess.PIPE,
                                 universal_newlines=True,
                                 stderr=subprocess.DEVNULL)
        return process.stdout
    except Exception as e:
        raise Exception(f"ERROR running {cmd}")
