# Status

**Status** displays information about all repositories in a given directory.

<div align="center">
    <img
        src="./assets/usage-example.png"
        alt="Status displaying 'git status' for multiple directories at once"
    />
</div>

## Installation

**Requires Python 3.12 or higher.**

```bash
git clone https://github.com/nicdgonzalez/status
```

Once downloaded, add the script to PATH (optional):

```bash
# Make sure `status.py` is executable:
chmod u+x ./status.py

mkdir --parents $HOME/.local/bin \
    && ln --symbolic "$PWD/status.py" "$HOME/.local/bin/status"
```

Once installed, simply run `status --verbose` in the same directory where you
keep your projects:

```bash
status --verbose [PATH]

# If the script is not on PATH, use "./status.py" instead.
# ./status.py --verbose [dirpath]
```
