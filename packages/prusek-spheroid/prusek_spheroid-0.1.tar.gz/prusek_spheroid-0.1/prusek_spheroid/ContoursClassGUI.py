import os
import numpy as np
import cv2 as cv
from skimage.filters import threshold_sauvola, threshold_niblack
from skimage import img_as_ubyte
from sklearn.cluster import spectral_clustering
from skimage import color
from shapely import geometry
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time
from threading import Lock
import matplotlib.pyplot as plt
import Funkce as f
import json
import sys
import glob
from skimage.segmentation import flood
import zipfile



def check_window_size(window_size):
    return window_size + 1 if window_size % 2 == 0 else window_size

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def zip_folder(folder_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname=arcname)

class BaseImageProcessing:
    @staticmethod
    def sauvola(parameters, img_gray):
        window_size = check_window_size(int(parameters["window_size"]))
        closing_size = int(parameters["closing_size"])
        dilation_size = int(parameters["dilation_size"])

        thresh_sauvola = threshold_sauvola(img_gray, window_size=window_size)
        img_binary = img_as_ubyte(img_gray > thresh_sauvola)

        img_binary = np.invert(img_binary)
        img_binary = f.Dilation(f.Erosion(img_binary, closing_size), closing_size)
        img_binary = f.Dilation(img_binary, dilation_size)

        return img_binary

    @staticmethod
    def niblack(parameters, img_gray):
        window_size = check_window_size(int(parameters["window_size"]))
        closing_size = int(parameters["closing_size"])
        dilation_size = int(parameters["dilation_size"])
        k = parameters["k"]

        thresh_niblack= threshold_niblack(img_gray, window_size=window_size, k=k)
        img_binary = img_as_ubyte(img_gray > thresh_niblack)

        img_binary = np.invert(img_binary)
        img_binary = f.Dilation(f.Erosion(img_binary, closing_size), closing_size)
        img_binary = f.Dilation(img_binary, dilation_size)

        return img_binary

    @staticmethod
    def gaussian_adaptive(parameters, img_gray):
        window_size = check_window_size(int(parameters["window_size"]))
        closing_size = int(parameters["closing_size"])
        dilation_size = int(parameters["dilation_size"])
        k = parameters["k"]

        adaptive_threshold = cv.adaptiveThreshold(img_gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,
                                                   window_size, k)

        img_binary = img_as_ubyte(adaptive_threshold > 0)

        # Invert the binary image
        img_binary = np.invert(img_binary)

        # Apply closing operation
        img_binary = f.Dilation(f.Erosion(img_binary, closing_size), closing_size)

        # Apply dilation operation
        img_binary = f.Dilation(img_binary, dilation_size)

        return img_binary

    @staticmethod
    def region_grow(parameters, img_gray):
        tolerance_k = parameters["tolerance"]
        closing_size = int(parameters["closing_size"])
        dilation_size = int(parameters["dilation_size"])

        std_dev = np.std(img_gray)
        tolerance = std_dev * tolerance_k

        _, mask = cv.threshold(img_gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        mask = np.invert(mask)

        white_points = np.column_stack(np.where(mask == 255))

        image_center = (mask.shape[1] // 2, mask.shape[0] // 2)

        # Najděte nejbližší bod k středu obrázku
        nearest_point_index = np.argmin(np.linalg.norm(white_points - image_center, axis=1))
        seed_point = tuple(white_points[nearest_point_index])

        img_binary = flood(img_gray, seed_point, tolerance=tolerance, connectivity=2).astype(np.uint8)*255

        img_binary = f.Dilation(f.Erosion(img_binary, closing_size), closing_size)
        img_binary = f.Dilation(img_binary, dilation_size)

        return img_binary

    @staticmethod
    def mean_shift(parameters, img):
        k = parameters["k"]
        closing_size = int(parameters["closing_size"])
        dilation_size = int(parameters["dilation_size"])

        spatial_radius, color_radius =f.compute_optimal_radii(img, k)

        shifted = cv.pyrMeanShiftFiltering(img, spatial_radius, color_radius)

        shifted_gray = cv.cvtColor(shifted, cv.COLOR_BGR2GRAY)

        _, img_binary = cv.threshold(shifted_gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

        img_binary = np.invert(img_binary)
        img_binary = f.Dilation(f.Erosion(img_binary, closing_size), closing_size)
        img_binary = f.Dilation(img_binary, dilation_size)

        return img_binary


class Contours(BaseImageProcessing):
    def __init__(self, adresaDatasetu, adresa_output, projekt, algorithm, parameters, show_img, function):
        super().__init__()
        self.adresaDatasetu = adresaDatasetu
        self.output_json_path = f"{adresa_output}/{projekt}/CVAT/{algorithm}/annotations/instances_default.json"
        self.output_images_path = f"{adresa_output}/{projekt}/CVAT/{algorithm}/images"
        self.output_segmented_path = f"{adresa_output}/{projekt}/segmented_images/{algorithm}"
        self.zipfile_address = f"{adresa_output}/{projekt}/CVAT/{algorithm}"
        self.coco_data = f.initialize_coco_data()
        self.show_img = show_img
        self.projekt = projekt
        self.algorithm = algorithm
        self.parameters = parameters
        self.f = function
        self.counter = 1

        create_directory(self.output_segmented_path)
        create_directory(os.path.dirname(self.output_json_path))
        create_directory(self.output_images_path)

    def run(self):
        filenames = os.listdir(self.adresaDatasetu)
        for filename in glob.glob(os.path.join(self.adresaDatasetu, '*.bmp')):
            with open(os.path.join(os.getcwd(), filename), 'r'):
                img = cv.imread(filename)
                basename = os.path.basename(filename)

                cv.imwrite(f"{self.output_images_path}/{basename}", img)

                img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

                if self.algorithm == "Sauvola":
                    img_binary = self.sauvola(self.parameters, img_gray)
                elif self.algorithm == "Niblack":
                    img_binary = self.niblack(self.parameters, img_gray)
                elif self.algorithm == "Mean Shift":
                    img_binary = self.mean_shift(self.parameters, img)
                elif self.algorithm == "Region Grow":
                    img_binary = self.region_grow(self.parameters, img_gray)
                elif self.algorithm == "Gaussian":
                    img_binary = self.gaussian_adaptive(self.parameters, img_gray)
                else:
                    print(f"Algoritmus s názvem {self.algorithm} nenalezen.")
                    sys.exit(1)

                contours, hierarchy = cv.findContours(img_binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)
                height, width = np.shape(img_binary)

                if len(sorted_contours) > 0:
                    contour = max(sorted_contours, key=cv.contourArea)
                    for cnt in sorted_contours:
                        if f.check_contour_in_corners(cnt, width, height):
                            contour = cnt
                            break

                    cv.drawContours(img, [contour], -1, [0, 0, 255], 2)


                cv.imwrite(f"{self.output_segmented_path}/{basename}", img)
                self.coco_data = f.convert_contour_to_coco(contour, height, width, basename, self.counter,
                                                           self.coco_data)
                print(f"{self.counter}/{len(filenames)}")
                self.counter += 1

        print("dumping json...")
        with open(self.output_json_path, "w") as json_file:
            json.dump(self.coco_data, json_file)
        print("zipping folder...")
        zip_folder(self.zipfile_address, f"{self.zipfile_address}.zip")


        print("HOTOVO")


class IoU(BaseImageProcessing):
    def __init__(self, adresaAnotaci, adresaObrazku, adresa_output, projekt, algorithm):
        super().__init__()
        self.adresaAnotaci = adresaAnotaci
        self.adresaObrazku = adresaObrazku
        self.adresa_output = f"{adresa_output}/{projekt}/IoU"
        self.adresa_plots = f"{adresa_output}/{projekt}/IoU/plots"
        self.projekt = projekt
        self.algorithm = algorithm
        self.margin = 2

        create_directory(self.adresa_output)
        create_directory(self.adresa_plots)

        self.plot_lock = Lock()

        self.polygons_CVAT, self.img_names = f.load_anotations(
            os.path.join(self.adresaAnotaci, 'instances_default.json'))
        print(f"Načteno {len(self.img_names)} anotovaných obrázků")

    def process_and_compute_iou(self, img_name, parameters, lock):
        img = cv.imread(os.path.join(self.adresaObrazku, img_name))
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        if self.algorithm == "Sauvola":
            img_binary = self.sauvola(parameters, img_gray)
        elif self.algorithm == "Niblack":
            img_binary = self.niblack(parameters, img_gray)
        elif self.algorithm == "Mean Shift":
            img_binary = self.mean_shift(parameters, img)
        elif self.algorithm == "Region Grow":
            img_binary = self.region_grow(parameters, img_gray)
        elif self.algorithm == "Gaussian":
            img_binary = self.gaussian_adaptive(parameters, img_gray)
        else:
            print(f"Algoritmus s názvem {self.algorithm} nenalezen.")
            sys.exit(1)

        contours, _ = cv.findContours(img_binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)
        height, width = np.shape(img_binary)

        if len(sorted_contours) > 0:
            contour = max(sorted_contours, key=cv.contourArea)
            for cnt in sorted_contours:
                if f.check_contour_in_corners(cnt, width, height):
                    contour = cnt
                    break


            if len(contour) > 2:
                chain = [geometry.Point(coord[0, 0], coord[0, 1]) for coord in contour]
                polygon = geometry.Polygon([(point.x, point.y) for point in chain])
            else:
                polygon = geometry.Point(0, 0)
        else:
            polygon = geometry.Point(0, 0)

        with self.plot_lock:
            # plt.imshow(img_binary, cmap="gray")
            # plt.show()
            pass

        iou = f.IoU(self.projekt, self.algorithm, self.polygons_CVAT[self.img_names.index(img_name)], polygon, img_name, plot=False,
                    lock=lock, address=self.adresa_plots)

        return iou

    def run(self, parameters, save_txt):
        IoUbuffer = []

        lock = Lock()  # Create a Lock for thread-safe IoU calculations
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.process_and_compute_iou, img_name, parameters, lock): img_name for img_name in
                       self.img_names}

            for future in concurrent.futures.as_completed(futures):
                img_name = futures[future]
                iou = future.result()
                IoUbuffer.append([img_name, iou])


        IoUs = [entry[1] for entry in IoUbuffer]
        averageIoU = np.average(IoUs)

        if save_txt:
            rounded_parameters = {key: round(value, 2) for key, value in parameters.items()}
            np.savetxt(
                f"{self.adresa_output}/IoU:{round(averageIoU * 100, 2)}, {self.projekt}, {self.algorithm}, {rounded_parameters}.csv",
                [f"{entry[0]} - {round(100 * entry[1], 2)}%" for entry in IoUbuffer], delimiter=", ", fmt='% s')

        return averageIoU


