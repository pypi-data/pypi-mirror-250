import os
import shutil
from uuid import uuid4

from jhammer.medical_image_converters import nifti2dicom

from cavasspy.ops import execute_cmd


def dicom2cavass(input_dir, output_file, offset_value=0):
    """
    Note that if the output file path is too long, this command may be failed.
    Args:
        input_dir:
        output_file:
        offset_value:

    """
    file_dir, file = os.path.split(output_file)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir, exist_ok=True)
    r = execute_cmd(f"from_dicom {input_dir}/* {output_file} +{offset_value}")
    return r


def nifti2cavass(input_file, output_file, offset_value=0, dicom_accession_number=1):
    """
    Convert nifti image to cavass image.
    Args:
        input_file:
        output_file:
        offset_value:
        dicom_accession_number:
    """
    save_path = os.path.split(output_file)[0]
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
    tmp_dicom_dir = os.path.join(save_path, f"{uuid4()}")
    r1 = nifti2dicom(input_file, tmp_dicom_dir, dicom_accession_number)
    r2 = dicom2cavass(tmp_dicom_dir, output_file, offset_value)
    shutil.rmtree(tmp_dicom_dir)
    return r1, r2
