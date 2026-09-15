# Lab 1 — The Process Zoo: Build It, Then Map It

> Module 18 · Unit 5 · Difficulty: Beginner-friendly
> Environment: your own VM/WSL2, normal user · Time: ~40 min
> Prerequisites: [Lesson 1](../lessons/01-processes-inspection.md)

You'll construct a small *forest* of processes on purpose, then use every
inspection tool from the lesson to describe it. Deliverable: a complete
"zoo map" in `lab-log.md`.

## 0. Setup

```console
$ mkdir -p ~/lab18 && cd ~/lab18
$ echo '=== LAB18 ===' >> ~/lab-log.md
```

## Part A — build the zoo

Open **one terminal** and create a launcher that spawns children:

```console
$ bash -c '
  echo "launcher PID: $$"
  sleep 300 &
  python3 -m http.server 8123 &
  wait
' &            # the launcher itself is backgrounded
[1] 7100
launcher PID: 7100
```

Open a **second terminal** (this is your "observation deck") for all
inspection commands. The zoo now contains: a bash launcher, a `sleep`, a
python http.server, plus your shells — four families, one tree each way.

## Part B — map it four ways

In the observation deck:

```console
$ pgrep -a -u $USER                     # 1. flat census (PIDs + commands)
$ pstree -p 7100                        # 2. the launcher's subtree — draw it
$ ps -u $USER -o pid,ppid,stat,ni,pcpu,rss,etime,cmd --forest   # 3. tree view
$ ps -fp $(pgrep -d, -u $USER)          # 4. one full-detail table of mine
```

**Record in `lab-log.md`:**
- the drawn tree of the launcher's family (from pstree), with PIDs;
- which process is the *parent* of `sleep` — and what its PPID says;
- the STAT of each member. Expect `S` for sleepers — justify why in one
  sentence (what are they waiting on?).

## Part C — the http.server experiment

```console
$ curl -s http://127.0.0.1:8123/ -o /dev/null -w "%{http_code}\n"   # 200?
$ ps -o pid,pcpu,stat,rss -p $(pgrep -f "http.server 8123")
```

Now hit it in a loop and watch CPU live:

```console
$ for i in $(seq 1 300); do curl -s http://127.0.0.1:8123/ -o /dev/null; done &
$ top -p $(pgrep -f "http.server 8123")    # watch %CPU; q to quit
```

**Record:** the %CPU you observed (it will be small — why? what is the
server *mostly doing* between requests, per Lesson 1 §3?). Kill the loop's
curl first (`pkill -f "seq 1 300"` — after `pgrep -af seq`!), then:

## Part D — the zombie minute (optional but worth it)

Zombies require a dead child and a living, unreaping parent — so we make
one deliberately with a negligent parent:

```console
$ bash -c 'sleep 1 & exec sleep 300' &    # child exits; its parent... actually
```

That's fiddly; the *reliable* classroom zombie is a python parent that
never calls wait:

```console
$ python3 - <<'EOF' &
import subprocess, time
subprocess.Popen(['true'])      # child exits immediately
time.sleep(120)                  # parent never reaps
EOF
$ sleep 2; ps axo pid,stat,cmd | grep ' Z '     # meet the zombie
```

**Record:** its STAT is `Z` and its PPID is the python PID — confirm both.
Then kill the python parent (TERM is fine — *why can't you kill the
zombie?*) and show the zombie vanished (re-parented to PID 1 and reaped).
This is the whole zombie lifecycle in 60 seconds.

## Part E — teardown & the zoo report

```console
$ pgrep -a -u $USER | grep -E "http.server|sleep 300|python3 -"   # preview!
$ pkill -u $USER -f "http.server 8123"
$ pkill -u $USER -f "sleep 300"
$ jobs   # in the FIRST terminal: the launcher exited when children died? Explain.
```

**Zoo report (deliverable):** one paragraph describing the tree you built:
root → children → grandchildren, each with PID, state, and the observation
tool that told you. If your paragraph needs no tools, you did it from
memory — re-run until the tools, not memory, are the source.

## Done when

- [ ] Tree drawn from `pstree -p` output (not invented)
- [ ] Every zoo member's STAT explained in a sentence
- [ ] http.server CPU observation + the "what is it waiting on" answer
- [ ] Zombie produced, confirmed (Z + PPID), and extinguished
- [ ] Teardown via *scoped* pkill after pgrep preview
