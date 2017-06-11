# The Gosper curve, also known as Peano-Gosper Curve, named after Bill Gosper,
# also known as the flowsnake (a spoonerism of snowflake), is a space-filling curve.
#
# It is a fractal object similar in its construction to the dragon curve and the Hilbert curve.
#
#
# Examples of use:
#
# python gosper.py --help
# python gosper.py 6
# python gosper.py 6 -o gosper_6.svg
# python gosper.py 6 -o gosper_6.gif

def create_gosper_fractal(max_level = 6):

    # Segment type and directions for pattern 1
    t1 = 'abbaaab'
    d1 = [0, 5, 3, 4, 0, 0, 1]

    # Segment type and directions for pattern 2
    t2 = 'abbbaab'
    d2 = [1, 0, 0, 4, 3, 5, 0]

    # Lambda function to determine new directions of generated line segments
    fAddModulo6 = lambda m, d: [(m + e)%6 for e in d]

    res = {}
    res[0] = {'s': 7.0**0.5, 't': ['a'], 'd': [0]}
    # Iterate on all level, creating each new level with the previous one
    for level in range(1, max_level+1):
        res[level] = {'s': res[level - 1]['s'] * (1.0/(7.0**.5)), 't':[], 'd' : []}
        for e, d in zip(res[level - 1]['t'], res[level-1]['d']):
            if e == 'a':
                res[level]['t'].extend(t1)
                res[level]['d'].extend(fAddModulo6(d, d1))
            else:
                res[level]['t'].extend(t2)
                res[level]['d'].extend(fAddModulo6(d, d2))
    return res


def generate_level(level):
    ''' convert the formal description of a level to a x, y curve
    '''
    # k1, k2 = cos(pi/3), sin(pi/3)
    k1, k2 = +0.5, +3.0**0.5 / 2.0
    d_cos = {0: +1.0, 1: +k1, 2: -k1, 3: -1.0, 4: -k1, 5: +k1}
    d_sin = {0: +0.0, 1: +k2, 2: +k2, 3: +0.0, 4: -k2, 5: -k2}
    scale = level['s']
    # scale = 1
    n = len(level['d']) + 1
    x, y = [0] * n, [0] * n
    for i, d in enumerate(level['d']):
        x[i + 1] = x[i] + scale * d_cos[d]
        y[i + 1] = y[i] + scale * d_sin[d]
    return x, y


def plot_level(max_level = 6, **kwargs):
    showAllLevel = kwargs.get('showAllLevel', False)
    filename = kwargs.get('filename', None)
    grid = kwargs.get('grid', False)
    tile = kwargs.get('tile', False)
    import matplotlib.pyplot as plt
    from math import sin, cos, atan
    fAdd = lambda m, d: [(m+e) for e in d]
    fRotateX = lambda c,s,x,y: [c * xx - s * yy for xx, yy in zip(x ,y)]
    fRotateY = lambda c,s,x,y: [s * xx + c * yy for xx, yy in zip(x, y)]
    alpha = atan((3**0.5)/5.0)
    fig, ax = plt.subplots()
    res = create_gosper_fractal(max_level)
    if showAllLevel:
        x_offset = 0.5
        for i in range(max_level, -1, -1):
            x, y = generate_level(res[i])
            c, s = cos(i * alpha), sin(i * alpha)
            xr, yr = fRotateX(c, s, x, y), fRotateY(c, s, x, y)
            ax.plot(fAdd( (+7.0**0.5 + x_offset) * i, xr), yr,  linewidth=0.5, color='C'+str(i))
        ax.set_aspect(1)
        plt.axis([-0.5, (+7.0**0.5 + x_offset) * (max_level+1) , -2.5, 1])
    else:
        x, y = generate_level(res[max_level])
        c, s = cos(max_level * alpha), sin(max_level * alpha)
        xr, yr = fRotateX(c, s, x, y), fRotateY(c, s, x, y)
        if tile:
            scale = +7.0**0.5
            for i in range(-2, 3):
                ax.plot(fAdd(i * scale, xr), yr,  linewidth=0.5, color='C'+str(i+2))
            for i in range(-2, 2):
                ax.plot(fAdd(scale*(i+0.5), xr), fAdd(+scale*3**0.5*0.5,yr),  linewidth=0.5, color='C'+str(i+5))
                ax.plot(fAdd(scale*(i+0.5), xr), fAdd(-scale*3**0.5*0.5,yr),  linewidth=0.5, color='C'+str(i+5))

            plt.axis([-0.5-2*7.0**0.5, +3*7.0**0.5+0.5 , -5.0, 3.0])
        else:
            ax.plot(xr, yr,  linewidth=0.5, color='k')
            plt.axis([-0.5, +7.0**0.5+0.5 , -2.5, 1])
        ax.set_aspect(1)
    if grid:
        ax.grid(True)
    else:
        ax.axis('off')
    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def create_animated_gif(maxRecursionLevel=6, filename='gosper_curve.gif', **kwargs):
    tile = kwargs.get('tile', False)
    grid = kwargs.get('grid', False)
    import subprocess
    generateLevel = lambda x: list(range(x)) + [x - i - 2 for i in range(x - 1)]
    cmd = 'convert -antialias -density 100 -delay 120 '
    for level in generateLevel(maxRecursionLevel + 1):
        cfilename = filename + '_' + '{0:03d}'.format(level) + '.png'
        cmd += cfilename + ' '
        plot_level(max_level=level, showAllLevel=False, filename=cfilename, tile=tile, grid=grid)
    cmd += filename
    subprocess.check_output(cmd.split(' '))


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate a gosper fractal curve')
    pa = parser.add_argument
    pa('level', type=int, help='number of recursion level. Reasonnable value is 6')
    pa('-t','--tile', action='store_true', help='boolean used to create a tiling of the generated curve')
    pa('-a', '--all', action='store_true', help='boolean used to display all levels (disable when tiling)')
    pa('-o', '--output', default=None, help='name of the generated file. If not provided, result will display on screen')
    pa('-g', '--grid', action='store_true', help='boolean used to display grid')
    args = parser.parse_args()
    if args.output and args.output.lower().endswith('gif'):
        create_animated_gif(maxRecursionLevel=args.level, filename=args.output, grid=args.grid, tile=args.tile)
    else:
        plot_level(args.level, showAllLevel=args.all, filename=args.output, grid=args.grid, tile=args.tile)


if __name__=='__main__':
    main()