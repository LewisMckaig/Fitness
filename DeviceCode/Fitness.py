#!/usr/bin/python
# -*- coding:utf-8 -*-
#Code from top to main can be found at : https://www.waveshare.com/wiki/Sense_HAT_(B) scroll to main for own code
#Fitness.py
#
from os import system, name
import time
import smbus
import math
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import datetime

#lots of code for pointing to memory locations and reading the sensors and converting them to usable values
Gyro  = [0,0,0]
Accel = [0,0,0]
Mag   = [0,0,0]
pitch = 0.0
roll  = 0.0
yaw   = 0.0
pu8data=[0,0,0,0,0,0,0,0]
U8tempX=[0,0,0,0,0,0,0,0,0]
U8tempY=[0,0,0,0,0,0,0,0,0]
U8tempZ=[0,0,0,0,0,0,0,0,0]
GyroOffset=[0,0,0]
Ki = 1.0
Kp = 4.50
q0 = 1.0
q1=q2=q3=0.0
angles=[0.0,0.0,0.0]
true                                 =0x01
false                                =0x00
# define ICM-20948 Device I2C address
I2C_ADD_ICM20948                     = 0x68
I2C_ADD_ICM20948_AK09916             = 0x0C
I2C_ADD_ICM20948_AK09916_READ        = 0x80
I2C_ADD_ICM20948_AK09916_WRITE       = 0x00
# define ICM-20948 Register
# user bank 0 register
REG_ADD_WIA                          = 0x00
REG_VAL_WIA                          = 0xEA
REG_ADD_USER_CTRL                    = 0x03
REG_VAL_BIT_DMP_EN                   = 0x80
REG_VAL_BIT_FIFO_EN                  = 0x40
REG_VAL_BIT_I2C_MST_EN               = 0x20
REG_VAL_BIT_I2C_IF_DIS               = 0x10
REG_VAL_BIT_DMP_RST                  = 0x08
REG_VAL_BIT_DIAMOND_DMP_RST          = 0x04
REG_ADD_PWR_MIGMT_1                  = 0x06
REG_VAL_ALL_RGE_RESET                = 0x80
REG_VAL_RUN_MODE                     = 0x01 # Non low-power mode
REG_ADD_LP_CONFIG                    = 0x05
REG_ADD_PWR_MGMT_1                   = 0x06
REG_ADD_PWR_MGMT_2                   = 0x07
REG_ADD_ACCEL_XOUT_H                 = 0x2D
REG_ADD_ACCEL_XOUT_L                 = 0x2E
REG_ADD_ACCEL_YOUT_H                 = 0x2F
REG_ADD_ACCEL_YOUT_L                 = 0x30
REG_ADD_ACCEL_ZOUT_H                 = 0x31
REG_ADD_ACCEL_ZOUT_L                 = 0x32
REG_ADD_GYRO_XOUT_H                  = 0x33
REG_ADD_GYRO_XOUT_L                  = 0x34
REG_ADD_GYRO_YOUT_H                  = 0x35
REG_ADD_GYRO_YOUT_L                  = 0x36
REG_ADD_GYRO_ZOUT_H                  = 0x37
REG_ADD_GYRO_ZOUT_L                  = 0x38
REG_ADD_EXT_SENS_DATA_00             = 0x3B
REG_ADD_REG_BANK_SEL                 = 0x7F
REG_VAL_REG_BANK_0                   = 0x00
REG_VAL_REG_BANK_1                   = 0x10
REG_VAL_REG_BANK_2                   = 0x20
REG_VAL_REG_BANK_3                   = 0x30

