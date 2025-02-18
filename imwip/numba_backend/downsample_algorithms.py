"""
:file:      downsample_algorithms.py
:brief:     Downsample algorithms using numba kernels
:author:    Jens Renders
"""

# This file is part of ImWIP.
#
# ImWIP is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# ImWIP is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of
# the GNU General Public License along with ImWIP. If not, see <https://www.gnu.org/licenses/>.

import numpy as np
from .downsample_kernels import (
    cubic_downsampling_2D_kernel,
    cubic_downsampling_3D_kernel
)
import os

path = os.path.dirname(__file__)
cubic_2D_coefficients = np.loadtxt(path+"/../cpp_backend/cubic_2D_coefficients.inc", delimiter= ",", dtype=np.float32)
cubic_2D_coefficients_dx = np.loadtxt(path+"/../cpp_backend/cubic_2D_coefficients_dx.inc", delimiter= ",", dtype=np.float32)
cubic_2D_coefficients_dy = np.loadtxt(path+"/../cpp_backend/cubic_2D_coefficients_dy.inc", delimiter= ",", dtype=np.float32)

cubic_3D_coefficients = np.loadtxt(path+"/../cpp_backend/cubic_3D_coefficients.inc", delimiter= ",", dtype=np.float32)
cubic_3D_coefficients_dx = np.loadtxt(path+"/../cpp_backend/cubic_3D_coefficients_dx.inc", delimiter= ",", dtype=np.float32)
cubic_3D_coefficients_dy = np.loadtxt(path+"/../cpp_backend/cubic_3D_coefficients_dy.inc", delimiter= ",", dtype=np.float32)
cubic_3D_coefficients_dz = np.loadtxt(path+"/../cpp_backend/cubic_3D_coefficients_dz.inc", delimiter= ",", dtype=np.float32)


__all__ = [
    'downsample_2D',
    'downsample_3D'
]


def downsample_2D(
        f,
        f_lr,
    ):
    coeffs = cubic_2D_coefficients
    threads_per_block = (16, 16)
    num_blocks = ((f_lr.shape[0] + 15)//16, (f_lr.shape[1] + 15)//16)
    cubic_downsampling_2D_kernel[num_blocks, threads_per_block](
        f,
        f_lr,
        coeffs,
        False
    )
    return f_lr


def adjoint_downsample_2D(
        f,
        f_lr,
    ):
    coeffs = cubic_2D_coefficients
    threads_per_block = (16, 16)
    num_blocks = ((f_lr.shape[0] + 15)//16, (f_lr.shape[1] + 15)//16)
    cubic_downsampling_2D_kernel[num_blocks, threads_per_block](
        f,
        f_lr,
        coeffs,
        True
    )
    return f

def downsample_3D(
        f,
        f_lr,
    ):
    coeffs = cubic_3D_coefficients
    threads_per_block = (8, 8, 8)
    num_blocks = ((f_lr.shape[0] + 7)//8, (f_lr.shape[1] + 7)//8, (f_lr.shape[2] + 7)//8)
    cubic_downsampling_3D_kernel[num_blocks, threads_per_block](
        f,
        f_lr,
        coeffs,
        False
    )
    return f_lr


def adjoint_downsample_3D(
        f,
        f_lr,
    ):
    coeffs = cubic_3D_coefficients
    threads_per_block = (8, 8, 8)
    num_blocks = ((f_lr.shape[0] + 7)//8, (f_lr.shape[1] + 7)//8, (f_lr.shape[2] + 7)//8)
    cubic_downsampling_3D_kernel[num_blocks, threads_per_block](
        f,
        f_lr,
        coeffs,
        True
    )
    return f
