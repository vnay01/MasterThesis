/////////////////////////////////////////////////////////////////////
////                                                             ////
////  Internal DMA Engine                                        ////
////                                                             ////
////                                                             ////
////  Author: Rudolf Usselmann                                   ////
////          rudi@asics.ws                                      ////
////                                                             ////
////                                                             ////
////  Downloaded from: http://www.opencores.org/cores/usb/       ////
////                                                             ////
/////////////////////////////////////////////////////////////////////
////                                                             ////
//// Copyright (C) 2000-2003 Rudolf Usselmann                    ////
////                         www.asics.ws                        ////
////                         rudi@asics.ws                       ////
////                                                             ////
//// This source file may be used and distributed without        ////
//// restriction provided that this copyright statement is not   ////
//// removed from the file and that any derivative work contains ////
//// the original copyright notice and the associated disclaimer.////
////                                                             ////
////     THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY     ////
//// EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED   ////
//// TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS   ////
//// FOR A PARTICULAR PURPOSE. IN NO EVENT SHALL THE AUTHOR      ////
//// OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,         ////
//// INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES    ////
//// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE   ////
//// GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR        ////
//// BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF  ////
//// LIABILITY, WHETHER IN  CONTRACT, STRICT LIABILITY, OR TORT  ////
//// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT  ////
//// OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         ////
//// POSSIBILITY OF SUCH DAMAGE.                                 ////
////                                                             ////
/////////////////////////////////////////////////////////////////////

//  CVS Log
//
//  $Id: usbf_idma.v,v 1.8 2003-10-17 02:36:57 rudi Exp $
//
//  $Date: 2003-10-17 02:36:57 $
//  $Revision: 1.8 $
//  $Author: rudi $
//  $Locker:  $
//  $State: Exp $
//
// Change History:
//               $Log: not supported by cvs2svn $
//               Revision 1.7  2001/11/04 12:22:45  rudi
//
//               - Fixed previous fix (brocke something else ...)
//               - Majore Synthesis cleanup
//
//               Revision 1.6  2001/11/03 03:26:22  rudi
//
//               - Fixed several interrupt and error condition reporting bugs
//
//               Revision 1.5  2001/09/24 01:15:28  rudi
//
//               Changed reset to be active high async.
//
//               Revision 1.4  2001/09/23 08:39:33  rudi
//
//               Renamed DEBUG and VERBOSE_DEBUG to USBF_DEBUG and USBF_VERBOSE_DEBUG ...
//
//               Revision 1.3  2001/09/19 14:38:57  rudi
//
//               Fixed TxValid handling bug.
//
//               Revision 1.2  2001/09/13 13:14:02  rudi
//
//               Fixed a problem that would sometimes prevent the core to come out of
//               reset and immediately be operational ...
//
//               Revision 1.1  2001/08/03 05:30:09  rudi
//
//
//               1) Reorganized directory structure
//
//               Revision 1.2  2001/03/31 13:00:51  rudi
//
//               - Added Core configuration
//               - Added handling of OUT packets less than MAX_PL_SZ in DMA mode
//               - Modified WISHBONE interface and sync logic
//               - Moved SSRAM outside the core (added interface)
//               - Many small bug fixes ...
//
//               Revision 1.0  2001/03/07 09:17:12  rudi
//
//
//               Changed all revisions to revision 1.0. This is because OpenCores CVS
//               interface could not handle the original '0.1' revision ....
//
//               Revision 0.1.0.1  2001/02/28 08:10:50  rudi
//               Initial Release
//
//                            

// `include "usbf_defines.v"