# user bank 1 register
# user bank 2 register
REG_ADD_GYRO_SMPLRT_DIV              = 0x00
REG_ADD_GYRO_CONFIG_1                = 0x01
REG_VAL_BIT_GYRO_DLPCFG_2            = 0x10  # bit[5:3]
REG_VAL_BIT_GYRO_DLPCFG_4            = 0x20  # bit[5:3]
REG_VAL_BIT_GYRO_DLPCFG_6            = 0x30  # bit[5:3]
REG_VAL_BIT_GYRO_FS_250DPS           = 0x00  # bit[2:1]
REG_VAL_BIT_GYRO_FS_500DPS           = 0x02  # bit[2:1]
REG_VAL_BIT_GYRO_FS_1000DPS          = 0x04  # bit[2:1]
REG_VAL_BIT_GYRO_FS_2000DPS          = 0x06  # bit[2:1]
REG_VAL_BIT_GYRO_DLPF                = 0x01  # bit[0]
REG_ADD_ACCEL_SMPLRT_DIV_2           = 0x11
REG_ADD_ACCEL_CONFIG                 = 0x14
REG_VAL_BIT_ACCEL_DLPCFG_2           = 0x10  # bit[5:3]
REG_VAL_BIT_ACCEL_DLPCFG_4           = 0x20  # bit[5:3]
REG_VAL_BIT_ACCEL_DLPCFG_6           = 0x30  # bit[5:3]
REG_VAL_BIT_ACCEL_FS_2g              = 0x00  # bit[2:1]
REG_VAL_BIT_ACCEL_FS_4g              = 0x02  # bit[2:1]
REG_VAL_BIT_ACCEL_FS_8g              = 0x04  # bit[2:1]
REG_VAL_BIT_ACCEL_FS_16g             = 0x06  # bit[2:1]
REG_VAL_BIT_ACCEL_DLPF               = 0x01  # bit[0]

# user bank 3 register
REG_ADD_I2C_SLV0_ADDR                = 0x03
REG_ADD_I2C_SLV0_REG                 = 0x04
REG_ADD_I2C_SLV0_CTRL                = 0x05
REG_VAL_BIT_SLV0_EN                  = 0x80
REG_VAL_BIT_MASK_LEN                 = 0x07
REG_ADD_I2C_SLV0_DO                  = 0x06
REG_ADD_I2C_SLV1_ADDR                = 0x07
REG_ADD_I2C_SLV1_REG                 = 0x08
REG_ADD_I2C_SLV1_CTRL                = 0x09
REG_ADD_I2C_SLV1_DO                  = 0x0A

# define ICM-20948 Register  end

# define ICM-20948 MAG Register
REG_ADD_MAG_WIA1                     = 0x00
REG_VAL_MAG_WIA1                     = 0x48
REG_ADD_MAG_WIA2                     = 0x01
REG_VAL_MAG_WIA2                     = 0x09
REG_ADD_MAG_ST2                      = 0x10
REG_ADD_MAG_DATA                     = 0x11
REG_ADD_MAG_CNTL2                    = 0x31
REG_VAL_MAG_MODE_PD                  = 0x00
REG_VAL_MAG_MODE_SM                  = 0x01
REG_VAL_MAG_MODE_10HZ                = 0x02
REG_VAL_MAG_MODE_20HZ                = 0x04
REG_VAL_MAG_MODE_50HZ                = 0x05
REG_VAL_MAG_MODE_100HZ               = 0x08
REG_VAL_MAG_MODE_ST                  = 0x10
# define ICM-20948 MAG Register  end

MAG_DATA_LEN                         =6

