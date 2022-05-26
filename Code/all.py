import math
import cv2
import numpy as np
import time
from collections import deque


test_img_file = None
ref_img_file = None


def generate_points_log(x,y,dx,dy):
    #print('Generate points around a center')
    points = []
    array_of_points = []
    points.append(x - dx)
    points.append(y - dy)
    #print(points)
    array_of_points.append(points)
    points = []
    points.append(x - dx)
    points.append(y)
    #print(points)
    array_of_points.append(points)
    points = []
    points.append(x - dx)
    points.append(y + dy)
    #print(points)
    array_of_points.append(points)
    points = []
    points.append(x)
    points.append(y - dy)
    #print(points)
    array_of_points.append(points)
    points = []
    points.append(x)
    points.append(y)
    #print(points)
    array_of_points.append(points)
    points = []
    points.append(x)
    points.append(y+dy)
    #print(points)
    array_of_points.append(points)
    points = []
    points.append(x+dx)
    points.append(y-dy)
    #print(points)
    array_of_points.append(points)
    points = []
    points.append(x+dx)
    points.append(y)
    #print(points)
    array_of_points.append(points)
    points = []
    points.append(x+dx)
    points.append(y+dy)
    #print(points)
    array_of_points.append(points)
    return array_of_points


def logarithmic_grayscale():
    global test_img_file, ref_img_file
    test_img = cv2.imread(test_img_file)
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    ref_img = cv2.imread(ref_img_file)
    ref_img = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
    copy_img = cv2.imread(test_img_file,cv2.IMREAD_COLOR)
    #print(copy_img)
    test_image_x = test_img.shape[0]
    test_image_y = test_img.shape[1]
    ref_img_x = ref_img.shape[0]
    ref_img_y = ref_img.shape[1]
    print(test_image_x,test_image_y,ref_img_x,ref_img_y)
    window_x = test_image_x - ref_img_x
    window_y = test_image_y - ref_img_y
    print("window ",window_x,window_y)
    px = int(window_x/2)
    py = int(window_y/2)
    kx = int(math.log(px,2))
    ky = int(math.log(py,2))
    dx = int(math.pow(2,kx-1))
    dy = int(math.pow(2,ky-1))
    centre_x = int(test_image_x/2)
    centre_y = int(test_image_y/2)
    print("Initial centres ",centre_x,centre_y)
    xloc, yloc, dist_loc = 0, 0, 0
    min_dist, dist = 999999999, 0
    while (dx >= 1 or dy >=1):
        array_of_points = generate_points_log(centre_x, centre_y, dx,dy)
        for points in array_of_points:
            x = points[0]
            y = points[1]
            if (x + ref_img_x > test_image_x or y + ref_img_y > test_image_y or x < 0 or y < 0):
                continue
            print("Point & Difference ",x, y, dx, dy)
            dist = 0
            for ti in range(ref_img_x):
                for tj in range(ref_img_y):
                    #if(x+ti >= test_image_x or y+tj >= test_image_y):
                    #     continue
                    aT = test_img[x + ti, y + tj]
                    tT = ref_img[ti, tj]
                    dist += (int(tT) - int(aT)) ** 2
                    #dist += int(aT) * int(tT)
            #print("dist : ", dist)
            if min_dist > dist:
                print("min dist : ", dist)
                min_dist = dist
                xloc = y
                yloc = x
                dist_loc = dist
        dx = int(dx/2)
        dy = int(dy/2)
        centre_x = xloc
        centre_y = yloc
        print("New centre ",centre_x,centre_y)
    print("XLOC, YLOC, dist", xloc, yloc, dist_loc)
    cv2.rectangle(copy_img, (xloc, yloc), (xloc + ref_img_x, yloc + ref_img_y), (0, 0, 0), 2)
    cv2.arrowedLine(copy_img,(xloc-30,yloc+30),(xloc,yloc),(255,255,255),2)
    cv2.imwrite('log_output_gray.png', copy_img)


