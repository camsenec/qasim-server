import ctypes
import numpy as np

class ColoringProblemSolver:
    def __init__(self, trotter_num, site_num):
        self.m = trotter_num
        self.n = site_num

    def solve(self):
        ans = 0.0

        lib = np.ctypeslib.load_library("libfort.so", ".")
        lib.qa_.argtypes = [
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
            ]
        lib.qa_.restype = ctypes.c_float

        fn = ctypes.byref(ctypes.c_int32(self.n))
        fm = ctypes.byref(ctypes.c_int32(self.m))

        ans = lib.qa_(fn, fm)

        print("done")
        print(ans)

        return ans


if __name__ == '__main__':

    simulator = ColoringProblemSolver(10,20)
    ans = simulator.solve()
    print("ans")
    print(ans)