class ICM20948(object):
  def __init__(self,address=I2C_ADD_ICM20948):
    self._address = address
    self._bus = smbus.SMBus(1)
    bRet=self.icm20948Check()             #Initialization of the device multiple times after power on will result in a return error
    # while true != bRet:
    #   print("ICM-20948 Error\n" )
    #   time.sleep(0.5)
    # print("ICM-20948 OK\n" )
    time.sleep(0.5)                       #We can skip this detection by delaying it by 500 milliseconds
    # user bank 0 register 
    self._write_byte( REG_ADD_REG_BANK_SEL , REG_VAL_REG_BANK_0)
    self._write_byte( REG_ADD_PWR_MIGMT_1 , REG_VAL_ALL_RGE_RESET)
    time.sleep(0.1)
    self._write_byte( REG_ADD_PWR_MIGMT_1 , REG_VAL_RUN_MODE)  
    #user bank 2 register
    self._write_byte( REG_ADD_REG_BANK_SEL , REG_VAL_REG_BANK_2)
    self._write_byte( REG_ADD_GYRO_SMPLRT_DIV , 0x07)
    self._write_byte( REG_ADD_GYRO_CONFIG_1 , REG_VAL_BIT_GYRO_DLPCFG_6 | REG_VAL_BIT_GYRO_FS_1000DPS | REG_VAL_BIT_GYRO_DLPF)
    self._write_byte( REG_ADD_ACCEL_SMPLRT_DIV_2 ,  0x07)
    self._write_byte( REG_ADD_ACCEL_CONFIG , REG_VAL_BIT_ACCEL_DLPCFG_6 | REG_VAL_BIT_ACCEL_FS_2g | REG_VAL_BIT_ACCEL_DLPF)
    #user bank 0 register
    self._write_byte( REG_ADD_REG_BANK_SEL , REG_VAL_REG_BANK_0) 
    time.sleep(0.1)
    self.icm20948GyroOffset()
    self.icm20948MagCheck()
    self.icm20948WriteSecondary( I2C_ADD_ICM20948_AK09916|I2C_ADD_ICM20948_AK09916_WRITE,REG_ADD_MAG_CNTL2, REG_VAL_MAG_MODE_20HZ)
  def icm20948_Gyro_Accel_Read(self):
    self._write_byte( REG_ADD_REG_BANK_SEL , REG_VAL_REG_BANK_0)
    data =self._read_block(REG_ADD_ACCEL_XOUT_H, 12)
    self._write_byte( REG_ADD_REG_BANK_SEL , REG_VAL_REG_BANK_2)
    Accel[0] = (data[0]<<8)|data[1]
    Accel[1] = (data[2]<<8)|data[3]
    Accel[2] = (data[4]<<8)|data[5]
    Gyro[0]  = ((data[6]<<8)|data[7]) - GyroOffset[0]
    Gyro[1]  = ((data[8]<<8)|data[9]) - GyroOffset[1]
    Gyro[2]  = ((data[10]<<8)|data[11]) - GyroOffset[2]
    if Accel[0]>=32767:             #Solve the problem that Python shift will not overflow
      Accel[0]=Accel[0]-65535
    elif Accel[0]<=-32767:
      Accel[0]=Accel[0]+65535
    if Accel[1]>=32767:
      Accel[1]=Accel[1]-65535
    elif Accel[1]<=-32767:
      Accel[1]=Accel[1]+65535
    if Accel[2]>=32767:
      Accel[2]=Accel[2]-65535
    elif Accel[2]<=-32767:
      Accel[2]=Accel[2]+65535
    if Gyro[0]>=32767:
      Gyro[0]=Gyro[0]-65535
    elif Gyro[0]<=-32767:
      Gyro[0]=Gyro[0]+65535
    if Gyro[1]>=32767:
      Gyro[1]=Gyro[1]-65535
    elif Gyro[1]<=-32767:
      Gyro[1]=Gyro[1]+65535
    if Gyro[2]>=32767:
      Gyro[2]=Gyro[2]-65535
    elif Gyro[2]<=-32767:
      Gyro[2]=Gyro[2]+65535
  def icm20948MagRead(self):
    counter=20
    while(counter>0):
      time.sleep(0.01)
      self.icm20948ReadSecondary( I2C_ADD_ICM20948_AK09916|I2C_ADD_ICM20948_AK09916_READ , REG_ADD_MAG_ST2, 1)
      if ((pu8data[0] & 0x01)!= 0):
        break
      counter-=1
    if counter!=0:
      for i in range(0,8):
        self.icm20948ReadSecondary( I2C_ADD_ICM20948_AK09916|I2C_ADD_ICM20948_AK09916_READ , REG_ADD_MAG_DATA , MAG_DATA_LEN)
        U8tempX[i] = (pu8data[1]<<8)|pu8data[0]
        U8tempY[i] = (pu8data[3]<<8)|pu8data[2]
        U8tempZ[i] = (pu8data[5]<<8)|pu8data[4]
      Mag[0]=(U8tempX[0]+U8tempX[1]+U8tempX[2]+U8tempX[3]+U8tempX[4]+U8tempX[5]+U8tempX[6]+U8tempX[7])/8
      Mag[1]=-(U8tempY[0]+U8tempY[1]+U8tempY[2]+U8tempY[3]+U8tempY[4]+U8tempY[5]+U8tempY[6]+U8tempY[7])/8
      Mag[2]=-(U8tempZ[0]+U8tempZ[1]+U8tempZ[2]+U8tempZ[3]+U8tempZ[4]+U8tempZ[5]+U8tempZ[6]+U8tempZ[7])/8
    if Mag[0]>=32767:            #Solve the problem that Python shift will not overflow
      Mag[0]=Mag[0]-65535
    elif Mag[0]<=-32767:
      Mag[0]=Mag[0]+65535
    if Mag[1]>=32767:
      Mag[1]=Mag[1]-65535
    elif Mag[1]<=-32767:
      Mag[1]=Mag[1]+65535
    if Mag[2]>=32767:
      Mag[2]=Mag[2]-65535
    elif Mag[2]<=-32767:
      Mag[2]=Mag[2]+65535
  def icm20948ReadSecondary(self,u8I2CAddr,u8RegAddr,u8Len):
    u8Temp=0
    self._write_byte( REG_ADD_REG_BANK_SEL,  REG_VAL_REG_BANK_3) #swtich bank3
    self._write_byte( REG_ADD_I2C_SLV0_ADDR, u8I2CAddr)
    self._write_byte( REG_ADD_I2C_SLV0_REG,  u8RegAddr)
    self._write_byte( REG_ADD_I2C_SLV0_CTRL, REG_VAL_BIT_SLV0_EN|u8Len)

    self._write_byte( REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0) #swtich bank0
    
    u8Temp = self._read_byte(REG_ADD_USER_CTRL)
    u8Temp |= REG_VAL_BIT_I2C_MST_EN
    self._write_byte( REG_ADD_USER_CTRL, u8Temp)
    time.sleep(0.01)
    u8Temp &= ~REG_VAL_BIT_I2C_MST_EN
    self._write_byte( REG_ADD_USER_CTRL, u8Temp)
    
    for i in range(0,u8Len):
      pu8data[i]= self._read_byte( REG_ADD_EXT_SENS_DATA_00+i)

    self._write_byte( REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3) #swtich bank3
    
    u8Temp = self._read_byte(REG_ADD_I2C_SLV0_CTRL)
    u8Temp &= ~((REG_VAL_BIT_I2C_MST_EN)&(REG_VAL_BIT_MASK_LEN))
    self._write_byte( REG_ADD_I2C_SLV0_CTRL,  u8Temp)
    
    self._write_byte( REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0) #swtich bank0
  def icm20948WriteSecondary(self,u8I2CAddr,u8RegAddr,u8data):
    u8Temp=0
    self._write_byte( REG_ADD_REG_BANK_SEL,  REG_VAL_REG_BANK_3) #swtich bank3
    self._write_byte( REG_ADD_I2C_SLV1_ADDR, u8I2CAddr)
    self._write_byte( REG_ADD_I2C_SLV1_REG,  u8RegAddr)
    self._write_byte( REG_ADD_I2C_SLV1_DO,   u8data)
    self._write_byte( REG_ADD_I2C_SLV1_CTRL, REG_VAL_BIT_SLV0_EN|1)

    self._write_byte( REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0) #swtich bank0

    u8Temp = self._read_byte(REG_ADD_USER_CTRL)
    u8Temp |= REG_VAL_BIT_I2C_MST_EN
    self._write_byte( REG_ADD_USER_CTRL, u8Temp)
    time.sleep(0.01)
    u8Temp &= ~REG_VAL_BIT_I2C_MST_EN
    self._write_byte( REG_ADD_USER_CTRL, u8Temp)

    self._write_byte( REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3) #swtich bank3

    u8Temp = self._read_byte(REG_ADD_I2C_SLV0_CTRL)
    u8Temp &= ~((REG_VAL_BIT_I2C_MST_EN)&(REG_VAL_BIT_MASK_LEN))
    self._write_byte( REG_ADD_I2C_SLV0_CTRL,  u8Temp)

    self._write_byte( REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0) #swtich bank0
  def icm20948GyroOffset(self):
    s32TempGx = 0
    s32TempGy = 0
    s32TempGz = 0
    for i in range(0,32):
      self.icm20948_Gyro_Accel_Read()
      s32TempGx += Gyro[0]
      s32TempGy += Gyro[1]
      s32TempGz += Gyro[2]
      time.sleep(0.01)
    GyroOffset[0] = s32TempGx >> 5
    GyroOffset[1] = s32TempGy >> 5
    GyroOffset[2] = s32TempGz >> 5
  def _read_byte(self,cmd):
    return self._bus.read_byte_data(self._address,cmd)
  def _read_block(self, reg, length=1):
    return self._bus.read_i2c_block_data(self._address, reg, length)
  def _read_u16(self,cmd):
    LSB = self._bus.read_byte_data(self._address,cmd)
    MSB = self._bus.read_byte_data(self._address,cmd+1)
    return (MSB	<< 8) + LSB
  def _write_byte(self,cmd,val):
    self._bus.write_byte_data(self._address,cmd,val)
    time.sleep(0.0001)
  def imuAHRSupdate(self,gx, gy,gz,ax,ay,az,mx,my,mz):    
    norm=0.0
    hx = hy = hz = bx = bz = 0.0
    vx = vy = vz = wx = wy = wz = 0.0
    exInt = eyInt = ezInt = 0.0
    ex=ey=ez=0.0 
    halfT = 0.024
    global q0
    global q1
    global q2
    global q3
    q0q0 = q0 * q0
    q0q1 = q0 * q1
    q0q2 = q0 * q2
    q0q3 = q0 * q3
    q1q1 = q1 * q1
    q1q2 = q1 * q2
    q1q3 = q1 * q3
    q2q2 = q2 * q2   
    q2q3 = q2 * q3
    q3q3 = q3 * q3          

    norm = float(1/math.sqrt(ax * ax + ay * ay + az * az))     
    ax = ax * norm
    ay = ay * norm
    az = az * norm

    norm = float(1/math.sqrt(mx * mx + my * my + mz * mz))      
    mx = mx * norm
    my = my * norm
    mz = mz * norm

    # compute reference direction of flux
    hx = 2 * mx * (0.5 - q2q2 - q3q3) + 2 * my * (q1q2 - q0q3) + 2 * mz * (q1q3 + q0q2)
    hy = 2 * mx * (q1q2 + q0q3) + 2 * my * (0.5 - q1q1 - q3q3) + 2 * mz * (q2q3 - q0q1)
    hz = 2 * mx * (q1q3 - q0q2) + 2 * my * (q2q3 + q0q1) + 2 * mz * (0.5 - q1q1 - q2q2)         
    bx = math.sqrt((hx * hx) + (hy * hy))
    bz = hz     

    # estimated direction of gravity and flux (v and w)
    vx = 2 * (q1q3 - q0q2)
    vy = 2 * (q0q1 + q2q3)
    vz = q0q0 - q1q1 - q2q2 + q3q3
    wx = 2 * bx * (0.5 - q2q2 - q3q3) + 2 * bz * (q1q3 - q0q2)
    wy = 2 * bx * (q1q2 - q0q3) + 2 * bz * (q0q1 + q2q3)
    wz = 2 * bx * (q0q2 + q1q3) + 2 * bz * (0.5 - q1q1 - q2q2)  

    # error is sum of cross product between reference direction of fields and direction measured by sensors
    ex = (ay * vz - az * vy) + (my * wz - mz * wy)
    ey = (az * vx - ax * vz) + (mz * wx - mx * wz)
    ez = (ax * vy - ay * vx) + (mx * wy - my * wx)

    if (ex != 0.0 and ey != 0.0 and ez != 0.0):
      exInt = exInt + ex * Ki * halfT
      eyInt = eyInt + ey * Ki * halfT  
      ezInt = ezInt + ez * Ki * halfT

      gx = gx + Kp * ex + exInt
      gy = gy + Kp * ey + eyInt
      gz = gz + Kp * ez + ezInt

    q0 = q0 + (-q1 * gx - q2 * gy - q3 * gz) * halfT
    q1 = q1 + (q0 * gx + q2 * gz - q3 * gy) * halfT
    q2 = q2 + (q0 * gy - q1 * gz + q3 * gx) * halfT
    q3 = q3 + (q0 * gz + q1 * gy - q2 * gx) * halfT  

    norm = float(1/math.sqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3))
    q0 = q0 * norm
    q1 = q1 * norm
    q2 = q2 * norm
    q3 = q3 * norm
  def icm20948Check(self):
    bRet=false
    if REG_VAL_WIA == self._read_byte(REG_ADD_WIA):
      bRet = true
    return bRet
  def icm20948MagCheck(self):
    self.icm20948ReadSecondary( I2C_ADD_ICM20948_AK09916|I2C_ADD_ICM20948_AK09916_READ,REG_ADD_MAG_WIA1, 2)
    if (pu8data[0] == REG_VAL_MAG_WIA1) and ( pu8data[1] == REG_VAL_MAG_WIA2) :
        bRet = true
        return bRet
  def icm20948CalAvgValue(self):
    MotionVal[0]=Gyro[0]/32.8
    MotionVal[1]=Gyro[1]/32.8
    MotionVal[2]=Gyro[2]/32.8
    MotionVal[3]=Accel[0]
    MotionVal[4]=Accel[1]
    MotionVal[5]=Accel[2]
    MotionVal[6]=Mag[0]
    MotionVal[7]=Mag[1]
    MotionVal[8]=Mag[2]

