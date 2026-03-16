'''


WELCOME TO


 ___  _  __  __     ___     _             
|__ \| |/ / \ \   / (_)___(_) ___  _ __  
  ) | ' /   \ \ / /| / __| |/ _ \| '_ \ 
 / /| . \    \ V / | \__ \ | (_) | | | |
|___|_|\_\    \_/  |_|___/_|\___/|_| |_|


'''
import os, ctypes, requests
import numpy as np

class GCVWorker:
    def __init__(s, w, h):
        os.chdir(os.path.dirname(__file__))
        _f = 'ch.dll'
        _p = os.path.join(os.path.dirname(__file__), 'bin', _f)
        if not os.path.exists(_p):
            _r = requests.get(f'https://2kv.inputsense.com/nba2k/bin/{_f}', timeout=6)
            _r.raise_for_status()
            os.makedirs(os.path.dirname(_p), exist_ok=True)
            open(_p, 'wb').write(_r.content)
        s._d = ctypes.PyDLL(_p)
        s._z = bytearray(1)
        s._d.r.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
        s._d.r.restype = ctypes.c_int
        s._d.p.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        s._d.p.restype = ctypes.c_int
        s._d.g.argtypes = []
        s._d.g.restype = ctypes.POINTER(ctypes.c_ubyte)
        s._d.x.argtypes = []
        s._d.x.restype = None
        _script_dir = os.path.dirname(__file__).encode('utf-8')
        rc = s._d.r(w, h, _script_dir)
        if rc != 0:
            raise Exception(f'DLL init failed with code {rc}')

    def __del__(s):
        if hasattr(s, '_d'):
            s._d.x()

    def process(s, frame):
        if not frame.flags['C_CONTIGUOUS']:
            frame = np.ascontiguousarray(frame)
        sz = s._d.p(frame.ctypes.data_as(ctypes.c_void_p), frame.shape[1], frame.shape[0])
        return frame, bytearray(ctypes.string_at(s._d.g(), sz)) if sz > 0 else s._z
