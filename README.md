# PSPEWC
![](https://raw.githubusercontent.com/jacquesCedric/PSPEWC-mac/master/icon_128x128.png)

A macOS application that allows you to use your PSP as a wireless controller.

## How to Setup
1. Download the app from the Releases page ([Releases page](https://github.com/jacquesCedric/PSPEWC-mac/releases)) or, optionally, compile from source (see below)
2. Unzip
4. Run the MAC/PSPEWC.app on your computer. This is the server
5. Put the PSP/GAME/PSPEasyWirelessController folder inside your GAME folder on your PSP
6. Start the PSPEWC homebrew on your PSP and set it up with the IP displayed in PSPEWC.app
7. PSP will display message confirming connection.

## Usage
When connected the PSP emulates keyboard button presses. So long as your game has assignable buttons, this controller should work. It's been tested in Retroarch and OpenEmu thus far, working perfectly!

##Compilation##
Requires py2app and RUMPS to be installed!
1. Clone source
2. Run "python setup.py py2app"
3. Locate app in "dist" folder

## Notes
All software written by myself is public domain.
This release is a heavily adapted version of [PSP Easy Wireless Controller](https://github.com/atphalix/PSP-Easy-Wireless-Controller) for Windows.

Built on macOS 10.11.4 for versions 10.9+
