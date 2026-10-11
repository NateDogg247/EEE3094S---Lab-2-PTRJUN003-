% Launch the original independent controller check.
clear; close all; clc;
addpath(genpath(fileparts(mfilename('fullpath'))));
verify_nominal_controller(lab_parameters());
