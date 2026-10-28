<div align="center">

# `0x00A5` • Valeo MFK3 (`2Q0 980 653`)
### Target Module Documentation for **Schutz-Kaput** (`Renesas RH850/P1H-C` • SW `13xx` / `14xx`)

**[← Back to `Schutz-Kaput` Main Page](../../README.en.md)** • **[🇷🇺 Читать на русском (`README.md`)](README.md) | 🇬🇧 English**

</div>

---

> [!CAUTION]
> **RISK REMINDER:**  
> Everything that happens to the camera afterwards is 100% your responsibility. This script only prepares files locally and does NOT control the flashing process. Always save a complete backup of your original Flash and `EEPROM` / `NvM` first. **Bricked units CANNOT be recovered over OBD — recovery is impossible without a hardware bench programmer!** See [`LICENSE.md`](../../LICENSE.md) for full terms.

---

## Supported Hardware & Input Formats

* **Control Unit:** **Valeo MFK3** front driver assistance camera (`2Q0 980 653` across hardware/software suffixes), diagnostic address **`0x00A5`**.
* **Hardware Architecture:** **`Renesas RH850/P1H-C` (`R7F701372A`)** host MCU + **`Mobileye EyeQ4`** vision SoC (`DB_03`).
* **Application Firmware (`MEAPP`):** **`13xx` / `14xx`** release branches.
* **Accepted Input Files:**
  * factory encrypted **`.frf`** and unpacked **`.odx-f` / `.odx` / `.pdx`** containers;
  * standalone extracted **`DB_01FLASHDATA.bin`** (`0x00048000..0x001FFFFF`, `~1.72 MiB`);
  * full bench programmer dumps: **`Bank 0` (`2 MiB`)**, **`Dual-Bank` (`4 MiB`)**, and linear **`9.84 MiB` / `10 MiB`** dumps.

---

## What the Patcher Does on `Valeo MFK3`

### 1. Component Protection Bypass (`KS_PASSIVE`, 5 sites in `DB_01`)
* Switches `Komponentenschutz` into passive mode, removing functional ADAS lockouts on retrofitted vehicles.
* Protects **`NvM 0x3C`** non-volatile memory from repeated CP error-counter write wear.
* **Built-in safety guards:**
  * verifies and preserves the 8-byte cold-boot application header (`0xAA000000` + `0x00048200` @ `0x00048000`);
  * automatically rejects accidental attempts to patch the **`0220_FBL`** bootloader updater (`~222 KB`) as `MEAPP`.

### 2. All 9 `FeC` / `SWaP` Features Unlocked (4 sites in `DB_01`)
* Enables all supported camera features at runtime (enabled by default; pass `--no-fecs` to skip).
* Reports the full factory **`0xFF`** status byte across all 9 slots in **`DID 0x3C00`** (*Status of all SWaP functions* in `ODIS`: `Release code: available`, `Cancellation: no`, `Individualization characteristic: valid`, `Preconditions met: Condition met`, `Configuration: OK`, `Functions: available`, `Authentication: Condition met`):

| `FeC` ID | Feature Description (`Valeo MFK3`) |
| :---: | :--- |
| `100E0F00` | Traffic Sign Recognition (**`VZE`**) |
| `100E1000` | Core Driver Assistants (**`Lane Assist`**, High Beam Assist **`FLA`**, **`pACC`**) |
| `100E1100` | Extended Lane Guidance |
| `100E1200` | Additional ADAS Feature Channel `#1` |
| `100E1300` | Additional ADAS Feature Channel `#2` |
| `100E1400` | Additional ADAS Feature Channel `#3` |
| `100E1500` | Additional ADAS Feature Channel `#4` |
| `100E1600` | Reserved Feature Slot `#1` |
| `100E1700` | Reserved Feature Slot `#2` |

### 3. Unadapted Key DTC Suppression (`--suppress-key-dtcs`, optional)
* Suppresses missing basic/individual CP key DTCs — useful on brand-new Virgin cameras that have never had CP keys adapted.

### 4. Engineering Option: `XCP` on `CAN0` (`--enable-xcp-can0`, OFF by default)
* **Ordinary users do NOT need this option for retrofitting.**
* Switches `Xcp_BootControl` into active mode `0x55` at startup on **`CAN0`**:
  * `T12a` connector: pin **`3 = CAN-H`**, pin **`4 = CAN-L`**, **`500 kbit/s`**;
  * `Extended 29-bit CAN`: master TX **`0x1BFE7E01`** → slave RX **`0x1BFE7E00`**.

### 5. Hardware-Safe `ODIS-E` Package Builder (`PART1` + `PART2`)
* Packs `DB_01` **strictly uncompressed (`method=00`, `<SECURITY-METHOD>SIG_SHA1-RSA1024_S</SECURITY-METHOD>`)**, preventing `0220` bootloader LZSS overlapping-RLE faults (`7F 36 72` / `generalProgrammingFailure`).
* Assigns distinct internal XML IDs (`_KS_FEC_PART1_S` and `_KS_FEC_PART2_S`) so `ODIS-E` (`MCD-3D`) never collides when loading both containers simultaneously.

---

## Two-Step `ODIS-E` Flashing (`PART1` → `PART2`)

When generating ODX containers for `ODIS-E`, two subfolders (`PART1` and `PART2`) are created:

1. **Step 1 (`PART1`):** flash the container inside `PART1`. At the very end (`RoutineControl 31 01 02 02`), `ODIS-E` will report an expected signature verification error on the patched `DB_01` block — **do not panic and do not turn off ignition**; the patched firmware is already written to flash.
2. **Step 2 (`PART2`):** without turning off ignition, immediately flash the container inside `PART2` (containing stock signed `DB_30` + `DB_04`). Flashing will complete **100% green** (`71 01 02 02 01`) and return the camera from bootloader to normal operating mode.

---

## CLI Examples for `mfk3`

```bash
# Inspect a factory container (.frf / .odx-f) or bench dump
python3 ks_patcher.py -l en -t mfk3 inspect FL_2Q0980653J_1423_MEAPP_V001_S.frf

# Build two-step ODIS-E PART1 + PART2 packages (KS_PASSIVE + all 9 FeCs)
python3 ks_patcher.py -l en -t mfk3 patch FL_2Q0980653J_1423_MEAPP_V001_S.frf --build-odx ./ODIS_MFK3_READY

# Build ODX from raw DB_01 using a factory .frf / .odx-f template
python3 ks_patcher.py -l en -t mfk3 patch DB_01FLASHDATA.bin --template-odx FL_2Q0980653J_1423_MEAPP_V001_S.frf --build-odx ./ODIS_MFK3_READY

# Patch a bench programmer dump (Bank 0 / Dual-Bank)
python3 ks_patcher.py -l en -t mfk3 patch Bank0_dump.bin -o Bank0_patched.bin

# Losslessly revert a patched dump back to 100% factory stock
python3 ks_patcher.py -l en -t mfk3 patch Bank0_patched.bin --restore-stock -o Bank0_restored.bin
```
