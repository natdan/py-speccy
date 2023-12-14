from spectrum.spectrum import Spectrum
from spectrum.video import SCREEN_WIDTH, SCREEN_HEIGHT
from z80.z80_state import Z80State


class SpectrumState:
    def __init__(self, tstate, video_buffer: memoryview, memory: memoryview, z80_state: Z80State) -> None:
        self.tstate = tstate
        self.video_buffer = video_buffer
        self.memory = memory
        self.state = z80_state

    def restore_to(self, spectrum: Spectrum) -> None:
        spectrum.bus_access.tstates = self.tstate
        spectrum.video.buffer_m[:] = self.video_buffer[:]
        spectrum.z80.bus_access.memory.mem[:] = self.memory[:]
        self.state.restore_to(spectrum.z80)
        spectrum.update_screen()

    def update_from(self, spectrum: Spectrum) -> None:
        self.tstate = spectrum.bus_access.tstates
        self.video_buffer[:] = spectrum.video.buffer_m[:]
        self.memory[:] = spectrum.z80.bus_access.memory.mem[:]
        self.state.update_from(spectrum.z80, 0)

    @classmethod
    def create(cls, spectrum: Spectrum) -> 'SpectrumState':
        memory = memoryview(bytearray(65536))
        memory[:] = spectrum.z80.bus_access.memory.mem[:]

        video_buffer = memoryview(bytearray(SCREEN_WIDTH * SCREEN_HEIGHT))
        video_buffer[:] = spectrum.video.buffer_m[:]
        return SpectrumState(
            spectrum.bus_access.tstates,
            video_buffer,
            memory,
            Z80State.create_from(spectrum.z80, 0)
        )


class Playback:
    def __init__(self, spectrum: Spectrum, backlog_size: int = 20000) -> None:
        self.spectrum = spectrum
        self.backlog_size = backlog_size
        self.backlog: list[SpectrumState] = []
        self.top = 0

    def reset(self) -> None:
        self.top = 0

    def record(self) -> None:
        if self.top == len(self.backlog):
            if len(self.backlog) >= self.backlog_size:
                state = self.backlog[0]
                self.backlog[0:-1] = self.backlog[1:]
                self.backlog[-1] = state

                state.update_from(self.spectrum)
            else:
                state = SpectrumState.create(self.spectrum)
                self.backlog.append(state)
                self.top = len(self.backlog)
        else:
            state = self.backlog[self.top]
            state.update_from(self.spectrum)
            self.top += 1

    def restore_previous(self, skip_count: int = 1) -> None:
        self.top -= skip_count
        if self.top < 0: self.top = 0

        if self.top < len(self.backlog):
            self.backlog[self.top].restore_to(self.spectrum)
