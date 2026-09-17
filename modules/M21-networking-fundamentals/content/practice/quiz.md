# Module 21 Quiz — Networking Fundamentals

> 22 questions. Closed-book where possible; the point is reflexes, not
> lookup speed. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Scope: lessons 1–5. Safety rules count as quiz material too.

## Section A — Fundamentals (Q1–6)

**Q1.** A host has MAC address `52:54:00:aa:bb:cc` and IP `192.168.1.7/24`.
Which address changes when the laptop moves to a different Wi-Fi network,
and which usually does not? Why?

**Q2.** `/24` is CIDR shorthand. Write the equivalent dotted-decimal subnet
mask, and state how many usable host addresses a `/24` network provides.

**Q3.** Which interface name is the IPv4 loopback, and which address range
does loopback occupy? Is `127.0.0.2` a valid loopback address?

**Q4.** A packet leaves your host for a server on a *different* subnet.
What device does it go to first, and how did your host learn that
device's address?

**Q5.** Put these in the order a packet meets them, from your application
downward: **router, NIC (MAC frame), TCP socket, IP header.**

**Q6.** Give one practical difference between TCP and UDP, and one
workload from this course that uses each (think: SSH vs the Jupyter
server's WebSocket streams vs DNS lookups).

## Section B — The `ip` toolkit (Q7–11)

**Q7.** Which single command shows interfaces **with** their IPv4
addresses and the link state? Show the invocation you'd actually type.

**Q8.** What does the `state DOWN` on an interface rule out immediately —
even before you look at addresses or routes?

**Q9.** `ip route` prints exactly one line starting `default via
10.0.2.2`. What is `10.0.2.2` on this host, in one sentence?

**Q10.** In a VM with NAT networking, your guest shows `10.0.2.15/24`.
Why can't a machine on your physical LAN ping it directly?

**Q11.** Which command and which *file* would you use, respectively, to
view the current ARP/neighbour table and the hostname-to-address
overrides checked before DNS?

## Section C — DNS (Q12–16)

**Q12.** Write the nsswitch resolution order used for `getent hosts
example.com`, and name the file that configures it.

**Q13.** `dig example.com` returns an answer from `127.0.0.53`. What is
that address, and why does it usually make `dig` answers *fast*?

**Q14.** Name the record type that maps a name to an IPv4 address, the
one for IPv6, and the one that maps `www` → the domain's main name.

**Q15.** Your `dig +short api.internal.corp` fails but `dig +short
api.internal.corp @10.8.0.1` works, where `10.8.0.1` is your VPN's DNS.
What does that prove, and name one systemd-resolved feature that fixes it.

**Q16.** `nslookup` still works on Ubuntu. Give the two reasons the
course prefers `dig`/`resolvectl` over it.

## Section D — Ports & sockets (Q17–22)

**Q17.** The ephemeral port range on modern Linux defaults to
32768–60999. Why should a Jupyter server *not* be configured on port
45000 without thinking?

**Q18.** Write the `ss` invocation that shows only TCP **listening**
sockets with the owning process name, and state what needs to be true
to see process names for sockets owned by other users.

**Q19.** `LISTEN`, `ESTAB`, `TIME-WAIT`: match each to its one-line
meaning, and say which one you'll see lots of, *correctly*, on a busy
client machine (i.e., it is not an error).

**Q20.** `curl http://127.0.0.1:8000` gives **connection refused**;
`curl http://10.0.2.15:8000` times out from another VM. Give the most
likely cause of each, and the single command that confirms the first.

**Q21.** State the exact scope of the `tcpdump` captures allowed in this
course and the one flag that keeps you from drowning in output while
learning.

**Q22.** A teammate says "the network is down" because `ping 8.8.8.8`
fails from a server. Name two other rungs of the six-rung ladder you
would test before agreeing, with one command for each.
