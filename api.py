from pymem import *
from pymem.process import *
from pymem.ptypes import RemotePointer
from flask import Flask, redirect, url_for, send_file, request, jsonify, request, send_file, Response, make_response, request, abort, current_app as app
import sys
import requests
import json

app = Flask(__name__)

pm = pymem.Pymem("echovr.exe")

@app.route('/')
def defaultResponse():
  return jsonify("Welcome to Mathie's Echo VR API, you can use /gameinfo to get more information about your game.")

gameModule = module_from_name(pm.process_handle, "echovr.exe").lpBaseOfDll
matchmakingModule = module_from_name(pm.process_handle, "pnsradmatchmaking.dll").lpBaseOfDll

def GetPtrAddr(base, offsets):
    remote_pointer = RemotePointer(pm.process_handle, base)
    for offset in offsets:
        if offset != offsets[-1]:
            remote_pointer = RemotePointer(pm.process_handle, remote_pointer.value + offset)
        else:
            return remote_pointer.value + offset

# Addresses
BaseCoords = GetPtrAddr(gameModule + 0x020A3138,[0x60, 0x2A0, 0xF8, 0xEA0, 0xD8, 0x134, 0x118])
BasePlayerList = GetPtrAddr(matchmakingModule + 0x009C49D8,[0x88, 0x0, 0x440, 0x28, 0x40, 0x378, 0x3C])

@app.route('/playerlist')
def playerlist():
    PlayerList = {"Player1":pm.read_string(BasePlayerList), "Player2":pm.read_string(BasePlayerList+0xD8), "Player3":pm.read_string(BasePlayerList+0x1B0), "Player4":pm.read_string(BasePlayerList+0x288), "Player5":pm.read_string(BasePlayerList+0x360), "Player6":pm.read_string(BasePlayerList+0x438), "Player7":pm.read_string(BasePlayerList+0x510), "Player8":pm.read_string(BasePlayerList+0x5E8), "Player9":pm.read_string(BasePlayerList+0x6C0), "Player10":pm.read_string(BasePlayerList+0x798)}
    return jsonify(PlayerList)

@app.route('/localplayer')
def LocalPlayer():
    LocalPlayerData = {"LocalPlayer":{"Coords":{"X":pm.read_float(BaseCoords),"Y":pm.read_float(BaseCoords+0x4),"Z":pm.read_float(BaseCoords+0x8)}}}
    return jsonify(LocalPlayerData)
    

if __name__ == "__main__":
  app.run("0.0.0.0", 8080)
