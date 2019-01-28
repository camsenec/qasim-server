import ctypes
import numpy as np

class ColoringProblemSolver:
    def __init__(self, trotter_num, site_num):
        self.m = trotter_num
        self.n = site_num

    def solve(self):

        lib = np.ctypeslib.load_library("qa_simulator/libfort.so", ".")
        lib.qa_.argtypes = [
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int)
            ]
        lib.qa_.restype = ctypes.c_float

        fn = ctypes.byref(ctypes.c_int(self.n))
        fm = ctypes.byref(ctypes.c_int(self.m))

        ans = lib.qa_(fn, fm)

        return ans