/////////////////////////////////////////////////////////////////////
////                                                             ////
////  USB function defines file                                  ////
////                                                             ////
////                                                             ////
////  Author: Rudolf Usselmann                                   ////
////          rudi@asics.ws                                      ////
////                                                             ////
////                                                             ////
////  Downloaded from: http://www.opencores.org/cores/usb/       ////
////                                                             ////
/////////////////////////////////////////////////////////////////////
////                                                             ////
//// Copyright (C) 2000-2003 Rudolf Usselmann                    ////
////                         www.asics.ws                        ////
////                         rudi@asics.ws                       ////
////                                                             ////
//// This source file may be used and distributed without        ////
//// restriction provided that this copyright statement is not   ////
//// removed from the file and that any derivative work contains ////
//// the original copyright notice and the associated disclaimer.////
////                                                             ////
////     THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY     ////
//// EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED   ////
//// TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS   ////
//// FOR A PARTICULAR PURPOSE. IN NO EVENT SHALL THE AUTHOR      ////
//// OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,         ////
//// INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES    ////
//// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE   ////
//// GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR        ////
//// BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF  ////
//// LIABILITY, WHETHER IN  CONTRACT, STRICT LIABILITY, OR TORT  ////
//// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT  ////
//// OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         ////
//// POSSIBILITY OF SUCH DAMAGE.                                 ////
////                                                             ////
/////////////////////////////////////////////////////////////////////

//  CVS Log
//
//  $Id: usbf_defines.v,v 1.6 2003-10-17 02:36:57 rudi Exp $
//
//  $Date: 2003-10-17 02:36:57 $
//  $Revision: 1.6 $
//  $Author: rudi $
//  $Locker:  $
//  $State: Exp $
//
// Change History:
//               $Log: not supported by cvs2svn $
//               Revision 1.5  2001/11/04 12:22:43  rudi
//
//               - Fixed previous fix (brocke something else ...)
//               - Majore Synthesis cleanup
//
//               Revision 1.4  2001/09/23 08:39:33  rudi
//
//               Renamed DEBUG and VERBOSE_DEBUG to USBF_DEBUG and USBF_VERBOSE_DEBUG ...
//
//               Revision 1.3  2001/09/13 13:14:02  rudi
//
//               Fixed a problem that would sometimes prevent the core to come out of
//               reset and immediately be operational ...
//
//               Revision 1.2  2001/08/10 08:48:33  rudi
//
//               - Changed IO names to be more clear.
//               - Uniquifyed define names to be core specific.
//
//               Revision 1.1  2001/08/03 05:30:09  rudi
//
//
//               1) Reorganized directory structure
//
//               Revision 1.2  2001/03/31 13:00:52  rudi
//
//               - Added Core configuration
//               - Added handling of OUT packets less than MAX_PL_SZ in DMA mode
//               - Modified WISHBONE interface and sync logic
//               - Moved SSRAM outside the core (added interface)
//               - Many small bug fixes ...
//
//               Revision 1.0  2001/03/07 09:17:12  rudi
//
//
//               Changed all revisions to revision 1.0. This is because OpenCores CVS
//               interface could not handle the original '0.1' revision ....
//
//               Revision 0.2  2001/03/07 09:08:13  rudi
//
//               Added USB control signaling (Line Status) block. Fixed some minor
//               typos, added resume bit and signal.
//
//               Revision 0.1.0.1  2001/02/28 08:11:35  rudi
//               Initial Release
//
//

`timescale 1ns / 10ps

// Uncomment the lines below to get various levels of debugging
// verbosity ...
//`define USBF_DEBUG
//`define USBF_VERBOSE_DEBUG

// Uncomment the line below to run the test bench
// Comment it out to use your own address parameters ...
//`define USBF_TEST_IMPL

// For each endpoint that should actually be instantiated,
// set the below define value to a one. Uncomment the define
// statement for unused endpoints. The endpoints should be
// sequential, e.q. 1,2,3. I have not tested what happens if
// you select endpoints in a non sequential manner e.g. 1,4,6
// Actual (logical) endpoint IDs are set by the software. There
// is no correlation between the physical endpoint number (below)
// and the actual (logical) endpoint number.
// `ifdef USBF_TEST_IMPL
// 		// Do not modify this section
// 		// this is to run the test bench
// 		`define	USBF_HAVE_EP1	1
// 		`define	USBF_HAVE_EP2	1
// 		`define	USBF_HAVE_EP3	1
// `else
// 		// Modify this section to suit your implementation
// 		`define	USBF_HAVE_EP1	1
// 		`define	USBF_HAVE_EP2	1
// 		`define	USBF_HAVE_EP3	1
// 		//`define	USBF_HAVE_EP4	1
// 		//`define	USBF_HAVE_EP5	1
// 		//`define	USBF_HAVE_EP6	1
// 		//`define	USBF_HAVE_EP7	1
// 		//`define	USBF_HAVE_EP8	1
// 		//`define	USBF_HAVE_EP9	1
// 		//`define	USBF_HAVE_EP10	1
// 		//`define	USBF_HAVE_EP11	1
// 		//`define	USBF_HAVE_EP12	1
// 		//`define	USBF_HAVE_EP13	1
// 		//`define	USBF_HAVE_EP14	1
// 		//`define	USBF_HAVE_EP15	1
// `endif


