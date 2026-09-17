# Frequently Made Mistakes — The Ten Classic Hits

> Seen every term in this course. Each: the mistake, why it feels
> right, what it actually does, and the **habit that replaces it**.
> The habits are the exam-grade content — the exam shows the mistake's
> aftermath and asks you to diagnose it.

## 1. `sudo` as reflex

**Why it feels right:** the error said "Permission denied"; sudo makes
it go away.
**What it does:** runs *everything* as root — a typo now has admin
power; files created become root-owned, generating tomorrow's
permission mystery.
**The habit:** ask *why* the operation needed privilege. If the answer
is "the file was root-owned", use targeted elevation (`sudo chown` on
that file), or keep the work in your own tree. `sudo` is a scalpel,
not a hammer.

## 2. Unquoted variables in scripts

**Why it feels right:** `rm $DIR/old` works when DIR has no spaces.
**What it does:** on the day DIR contains a space — or is empty —
word-splitting turns `rm $DIR/old` into something you did not type.
Empty `$DIR` makes it `rm /old`.
**The habit:** `"$DIR"`, always; plus a guard:
`: "${DIR:?DIR is unset}"`.

## 3. Blind `rm -rf` composition

**Why it feels right:** the target dir is "just scratch".
**What it does:** an unexpanded variable (`rm -rf $TMPDIR/` with
TMPDIR empty) or a stray glob turns the command into a different
instruction entirely.
**The habit:** the course's safety card —
`echo` the expansion first, prefer `rmdir`/explicit paths, never
`~`-adjacent globs, and keep anything destructive inside a created
scratch dir you can name aloud.

## 4. `chmod 777` as a permission fix

**Why it feels right:** everyone can work; nobody complains.
**What it does:** grants write to *every* account on the machine,
including services; destroys the meaning of group membership.
**The habit:** the shared-dir design (M13): owner `rwx`, group `rwx`
with SGID, others `r-x` at most — 2775. Fix the *group*, not the
gates.

## 5. Restart as a diagnostic

**Why it feels right:** reboot/restart fixed it; done.
**What it does:** resets the evidence and the symptom together. The
next failure teaches you nothing, and the real fault (bad config,
full disk, expired cert) survives the restart.
**The habit:** evidence first — `status`, then the journal — *then*
restart as a deliberate test, and verify what changed.

## 6. Editing crontabs without environment awareness

**Why it feels right:** the script runs fine from the shell.
**What it does:** cron's PATH/HOME/cwd differ; the job fails at 2 a.m.
and mails nobody, because output wasn't redirected.
**The habit:** absolute paths for interpreter and files, a PATH line
in the crontab, and `>/log 2>&1` from day one. Test with a 1-minute
`* * * * *` schedule before trusting the real one.

## 7. Installing into the wrong Python

**Why it feels right:** `pip install pandas` printed "Successfully
installed".
**What it does:** pip and python can belong to different
environments; the import still fails, or worse, succeeds in one
notebook and fails in another.
**The habit:** `python3 -m pip install` (binds pip to the interpreter
you'll run), inside a venv, verified with `which python3` +
`python3 -m pip -V`.

## 8. Treating containers as persistent

**Why it feels right:** the data was "in the container".
**What it does:** the writable layer dies with the container; `docker
rm` takes a week of results with it.
**The habit:** outputs to bind mounts/volumes (`-v`), images
immutable, containers disposable — verify the mount with
`docker inspect` *before* the first real run.

## 9. Forgetting `enable` after `start`

**Why it feels right:** "it's running, we're done."
**What it does:** the service evaporates at reboot; the "gone
overnight" ticket writes itself.
**The habit:** say the pair aloud — *start runs now, enable wires
boot* — and check both: `is-active` **and** `is-enabled`.

## 10. Copying without verifying

**Why it feels right:** the transfer printed no error.
**What it does:** silent truncation, stale targets, or wrong
trailing-slash semantics land incomplete or misplaced data into the
pipeline, discovered at analysis time — the most expensive place.
**The habit:** checksum manifests for datasets (sha256), rsync dry-run
first, `--itemize-changes` when the *what* matters, and verify counts
against the source — every transfer is a claim until verified.

---

## The meta-habit

Every mistake above is the same story: **an action taken on
assumption, where evidence was one command away.** The course's
repeated discipline — read the error, check the state, quote the
line, then act — is not bureaucracy; it is what separates the
operator from the passenger.
