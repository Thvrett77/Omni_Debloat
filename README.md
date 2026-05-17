# 📱 Omni_Debloat

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-sharp)](http://makeapullrequest.com)
[![Status](https://img.shields.io/badge/Status-In--Development-orange)](https://github.com/)
[![Discord](https://img.shields.io/badge/Discord-Join%20Server-5865F2?style=flat&logo=discord&logoColor=white)](https://discord.gg/AxAvFCyVvK)

**Omni_Debloat** is a powerful, streamlined tool designed to help you strip away unwanted bloatware from your smartphone, reclaiming your privacy, storage, and battery life. 

---

## 🚀 Features

*   **Presets Support:** Choose from curated official presets or experiment with community-driven configurations.
*   **Interactive Mode:** A beginner-friendly, guided wizard that safely walks you through the debloating process.
*   **Advanced Mode (WIP):** A simplified ADB command-line interface for power users who want granular control without typing raw syntax.

---

## 🛠️ Presets

The tool relies on configuration presets to know what to remove:

| Preset Type | Reliability | Description
| :--- | :--- | :--- | 
| **Official Presets** | 🟢 Safe | Tested configurations designed *not* to brick your phone. Available in the repository. |
| **User Presets** | 🟡 Experimental | Community-made presets. Use with caution as they are largely untested and may break features. |

---

## ⚠️ Disclaimer

> [!WARNING]
> **Use this software at your own risk.** 
> While official presets are designed to be safe and won't brick your device, we are **not responsible** for any damages, bootloops, or data loss this software may cause. Always backup your data before proceeding.
> 
> *Note: **Advanced Mode** is currently a Work In Progress (WIP). We do not recommend using it in its current state unless you know exactly what you are doing.*

---


---

## ⚖️ Why Omni_Debloat? (vs. UAD-NG)

While excellent tools like *Universal Android Debloater Next Generation (UAD-NG)* exist, **Omni_Debloat** is built with a different philosophy:

* **Reduced Risk via Presets:** Instead of guessing which individual packages to uninstall, our curated **Official Presets** eliminate the guesswork, drastically reducing the risk of bootloops or stripping critical system functions.
* **Friendly CLI Experience:** No overwhelming walls of text or complex flag configurations. The **Interactive Mode** guides you safely step-by-step, making terminal-based debloating accessible to everyone.

---

## 🗺️ Future Plans

We are constantly working to make Omni_Debloat better. Here is what is planned for future releases:

| 📋 To Do | ⏳ In Progress | ✅ Done |
| :--- | :--- | :--- |
| 🔹 Rommify Mode (check below) | 🔸 Fixing Bugs | 🔹 Core ADB integration |
| 🔹 Fixing Advanced Mode | 🔸 Cleaning Code | 🔹 Official Presets engine |
| 🔹 App Alternatives Installer | 🔸 Experimental Alternatives Installer | 🔹 Basic CLI Framework |
| 🔹 Lua Extension Support | | 🔹 Discord Server Launch |


### Rommify Mode
Transform your stock firmware into a privacy-respecting, lightweight custom ROM experience without unlocking your bootloader. 

Instead of just removing junk, **Rommify Mode** swaps out your OEM's stock ecosystem for an open-source one by debloating system packages, adjusting system settings for better privacy, and installing clean user-space apps.

* **Custom ROM Ecosystem:** The tool attempts to install official open-source application packages from **LineageOS** and other popular custom ROMs. 
* **FOSS Suite Fallbacks:** If certain LineageOS apps aren't compatible with your device's specific stock software layer, the tool intelligently falls back to installing the privacy-hardened **Fossify Suite**.

The result is a stock ROM that behaves like a clean AOSP build, respects your privacy, and completely replaces heavy OEM system apps.



## 📦 Getting Started

### Prerequisites
*   Android Device with **USB Debugging** enabled.
*   A USB cable to connect your phone to your PC.

### Building From Scratch

1. Clone the repository:
   
   ```git clone https://github.com/Thvrett77/Omni_Debloat```

