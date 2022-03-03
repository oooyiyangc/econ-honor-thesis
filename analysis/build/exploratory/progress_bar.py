import sys


def start_progress(t):
    global progress_x
    progress_x = 0.00
    global title
    title = t

    sys.stdout.write("\r" + title + ": [" + "-" * 40 + "]" + " " + "0.0%")
    sys.stdout.flush()


def progress(x):
    global progress_x
    num_block = int(x * 40 // 100)
    sys.stdout.write(
        "\r" + title + ": [" + "#" * num_block + "-" * (40 - num_block) + "]" + " " + str(round(x, 1)) + "%")
    sys.stdout.flush()
    progress_x = x


def end_progress():
    sys.stdout.write("\r" + title + ": [" + "#" * 15 + " COMPLETE " + "#" * 15 + "] 100.0%")
    sys.stdout.flush()


# Test Version
if __name__ == "__main__":
    import time
    ITERATION = 30
    start_progress("Test")
    for i in range(ITERATION):
        progress(i / ITERATION * 100)
        time.sleep(0.1)
    end_progress()


