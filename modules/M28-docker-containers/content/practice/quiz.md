# Module 28 Quiz — Docker and Containers

> 22 questions. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Scope: lessons 1–5 and all labs. The safety rules (pin tags, loopback
> ports, targeted cleanup, volume-removal-is-deletion) count as quiz
> material.

## Section A — fundamentals (Q1–6)

**Q1.** State precisely what a container shares with the host and what
it does not. Which two kernel features draw each boundary?

**Q2.** Your VM has 8 GB RAM and runs three Ubuntu VMs poorly. Why do
three containers of the same workload run easily?

**Q3.** Inside a container `ps aux` shows one process at PID 1; the
host's `ps aux` shows that process at PID 5432. Both are true — explain.

**Q4.** Two images both start `FROM python:3.12-slim`. What does the
disk actually hold, and what does `docker system df` report that
`docker images` cannot?

**Q5.** What is the difference between a tag and a digest, and why does
this course pin one by default and name the other the publishing-grade
upgrade?

**Q6.** The `docker` command errors with "Cannot connect to the Docker
daemon." Walk the three suspects in order, with the check for each.

## Section B — CLI & lifecycle (Q7–12)

**Q7.** Explain exactly what `--rm` changes about the container
lifecycle, and when you deliberately *don't* want it.

**Q8.** `docker stop` is sometimes slow, and `docker kill` never is.
What two signals are involved, and what image-side behavior makes
`stop` fast?

**Q9.** A teammate "fixed" a running container via `docker exec`
(added a package), and the fix disappeared after the next
`docker rm`/re-run. Why — and where should the fix have gone?

**Q10.** Decode: a container exits with code 137 shortly after a
memory-hungry job starts. Name the exit arithmetic and the likely
mechanism.

**Q11.** What does `-p 127.0.0.1:8899:8888` guarantee that
`-p 8899:8888` does not — and which earlier module's posture is this?

**Q12.** Why does `docker run ubuntu:24.04` exit immediately, and what
single flag turns it into an interactive session?

## Section C — images, data, networks (Q13–18)

**Q13.** Your Dockerfile runs `pip install` in layer 6 and your
teammate keeps editing source files that are COPY'd in layer 7. Why is
this ordering good — and what happens to build time if the COPY moves
above the pip layer?

**Q14.** Why does `RUN apt-get update && apt-get install -y x && rm -rf
/var/lib/apt/lists/*` produce a small layer while splitting the `rm`
into the next RUN does not?

**Q15.** A Postgres container runs for a week with no volume. Describe
its data's location and fate, then the exact `-v` syntax that fixes it.

**Q16.** Named volume vs bind mount for: (a) a database's data
directory, (b) the dataset you're actively exploring in notebooks,
(c) the config file you edit per deployment. Choose and defend each.

**Q17.** Two containers, `api` and `db`, on a user-defined network.
What resolves the name `db` from inside `api`, and why would this fail
on the *default* bridge network?

**Q18.** Inside a container, `--ip=0.0.0.0` for a web service can be
safe in this course's labs. State the two boundaries that make it safe,
and the exact flag text that enforces the host-side one.

## Section D — compose, security, synthesis (Q19–22)

**Q19.** `depends_on` alone fails on cold start ("connection refused").
Which two compose keys fix it, and what does each contribute?

**Q20.** List four places a secret baked via `ENV API_KEY=…` leaks from,
and the taught alternative.

**Q21.** Your compose project ran for a month. Rank what survives
`docker compose down` vs `down -v`: containers, network, named volumes,
bind-mounted host files, images.

**Q22.** A colleague wants to "just run `docker system prune --volumes`
to clean the shared server." Compose the three-sentence refusal that
names what it deletes, the safe alternative, and the one command to run
first.

Check answers: [quiz-answers.md](quiz-answers.md) ·
Practice more: [challenges.md](challenges.md) ·
Symptoms index: [../troubleshooting.md](../troubleshooting.md)
