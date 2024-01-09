[![coverage report](https://gitlab.com/nobodyinperson/annextimelog/badges/main/coverage.svg)](https://gitlab.com/nobodyinperson/annextimelog/-/commits/main)
[![PyPI version](https://badge.fury.io/py/annextimelog.svg)](https://badge.fury.io/py/annextimelog)
[![REUSE status](https://api.reuse.software/badge/gitlab.com/nobodyinperson/annextimelog)](https://api.reuse.software/info/gitlab.com/nobodyinperson/annextimelog)

> ⚠️  This tool is early development. The most basic time tracking feature (recording, deletion, time frame search) as well as syncing are implemented though.

# `annextimelog` - ⏱️ [Git Annex](https://git-annex.branchable.com)-backed Time Tracking

This is a brainstorm for a [Git Annex](https://git-annex.branchable.com)-backed time tracker.
The idea originated across some of my Mastodon threads:

- https://fosstodon.org/@nobodyinperson/109596495108921683
- https://fosstodon.org/@nobodyinperson/109159397807119512
- https://fosstodon.org/@nobodyinperson/111591979214726456

The gist is that I was (and still am) unhappy with the existing time tracking solutions. I worked with [hledger's timeclock](https://hledger.org/1.32/hledger.html#timeclock-format) and [timewarrior](https://timewarrior.net/) each for quite some time and built my own workflow and scripts around them.

## ✅ Requirements

Over the years, the below features turned out to be **my** personal requirements for a time-tracking system (**TL;DR**: easy and intuitive recording, hassle-free syncing, data export for further analysis).
Here is a table comparing annextimelog with [timewarrior](https://timewarrior.net/) and [hledger timeclock](https://hledger.org/1.32/hledger.html#timeclock-format):

✅ = feature available, 🟡 = partly available, ❌ = not available

| feature                                            | `timewarrior` | `hledger` timeclock    | `annextimelog`                       |
|----------------------------------------------------|---------------|------------------------|--------------------------------------|
| precise **start and end times**                    | ✅            | ✅                     | ✅ as git-annex metadata             |
| tracking of overlapping/simultaneous periods       | ❌            | 🟡 (separate files)    | ✅ backend can do it                 |
| nice, colourful, **graphical summary**             | ✅            | 🟡                     | ✅ with Python `rich`, more planned  |
| **plain text** data storage                        | ✅            | ✅                     | 🟡 buried in `git-annex` branch      |
| git-friendly, **merge conflict free data format**  | 🟡¹           | 🟡¹                    | ✅ git-annex’ own merge strategy     |
| arbitrary **tags** attachable to tracked periods   | ✅            | 🟡 hledger tags²       | ✅ just git-annex metadata           |
| arbitrary **notes** attachable to tracked periods  | 🟡³           | 🟡 hledger tags²       | ✅ just git-annex metadata           |
| tags can have **values**                           | ❌            | ✅ hledger tags²       | ✅ just git-annex metadata           |
| **files** attach-/linkable to tracked periods      | ❌            | 🟡 path as `file:` tag | 🟡 annexed files, linking is planned |
| **cli** to start, stop, edit, etc. tracked periods | ✅⁴           | ❌ own scripts needed  | 🟡 very basic, more planned          |
| **plugin system**                                  | 🟡⁵           | 🟡⁶ (hledger’s own)    | ❌ git-style plugin system planned   |
| **data export** to common format                   | ✅ (JSON)     | ✅ (CSV, JSON)         | ✅ as timeclock, JSON, cli commands  |
| **syncing** functionality built-in                 | ❌            | ❌                     | ✅ git-annex’s purpose is syncing    |
| **multi-user** support                             | ❌            | ❌                     | 🟡 e.g. use tag `user=NAME`          |

¹last line is always modified, merge conflicts can arise when working from different machines

²[hledger tags](https://hledger.org/1.32/hledger.html#tags) have limitations, e.g. no spaces, colons, commas, etc.

³timewarrior annotations can't contain newlines for example. I wrote an extension to edit your annotation in your `$EDITOR` and optionally GPG-encrypt it, which lets you add newlines. Quite an inconvenience.

⁴timewarrior’s cli has some nasty inconveniences (e.g. no shortcut for ‘yesterday’, must painfully type out the full date, no intelligence to operate only on yesterday, gets confused and errors out in certain combinations of start/end times, etc…)

⁵timewarrior extensions ([here mine](https://gitlab.com/-/snippets/2498711)) are just fed the data via STDIN, not other command-line arguments. Not as useful as the git-style plugin system.

⁶for the analysis part, `hledger` plugins can be used. But as there is no actual cli to manage the data, there’s no plugin system for that.

## 🛠️ Implementation

To learn more about how `annextimelog` works under the hood with git-annex as backend, have a look at [doc/internals](doc/internals.md).

## 📦 Installation

You can run this tool if you have [nix](https://nixos.org) installed:

```bash
# drop into a temporary shell with the command available
nix shell gitlab:nobodyinperson/annextimelog

# install it
nix profile install gitlab:nobodyinperson/annextimelog
```

On Arch Linux you can install from the [AUR](https://aur.archlinux.org/packages/annextimelog) with your favorite helper, or directly with pacman from [this user repository](https://wiki.archlinux.org/title/Unofficial_user_repositories#alerque).

```bash
# use an AUR helper to install
paru -S annextimelog
```

Otherwise, you can install it like any other Python package, e.g. with `pip` or better `pipx`:

```bash
pipx install annextimelog

# latest development version
pipx install git+https://gitlab.com/nobodyinperson/annextimelog
```

Note that in this case you will need to install [git-annex](https://git-annex.branchable.com) manually.

Any of the above makes the `annextimelog` (or `atl`) command available.

## ❓ Usage

```bash
# Show help page
atl --help
atl tr --help # subcommand help page

# Show exactly what's going on underneath (more -v → more detail)
atl -vvvvv ...

# Add a remote to sync to
atl git remote add myserver git@myserver.com:...

# Sync status with git annex
atl sync

# Track a time period with metadata
atl track 10:00 15:00 work @home ="make a title with the equals sign" :"make a note with a colon"
atl tr 15:00 - 10min ago code @home # timewarrior-style time ranges

# List events
atl ls # default: what happened today
atl ls --week|--month|--all  # predefined periods
atl ls -b 2023-01-01 -e 2023-02-01  # specific time period

# Delete an event
atl rm 3QicA4G4

# Output formats
atl -O timeclock ls -a # output all events in hledger timeclock format
atl -O timeclock ls -a | hledger -f timeclock:- bal --daily # analyse with hledger
atl -O json ls -a # output JSON
```

There's some example periods in the `doc` folder you can try out.

## ⚙️  Configuration

`annextimelog` reuses git's configuration system. You can configure annextimelog per-repo (`atl git config ...`), per-user (`atl git config --global ...`) or system-wide (typically in `/etc/gitconfig`).

```bash
# list all annextimelog configs known to git
atl git config --get-regexp '^annextimelog'

# open the git config in your $EDITOR
atl git config --edit

# let the week start at Sunday
atl git config annextimelog.weekstartssunday true

# Don't commit, except in 'annextimelog sync'.
# This speeds up things but reduces granularity to undo changes
atl git config annextimelog.commit false

# Skip steps that are not strictly necessary.
# This speeds up things but might leave the repository in a less ordered state.
atl git config annextimelog.fast true
```

## 🛠️ Development

This project uses [poetry](https://python-poetry.org/), so you can run the following in this repository to get into a development environment:

```bash
poetry install
poetry shell
# now you're in a shell with everything set up
```

Other:

```bash
# Auto-run mypy when file changes:
just watch-mypy

# Auto-run tests when file changes:
just watch-test

# Test how a sequence of command-line args is interpreted as event metadata
just test-tokens work @home note=bla myfield+=one,two,three 2h ago until now

# Run tests against a different Python version
just test-with-python-version 3.10
```
