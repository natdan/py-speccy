from spectrum.spectrum import Spectrum
from spectrum.spectrum_bus_access import ZXSpectrum48ClockAndBusAccess
from spectrum.video import SCREEN_WIDTH, SCREEN_HEIGHT, Video
from z80.z80_state import Z80State


class VideoState:
    def __init__(self) -> None:
        self.offs = 0
        self.pix_addr = 0
        self.attr_addr = 0
        self.pixel_byte_y = 0
        self.pixel_byte_x = 0
        self.video_buffer: memoryview = memoryview(bytearray(SCREEN_WIDTH * SCREEN_HEIGHT))

    def update_from(self, video: Video) -> None:
        self.offs = video.offs
        self.pix_addr = video.pix_addr
        self.attr_addr = video.attr_addr
        self.pixel_byte_x = video.pixel_byte_x
        self.pixel_byte_y = video.pixel_byte_y
        self.video_buffer[:] = video.buffer_m[:]

    def restore_to(self, video: Video) -> None:
        video.offs = self.offs
        video.pix_addr = self.pix_addr
        video.attr_addr = self.attr_addr
        video.pixel_byte_x = self.pixel_byte_x
        video.pixel_byte_y = self.pixel_byte_y
        video.buffer_m[:] = self.video_buffer[:]

    @classmethod
    def create_from(cls, video: Video) -> 'VideoState':
        video_state = VideoState()
        video_state.offs = video.offs
        video_state.pix_addr = video.pix_addr
        video_state.attr_addr = video.attr_addr
        video_state.pixel_byte_x = video.pixel_byte_x
        video_state.pixel_byte_y = video.pixel_byte_y
        video_state.video_buffer[:] = video.buffer_m[:]
        return video_state


class BusState:
    def __init__(self) -> None:
        self.tstates = 0
        self.border = 0
        self.next_screen_byte_index = 0

    def update_from(self, bus_access: ZXSpectrum48ClockAndBusAccess) -> None:
        self.tstates = bus_access.tstates
        self.next_screen_byte_index = bus_access.next_screen_byte_index
        self.border = bus_access.ports.current_border

    def restore_to(self, bus_access: ZXSpectrum48ClockAndBusAccess) -> None:
        bus_access.tstates = self.tstates
        bus_access.next_screen_byte_index = self.next_screen_byte_index
        bus_access.ports.current_border = self.border

    @classmethod
    def create_from(cls, bus_access: ZXSpectrum48ClockAndBusAccess) -> 'BusState':
        bus_state = BusState()
        bus_state.tstates = bus_access.tstates
        bus_state.next_screen_byte_index = bus_access.next_screen_byte_index
        bus_state.border = bus_access.ports.current_border
        return bus_state


class SpectrumState:
    def __init__(self,
                 memory: memoryview,
                 bus_state: BusState,
                 z80_state: Z80State,
                 video_state: VideoState) -> None:
        self.memory = memory
        self.bus_state = bus_state
        self.state = z80_state
        self.video_state = video_state

    def restore_to(self, spectrum: Spectrum) -> None:
        spectrum.z80.bus_access.memory.mem[:] = self.memory[:]
        self.bus_state.restore_to(spectrum.bus_access)
        self.state.restore_to(spectrum.z80)
        self.video_state.restore_to(spectrum.video)
        spectrum.update_screen()

    def update_from(self, spectrum: Spectrum) -> None:
        self.memory[:] = spectrum.z80.bus_access.memory.mem[:]
        self.bus_state.update_from(spectrum.bus_access)
        self.state.update_from(spectrum.z80, 0)
        self.video_state.update_from(spectrum.video)

    @classmethod
    def create(cls, spectrum: Spectrum) -> 'SpectrumState':
        memory = memoryview(bytearray(65536))
        memory[:] = spectrum.z80.bus_access.memory.mem[:]

        bus_state = BusState.create_from(spectrum.bus_access)

        video_buffer = memoryview(bytearray(SCREEN_WIDTH * SCREEN_HEIGHT))
        video_buffer[:] = spectrum.video.buffer_m[:]

        video_rendering_state = VideoState.create_from(spectrum.video)
        return SpectrumState(
            memory,
            bus_state,
            Z80State.create_from(spectrum.z80, 0),
            video_rendering_state
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
