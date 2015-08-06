from sage.misc.temporary_file import tmp_filename

SUGAR_CMD = "/opt/sugar-v2-2-1/bin/sugar"

def sugar_input(b, s):
    r"""
    INPUT:

    - ``b`` - the bibd

    - ``s`` - integer

    OUTPUT:

    - a string that corresponds to the path to the temporary file created for
      the sugar input file

    EXAMPLES::

        sage: b = designs.balanced_incomplete_block_design(13,3)
        sage: filename = sugar_input(b,2)
        sage: print filename # random
        /home/jojo/.sage/temp/mangouste/6214/tmp_Ryb_nH
        sage: print open(filename).read()
        ; 2-arc for a (13,3,1)-bibd
        (int q_0 0 1)
        (int q_1 0 1)
        (int q_2 0 1)
        (int q_3 0 1)
        (int q_4 0 1)
        (int q_5 0 1)
        (int q_6 0 1)
        ...
        (le (+ q_5 q_7 q_8) 2)
        (le (+ q_6 q_7 q_10) 2)
        (le (+ q_6 q_8 q_12) 2)
        (le (+ q_7 q_9 q_12) 2)
        ;END
    """
    filename = tmp_filename()
    f = open(filename, "w")
    f.write("; {}-arc for a ({},{},1)-bibd\n".format(s,b.num_points(),len(b._blocks[0])))
    for p in b._points:
        f.write("(int q_{} 0 1)\n".format(p))
    f.write("(int m 0 ")
    l=str(len(b._points))
    f.write(l)
    f.write(") \n")
    f.write("(objective maximize m)\n")
    f.write("(= m (+ ")
    for p in b._points:
        f.write(" q_{}".format(p))
    f.write("))\n")
    for bl in b._blocks:
        f.write("(le (+")
        for i in bl:
            f.write(" q_{}".format(i))
        f.write(") {})\n".format(s))
    f.write(";END")
    f.close()

    return filename

def arc_sugar(b, s, verbose=False):
    r"""
    INPUT:

    - ``b`` -- the bibd

    - ``s`` -- positive integer

    EXAMPLES::

        sage: b = designs.balanced_incomplete_block_design(13,3)
        sage: arc_sugar(b,2)
        [0, 3, 4, 6, 11, 12]
    """
    # run sugar
    from subprocess import Popen, PIPE
    filename = sugar_input(b,s)
    args = [SUGAR_CMD, filename]
    sugar_proc = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    ans,err = sugar_proc.communicate()  # run the command
    ret_code = sugar_proc.poll()        # retrieve the output of the command

    if ret_code:
        raise RuntimeError("sugar returned {}".format(ret_code))

    #  parse the output
    v = {}
    if verbose:
        print ans
    for line in ans.splitlines():
        line = line.replace('\t', ' ').split(' ')
        if line and line[0] == 'a' and len(line) == 3:
            v[line[1]] = int(line[2])
    a = [b._points[i] for i in range(b.num_points()) if v['q_{}'.format(i)]]

    # quick check that the answer is an arc
    sa = set(a)
    for block in b.blocks():
        if len(sa.intersection(block)) > s:
            raise RuntimeError("wrong output {} from sugar. It intersects the block {} more than s={} times".format(a, block, s))

    # return the value
    return a
