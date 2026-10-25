
`default_nettype none

module tt_um_guardian_m2n_bb05 (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    wire [1:0] guardian_state;
    wire active_signal;
    wire fault_signal;

    guardian_fsm core (
        .clk(clk),
        .rst(~rst_n),
        .fault_in(ui_in[0]),
        .activate_in(ui_in[1]),
        .stop_in(ui_in[2]),
        .state(guardian_state),
        .active_out(active_signal),
        .fault_out(fault_signal)
    );

    assign uo_out = {
        4'b0000,
        guardian_state,
        fault_signal,
        active_signal
    };

    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    wire _unused = &{
        ena, ui_in[7:3], uio_in, 1'b0
    };

endmodule

`default_nettype wire

// Paste your existing guardian_fsm module below.