// Highest address line number that goes to the USB core
// Typically only A0 through A17 are needed, where A17
// selects between the internal buffer memory and the
// register file.
// Implementations may choose to have a more complex address
// decoding ....

// `ifdef USBF_TEST_IMPL
// 		// Do not modify this section
// 		// this is to run the test bench
// 		`define USBF_UFC_HADR	17
// 		`define USBF_RF_SEL	(!wb_addr_i[17])
// 		`define USBF_MEM_SEL	(wb_addr_i[17])
// 		`define USBF_SSRAM_HADR	14
// 		//`define USBF_ASYNC_RESET
// 
// `else
// 		// Modify this section to suit your implementation
// 		`define USBF_UFC_HADR	12
// 		// Address Decoding for Register File select
// 		`define USBF_RF_SEL	(!wb_addr_i[12])
// 		// Address Decoding for Buffer Memory select
// 		`define USBF_MEM_SEL	(wb_addr_i[12])
// 		`define USBF_SSRAM_HADR	9
// 		// The next statement determines if reset is async or sync.
// 		// If the define is uncommented the reset will be ASYNC.
// 		//`define USBF_ASYNC_RESET
// `endif
// 

/////////////////////////////////////////////////////////////////////
//
// Items below this point should NOT be modified by the end user
// UNLESS you know exactly what you are doing !
// Modify at you own risk !!!
//
/////////////////////////////////////////////////////////////////////

