# Wooting Mouse

## Introduction

Use your Wooting 60HE (in analog/gamepad mode) as a virtual mouse (Linux only).

Currently it supports moving the mouse cursor, horizontal and vertical
scrolling using analog input.

It also supports the left, middle and right mouse button, and for my
convience pressing capslock, left ctrl, left alt, back and forward.

I also added a nice feature to change the RGB colors of the keyboard
throughout the day.

## Installation

1. Install this Python project (ie. using `poetry install`)
1. Obtain the path to `wooting-mouse` (ie. use `poetry run which wooting-mouse`)
1. Update `data/wooting-mouse@.service` with the path of `wooting-mouse`
1. Copy `data/wooting-mouse@.service` to `/etc/systemd/system`
1. Copy `data/50-wooting.rules` to `/etc/udev/rules.d/50-wooting.rules`
1. Load the following profiles in wootility.io:
   `afb6fa5e78af3918bf16c96cdeaa6e61e3c5` and
   `63334117673c8f6cff3e618edec7466caf3a`
1. Reboot or reload udev
