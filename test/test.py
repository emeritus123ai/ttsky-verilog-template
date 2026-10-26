
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

@cocotb.test()
async def test_guardian(dut):
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    cocotb.start_soon(Clock(dut.clk, 10, unit="us").start())

    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)
    await Timer(1, unit="ns")

    # IDLE
    assert int(dut.uo_out.value) & 15 == 4

    # Activate
    dut.ui_in.value = 2
    await ClockCycles(dut.clk, 2)
    await Timer(1, unit="ns")
    assert int(dut.uo_out.value) & 15 == 9

    # Fault immediately disables active_out
    dut.ui_in.value = 1
    await Timer(1, unit="ns")
    assert int(dut.uo_out.value) & 1 == 0

    # Enter protection latch
    await ClockCycles(dut.clk, 2)
    await Timer(1, unit="ns")
    assert int(dut.uo_out.value) & 15 == 14

    # Latch remains active after fault clears
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 2)
    await Timer(1, unit="ns")
    assert int(dut.uo_out.value) & 15 == 14
