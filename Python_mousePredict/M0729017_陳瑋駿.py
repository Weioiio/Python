# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 11:49:17 2019

@author: hihih
"""

import cv2
import numpy as np
from sklearn.linear_model import LinearRegression

# 建立一個大小1024*768的空幀
frame = np.zeros((768, 1024, 3), np.uint8)

def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

def theta(martix):
    x_1 = np.vstack((martix[0][0],martix[1][0]))
    x_2 = np.vstack((martix[1][0],martix[2][0]))
    y_1 = np.vstack((martix[0][1],martix[1][1]))
    y_2 = np.vstack((martix[1][1],martix[2][1]))
    
    linreg = LinearRegression()
    model_1 = linreg.fit(x_1, y_1)
    #斜率
    coef_1=linreg.coef_
    
    model_2 = linreg.fit(x_2, y_2)
    coef_2=linreg.coef_
    #print(coef)

    #print(model)
    #print('coef:', linreg.coef_)
    #截距
    #print('intercept:', linreg.intercept_)
    
    #最小二乘法LS偏移量
    theta_X_1 = np.dot(np.dot(np.linalg.inv(np.dot(x_1.T, x_1)), x_1.T), y_1)
    theta_X_2 = np.dot(np.dot(np.linalg.inv(np.dot(x_2.T, x_2)), x_2.T), y_2)
    theta_Y_1 = np.dot(np.dot(np.linalg.inv(np.dot(y_1.T, y_1)), y_1.T), x_1)
    theta_Y_2 = np.dot(np.dot(np.linalg.inv(np.dot(y_2.T, y_2)), y_2.T), x_2)
    
    return theta_X_1,theta_Y_1,theta_X_2,theta_Y_2,coef_1,coef_2



# 初始化測量座標和滑鼠運動預測的陣列
last_measurement = current_measurement = np.array((2, 1), np.float32)
last_predicition = current_prediction = np.zeros((2, 1), np.float32)
#last_predicition_2 = current_prediction = np.zeros((2, 1), np.float32)


#傳遞X,Y座標
def mousemove(event, x, y, s, p):
    global frame, current_measurement, last_last_measurement, last_measurement, current_prediction, last_prediction
    
    #if(event == CV_EVENT_MOUSEMOVE):
        #mousePosition = Point(x,y)
    
    # 初始化
    last_last_measurement = last_measurement
    last_measurement = current_measurement
    last_prediction = current_prediction
    #last_prediction_2 = current_prediction
    print('Start-----------------------')
    # 傳遞當前測量座標值
    current_measurement = np.array([[np.float32(x)], [np.float32(y)]])
    print('---------------當前座標---------------')
    print(current_measurement)
    
    #預測結果
    k.correct(current_measurement)
    current_prediction = k.predict()
    #print('----------預測座標----------')
    #print(current_prediction)
    
    # 上上一次測量值
    llmx, llmy = last_last_measurement[0], last_last_measurement[1]
    #print('----------上上一次測量值----------')
    #print(llmx,llmy)
    # 上一次測量值
    lmx, lmy = last_measurement[0], last_measurement[1]
    #print('----------上次測量值----------')
    #print(lmx,lmy)
    # 當前測量值
    cmx, cmy = current_measurement[0], current_measurement[1]
    print('當前測量值')
    print(cmx,cmy)
    
    # 上一次預測值
    lpx, lpy = last_prediction[0], last_prediction[1]
    print('上次預測值')
    print(lpx,lpy)
    # 當前預測值
    cpx, cpy = current_prediction[0], current_prediction[1]
    print('當前預測值')
    print(cpx,cpy)
    
    
    martix = np.vstack((last_last_measurement,last_measurement,current_measurement))
    #print(martix)
    martix_2 = martix.reshape(3,2)
    #print(martix_2)
    #print('----------Theta---------')
    #print(theta(martix_2))
    
    ttx_1, tty_1, ttx_2, tty_2, coef_1,coef_2= theta(martix_2)
    #print(ttx_1, tty_1, ttx_2, tty_2)
    llpx = ttx_1*lmx+llmx*(1-ttx_1)+coef_1
    llpy = (tty_1-1)*lmy+llmy*(1-(tty_1-1))+coef_1
    
    ccpx = ttx_2*cmx+lmx*(1-ttx_2)+coef_2
    ccpy = (tty_2-1)*cmy+lmy*(1-(tty_2-1))+coef_2
    #print('----------KAL上次預測值----------')
    #print(lpx,lpy)
    #print('----------LES上次預測值----------')
    #print(llpx,llpy)
    #print('----------KAL當前預測值----------')
    #print(cpx,cpy)
    print('LES當前預測值')
    print(ccpx,ccpy)
    

    
    
    
    # 繪製測量值軌跡（灰白色）
    cv2.line(frame, (lmx, lmy), (cmx, cmy), (255,255,255),lineType=1)
    # 繪製預測值軌跡（暗紅色）
    cv2.line(frame, (lpx, lpy), (cpx, cpy), (42,42,165),lineType=8)
    # 繪製預測值軌跡（土黃色）
    cv2.line(frame, (llpx, llpy), (ccpx, ccpy), (12,149,205),lineType=8)
    
    ccpx = ccpx.reshape(1)
    ccpy = ccpy.reshape(1)
    ccpx = np.rint(ccpx)
    ccpy = np.rint(ccpy)
    lpx = np.rint(cpx)
    lpy = np.rint(cpy)
    print('求整數')
    print(lpx,lpy)
    print(ccpx,ccpy)
    print('-----當前座標-----')
    print(cmx,cmy)
    

        
    if((cmx==lpx)&(cmy==lpy)):
        cv2.circle(frame,(cmx,cmy), 3, (255,0,255), -1)
        #cv2.imshow('image', frame)
        #cv2.waitKey (10000) # 显示 10000 ms 即 10s 后消失
        #cv2.destroyAllWindows()
        print('Model 1-1 Predict Touch!!!!!!!!!!!!!')
        
        
    if((cmx==cpx)&(cmy==cpy)):
        cv2.circle(frame,(cmx,cmy), 10, (255,0,255), -1)
        #cv2.imshow('image', frame)
        #cv2.waitKey (10000) # 显示 10000 ms 即 10s 后消失
        #cv2.destroyAllWindows()
        print('Model 1-2 Predict Touch!!!!!!!!!!!!!')
        
    if((cmx==ccpx)&(cmy==ccpy)):
        cv2.circle(frame,(cmx,cmy), 3, (0,255,255), -1)
        #cv2.imshow('image', frame)
        #cv2.waitKey (10000) # 显示 10000 ms 即 10s 后消失
        #cv2.destroyAllWindows()
        print('Model 2-1 Predict Touch!!!!!!!!!!!!!')
        
        
    if((cmx==llpx)&(cmy==llpy)):
        cv2.circle(frame,(cmx,cmy), 10, (0,255,255), -1)
        #cv2.imshow('image', frame)
        #cv2.waitKey (10000) # 显示 10000 ms 即 10s 后消失
        #cv2.destroyAllWindows()
        print('Model 2-2 Predict Touch!!!!!!!!!!!!!')
        
        
    
        
    print('End------------------------')

    
cv2.namedWindow("LSE mouse track&predict")
cv2.setMouseCallback("LSE mouse track&predict", mousemove)

k = cv2.KalmanFilter(4, 2) 
#公式中的H
k.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
#公式中的A
k.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
#公式中的Q
k.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32) * 0.03

#Xn = A*Xn-1 + B + W
#Zn = H*Xn + V



#設定視窗ESC時Break
while True:
    cv2.imshow("LSE mouse track&predict", frame)
    if (cv2.waitKey(30) & 0xff) == 27:
        break
#關閉所有OpenCV視窗
cv2.destroyAllWindows()