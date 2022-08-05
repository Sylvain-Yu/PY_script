# -*- coding: UTF-8 -*-
# from typing import List
import numpy as np
import matplotlib.pyplot as plt



##   This script is used for Checking the data saved.
##   Designer: Sylvain
##   email:jasonshake@163.com
##   Date: 10/27/2021

filepath = r'D:\SourceCode\NxxSy_RaceInverter\Apsw\Calibration\CSITM_0.bin'


CpuCurrSc_PsCfg = 700
CpuVoltSc_PsCfg = 1000
time_base_gap = 1/(20000*2)


Resolver_Max = 0.0
Resolver_Min = 0.0

def power2(Qf):
    if Qf>= 0:
        value = 1<<Qf
    else:
        value = 1/(1<<(-Qf))
    return value

def mask(width):
    mask = (1 << width) -1
    return mask


def decodetype(v,s,width,Qf):
    mask_v = mask(width)
    v = v & mask_v
    if s == 0:  # unsigned
        temp = v / power2(Qf)
    else:     # signed
        if (v & 1 <<(width -1 ))>>(width -1) == 1: # sign bit == 1            
            v = mask_v - v
            v = v + 1
            temp = v/power2(Qf)
            temp = (-1) * temp
        else:
            temp = v / power2(Qf)
    return temp

def ListDecode(list = [],sign =1,width=32,Qf =16):
    retList = []
    for v in list:
        n = int.from_bytes(v, "little",signed= False)
        n = decodetype(n,sign,width,Qf)
        retList.append(n)
    return retList



#### 初始化定位参数


raw_pattern = "aa55feca"
pattern_v =bytes.fromhex(raw_pattern)
raw_data = []


# 初始化所有参数列表

Trc_Angle_ELEC = []          #1
Trc_adc_Current_PHA = []    #2
Trc_adc_Current_PHB = []     #3
Trc_adc_Current_PHC = []     #4
Trc_adc_Res_Sine = []        #5
Trc_adc_Res_Cosine = []     #6
Trc_VdMath_meas = []      #7
Trc_VqMath_meas = []    #8
Trc_PosMath0_meas = []     #9
Trc_SpeedMath0_meas = []   #10
Trc_DC_Voltage = []     #11
Trc_Speed_rpm = []     #12
Trc_Id_ref = []    #13
Trc_Vd_ref = []    #14
Trc_Iq_ref = []    #15
Trc_Vq_ref = []    #16
Trc_SVPWM_Id_KP = []    #17
Trc_SVPWM_Id_KI = []   #18
Trc_SVPWM_Iq_KP = []   #19
Trc_SVPWM_Iq_KI = []    #20
Trc_SSCSpeed_Rp = []    #21
Trc_TorqueMeas_N = []   #22
Trc_TorqueSP_N = []    #23
Trc_IdFilt_meas = []    #24
Trc_IqFilt_meas = []   #25
Trc_Duty_A_PWM = []   #26
Trc_Duty_B_PWM = []   #27
Trc_Duty_C_PWM = []   #28


