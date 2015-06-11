def arc(s, filename):
    f = open(filename, "w")
    for p in s._points:
        f.write("(int q_{} 0 1)\n".format(p))
    for b in s._blocks:
        f.write("(weightedsum(")
        for i in b:
            f.write(" (1 q_{})".format(i))
        f.write(") le 2)\n")
    f.close()
