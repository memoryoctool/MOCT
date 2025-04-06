# MOCT - Memory OverClocking Tool

[![Static Badge](https://img.shields.io/badge/%20Discord-grey?logo=discord)](https://discord.gg/SU9db8WgUp)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/memoryoctool/MOCT/total)

Memory overclocking is tideous. There are many parameters to adjust: voltage, frequency, timings, subtimings. A lot of trial and error is needed to get the best results. After each change you reboot your system, check if the changes are applied or not, run system or memory stability tests. And while tests are running you have to look after it to see if the system is stable or not.

MOCT is a tool that makes overclocking easier. When you make a change in BIOS and reboot your PC, the tool will automatically start with the system to check if memory changes were applied correctly and were not set to default. Then it will run stability tests. If any issue occurs during stability tests, it will notify you as soon as error is detected. If tests are finished successfully, it will also notifiy you.

## Features

<img src="https://github.com/user-attachments/assets/3507cfa6-24f4-43e3-8ba2-7fd5165216fe" align="right">

* 🔧 **Check memory frequency on startup**: When you boot up your system, MOCT checks if the changes made in BIOS were applied correctly. 
* 🔥 **Stability Tests**: Run stability tests on your memory to ensure that overclocking is stable.
* 💬 **Telegram integration**: Send notification to Telegram when stability tests are done, so you do not have to check the computer all the time.
* 🔃 **Reboot PC into BIOS**: When testing is done (with errors or without), system will reboot automatically into BIOS. This way you can make changes faster and test again.

<br clear="both">

## Download

You can download exe file from releases.

## Do i still need to set memory timings manually?

Yes, you should still manually set memory timings in the BIOS.

## How does testing work?

MOCT will run [TestMem5](https://github.com/CoolCmd/TestMem5) and get results from it. If any issue occurs, it will notify you as soon as error is detected.

## Contributing

We love contributions! If you have an idea for a feature or found a bug, please open an issue or write us directly on Discord.

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Disclaimer

This software does not modify you computer's settings in any way. It only checks to make sure that system will be stabl and perform well with overclocked memory.