with open(filepath,'rb') as f:
    f.seek(0,2)
    end = f.tell()
    f.seek(0,0)
    while f.tell() < end:
        raw_data.append(f.read(4))
    first_index = raw_data.index(pattern_v)
    secd_index = raw_data.index(pattern_v,first_index+1)
    count = raw_data.count(pattern_v)

    # gap = secd_index - first_index
    f.seek((first_index+1)*4,0)
    i = 0
    while i< count-2:
        Trc_Angle_ELEC.append(f.read(4))   # 1
        Trc_adc_Current_PHA.append(f.read(4))    # 2
        Trc_adc_Current_PHB.append(f.read(4))     #3
        Trc_adc_Current_PHC.append(f.read(4))     #4
        Trc_adc_Res_Sine.append(f.read(4))       #5
        Trc_adc_Res_Cosine.append(f.read(4))     #6
        Trc_VdMath_meas.append(f.read(4))      #7
        Trc_VqMath_meas.append(f.read(4))    #8
        Trc_PosMath0_meas.append(f.read(4))     #9
        Trc_SpeedMath0_meas.append(f.read(4))   #10
        Trc_DC_Voltage.append(f.read(4))     #11
        Trc_Speed_rpm.append(f.read(4))     #12
        Trc_Id_ref.append(f.read(4))    #13
        Trc_Vd_ref.append(f.read(4))    #14
        Trc_Iq_ref.append(f.read(4))    #15
        Trc_Vq_ref.append(f.read(4))    #16
        Trc_SVPWM_Id_KP.append(f.read(4))    #17
        Trc_SVPWM_Id_KI.append(f.read(4))   #18
        Trc_SVPWM_Iq_KP.append(f.read(4))   #19
        Trc_SVPWM_Iq_KI.append(f.read(4))    #20
        Trc_SSCSpeed_Rp.append(f.read(4))    #21
        Trc_TorqueMeas_N.append(f.read(4))   #22
        Trc_TorqueSP_N.append(f.read(4))    #23
        Trc_IdFilt_meas.append(f.read(4))    #24
        Trc_IqFilt_meas.append(f.read(4))   #25
        Trc_Duty_A_PWM.append(f.read(4))   #26
        Trc_Duty_B_PWM.append(f.read(4))   #27
        Trc_Duty_C_PWM.append(f.read(4))   #28
        f.seek(4,1) # 此为pattern项，跳过
        i = i + 1


def TimesList(t, list = []):
    i = 0

    for v in list:
        v = v * t
        list[i] = v
        i = i + 1
    return list



Trc_adc_Current_PHA_v = TimesList(CpuCurrSc_PsCfg ,ListDecode(Trc_adc_Current_PHA,1,16,13))
Trc_adc_Current_PHB_v = TimesList(CpuCurrSc_PsCfg ,ListDecode(Trc_adc_Current_PHB,1,16,13))
Trc_adc_Current_PHC_v = TimesList(CpuCurrSc_PsCfg ,ListDecode(Trc_adc_Current_PHC,1,16,13))
Trc_Id_ref_v = TimesList(CpuCurrSc_PsCfg ,ListDecode(Trc_Id_ref,1,32,30))
Trc_Iq_ref_v = TimesList(CpuCurrSc_PsCfg ,ListDecode(Trc_Iq_ref,1,32,30))
Trc_Vq_ref_v = TimesList(CpuVoltSc_PsCfg ,ListDecode(Trc_Vq_ref,1,32,30))
Trc_Vd_ref_v = TimesList(CpuVoltSc_PsCfg ,ListDecode(Trc_Vd_ref,1,32,30))
Trc_VqMath_meas_v =TimesList(CpuVoltSc_PsCfg , ListDecode(Trc_VqMath_meas,1,32,30))
Trc_VdMath_meas_v = TimesList(CpuVoltSc_PsCfg ,ListDecode(Trc_VdMath_meas,1,32,30))
Trc_Angle_ELEC_v = ListDecode(Trc_Angle_ELEC,0,16,0)
Trc_adc_Res_Sine_v = ListDecode(Trc_adc_Res_Sine,1,16,13)
Trc_adc_Res_Cosine_v = ListDecode(Trc_adc_Res_Cosine,1,16,13)

Trc_Speed_rpm_v = ListDecode(Trc_Speed_rpm,1,32,16)
Trc_DC_Voltage_v = ListDecode(Trc_DC_Voltage,0,32,16)

Trc_IdFilt_meas_v = ListDecode(Trc_IdFilt_meas,1,32,16)
Trc_IqFilt_meas_v = ListDecode(Trc_IqFilt_meas,1,32,16)

Trc_TorqueMeas_N_v = ListDecode(Trc_TorqueMeas_N,1,32,16)
Trc_TorqueSP_N_v = ListDecode(Trc_TorqueSP_N,1,32,16)
Trc_SSCSpeed_Rp_v = ListDecode(Trc_SSCSpeed_Rp,1,32,16)
Trc_SpeedMath0_meas_v = ListDecode(Trc_SpeedMath0_meas,1,32,25)
Trc_PosMath0_meas_v = ListDecode(Trc_PosMath0_meas,0,16,0)
Trc_Duty_A_PWM_v = ListDecode(Trc_Duty_A_PWM,0,16,0)
Trc_Duty_B_PWM_v = ListDecode(Trc_Duty_B_PWM,0,16,0)
Trc_Duty_C_PWM_v = ListDecode(Trc_Duty_C_PWM,0,16,0)



