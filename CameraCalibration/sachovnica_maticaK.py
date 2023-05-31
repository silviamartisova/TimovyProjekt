import cv2
import numpy as np
import cv2 as cv

# Načítanie obrázku kamery
img = cv2.imread(f'sachovnica.jpg')
img_size = (img.shape[1], img.shape[0])

# Načítanie obrázku šachovnice
pattern = cv2.imread(f'sachovnica.jpg')

# Definovanie počtu stĺpcov a riadkov šachovnice
pattern_size = (6, 9)

# Hľadanie rohov šachovnice na obrázku
found, corners = cv2.findChessboardCorners(pattern, pattern_size)

# Vytvorenie zoznamu rohov pre každý obrázok
object_points = []
image_points = []

found, corners = cv2.findChessboardCorners(img, pattern_size)
if found:
    # Pridanie rohov šachovnice do zoznamu
    object_points.append(np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32))
    object_points[-1][:,:2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
    image_points.append(corners)

# Výpočet vnútorných parametrov kamery
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, img_size, None, None)

# Získanie vnútorných parametrov kamery
fx = mtx[0][0]
fy = mtx[1][1]
cx = mtx[0][2]
cy = mtx[1][2]

print(f"Obr: Fx::{fx}, fy: {fy}, cx: {cx}, cy:{cy}")
