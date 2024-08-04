import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

for p in ports:
    print(p)
    print(p.vid)
    print(p.pid)

print(len(ports), "ports found")
