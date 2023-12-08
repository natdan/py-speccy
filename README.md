# py-speccy
Python/Pygame implementation ZX Spectrum Emulator
====================================================

This is ZX Spectrum 48k emulator completely implemented in
python and pyame (https://www.pygame.org/) and based on:

- PyZX (https://github.com/Q-Master/PyZX) - original code
- JSpeccy (https://github.com/jsanchezv/JSpeccy) - Z80 code and memory timings

Main intention for this emulator is to provide clock correct version of
original ZX Spectrum 48k for development and debugging purposes.

With code entirely made in Python it might not achieve full 100% speed
on a single core on every machine, but idea is to have fully accessible
Z80 emulation along with correct memory contention timings. As such it is
ideal for reasearch and development for this platform.


Requirements
-------------

This code is done on python 3.9 with pygame 2.5.2 (see requirements file).


Running
--------

To run pygame-emulator example:

```bash
git clone https://github.com/natdan/py-speccy
cd py-speccy
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

python3 run.py
```

You can use following keys:
- F1 to pause/unpause
- F3 to change size of window


Current state of development
-----------------------------

Thanks to JSpeecy code, memory contention is fully implmemented along with
correct Z80 core emulation.

What is working:
- Z80 passes zexall - https://mdfs.net/Software/Z80/Exerciser/Spectrum/)
- video is working with correct timings ('nirvana-demo.sna') thanks to JSpeccy code (https://github.com/jsanchezv/JSpeccy)


What is not working:
- border is not emulated aside of setting it for complete screen
- sound is not working
- only snapshot loads are working (thanks to PyZX - https://github.com/Q-Master/PyZX)
- no emulation of any other kind of joysticks but what was implemented in PyZX