//// PID Encodings
//`define USBF_T_PID_OUT		4'b0001
//`define USBF_T_PID_IN		4'b1001
//`define USBF_T_PID_SOF		4'b0101
//`define USBF_T_PID_SETUP	4'b1101
//`define USBF_T_PID_DATA0	4'b0011
//`define USBF_T_PID_DATA1	4'b1011
//`define USBF_T_PID_DATA2	4'b0111
//`define USBF_T_PID_MDATA	4'b1111
//`define USBF_T_PID_ACK		4'b0010
//`define USBF_T_PID_NACK		4'b1010
//`define USBF_T_PID_STALL	4'b1110
//`define USBF_T_PID_NYET		4'b0110
//`define USBF_T_PID_PRE		4'b1100
//`define USBF_T_PID_ERR		4'b1100
//`define USBF_T_PID_SPLIT	4'b1000
//`define USBF_T_PID_PING		4'b0100
//`define USBF_T_PID_RES		4'b0000
//
//// The HMS_DEL is a constant for the "Half Micro Second"
//// Clock pulse generator. This constant specifies how many
//// Phy clocks there are between two hms_clock pulses. This
//// constant plus 2 represents the actual delay.
//// Example: For a 60 Mhz (16.667 nS period) Phy Clock, the
//// delay must be 30 phy clocks: 500ns / 16.667nS = 30 clocks
//`define USBF_HMS_DEL		5'h1c
//
//// After sending Data in response to an IN token from host, the
//// host must reply with an ack. The host has 622nS in Full Speed
//// mode and 400nS in High Speed mode to reply. RX_ACK_TO_VAL_FS
//// and RX_ACK_TO_VAL_HS are the numbers of UTMI clock cycles
//// minus 2 for Full and High Speed modes.
//`define USBF_RX_ACK_TO_VAL_FS	8'd36
//`define USBF_RX_ACK_TO_VAL_HS	8'd22
//
//
//// After sending an OUT token the host must send a data packet.
//// The host has 622nS in Full Speed mode and 400nS in High Speed
//// mode to send the data packet.
//// TX_DATA_TO_VAL_FS and TX_DATA_TO_VAL_HS are is the numbers of
//// UTMI clock cycles minus 2.
//`define USBF_TX_DATA_TO_VAL_FS	8'd36
//`define USBF_TX_DATA_TO_VAL_HS	8'd22
//
//
//// --------------------------------------------------
//// USB Line state & Speed Negotiation Time Values
//
//
// Prescaler Clear value.
// The prescaler generates a 0.25uS pulse, from a nominal PHY clock of
// 60 Mhz. 250nS/16.667ns=15. The prescaler has to be cleared every 15
// cycles. Due to the pipeline, subtract 2 from 15, resulting in 13 cycles.
// !!! This is the only place that needs to be changed if a PHY with different
// // !!! clock output is used.
// `define	USBF_T1_PS_250_NS	4'd13
// 
// // uS counter representation of 2.5uS (2.5/0.25=10)
// `define	USBF_T1_C_2_5_US	8'd10
// 
// // uS counter clear value
// // The uS counter counts the time in 0.25uS intervals. It also generates
// // a count enable to the mS counter, every 62.5 uS.
// // The clear value is 62.5uS/0.25uS=250 cycles.
// `define USBF_T1_C_62_5_US	8'd250
// 
// // mS counter representation of 3.0mS (3.0/0.0625=48)
// `define USBF_T1_C_3_0_MS	8'd48
// 
// // mS counter representation of 3.125mS (3.125/0.0625=50)
// `define USBF_T1_C_3_125_MS	8'd50
// 
// // mS counter representation of 5mS (5/0.0625=80)
// `define USBF_T1_C_5_MS		8'd80
// 
// // Multi purpose Counter Prescaler, generate 2.5 uS period
// // 2500/16.667ns=150 (minus 2 for pipeline)
// `define	USBF_T2_C_2_5_US	8'd148
// 
// // Generate 0.5mS period from the 2.5 uS clock
// // 500/2.5 = 200
// `define	USBF_T2_C_0_5_MS	8'd200
// 
// // Indicate when internal wakeup has completed
// // me_cnt counts 0.5 mS intervals. E.g.: 5.0mS are (5/0.5) 10 ticks
// // Must be 0 =< 10 mS
// `define USBF_T2_C_WAKEUP	8'd10
// 
// // Indicate when 100uS have passed
// // me_ps2 counts 2.5uS intervals. 100uS are (100/2.5) 40 ticks
// `define USBF_T2_C_100_US	8'd40
// 
// // Indicate when 1.0 mS have passed
// // me_cnt counts 0.5 mS intervals. 1.0mS are (1/0.5) 2 ticks
// `define USBF_T2_C_1_0_MS	8'd2
// 
// // Indicate when 1.2 mS have passed
// // me_cnt counts 0.5 mS intervals. 1.2mS are (1.2/0.5) 2 ticks
// `define USBF_T2_C_1_2_MS	8'd2
// 
// // Indicate when 100 mS have passed
// // me_cnt counts 0.5 mS intervals. 100mS are (100/0.5) 200 ticks
// // `define USBF_T2_C_100_MS	8'd200



module usbf_idma(	clk, rst,

		// Packet Disassembler/Assembler interface
		rx_data_st, rx_data_valid, rx_data_done, 
		send_data, tx_data_st, rd_next,

		// Protocol Engine
		rx_dma_en, tx_dma_en,
		abort, idma_done,
		buf_size, dma_en,
		send_zero_length,

		// Register File Manager Interface
		adr, size, sizu_c,

		// Memory Arb interface
		madr, mdout, mdin, mwe, mreq, mack
		);

parameter	SSRAM_HADR = 14;

// Packet Disassembler/Assembler interface
input		clk, rst;
input	[7:0]	rx_data_st;
input		rx_data_valid;
input		rx_data_done;
output		send_data;
output	[7:0]	tx_data_st;
input		rd_next;

