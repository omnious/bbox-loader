#!/usr/bin/env python3

import os
import re
import sys
import platform
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion


_PACKAGE_NAME_POSTFIX = os.getenv("PACKAGE_NAME_POSTFIX", None)
if _PACKAGE_NAME_POSTFIX is None:
    PACKAGE_NAME_POSTFIX = ""
else:
    PACKAGE_NAME_POSTFIX = "-" + _PACKAGE_NAME_POSTFIX


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: "
                + ", ".join(e.name for e in self.extensions)
            )

        cmake_version = LooseVersion(
            re.search(r"version\s*([\d.]+)", out.decode()).group(1)
        )
        if cmake_version < "3.14.0":
            raise RuntimeError("CMake >= 3.14.0 is required")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + extdir,
            "-DPYTHON_EXECUTABLE=" + sys.executable,
        ]

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        if platform.system() == "Windows":
            cmake_args += [
                "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)
            ]
            if sys.maxsize > 2**32:
                cmake_args += ["-A", "x64"]
            build_args += ["--", "/m"]
        else:
            cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
            build_args += ["--", "-j2"]

        env = os.environ.copy()
        env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get("CXXFLAGS", ""), self.distribution.get_version()
        )

        cmake_args += [
            "-GNinja",
            "-DUSE_AVX_INSTRUCTIONS=ON",
            "-DUSE_SSE2_INSTRUCTIONS=ON",
            "-DUSE_SSE4_INSTRUCTIONS=ON",
            "-DDLIB_NO_GUI_SUPPORT=ON",
            "-DDLIB_USE_CUDA=OFF",
            "-DDLIB_JPEG_SUPPORT=OFF",
            "-DDLIB_PNG_SUPPORT=OFF",
            "-DDLIB_GIF_SUPPORT=OFF",
        ]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(
            ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env
        )
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=self.build_temp
        )


setup(
    name=f"bboxloader{PACKAGE_NAME_POSTFIX}",
    version="1.0.0",
    author="Adri?? Arrufat",
    author_email="adria.arrufat@omnious.com",
    description="Bounding box loader",
    long_description="Fast bounding box loader for big datasets",
    ext_modules=[CMakeExtension("bboxloader")],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
)
