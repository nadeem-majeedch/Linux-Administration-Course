# 1 — Linux Command Line

> Learn it: [M05 — Terminal and Shell](../modules/M05-terminal-and-shell/content/README.md) ·
> This is lookup, not understanding.

## Navigation

| Command | Purpose | Syntax | Example |
|---|---|---|---|
| `pwd` | print working directory | `pwd` | `pwd` → `/home/ana` |
| `cd DIR` | change directory | `cd [dir]` | `cd ~/projects/ds-lab` |
| `cd -` | jump to previous directory | `cd -` | toggle between two dirs |
| `cd` | go home | `cd` | shortcut for `cd ~` |
| `cd ..` | up one level | `cd ..` | from `raw/` to its parent |
| `pushd`/`popd` | directory stack | `pushd DIR` | `pushd /var/log` … `popd` |

## Path shortcuts

| Token | Meaning | Example |
|---|---|---|
| `~` | home | `cd ~/data` |
| `.` | this directory | `./script.sh` |
| `..` | parent | `cp ../notes.md .` |
| `-` (in `cd`) | previous dir | `cd -` |

## Listing & inspecting

| Command | Purpose | Important options | Example |
|---|---|---|---|
| `ls` | list files | `-l` long · `-a` hidden · `-h` human sizes · `-t` time-sorted · `-S` size-sorted | `ls -lht` newest first |
| `stat FILE` | full metadata | `-` | `stat data.csv` |
| `file FILE` | detect type | `-i` MIME | `file image.bin` |
| `tree DIR` | recursive view | `-L N` depth limit | `tree ~/project -L 2` |

## History & recall

| Command | Purpose | Example |
|---|---|---|
| `history` | list past commands | `history \| tail -20` |
| `↑`/`↓` | walk history | — |
| `Ctrl+R` | interactive search | type to find, `Enter` runs |
| `!N` | run history entry N | `!513` — **preview with `!513:p`** |
| `!!` | previous command | `sudo !!` |
| `!cmd` | last command starting with `cmd` | `!ssh` |
| `history -a` | append now (not at exit) | shared across terminals |

## Aliases

```bash
alias lht='ls -lht'      # define
alias                    # list
unalias lht              # remove
type ll                  # reveal what an alias is
```
⚠️ Aliases do **not** exist in scripts — safety habits can't live in dotfiles.

## Getting help

| Command | Use when | Example |
|---|---|---|
| `man CMD` | full manual | `man rsync` (`/pattern` to search, `q` quits) |
| `CMD --help` | quick option list | `tar --help` |
| `help CMD` | shell builtins | `help cd` |
| `whatis CMD` | one-line description | `whatis crontab` |
| `apropos KEYWORD` | find the command you've forgotten | `apropos compress` |

## Command shape

```console
command -option --long-option argument1 argument2
```
- Options before arguments, in general; `--` ends options (`rm -- -weirdfile`).
- Short options combine: `ls -lh` = `ls -l -h`.

## Keyboard essentials

`Tab` completion (commands, paths, options) · `Ctrl+C` interrupt ·
`Ctrl+D` end-of-input/exit · `Ctrl+L` clear · `Ctrl+A`/`Ctrl+E` line
start/end · `Ctrl+U`/`Ctrl+W` erase line/word.
