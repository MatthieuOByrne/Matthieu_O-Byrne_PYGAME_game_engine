import time as time

frames = ["frame1.png", "frame2.png", "frame3.png", "frame4.png"]
i = 0
while True:
    time.sleep(1)
    print(frames[i])
    i = (i+1) % len(frames)