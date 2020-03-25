from Cango import ABCango


def test_ABCango():
    ip_range = "192.168.1.1/24"
    ports = "80,443,3306"
    cmd = ["masscan", "--ports", ports, ip_range]
    masscan = ABCango(cmd)
    masscan.run()
    print(masscan.finished)
    for item in masscan.genresult():
        if item:
            print(item)


if __name__ == "__main__":
    test_ABCango()
