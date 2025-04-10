# MOCT - Memory OverClocking Tool

[![Static Badge](https://img.shields.io/badge/%20Discord-grey?logo=discord)](https://discord.gg/SU9db8WgUp)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/memoryoctool/MOCT/build.yml)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/memoryoctool/MOCT/total)

MOCT simplifies the tedious process of memory overclocking. Tuning memory involves adjusting voltage, frequency, timings, and subtimings—with lots of trial and error. After every BIOS change, you reboot, verify the settings, and run stability tests, constantly monitoring for errors.

MOCT automates all that. After a reboot, it verifies your memory settings, runs stress tests automatically, and notifies you of any instability.

## Features

<img src="https://github.com/user-attachments/assets/3507cfa6-24f4-43e3-8ba2-7fd5165216fe" align="right">

🔧 **Automatic Frequency Check**:
On startup, MOCT checks if your memory settings were applied or reset to defaults. 

🔥 **Stability Testing**:
Automatically runs TestMem5 to validate system stability after each reboot.

💬 **Telegram Notifications**:
Get notified on Telegram when tests complete—no need to keep checking manually.

🔃 **BIOS Reboot Automation**:
After testing (whether passed or failed), your system will automatically reboot into BIOS so you can tweak settings faster.

<br clear="both">

## 📦 Download

You can download exe file from releases.

## ❓ Do i still need to set memory timings manually?

Yes, you should still manually set memory timings in the BIOS.

## 🧪 How does testing work?

MOCT will run [TestMem5](https://github.com/CoolCmd/TestMem5) and get results from it. If any issue occurs, it will notify you as soon as error is detected.

## 🤝 Contributing

We love contributions! If you have an idea, feature request, or bug report, please open an issue or chat with us on Discord.

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

If MOCT has helped you, consider ⭐️ starring the repo.

## ⚠️ Disclaimer

This software **does not modify** any system or BIOS settings. It only verifies if memory overclocking settings were applied and ensures system stability through testing.


