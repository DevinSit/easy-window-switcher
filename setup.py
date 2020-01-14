from setuptools import setup, find_packages

setup(
    name="EasyWindowSwitcher",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click>=7.0",
        "typing>=3.6.4"
    ],
    entry_points={
        "console_scripts": [
            "easywindowswitcher = easywindowswitcher.main:cli"
        ]
    }
)
