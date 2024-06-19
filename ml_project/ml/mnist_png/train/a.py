import os

directory = os.getcwd()

for dir_n in range(0, 10):
    dir_name = directory
    dir_name += "\\" + str(dir_n)
    
    cnt = 0
    for filename in os.listdir(dir_name):
        if filename.endswith(".png"):
            a = True
            
            while a:
                try:
                    os.rename(dir_name + "\\" + filename, dir_name + "\\" + str(cnt) + ".png")
                    a = False
                
                except Exception:
                    pass
                cnt += 1