## find the Sine Resolver Max & Min
i = 0
for x in Trc_adc_Res_Sine_v:
    if i > 20:
        if x > Resolver_Max:
            Resolver_Max = x
        if x < Resolver_Min:
            Resolver_Min = x
    elif i == 19:
        Resolver_Max = x
        Resolver_Min = x
    i = i + 1

print("Resovler Sin Max = ", Resolver_Max)
print("Resolver Sin Min = ", Resolver_Min)


## find the Cosine Resolver Max & Min
i = 0
for x in Trc_adc_Res_Cosine_v:
    if i > 20:
        if x > Resolver_Max:
            Resolver_Max = x
        if x < Resolver_Min:
            Resolver_Min = x
    elif i == 19:
        Resolver_Max = x
        Resolver_Min = x            
    i = i + 1

print("Resolver Cos Max =", Resolver_Max)
print("Resovler Cos Min =", Resolver_Min)

print("Trc_VqMath_meas_v mean = ", np.mean(Trc_VqMath_meas_v))
print("Trc_VdMath_meas_v mean = ", np.mean(Trc_VdMath_meas_v))

## init for the time base : x
x = []
time_base = 0
for i in Trc_adc_Current_PHA:
    x.append(time_base)
    time_base = time_base + time_base_gap  # 200us
x = np.array(x)
MathPos = np.array(Trc_PosMath0_meas_v)
elec_angle = np.array(Trc_Angle_ELEC_v)
sine = np.array(Trc_adc_Res_Sine_v)
cosine = np.array(Trc_adc_Res_Cosine_v)
CurrentA = np.array(Trc_adc_Current_PHA_v)
CurrentB = np.array(Trc_adc_Current_PHB_v)
CurrentC = np.array(Trc_adc_Current_PHC_v)
MathSpeed = np.array(Trc_SpeedMath0_meas_v)
Speed = np.array(Trc_Speed_rpm_v)
Dc_voltage = np.array(Trc_DC_Voltage_v)
Iq_Ref = np.array(Trc_Iq_ref_v)
Id_Ref = np.array(Trc_Id_ref_v)
Iq_Meas = np.array(Trc_IqFilt_meas_v)
Id_Meas = np.array(Trc_IdFilt_meas_v)
Vq_Meas = np.array(Trc_VqMath_meas_v)
Vd_Meas = np.array(Trc_VdMath_meas_v)
Vq_Ref = np.array(Trc_Vq_ref_v)
Vd_Ref = np.array(Trc_Vd_ref_v)
TorqueSp = np.array(Trc_TorqueSP_N_v)
TorqueMeas = np.array(Trc_TorqueMeas_N_v)
SSCSpeed = np.array(Trc_SSCSpeed_Rp_v)
DutyA = np.array(Trc_Duty_A_PWM_v)
DutyB = np.array(Trc_Duty_B_PWM_v)
DutyC = np.array(Trc_Duty_C_PWM_v)

## 绘制图片

fig1 = plt.figure("Resolver")
# fig, (ax1,ax2) = plt.subplots(2,1)
ax11 = plt.subplot(3,1,1)
ax12 = plt.subplot(3,1,2)
ax13 = plt.subplot(3,1,3)

line11, = ax11.plot(x,elec_angle, label = "Trc_Angle_ELEC")
line11_1, = ax11.plot(x, MathPos, label="MathPos")
line12, = ax12.plot(x,sine, label ="Trc_adc_Sine")
line13, = ax12.plot(x,cosine, label="Trc_adc_Cosine")
line12_v = ax12.axvline(x[-1],color="skyblue")
line14, = ax13.plot(x,Speed, label="Speed")
line15, = ax13.plot(x, SSCSpeed, label="SSCSpeed")
ax11.set_title("Angle")
ax12.set_title("Resolver")
ax13.set_title("speed")
ax13.set_xlabel("time(s)")


