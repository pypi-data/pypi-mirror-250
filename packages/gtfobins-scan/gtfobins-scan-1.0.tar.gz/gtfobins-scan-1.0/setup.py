from setuptools import setup, find_packages

setup(
    name="gtfobins-scan",
    version="1.0",
    description="Vulnerability Scanner for GTFOBins",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Vinal",
    url="https://github.com/vinal-2/GTFObins",
    license="GPL-3.0",
    scripts=["gtfobins_scan.sh"],
    entry_points={
        "console_scripts": [
            "gtfobins-scan=gtfobins_scan:main",
        ],
    },
    package_data={
        "": ["gtfobins_scan.sh"],
    },
)
