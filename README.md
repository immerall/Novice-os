# NOVICE OS v3.0 — Offline Cyberdeck CLI

A modular, offline Python command-line assistant and cyberdeck utility suite featuring text-to-speech feedback, AES-encrypted password storage, local network reconnaissance, image steganography, and system telemetry.

## Features
- **System & UI:** Live CPU/RAM/disk/battery telemetry (`stats`), process manager (`ps`, `kill`), workflow macros (`macro`), workstation lock (`lock`), and switchable terminal themes (`cyber`, `matrix`, `stealth`).
- **Voice & Audio:** Offline text-to-speech (`pyttsx3`), hands-free voice commands (`voice`, `handsfree`), and audio alerts.
- **Security & PIN Vault:** AES-encrypted local credential vault (`savepass`, `getpass`, `delpass`), strong password & hex key generator (`genpass`), LSB image steganography (`hide`, `reveal`), SHA-256 file hashing (`hash`), and idle auto-lock (`autolock`).
- **Networking & Reconnaissance:** Multi-threaded subnet scanner with MAC vendor lookup, NetBIOS hostname resolution, ping latency, and open-port fingerprinting (`lanscan`), Wi-Fi telemetry (`netscan`), saved Wi-Fi key viewer (`wifipass`), USB/port monitors, and ping utility.
- **Productivity & Tools:** Background spoken countdown timers (`timer`), clipboard history (`clips`), terminal ASCII QR code generator (`qr`), audible Morse & binary encoder (`morse`), math evaluator (`calc`), instant file/app launcher (`search`, `open`, `findapp`), and timestamped notes (`note`).

## Cyberdeck & OS Compatibility Notice

While **Novice OS v3.0** supports **Windows, Linux, and Raspberry Pi OS** cyberdecks, hardware and OS behavior varies across builds:

- **Cross-Platform Subsystems:** Core utilities (`stats`, `ps`, `kill`, `savepass`, `getpass`, `hide`, `reveal`, `qr`, `timer`, `note`, `lanscan`, `netscan`, `wifipass`, `usb`, `lock`, and `morse`) work across **Windows, Linux, and Raspberry Pi OS**.
- **Linux / Raspberry Pi Requirements:**
  - Text-to-speech (`pyttsx3`) requires `espeak` (`sudo apt install espeak`).
  - Wi-Fi management (`netscan`, `wifipass`) uses NetworkManager (`nmcli`), and `wifipass` may require `sudo` privileges on Linux.
  - USB listing (`usb`) uses `lsusb` (`sudo apt install usbutils`).
  - Audio chimes (`morse`, `testalert`) fall back to the terminal bell (`\a`) when Windows `winsound` is unavailable.
- **Voice Input:** `voice` and `handsfree` require a connected microphone, `pyaudio`, and an internet connection for speech recognition.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch Novice OS:**
   ```bash
   python novice.py
   ```





   <img width="1108" height="579" alt="image" src="https://github.com/user-attachments/assets/28cc7de7-8796-42ef-b606-157417de6a8c" />

Novice starting page