text_sine = ax12.text(x[-1],sine[-1],str(sine[-1]))
text_cosine = ax12.text(x[-1],cosine[-1],str(cosine[-1]))

def resolver_motion(event):
    if event.inaxes == ax12:
        if 0< event.xdata and event.xdata < x[-1]:
            index = round(event.xdata/time_base_gap)
            pos_x = x[index]
            pos_sine = sine[index]
            pos_cosine = cosine[index]
            text_sine.set_position((pos_x, pos_sine))
            text_sine.set_text(str(pos_sine))
            text_cosine.set_position((pos_x,pos_cosine))
            text_cosine.set_text(str(pos_cosine))
            line12_v.set_xdata(pos_x)
            fig1.canvas.draw_idle()





fig1.canvas.mpl_connect("button_press_event",resolver_motion)



ax11.legend()
ax12.legend()
ax13.legend()
plt.grid()


fig2 = plt.figure("Current& Duty")
ax21 = plt.subplot(3,1,1)
ax22 = plt.subplot(3,1,2)
ax23 = plt.subplot(3,1,3)
line2_1, = ax21.plot(x, DutyA, label="Phase A")
line2_2, = ax21.plot(x, DutyB, label="Phase B")
line2_3, = ax21.plot(x, DutyC, label="Phase C")


line21, = ax22.plot(x, CurrentA, label = "Current A")
line22, = ax22.plot(x, CurrentB, label = "Current B")
line23, = ax22.plot(x, CurrentC, label = "Current C")
line22_v = ax22.axvline(x[-1],color="skyblue")

CurrA_text = ax22.text(x[-1],CurrentA[-1],str(CurrentA[-1]))
CurrB_text = ax22.text(x[-1],CurrentB[-1],str(CurrentB[-1]))
CurrC_text = ax22.text(x[-1],CurrentC[-1],str(CurrentC[-1]))


line24, = ax23.plot(x, Dc_voltage, label= "DC Voltage")


def current_motion(event):    
    if event.inaxes == ax22:
        if (0 < event.xdata and event.xdata < x[-1]):
            index = round(event.xdata/time_base_gap)
            pos_x = x[index]
            pos_currA = CurrentA[index]
            pos_currB = CurrentB[index]
            pos_currC = CurrentC[index]
            CurrA_text.set_position((pos_x,pos_currA))
            CurrB_text.set_position((pos_x,pos_currB))
            CurrC_text.set_position((pos_x,pos_currC))
            CurrA_text.set_text(str(pos_currA))
            CurrB_text.set_text(str(pos_currB))
            CurrC_text.set_text(str(pos_currC))
            line22_v.set_xdata(pos_x)
            fig2.canvas.draw_idle()

fig2.canvas.mpl_connect("button_press_event",current_motion)




ax21.set_title("duty")
ax22.set_title("Current")
ax23.set_title("HV")
ax21.legend()
ax22.legend()
ax23.legend()
plt.grid()


fig3 = plt.figure("D/Q")
ax31 = plt.subplot(3,1,1)
ax32 = plt.subplot(3,1,2)
ax33 = plt.subplot(3,1,3)
line31, = ax31.plot(x, Id_Meas, label="IdMeas")
line32, = ax31.plot(x, Id_Ref, label="IdRef")
line33, = ax31.plot(x, Iq_Meas, label="IqMeas")
line34, = ax31.plot(x, Iq_Ref, label="IqRef")


line35, = ax32.plot(x, Vq_Meas, label="VqMeas")
line36, = ax32.plot(x, Vd_Meas, label="VdMeas")
line37, = ax32.plot(x, Vd_Ref, label="VdRef")
line38, = ax32.plot(x, Vq_Ref, label="VqRef")

line39, = ax33.plot(x, TorqueSp, label="TorqueSp")
line3_1, = ax33.plot(x, TorqueMeas, label="TorqueMeas")


ax31.set_title("D/Q current")
ax32.set_title("D/Q Voltage")
ax33.set_title("Torque")
ax31.legend()
ax32.legend()
ax33.legend()
plt.grid()
plt.show()