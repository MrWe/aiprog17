import helper as hp

def read_file(file, screen_width, screen_height):
    f = open(file)
    x = []
    y = []
    points = []
    next(f)
    next(f)
    for line in f.readlines():
        l = line.strip().split(' ')
        if(len(l) != 3):
            continue
        x.append(float(l[1]))
        y.append(float(l[2]))

    x_min, x_max = hp.get_min_max(x)
    y_min, y_max = hp.get_min_max(y)
    for i in range(len(x)):
        curr_x = hp.translate(x[i], x_min, x_max, 10, screen_width-10)
        curr_y = hp.translate(y[i], y_min, y_max, 10, screen_height-10)

        points.append([curr_x,curr_y])

    return points, x_max, x_min, y_max, y_min


