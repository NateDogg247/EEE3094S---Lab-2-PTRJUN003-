function run_simulink_tests(P)
% Execute both explicitly defined reference tests in native Simulink.
% Requires MATLAB/Simulink. No generated result is claimed until this runs.
if nargin==0,P=lab_parameters();end
model=create_simulink_model(P);
target=fullfile(P.project_root,'results','matlab');
cases={'nominal',0,0,5;'supplied_reference',2.5,2.5,5};
for i=1:size(cases,1)
 name=cases{i,1};event=cases{i,2};before=cases{i,3};after=cases{i,4};
 set_param([model '/Reference_m'],'Time',num2str(event),...
  'Before',num2str(before),'After',num2str(after));
 result=sim(model,'ReturnWorkspaceOutputs','on');
 altitude=result.get('altitude_m');command=result.get('command_v');
 t=altitude.Time;y=altitude.Data(:);
 [commandTime,uniqueIndex]=unique(command.Time,'last');
 commandData=command.Data(:);
 u=interp1(commandTime,commandData(uniqueIndex),t,'linear');
 reference=before*ones(size(t));reference(t>=event)=after;
 trace=table(t,reference,y,u,'VariableNames',{'time_s','reference_m','altitude_m','command_V'});
 writetable(trace,fullfile(target,['simulink_' name '.csv']));
 f=figure('Color','w');layout=tiledlayout(2,1,'TileSpacing','compact');
 nexttile;plot(t,y,t,reference,'--');ylabel('Altitude (m)');grid on;
 nexttile;plot(t,u);xlabel('Simulation clock (s)');ylabel('Command (V)');grid on;
 exportgraphics(layout,fullfile(target,['simulink_' name '.pdf']),'ContentType','vector');
 exportgraphics(layout,fullfile(target,['simulink_' name '.png']),'Resolution',200);
end
% Restore and save the isolated nominal 0-to-5 m design model.
set_param([model '/Reference_m'],'Time','0','Before','0','After','5');
save_system(model);
end
