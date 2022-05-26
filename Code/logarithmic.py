import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import time

start_time = time.time()

org_test = cv2.imread("simpsons.jpg")
ref_= cv2.imread("barts_face.jpg")


test= cv2.cvtColor(org_test, cv2.COLOR_BGR2GRAY)
ref= cv2.cvtColor(ref_, cv2.COLOR_BGR2GRAY)

testImg = np.zeros((test.shape[0]+2*ref.shape[0],test.shape[1]+2*ref.shape[1]))
testImg[ref.shape[0]:test.shape[0]+ref.shape[0], ref.shape[1]:test.shape[1] +ref.shape[1]] = test

test_row, test_col= test.shape
ref_row, ref_col = ref.shape


p_row = (test_row-ref_row)//2
p_col = (test_col-ref_col)//2

k_row = math.ceil(math.log(p_row,2))
k_col = math.ceil(math.log(p_col,2))

d_row = math.pow(2, k_row - 1)
d_col = math.pow(2, k_col - 1)

class coord(object):
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y


def difference(m,n):
    diff_sum=0
    for i in range(m, m + ref_row):
        for j in range(n, n + ref_col):
            x= int(testImg[i][j])-int(ref[i-m][j-n])
            diff_sum = diff_sum + x*x
    return diff_sum

nine_coords=[]
x=0
y=0
diff=0


while True:
    nine_coords.append(coord(x - d_row, y - d_col))
    nine_coords.append(coord(x - d_row, y))
    nine_coords.append(coord(x - d_row, y + d_col))
    nine_coords.append(coord(x , y - d_col))
    nine_coords.append(coord(x , y ))
    nine_coords.append(coord(x , y + d_col))
    nine_coords.append(coord(x + d_row, y - d_col))
    nine_coords.append(coord(x + d_row, y ))
    nine_coords.append(coord(x + d_row, y + d_col))

    for i in range(0,9):
        temp_diff = difference(int(nine_coords[i].x) + int(p_row), int(nine_coords[i].y) + int(p_col))
        if i == 0:
            diff = temp_diff
            x = nine_coords[i].x
            y = nine_coords[i].y
        elif temp_diff < diff:
            diff = temp_diff
            x = nine_coords[i].x
            y = nine_coords[i].y
    if d_row==1 or d_col==1:
        break
    d_row = d_row//2
    d_col = d_col//2
    nine_coords=[]

min_m = x + p_row
min_n = y + p_col
print(min_m)
print(min_n)

print("--- %s seconds ---" % (time.time() - start_time))

cv2.rectangle(org_test, (int(min_n), int(min_m)), (int(min_n+ref_col), int(min_m+ref_row)), (255,0,0), 3)
plt.axis("off")
plt.imshow(cv2.cvtColor(org_test, cv2.COLOR_BGR2RGB))
plt.show()