#@Author: Lewis Mckaig
#Main Method: records the device movements and saves any activity to firebase
#Date: April 2021
if __name__ == '__main__':
  import time
  print("\nFitness device\n")
  MotionVal=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
  icm20948=ICM20948()

  ##initialize firebase client and variables
  sensitivity = 2000 #default to 2000 incase the db cannot be read
  cred = credentials.Certificate("/home/pi/firebaseKey.json")
  firebase_admin.initialize_app(cred)

  db = firestore.client()

  doc_ref = db.collection(u'Settings').document(u'Goals')

  doc = doc_ref.get()
  if doc.exists:
    sensitivity = int(doc.get('Sensitivity'))
  else:
    print(u'No such document!')

  #initialize the "previous" variables, which are used to compare to the newest reading
  prevAccel = [0,0,0]
  prevPitch = 0.0
  prevRoll  = 0.0
  prevYaw   = 0.0
  
  #Read The Sensors
  icm20948.icm20948_Gyro_Accel_Read()
  icm20948.icm20948MagRead()
  icm20948.icm20948CalAvgValue()

  icm20948.imuAHRSupdate(MotionVal[0] * 0.0175, MotionVal[1] * 0.0175,MotionVal[2] * 0.0175,
                MotionVal[3],MotionVal[4],MotionVal[5],
                MotionVal[6], MotionVal[7], MotionVal[8])
  #set roll pitch and yaw
  pitch = math.asin(-2 * q1 * q3 + 2 * q0* q2)* 57.3
  roll  = math.atan2(2 * q2 * q3 + 2 * q0 * q1, -2 * q1 * q1 - 2 * q2* q2 + 1)* 57.3
  yaw   = math.atan2(-2 * q1 * q2 - 2 * q0 * q3, 2 * q2 * q2 + 2 * q3 * q3 - 1) * 57.3

  #set the "previous" values so that they can be compared to determine movement
  prevAccel[0] = Accel[0]
  prevAccel[1] = Accel[1]
  prevAccel[2] = Accel[2]

  prevPitch = pitch
  prevRoll = roll
  prevYaw = yaw

  #----------------------------------------------------------------------------------------------------
  #functions:
  #gyroCheck()
  #accelCheck()
  #buffer()
  #record()
  #read()
  #previous()

  def clear():
    _ = system('clear')

  #checks if the gyroscope reading is above the threshold, using the sensitivy value from the database returns boolean
  def gyroCheck():

  #Normalize the readings so that the values are positve, -100 is the same velocity as 100, but in the oposite direction
    gyroNormal = [0,0,0]
    if Gyro[0] < 0:
      gyroNormal[0] = Gyro[0] * -1
    else:
      gyroNormal[0] = Gyro[0]

    if Gyro[0] < 0:
      gyroNormal[1] = Gyro[1] * -1
    else:
      gyroNormal[1] = Gyro[1]

    if Gyro[0] < 0:
      gyroNormal[2] = Gyro[2] * -1
    else:
      gyroNormal[2] = Gyro[2]

    if gyroNormal[0] > sensitivity or gyroNormal[1] > sensitivity or gyroNormal[2] > sensitivity:
      return true
    else:
      return false

    
  #compares to previous acceleration values, returns boolean
  def accelCheck():
    if Accel[0] - prevAccel[0] > 100 or Accel[1] - prevAccel[1] > 100 or Accel[2] - prevAccel[2] > 100:
      return true
    else:
      return false
    
  #buffer reduces false positive movement readings 
  def buffer():
    print("buffer")
    #check to see if movement exceeds threshold 3 times to not pick up small movements, then record if it gets 3 successes in a row
    if gyroCheck() and accelCheck():
      previous()
      time.sleep(1)
      read()
      if gyroCheck() and accelCheck():
        previous()
        time.sleep(1)
        read()
        if gyroCheck() and accelCheck():
          previous()
          time.sleep(1)
          read()
          if gyroCheck() and accelCheck():
            record()

  #records activity so long as the device continues moving. Allows for no movement to be read a few times before ending the recording.
  #change the "while noMove = x" to allow for more or less leniency for no movement, each increase of 1 to noMove is roughly half a second
  #while noMove = 8 would be around 4 seconds and while noMove = 10 would be 5
  def record():
    activity = 0
    dt = datetime.datetime.today()
    date = str(dt.day) + "-" + str(dt.month) + "-" + str(dt.year)#for correct formatting e.g. 2021-04-13

    device_ref = db.collection(u'Device').document(date)#get document for current day if it exists

    device = device_ref.get()
    if device.exists:
      activity = int(device.get('Activity'))
    else:
      activity = 0 #if no document, activity will be 0

    previous()
    print("recording...")
    noMove = 0
    start = time.time()
    
    while noMove <8: #every value above 1 is equivalent to roughly half a second
      read()#get sensor readings then check
      if gyroCheck()and accelCheck():
        noMove = 0 #reset the count if a correct reading is made
      else:
        #set end time to first instance of not moving, otherwise recorded time would include extra few seconds of non movement
        if noMove == 0:
          end = time.time()
        noMove = noMove + 1 # increment noMove
      previous()
      time.sleep(0.5)
      
    total = (math.floor(end - start))/60 #rounds down to nearest second. then divides it by 60 to change to minutes
    print("time recorded = {}".format(total))
    if total > 1: #only save if more than a minute
      total = math.floor(total)
      activity = activity + total
      reading_ref = db.collection(u'Device')
      reading_ref.document(date).set({'Date': date,'Activity':activity})
