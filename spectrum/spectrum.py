import os.path

import sys

from spectrum.keyboard import Keyboard
from spectrum.profiling_spectrum_bus_access import ProfilingZXSpectrum48ClockAndBusAccess
from spectrum.spectrum_bus_access import ZXSpectrum48ClockAndBusAccess
from spectrum.spectrum_ports import SpectrumPorts
from spectrum.video import TSTATES_PER_INTERRUPT, Video
from utils.loader import Loader
from z80.instructions import Instruction, AddrMode
from z80.instructions.instruction_def import decode_instruction
from z80.instructions.instructions import HALT
from z80.memory import Memory
from z80.z80_cpu import Z80CPU

ROMFILE = "zxspectrum48k.rom"


# This class mostly instatiates and encapsulates several different parts
# including memory, ports, bus access, processor and video
class Spectrum:
    def __init__(self):
        self.keyboard = Keyboard()
        self.ports = SpectrumPorts(self.keyboard)
        self.memory = Memory()

        self.video = Video(self.memory, self.ports)

        self._normal_bus_access = ZXSpectrum48ClockAndBusAccess(
            self.memory,
            self.ports,
            self.video.update_next_screen_word)

        self._profiling_bus_access = ProfilingZXSpectrum48ClockAndBusAccess(
            self.memory,
            self.ports,
            self.video.update_next_screen_word)
        self._bus_access = self._normal_bus_access
        self.instructions = []

        self.z80 = Z80CPU(self._bus_access)

        self.loader = Loader(self.z80, self.ports)

        self.video_update_time = 0

        self.video.init()

    @property
    def bus_access(self) -> ZXSpectrum48ClockAndBusAccess: return self._bus_access

    @bus_access.setter
    def bus_access(self, bus_access: ZXSpectrum48ClockAndBusAccess) -> None:
        self._bus_access = bus_access
        self.z80.bus_access = bus_access

    def load_rom(self, romfilename):
        with open(os.path.join(os.path.dirname(__file__), romfilename), "rb") as rom:
            rom.readinto(self.memory.mem)

        print(f"Loaded ROM: {romfilename}")

    def init(self):
        self.load_rom(ROMFILE)
        self.ports.out_port(254, 0xff)  # white border on startup
        self.z80.reset()
        self.bus_access.reset()

        sys.setswitchinterval(255)  # we don't use threads, kind of speed up

    def update_screen(self) -> None:
        self.video.update_screen()

    def end_frame(self) -> None:
        self.bus_access.end_frame(TSTATES_PER_INTERRUPT)
        self.video.update_screen()
        self.video.start_screen()

    def execute(self, tstate_limit: int) -> None:
        self.z80.execute(tstate_limit)

    def profile(self, tstate_limit: int = TSTATES_PER_INTERRUPT) -> None:
        ptr = [0]

        def next_byte() -> int:
            p = ptr[0]
            ptr[0] += 1
            return self.memory.mem[p]

        self._profiling_bus_access.copy_from_bus_access(self._normal_bus_access)
        self._bus_access = self._profiling_bus_access
        self.z80.bus_access = self._profiling_bus_access
        del self.instructions[:]
        while self.bus_access.tstates < tstate_limit:
            self._profiling_bus_access.profile = []
            address = self.z80.regPC
            ptr[0] = address
            # code = self.memory.mem[address]
            tstates = self._profiling_bus_access.tstates
            self.z80.execute_one_cycle()
            if self.z80.halted:
                instruction = Instruction(address, HALT(), AddrMode.SIMPLE)
            else:
                instruction = decode_instruction(address, next_byte)
            instruction.profile = self._profiling_bus_access.profile
            instruction.tstates = tstates
            self.instructions.append(instruction)
        self._normal_bus_access.copy_from_bus_access(self._profiling_bus_access)
        self._bus_access = self._normal_bus_access
        self.z80.bus_access = self._bus_access

    def load_sna(self, filename: str) -> None:
        self.loader.load_sna(filename)

    def execute_one_instruction(self) -> bool:
        self.z80.execute_one_cycle()
        return self.bus_access.tstates >= TSTATES_PER_INTERRUPT
