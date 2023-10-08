# Track The Blueprint

I have a lot of ideas for things I would like to program to help track progress with the amazing Mandarin Chinese course - [The Mandarin Blueprin Method](https://www.mandarinblueprint.com/)

But for now this repository contains some code that scrapes the [Traverse learned characters website](https://traverse.link/Mandarin_Blueprint/word-progress/?level=36) and outputs files that one can import in [Legacy Migaku](https://chrome.google.com/webstore/detail/migaku-legacy/acpchjgielgmkgkplljakcibfbjjppbk) as **Known Words**

# How to get the Migaku files
Simply navigate to the folder [_migaku_known_words_](https://github.com/benjaminorthner/trackTheBlueprint/tree/master/migaku_known_words), click on the file matching your current MandarinBlueprint level and then click download inside the button with the three dots.

You can upload this file inside the Legacy Migaku settings, on the page _Learning Status_ by clicking on the import word data _From Backup_ button.


# For Programmers
I programmed this to run in WSL (Windows subsystems for linux) and before running one should install the following packages

```bash
sudo apt-get update
sudo apt-get install firefox-geckodriver
pip3 install selenium
pip3 install hanzidentifier
```
