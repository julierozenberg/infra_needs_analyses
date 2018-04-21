# -*- coding: utf-8 -*-
"""
Created on Wed May 31 15:55:18 2017

@author: Vivien FISCH
"""

# -*- coding: utf-8 -*-
"""
sobol 
"""




from pandas import DataFrame,read_csv,concat,notnull
import glob
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import SALib
from SALib.analyze import sobol
from SALib.sample import saltelli

import numpy as np
from numpy import *
from matplotlib.font_manager import FontProperties
import os
import functools
import copy
import time
import math
import csv
from matplotlib.font_manager import FontProperties

pathsep=os.sep


for region in ['ASIA','CIS','MAF', 'LAM', 'OCDE90']:

    
    print(region)
    data=loadtxt(r'C:\Users\Vivien\Documents\World_Bank_infra_transport\WB_InfraTrans_dev\results'+pathsep+region+pathsep+'sum_results_'+region+'3.csv',dtype=float, delimiter=';', skiprows=1)
    inputs=data[:,2:14]
   
        
    problem = {'num_vars': 12,'names': ['ind_growth', 'ind_mitig','ind_trans_A', 'ind_trans_S', 'ind_trans_I','ind_trans_F','modal_scenario','costs_evolution_road','costs_evolution_rail', 'ur_ideal', 'urt_ideal', 'delay'],
    'bounds': [[0.5000001,3.49999999],[1, 2],[1,2], [1,2],[1,2], [1,2], [0,1], [-0.499999999,2.49999999], [-0.49999999,2.49999999], [1,2], [1,2], [1,2]]}
    
    
    X=saltelli.sample(problem, 1000,calc_second_order=True)
    X=X.round()
    #X[:,0][X[:,0]==2]=4    
    #X[:,0][X[:,0]==1]=2 
    X[:,9][X[:,9]==0]=300
    X[:,9][X[:,9]==1]=600
    X[:,9][X[:,9]==2]=900
    X[:,10][X[:,10]==1]=5000
    X[:,10][X[:,10]==2]=30000
    X[:,11][X[:,11]==1]=35
    X[:,11][X[:,11]==2]=65
    
    Y=full(len(X),1)
    
    for i in range(0,len(X)):
        for j in range(0,len(data)):
            if (inputs[j,:]==X[i,:]).all():
                Y[i]=data[j,14]
                
                
                
    Si=sobol.analyze(problem, Y, print_to_console=True, calc_second_order=True, conf_level=0.95)
    savetxt('S2__'+region+'.csv', Si['S2'], delimiter=',')
    savetxt('S2_conf_'+region+'.csv', Si['S2_conf'], delimiter=',')
    savetxt('S1'+region+'.csv', Si['S1'], delimiter=',')
    savetxt('S1_conf_'+region+'.csv', Si['S1_conf'], delimiter=',')
    savetxt('ST'+region+'.csv', Si['ST'], delimiter=',')
    savetxt('ST_conf'+region+'.csv', Si['ST_conf'], delimiter=',')
