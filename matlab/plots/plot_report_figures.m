function plot_report_figures(P)
% MATLAB counterparts of every Python numerical figure used in the report.
% Exports native MATLAB figures to results/matlab/figures as PDF and PNG.
% Pure analytical nominal responses avoid a Control System Toolbox dependency.
% Image-derived traces are read from separately labelled digitisation CSVs;
% they are not relabelled as original Simulink logs or instrument samples.
if nargin==0, P=lab_parameters(); end
target=fullfile(P.project_root,'results','matlab','figures');
if ~exist(target,'dir'), mkdir(target); end
set(groot,'defaultAxesFontName','Times New Roman','defaultAxesFontSize',11,...
 'defaultLineLineWidth',1.4,'defaultFigureColor','w');
C=[0.314 0.561 0.675;0.824 0.416 0.157;0.184 0.482 0.384];
raw=readmatrix(fullfile(P.project_root,'data','session1','PTRJUN003_raw.csv'));
reset=find(diff(raw(:,1))<0,1,'last');
if ~isempty(reset), raw=raw(reset+1:end,:); end
t=raw(:,1);u=raw(:,2);sv=raw(:,3);y=raw(:,4);v=[NaN;diff(y)./diff(t)];
t0=15.91583783;age=max(t-t0,0);
vm=P.identification_step_V*P.A*(1-exp(-age/P.tau_s));
ym=P.identification_step_V*P.A*(age-P.tau_s*(1-exp(-age/P.tau_s)));
f=figure('Visible','off');tiledlayout(3,1,'TileSpacing','compact');
nexttile;plot(t,u,'Color',C(1,:));ylabel('Command (V)');grid on;
nexttile;plot(t,y,'Color',C(1,:));ylabel('Altitude (m)');grid on;
nexttile;plot(t,sv,'Color',C(2,:));ylabel('Sensor (V)');xlabel('Time (s)');grid on;
saveplot(f,target,'identification_record');
f=figure('Visible','off');q=t>=14.5&t<=17.5;
plot(t(q),u(q),'o-','Color',C(1,:));hold on;
plot([14.5 15.9 15.9 17.5],[2.5 2.5 5 5],'--','Color',C(2,:));
xlabel('Retained run time (s)');ylabel('Input command (V)');grid on;
legend('Logged manual input','Ideal 2.5 V step approximation','Location','southeast');
saveplot(f,target,'step_input_transition');
[tm,vm_measured]=ode45(@(tt,state)(P.A*(interp1(t,u,tt,'linear')-P.hover_command_V)-state)/P.tau_s,...
 t(t>=15.7),0,odeset('RelTol',1e-8,'AbsTol',1e-9,'MaxStep',0.05));
f=figure('Visible','off');plot(t,v,'Color',C(1,:));hold on;plot(t,vm,'--','Color',C(2,:));
plot(tm,vm_measured,':','Color',C(3,:));
yline(0.632*mean(v(t>=120)),':','63.2%');xlabel('Time (s)');ylabel('Velocity (m/s)');
legend('Backward difference','Adopted model','Model driven by recorded input','Location','southeast');grid on;
saveplot(f,target,'velocity_identification');
f=figure('Visible','off');tiledlayout(1,2,'TileSpacing','compact');
valid=sv>0&sv<9.9&y>0;
nexttile;plot(y(valid),sv(valid),'o');hold on;plot(y(valid),P.sensor_gain_V_per_m*y(valid));
xlabel('Altitude (m)');ylabel('Sensor (V)');grid on;
nexttile;plot(t,v-vm);xlabel('Time (s)');ylabel('Velocity residual (m/s)');grid on;
saveplot(f,target,'validation_sensor');
f=figure('Visible','off');tiledlayout(2,1,'TileSpacing','compact');
nexttile;plot(t,y,t,ym,'--');ylabel('Altitude (m)');legend('Recorded','Model');grid on;
nexttile;plot(t,y-ym);xlabel('Time (s)');ylabel('Residual (m)');grid on;
saveplot(f,target,'position_validation');
b=1/P.tau_s;kT=P.A/P.tau_s;ks=P.sensor_gain_V_per_m;kp=P.controller_gain;
gain=linspace(0,0.035,1200);poles=zeros(2,numel(gain));
for i=1:numel(gain),poles(:,i)=roots([1 b kT*ks*gain(i)]);end
f=figure('Visible','off');plot(real(poles.'),imag(poles.'),'Color',C(1,:));hold on;
selected=roots([1 b kT*ks*kp]);plot(real(selected),imag(selected),'o','Color',C(2,:));
plot([0 -b],[0 0],'kx');xline(-b/2,':');xline(-4/30,'--');
zmin=-log(.3)/sqrt(pi^2+log(.3)^2);xx=linspace(-.16,0,100);
plot(xx,[-xx;xx]*sqrt(1-zmin^2)/zmin,'--','Color',[.5 .5 .5]);
xlabel('Real part (s^{-1})');ylabel('Imaginary part (s^{-1})');grid on;
saveplot(f,target,'root_locus');
tt=(0:P.simulation_interval_s:P.simulation_end_s)';
yn=response(tt,b,kT*kp*ks,5);un=P.hover_command_V+kp*ks*(5-yn);
f=figure('Visible','off');tiledlayout(2,1,'TileSpacing','compact');
nexttile;plot(tt,yn,'Color',C(1,:));yline(5,'--');yline(4.9,':');yline(5.1,':');
ylabel('Altitude (m)');grid on;xlim([0 100]);
nexttile;plot(tt,un,'Color',C(2,:));ylabel('Command (V)');xlabel('Time from step (s)');grid on;xlim([0 100]);
saveplot(f,target,'nominal_response');
f=figure('Visible','off');hold on;
for factor=[.9 1 1.1]
 plot(tt,response(tt,factor*b,kT*kp*ks,5),'DisplayName',sprintf('b x %.1f',factor));
