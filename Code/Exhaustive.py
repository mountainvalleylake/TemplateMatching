import cv2
import numpy as np
import time
from scipy.stats.stats import pearsonr,spearmanr

test_img_file = 'D:\Study\Python Codes\TemplateMatching\Data\\test2.jpg'
ref_img_file = 'D:\Study\Python Codes\TemplateMatching\Data\\ref2.png'


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
                print("dist : ", dist)
                min_dist = dist
                yloc = ai
                xloc = aj
                dist_loc = dist
    print("XLOC, YLOC, DIST", xloc, yloc, dist_loc)
    cv2.rectangle(copy_img, (xloc, yloc), (xloc + ref_img_x, yloc + ref_img_y), (0, 0, 0), 2)
    cv2.arrowedLine(copy_img, (xloc - 30, yloc + 30), (xloc, yloc), (255, 255, 255), 2)
    cv2.imwrite('ext_output_gray.png', copy_img)


def exhaustive_rgb():
    global test_img_file, ref_img_file
    test_img = cv2.imread(test_img_file, cv2.IMREAD_COLOR)
    ref_img = cv2.imread(ref_img_file, cv2.IMREAD_COLOR)
    copy_img = test_img.copy()
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
            print("Window ",ai,aj)
            for ti in range(ref_img_x):
                for tj in range(ref_img_y):
                    aT = test_img[ai + ti, aj + tj]
                    tT = ref_img[ti, tj]
                    #dist += pearsonr(aT, tT)[0]
                    dist += sum(abs(aT - tT)**2)
            if min_dist > dist:
                print("dist : ", dist)
                min_dist = dist
                xloc = ai
                yloc = aj
                dist_loc = dist
    print("XLOC, YLOC, DIST", xloc, yloc, dist_loc)
    cv2.rectangle(copy_img, (xloc, yloc), (xloc + ref_img_x, yloc + ref_img_y), (0, 255, 0), 3)
    cv2.imwrite('ext_output_rgb.png', copy_img)


if __name__ == '__main__':
    time_start = time.clock()
    #exhaustive_rgb()
    exhaustive_grayscale()
    time_elapsed = (time.clock() - time_start)
    print("Total time taken ", time_elapsed)