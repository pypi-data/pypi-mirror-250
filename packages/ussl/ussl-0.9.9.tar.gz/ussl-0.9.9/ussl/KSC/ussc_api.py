from ussl.KSC.KlAkOAPI.Params import KlAkArray
from ussl.KSC.KlAkOAPI.AdmServer import KlAkAdmServer
from ussl.KSC.KlAkOAPI.HostGroup import KlAkHostGroup
from ussl.KSC.KlAkOAPI.ChunkAccessor import KlAkChunkAccessor

import socket, struct
import urllib3

def ip2long(ip):
    """
    Convert an IP string to long
    params:
        ip
    return:
        ip as long
    """
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

def GetServer(server, port, username, password):
    '''
        Connect to KSC server
        params:
            server   - ksc server address
            port     - ksc server port
            username - ksc server username
            password - ksc server password
        return:
            KSC server object
    '''

    try:
        server = KlAkAdmServer.Create(
            f'https://{server}:{port}',
            username,
            password,
            verify = False)
        return server
    except Exception:
        return None
    

def FindHostsByQueryString(server, oHostGroup, strQueryString):
    '''
        Find host by query
        params:
            server         - sever object
            oHostGroup     - HostGroup server object
            strQueryString - query for searching
        return:
            Host id
    '''

    strAccessor = oHostGroup.FindHosts(
        strQueryString,
        ['KLHST_WKS_HOSTNAME', 'KLHST_WKS_DN'],
        [],
        {'KLGRP_FIND_FROM_CUR_VS_ONLY': True},
        lMaxLifeTime = 60 * 60).OutPar('strAccessor')
    
    nStart = 0
    nStep = 100
    oChunkAccessor = KlAkChunkAccessor (server)    
    nCount = oChunkAccessor.GetItemsCount(strAccessor).RetVal()

    oResult = KlAkArray([])
    while nStart < nCount:
        oChunk = oChunkAccessor.GetItemsChunk(strAccessor, nStart, nStep).OutPar('pChunk')
        oHosts = oChunk['KLCSP_ITERATOR_ARRAY']
        for oObj in oHosts:
            oResult.Add(oObj.GetValue('KLHST_WKS_HOSTNAME'))
        nStart += nStep

    return oResult

def FindTask(oTasks, strDisplayName):
    """
        Find task by name
        params:
            oTasks         - server tasks object
            strDisplayName - task display name
        return:
            task id
    """

    strTaskIteratorId = oTasks.ResetTasksIterator(nGroupId=0,
        bGroupIdSignificant=False,
        strProductName=None,
        strVersion=None,
        strComponentName=None,
        strInstanceId=None,
        strTaskName=None,
        bIncludeSupergroups=True).OutPar("strTaskIteratorId")       
    nTaskId = None

    while True:
        pTaskData = oTasks.GetNextTask(strTaskIteratorId).OutPar("pTaskData")
        if pTaskData == None or len(pTaskData) == 0:
            break
        strDN = pTaskData["TASK_INFO_PARAMS"]["DisplayName"]
        if strDN == strDisplayName:
            nTaskId = pTaskData["TASK_UNIQUE_ID"]
            break
                        
    oTasks.ReleaseTasksIterator(strTaskIteratorId)
    return nTaskId

def GetKesVersion(oHostGroup, host_id):
    """
        Get installed KES version 
        params:
            oHostGroup - HostGroup server object
            host_id - A unique server-generated string for host
        return:
            kes version
    """

    res = oHostGroup.GetHostInfo(host_id, ["KLHST_APP_INFO"]).RetVal()
    kes_key = None
    for name in res["KLHST_APP_INFO"].GetNames():
        if name.lower() == "kes":
            kes_key = name
            break

    if kes_key and kes_key in res["KLHST_APP_INFO"]:
        kes_version = list(res["KLHST_APP_INFO"][kes_key].GetNames())[0]
        return kes_key, kes_version
    else:
        return None, None

def GetKeslVersion(oHostGroup, host_id):
    """
        Get installed KESL version
        params:
            oHostGroup - HostGroup server object
            host_id - A unique server-generated string for host
        return:
            kesl version
    """

    res = oHostGroup.GetHostInfo(host_id, ["KLHST_APP_INFO"]).RetVal()
    kesl_key = None
    for name in res["KLHST_APP_INFO"].GetNames():
        if name.lower() == "kesl":
            kesl_key = name
            break

    if kesl_key and kesl_key in res["KLHST_APP_INFO"]:
        kesl_version = list(res["KLHST_APP_INFO"][kesl_key].GetNames())[0]
        return kesl_key, kesl_version
    else:
        return None, None