// Protocol Engine
input		rx_dma_en;	// Allows the data to be stored
input		tx_dma_en;	// Allows for data to be retrieved
input		abort;		// Abort Transfer (time_out, crc_err or rx_error)
output		idma_done;	// DMA is done
input	[13:0]	buf_size;	// Actual buffer size
input		dma_en;		// External DMA enabled
input		send_zero_length;

// Register File Manager Interface
input	[SSRAM_HADR + 2:0]	adr;	// Byte Address
input	[13:0]	size;		// Size in bytes
output	[10:0]	sizu_c;		// Up and Down counting size registers, used to update

// Memory Arb interface
output	[SSRAM_HADR:0]	madr;	// word address
output	[31:0]	mdout;
input	[31:0]	mdin;
output		mwe;
output		mreq;
input		mack;

///////////////////////////////////////////////////////////////////
//
// Local Wires and Registers
//

parameter	[7:0]	// synopsys enum state
		IDLE		= 8'b00000001,
		WAIT_MRD	= 8'b00000010,
		MEM_WR		= 8'b00000100,
		MEM_WR1		= 8'b00001000,
		MEM_WR2		= 8'b00010000,
		MEM_RD1		= 8'b00100000,
		MEM_RD2		= 8'b01000000,
		MEM_RD3		= 8'b10000000;

reg	[7:0]	/* synopsys enum state */ state, next_state;
// synopsys state_vector state

reg		tx_dma_en_r, rx_dma_en_r;

reg	[SSRAM_HADR:0]	adr_cw;		// Internal word address counter
reg	[2:0]	adr_cb;			// Internal byte address counter
reg	[SSRAM_HADR:0]	adrw_next;	// next address
reg	[SSRAM_HADR:0]	adrw_next1;	// next address (after overrun check)
reg	[SSRAM_HADR:0]	last_buf_adr;	// Last Buffer Address
reg	[2:0]	adrb_next;		// next byte address
reg	[13:0]	sizd_c;			// Internal size counter
reg	[10:0]	sizu_c;			// Internal size counter
wire		adr_incw;
wire		adr_incb;
wire		siz_dec;
wire		siz_inc;

reg		word_done;		// Indicates that a word has been
					// assembled
reg		mreq_d;			// Memory request from State Machine
reg	[31:0]	dtmp_r;			// Temp data assembly register
reg	[31:0]	dout_r;			// Data output register
reg		mwe_d;			// Memory Write enable
reg		dtmp_sel;		// Selects tmp data register for pre-fetch

reg		sizd_is_zero;		// Indicates when all bytes have been
					// transferred
wire		sizd_is_zero_d;

reg	[7:0]	tx_data_st;		// Data output to packet assembler
reg	[31:0]	rd_buf0, rd_buf1;	// Mem Rd. buffers for TX
reg		rd_first;		// Indicates initial fill of buffers

reg		idma_done;		// DMA transfer is done

reg		mack_r;
wire		send_data;		// Enable UTMI Transmitter
reg		send_data_r;

reg		word_done_r;
reg		wr_last;
reg		wr_last_en;
reg		wr_done;
reg		wr_done_r;
reg		dtmp_sel_r;
reg		mwe;
reg		rx_data_done_r2;
wire		fill_buf0, fill_buf1;
wire		adrb_is_3;

reg		rx_data_done_r;
reg		rx_data_valid_r;
reg	[7:0]	rx_data_st_r;

reg		send_zero_length_r;

///////////////////////////////////////////////////////////////////
//
// Memory Arb interface
//

// Memory Request
assign mreq = (mreq_d & !mack_r) | word_done_r;

// Output Data
assign mdout = dout_r;

// Memory Address
assign madr = adr_cw;

always@(posedge clk)
	mwe <= mwe_d;

always@(posedge clk)
	mack_r <= mreq & mack;

///////////////////////////////////////////////////////////////////
//
// Misc Logic
//

always@(posedge clk)
	rx_data_valid_r <= rx_data_valid;

always@(posedge clk)
	rx_data_st_r <= rx_data_st;

always@(posedge clk)
	rx_data_done_r <= rx_data_done;

always@(posedge clk)
	rx_data_done_r2 <= rx_data_done_r;

