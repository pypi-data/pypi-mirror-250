import os
import subprocess
import time
import uuid
from typing import Optional, Iterable

from jhammer.io import read_mat, save_mat

# CAVASS build path, default in installation is ~/cavass-build.
# If CAVASS build path is not in PATH or is not as same as default, set `CAVASS_PROFILE_PATH` to your CAVASS build path.
if os.path.exists(os.path.expanduser("~/cavass-build")):
    CAVASS_PROFILE_PATH = os.path.expanduser("~/cavass-build")
else:
    CAVASS_PROFILE_PATH = None


def env():
    if CAVASS_PROFILE_PATH is not None:
        PATH = f"{os.environ['PATH']}:{os.path.expanduser(CAVASS_PROFILE_PATH)}"
        VIEWNIX_ENV = os.path.expanduser(CAVASS_PROFILE_PATH)
        return {"PATH": PATH, "VIEWNIX_ENV": VIEWNIX_ENV}
    return None


def execute_cmd(cavass_cmd):
    p = subprocess.Popen(cavass_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env())
    r, e = p.communicate()
    try:
        r = r.decode()
    except UnicodeDecodeError:
        r = r.decode("gbk")
    e = e.decode().strip()
    if e:
        print(e)
    r = r.strip()
    return r


class ExecutionError(Exception):
    def __init__(self, command, inner_error=None, execution_result=None):
        self.command = command
        self.inner_error = inner_error
        self.execution_result = execution_result

    def __str__(self):
        msg = f"CAVASS operation failed. CAVASS command is {self.command} "
        if self.execution_result is not None:
            msg += f"Execution result is: {self.execution_result} "
        if self.inner_error is not None:
            msg += f"Inner error is: {self.inner_error}"
        return


def get_image_resolution(input_file):
    """
    Get (H,W,D) resolution of input_file.
    Args:
        input_file:

    Returns:
    """
    if not os.path.exists(input_file):
        raise FileExistsError(f"{input_file} does not exist.")
    cmd = f"get_slicenumber {input_file} -s"
    r = execute_cmd(cmd)
    if r:
        try:
            r = r.split("\n")[2]
            r = r.split(" ")
            r = tuple(map(lambda x: int(x), r))
            return r
        except Exception as error:
            raise ExecutionError(cmd, error, r)
    else:
        raise ExecutionError(cmd)


def get_voxel_spacing(input_file):
    """
    Get spacing between voxels.
    Args:
        input_file:

    Returns:

    """
    if not os.path.exists(input_file):
        raise FileExistsError(f"{input_file} does not exist.")
    cmd = f"get_slicenumber {input_file} -s"
    r = execute_cmd(cmd)
    if r:
        try:
            r = r.split("\n")[0]
            r = r.split(" ")
            r = tuple(map(lambda x: float(x), r))
            return r
        except Exception as error:
            raise ExecutionError(cmd, error, r)
    else:
        raise ExecutionError(cmd)


def read_cavass_file(input_file, first_slice=None, last_slice=None, sleep_time=1, ):
    """
    Load data of input_file.
    Use the assigned slice indices if both the first slice and the last slice are given.
    Args:
        sleep_time: set a sleep_time between saving and loading temp mat to avoid system IO error.
        first_slice: Loading from the first slice (included). Load from the inferior slice to the superior slice if first_slice is None.
        last_slice: Loading end at the last_slice (included). Load from the inferior slice to the superior slice if last_slice is None.
    """
    if not os.path.exists(input_file):
        raise FileExistsError(f"{input_file} does not exist.")
    tmp_path = "/tmp/cavass"
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path, exist_ok=True)

    output_file = os.path.join(tmp_path, f"{uuid.uuid1()}.mat")
    if first_slice is None or last_slice is None:
        cvt2mat = f"exportMath {input_file} matlab {output_file} `get_slicenumber {input_file}`"
    else:
        cvt2mat = f"exportMath {input_file} matlab {output_file} {first_slice} {last_slice}"
    execute_cmd(cvt2mat)
    time.sleep(sleep_time)
    ct = read_mat(output_file)
    os.remove(output_file)
    return ct


