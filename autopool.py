from multiprocessing import Pool
import subprocess
import sys


def run(cmd, echo=True):
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    stdout, stderr = process.communicate()

    if echo:
        # Since the stdout/stderr streams for each process are being captured
        # we'll need to explicitly write them out if we want console output.
        sys.stdout.write(stdout.decode())
        sys.stdout.flush()
        sys.stderr.write(stderr.decode())
        sys.stderr.flush()

    return {
        'cmd': cmd,
        'returncode': process.returncode,
        'stdout': stdout.decode(),
        'stderr': stderr.decode(),
    }


def autopool(commands, echo=True):
    # Initialize the Pool with the num of commands you intend to run.
    pool = Pool(len(commands))

    results = pool.starmap(run, [(c, echo) for c in commands])

    pool.close()
    pool.join()

    return results


# Now you can invoke multiple commands simultaneously.

parallel_cmds = [
    'ls -al | grep py',
    'echo hello',
    'python3 test.py',
]

results = autopool(parallel_cmds,echo=False)

# "results" is a list -- one item per process run.

# Each item here will be the dict returned by run()

# This way, you can still inspect the return code, stdout/stderr of each command.

print('Look at the `results` object...\n')

# Uncomment this to inspect results in IPython
from IPython import embed
embed()
