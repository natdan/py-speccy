from typing import Callable

from spectrum.spectrum_bus_access import ZXSpectrum48ClockAndBusAccess
from z80.instructions.profile import FetchOpcode, PeekB, PokeB, PeekW, PokeW, AddrOnBus, InPort, OutPort
from z80.memory import Memory
from z80.ports import Ports


INTERRUPT_LENGTH = 24


# This implementation heavily inspired by one from JSpeccy
# https://github.com/jsanchezv/JSpeccy/blob/master/src/main/java/machine/Spectrum.java
class ProfilingZXSpectrum48ClockAndBusAccess(ZXSpectrum48ClockAndBusAccess):
    def __init__(self,
                 memory: Memory,
                 ports: Ports,
                 update_next_screen_byte: Callable) -> None:
        super().__init__(memory, ports, update_next_screen_byte)
        self.profile = []

    def fetch_opcode(self, address: int) -> int:
        if 16384 <= address < 32768:
            self.profile.append(FetchOpcode(self.tstates, 4, self.delay_tstates[self.tstates]))
            self.tstates += self.delay_tstates[self.tstates] + 4
        else:
            self.profile.append(FetchOpcode(self.tstates, 4))
            self.tstates += 4

        if self.tstates >= self.screen_byte_tstate[self.next_screen_byte_index]:
            self.update_next_screen_word()
            self.next_screen_byte_index += 1

        t = self.memory.peekb(address)
        return t

    def peekb(self, address: int) -> int:
        if 16384 <= address < 32768:
            self.profile.append(PeekB(self.tstates, 3, self.delay_tstates[self.tstates]))
            self.tstates += self.delay_tstates[self.tstates] + 3
        else:
            self.profile.append(PeekB(self.tstates, 3))
            self.tstates += 3

        if self.tstates >= self.screen_byte_tstate[self.next_screen_byte_index]:
            self.update_next_screen_word()
            self.next_screen_byte_index += 1

        return self.memory.peekb(address)

    def peeksb(self, address: int) -> int:
        if 16384 <= address < 32768:
            self.profile.append(PeekB(self.tstates, 3, self.delay_tstates[self.tstates]))
            self.tstates += self.delay_tstates[self.tstates] + 3
        else:
            self.profile.append(PeekB(self.tstates, 3))
            self.tstates += 3

        if self.tstates >= self.screen_byte_tstate[self.next_screen_byte_index]:
            self.update_next_screen_word()
            self.next_screen_byte_index += 1

        return self.memory.peeksb(address)

    def pokeb(self, address: int, value: int) -> None:
        if 16384 <= address < 32768:
            self.profile.append(PokeB(self.tstates, 3, self.delay_tstates[self.tstates]))
            self.tstates += self.delay_tstates[self.tstates] + 3
        else:
            self.profile.append(PokeB(self.tstates, 3))
            self.tstates += 3

        if self.tstates >= self.screen_byte_tstate[self.next_screen_byte_index]:
            self.update_next_screen_word()
            self.next_screen_byte_index += 1

        self.memory.pokeb(address, value & 0xFF)

    def peekw(self, address: int) -> int:
        delay1 = 0
        delay2 = 0
        if 16384 <= address < 32768:
            delay1 = self.delay_tstates[self.tstates]
            self.tstates += self.delay_tstates[self.tstates] + 3
        else:
            self.tstates += 3

        if self.tstates >= self.screen_byte_tstate[self.next_screen_byte_index]:
            self.update_next_screen_word()
            self.next_screen_byte_index += 1

        lsb = self.memory.peekb(address)

        address = (address + 1) & 0xffff
        if 16384 <= address < 32768:
            delay2 = self.delay_tstates[self.tstates]
            self.tstates += self.delay_tstates[self.tstates] + 3
        else:
            self.tstates += 3

        self.profile.append(PeekW(self.tstates, 3, 3,  delay1, delay2))

        if self.tstates >= self.screen_byte_tstate[self.next_screen_byte_index]:
            self.update_next_screen_word()
            self.next_screen_byte_index += 1

        msb = self.memory.peekb(address)

        return (msb << 8) + lsb

    def pokew(self, address: int, value: int) -> None:
        delay1 = 0
        delay2 = 0
        if 16384 <= address < 32768:
            delay1 = self.delay_tstates[self.tstates]
            self.tstates += self.delay_tstates[self.tstates] + 3
        else:
            self.tstates += 3

        if self.tstates >= self.screen_byte_tstate[self.next_screen_byte_index]:
            self.update_next_screen_word()
            self.next_screen_byte_index += 1

        self.memory.pokeb(address, value & 0xff)

        address = (address + 1) & 0xffff
        if 16384 <= address < 32768:
            delay2 = self.delay_tstates[self.tstates]
            self.tstates += self.delay_tstates[self.tstates] + 3
        else:
            self.tstates += 3

        self.profile.append(PokeW(self.tstates, 3, 3,  delay1, delay2))

        if self.tstates >= self.screen_byte_tstate[self.next_screen_byte_index]:
            self.update_next_screen_word()
            self.next_screen_byte_index += 1

        self.memory.pokeb(address, (value >> 8))

    def address_on_bus(self, address: int, tstates: int) -> None:
        delays = []
        if 16384 <= address < 32768:
            for i in range(tstates):
                delays.append(self.delay_tstates[self.tstates])
                self.tstates += self.delay_tstates[self.tstates] + 1
        else:
            self.tstates += tstates

        self.profile.append(AddrOnBus(self.tstates, tstates, *delays))

        while self.tstates >= self.screen_byte_tstate[self.next_screen_byte_index]:
            self.update_next_screen_word()
            self.next_screen_byte_index += 1

    def interrupt_handling_time(self, tstates: int) -> None:
        self.tstates += tstates

        while self.tstates >= self.screen_byte_tstate[self.next_screen_byte_index]:
            self.update_next_screen_word()
            self.next_screen_byte_index += 1

    def in_port(self, port: int) -> int:
        delays = []
        if 16384 <= port < 32768:
            delays.append(self.delay_tstates[self.tstates])
            self.tstates += self.delay_tstates[self.tstates] + 1
        else:
            delays.append(0)
            self.tstates += 1

        if self.tstates >= self.screen_byte_tstate[self.next_screen_byte_index]:
            self.update_next_screen_word()
            self.next_screen_byte_index += 1

        if port & 0x0001 != 0:
            if 16384 <= port < 32768:
                delays.append(self.delay_tstates[self.tstates])
                self.tstates += self.delay_tstates[self.tstates] + 1
                delays.append(self.delay_tstates[self.tstates])
                self.tstates += self.delay_tstates[self.tstates] + 1
                delays.append(self.delay_tstates[self.tstates])
                self.tstates += self.delay_tstates[self.tstates] + 1
                delays.append(self.delay_tstates[self.tstates])
            else:
                self.tstates += 3
                delays.append(0)
                delays.append(0)
                delays.append(0)
        else:
            self.tstates += self.delay_tstates[self.tstates] + 3
            delays.append(0)
            delays.append(0)
            delays.append(0)

        self.profile.append(InPort(self.tstates, 4, *delays))

        if self.tstates >= self.screen_byte_tstate[self.next_screen_byte_index]:
            self.update_next_screen_word()
            self.next_screen_byte_index += 1

        return self.ports.in_port(port)

    def out_port(self, port: int, value: int):
        delays = []
        if 16384 <= port < 32768:
            delays.append(self.delay_tstates[self.tstates])
            self.tstates += self.delay_tstates[self.tstates] + 1
        else:
            self.tstates += 1
            delays.append(0)

        self.ports.out_port(port, value)
        if port & 0x0001 != 0:
            if 16384 <= port < 32768:
                delays.append(self.delay_tstates[self.tstates])
                self.tstates += self.delay_tstates[self.tstates] + 1
                delays.append(self.delay_tstates[self.tstates])
                self.tstates += self.delay_tstates[self.tstates] + 1
                delays.append(self.delay_tstates[self.tstates])
                self.tstates += self.delay_tstates[self.tstates] + 1
            else:
                self.tstates += 3
                delays.append(0)
                delays.append(0)
                delays.append(0)
        else:
            self.tstates += self.delay_tstates[self.tstates] + 3
            delays.append(0)
            delays.append(0)
            delays.append(0)

        self.profile.append(OutPort(self.tstates, 4, *delays))

        if self.tstates >= self.screen_byte_tstate[self.next_screen_byte_index]:
            self.update_next_screen_word()
            self.next_screen_byte_index += 1
