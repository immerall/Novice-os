import os, sys, time, math, json, base64, ctypes, shutil, socket, secrets, hashlib, zipfile, datetime, threading, subprocess, pyttsx3

try: import psutil
except Exception: psutil = None
try: import qrcode
except Exception: qrcode = None
try: import pyperclip
except Exception: pyperclip = None
try: from PIL import Image
except Exception: Image = None
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except Exception:
    Fernet = None
try: import speech_recognition as sr
except Exception: sr = None

if os.name == "nt":
    import winsound

THEMES = {
    "cyber": {"b": "\033[95m", "a": "\033[96m", "p": "\033[92m", "t": "\033[97m", "d": "\033[90m", "w": "\033[93m", "r": "\033[0m"},
    "matrix": {"b": "\033[92m", "a": "\033[32m", "p": "\033[92m", "t": "\033[92m", "d": "\033[32m", "w": "\033[93m", "r": "\033[0m"},
    "stealth": {"b": "\033[90m", "a": "\033[37m", "p": "\033[37m", "t": "\033[37m", "d": "\033[90m", "w": "\033[37m", "r": "\033[0m"}
}

MORSE = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'.','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.','0':'-----',' ':'/'}

class NoviceOS:
    def __init__(self):
        self.version = "3.0"
        self.theme, self.muted, self.running = "cyber", False, True
        self.last_activity = time.time()
        self.autolock_secs = 0
        self.data_dir = os.path.join(os.path.expanduser("~"), ".novice_os")
        os.makedirs(self.data_dir, exist_ok=True)
        self.notes_file = os.path.join(self.data_dir, "notes.txt")
        self.macros_file = os.path.join(self.data_dir, "macros.json")
        self.vault_file = os.path.join(self.data_dir, "vault.json")
        self.salt_file = os.path.join(self.data_dir, "vault.salt")
        self.timers, self.tid_seq, self.clip_history = {}, 1, []
        self._start_watchers()
        try:
            self.tts = pyttsx3.init()
            self.tts.setProperty("rate", 175)
        except Exception:
            self.tts = None

    def beep(self, freq=800, ms=200):
        if self.muted: return
        if os.name == "nt":
            winsound.Beep(freq, ms)
        else:
            print("\a", end="", flush=True)
            time.sleep(ms / 1000.0)

    def c(self, k): return THEMES[self.theme].get(k, "")
    def speak(self, txt):
        if not self.muted and self.tts:
            try: self.tts.say(txt); self.tts.runAndWait()
            except Exception: pass

    def out(self, msg, voice=False):
        print(f"{self.c('a')}[NOVICE]:{self.c('t')} {msg}{self.c('r')}")
        if voice: self.speak(msg)

    def _start_watchers(self):
        def bg():
            last_c = ""
            while self.running:
                if self.autolock_secs > 0 and (time.time() - self.last_activity) > self.autolock_secs:
                    self.autolock_secs = 0
                    ctypes.windll.user32.LockWorkStation() if os.name == "nt" else os.system("loginctl lock-session 2>/dev/null || xdg-screensaver lock 2>/dev/null")
                if pyperclip:
                    try:
                        curr = pyperclip.paste()
                        if curr and curr != last_c:
                            last_c = curr
                            if curr in self.clip_history: self.clip_history.remove(curr)
                            self.clip_history.insert(0, curr)
                            self.clip_history = self.clip_history[:5]
                    except Exception: pass
                time.sleep(1.5)
        threading.Thread(target=bg, daemon=True).start()

    def banner(self):
        os.system("cls" if os.name == "nt" else "clear")
        b, a, r = self.c("b"), self.c("a"), self.c("r")
        print(f"{b}\n ███╗   ██╗ ██████╗ ██╗   ██╗██╗ ██████╗███████╗\n ████╗  ██║██╔═══██╗██║   ██║██║██╔════╝██╔════╝\n ██╔██╗ ██║██║   ██║██║   ██║██║██║     █████╗  \n ██║╚██╗██║██║   ██║╚██╗ ██╔╝██║██║     ██╔══╝  \n ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║╚██████╗███████╗\n ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝ ╚═════╝╚══════╝\n{a}        [ OFFLINE CYBERDECK OS v{self.version} ]{r}\n")

    def help_menu(self):
        a, t, d, r = self.c("a"), self.c("t"), self.c("d"), self.c("r")
        print(f"""
{a}=== NOVICE OS v{self.version} COMMAND DIRECTORY ==={r}
{a}[ SYSTEM & UI ]{r}
  {t}help{d}                    : Show this command directory{r}
  {t}briefing{d}                : Full system, Wi-Fi, and notes report{r}
  {t}stats / battery{d}         : Live CPU, RAM, disk, and power telemetry{r}
  {t}time / date{d}             : Current local time and date{r}
  {t}theme / matrix / stealth{d}: Switch terminal color theme{r}
  {t}work mode / macro{d}       : Multi-step workflow macros{r}
  {t}ps / kill [app]{d}         : View running apps or force-close one{r}
  {t}backup / purge{d}          : Save zip backup or shred all data{r}
  {t}lock / clear / exit{d}     : Lock Windows, clear screen, or quit{r}

{a}[ VOICE & AUDIO ]{r}
  {t}voice / handsfree{d}       : Single voice command or hands-free mode{r}
  {t}mute / unmute / testalert{d}: Toggle voice or test alert chime{r}

{a}[ SECURITY & PIN VAULT ]{r}
  {t}genpass [length]{d}        : Generate strong password or hex key{r}
  {t}savepass [site] [pass]{d}  : Encrypt & save password behind PIN{r}
  {t}getpass [site]{d}          : Unlock & retrieve saved password{r}
  {t}delpass [site]{d}          : Delete an account from the vault{r}
  {t}hide / reveal [img]{d}     : Hide or extract secret text in images{r}
  {t}hash [path] / autolock{d}  : SHA-256 file hash or idle PC lock{r}

{a}[ WIFI, FILES & TOOLS ]{r}
  {t}netscan / lanscan{d}                 : Local IP, Wi-Fi stats, & nearby scan{r}
  {t}wifipass [network]{d}      : View saved Windows Wi-Fi passwords{r}
  {t}usb / ports{d}             : Connected USB devices or open ports{r}
  {t}clips / clip [1-5]{d}      : View or re-copy clipboard history{r}
  {t}morse [text]{d}            : Audible Morse code & binary encoder{r}
  {t}qr [text]{d}               : Render terminal matrix barcode{r}
  {t}search / open [file]{d}    : Find and launch local files instantly{r}
  {t}findapp [word]{d}          : Search & launch top match instantly{r}
  {t}timer [mins] [label]{d}    : Background timer with spoken alert{r}
  {t}timers / stoptimer{d}      : View or cancel active timers{r}
  {t}calc [math] / ping [ip]{d} : Evaluate math or ping a host{r}
  {t}note [text] / read notes{d}: Save or read timestamped notes{r}
""")
        self.out("Command directory displayed.")
    def cmd_stats(self):
        if not psutil: self.out("Run: pip install psutil"); return
        cpu, ram, disk, bat = psutil.cpu_percent(0.4), psutil.virtual_memory(), psutil.disk_usage(os.path.abspath(os.sep)), psutil.sensors_battery()
        print(f"{self.c('a')}--- SYSTEM TELEMETRY ---{self.c('t')}\n  CPU : {cpu}%\n  RAM : {ram.percent}% ({ram.used//(1024**2)}MB / {ram.total//(1024**2)}MB)\n  Disk: {disk.percent}% ({disk.free//(1024**3)}GB free)")
        print(f"  Bat : {bat.percent}% ({'Charging' if bat.power_plugged else 'Discharging'})" if bat else "  Bat : AC Power / Desktop")
        print(self.c("r"), end="")

    def cmd_ps(self):
        if not psutil: self.out("Run: pip install psutil"); return
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'memory_info']):
            try: procs.append((p.info['memory_info'].rss / (1024*1024), p.info['pid'], p.info['name']))
            except Exception: pass
        procs.sort(reverse=True)
        for mem, pid, name in procs[:15]: print(f"  PID {pid:<6} | {mem:>6.1f} MB | {name}")

    def cmd_kill(self, target):
        if not psutil or not target: self.out("Usage: kill [app_name or PID]"); return
        n = 0
        for p in psutil.process_iter(['pid', 'name']):
            try:
                if str(p.info['pid']) == target or target.lower() in p.info['name'].lower():
                    p.terminate(); n += 1
            except Exception: pass
        self.out(f"Terminated {n} process(es)." if n else f"No process matching '{target}'.")

    def cmd_briefing(self):
        self.out(f"Cyberdeck Briefing for {datetime.datetime.now().strftime('%A, %B %d, %Y | %I:%M %p')}", True)
        self.cmd_stats()
        nc = len([l for l in open(self.notes_file, encoding="utf-8") if l.strip()]) if os.path.exists(self.notes_file) else 0
        print(f"  Notes: {nc} | Active Timers: {len(self.timers)}")

    def cmd_macro(self, args):
        macros = json.load(open(self.macros_file, encoding="utf-8")) if os.path.exists(self.macros_file) else {}
        if not args or args[0].lower() == "list":
            self.out("Macros: " + (", ".join(macros.keys()) if macros else "None (macro save [name] cmd1 ; cmd2)"))
            return
        act = args[0].lower()
        if act == "save" and len(args) >= 3:
            name = args[0].lower()
            macros[name] = [s.strip() for s in " ".join(args[2:]).split(";") if s.strip()]
            json.dump(macros, open(self.macros_file, "w", encoding="utf-8"), indent=2)
            self.out(f"Saved macro '{name}'.")
        elif act in macros:
            for step in macros[act]: self.handle(step)
        else:
            self.out("Usage: macro list | macro save [name] cmd1 ; cmd2 | macro [name]")

    def _fernet(self, pin):
        if not os.path.exists(self.salt_file): open(self.salt_file, "wb").write(os.urandom(16))
        salt = open(self.salt_file, "rb").read()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390000)
        return Fernet(base64.urlsafe_b64encode(kdf.derive(pin.encode())))

    def cmd_savepass(self, args):
        if not Fernet or len(args) < 2: self.out("Usage: savepass [site] [password]"); return
        site, pwd = args[0].lower(), " ".join(args[1:])
        pin = input(f"{self.c('w')}Enter Vault PIN: {self.c('t')}").strip()
        vault = json.load(open(self.vault_file, encoding="utf-8")) if os.path.exists(self.vault_file) else {}
        vault[site] = self._fernet(pin).encrypt(pwd.encode()).decode()
        json.dump(vault, open(self.vault_file, "w", encoding="utf-8"), indent=2)
        self.out(f"Saved encrypted password for '{site}'.")

    def cmd_getpass(self, args):
        if not Fernet or not args or not os.path.exists(self.vault_file): self.out("Usage: getpass [site]"); return
        site = args[0].lower()
        vault = json.load(open(self.vault_file, encoding="utf-8"))
        if site not in vault: self.out(f"Not found. Saved: {', '.join(vault.keys())}"); return
        pin = input(f"{self.c('w')}Enter Vault PIN: {self.c('t')}").strip()
        try:
            dec = self._fernet(pin).decrypt(vault[site].encode()).decode()
            if pyperclip: pyperclip.copy(dec)
            self.out(f"[{site}] Password: {dec}")
        except Exception: self.out("Invalid PIN.")

    def cmd_delpass(self, args):
        if not args or not os.path.exists(self.vault_file): return
        vault = json.load(open(self.vault_file, encoding="utf-8"))
        if vault.pop(args[0].lower(), None):
            json.dump(vault, open(self.vault_file, "w", encoding="utf-8"), indent=2)
            self.out(f"Deleted '{args}'.")

    def cmd_hide(self, args):
        if not Image or len(args) < 2: self.out("Usage: hide [image_path] [secret]"); return
        path = args[0].strip('"')
        if not os.path.exists(path): self.out("Image not found."); return
        img = Image.open(path).convert("RGB")
        bits = "".join(format(ord(ch), "08b") for ch in (" ".join(args[1:]) + "###END###"))
        px = list(img.getdata())
        if len(bits) > len(px) * 3: self.out("Message too long for image."); return
        new_px, idx = [], 0
        for r, g, b in px:
            ch = [r, g, b]
            for i in range(3):
                if idx < len(bits): ch[i] = (ch[i] & ~1) | int(bits[idx]); idx += 1
            new_px.append(tuple(ch))
        out_p = os.path.splitext(path)[0] + "_hidden.png"
        img.putdata(new_px); img.save(out_p, "PNG")
        self.out(f"Secret hidden in: {out_p}")

    def cmd_reveal(self, args):
        if not Image or not args: self.out("Usage: reveal [image_path]"); return
        path = args[0].strip('"')
        if not os.path.exists(path): self.out("Image not found."); return
        bits = "".join(str(r&1)+str(g&1)+str(b&1) for r,g,b in Image.open(path).convert("RGB").getdata())
        chars = []
        for i in range(0, len(bits), 8):
            if len(bits[i:i+8]) < 8: break
            chars.append(chr(int(bits[i:i+8], 2)))
            if "".join(chars[-9:]) == "###END###":
                self.out(f"Secret: {''.join(chars[:-9])}"); return
        self.out("No hidden message found.")
    def cmd_voice(self, loop=False):
        if not sr: self.out("Run: pip install SpeechRecognition pyaudio"); return
        rec = sr.Recognizer()
        with sr.Microphone() as src:
            while True:
                self.out("Listening...", not loop)
                try:
                    txt = rec.recognize_google(rec.listen(src, timeout=5, phrase_time_limit=7))
                    print(f"{self.c('p')}[VOICE] > {self.c('t')}{txt}{self.c('r')}")
                    if txt.lower() in ("stop listening", "exit handsfree"): break
                    self.handle(txt)
                except Exception: self.out("No clear speech detected.")
                if not loop or not self.running: break

    def cmd_search(self, query, launch=False):
        if not query: self.out("Usage: search [name] or open [name]"); return
        roots = [os.path.join(os.path.expanduser("~"), d) for d in ("Desktop", "Documents", "Downloads")]
        hits = []
        for rd in roots:
            if not os.path.exists(rd): continue
            for r, _, fs in os.walk(rd):
                for f in fs:
                    if query.lower() in f.lower():
                        hits.append(os.path.join(r, f))
                        if len(hits) >= 10: break
                if len(hits) >= 10: break
        if not hits: self.out(f"No matches for '{query}'."); return
        if launch:
            self.out(f"Opening {hits[0]}", True)
            if os.name == "nt": os.startfile(hits[0])
        else:
            for h in hits: print(" ", h)

    def cmd_findapp(self, query):
        if not query: self.out("Usage: findapp [app]"); return
        if os.name == "nt":
            dirs = [os.path.join(os.environ.get(k, ""), "Microsoft\\Windows\\Start Menu\\Programs") for k in ("ProgramData", "APPDATA")]
            for d in dirs:
                if not os.path.exists(d): continue
                for r, _, fs in os.walk(d):
                    for f in fs:
                        if query.lower() in f.lower() and f.endswith((".lnk", ".exe")):
                            self.out(f"Launching {f}...", True); os.startfile(os.path.join(r, f)); return
        else:
            path = subprocess.getoutput(f"which {query}").strip()
            if path:
                subprocess.Popen([path]); self.out(f"Launching {query}...", True); return
        try: subprocess.Popen(query, shell=True); self.out(f"Launched '{query}'.")
        except Exception: self.out(f"App '{query}' not found.")
    def cmd_lanscan(self):
        import concurrent.futures, re
        self.out("Running deep LAN reconnaissance scan...", True)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip, _ = s.getsockname()
            s.close()
        except Exception:
            local_ip = socket.gethostbyname(socket.gethostname())
        prefix = ".".join(local_ip.split(".")[:3])

        OUI = {
            "00:50:56": "VMware", "00:0C:29": "VMware", "08:00:27": "VirtualBox",
            "B8:27:EB": "Raspberry Pi", "DC:A6:32": "Raspberry Pi", "E4:5F:01": "Raspberry Pi",
            "3C:22:FB": "Apple", "F0:18:98": "Apple", "A4:83:E7": "Apple", "28:CF:E9": "Apple",
            "00:1A:11": "Google", "F4:F5:D8": "Google", "54:60:09": "Google",
            "FC:A6:67": "Amazon", "44:65:0D": "Amazon", "74:C2:46": "Amazon",
            "00:15:5D": "Microsoft Hyper-V", "28:18:78": "Microsoft",
            "D4:BE:D9": "Dell", "18:03:73": "Dell", "F8:BC:12": "Dell",
            "3C:D9:2B": "HP", "94:57:A5": "HP", "00:1B:63": "Apple",
            "00:1E:67": "Intel", "8C:8D:28": "Intel", "A4:C3:F0": "Intel",
            "00:18:0A": "Cisco Meraki", "00:00:0C": "Cisco", "C0:25:E9": "TP-Link",
            "50:C7:BF": "TP-Link", "B0:BE:76": "TP-Link", "20:4E:7F": "Netgear"
        }

        COMMON_PORTS = {21: "FTP", 22: "SSH", 23: "Telnet", 80: "HTTP", 139: "SMB", 443: "HTTPS", 445: "SMB", 3389: "RDP", 8080: "HTTP-Alt"}

        def probe_host(ip):
            t0 = time.time()
            flag = "-n" if os.name == "nt" else "-c"
            w = "-w" if os.name == "nt" else "-W"
            res = subprocess.run(["ping", flag, "1", w, "300", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res.returncode != 0:
                return None
            ms = int((time.time() - t0) * 1000)

            # Hostname via DNS or Windows NetBIOS
            host = "Unknown"
            try:
                host, _, _ = socket.gethostbyaddr(ip)
            except Exception:
                if os.name == "nt":
                    nb = subprocess.getoutput(f"nbtstat -A {ip}")
                    for line in nb.splitlines():
                        if "<00>" in line and "UNIQUE" in line:
                            host = line.split().pop(0)
                            break

            # Quick open-port fingerprint
            open_svcs = []
            for port, svc in COMMON_PORTS.items():
                ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ps.settimeout(0.15)
                if ps.connect_ex((ip, port)) == 0:
                    open_svcs.append(f"{port}/{svc}")
                ps.close()

            return (ip, ms, host, open_svcs)

        ips = [f"{prefix}.{i}" for i in range(1, 255)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as ex:
            results = [r for r in ex.map(probe_host, ips) if r]

        arp_map = {}
        if os.name == "nt":
            for line in subprocess.getoutput("arp -a").splitlines():
                p_ip, p_mac = (line.split() + ['',''])[:2]
                if p_ip.startswith(prefix + '.'): arp_map[p_ip] = p_mac.upper().replace('-', ':')
                if False: pass
                parts = line.split()
                if len(parts) >= 2 and parts.pop(0).startswith(prefix + "."):
                    pass

        print(f"\n{self.c('a')}=== DETAILED LAN SCAN: {prefix}.0/24 ({len(results)} ACTIVE) ==={self.c('t')}")
        for ip, ms, host, svcs in results:
            mac = arp_map.get(ip, "LOCAL-HOST" if ip == local_ip else "UNKNOWN-MAC")
            vendor = OUI.get(mac[:8], "Self" if ip == local_ip else "Generic / Randomized MAC")
            role = " [GATEWAY]" if ip.endswith(".1") else (" [THIS PC]" if ip == local_ip else "")
            svc_str = ", ".join(svcs) if svcs else "None detected"
            print(f"{self.c('p')}[+] {ip:<15}{role}{self.c('t')} ({ms}ms)")
            print(f"    Host   : {host}")
            print(f"    MAC    : {mac} ({vendor})")
            print(f"    Ports  : {svc_str}")
        print(self.c("r"), end="")
    def handle(self, raw):
        self.last_activity = time.time()
        line = raw.strip()
        if not line: return
        low = line.lower()
        if low == "read notes":
            print(open(self.notes_file, encoding="utf-8").read().strip() if os.path.exists(self.notes_file) else "No notes.")
            return
        if low.startswith("work mode"): self.cmd_macro(["work"]); return

        parts = line.split()
        cmd, args, arg_str = parts[0].lower(), parts[1:], " ".join(parts[1:])

        if cmd == "help": self.help_menu()
        elif cmd == "clear": self.banner()
        elif cmd == "exit": self.out("Shutting down Novice OS.", True); self.running = False
        elif cmd in ("theme", "matrix", "stealth"):
            t = cmd if cmd in ("matrix", "stealth") else (args[0].lower() if args else "cyber")
            if t in THEMES: self.theme = t; self.banner(); self.out(f"Theme: {t.upper()}")
        elif cmd in ("time", "date"): self.out(datetime.datetime.now().strftime("%A, %B %d, %Y | %I:%M:%S %p"))
        elif cmd in ("stats", "battery"): self.cmd_stats()
        elif cmd == "ps": self.cmd_ps()
        elif cmd == "kill": self.cmd_kill(arg_str)
        elif cmd == "briefing": self.cmd_briefing()
        elif cmd == "macro": self.cmd_macro(args)
        elif cmd == "purge":
            if input("Type YES to shred all Novice data: ").strip() == "YES":
                shutil.rmtree(self.data_dir, ignore_errors=True); os.makedirs(self.data_dir, exist_ok=True)
                self.out("All local data purged.", True)
        elif cmd == "mute": self.muted = True; self.out("Voice muted.")
        elif cmd == "unmute": self.muted = False; self.out("Voice online.", True)
        elif cmd == "testalert":
            self.beep(900, 300)
            self.out("Alert chime triggered.", True)
        elif cmd == "voice": self.cmd_voice(False)
        elif cmd == "handsfree": self.cmd_voice(True)
        elif cmd == "genpass":
            n = int(args[0]) if args and args[0].isdigit() else 16
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*_-+="
            pwd = "".join(secrets.choice(chars) for _ in range(max(8, min(64, n))))
            if pyperclip: pyperclip.copy(pwd)
            self.out(f"Password: {pwd} | Hex: {secrets.token_hex(max(4, n//2))}")
        elif cmd == "savepass": self.cmd_savepass(args)
        elif cmd == "getpass": self.cmd_getpass(args)
        elif cmd == "delpass": self.cmd_delpass(args)
        elif cmd == "hide": self.cmd_hide(args)
        elif cmd == "reveal": self.cmd_reveal(args)
        elif cmd == "hash" and os.path.exists(arg_str.strip('"')):
            self.out("SHA-256: " + hashlib.sha256(open(arg_str.strip('"'), "rb").read()).hexdigest())
        elif cmd == "autolock" and args and args[0].isdigit():
            self.autolock_secs = int(args[0]) * 60; self.out(f"Autolock set to {args}m.")
        elif cmd == "lanscan": self.cmd_lanscan()
        elif cmd == "netscan":
            h = socket.gethostname()
            self.out(f"Host: {h} | IP: {socket.gethostbyname(h)}")
            if os.name == "nt":
                for l in subprocess.getoutput("netsh wlan show interfaces").splitlines():
                    if any(k in l for k in ("SSID", "Signal", "State")): print(" ", l.strip())
        elif cmd == "wifipass" and os.name == "nt":
            if not arg_str:
                out = subprocess.getoutput("netsh wlan show profiles")
                self.out("Profiles: " + ", ".join(l.split(":")[1].strip() for l in out.splitlines() if "All User Profile" in l and ":" in l))
            else:
                out = subprocess.getoutput(f'netsh wlan show profile name="{arg_str}" key=clear')
                keys = [l.split(":")[1].strip() for l in out.splitlines() if "Key Content" in l and ":" in l]
                self.out(f"Password: {keys}" if keys else "No password found.")
        elif cmd == "usb" and os.name == "nt":
            print(subprocess.getoutput('powershell "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match \'^USB\' } | Select-Object -ExpandProperty FriendlyName"'))
        elif cmd == "ports" and psutil:
            for c in psutil.net_connections(kind="inet"):
                if c.status == "LISTEN": print(f"  {c.laddr.ip}:{c.laddr.port} (PID {c.pid})")
        elif cmd == "clips":
            for i, item in enumerate(self.clip_history, 1): print(f"  [{i}] {item.replace(chr(10), ' ')[:60]}")
            if not self.clip_history: self.out("Clipboard history empty.")
        elif cmd == "clip" and pyperclip and args and args[0].isdigit() and 1 <= int(args[0]) <= len(self.clip_history):
            pyperclip.copy(self.clip_history[int(args[0])-1]); self.out(f"Copied clip #{args}.")
        elif cmd == "qr" and qrcode and arg_str:
            q = qrcode.QRCode(border=1); q.add_data(arg_str); q.make(fit=True); q.print_ascii(invert=True)
        elif cmd == "search": self.cmd_search(arg_str, False)
        elif cmd == "open": self.cmd_search(arg_str, True)
        elif cmd == "findapp": self.cmd_findapp(arg_str)
        elif cmd == "ping" and arg_str: print(subprocess.getoutput(f"ping {'-n' if os.name=='nt' else '-c'} 2 {arg_str}"))
        elif cmd == "morse" and arg_str:
            m = " ".join(MORSE.get(ch.upper(), "?") for ch in arg_str)
            print(f"Morse : {m}\nBinary: {' '.join(format(ord(ch), '08b') for ch in arg_str)}")
            if not self.muted:
                for s in m:
                    if s == ".": self.beep(800, 100)
                    elif s == "-": self.beep(800, 280)
                    elif s == " ": time.sleep(0.15)
        elif cmd == "timer" and args:
            mins, lbl, tid = float(args[0]), " ".join(args[1:]) or f"Timer #{self.tid_seq}", self.tid_seq
            self.tid_seq += 1; end = time.time() + mins * 60; flag = threading.Event()
            self.timers[tid] = (lbl, end, flag)
            def run_t():
                while time.time() < end and not flag.is_set(): time.sleep(0.5)
                if not flag.is_set():
                    self.timers.pop(tid, None); print(f"\n[ALARM]: {lbl} finished!")
                    self.beep(1000, 600)
                    self.speak(f"Timer {lbl} finished.")
            threading.Thread(target=run_t, daemon=True).start()
            self.out(f"Started '{lbl}' ({mins}m) [ID: {tid}].")
        elif cmd == "timers":
            for tid, (lbl, end, _) in self.timers.items():
                rem = max(0, int(end - time.time())); print(f"  [{tid}] {lbl} ({rem//60}m {rem%60}s left)")
            if not self.timers: self.out("No active timers.")
        elif cmd == "stoptimer" and args and args[0].isdigit() and int(args[0]) in self.timers:
            self.timers.pop(int(args[0])).set(); self.out(f"Cancelled timer #{args}.")
        elif cmd == "calc":
            safe = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
            try: self.out(f"Result: {eval(arg_str, {'__builtins__': None}, safe)}")
            except Exception as e: self.out(f"Error: {e}")
        elif cmd == "note" and arg_str:
            with open(self.notes_file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] {arg_str}\n")
            self.out("Note saved.")
        elif cmd == "backup":
            zp = os.path.join(os.path.expanduser("~"), "Desktop", "novice_backup.zip")
            with zipfile.ZipFile(zp, "w") as zf:
                for fn in os.listdir(self.data_dir): zf.write(os.path.join(self.data_dir, fn), fn)
            self.out(f"Backup saved to {zp}", True)
        elif cmd == "lock" and os.name == "nt": ctypes.windll.user32.LockWorkStation()
        else: self.out(f"Unknown command '{cmd}'. Type 'help'.")

    def run(self):
        if os.name == "nt": os.system("")
        self.banner()
        self.out("Novice OS version 3.0 initialized. All cyberdeck subsystems online.", True)
        while self.running:
            try:
                inp = input(f"\n{self.c('p')}[YOU] > {self.c('t')}")
                print(self.c("r"), end="")
                self.handle(inp)
            except (KeyboardInterrupt, EOFError): break

if __name__ == "__main__":
    NoviceOS().run()











