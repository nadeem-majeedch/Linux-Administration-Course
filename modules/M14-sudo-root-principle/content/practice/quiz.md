# Module 14 Quiz — 18 Questions

Answer in `lab-log.md`; key: [quiz-answers.md](quiz-answers.md).

1. **R** What single property of an account makes it root, technically?
2. **U** Why does Ubuntu ship with root's password locked instead of just
   choosing a strong default?
3. **R** What does the `!` in root's `/etc/shadow` hash field mean?
4. **U** `su -` vs `sudo -i`: same destination, different trust model.
   Explain the difference in terms of *whose password* and *what's logged*.
5. **P** Decode `%wheel ALL=(ALL:ALL) ALL` field by field. (Yes, `wheel` —
   some distros use it; know it on sight.)
6. **R** What does `%` mean at the start of a sudoers who-field?
7. **U** Why does sudo log *both* to journald and (indirectly) auth.log,
   and why does that matter on a shared server?
8. **P** Your `sudo -l` shows `(ALL : ALL) ALL`. What, precisely, may you
   run as whom?
9. **R** Command to check the *whole* sudoers policy for syntax errors
   without editing anything?
10. **U** Why must a sudoers drop-in filename avoid `.` and `~`, and what
    useful behavior does that rule give you for free?
11. **P** Write a drop-in: members of `sync` may run
    `/usr/local/bin/mirror-datasets` as root with no password. Then state
    the one risk NOPASSWD introduces and the control that compensates.
12. **U** Explain why `sudo echo "x" > /etc/hosts` fails, in terms of what
    the shell does first. Give both standard remedies.
13. **R** What does `Defaults secure_path` protect against? Describe the
    attack concretely.
14. **U** Why is `env_reset` a blessing for security and an occasional
    curse for a `pip install` behind a proxy? Name the sudo flag that
    passes selected variables deliberately.
15. **P** A teammate's drop-in: `dsstudent ALL=(ALL) NOPASSWD: /usr/bin/apt`.
    Is this safe? Enumerate the specific abuse (hint: `apt` can run
    pre-configure scripts as root — so what else can it effectively run?)
16. **DS** Your Jupyter-on-GPU-server pipeline needs to read a root-owned
    700 file nightly. Design the grant two ways: (a) make it work, (b) make
    it least-privilege. Prefer (b) and say why in one sentence.
17. **DS** Why do we say "a data pipeline that needs root is usually a
    permissions smell"? What M13 tool usually dissolves the need?
18. **R** Where does `sudo` record your commands on Ubuntu, and what
    one-liner shows your recent entries?
