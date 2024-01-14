#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uscpi.client import ClientBase


class Instrument:
    """Instrument representation.

    Implements common commands associated with IEEE-488.2.
    """

    def __init__(self, client: ClientBase) -> None:
        self.client = client

    @property
    def client(self) -> ClientBase:
        return self._client

    @client.setter
    def client(self, value: ClientBase) -> None:
        if isinstance(value, ClientBase):
            self._client = value
            return
        raise TypeError("Expected a ClientBase object")

    def cls(self) -> None:
        """Clear Status Command.

        Clears the event registers in all register groups.
        Also clears the error queue.
        """

        return self.client.write(b"*CLS\n")

    def ese(self, value: int | None = None) -> bytes | None:
        """Event Status Enable Command and Query.

        Enables bits in the enable register for the Standard
        Event Register group. The selected bits are then
        reported to bit 5 of the Status Byte Register. An
        enable register defines which bits in the event
        register will be reported to the Status Byte
        register group. You can write to or read from an
        enable register.
        """

        if isinstance(value, int):
            if value not in range(256):
                raise ValueError(value)
            return self.client.write(f"*ESE {value}\n".encode())
        return self.client.write_readline(b"*ESE?\n")

    def esr(self) -> bytes:
        """Standard Event Status Register Query.

        Queries the event register for the Standard Event
        Register group.

        An event register is a read-only register that
        latches events from the condition register. While an
        event bit is set, subsequent events corresponding to
        that bit are ignored.
        """

        return self.client.write_readline(b"*ESR?\n")

    def idn(self) -> bytes:
        """Identification Query.

        Returns the instrument’s identification string.
        """

        return self.client.write_readline(b"*IDN?\n")

    def opc(self, complete: bool = False) -> bytes | None:
        """Operation Complete Command and Query.

        Sets "Operation Complete" (bit 0) in the Standard
        Event register at the completion of the current
        operation.
        """

        if isinstance(complete, bool) and complete:
            return self.client.write(b"*OPC\n")
        return self.client.write_readline(b"*OPC?\n")

    def rst(self) -> None:
        """Reset Command.

        Resets instrument to factory default state,
        independent of MMEMory:STATe:RECall:AUTO setting.
        This is similar to SYSTem:PRESet. The difference is
        that *RST resets the instrument for SCPI operation,
        and SYSTem:PRESet resets the instrument for
        front-panel operation. As a result, *RST turns the
        histogram and statistics off, and SYSTem:PRESet
        turns them on (CALC:TRAN:HIST:STAT ON).
        """

        return self.client.write(b"*RST\n")

    def sre(self, value: int | None = None) -> bytes | None:
        """Service Request Enable Command and Query.

        Service Request Enable. Enables bits in the enable
        register for the Status Byte Register group. An
        enable register defines which bits in the event
        register will be reported to the Status Byte
        register group. You can write to or read from an
        enable register.

        If a value is not specified, returns the content
        of the Service Request Enable register.
        """

        if isinstance(value, int):
            if value not in range(256):
                raise ValueError(value)
            return self.client.write(f"*SRE {value}\n".encode())
        return self.client.write_readline(b"*SRE?\n")

    def stb(self) -> bytes:
        """Read Status Byte Query.

        Queries the condition register for the Status Byte
        Register group and returns a decimal value equal to
        the binary-weighted sum of all bits set in the
        register.

        A condition register continuously monitors the state
        of the instrument. Condition register bits are
        updated in real time; they are neither latched nor
        buffered.
        """

        return self.client.write_readline(b"*STB?\n")

    def trg(self) -> None:
        """Trigger Command.

        Triggers the instrument if TRIGger:SOURce BUS is
        selected.
        """

        return self.client.write("*TRG\n")

    def tst(self) -> bytes:
        """Self-Test Query.

        Performs a basic self-test of the instrument and
        returns a pass/fail indication. The TEST:ALL?
        self-test is more comprehensive than the *TST?
        self-test.

        Returns an integer value in the range of -32767
        and 32767. A response of 0 indicates that the
        self-test completed without errors detected.
        """

        return self.client.write_readline(b"*TST?\n")

    def wai(self) -> None:
        """Wait-to-Continue Command.

        Configures the instrument's output buffer to wait
        for all pending operations to complete before
        executing any additional commands over the
        interface.
        """

        return self.client.write(b"*WAI\n")
