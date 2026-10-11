% Launch the Simulink model builder; no DAQ hardware is required.
clear; clc;
addpath(genpath(fileparts(mfilename('fullpath'))));
model = create_simulink_model(lab_parameters());
