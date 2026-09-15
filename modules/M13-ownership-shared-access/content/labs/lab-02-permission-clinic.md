# Lab 2 — The Permission Clinic

> Lesson 2 · Time: ~60 min · Risk: low — VM only, sacrificial tree, throwaway users
>
> **You are the on-call admin.** Five broken setups, five tickets. Diagnose with
> the I-G-A-T-E method (Lesson 2 §7) *before* every fix, and apply the *minimal*
> repair. Grading: evidence of diagnosis, not just the fix.

## Setup (10 min, VM)

Build the cast and the *correct* baseline, then break each case on a copy:

```console
$ sudo groupadd t-lab
$ for u in t-alice t-bob t-carol; do sudo adduser --disabled-password --gecos "$u" $u; sudo usermod -aG t-lab $u; done
$ sudo mkdir -p /srv/clinic/{case1,case2,case3,case4,case5/datasets}
$ sudo chgrp -R t-lab /srv/clinic && sudo chmod -R 2770 /srv/clinic
$ sudo -iu t-alice echo baseline > /srv/clinic/case1/probe.txt   # sanity check
```

Run every diagnosis **as the victim** (`sudo -iu t-bob ...`) — not as root.
Root sees everything; that's precisely why root can't diagnose users' failures.

---

## Case 1 — "Bob can't read the dataset" (10 min)

```console
$ sudo chgrp t-lab /srv/clinic/case1 && sudo chmod 2770 /srv/clinic/case1
$ sudo -iu t-alice echo data > /srv/clinic/case1/dataset.csv
$ sudo chmod 640 /srv/clinic/case1/dataset.csv        # then:
$ sudo chgrp t-bob /srv/clinic/case1/dataset.csv      # the actual break
```

Ticket: *t-bob gets "Permission denied" reading `dataset.csv`.*

Expected diagnosis path: `id t-bob` → `namei -l /srv/clinic/case1/dataset.csv`
→ notice the **file's group** isn't the team's → fix (`sudo chgrp t-lab ...`)
→ verify as t-bob. Log: the one-line root cause and why `namei` beat guessing.

## Case 2 — "New files aren't shared" (10 min)

```console
$ sudo chmod 770 /srv/clinic/case2                     # setgid quietly removed
$ sudo -iu t-alice echo x > /srv/clinic/case2/new.txt
$ ls -l /srv/clinic/case2/new.txt                      # group = alice, not t-lab
```

Ticket: *every file t-alice creates is uneditable by the team; re-chmodding
works for a day, then breaks again.*

Diagnose (`ls -ld case2` — what's missing?), then fix **structurally** (the
bit that makes it never-recur), and prove the fix with a second newborn.

## Case 3 — "Carol was removed from the team but still edits" (10 min)

```console
$ sudo -iu t-carol echo y > /srv/clinic/case3/hers.txt
$ sudo gpasswd -d t-carol t-lab                        # revoke membership
$ sudo -iu t-carol echo edited >> /srv/clinic/case3/hers.txt   # STILL WORKS?!
```

Ticket: *we fired Carol's membership but she still edits files.*

Diagnose the two-layer truth: (1) sessions cache memberships — does a *fresh*
`sudo -iu t-carol` still work? (2) the file's mode grants... whom, exactly?
Fix completely (which `chmod` on `hers.txt`?), and write the one-paragraph
"leaver procedure" this case proves every lab needs.

## Case 4 — "The external collaborator" (15 min)

Ticket: *farid (no account design yet — create him:
`sudo adduser --disabled-password t-farid`) must read — only read —
`/srv/clinic/case4/datasets/`, without joining `t-lab`.*

Apply Lesson 2: one ACL entry (+ default ACL so *future* files grant him too),
verify with `getfacl`, act as t-farid to prove read-only-ness (try a write —
quote the denial), then demonstrate the **mask**: `sudo chmod g-rx case4/datasets`
and show what happened to farid's `#effective` line. Restore thoughtfully.

## Case 5 — "Nobody can trace the path" (10 min)

```console
$ sudo chmod o=rx /srv/clinic           # then the break:
$ sudo chmod 770 /srv/clinic            # 'other' loses traversal entirely
$ sudo -iu t-alice ls /srv/clinic/case5/datasets    # fails ABOVE the file!
```

Ticket: *t-alice gets "Permission denied" on a directory she has 2770 on.*

Diagnose with `namei -l /srv/clinic/case5/datasets` and identify the
**component** that stalls traversal. Fix the *minimal* bit (which audience,
which permission?), and state the general rule this case teaches about path
failures.

---

## Clinic report (your deliverable)

Per case, in `lab-log.md`: **symptom → I-G-A-T-E evidence (commands + key
output lines) → root cause (one sentence) → minimal fix → verification (as the
victim) → prevention note** (what design makes this impossible next time).

## Cleanup + wrap-up checklist

```console
$ sudo userdel -r t-alice t-bob t-carol t-farid; sudo groupdel t-lab; sudo rm -rf /srv/clinic
```

- [ ] All five cases diagnosed *before* fixing (evidence logged)
- [ ] Every verification performed as the affected user, not root
- [ ] The mask demonstration (Case 4) and leaver procedure (Case 3) written up
- [ ] Cleanup command executed and recorded
- [ ] One paragraph: which case would have been *hardest* to guess without
      `namei -l`, and why
