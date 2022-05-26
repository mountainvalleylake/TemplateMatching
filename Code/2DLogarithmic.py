import cv2
import numpy as np
import time
import math
from scipy.stats.stats import pearsonr,spearmanr


test_img_file = 'D:\Study\Python Codes\TemplateMatching\Data\\test.png'
ref_img_file = 'D:\Study\Python Codes\TemplateMatching\Data\\ref.jpg'


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
    #p = min(int(window_x/2),int(window_y/2))
    px = int(window_x/2)
    py = int(window_y/2)
    kx = int(math.log(px,2))
    ky = int(math.log(py,2))
    dx = int(math.pow(2,kx-1))
    dy = int(math.pow(2,ky-1))
    #print(p)
    centre_x = int(test_image_x/2)
    centre_y = int(test_image_y/2)
    print("Initial centres ",centre_x,centre_y)
    xloc, yloc, dist_loc = 0, 0, 0
    min_dist, dist = 999999999, 0
    #ratio = 4
    while (dx >= 1 and dy >=1):
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
                #cv2.rectangle(copy_img, (xloc, yloc), (xloc + ref_img_x, yloc + ref_img_y), (255, 0, 255), 1)
        #p = int( p / 2)
        dx = int(dx/2)
        dy = int(dy/2)
        centre_x = xloc
        centre_y = yloc
        print("New centre ",centre_x,centre_y)
        #ratio = ratio * 2
    print("XLOC, YLOC, dist", xloc, yloc, dist_loc)
    cv2.rectangle(copy_img, (xloc, yloc), (xloc + ref_img_x, yloc + ref_img_y), (0, 0, 0), 2)
    cv2.arrowedLine(copy_img,(xloc-30,yloc+30),(xloc,yloc),(255,255,255),2)
    cv2.imwrite('log_output_gray.png', copy_img)

def logarithmic_rgb(param):
    global test_img_file, ref_img_file
    test_img = cv2.imread(test_img_file, cv2.IMREAD_COLOR)
    ref_img = cv2.imread(ref_img_file, cv2.IMREAD_COLOR)
    copy_img = test_img.copy()
    test_image_x = test_img.shape[0]
    test_image_y = test_img.shape[1]
    ref_img_x = ref_img.shape[0]
    ref_img_y = ref_img.shape[1]
    p = param
    print(p)
    window_x = test_image_x - ref_img_x
    window_y = test_image_y - ref_img_y
    centre_x = int(window_x / 2)
    centre_y = int(window_y / 2)
    xloc, yloc, dist_loc = 0, 0, 0
    min_dist, dist = 999999999999, 0
    while (p >= 1):
        array_of_points = generate_points_log(centre_x, centre_y, p)
        for points in array_of_points:
            x = points[0]
            y = points[1]
            print(x, y, p)
            #if (x + ref_img_x >= test_image_x or y + ref_img_y >= test_image_y):
            #    continue
            dist = 0
            for ti in range(ref_img_x):
                for tj in range(ref_img_y):
                    # if (x + ti >= test_image_x or y + tj >= test_image_y):
                    #     continue
                    aT = test_img[x + ti, y + tj]
                    tT = ref_img[ti, tj]
                    #dist += pearsonr(aT, tT)[0]
                    #print(sum(abs(aT - tT) ** 2))
                    dist = dist + sum(abs(int(aT) - int(tT)) ** 2)
            if min_dist > dist:
                print("dist : ", dist)
                min_dist = dist
                xloc = x
                yloc = y
                dist_loc = dist
        p = int(p / 2)
        centre_x = xloc
        centre_y = yloc
    print("XLOC, YLOC, dist", xloc, yloc, dist_loc)
    cv2.rectangle(copy_img, (xloc, yloc), (xloc + ref_img_x, yloc + ref_img_y), (0, 255, 0), 3)
    cv2.imwrite('log_output_rgb.png', copy_img)


if __name__ == '__main__':
    time_start = time.clock()
    logarithmic_grayscale()
    #logarithmic_rgb(16)
    time_elapsed = (time.clock() - time_start)
    print("Total time taken ", time_elapsed)