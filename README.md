# MasterThesis
repo contains code for Framework for Automatic Generation of Assertion


# Behavioral description of "test_code.v"

  ## if reset = 1 then data_out = 0
  
  ## if reset = 0 then data_out is dependent on the current state based on the table below:
  
    |current_state| data_out|
    |-------------|---------|
    |S0           | 0       |
    |S1           | 1       |
    |S2           | 0       |
    |S3           | 1       |
