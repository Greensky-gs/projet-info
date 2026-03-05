from ctypes import CDLL
game = CDLL("./build/shared.so")
_ = game.main()
