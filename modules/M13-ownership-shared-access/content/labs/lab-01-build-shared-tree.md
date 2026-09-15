# Lab 1 — Build the Shared Research Tree

> Lesson 1 · Time: ~50 min · Risk: low — VM only, throwaway users/groups (`t-*`),
> all under `/srv/t-lab`

## Goal

Build the complete shared-directory pattern from Lesson 1 — group, setgid,
umask-aware newborns, sticky drop-box — and *prove* every property by acting as
the users.

## Part 0 — Cast (10 min, VM)

```console
$ sudo groupadd t-lab
$ sudo adduser --disabled-password --gecos "Alice" t-alice
$ sudo adduser --disabled-password --gecos "Bob" t-bob
$ sudo usermod -aG t-lab t-alice; sudo usermod -aG t-lab t-bob
$ getent group t-lab
```

Acting as users: `sudo -iu t-alice` (opens a shell *as* them — read-only
preview of M14's `sudo -i`; `exit` to return). Confirm `id` shows `t-lab`.

## Part 1 — The skeleton (10 min)

```console
$ sudo mkdir -p /srv/t-lab/{datasets,results,inbox}
$ sudo chgrp -R t-lab /srv/t-lab
$ sudo chmod 2770 /srv/t-lab /srv/t-lab/datasets /srv/t-lab/results
$ sudo chmod 3770 /srv/t-lab/inbox
$ ls -ld /srv/t-lab /srv/t-lab/*
```

Predict *before* looking: which lines show `s`, which show `t`, and why.

## Part 2 — Prove the inheritance (15 min)

As t-alice (`sudo -iu t-alice`):

```console
$ echo "run 42 data" > /srv/t-lab/datasets/metrics.csv
$ ls -l /srv/t-lab/datasets/metrics.csv     # group stamp?
```

As t-bob (second `sudo -iu`):

```console
$ echo "appended" >> /srv/t-lab/datasets/metrics.csv    # works? why exactly?
$ ls -l /srv/t-lab/datasets/metrics.csv                 # whose name owns it now?
```

Return to your user. Log the causal chain: **setgid → group stamp → umask 002 →
group-writable newborn** — one sentence per link.

## Part 3 — The sticky drop-box (10 min)

As t-alice: `echo submission-1 > /srv/t-lab/inbox/alice-sub.txt`.
As t-bob:

```console
$ cat /srv/t-lab/inbox/alice-sub.txt        # readable? (mode of newborn?)
$ rm /srv/t-lab/inbox/alice-sub.txt         # quote the denial
$ echo evil > /srv/t-lab/inbox/alice-sub.txt   # append/overwrite? quote it
```

Which single bit produced each denial? Remove it (`sudo chmod 2770 inbox`),
repeat as t-bob, observe the sabotage become possible, **restore 3770** — and
write the one-paragraph incident note you'd send the lab about why the sticky
bit is non-negotiable there.

## Part 4 — The audit (5 min)

```console
$ ls -lR /srv/t-lab | head -30
$ find /srv/t-lab -type d -printf '%m %u:%g %p\n' | sort
```

Paste both into the log. End state must be: all dirs team-grouped, setgid
everywhere, sticky on inbox, zero `o` access. Any drift: fix and re-audit.

## Wrap-up checklist

- [ ] Cast built with `--disabled-password` + `sudo -iu` verified
- [ ] Inheritance chain demonstrated with both users acting
- [ ] Sticky-bit before/after sabotage documented
- [ ] Final audit pasted; zero drift
- [ ] Cleanup: `sudo userdel -r t-alice t-bob; sudo groupdel t-lab; sudo rm -rf /srv/t-lab`
      (record it even though it's the end)
