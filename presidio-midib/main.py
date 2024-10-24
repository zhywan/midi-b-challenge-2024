import glob
from pathlib import Path
import matplotlib.pyplot as plt
import pydicom
from presidio_image_redactor import DicomImageRedactorEngine
import time

from presidio_analyzer import Pattern, PatternRecognizer
def compare_dicom_images(
    instance_original: pydicom.dataset.FileDataset,
    instance_redacted: pydicom.dataset.FileDataset,
    figsize: tuple = (11, 11)
) -> None:
    """
        将原始图像和编辑图像的 DICOM 像素数组显示为图像。

    参数
        instance_original (pydicom.dataset.FileDataset)： 单个 DICOM 实例（带 PHI 文本）。
        instance_redacted (pydicom.dataset.FileDataset)： 单个 DICOM 实例（经编辑的 PHI）。
        figsize（元组）： 图片尺寸，以英寸为单位（宽、高）
    """
    _, ax = plt.subplots(1, 2, figsize=figsize)
    ax[0].imshow(instance_original.pixel_array, cmap="gray")
    ax[0].set_title('Original')
    ax[1].imshow(instance_redacted.pixel_array, cmap="gray")
    ax[1].set_title('Redacted')
#实例化 DICOM 图像编辑引擎对象
engine = DicomImageRedactorEngine()
# Single DICOM (.dcm) file or directory containing DICOM files
input_path = 'E:/input' #input data path

# Directory where the output will be written
output_parent_dir = ('E:/result')   #output data path
# Redact text PHI from DICOM images
engine.redact_from_directory(
    input_dicom_path = input_path,
    output_dir = output_parent_dir,
    fill="contrast",
    use_metadata=True,
    allow_list=["[M]","[F]","[U]","PORTABLE","portable","upright","SEMI-ERECT","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"],
    #allow_list_match = "regex",
    save_bboxes=True # if True, saves the redacted region bounding box info to .json files in the output dir
)
# Original DICOM images
p = Path(input_path).glob("**/*.dcm")
original_files = [x for x in p if x.is_file()]

# Redacted DICOM images
p = Path(output_parent_dir).glob("**/*.dcm")
redacted_files = [x for x in p if x.is_file()]
for i in range(0, len(original_files)):
    original_file = pydicom.dcmread(original_files[i])
    redacted_file = pydicom.dcmread(redacted_files[i])

    compare_dicom_images(original_file, redacted_file)
    #time.sleep(5)