// Generate one cycle pulses for tx and rx dma enable
always@(posedge clk)
	tx_dma_en_r <= tx_dma_en;

always@(posedge clk)
	rx_dma_en_r <= rx_dma_en;

always@(posedge clk)
	send_zero_length_r <= send_zero_length;

// address counter
always@(posedge clk)
	if(rx_dma_en_r || tx_dma_en_r)	adr_cw <= adr[SSRAM_HADR + 2:2];
	else				adr_cw <= adrw_next1;

always@(posedge clk)
	last_buf_adr <= adr + { {SSRAM_HADR+2-13{1'b0}}, buf_size };

always@(dma_en or adrw_next or last_buf_adr)
	if(adrw_next == last_buf_adr && dma_en)	adrw_next1 = {SSRAM_HADR+1{1'b0}};
	else					adrw_next1 = adrw_next;

always@(adr_incw or adr_cw)
	if(adr_incw)	adrw_next = adr_cw + {{SSRAM_HADR{1'b0}}, 1'b1};
	else		adrw_next = adr_cw;


always@(posedge clk)
	if(!rst)			adr_cb <= 3'h0;
	else
	if(rx_dma_en_r || tx_dma_en_r)	adr_cb <= adr[2:0];
	else				adr_cb <= adrb_next;

always@(adr_incb or adr_cb)
	if(adr_incb)	adrb_next = adr_cb + 3'h1;
	else		adrb_next = adr_cb;

assign adr_incb = rx_data_valid_r | rd_next;
assign adr_incw = !dtmp_sel_r & mack_r;

// Size Counter (counting backward from input size)

always@(posedge clk)
	if(!rst)			sizd_c <= 14'h3fff;
	else
	if(tx_dma_en || tx_dma_en_r)	sizd_c <= size;
	else
	if(siz_dec)			sizd_c <= sizd_c - 14'h1;

assign siz_dec = (rd_first & mack_r) | (rd_next & (sizd_c != 14'h0));

assign sizd_is_zero_d = sizd_c == 14'h0;

always@(posedge clk)
	sizd_is_zero <= sizd_is_zero_d;

// Size Counter (counting up from zero)
always@(posedge clk)
	if(!rst)		sizu_c <= 11'h0;
	else
	// Do I need to add "abort" in the next line ???
	if(rx_dma_en_r)		sizu_c <= 11'h0;
	else
	if(siz_inc)		sizu_c <= sizu_c + 11'h1;

assign siz_inc = rx_data_valid_r;

// DMA Done Indicator
always@(posedge clk)
	idma_done <= (rx_data_done_r | sizd_is_zero_d); // & !tx_dma_en;

///////////////////////////////////////////////////////////////////
//
// RX Logic
//

always@(posedge clk)
	dtmp_sel_r <= dtmp_sel;

// Memory data input
always@(posedge clk)
	if(dtmp_sel_r)			dtmp_r <= mdin;
	else
	if(rx_data_valid_r)
	   begin
		if(adr_cb[1:0] == 2'h0)	dtmp_r[07:00] <= rx_data_st_r;
		if(adr_cb[1:0] == 2'h1)	dtmp_r[15:08] <= rx_data_st_r;
		if(adr_cb[1:0] == 2'h2)	dtmp_r[23:16] <= rx_data_st_r;
		if(adr_cb[1:0] == 2'h3)	dtmp_r[31:24] <= rx_data_st_r;
	   end

always@(posedge clk)
	word_done <= ((adr_cb[1:0] == 2'h3) & rx_data_valid_r) | wr_last;

always@(posedge clk)
	word_done_r <= word_done & !word_done_r;

// Store output data and address when we got a word
always@(posedge clk)
	if(word_done)	dout_r <= dtmp_r;

always@(posedge clk)
	wr_last <= (adr_cb[1:0] != 2'h0) & !rx_data_valid_r & wr_last_en;

always@(posedge clk)
	wr_done_r <= rx_data_done_r;

always@(posedge clk)
	wr_done <= wr_done_r;

///////////////////////////////////////////////////////////////////
//
// TX Logic
//

// Fill TX Buffers
always@(posedge clk)
	if(fill_buf0)	rd_buf0 <= mdin;

always@(posedge clk)
	if(fill_buf1)	rd_buf1 <= mdin;

always@(adrb_next or rd_buf0 or rd_buf1)
	case(adrb_next[2:0])	// synopsys full_case parallel_case
	   3'h0: tx_data_st = rd_buf0[07:00];
	   3'h1: tx_data_st = rd_buf0[15:08];
	   3'h2: tx_data_st = rd_buf0[23:16];
	   3'h3: tx_data_st = rd_buf0[31:24];
	   3'h4: tx_data_st = rd_buf1[07:00];
	   3'h5: tx_data_st = rd_buf1[15:08];
	   3'h6: tx_data_st = rd_buf1[23:16];
	   3'h7: tx_data_st = rd_buf1[31:24];
	endcase

assign fill_buf0 = !adr_cw[0] & mack_r;
assign fill_buf1 =  adr_cw[0] & mack_r;

assign	adrb_is_3 = adr_cb[1:0] == 2'h3;

always@(posedge clk)
	if(!rst)		send_data_r <= 1'b0;
	else
	if(rd_first)		send_data_r <= 1'b1;
	else
	if(((sizd_c==14'h1) && rd_next) || sizd_is_zero_d)	send_data_r <= 1'b0;

assign send_data = send_data_r | send_zero_length_r;

///////////////////////////////////////////////////////////////////
//
// IDMA Load/Store State Machine
//

// store incoming data to memory until rx_data done
// First pre-fetch data from memory, so that bytes can be stuffed properly

always@(posedge clk)
	if(!rst)	state <= IDLE;
	else		state <= next_state;

always@(state or mack_r or abort or rx_dma_en_r or tx_dma_en_r or 
	sizd_is_zero or wr_last or wr_done or rx_data_done_r2 or 
	rd_next or adrb_is_3 or send_zero_length_r)
   begin
	next_state = state;	// Default do not change state
	mreq_d = 1'b0;
	mwe_d = 1'b0;
	rd_first = 1'b0;
	dtmp_sel = 1'b0;
	wr_last_en = 1'b0;

	case(state)	// synopsys full_case parallel_case
	   IDLE:
		   begin
// synopsys translate_on

			if(rx_dma_en_r && !abort)
			   begin
				next_state = WAIT_MRD;
			   end
			if(tx_dma_en_r && !abort && !send_zero_length_r)
			   begin
				next_state = MEM_RD1;
			   end
		   end

	   WAIT_MRD:	// Pre-fetch a word from memory
		   begin
			if(abort)	next_state = IDLE;
			else
			if(mack_r)	next_state = MEM_WR;
			else
			   begin
				dtmp_sel = 1'b1;
				mreq_d = 1'b1;
			   end
		   end

	   MEM_WR:
		   begin
			mwe_d = 1'b1;
			if(abort)			next_state = IDLE;
			else
			if(rx_data_done_r2)	
			   begin
				wr_last_en = 1'b1;
				next_state = MEM_WR1;
			   end

		   end
	   MEM_WR1:
		   begin

			mwe_d = 1'b1;
			wr_last_en = 1'b1;
			if(abort)			next_state = IDLE;
			else
			if(wr_last)			next_state = MEM_WR2;
			else
			if(wr_done)			next_state = IDLE;
		   end

	   MEM_WR2:
		   begin
			mwe_d = 1'b1;
			if(mack_r)			next_state = IDLE;
		   end

	   MEM_RD1:
		   begin
			mreq_d = 1'b1;
			if(mack_r)		rd_first = 1'b1;
			if(abort)		next_state = IDLE;
			else
			if(mack_r)		next_state = MEM_RD2;
		   end
	   MEM_RD2:
		   begin

			mreq_d = 1'b1;
			if(abort)		next_state = IDLE;
			else
			if(mack_r)		next_state = MEM_RD3;
		   end
	   MEM_RD3:
		   begin

			if(sizd_is_zero || abort)	next_state = IDLE;
			else
			if(adrb_is_3 && rd_next)	next_state = MEM_RD2;
		   end
	endcase

   end

endmodule

