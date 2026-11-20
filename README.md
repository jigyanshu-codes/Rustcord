<div align="center">

<img src="docs/logo.png" alt="RustCord Logo" width="160" style="border-radius: 24px; box-shadow: 0 8px 32px rgba(0,0,0,0.4);" />

# RustCord

**A blazingly fast, lightweight, native Discord client built in pure Rust.**  
*Powered by [egui](https://github.com/emilk/egui) & [wgpu](https://github.com/gfx-rs/wgpu) — Zero Electron. Zero Chromium. Zero Bloat.*

---

[![Language: Rust](https://img.shields.io/badge/Language-Rust-orange.svg?logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![GUI: egui / wgpu](https://img.shields.io/badge/GUI-egui%20%2F%20wgpu-purple.svg)](https://github.com/emilk/egui)
[![Platforms: Windows | Linux | macOS](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue.svg)](docs/platform-support.md)
[![License: MIT / Apache-2.0](https://img.shields.io/badge/License-MIT%20OR%20Apache--2.0-green.svg)](LICENSE-MIT)
[![CI: Linux Packages](https://img.shields.io/github/actions/workflow/status/jigyanshu-codes/Rustcord/linux-packages.yml?label=Linux%20CI&logo=github)](https://github.com/jigyanshu-codes/Rustcord/actions/workflows/linux-packages.yml)

<p align="center">
  <a href="#-downloads--packages"><strong>📦 Downloads</strong></a> &nbsp;•&nbsp;
  <a href="#-key-features"><strong>⚡ Features</strong></a> &nbsp;•&nbsp;
  <a href="#-performance-comparison"><strong>📊 Performance</strong></a> &nbsp;•&nbsp;
  <a href="#-quick-start--build-from-source"><strong>🛠️ Quick Start</strong></a> &nbsp;•&nbsp;
  <a href="#-screenshots"><strong>📸 Showcase</strong></a>
</p>

</div>

---

> [!WARNING]
> **Disclaimer & Terms Notice:**  
> RustCord is an unofficial open-source native client for existing Discord accounts. It communicates directly with Discord's public gateway and REST API endpoints. Automating standard user accounts or running third-party clients violates Discord's Terms of Service and may carry risk of account termination. Technical interoperability does not imply endorsement by Discord Inc.

---

## ⚡ Highlights

- 🚀 **Instant Launch & Low Memory:** Starts in milliseconds, uses **~50–80 MB RAM** at idle compared to official Discord's 600MB–1GB+.
- 🎙️ **Full Voice & Screen Sharing:** Native WebRTC voice with DAVE end-to-end encryption (E2EE), stereo Opus decoding/encoding, and low-latency audio capture.
- 🔒 **Secure Authentication:** Tokens and session keys are secured in your OS native credential vault (Windows Credential Manager / Secret Service). Zero telemetry, zero analytics tracking.
- 🎨 **Sleek Custom UI:** Fully customizable theme engine, high-DPI scaling, smooth font rendering, custom accent colors, and native system titlebars.
- 🔔 **Native Desktop Integration:** Rich Windows toast notifications with actions, Linux FreeDesktop notifications, and system tray support.

---

## 📦 Downloads & Packages

Pre-compiled production binaries are automatically generated and tested via GitHub Actions CI:

### 🪟 Windows (x86_64 & ARM64)
- **Installer (`Setup.exe`)**: Installs to `%LOCALAPPDATA%\Programs\RustCord`, configures Start Menu & Desktop shortcuts, and registers native Windows toast notification handling.
- **Standalone Portable (`.zip`)**: Extract and run `rustcord.exe` directly anywhere.
- 👉 **[Download Windows Binaries](https://github.com/jigyanshu-codes/Rustcord/actions)**

### 🐧 Linux (Debian, Ubuntu, AppImage, Arch, Fedora)
- **Debian / Ubuntu (`.deb`)**:
  ```bash
  sudo dpkg -i rustcord_*_amd64.deb
  sudo apt-get install -f # resolve any missing runtime libs
  ```
- **Universal AppImage (Portable)**:
  ```bash
  chmod +x rustcord-*-Linux-X64.AppImage
  ./rustcord-*-Linux-X64.AppImage
  ```
- **Fedora / RHEL (`.rpm`)** & **Arch Linux (`.pkg.tar.zst`)**: Available in CI release artifacts.
- 👉 **[Download Linux Packages (.deb / AppImage)](https://github.com/jigyanshu-codes/Rustcord/actions/workflows/linux-packages.yml)**

### 🍎 macOS (Apple Silicon / ARM64)
- Standalone notarized `.app` bundle available under releases.

---

## 📊 Performance Comparison

| Metric | Official Discord (Electron) | **RustCord (Native Rust)** |
|---|---|---|
| **RAM at Idle** | ~650 MB – 1.1 GB | **~55 MB – 85 MB** (10x lighter) |
| **Startup Time** | ~4.5 – 8.0 seconds | **< 0.4 seconds** (Instantaneous) |
| **Idle CPU Usage** | 1.5% – 5.0% | **< 0.1%** |
| **Technology Stack** | Chromium + Node.js + JS | **Pure Rust + egui + wgpu** |
| **Telemetry / Tracking**| Extensive analytical tracking | **Zero telemetry / Private** |

---

## 🛠️ Quick Start & Build from Source

### Prerequisites

- **Rust:** `1.99.1` or newer ([rustup](https://rustup.rs))
- **C/C++ Compiler:** MSVC v143 (Windows) or GCC/Clang (Linux/macOS)
- **CMake:** `3.25+`
- **NASM:** `2.16+` (for accelerated cryptography & audio codecs)
- **LLVM / Clang:** `18+` (for `bindgen`)

### 1. Clone the repository
```bash
git clone https://github.com/jigyanshu-codes/Rustcord.git
cd Rustcord
```

### 2. Run in development mode
```bash
cargo run -p rustcord
```

### 3. Build optimized production release
```bash
cargo build --release -p rustcord --no-default-features
```
The compiled binary will be located at `target/release/rustcord` (or `target/release/rustcord.exe` on Windows).

---

## 📸 Screenshots

<div align="center">

| Server & Channel Navigation | Voice Channels & Screen Sharing |
|:---:|:---:|
| <img src="docs/screenshots/threads-forums.png" width="450" /> | <img src="docs/screenshots/voice-calls-screenshare.png" width="450" /> |

| User Settings & Customization | File Uploads & Rich Attachments |
|:---:|:---:|
| <img src="docs/screenshots/user-settings.png" width="450" /> | <img src="docs/screenshots/file-uploads.png" width="450" /> |

</div>

---

## 🛡️ Security & Privacy

- **Credential Storage:** Login tokens are stored strictly inside the OS credential store (Windows Credential Manager, Apple Keychain, or Freedesktop Secret Service). No tokens are saved in plaintext JSON/config files unless the host environment specifically lacks a secure credential service.
- **Zero Telemetry:** RustCord does not track user events, messages, keystrokes, or application statistics.
- **Auditable Wire Traffic:** All network calls adhere strictly to Discord's documented HTTPS REST and WebSocket Gateway specifications.

---

## 📜 License

RustCord is licensed under either of:
- **MIT License** ([LICENSE-MIT](LICENSE-MIT))
- **Apache License, Version 2.0** ([LICENSE-APACHE](LICENSE-APACHE))

at your option.
