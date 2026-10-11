function result = run_root_locus_design(P)
% Detailed root locus method and response checks. Requires Control System Toolbox.
%% 1. Adopt exactly the model and gain in the saved report
A = P.A;                 % Velocity DC gain, m/(s V)
tau = P.tau_s;                   % Velocity time constant, s
ks = P.sensor_gain_V_per_m;                   % Sensor gain, V/m
Kp = P.controller_gain;                % Report controller voltage-error gain, V/V
hoverV = P.hover_command_V;                % Equilibrium actuator command, V
reference_m = P.reference_step_m;             % Report nominal reference: 0 to 5 m
identificationDeltaU_V = P.identification_step_V; % Identification input: 2.5 to 5.0 V
% The identification actuator step and closed-loop position reference have
% different units. Do not substitute the 2.5 V identification step for 5 m.
b = 1/tau;
kT = A/tau;
s = tf('s');
Gpos = A/(s*(tau*s + 1));
G0 = ks*Gpos;                % Exclude Kp: rlocus varies this multiplier
L = Kp*G0;
T = feedback(L,1);          % y/reference; equivalent sensor-scaled loop
outDir = fullfile(P.project_root,'results','matlab','root_locus');
if ~exist(outDir,'dir'), mkdir(outDir); end
diary(fullfile(outDir,'root_locus_calculations.txt'));
fprintf('REPORT MODEL: A=%.4f, tau=%.1f, ks=%.2f, Kp=%.5f\n',A,tau,ks,Kp);
fprintf('Identification actuator increment: %.1f V; position reference: %.1f m\n',...
    identificationDeltaU_V,reference_m);
disp('G0(s), with sensor gain but without the variable Kp:'); disp(G0);

%% 2. Open-loop poles, real-axis section, centroid and breakaway
% Poles: 0 and -1/tau. There are no finite zeros.
% Real-axis locus: [-1/tau,0]. Two asymptotes: +90 and -90 degrees.
% Kp(s) = -s*(tau*s+1)/(A*ks).
% dKp/ds = -(2*tau*s+1)/(A*ks) = 0 at sb = -1/(2*tau).
openPoles = pole(G0);
openZeros = zero(G0);
sb = -1/(2*tau);
Kbreak = 1/(4*tau*A*ks);
fprintf('\nOpen-loop poles:\n'); disp(openPoles);
fprintf('Number of finite zeros: %d\n',numel(openZeros));
fprintf('Centroid and breakaway pole: %.9f 1/s\n',sb);
fprintf('Breakaway gain: %.9f\n',Kbreak);

%% 3. Convert the 30%% overshoot limit into a damping/gain limit
MpLimit = 0.30;              % Fraction, not percentage
zetaMin = -log(MpLimit)/sqrt(pi^2 + log(MpLimit)^2);
% Characteristic polynomial: tau*s^2+s+A*ks*Kp = 0.
% wn = sqrt(A*ks*Kp/tau); zeta = 1/(2*sqrt(tau*A*ks*Kp)).
KmaxNominal = 1/(4*tau*A*ks*zetaMin^2);
% For aerodynamic uncertainty, vary b while kT stays fixed.
% Scalar gain tolerance models overall gain only, not resistor mismatch.
KmaxJointScalar = (0.9*b)^2/(4*kT*ks*zetaMin^2*1.1);
fprintf('\nMinimum damping ratio for <30%% overshoot: %.9f\n',zetaMin);
fprintf('Nominal overshoot limit: 0 < Kp < %.9f\n',KmaxNominal);
fprintf('Joint +/-10%% drag/gain limit: Kp < %.9f\n',KmaxJointScalar);

%% 4. Calculate the selected closed-loop pole pair
q = A*ks*Kp;
selectedPoles = roots([tau 1 q]);
wn = sqrt(q/tau);
sigma = 1/(2*tau);
zeta = sigma/wn;
wd = sqrt(wn^2-sigma^2);
MpAnalytic = 100*exp(-pi*zeta/sqrt(1-zeta^2));
tp = pi/wd;
TsApprox = 4/sigma;          % Standard 2%% settling approximation
TsEnvelope = -log(0.02*sqrt(1-zeta^2))/sigma;
fprintf('\nCharacteristic polynomial: %.1f*s^2+s+%.9f = 0\n',tau,q);
fprintf('Selected poles:\n'); disp(selectedPoles);
fprintf('wn=%.9f rad/s; zeta=%.9f; wd=%.9f rad/s\n',wn,zeta,wd);
fprintf('Analytic overshoot=%.6f%%; peak time=%.6f s\n',MpAnalytic,tp);
fprintf('4/sigma approximation=%.6f s; 2%% envelope bound=%.6f s\n',...
    TsApprox,TsEnvelope);

