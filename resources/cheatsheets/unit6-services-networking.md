# Cheatsheet — Unit 6: Services, Network, SSH, Logs, Firewall

## systemctl (M20)

```bash
systemctl status ssh               # is it running? since when?
sudo systemctl start|stop|restart ssh
sudo systemctl enable ssh          # start at boot (enable != start!)
systemctl --failed                 # what died?
systemctl cat ssh                  # read the unit file
systemctl --user daemon-reload     # after editing YOUR user units
journalctl -u ssh -b               # unit logs since boot
```

## Network (M21)

```bash
ip -brief addr; ip route           # addresses, gateways
ping -c3 8.8.8.8                   # L3 reachability (then DNS:)
dig example.com +short; resolvectl status
ss -tulpn                          # listening ports (-p names need sudo)
curl -I http://localhost:8080/health   # HTTP check
```

Diagnose in layers: link -> IP -> DNS -> port -> application.

## SSH (M22)

```bash
ssh-keygen -t ed25519              # modern key pair (passphrase it!)
ssh-copy-id dslab                  # deploy your public key
ssh dslab                          # alias from ~/.ssh/config:
```

```
Host dslab
  HostName 192.168.56.10
  User dsstudent
  IdentityFile ~/.ssh/id_ed25519
  LocalForward 8888 localhost:8888
```

```bash
ssh dslab 'uptime'                 # remote one-liner
tmux new -s work / tmux a -t work  # sessions survive disconnects
ssh -L 8888:localhost:8888 dslab   # reach VM's Jupyter on your localhost
```

## Transfer (M23)

```bash
rsync -avn src/ dst/               # DRY RUN first — always
rsync -av --exclude='*.tmp' src/ dslab:~/data/
rsync -avP big.iso dslab:~/        # resumable (-P = --partial --progress)
scp file dslab:~/                  # quick single file (-P port, -r dirs)
sha256sum f;  # compare after transfer
```

## Logs & monitoring (M24)

```bash
journalctl -u myapp -f             # follow a unit's logs live
journalctl --since "1 hour ago" -p err
journalctl --disk-usage            # how much space logs take
tail -f /var/log/syslog            # classic text logs (grep them!)
iostat -x 2 5; vmstat 2 5          # disk I/O; memory/cpu (sysstat)
tar -czf backup.tgz ~/projects     # archive;  -tzf to list; -xzf to extract
```

Backups: 3 copies, 2 media, 1 offsite — and a **restore you have tested**.

## Firewall (M25)

```bash
sudo ufw status verbose
sudo ufw default deny incoming
sudo ufw allow OpenSSH             # BEFORE enabling, if remote!
sudo ufw allow 80,443/tcp
sudo ufw enable
sudo sshd -t                       # test sshd config before restart
```
