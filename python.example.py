from ctypes import CDLL
_ = CDLL("./build/shared.so").main()
