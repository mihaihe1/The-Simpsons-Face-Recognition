import os
import numpy as np
import cv2 as cv


def intersection_over_union(bbox_a, bbox_b):
	x_a = max(bbox_a[0], bbox_b[0])
	y_a = max(bbox_a[1], bbox_b[1])
	x_b = min(bbox_a[2], bbox_b[2])
	y_b = min(bbox_a[3], bbox_b[3])

	inter_area = max(0, x_b - x_a + 1) * max(0, y_b - y_a + 1)

	box_a_area = (bbox_a[2] - bbox_a[0] + 1) * (bbox_a[3] - bbox_a[1] + 1)
	box_b_area = (bbox_b[2] - bbox_b[0] + 1) * (bbox_b[3] - bbox_b[1] + 1)

	iou = inter_area / float(box_a_area + box_b_area - inter_area)

	return iou


root_path = "../antrenare/"

names  = ["bart", "homer", "lisa", "marge"]

image_names = []
bboxes = []
characters = []
nb_examples = 0
width_hog = 36
height_hog = 36
idx = 0

for name in names:
	filename_annotations = root_path + name + ".txt"
	f = open(filename_annotations)
	l1 = f.readline()
	im = root_path+name+"/"+"pic_0000.jpg"
	a = l1.split(os.sep)[-1]
	b = a.split(" ")
	bbox_curent = [[int(b[1]), int(b[2]), int(b[3]), int(b[4])]]
	for line in f:
		a = line.split(os.sep)[-1]
		b = a.split(" ")

		image_name = root_path + name + "/" + b[0]
		if im != image_name:
			cnt = 0
			img = cv.imread(im)
			num_rows = img.shape[0]
			num_cols = img.shape[1]
			while cnt < 5:
				x = np.random.randint(low=0, high=num_cols - width_hog)
				y = np.random.randint(low=0, high=num_rows - height_hog)

				bbox_rand = [x, y, x + width_hog, y + height_hog]

				xmin = bbox_rand[0]
				ymin = bbox_rand[1]
				xmax = bbox_rand[2]
				ymax = bbox_rand[3]
				ok = True
				iou = 0
				for x1, y1, x2, y2 in bbox_curent:
					iou = intersection_over_union([x1, y1, x2, y2], bbox_rand)
					im_af = img[ymin:ymax,xmin:xmax]
					# cv.imshow("test", im_af)
					# cv.waitKey(0)
					#
					# # closing all open windows
					# cv.destroyAllWindows()
					if iou > 0.01:
						ok = False
						break

				if ok:
					negative_example = img[ymin:ymax, xmin:xmax]
					filename = "../data/exempleNegative/" + str(idx) + "_" + str(cnt) + ".jpg"
					print(filename, iou)
					cv.imwrite(filename, negative_example)
					cnt += 1

			im = image_name
			bbox_curent = []
			idx += 1

		bbox = [int(b[1]),int(b[2]),int(b[3]),int(b[4])]
		bbox_curent.append(bbox)
		character = b[5][:-1]

		image_names.append(image_name)
		bboxes.append(bbox)
		characters.append(character)
		nb_examples = nb_examples + 1

# width_hog = 36
# height_hog = 36
#
#
#
# #compute negative examples using 36 X 36 template
#
# for idx, img_name in enumerate(image_names):
# 	print(idx,img_name)
# 	img = cv.imread(img_name)
# 	print("img shape")
# 	print(img.shape)
#
# 	num_rows = img.shape[0]
# 	num_cols = img.shape[1]
#
# 	#genereaza 10 exemple negative fara sa compari cu nimic, iei ferestre la intamplare 36 x 36
# 	for i in range(5):
#
# 		x = np.random.randint(low=0, high=num_cols - width_hog)
# 		y = np.random.randint(low=0, high=num_rows - height_hog)
#
# 		bbox_curent = [x, y, x + width_hog, y + height_hog]
#
# 		xmin = bbox_curent[0]
# 		ymin = bbox_curent[1]
# 		xmax = bbox_curent[2]
# 		ymax = bbox_curent[3]
# 		negative_example = img[ymin:ymax,xmin:xmax]
# 		filename = "../data/exempleNegative/" + str(idx) + "_" + str(i) + ".jpg"
# 		cv.imwrite(filename,negative_example)
