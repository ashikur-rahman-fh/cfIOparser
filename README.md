# Codeforces tools
Tools that makes participating in codeforces contest the easiest

## Development guide
1. Install python in your development machine. Python 3.10.8 is recomended.
2. Create a python virtual environment called `devenv`. Activate the environment and install the dependencies from the `requirements.txt` file.
3. `cp.py` is the entrypoint of the application.

## Usage
To parse a contest just use the command `python cp.py -c <contest_id>`. - Contest ID is the suffix url that comes in the url. Ex: `https://codeforces.com/contest/1520` the contest ID will be `1520`.
