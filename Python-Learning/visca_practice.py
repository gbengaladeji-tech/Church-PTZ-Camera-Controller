# We want 
#Camera 1
# Move left
# Pan speed = 05
# Tilt speed = 05
# Hexadecimal calculation: Y * 16 + X
# 8x 01 06 01 VV WW H V FF (01, 06, 01 is the command for pan and tilt and will stay how they are)
#----------------------------------------------------------
#8x = camera address
#01 = command
#06 = pan/tilt category
#01 = pan/tilt drive
#VV = pan speed
#WW = tilt speed
#H = horizontal direction
#V = vertical direction
#FF = end of packet
#----------------------------------------------------------
camera_header = 129 # 8 * 16 + 1
pan_speed =  5 # 0 x 16 + 5
tilt_speed = 5 # 0 x16 + 5
horizontal = 0x01 
vertical =  0x03
# Now we will write a Packet in this order.
packet = [
camera_header,
0x01,
0x06,
0x01,
pan_speed,
tilt_speed,
horizontal,
vertical,
0xFF
]
print(packet)
# What we just did is took a command from a hardware manuel and repersented it in python
for value in packet:
    print(f"{value:02X}", end=" ")
    #f"..." = formatted text
# value = the number
# 02 = always use at least 2 digits
# X = show it in uppercase hexadecimal
# when we add end=" " we are telling puthon to add a space instead of printing a new line for each
# We just made a loop, a loop is like telling python instructions on what to do over and over again
