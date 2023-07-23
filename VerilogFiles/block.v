// This file contains the extracted FSM from urd_rx_fdec_controller module
// Created by : ESNIVIN

//`include "macros.v"

module urd_rx_fdec_controller_fsm(
									input clk,
									input rst_n,
									input rxf_lower_dav,
									input zero_payload,// Deal with this    assign zero_payload = current_job.len + 'd32 == current_job.offset;
									input processing_queue_slot_available,
									input processing_queue_slot_available_early,
									input current_job_data_available,
									input rxf_upper_dav,						// mapped
									input rxl_result_data_con_concatenate,
									input current_job_e,
									input current_job_e_pre_urd_error,
								    input current_job_e_size_error,
								    input current_job_e_hdr_error,
//								    input rxl_result_dav,			// mapped
								    input [7:0]rx_ev_inc_err,
								    input [7:0]rx_ev_oversize_ip,
								    input [7:0]rx_ev_eth_head_err,
								    output reg rxl_load_lower_and_trigger, 			// MAPPED
								    output reg rxl_load_upper,
								    output reg rxf_stop,
									output reg update_job_info_from_info_fifo,
									output reg trigger_write_fd_job_queue,
									output reg trigger_write_fd_job_queue_error_job
									);



  reg [1:0] rxf_flags, rxf_flags_d;			// Internal flags
 
  // states
  parameter newframe_wait = 3'd1,
  			frame_pl64 = 3'd2,
  			newconcat_wait = 3'd3,
  			frame_pl64_concat = 3'd4,
  			rxl_wait = 3'd5,
  			error_frame_hdr = 3'd6 ;
// state register
  reg [2:0] state, state_nxt;

  reg       trigger_pl64_read;
  reg       trigger_hdr_read;							// INTERNAL REGISTER
  reg       err_ind, err_ind_d;
  reg [7:0] err_id,  err_id_d;
  reg       check_err, check_err_nxt;

  reg trigger_pl64_read_immediate;

  reg  zero_payload_d;
	///Check mapping below
	// assign zero_payload = (current_job_len + 'd32 == current_job_offset);