%% 5. Check the root locus angle and magnitude conditions
sd = complex(-sigma,wd);     % Upper selected pole
theta1 = atan2d(imag(sd),real(sd));
theta2 = atan2d(imag(sd),real(sd)+b);
GatPole = evalfr(G0,sd);
angleGdeg = angle(GatPole)*180/pi;
KfromMagnitude = 1/abs(GatPole);
KfromDistances = abs(sd)*abs(sd+b)/(kT*ks);
charResidual = abs(tau*sd^2+sd+q);
fprintf('\nAngle from pole 0 = %.6f degrees\n',theta1);
fprintf('Angle from pole -1/tau = %.6f degrees\n',theta2);
fprintf('Pole angle sum=%.6f degrees; angle G0(sd)=%.6f degrees\n',...
    theta1+theta2,angleGdeg);
fprintf('Magnitude gain 1/|G0(sd)| = %.9f\n',KfromMagnitude);
fprintf('Pole-distance gain = %.9f; characteristic residual = %.3g\n',...
    KfromDistances,charResidual);

%% 6. Plot the root locus and the specification boundaries
gainVector = linspace(0,0.04,2001);
r = rlocus(G0,gainVector);   % Each column corresponds to one gain
angelBlue = [143 201 230]/255;
darkBlue = [57 123 156]/255;
f1 = figure('Color','w');
plot(real(r(1,:)),imag(r(1,:)),'Color',darkBlue,'LineWidth',1.8);
hold on;
plot(real(r(2,:)),imag(r(2,:)),'Color',darkBlue,'LineWidth',1.8,...
    'HandleVisibility','off');
plot(real(openPoles),imag(openPoles),'kx','MarkerSize',10,'LineWidth',2);
plot(real(selectedPoles),imag(selectedPoles),'o','Color',[0.85 0.35 0.12],...
    'MarkerFaceColor',[0.85 0.35 0.12],'MarkerSize',7);
plot(sb,0,'ks','MarkerFaceColor',angelBlue,'MarkerSize',7);
xline(sb,':','Fixed complex-pole real part','Color',[0.2 0.5 0.3]);
x = linspace(-0.18,0,200);
slope = sqrt(1-zetaMin^2)/zetaMin;
plot(x,-x*slope,'--','Color',[0.5 0.5 0.5]);
plot(x,x*slope,'--','Color',[0.5 0.5 0.5],'HandleVisibility','off');
TsTarget = 30;
sigmaTarget = 4/TsTarget;
xline(-sigmaTarget,'--','30 s approximate settling boundary',...
    'Color',[0.7 0.2 0.2]);
grid on; xlabel('Real part (1/s)'); ylabel('Imaginary part (1/s)');
title(sprintf('Kitticopter root locus: Kp = %.5f',Kp));
xlim([-0.18 0.015]); ylim([-0.30 0.30]);
exportgraphics(f1,fullfile(outDir,'root_locus.png'),'Resolution',200);
exportgraphics(f1,fullfile(outDir,'root_locus.pdf'),'ContentType','vector');
fprintf('\n30 s design line: Re(s) <= %.9f\n',-sigmaTarget);
fprintf('Available complex-pole real part: %.9f\n',sb);
fprintf(['The standard 30 s decay-rate target is outside this P-only locus.\n'...
    'This line uses Ts approximately 4/sigma; the exact response is checked next.\n']);

%% 7. Verify the step response and report-compatible settling time
t = (0:0.005:160)';
y = reference_m*step(T,t);
info = stepinfo(y,t,reference_m,'SettlingTimeThreshold',0.02);
% Also reproduce the report's sampled final-entry definition explicitly.
outside = find(abs(y-reference_m)>0.02*reference_m);
if isempty(outside)
    TsSampled = 0;