def hierarchical_grayscale(levels):
    global test_img_file, ref_img_file
    test_img = cv2.imread(test_img_file)
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    ref_img = cv2.imread(ref_img_file)
    ref_img = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
    copy_img = cv2.imread(test_img_file, cv2.IMREAD_COLOR)
    test_image_x = test_img.shape[0]
    test_image_y = test_img.shape[1]
    ref_img_x = ref_img.shape[0]
    ref_img_y = ref_img.shape[1]
    test_queue = deque()
    ref_queue = deque()
    t, r = None, None
    for l in range(levels):
        if l == 0:
            test_queue.appendleft(test_img)
            ref_queue.appendleft(ref_img)
            t = test_img
            r = ref_img
            continue
        blurt = cv2.blur(t, (4, 4))
        dimt = (int(t.shape[0] / 2), int(t.shape[1] / 2))
        rest = cv2.resize(blurt, dimt, interpolation=cv2.INTER_AREA)
        blurr = cv2.blur(r, (4, 4))
        dimr = (int(r.shape[0] / 2), int(r.shape[1] / 2))
        resr = cv2.resize(blurr, dimr, interpolation=cv2.INTER_AREA)
        test_queue.appendleft(rest)
        ref_queue.appendleft(resr)
        t = rest
        r = resr
    window_x = test_image_x - ref_img_x
    window_y = test_image_y - ref_img_y
    px = int(window_x / 2)
    py = int(window_y / 2)
    # kx = int(math.log(px, 2))
    # ky = int(math.log(py, 2))
    # dx = int(math.pow(2, kx - 1))
    # dy = int(math.pow(2, ky - 1))
    x = int(test_image_x/2)
    y = int(test_image_y/2)
    xl,yl,tempx,tempy = 0,0,0,0
    xloc, yloc, dist_loc = 0, 0, 0
    min_dist, dist = 999999999, 0
    for l in range(levels-1, -1, -1):
        if l==levels-1:
            kx = int(math.log(px, 2))
            ky = int(math.log(py, 2))
            dx = int(math.pow(2, kx - 1))
            dy = int(math.pow(2, ky - 1))
            tempx = int(dx/2**l)
            tempy = int(dy/2**l)
            xl = int(x / 2**l)
            yl = int(y / 2**l)
            print("xl yl", xl, yl)
        else:
            tempx = 1
            tempy = 1
            xl = int(2* xloc)
            #xloc = xl
            yl = int(2* yloc)
            #yloc = yl
            print("xl yl",xl,yl)
        array_of_points = generate_points_log(xl,yl,tempx,tempy)
        test = test_queue.popleft()
        ref = ref_queue.popleft()
        min_dist = 999999999
        for points in array_of_points:
            xp = points[0]
            yp = points[1]
            if (xp + ref.shape[0] > test.shape[0] or yp + ref.shape[1] > test.shape[1]):
                 continue
            #print("xp yp ", xp, yp)
            dist = 0
            for ti in range(ref.shape[0]):
                for tj in range(ref.shape[1]):
                    #if (xp + ti >= test.shape[0] or yp + tj >= test.shape[1]):
                    #     continue
                    aT = test[xp + ti, yp + tj]
                    tT = ref[ti, tj]
                    #dist += int(aT) * int(tT)
                    dist += (int(tT) - int(aT)) ** 2
            #print("dist : ", dist)
            if min_dist > dist:
                print("xp,yp,dist : ", dist,xp,yp)
                min_dist = dist
                xloc = yp
                yloc = xp
                dist_loc = dist
    #xloc = int(2*xloc)
    #yloc = int(2*yloc)
    print("XLOC, YLOC, Dist", xloc, yloc, dist_loc)
    cv2.rectangle(copy_img, (xloc, yloc), (xloc + ref_img_x, yloc + ref_img_y), (0, 0, 0), 2)
    cv2.arrowedLine(copy_img, (xloc - 30, yloc + 30), (xloc, yloc), (255, 255, 255), 2)
    cv2.imwrite('hier_output_gray.png', copy_img)


def exhaustive_grayscale():
    global test_img_file,ref_img_file
    test_img = cv2.imread(test_img_file)
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    ref_img = cv2.imread(ref_img_file)
    ref_img = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
    copy_img = cv2.imread(test_img_file, cv2.IMREAD_COLOR)
    test_image_x = test_img.shape[0]
    test_image_y = test_img.shape[1]
    ref_img_x = ref_img.shape[0]
    ref_img_y = ref_img.shape[1]
    window_x = test_image_x - ref_img_x
    window_y = test_image_y - ref_img_y
    xloc, yloc, dist_loc = 0, 0, 0
    min_dist, dist = 999999999999, 0
    for ai in range(window_x):
        for aj in range(window_y):
            dist = 0
            for ti in range(ref_img_x):
                for tj in range(ref_img_y):
                    aT = test_img[ai + ti, aj + tj]
                    tT = ref_img[ti, tj]
                    #dist += int(aT) * int(tT)
                    dist += (int(tT) - int(aT)) ** 2
            if min_dist > dist:
                #print("dist : ", dist)
                min_dist = dist
                yloc = ai
                xloc = aj
                dist_loc = dist
    print("XLOC, YLOC, DIST", xloc, yloc, dist_loc)
    cv2.rectangle(copy_img, (xloc, yloc), (xloc + ref_img_x, yloc + ref_img_y), (0, 0, 0), 2)
    cv2.arrowedLine(copy_img, (xloc - 30, yloc + 30), (xloc, yloc), (255, 255, 255), 2)
    cv2.imwrite('ext_output_gray.png', copy_img)


if __name__ == '__main__':
    ref_img_file = input("Enter Reference Image File : ")
    test_img_file = input("Enter Test Image File : ")
    time_start = time.clock()
    #exhaustive_grayscale()
    hierarchical_grayscale(3)
    #logarithmic_grayscale()
    time_elapsed = (time.clock() - time_start)
    print("Total time taken ", time_elapsed)