end
yline(5,'--');xlabel('Time (s)');ylabel('Altitude (m)');legend('Location','southeast');grid on;
saveplot(f,target,'aerodynamic_robustness');
corners=readtable(fullfile(P.project_root,'results','independent_resistor_corners.csv'));
f=figure('Visible','off');scatter(corners.tracking_error_percent,corners.overshoot_percent,10,corners.b_factor,'filled');
xline(8,'--');yline(30,'--');xlabel('Tracking error (%)');
ylabel('Overshoot (%)');colorbar;grid on;
saveplot(f,target,'component_robustness');
hardware=readtable(fullfile(P.project_root,'results','hardware_screenshot_digitised.csv'));
keep=hardware.time_s_digitised<=86.2;
f=figure('Visible','off');plot(hardware.time_s_digitised(keep),hardware.altitude_m_digitised(keep),'Color',C(1,:));hold on;
plot(tt,response(tt,b,kT*kp*ks,5.033),'--','Color',C(2,:));yline(5.033,':');
xlabel('Graph time (s)');ylabel('Altitude (m)');legend('Connected controller (digitised)','Nominal model');grid on;xlim([0 88]);
saveplot(f,target,'hardware_comparison');
scope=readtable(fullfile(P.project_root,'results','simulink_scope_digitised.csv'));
reference=2.5*ones(size(tt));reference(tt>=2.5)=5;
seq=response(tt,b,kT*kp*ks,2.5)+response(max(tt-2.5,0),b,kT*kp*ks,2.5);
command=P.hover_command_V+kp*ks*(reference-seq);
f=figure('Visible','off');tiledlayout(2,1,'TileSpacing','compact');
nexttile;plot(scope.time_s_digitised,scope.altitude_m_digitised,'Color',C(2,:));hold on;
plot(tt,seq,'--','Color',C(1,:));plot(tt,reference,':k');ylabel('Altitude (m)');
legend('Supplied Simulink (digitised)','MATLAB same-reference prediction','Reference');grid on;xlim([0 100]);
nexttile;plot(scope.time_s_digitised,scope.command_V_digitised,'Color',C(3,:));hold on;
plot(tt,command,'--','Color',C(1,:));xlabel('Simulation clock (s)');ylabel('Command (V)');grid on;xlim([0 100]);
saveplot(f,target,'simulink_comparison');
f=figure('Visible','off');plot(scope.time_s_digitised,scope.altitude_m_digitised,'Color',C(2,:));hold on;
plot(tt,seq,'--','Color',C(1,:));plot(tt,reference,':k');xlabel('Simulation clock (s)');ylabel('Altitude (m)');
legend('Supplied Simulink (digitised)','MATLAB same-reference prediction','Reference');grid on;xlim([0 100]);
saveplot(f,target,'simulink_altitude_comparison');
% A 2 mV command bias at 70 s produces 0.002/(Kp*ks) final displacement.
disturbed=yn+response(max(tt-70,0),b,kT*kp*ks,0.002/(kp*ks));
f=figure('Visible','off');plot(tt,disturbed,'Color',C(1,:));hold on;plot(tt,yn,'--');
yline(5,'--');yline(4.6,':');yline(5.4,':');xlabel('Time (s)');ylabel('Altitude (m)');grid on;
saveplot(f,target,'disturbance_prediction');
fprintf('MATLAB numerical figure exports saved to %s\n',target);
end

function y=response(t,b,c,amplitude)
sigma=b/2;wd=sqrt(c-sigma^2);
y=amplitude*(1-exp(-sigma*t).*(cos(wd*t)+sigma/wd*sin(wd*t)));
end

function saveplot(f,target,name)
layout=findall(f,'Type','tiledlayout');
if isempty(layout)
 axesHandles=findall(f,'Type','axes');object=axesHandles(1);
else
 object=layout(1);
end
exportgraphics(object,fullfile(target,[name '.pdf']),'ContentType','vector');
exportgraphics(object,fullfile(target,[name '.png']),'Resolution',200);
close(f);
end
