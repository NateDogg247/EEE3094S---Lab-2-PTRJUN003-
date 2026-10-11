% Run the detailed root locus method. Requires Control System Toolbox.
clear; close all; clc;
addpath(genpath(fileparts(mfilename('fullpath'))));
P = lab_parameters();
root_locus_result = run_root_locus_design(P);
