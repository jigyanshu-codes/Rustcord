<div align="center">

<img src="docs/logo.png" alt="RustCord Logo" width="160" style="border-radius: 24px; box-shadow: 0 8px 32px rgba(0,0,0,0.4);" />

# RustCord

**A blazingly fast, lightweight, native Discord client built in pure Rust.**  
*Powered by [egui](https://github.com/emilk/egui) and [wgpu](https://github.com/gfx-rs/wgpu) &mdash; Zero Electron, Zero Chromium, Zero Web Bloat.*

<br/>

[![Language: Rust](https://img.shields.io/badge/Language-Rust-orange.svg?style=flat-square&logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![GUI: egui / wgpu](https://img.shields.io/badge/GUI-egui%20%2F%20wgpu-8A2BE2.svg?style=flat-square)](https://github.com/emilk/egui)
[![Platforms: Windows | Linux | macOS](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-0078D6.svg?style=flat-square)](docs/platform-support.md)
[![License: MIT / Apache-2.0](https://img.shields.io/badge/License-MIT%20OR%20Apache--2.0-2ea44f.svg?style=flat-square)](LICENSE-MIT)
[![CI: Linux Packages](https://img.shields.io/github/actions/workflow/status/jigyanshu-codes/Rustcord/linux-packages.yml?label=Linux%20CI&logo=github&style=flat-square)](https://github.com/jigyanshu-codes/Rustcord/actions/workflows/linux-packages.yml)

<br/>

<p align="center">
  <a href="#downloads-and-packages"><strong>Downloads</strong></a> &nbsp;&bull;&nbsp;
  <a href="#highlights"><strong>Highlights</strong></a> &nbsp;&bull;&nbsp;
  <a href="#performance-comparison"><strong>Performance</strong></a> &nbsp;&bull;&nbsp;
  <a href="#quick-start"><strong>Quick Start</strong></a> &nbsp;&bull;&nbsp;
  <a href="#screenshots"><strong>Showcase</strong></a>
</p>

</div>

---

> [!WARNING]
> **Disclaimer & Terms Notice:**  
> RustCord is an independent open-source native client for existing Discord accounts. It communicates directly with Discord's public gateway and REST API endpoints. Automating standard user accounts or running third-party clients violates Discord's Terms of Service and carries risk of account termination. Technical interoperability does not imply endorsement by Discord Inc.

---

## Highlights

- **Instant Launch & Low Memory Footprint:** Starts in milliseconds, consuming **50&ndash;80 MB RAM** at idle compared to official Discord's 600 MB&ndash;1.1 GB.
- **Native WebRTC Voice & Screen Sharing:** Full end-to-end encryption with DAVE protocol, stereo Opus audio encoding/decoding, low-latency audio capture, and desktop screen sharing.
- **Secure OS Credential Storage:** Authentication tokens and session keys are secured in native OS vaults (Windows Credential Manager, Freedesktop Secret Service, Apple Keychain). Zero telemetry, zero analytics tracking.
- **Responsive Custom Interface:** Fast immediate-mode rendering, high-DPI scaling, smooth font rendering, custom accent palettes, and native system titlebars.
- **Deep Desktop Integration:** Native Windows toast notifications with action buttons, Linux FreeDesktop notifications, and background tray minimization.

---

## Downloads and Packages

Official pre-compiled binaries are published on [GitHub Releases (v0.1.0)](https://github.com/jigyanshu-codes/Rustcord/releases/tag/v0.1.0):

### <img src="https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black" height="18" /> Linux (Universal & Distributions)

- **[Direct Download: Universal AppImage (.AppImage)](https://github.com/jigyanshu-codes/Rustcord/releases/download/v0.1.0/rustcord-0.1.0-Linux-X64.AppImage)** &mdash; Works on all Linux distributions (Ubuntu, Fedora, Arch, Debian, Mint).
  ```bash
  chmod +x rustcord-0.1.0-Linux-X64.AppImage
  ./rustcord-0.1.0-Linux-X64.AppImage
  ```
- **[Direct Download: Ubuntu / Debian (.deb)](https://github.com/jigyanshu-codes/Rustcord/releases/tag/v0.1.0)** &mdash; Native deb package for Ubuntu 24.04/26.04, Debian 12+, and Linux Mint:
  ```bash
  sudo dpkg -i rustcord_*_amd64.deb
  sudo apt-get install -f
  ```

### <img src="https://img.shields.io/badge/Windows-0078D6?style=flat-square&logo=windows&logoColor=white" height="18" /> Windows (x86_64)

- **[Direct Download: Windows Portable (.zip)](https://github.com/jigyanshu-codes/Rustcord/releases/download/v0.1.0/rustcord-v0.1.0-windows-x86_64.zip)** &mdash; Extract and run `rustcord.exe` directly.
- **Installer (`Setup.exe`)**: Installs to `%LOCALAPPDATA%\Programs\RustCord`, configures Start Menu shortcuts and native toast notifications.

### <img src="https://img.shields.io/badge/macOS-000000?style=flat-square&logo=apple&logoColor=white" height="18" /> macOS (Apple Silicon / ARM64)

- Standalone `.app` bundle available under [Releases](https://github.com/jigyanshu-codes/Rustcord/releases).

---

## Performance Comparison

| Metric | Official Discord (Electron) | RustCord (Native Rust) |
|---|---|---|
| **RAM at Idle** | ~650 MB &ndash; 1.1 GB | **~55 MB &ndash; 85 MB** (10x lighter) |
| **Startup Time** | ~4.5 &ndash; 8.0 seconds | **< 0.4 seconds** (Instantaneous) |
| **Idle CPU Usage** | 1.5% &ndash; 5.0% | **< 0.1%** |
| **Technology Stack** | Chromium + Node.js + JS | **Pure Rust + egui + wgpu** |
| **Telemetry / Tracking**| Extensive analytical tracking | **Zero telemetry / Private** |

---

## Quick Start

### Prerequisites

- **Rust:** `1.99.1` or newer ([rustup](https://rustup.rs))
- **C/C++ Compiler:** MSVC v143 (Windows) or GCC / Clang (Linux / macOS)
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

## Screenshots

<div align="center">

| Server & Channel Navigation | Voice Channels & Screen Sharing |
|:---:|:---:|
| <img src="docs/screenshots/threads-forums.png" width="450" /> | <img src="docs/screenshots/voice-calls-screenshare.png" width="450" /> |

| User Settings & Customization | File Uploads & Rich Attachments |
|:---:|:---:|
| <img src="docs/screenshots/user-settings.png" width="450" /> | <img src="docs/screenshots/file-uploads.png" width="450" /> |

</div>

---

## Security and Privacy

- **Credential Storage:** Login tokens are stored strictly inside the OS native credential store (Windows Credential Manager, Apple Keychain, or Freedesktop Secret Service). No tokens are saved in plaintext JSON or config files unless the host environment specifically lacks a secure credential service.
- **Zero Telemetry:** RustCord does not track user events, messages, keystrokes, or application statistics.
- **Auditable Wire Traffic:** All network calls adhere strictly to Discord's documented HTTPS REST and WebSocket Gateway specifications.

---

## License

RustCord is licensed under either of:
- **MIT License** ([LICENSE-MIT](LICENSE-MIT))
- **Apache License, Version 2.0** ([LICENSE-APACHE](LICENSE-APACHE))

at your option.
