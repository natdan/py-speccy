from pygame_emulator import PyGameEmulator
from spectrum.machine import Spectrum
from utils.load import Load


spectrum = Spectrum()
spectrum.init()

emulator = PyGameEmulator(spectrum, show_fps=True, ratio=3)
emulator.init()

load = Load(spectrum.z80, spectrum.ports)

# load.load_sna("snapshots/zexall.sna")
load.load_sna("snapshots/nirvana-demo.sna")

# spectrum.video.fast = True
# spectrum.z80.show_debug_info = True
# spectrum.keyboard.do_key(True, 13, 0)

emulator.run()
