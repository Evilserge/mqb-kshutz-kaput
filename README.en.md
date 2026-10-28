<div align="center">

# Schutz-Kaput • VAG ECU CP & SWaP Patcher
### Modular Offline Component Protection (`KS_PASSIVE`) & `FeC` / `SWaP` Unlocking Toolkit

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B%20(stdlib%20only)-3776AB?style=for-the-badge&logo=python&logoColor=white)](#quick-start)
[![Not For Sale](https://img.shields.io/badge/License-FREE%20%E2%80%A2%20NOT%20FOR%20SALE-D9381E?style=for-the-badge)](LICENSE.md)

[![Website](https://img.shields.io/badge/Web-vwhacking.antonperk.com-181717?style=flat-square&logo=googlechrome&logoColor=00D8FF)](https://vwhacking.antonperk.com)
[![Drive2](https://img.shields.io/badge/Drive2-PerkTheFox-E31E24?style=flat-square&logo=rss&logoColor=white)](https://www.drive2.ru/users/perkthefox/)
[![Telegram](https://img.shields.io/badge/Telegram-%40perkthefox-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/perkthefox)

**Made by PerkTheFox** • **Zero Dependencies (Pure Python 3)** • **[🇷🇺 Читать на русском (`README.md`)](README.md) | 🇬🇧 English**

</div>

---

## Disclaimer & Responsibility

> [!CAUTION]
> **USE AT YOUR OWN RISK (`AS IS`):**  
> - **Everything that happens to the control unit afterwards is 100% YOUR responsibility.**  
> - This script only prepares files locally — it has **NO** connection to the ECU and does **NOT** control the flashing process.  
> - Always save a complete, unmodified backup of your original Flash and `EEPROM` / `NvM` before performing any modifications.  
> - **Bricked units CANNOT be recovered over OBD — recovery is impossible without a hardware bench programmer!**

> [!WARNING]
> **FREE COMMUNITY TOOL — STRICTLY NOT FOR SALE:**  
> Built for non-commercial community research and personal VAG retrofits. Selling this tool, bundling it into paid packages, or commercially selling dumps/containers generated with it is strictly prohibited. Full legal terms are set out in **[`LICENSE.md`](LICENSE.md)**. Please preserve author attribution when sharing or redistributing: **[vwhacking.antonperk.com](https://vwhacking.antonperk.com)** • **[Drive2](https://www.drive2.ru/users/perkthefox/)** • **[Telegram](https://t.me/perkthefox)**.

### Legal Framework & Right-to-Repair Notice (TL;DR)

* **Exactly `0` Bytes of OEM Firmware Inside:** This repository contains zero bytes of Volkswagen AG, Valeo, Renesas, or Mobileye proprietary code — only original Python source code and byte-sequence transformation logic operating on files locally owned by the user. Claiming firmware copyright infringement against this repository makes about as much sense as suing a hex editor or a soldering iron.
* **Your Hardware, Your Rules (*Right to Repair*):** When you buy a replacement camera and windshield with your own money, yet a remote server insists your own hardware isn't allowed to open its eyes without a paid online permission slip, statutory interoperability and Right-to-Repair exemptions apply: **EU Directive 2009/24/EC (Arts. 5–6)**, **17 U.S.C. § 1201(f) & 37 C.F.R. § 201.40(b) (DMCA Land Motor Vehicle Repair & Modification Exemption)**, and **Art. 1280 of the Civil Code of the RF**.
* **Zero Tolerance for Stolen Parts:** Built strictly for honest owners and security researchers dealing with unavailable dealer online servers during legitimate repairs or retrofits. Any use on stolen vehicles or parts of unlawful origin is strictly prohibited and automatically voids the license *ab initio*.
* **A Camera Is Not Autopilot, and a Script Is Not Insurance:** Modifying `ADAS` firmware voids manufacturer warranties, may affect public-road homologation (`ECE` / `StVZO` / `DOT`), and requires proper optical calibration (`VAS 6430`). Unless explicitly permitted by local vehicle inspection laws, modified ECUs are intended for bench research, emulation, and closed-course testing — and the human driver remains 100% responsible behind the wheel.
* **Independent Research:** Not affiliated with or endorsed by VAG or its suppliers; all part numbers and protocol acronyms (`ODIS`, `SWaP`, `FeC`, `GEKO`) are referenced strictly under *nominative fair use* to describe compatibility. Read the full binding license in **[`LICENSE.md`](LICENSE.md)**.

---

## Overview

**`Schutz-Kaput`** (`ks_patcher.py`) is a zero-dependency **Python 3** toolkit featuring both a full-screen **`ncurses`-style interactive TUI** and a scriptable **CLI** for preparing VAG ECU firmware:

- switches Component Protection into passive mode (**`KS_PASSIVE`**) while protecting `NvM` against counter wear on retrofitted vehicles;
- unlocks all built-in **`FeC` / `SWaP`** functions offline with clean factory `0xFF` diagnostic state reporting in `ODIS`;
- natively unpacks and rebuilds dealer **`.frf` / `.odx-f` / `.odx`** containers (with built-in `frf.key` decryption);
- supports **100% bit-exact rollback (`--restore-stock`)** back to original factory bytes.

---

## Supported ECU Modules

Detailed patch descriptions, `FeC` / `SWaP` tables, pinouts, and step-by-step flashing instructions live inside each target module's folder:

| Address | Target (`-t`) | ECU Module & SW | Platform / MCU | Input Formats | Capabilities | Documentation |
| :---: | :---: | :--- | :--- | :--- | :--- | :---: |
| `0x00A5` | `mfk3` | **Valeo MFK3** (`2Q0 980 653`, SW `13xx` / `14xx`) — front ADAS camera | `Renesas RH850/P1H-C` | `.frf`, `.odx-f`, `.odx`, `.pdx`, `.bin` | `KS_PASSIVE`, all `9 FeC/SWaP` (`0xFF`), `KeyDTC`, `XCP CAN0`, `ODIS-E ODX` | **[🇬🇧 EN](targets/mfk3/README.en.md)** · **[🇷🇺 RU](targets/mfk3/README.md)** |

---

## Quick Start

Requires only standard **Python `3.9+`** (macOS / Linux / Windows) with zero external packages.

### Interactive TUI Mode (Recommended)

```bash
python3 ks_patcher.py
```

TUI shortcuts:
- `↑` / `↓`, `Enter`, `Space` — navigate menus and toggle checkboxes;
- `L` — switch interface language (`Русский` ⇄ `English`);
- `D` — show / hide technical details (addresses, `CRC-32`, `SHA-256`, patch bytes);
- `A` — author credits & terms of use.

### Core Command-Line (CLI) Commands

```bash
# 1. Print table of all supported ECU target modules
python3 ks_patcher.py -l en --list-targets

# 2. Inspect a factory container (.frf / .odx-f) or bench dump (.bin)
python3 ks_patcher.py -l en -t <target> inspect <firmware.frf|dump.bin>

# 3. Patch firmware and build ODIS-E packages (when supported by target)
python3 ks_patcher.py -l en -t <target> patch <firmware.frf> --build-odx ./ODIS_READY

# 4. Patch a raw bench dump (.bin)
python3 ks_patcher.py -l en -t <target> patch <dump.bin> -o <patched.bin>

# 5. Losslessly restore a patched dump back to 100% factory stock
python3 ks_patcher.py -l en -t <target> patch <patched.bin> --restore-stock -o <restored.bin>

# 6. Unpack a factory .frf or .odx-f container into raw datablocks
python3 ks_patcher.py -l en -t <target> unpack <firmware.frf> -o ./unpacked --skip-large

# 7. Run built-in self-tests across all target modules
python3 ks_patcher.py -l en selftest
```

*(Target-specific examples and flashing instructions are documented in each target's own `README` linked in the table above.)*

---

## Project Architecture

Each supported ECU is isolated inside its own self-contained plugin folder under `targets/<module>/` alongside its own documentation:

```text
.
├── ks_patcher.py          # Entry point (interactive TUI + CLI)
├── LICENSE.md             # Non-commercial Right-to-Repair license & liability disclaimer (EN / RU)
├── core/
│   ├── i18n.py            # RU/EN localization, ANSI styling, safety warnings
│   ├── pattern.py         # Masked byte-pattern scanner & alignment checks
│   ├── containers.py      # FRF, ODX, PDX parser/builder & LZSS A0 codec
│   └── target_base.py     # Abstract ECU target plugin interface (EcuTargetPlugin)
├── tui/
│   ├── screen.py          # Terminal engine (?1049h, raw input, SIGWINCH)
│   ├── widgets.py         # Windowing widgets, menus, checkboxes, file picker
│   └── app.py             # Interactive TUI workflow controller
└── targets/
    └── mfk3/              # Target 0x00A5 Valeo MFK3 (2Q0 980 653, RH850)
        ├── README.md      # MFK3 module & flashing guide (RU)
        ├── README.en.md   # MFK3 module & flashing guide (EN)
        ├── constants.py   # Memory layout, dump sizes, and 9 FeC table
        ├── signatures.py  # RH850 opcode signatures & patch/rollback specs
        ├── loader.py      # Auto-detection of FRF / ODX / DB_01 / bench dumps
        └── plugin.py      # Inspection, patching, ODX builder & self-tests
```

---

<div align="center">

**Made with research & love for VAG retrofitting by [PerkTheFox](https://vwhacking.antonperk.com)**  
[vwhacking.antonperk.com](https://vwhacking.antonperk.com) • [Drive2](https://www.drive2.ru/users/perkthefox/) • [Telegram](https://t.me/perkthefox)

</div>
