"""Replot the supplied Simulink scope and compare its actual reference sequence.

The digitised samples remain approximate image-derived evidence. They are not
exported Simulink logs. The second curve is a Python model reconstruction.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from .plot_style import BLUE, ORANGE, GREEN, exporter
from .controller import closed_response


def run(project_root, parameters):
    image=np.asarray(Image.open(project_root/'data/session2/simulink_scope.png').convert('RGB'))
    x0,x1=40,1239
    yzero,ytop=596,31
    ts=[]; altitude=[]; command=[]
    for x in range(x0,x1+1):
        rgb=image[31:640,x].astype(float)
        r,g,b=rgb.T
        out=(r>180)&(r-g>65)&(g-b>35)&(g>45)&(g<190)&(b<100)
        cmd=(b-r>70)&(g-r>50)&(b-g>10)&(b>150)&(r<110)
        if out.any() and cmd.any():
            ts.append((x-x0)*100/(x1-x0))
            altitude.append((yzero-(31+np.median(np.flatnonzero(out))))*7/(yzero-ytop))
            command.append((yzero-(31+np.median(np.flatnonzero(cmd))))*7/(yzero-ytop))
    t=np.asarray(ts); y=np.asarray(altitude); u=np.asarray(command)
    assert len(t)>1000, 'Unexpected scope plot geometry or colour mask'
    pd.DataFrame({'time_s_digitised':t,'altitude_m_digitised':y,'command_V_digitised':u}).to_csv(project_root/'results/simulink_scope_digitised.csv',index=False)
    tm=np.arange(0,100.0001,parameters.interval_s)
    reference=np.where(tm<2.5,2.5,5.0)
    first=closed_response(tm,parameters,amplitude=2.5)
    delayed=np.interp(np.maximum(tm-2.5,0),tm,first)
    yp=first+delayed
    up=np.clip(parameters.hover_v+parameters.kp*parameters.ks*(reference-yp),0,5)
    pd.DataFrame({'time_s':tm,'reference_m':reference,'position_model_m':yp,'command_model_V':up}).to_csv(project_root/'results/simulink_reference_reconstruction.csv',index=False)
    residual=y-np.interp(t,tm,yp)
    fig,ax=plt.subplots(figsize=(7.1,2.3))
    ax.plot(t,y,color=ORANGE,lw=1.5,label='Supplied Simulink altitude (digitised)')
    ax.plot(tm,yp,'--',color=BLUE,lw=1.4,label='Python: matching reference sequence')
    ax.plot(tm,reference,':',color='black',label='Reference; change at 2.5 s')
    ax.set(xlabel='Simulation clock (s)',ylabel='Altitude (m)',xlim=(0,100),ylim=(0,7))
    ax.legend(fontsize=8,loc='lower right');fig.tight_layout()
    exporter(project_root/'report/figures')(fig,'simulink_altitude_comparison')
    fig,axes=plt.subplots(2,1,figsize=(7.1,3.5),sharex=True)
    axes[0].plot(t,y,color=ORANGE,lw=1.5,label='Supplied Simulink altitude (digitised)')
    axes[0].plot(tm,yp,'--',color=BLUE,lw=1.4,label='Python: same 2.5 to 5 m reference')
    axes[0].plot(tm,reference,':',color='black',label='Reference; change at 2.5 s')
    axes[0].set(ylabel='Altitude (m)',ylim=(0,7));axes[0].legend(fontsize=8,loc='lower right')
    axes[1].plot(t,u,color=GREEN,label='Supplied Simulink command (digitised)')
    axes[1].plot(tm,up,'--',color=BLUE,label='Python command prediction')
    axes[1].set(xlabel='Simulation clock (s)',ylabel='Command (V)',xlim=(0,100),ylim=(2.46,2.58))
    axes[1].legend(fontsize=8,loc='upper right');fig.tight_layout()
    exporter(project_root/'report/figures')(fig,'simulink_comparison')
    peak_idx=int(np.argmax(y)); outside=np.flatnonzero(np.abs(y-5)>0.1)
    result={
        'reference_before_m':2.5,'reference_after_m':5.0,'reference_change_s':2.5,
        'scope_peak_m':float(y[peak_idx]),'scope_peak_clock_s':float(t[peak_idx]),
        'scope_peak_above_final_reference_percent':float((y.max()-5)/5*100),
        'scope_terminal_m':float(y[-1]),'scope_terminal_tracking_percent':float(100*(1-abs(5-y[-1])/5)),
        'scope_settling_2percent_clock_s':float(t[outside[-1]+1]) if len(outside) and outside[-1]+1<len(t) else None,
        'scope_altitude_RMSE_against_matched_python_m':float(np.sqrt(np.mean(residual**2))),
        'pixel_time_s':100/(x1-x0),'pixel_height_m':7/(yzero-ytop),
        'matched_python_peak_m':float(yp.max()),'matched_python_peak_clock_s':float(tm[np.argmax(yp)]),
        'matched_python_maximum_command_V':float(up.max()),
        'reported_potentiometer_input_V':2.565,
        'reported_adjustment_provenance':'User recollection of the connected physical controller test; not a logged time series',
        'extraction':'Approximate colour digitisation; x=40..1239 is 0..100 s, y=596 is 0 m, y=31 is 7 m',
    }
    return {'supplied_simulink_scope':result}
