import os
import time
import win32gui
from pywinauto import Desktop

SIZE = 100_000
difs = [SIZE]
start = time.time()
for i in range(SIZE):
    ns1 = time.time_ns()
    def winEnumHandler( hwnd, ctx ):
        if win32gui.IsWindowVisible( hwnd ):
            name = win32gui.GetWindowText( hwnd )

    win32gui.EnumWindows( winEnumHandler, None )
    ns2 = time.time_ns()
    
    ns3 = time.time_ns()
    windows = Desktop(backend="uia").windows()
    for w in windows:
        name = w.window_text()
    ns4 = time.time_ns()
    print(str(ns4 - ns3) + " | " + str(ns2 - ns1))
    if (ns2 - ns1) != 0:
        difs.append((ns4 - ns3)/(ns2 - ns1))
al = 0
for elem in difs:
    al = al + elem
al = al / len(difs)
end = time.time()
os.system('cls')
print("Amount of tests: " + str(SIZE) + "\nTesting time: " + str(end - start) + "s")
print("In " + str(al) + " times faster")