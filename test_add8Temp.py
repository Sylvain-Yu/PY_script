# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib.pyplot as plt


filepath = r'D:\SourceCode\NxxSy_RaceInverterR31b\Apsw\Model\TraceDump\CSITM_0.bin'


CpuCurrSc_PsCfg = 700
CpuVoltSc_PsCfg = 1000


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


#### 初始化定位参数


raw_pattern = "aa55feca"
pattern_v =bytes.fromhex(raw_pattern)
raw_data = []


# 初始化所有参数列表

Trc_Angle_ELEC = []          # 1
Trc_adc_Current_PHA = []    # 2
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

# 8 temperature
Trc_temp1 = []
Trc_temp2 = []
Trc_temp3 = []
Trc_temp4 = []
Trc_temp5 = []
Trc_temp6 = []
Trc_temp7 = []
Trc_temp8 = []




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
        Trc_temp1.append(f.read(4))
        Trc_temp2.append(f.read(4))
        Trc_temp3.append(f.read(4))
        Trc_temp4.append(f.read(4))
        Trc_temp5.append(f.read(4))
        Trc_temp6.append(f.read(4))
        Trc_temp7.append(f.read(4))
        Trc_temp8.append(f.read(4))
        f.seek(4,1) # 此为pattern项，跳过
        i = i + 1


def ListDecode(list = [],sign =1,width=32,Qf =16):
    retList = []
    for v in list:
        n = int.from_bytes(v, "little",signed= False)
        n = decodetype(n,sign,width,Qf)
        retList.append(n)
    return retList

    # decode the Trc_adc_Res_Sine
Trc_adc_Res_Sine_v = []
for v in Trc_adc_Res_Sine:
    n = int.from_bytes(v,"little",signed=False)
    n = decodetype(n,1,16,13)
    Trc_adc_Res_Sine_v.append(n)

Trc_adc_Res_Cosine_v = []
for v in Trc_adc_Res_Cosine:
    n = int .from_bytes(v,"little",signed= False )
    n = decodetype(n,1,16,13)
    Trc_adc_Res_Cosine_v.append(n)

Trc_adc_Current_PHA_v = []
for v in Trc_adc_Current_PHA:
    n = int .from_bytes(v,"little",signed= False )
    n = decodetype(n,1,16,13)
    Trc_adc_Current_PHA_v.append(n)

Trc_adc_Current_PHB_v = []
for v in Trc_adc_Current_PHB:
    n = int .from_bytes(v,"little",signed= False )
    n = decodetype(n,1,16,13)
    Trc_adc_Current_PHB_v.append(n)
    
Trc_adc_Current_PHC_v = []
for v in Trc_adc_Current_PHC:
    n = int .from_bytes(v,"little",signed= False )
    n = decodetype(n,1,16,13)
    Trc_adc_Current_PHC_v.append(n)

Trc_Speed_rpm_v = []
for v in Trc_Speed_rpm:
    n = int.from_bytes(v, "little",signed= False)
    n = decodetype(n,1,32,16)
    Trc_Speed_rpm_v.append(n)

Trc_DC_Voltage_v = []
for v in Trc_DC_Voltage:
    n = int.from_bytes(v, "little", signed=False)
    n = decodetype(n,0,32,16)
    Trc_DC_Voltage_v.append(n)

Trc_Id_ref_v = []
for v in Trc_Id_ref:
    n = int.from_bytes(v, "little", signed=False)
    n = decodetype(n,1,32,30)
    n = n*CpuCurrSc_PsCfg
    Trc_Id_ref_v.append(n)

Trc_Iq_ref_v = []
for v in Trc_Iq_ref:
    n = int.from_bytes(v, "little", signed=False)
    n = decodetype(n,1,32,30)
    n = n* CpuCurrSc_PsCfg
    Trc_Iq_ref_v.append(n)
# print(Trc_Iq_ref_v)

Trc_IdFilt_meas_v = []
for v in Trc_IdFilt_meas:
    n = int.from_bytes(v, "little", signed=False)
    n = decodetype(n,1,32,16)
    # n = (n* CpuVoltSc_PsCfg)/(1<< 30)
    Trc_IdFilt_meas_v.append(n)

Trc_IqFilt_meas_v = []
for v in Trc_IqFilt_meas:
    n = int.from_bytes(v, "little", signed=False)
    n = decodetype(n,1,32,16)
    # n = (n* CpuVoltSc_PsCfg)/(1<< 30)
    Trc_IqFilt_meas_v.append(n)


Trc_Vq_ref_v = []
for v in Trc_Vq_ref:
    n = int.from_bytes(v, "little", signed= False)
    n = decodetype(n, 1,32,30)
    n = n* CpuVoltSc_PsCfg
    Trc_Vq_ref_v.append(n)

