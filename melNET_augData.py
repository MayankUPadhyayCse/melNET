import cv2
import numpy as np
import os.path
import os
from tkinter import *
import shutil


# Functions >>>
def show_image(_window_name, _image):
    cv2.namedWindow(_window_name, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(_window_name, _image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def load_images_from_folder(_folder_name):
    _image_list = []
    for _file_name in os.listdir(_folder_name):
        _img = cv2.imread(os.path.join(_folder_name, _file_name), cv2.IMREAD_COLOR)
        if _img is not None:
            _image_list.append(_img)
        else:
            print("Could not open or find any image in [" + _folder_name + "] folder!\n")
    return _image_list


def generate_aug_folders(_folder_list):
    if five_fold:
        path_root = "Data/Five_Fold_(Aug)"
        if os.path.exists(path_root):
            shutil.rmtree(path_root)  # Removing old dir.
            os.makedirs(path_root)
        else:
            os.makedirs(path_root)

        for x in range(fold_num):
            fold_path = path_root + "/Fold_" + str(x+1)
            os.makedirs(fold_path)
            set_path = path_root + "/Temp/Set_" + str(x+1)
            os.makedirs(set_path)

            # Set Folder
            for _folder in _folder_list:
                path_temp = set_path + "/" + _folder
                os.makedirs(path_temp)

            # Train Folder
            for _folder in _folder_list:
                path_temp = fold_path + "/Train/" + _folder
                os.makedirs(path_temp)

            # Test Folder
            for _folder in _folder_list:
                path_temp = fold_path + "/Test/" + _folder
                os.makedirs(path_temp)
    else:
        path = "Data/Single_Fold_(Aug)"
        if os.path.exists(path):
            shutil.rmtree(path)  # Removing old dir.
            os.makedirs(path)
        for _folder in _folder_list:
            path_temp = path + "/" + _folder
            os.makedirs(path_temp)


def copy_all(_src, _dst):
    src_files = os.listdir(_src)
    for file_name in src_files:
        full_file_name = os.path.join(_src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, _dst)


def file_naming(_img, process_initial, _folder, _set_counter):
    if five_fold:
        dst_root = "Data/Five_Fold_(Aug)/Temp/Set_" + str(_set_counter) + "/"
    else:
        dst_root = "Data/Single_Fold_(Aug)/"

    global name_counter
    name_counter += 1

    if rotationAngle is not None:
        # Rotation Code
        for angle in range(0, 360, rotationAngle):
            dim = _img.shape
            _scaleFactor = 1
            _rotationMatrix = cv2.getRotationMatrix2D((dim[1] / 2, dim[0] / 2), angle, _scaleFactor)
            _imgRotated = cv2.warpAffine(_img, _rotationMatrix, (dim[1], dim[0]), flags=cv2.INTER_LINEAR,
                                         borderMode=cv2.BORDER_REFLECT_101)
            _savingName = dst_root + _folder + "/" + _folder + "_" + str(name_counter) + "_" \
                                   + process_initial + "_Rot_" + str(angle) + ".jpg"
            cv2.imwrite(_savingName, _imgRotated)

    else:
        _savingName = dst_root + _folder + "/" + _folder + "_" + str(name_counter) + "_" + process_initial + ".jpg"
        cv2.imwrite(_savingName, _img)


def get_fold_ready():
    for fold_scroll in range(fold_num):
        fold_root = "Data/Five_Fold_(Aug)/Fold_" + str(fold_scroll+1)

        for set_scroll in range(fold_num):
            set_root = "Data/Five_Fold_(Aug)/Temp/Set_" + str(set_scroll+1)
            if set_scroll is fold_scroll:
                for _folder in folder_list:
                    _src = set_root + "/" + _folder
                    _dst = fold_root + "/Test/" + _folder
                    copy_all(_src, _dst)
            else:
                for _folder in folder_list:
                    _src = set_root + "/" + _folder
                    _dst = fold_root + "/Train/" + _folder
                    copy_all(_src, _dst)

    shutil.rmtree("Data/Five_Fold_(Aug)/Temp")  # Removing [Temp] Folder


# Main >>>

# Check-Box creation
root = Tk()
root.title("Augmentation Wizard")  # Title
pressed = False


# Check if the Start button is pressed or not
def button_pressed():
    root.destroy()
    global pressed
    pressed = True


# Check Box variables
_original = BooleanVar()
_histEqualization = BooleanVar()
_dilation = BooleanVar()
_erosion = BooleanVar()
_blur = BooleanVar()
_sharpen = BooleanVar()
_mirror = BooleanVar()
_rotate = BooleanVar()
_five_fold = BooleanVar()
_rotate_ang = IntVar(0)

# UI Creation
Checkbutton(root, text="Original", variable=_original).grid(row=0, sticky=W)
Checkbutton(root, text="Hist. Equalization", variable=_histEqualization).grid(row=1, sticky=W)
Checkbutton(root, text="Dilation", variable=_dilation).grid(row=2, sticky=W)
Checkbutton(root, text="Erosion", variable=_erosion).grid(row=3, sticky=W)
Checkbutton(root, text="Blur", variable=_blur).grid(row=4, sticky=W)
Checkbutton(root, text="Sharpen", variable=_sharpen).grid(row=5, sticky=W)
Checkbutton(root, text="Mirror", variable=_mirror).grid(row=6, sticky=W)
Checkbutton(root, text="Rotate All", variable=_rotate).grid(row=7, sticky=W)

angle_label1 = Label(root, text="Angle Span in Degrees: ").grid(row=7, column=2)
angle_label2 = Label(root, text="(Default: 45)").grid(row=8, column=2)
angle_entry = Entry(root, textvariable=_rotate_ang).grid(row=7, column=3)

Checkbutton(root, text="Five-Fold   (Default: Single-Fold)", variable=_five_fold).grid(row=10, sticky=W)
button1 = Button(root, text="Start", command=button_pressed, width=15).grid(row=11, sticky=W)

root.mainloop()

# Checking [Start] status
if pressed:
    original = _original.get()
    histEqualization = _histEqualization.get()
    dilation = _dilation.get()
    erosion = _erosion.get()
    blur = _blur.get()
    sharpen = _sharpen.get()
    mirror = _mirror.get()
    rotate = _rotate.get()
    five_fold = _five_fold.get()
    rot_ang = _rotate_ang.get()

    if (original is False and histEqualization is False and dilation is False and
            erosion is False and blur is False and sharpen is False and mirror is False):
        print("Nothing is Selected!")
        exit()
else:
    print("Augmentation Process has not been Started!")
    exit()

# Checking for a valid rotation angle
if rotate:
    if (rot_ang > 0) & (rot_ang < 360):
        rotationAngle = rot_ang
    else:
        rotationAngle = 45  # Default: 45
else:
    rotationAngle = None

# Number of folds
fold_num = 5  # For 5Folds

# Getting Sub-Folder names in [Data] folder
folder_list = []
if len(os.listdir("Data")) == 0:
    print("[Data] folder is empty!\n")
    exit()
else:
    for entry_name in os.listdir("Data"):
        if entry_name.find("Aug") < 0:  # Skipping old folders with Augmented data
            entry_path = os.path.join("Data", entry_name)
            if os.path.isdir(entry_path):
                folder_list.append(entry_name)
        else:
            continue
    if len(folder_list) == 0:  # All sub-folders contain augmented data
        exit()

# Generate folders for augmented images
generate_aug_folders(folder_list)

# Read, Process and Distribute images from Sub-Folders
name_counter = 0
for folder in folder_list:
    folderPath = "Data/" + folder
    image_list = load_images_from_folder(folderPath)
    set_counter = 0

    for img in image_list:
        set_counter += 1

        # Original Saving Code
        if original:
            file_naming(img, "O", folder, set_counter)

        # Histogram Equalization Code
        if histEqualization:
            ycbImage = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
            Y_channel, Cr, Cb = cv2.split(ycbImage)
            Y_channel = cv2.equalizeHist(Y_channel)
            ycbImage = cv2.merge([Y_channel, Cr, Cb])
            imgEqualized = cv2.cvtColor(ycbImage, cv2.COLOR_YCrCb2BGR)
            file_naming(imgEqualized, "HE", folder, set_counter)

        # Dilation Code
        if dilation:
            dilationSize = 1
            dilationElement = cv2.getStructuringElement(cv2.MORPH_CROSS, (2 * dilationSize + 1, 2 * dilationSize + 1),
                                                        (dilationSize, dilationSize))
            imgDilated = cv2.dilate(img, dilationElement)
            file_naming(imgDilated, "D", folder, set_counter)

        # Erosion Code
        if erosion:
            erosionSize = 1
            erosionElement = cv2.getStructuringElement(cv2.MORPH_CROSS, (2 * erosionSize + 1, 2 * erosionSize + 1),
                                                       (erosionSize, erosionSize))
            imgEroded = cv2.erode(img, erosionElement)
            file_naming(imgEroded, "E", folder, set_counter)

        # Blur Code
        if blur:
            kernelSize = 3
            imgBlur = cv2.medianBlur(img, kernelSize)
            file_naming(imgBlur, "B", folder, set_counter)

        # Sharpen Code
        if sharpen:
            sharpenElement = np.array((
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]), dtype="int")
            imgSharp = cv2.filter2D(img, -1, sharpenElement)
            file_naming(imgSharp, "S", folder, set_counter)

        # Mirror Code
        if mirror:
            imgMirror = cv2.flip(img, 1)
            file_naming(imgMirror, "M", folder, set_counter)

        if set_counter is fold_num:
            set_counter = 0

# Make five-fold ready
if five_fold:
    get_fold_ready()
