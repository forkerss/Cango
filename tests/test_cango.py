import time
from cango import Cango


def test_cango():
    cmd = ["python3", "-c", "[print(i) for i in range(100)]"]
    masscan = Cango(cmd)
    masscan.run()
    print(masscan.finished)
    # time.sleep(0.5)
    for item in masscan.genresult():
        if item:
            print(item)


if __name__ == "__main__":
    test_cango()
