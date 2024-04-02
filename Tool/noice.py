import platform
import os
import time

def play_sound():
    system = platform.system()
    if system == "Windows":
        import winsound
        winsound.Beep(500, 10000)
    elif system == "Linux" or system == "Darwin":
        os.system("play -nq -t alsa synth {} sine {}".format(1, 1000))

def main():
    # 在这里编写你的程序
    time.sleep(10)
    pass

if __name__ == "__main__":
    main()
    play_sound()