/// Register updates:
  always @(posedge clk or negedge rst_n) begin
    if (rst_n == 1'b0) begin
      state                                <= newframe_wait;
      rxf_flags_d                          <= 2'b00;
      err_ind_d                            <= 1'b0;
      err_id_d                             <= {8{1'b0}};  
      check_err                            <= {8{1'b0}};
      zero_payload_d                       <= 1'b0;
    end else begin
      state                                <= state_nxt;
      rxf_flags_d                          <= rxf_flags;
      err_ind_d                            <= err_ind;
      err_id_d                             <= err_id;
      check_err                            <= check_err_nxt;
      zero_payload_d                       <= zero_payload;
    end
  end

// Combinational block

always@(*)
begin

    //
    // DEFAULT VALUES
    //
    trigger_pl64_read                              = 1'b0;
    trigger_pl64_read_immediate                    = 1'b0;
    trigger_hdr_read                               = 1'b0; // trigger readout of the ethernet header from rx fifo
    update_job_info_from_info_fifo                 = 1'b0;
    trigger_write_fd_job_queue                     = 1'b0;
    trigger_write_fd_job_queue_error_job           = 1'b0;
    rxf_flags                                      = rxf_flags_d;
    rxf_stop                                       = 1'b0;
    state_nxt                                      = state;
    err_ind                                        = 1'b0;
    err_id                                         = err_id_d;
    check_err_nxt                                  = 1'b0;
    rxl_load_lower_and_trigger                     = 1'b0;			// Mapped
    rxl_load_upper                                 = 1'b0;          // Mapped

    
    //
    // STATE MACHINE
    // CURRENT: store-and-forward support
    //
    case (state)
      // newframe_wait: see default case

	      error_frame_hdr: begin
	        if (rxf_lower_dav == 1'b1) begin				// input port

	          err_ind       = 1'b1;									// MAPPED
	          check_err_nxt = 1'b1;									// MAPPED
	          state_nxt     = newframe_wait;						// MAPPED
	        end
	      end

	      frame_pl64: begin
	        if (rxf_lower_dav == 1'b1) begin			// INPUT PORT
	          rxl_load_lower_and_trigger = 1'b1;
	        end
	        if (rxf_upper_dav == 1'b1) begin			// MAPPED
	          rxl_load_upper             = 1'b1;
	          trigger_hdr_read           = 1'b1;
	          state_nxt                  = rxl_wait;
	        end
	        if (zero_payload_d == 1'b1) begin				// Mapped. LOOK into assign statement below declaration
	          rxl_load_lower_and_trigger = 1'b1;
	          rxl_load_upper             = 1'b1;			// Mapped.
	          trigger_hdr_read           = 1'b1;			// Mapped
	          state_nxt                  = rxl_wait;
	        end
	      end



	      newconcat_wait: begin
	        if (check_err == 1'b1 && err_ind_d == 1'b1) begin
	          state_nxt                   = newframe_wait;
	        end else if (processing_queue_slot_available == 1'b1) begin		// LOOK above for details and map accordingly.
	          trigger_pl64_read_immediate = 1'b1;							// Mapped
	          state_nxt                   = frame_pl64_concat;
	        end
	      end

	      frame_pl64_concat: begin
	        if (check_err == 1'b1 && err_ind_d == 1'b1) begin
	          state_nxt                   = newframe_wait;
	          rxf_stop                    = 1'b1;
	        end else begin
	          if (rxf_lower_dav == 1'b1 || zero_payload_d == 1'b1) begin			// Deal with   assign zero_payload = current_job.len + 'd32 == current_job.offset;
	            rxl_load_lower_and_trigger = 1'b1;
	          end
	          if (rxf_upper_dav == 1'b1) begin
	            rxl_load_upper = 1'b1;
	            state_nxt = rxl_wait;
	          end
	        end
	      end

	      rxl_wait: 
	       begin
	        rxf_flags = 2'b00;
		     // Skipping complex data types struct.struct.struct !!!!!
	            trigger_write_fd_job_queue = 1'b1;					// MAPPED
	            check_err_nxt = 1'b1;								// MAPPED
	            if (rxl_result_data_con_concatenate == 0) begin						// rxl_result_data is a struct type. This is mapped into Verilog construct . Look into macros.v file for declarations
	              state_nxt = newframe_wait;
	            end else begin
	              if (processing_queue_slot_available_early == 1'b1) begin
	                trigger_pl64_read_immediate = 1'b1;				// MAPPED
	                state_nxt                   = frame_pl64_concat;
	              end else begin
	                state_nxt                   = newconcat_wait;
	              end
	            
	//          end
	        end
	      end

	      default: begin // newframe_wait
	        if (current_job_data_available == 1'b1 && processing_queue_slot_available == 1'b1) begin
	          update_job_info_from_info_fifo = 1'b1;						// Map
	          trigger_pl64_read     = 1'b1;
	          if (current_job_e == 1'b0) begin
	            state_nxt = frame_pl64;
	          end else if (current_job_e_pre_urd_error == 1'b1) begin				// derive vector size from struct defined
	            err_id           = rx_ev_inc_err;
	            trigger_hdr_read = 1'b1;
	            state_nxt        = error_frame_hdr;
	          end else if (current_job_e_size_error == 1'b1) begin
	            err_id           = rx_ev_oversize_ip;
	            trigger_hdr_read = 1'b1;
	            state_nxt        = error_frame_hdr;
	          end else if (current_job_e_hdr_error == 1'b1) begin
	            err_id           = rx_ev_eth_head_err;				// rx_ev_eth_head_err Where is this??
	            trigger_hdr_read = 1'b1;
	            state_nxt        = error_frame_hdr;
	          end
	        end
	      end
	    endcase
	    end
 endmodule