elseif outside(end)==numel(t)
    TsSampled = NaN;          % Not settled within the simulated interval
else
    TsSampled = t(outside(end)+1);
end
u = hoverV+Kp*ks*(reference_m-y);
steadyGain = dcgain(T);
fprintf('\nMATLAB stepinfo results:\n'); disp(info);
fprintf('Sampled last-entry 2%% settling time=%.6f s\n',TsSampled);
fprintf('DC tracking gain=%.9f; ideal step tracking error=%.9f%%\n',...
    steadyGain,100*abs(1-steadyGain));
fprintf('Command range=%.6f to %.6f V\n',min(u),max(u));
f2 = figure('Color','w');
subplot(2,1,1);
plot(t,y,'Color',darkBlue,'LineWidth',1.5); hold on;
yline(reference_m,'k--','Reference');
yline(0.98*reference_m,':','2% lower bound');
yline(1.02*reference_m,':','2% upper bound');
grid on; ylabel('Position (m)'); title('Report nominal 0 to 5 m response');
subplot(2,1,2);
plot(t,u,'Color',[0.85 0.35 0.12],'LineWidth',1.5); hold on;
yline(hoverV,':','Hover command'); grid on;
xlabel('Time from reference step (s)'); ylabel('Actuator command (V)');
exportgraphics(f2,fullfile(outDir,'nominal_response.png'),'Resolution',200);
writetable(table(t,y,u,'VariableNames',{'time_s','position_m','command_V'}),...
    fullfile(outDir,'nominal_response.csv'));

%% 8. Aerodynamic constant uncertainty: b times 0.9, 1.0 and 1.1
% With kT fixed, tau'=1/b' and A'=kT/b': do not vary tau alone.
f3 = figure('Color','w'); hold on; grid on;
for bf = [0.9 1.0 1.1]
    Tb = tf(kT*Kp*ks,[1 bf*b kT*Kp*ks]);
    yb = reference_m*step(Tb,t);
    ib = stepinfo(yb,t,reference_m,'SettlingTimeThreshold',0.02);
    plot(t,yb,'LineWidth',1.4,'DisplayName',sprintf('b x %.1f',bf));
    fprintf('b x %.1f: overshoot %.6f%%; stepinfo settling %.6f s\n',...
        bf,ib.Overshoot,ib.SettlingTime);
end
yline(reference_m,'k--','HandleVisibility','off'); legend('Location','best');
xlabel('Time (s)'); ylabel('Position (m)'); title('Aerodynamic uncertainty');
exportgraphics(f3,fullfile(outDir,'aerodynamic_uncertainty.png'),'Resolution',200);

%% 9. Joint scalar gain and drag uncertainty: four corners
% Independent circuit-resistor tolerance is NOT covered by these four cases.
% The original analysis/analyse.py evaluates 2,048 resistor/drag corners.
cornerResults = zeros(4,4);
row = 0;
for bf = [0.9 1.1]
    for kf = [0.9 1.1]
        row = row+1;
        Tc = tf(kT*(kf*Kp)*ks,[1 bf*b kT*(kf*Kp)*ks]);
        yc = reference_m*step(Tc,t);
        ic = stepinfo(yc,t,reference_m,'SettlingTimeThreshold',0.02);
        cornerResults(row,:) = [bf kf ic.Overshoot ic.SettlingTime];
    end
end
cornerTable = array2table(cornerResults,'VariableNames',...
    {'drag_factor','gain_factor','overshoot_percent','settling_time_s'});
disp('Joint scalar uncertainty results:'); disp(cornerTable);
writetable(cornerTable,fullfile(outDir,'joint_scalar_corners.csv'));
fprintf('Largest scalar-corner overshoot: %.6f%%\n',max(cornerResults(:,3)));
fprintf('Detailed independent component tolerance: run analysis/analyse.py.\n');
diary off;
fprintf('\nFigures, tables and calculation log saved in:\n%s\n',outDir);

result = struct("gain",Kp,"poles",selectedPoles,"damping_ratio",zeta,...
    "overshoot_percent",MpAnalytic,"settling_time_s",TsSampled);
end
