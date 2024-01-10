# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 03:23:21 2024

@author: Ajithabh
"""

import json, math
from scipy import signal
from sigmt import mtproc, data_sel, mahaDist, tipper, var, plotting
import numpy as np

def read_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
        # # Access values using keys
        # FFT_Length = data['FFT_Length']
        # parzen_radius = data['parzen_radius']
        # MD_threshold_impedance = data['MD_threshold_impedance']
        # MD_threshold_tipper = data['MD_threshold_tipper']
    return config

def read_ts(project_path):
    procinfo = {}
    procinfo['sites'], procinfo['selectedsite'], procinfo['measid'], \
        procinfo['all_meas'], procinfo['select_meas'], procinfo['proc_path'] = mtproc.makeprocpath(project_path)
    ts, procinfo['fs'], procinfo['sensor_no'], timeline, \
    procinfo['ChoppStat'], loc = mtproc.ts(procinfo['proc_path'])
    all_meas = procinfo['all_meas']
    select_meas = procinfo['select_meas']
    procinfo['meas'] = all_meas[select_meas]
    return ts, procinfo

def decimate(ts, procinfo, decimation):
    for d in decimation:
        ts['tsEx'] = signal.decimate(ts.get('tsEx'), d, n=None, ftype='iir')
        ts['tsEy'] = signal.decimate(ts.get('tsEy'), d, n=None, ftype='iir')
        ts['tsHx'] = signal.decimate(ts.get('tsHx'), d, n=None, ftype='iir')
        ts['tsHy'] = signal.decimate(ts.get('tsHy'), d, n=None, ftype='iir')
        ts['tsHz'] = signal.decimate(ts.get('tsHz'), d, n=None, ftype='iir')
        procinfo['fs'] = procinfo.get('fs')/d
        return ts, procinfo
    
def bandavg(ts,procinfo,config):
    # Find out window length
    procinfo['nofs'] = len(ts['tsEx'])
    if config['FFT_Length'] == 0:
        procinfo['WindowLength'] = mtproc.FFTLength(procinfo.get('nofs'))
    else:
        procinfo['WindowLength'] = config['FFT_Length']
    procinfo['overlap'] = 50 # Input in percentage %
    print('\nFFT Window Length: '+ str(procinfo.get('WindowLength')))
    procinfo['nstacks'] = math.floor(procinfo.get('nofs')/procinfo.get('WindowLength'))
    procinfo['nstacks'] = (procinfo.get('nstacks') * 2) - 1
    print('Time series overlap: ' + str(procinfo.get('overlap'))+'%')
    print('No. of windows: '+ str(procinfo.get('nstacks')))
    ftlist,bandavg = mtproc.bandavg(ts, procinfo, config)
    bandavg['ftlist'] = ftlist
    return ftlist, bandavg

def coherencies(bandavg):
    AllcohEx = data_sel.cohEx(bandavg)
    AllcohEy = data_sel.cohEy(bandavg)
    bandavg['AllcohEx'] = AllcohEx
    bandavg['AllcohEy'] = AllcohEy
    return bandavg

def perform_ct(CohThre, minpercent, bandavg):
    ctflag = 1
    [cohMatrixEx, cohMatrixEy] = data_sel.performct(ctflag,CohThre,minpercent,bandavg['ftlist'],bandavg,bandavg['AllcohEx'],bandavg['AllcohEy'])
    bandavg['cohMatrixEx'] = cohMatrixEx
    bandavg['cohMatrixEy'] = cohMatrixEy
    return bandavg

def perform_robust(config,ftlist,bandavg):
    bandavg['pre_sel_matEx'] = bandavg['cohMatrixEx']
    bandavg['pre_sel_matEy'] = bandavg['cohMatrixEx']
    bandavg['mdmatrixEx'],bandavg['Zxx_mcd'],bandavg['Zxy_mcd'],bandavg['mahal_robustEx'] = mahaDist.mcd(bandavg,'Ex',config)
    bandavg['mdmatrixEy'],bandavg['Zyx_mcd'],bandavg['Zyy_mcd'],bandavg['mahal_robustEy'] = mahaDist.mcd(bandavg,'Ey',config)
    bandavg['selectedEx'] = bandavg.get('mdmatrixEx')
    bandavg['selectedEy'] = bandavg.get('mdmatrixEy')
    bandavg['avgt'] = np.sum((bandavg.get('selectedEx'))!=0,axis=1)
    [TxAll, TyAll] = tipper.tippall(bandavg)
    mahaWtTx, Tx_mcd_mean = tipper.mcd(TxAll,config)
    mahaWtTy, Ty_mcd_mean = tipper.mcd(TyAll,config)
    bandavg['tipp_selected'] = mahaWtTx * mahaWtTy
    [Tx, Ty] = tipper.tipper(bandavg)
    [TxVar, TyVar] = tipper.tipperVar(bandavg)
    #=========== Tipper estimation DONE===============================
    #
    #==================== Robust estimation begins ===================
    #
    Z_huber = mtproc.perform_robust(ftlist,bandavg)
    #
    #==================== Calculation of variance ===================
    Zvar = {}
    Zvar['xx'],Zvar['xy'],cohEx = var.ZExvar(Z_huber,bandavg)
    Zvar['yx'],Zvar['yy'],cohEy = var.ZEyvar(Z_huber,bandavg)
    return Z_huber, Zvar, Tx, Ty, TxVar, TyVar, cohEx, cohEy
    
def plotfigs(procinfo, ftlist, Z_huber, Zvar, Tx, Ty, cohEx, cohEy):
    plotting.plotfigs(procinfo, ftlist, Z_huber, Zvar, Tx, Ty, cohEx, cohEy)
    
