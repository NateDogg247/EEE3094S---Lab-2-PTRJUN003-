function model = create_simulink_model(P)
% Reconstruct the nominal architecture; requires Simulink.
model='PTRJUN003_Kitticopter_Lab2';
if bdIsLoaded(model), close_system(model,0); end
new_system(model); open_system(model);
set_param(model,'StopTime','160','Solver','ode45','MaxStep','0.02',...
    'RelTol','1e-8','AbsTol','1e-10');
add_block('simulink/Sources/Step',[model '/Reference_m'],...
 'Time','0','Before','0','After',num2str(P.reference_step_m),'Position',[25 65 55 95]);
add_block('simulink/Math Operations/Gain',[model '/ReferenceSensorGain'],...
 'Gain',num2str(P.sensor_gain_V_per_m),'Position',[95 60 145 100]);
add_block('simulink/Math Operations/Sum',[model '/VoltageError'],...
 'Inputs','+-','Position',[190 65 215 95]);
add_block('simulink/Math Operations/Gain',[model '/Kp'],...
 'Gain',num2str(P.controller_gain),'Position',[255 60 310 100]);
add_block('simulink/Math Operations/Sum',[model '/AddHover'],...
 'Inputs','++','Position',[355 65 380 95]);
add_block('simulink/Sources/Constant',[model '/Hover'],...
 'Value',num2str(P.hover_command_V),'Position',[310 175 345 205]);
add_block('simulink/Discontinuities/Saturation',[model '/ActuatorLimits'],...
 'UpperLimit','5','LowerLimit','0','Position',[420 60 465 100]);
add_block('simulink/Math Operations/Sum',[model '/SubtractHover'],...
 'Inputs','+-','Position',[505 65 530 95]);
add_block('simulink/Continuous/Transfer Fcn',[model '/VelocityPlant'],...
 'Numerator',num2str(P.A),'Denominator',mat2str([P.tau_s 1]),...
 'Position',[565 60 655 100]);
add_block('simulink/Continuous/Integrator',[model '/Position'],...
 'InitialCondition','0','Position',[695 60 730 100]);
add_block('simulink/Math Operations/Gain',[model '/SensorGain'],...
 'Gain',num2str(P.sensor_gain_V_per_m),'Position',[565 280 620 315]);
add_block('simulink/Discontinuities/Saturation',[model '/SensorLimits'],...
 'UpperLimit','10','LowerLimit','0','Position',[430 280 475 315]);
set_param([model '/SensorGain'],'Orientation','left');
set_param([model '/SensorLimits'],'Orientation','left');
add_block('simulink/Sinks/To Workspace',[model '/OutputLog'],...
 'VariableName','altitude_m','SaveFormat','Timeseries','Position',[785 55 885 90]);
add_block('simulink/Sinks/To Workspace',[model '/CommandLog'],...
 'VariableName','command_v','SaveFormat','Timeseries','Position',[475 170 575 205]);
add_block('simulink/Sinks/Scope',[model '/Scope'],...
 'NumInputPorts','3','Position',[915 110 960 190]);
connections={ 'Reference_m/1','ReferenceSensorGain/1';
 'ReferenceSensorGain/1','VoltageError/1';
 'VoltageError/1','Kp/1'; 'Kp/1','AddHover/1';
 'Hover/1','AddHover/2'; 'AddHover/1','ActuatorLimits/1';
 'ActuatorLimits/1','SubtractHover/1'; 'Hover/1','SubtractHover/2';
 'SubtractHover/1','VelocityPlant/1'; 'VelocityPlant/1','Position/1';
 'Position/1','SensorGain/1'; 'SensorGain/1','SensorLimits/1';
 'SensorLimits/1','VoltageError/2'; 'Position/1','OutputLog/1';
 'ActuatorLimits/1','CommandLog/1';'Reference_m/1','Scope/1';
 'Position/1','Scope/2'; 'ActuatorLimits/1','Scope/3'};
for i=1:size(connections,1)
 add_line(model,connections{i,1},connections{i,2},'autorouting','on');
end
target=fullfile(P.project_root,'results','matlab');
if ~exist(target,'dir'), mkdir(target); end
save_system(model,fullfile(target,[model '.slx']));
disp('Model saved. Run sim(model) to generate logged nominal response.');

end
