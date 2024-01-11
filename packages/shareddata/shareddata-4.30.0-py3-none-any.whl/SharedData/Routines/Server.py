from SharedData.RealTime import RealTime
import time
import sys
import json

#TODO: DONT SERVE DATA IF TABLE IS NOT IN MEMORY

from SharedData.Logger import Logger
from SharedData.SharedData import SharedData
shdata = SharedData('SharedData.Routines.Server', user='master')

if len(sys.argv) >= 2:
    _argv = sys.argv[1:]
else:
    msg = 'Please specify IP and port to bind!'
    Logger.log.error(msg)
    raise Exception(msg)

args = _argv[0].split(',')
host = args[0]
port = int(args[1])
RealTime.runserver(shdata, host, port)

Logger.log.info('ROUTINE STARTED!')
while True:
    n = 0
    sendheartbeat = True
    # Create a list of keys before entering the loop
    client_keys = list(RealTime.clients.keys())
    for client_key in client_keys:
        n = n+1
        c = RealTime.clients.get(client_key)
        if c is not None:
            if 'table' in c:
                table = c['table'].table
                tf = c['transfer_rate']
                Logger.log.debug('#heartbeat#%.2fMB/s,%i:%s,%s' %
                                (tf,n, client_key.getpeername(), table.relpath))
            else:            
                Logger.log.debug('#heartbeat# %i:%s' %
                                (n, client_key.getpeername()))
            sendheartbeat = False
    if sendheartbeat:
        Logger.log.debug('#heartbeat#host:%s,port:%i' % (host, port))
    time.sleep(15)