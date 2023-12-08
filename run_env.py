from debug_environment import DebugEnvironment
from spectrum.spectrum import Spectrum


spectrum = Spectrum()
spectrum.init()

environment = DebugEnvironment(spectrum, show_fps=True)
environment.init()


# Comment these out if you want to start with normal reset and basic
#
# spectrum.load_sna("snapshots/screen_timing.sna")
# spectrum.load_sna("snapshots/screen_timing_early.sna")
# spectrum.load_sna("snapshots/screen_timing_late.sna")
# spectrum.load_sna("snapshots/zexall.sna")
spectrum.load_sna("snapshots/nirvana-demo.sna")

# spectrum.video.fast = True
# spectrum.z80.show_debug_info = True
# spectrum.keyboard.do_key(True, 13, 0)

environment.run()