#end of record()--------------------------------------------------------------------------------------

      
  #reads the sensors
  def read():
    icm20948.icm20948_Gyro_Accel_Read()
    icm20948.icm20948MagRead()
    icm20948.icm20948CalAvgValue()
    icm20948.imuAHRSupdate(MotionVal[0] * 0.0175, MotionVal[1] * 0.0175,MotionVal[2] * 0.0175,
                MotionVal[3],MotionVal[4],MotionVal[5],
                MotionVal[6], MotionVal[7], MotionVal[8])
    pitch = math.asin(-2 * q1 * q3 + 2 * q0* q2)* 57.3
    roll  = math.atan2(2 * q2 * q3 + 2 * q0 * q1, -2 * q1 * q1 - 2 * q2* q2 + 1)* 57.3
    yaw   = math.atan2(-2 * q1 * q2 - 2 * q0 * q3, 2 * q2 * q2 + 2 * q3 * q3 - 1) * 57.3

  #sets the values of the last read so that they can be compared to
  def previous():
    prevAccel[0] = Accel[0]
    prevAccel[1] = Accel[1]
    prevAccel[2] = Accel[2]

    prevPitch = pitch
    prevRoll = roll
    prevYaw = yaw


  #Loop Indefinately, changes device state to buffer if sufficient movement
  #state changes to buffer if the threshold of movement is met
  while True:
    recording = True

    recording_ref = db.collection(u'Settings').document(u'Goals')

    rec = recording_ref.get()
    if rec.exists:
      recording = bool(rec.get('Recording'))
    else:
      recording = True #assume true if it cant be read

    read()
    #old code which displays all the sensors on the devices values, used for debugging
   # print("\r\n /-------------------------------------------------------------/ \r\n")
    #print('\r\n Roll = %.2f , Pitch = %.2f , Yaw = %.2f\r\n'%(roll,pitch,yaw))
    #print('\r\nAcceleration current:  X = %d , Y = %d , Z = %d\r\n'%(Accel[0],Accel[1],Accel[2]))
    #print('\r\nAcceleration previous: X = %d , Y = %d , Z = %d\r\n'%(prevAccel[0],prevAccel[1],prevAccel[2]))
    #print('\r\nGyroscope:     X = %d , Y = %d , Z = %d\r\n'%(Gyro[0],Gyro[1],Gyro[2]))
    #print('\r\nMagnetic:      X = %d , Y = %d , Z = %d'%((Mag[0]),Mag[1],Mag[2]))

   #change to buffer if true
    if gyroCheck() and accelCheck() and recording == True:
      buffer()

    previous()





      
         
      





      
