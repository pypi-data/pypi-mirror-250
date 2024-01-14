from setuptools import setup, find_packages
from pathlib import Path

VERSION = "0.0.1"
DESCRIPTION = "Scripts for logging CPU and GPU memory usage and subsequently plotting for analysis and debugging"
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="plot_and_log_memory_usage",
    version=VERSION,
    author="Tyler Lum",
    author_email="tylergwlum@gmail.com",
    url="https://github.com/tylerlum/plot_and_log_memory_usage",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["matplotlib", "tyro", "GPUtil", "psutil", "pandas"],
    keywords=["python", "memory", "usage", "plot", "logging"],
    entry_points={
        "console_scripts": [
            "log_memory_usage=plot_and_log_memory_usage.log_memory_usage:main",
            "plot_logged_memory_usage=plot_and_log_memory_usage.plot_logged_memory_usage:main",
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