Trc_Vd_ref_v = []
for v in Trc_Vd_ref:
    n = int.from_bytes(v, "little", signed= False)
    n = decodetype(n, 1,32,30)
    n = n * CpuVoltSc_PsCfg
    Trc_Vd_ref_v.append(n)

Trc_VqMath_meas_v = []
for v in Trc_VqMath_meas:
    n = int.from_bytes(v, "little", signed=False)
    n = decodetype(n, 1,32, 30)
    n = n * CpuVoltSc_PsCfg
    Trc_VqMath_meas_v.append(n)

Trc_VdMath_meas_v = []
for v in Trc_VdMath_meas:
    n = int.from_bytes(v, "little", signed= False)
    n = decodetype(n, 1,32,30)
    n = n * CpuVoltSc_PsCfg
    Trc_VdMath_meas_v.append(n)


Trc_TorqueMeas_N_v = []
for v in Trc_TorqueMeas_N:
    n = int.from_bytes(v, "little", signed= False)
    n = decodetype(n, 1,32,16)
    Trc_TorqueMeas_N_v.append(n)

Trc_TorqueSP_N_v = []
for v in Trc_TorqueSP_N:
    n = int.from_bytes(v, "little", signed= False)
    n = decodetype(n, 1,32,16)
    Trc_TorqueSP_N_v.append(n)


Trc_SSCSpeed_Rp_v = []
for v in Trc_SSCSpeed_Rp:
    n = int.from_bytes(v, "little", signed=False)
    n = decodetype(n ,1,32,16)
    Trc_SSCSpeed_Rp_v.append(n)

Trc_SpeedMath0_meas_v = []
for v in Trc_SpeedMath0_meas:
    n = int.from_bytes(v,"little", signed=False)
    n = decodetype(n, 1,32,25)
    Trc_SpeedMath0_meas_v.append(n)


Trc_PosMath0_meas_v = []
for v in Trc_PosMath0_meas:
    n = int.from_bytes(v, "little", signed=False)
    n = decodetype(n, 0,16,0)
    Trc_PosMath0_meas_v.append(n)

Trc_Duty_A_PWM_v = []
for v in Trc_Duty_A_PWM:
    n = int.from_bytes(v, "little", signed=False)
    n = decodetype(n, 0,16,0)
    Trc_Duty_A_PWM_v.append(n)

Trc_Duty_B_PWM_v = []
for v in Trc_Duty_B_PWM:
    n = int.from_bytes(v, "little", signed=False)
    n = decodetype(n, 0,16,0)
    Trc_Duty_B_PWM_v.append(n)

Trc_Duty_C_PWM_v = []
for v in Trc_Duty_C_PWM:
    n = int.from_bytes(v, "little", signed=False)
    n = decodetype(n, 0,16,0)
    Trc_Duty_C_PWM_v.append(n)

Trc_Angle_ELEC_v = ListDecode(Trc_Angle_ELEC,0,16,0)
temp1_v = ListDecode(Trc_temp1,1,32,16)
temp2_v = ListDecode(Trc_temp2,1,32,16)
temp3_v = ListDecode(Trc_temp3,1,32,16)
temp4_v = ListDecode(Trc_temp4,1,32,16)
temp5_v = ListDecode(Trc_temp5,1,32,16)
temp6_v = ListDecode(Trc_temp6,1,32,16)
temp7_v = ListDecode(Trc_temp7,1,32,16)
temp8_v = ListDecode(Trc_temp8,1,32,16)

## init for the time base : x
x = []
time_base = 0
for i in Trc_adc_Current_PHA:
    x.append(time_base)
    time_base = time_base + 0.0002  # 200us
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
Temp1 = np.array(temp1_v)
Temp2 = np.array(temp2_v)
Temp3 = np.array(temp3_v)
Temp4 = np.array(temp4_v)
Temp5 = np.array(temp5_v)
Temp6 = np.array(temp6_v)
Temp7 = np.array(temp7_v)
Temp8 = np.array(temp8_v)



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
line14, = ax13.plot(x,Speed, label="Speed")
line15, = ax13.plot(x, SSCSpeed, label="SSCSpeed")
ax11.set_title("Angle")
ax12.set_title("Resolver")
ax13.set_title("speed")
ax13.set_xlabel("time(s)")
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
line24, = ax23.plot(x, Dc_voltage, label= "DC Voltage")

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

fig4 = plt.figure("temperature")
ax40 = plt.subplot(1,1,1)
line41, = ax40.plot(x, Temp1, label="temp1")
line42, = ax40.plot(x, Temp2, label="temp2")
line43, = ax40.plot(x, Temp3, label="temp3")
line44, = ax40.plot(x, Temp4, label="temp4")
line45, = ax40.plot(x, Temp5, label="temp5")
line46, = ax40.plot(x, Temp6, label="temp6")
line47, = ax40.plot(x, Temp7, label="temp7")
line48, = ax40.plot(x, Temp8, label="temp8")
ax40.legend()
plt.show()