def copy_pose(skew_file, good_file, output_file):
    output_dir = os.path.split(output_file)[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    execute_cmd(f"copy_pose {skew_file} {good_file} {output_file}")


def save_cavass_file(output_file,
                     data,
                     binary=False,
                     size: Optional[Iterable] = None,
                     spacing: Optional[Iterable] = None,
                     reference_file=None):
    """
    Save data as CAVASS format. Do not provide spacing and reference_file at the same time.
    Recommend to use binary for mask files and reference_file to copy all properties.
    Args:
        output_file:
        data:
        binary: Save as binary data if True.
        size: Size for converting with dimensions of (H,W,D), default: the size of input data.
        spacing: Spacing for converted CAVASS file with dimensions of (H,W,D), default: 1mm.
        reference_file: Copy pose from the given file.
    """
    assert spacing is None or reference_file is None
    if reference_file is not None:
        if not os.path.exists(reference_file):
            raise FileExistsError(f"{reference_file} does not exist.")

    if size is None:
        size = data.shape
    size = " ".join(list(map(lambda x: str(x), size)))

    spacing = " ".join(list(map(lambda x: str(x), spacing))) if spacing is not None else ""

    output_path = os.path.split(output_file)[0]
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    tmp_files = []
    tmp_mat = os.path.join(output_path, f"tmp_{uuid.uuid1()}.mat")
    tmp_files.append(tmp_mat)
    save_mat(tmp_mat, data)

    if not binary:
        if reference_file is None:
            execute_cmd(f"importMath {tmp_mat} matlab {output_file} {size} {spacing}")
        else:
            tmp_file = os.path.join(output_path, f"tmp_{uuid.uuid1()}.IM0")
            tmp_files.append(tmp_file)
            execute_cmd(f"importMath {tmp_mat} matlab {tmp_file} {size}")
            copy_pose(tmp_file, reference_file, output_file)
    if binary:
        if reference_file is None:
            tmp_file = os.path.join(output_path, f"tmp_{uuid.uuid1()}.IM0")
            tmp_files.append(tmp_file)
            execute_cmd(f"importMath {tmp_mat} matlab {tmp_file} {size} {spacing}")
            execute_cmd(f"ndthreshold {tmp_file} {output_file} 0 1 1")
        else:
            tmp_file = os.path.join(output_path, f"tmp_{uuid.uuid1()}.IM0")
            tmp_files.append(tmp_file)
            execute_cmd(f"importMath {tmp_mat} matlab {tmp_file} {size}")

            tmp_file1 = os.path.join(output_path, f"tmp_{uuid.uuid1()}.BIM")
            tmp_files.append(tmp_file1)
            execute_cmd(f"ndthreshold {tmp_file} {tmp_file1} 0 1 1")
            copy_pose(tmp_file1, reference_file, output_file)

    for each in tmp_files:
        os.remove(each)


def bin_ops(input_file_1, input_file_2, output_file, op):
    """
    Execute binary operations.
    Args:
        op: Supported options: or, nor, xor, xnor, and, nand, a-b
    """
    output_dir = os.path.split(output_file)[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    cmd_str = f"bin_ops {input_file_1} {input_file_2} {output_file} {op}"
    execute_cmd(cmd_str)


def median2d(input_file, output_file, mode=0):
    """
    Perform median filter.
    Args:
        mode: 0 for foreground, 1 for background, default is 0
    """
    output_dir = os.path.split(output_file)[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    execute_cmd(f"median2d {input_file} {output_file} {mode}")


def export_math(input_file, output_file, output_file_type="matlab", first_slice=None, last_slice=None):
    """
    Export CAVASS format file to other formats.
    Args:
        input_file:
        output_file:
        output_file_type: Support export format: mathematica, mathlab, r, vtk.
        first_slice:
        last_slice: Export all slices if first slice or last slice is None
    """
    if first_slice or last_slice is None:
        resolution = get_image_resolution(input_file)
        first_slice, last_slice = 0, resolution[2] - 1
    output_dir = os.path.split(output_file)[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    execute_cmd(f'exportMath {input_file} {output_file_type} {output_file} {first_slice} {last_slice}')


def render_surface(input_bim_file, output_file):
    """
    Render surface of segmentation. The output file should with postfix of `BS0`.
    Note that the rendering script may be failed when saving surface file in extension disks.
    This may be caused by permission limitations and may be solved by outputting the surface file in a different disk.
    """
    output_dir, file_name = os.path.split(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    interpl_tmp_bim_file = os.path.join(output_dir, f"{uuid.uuid1()}.BIM")
    ndinterpolate_cmd = f"ndinterpolate {input_bim_file} {interpl_tmp_bim_file} 0 `get_slicenumber {input_bim_file} -s | head -c 9` `get_slicenumber {input_bim_file} -s | head -c 9` `get_slicenumber {input_bim_file} -s | head -c 9` 1 1 1 1 `get_slicenumber {input_bim_file}`"
    r = execute_cmd(ndinterpolate_cmd)
    if r.find("ERROR:") != -1:
        raise ValueError(f"Error was occured.\nERROR MESSAGE: {r}\n CAVASS COMMAND: {ndinterpolate_cmd}")

    gaussian_tmp_im0_file = os.path.join(output_dir, f"{uuid.uuid1()}.IM0")
    gaussian_cmd = f"gaussian3d {interpl_tmp_bim_file} {gaussian_tmp_im0_file} 0 1.500000"
    r = execute_cmd(gaussian_cmd)
    if r.find("ERROR:") != -1:
        raise ValueError(f"Error was occured.\nERROR MESSAGE: {r}\n CAVASS COMMAND: {gaussian_cmd}")

    render_cmd = f"track_all {gaussian_tmp_im0_file} {output_file} 1.000000 115.000000 254.000000 26 0 0"
    r = execute_cmd(render_cmd)
    if r.find("ERROR:") != -1:
        raise ValueError(f"Error was occured.\nERROR MESSAGE: {r}\n CAVASS COMMAND: {gaussian_cmd}")
    os.remove(interpl_tmp_bim_file)
    os.remove(gaussian_tmp_im0_file)
