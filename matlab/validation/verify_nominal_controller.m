function verify_nominal_controller(P)
% Original independent report check, using the shared parameters.
A=P.A; tau=P.tau_s; ks=P.sensor_gain_V_per_m; Kp=P.controller_gain;
b=1/tau; kT=A/tau;
s=tf('s'); Gy=A/(s*(tau*s+1));
L=Kp*ks*Gy; T=feedback(L,1);
t=(0:0.005:160)'; y=5*step(T,t);
wn=sqrt(A*Kp*ks/tau); zeta=1/(2*sqrt(tau*A*Kp*ks));
wd=wn*sqrt(1-zeta^2);
fprintf('Poles:'); disp(pole(T));
fprintf('zeta=%.7f, wn=%.7f, wd=%.7f\n',zeta,wn,wd);
fprintf('Analytic Mp=%.6f%%, tp=%.6f s\n',100*exp(-pi*zeta/sqrt(1-zeta^2)),pi/wd);
info=stepinfo(y,t,5,'SettlingTimeThreshold',0.02);
disp(info);
u=2.5+Kp*ks*(5-y);
assert(all(u>=0 & u<=5),'Nominal command is outside 0-5 V');
figure; rlocus(ks*Gy); grid on; hold on;
plot(real(pole(T)),imag(pole(T)),'ro','MarkerFaceColor','r');
title('Proportional root locus; sensor gain included');
xline(-1/(2*tau),'--','Fixed complex-pole real part');
figure; subplot(2,1,1);plot(t,y,t,5*ones(size(t)),'--');
yline(4.9,':');yline(5.1,':'); ylabel('Position (m)');grid on;
subplot(2,1,2);plot(t,u);ylabel('Command (V)');xlabel('Time (s)');grid on;
figure; hold on;
for bf=[0.9 1 1.1]
 Tb=tf(kT*Kp*ks,[1 bf*b kT*Kp*ks]);
 yb=5*step(Tb,t);ib=stepinfo(yb,t,5,'SettlingTimeThreshold',0.02);
 fprintf('b x %.1f: Mp %.5f%%, Ts %.5f s\n',bf,ib.Overshoot,ib.SettlingTime);
 plot(t,yb,'DisplayName',sprintf('b x %.1f',bf));
end
legend;grid on; xlabel('Time (s)');ylabel('Position (m)');
fprintf('Joint scalar worst Mp: ');
Tw=tf(kT*(1.1*Kp)*ks,[1 .9*b kT*(1.1*Kp)*ks]);
iw=stepinfo(5*step(Tw,t),t,5,'SettlingTimeThreshold',0.02);disp(iw.Overshoot);

end
