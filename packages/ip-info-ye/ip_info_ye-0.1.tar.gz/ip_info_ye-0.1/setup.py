from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ip_info_ye',
    version='0.1',
    packages=['ip_info_ye'],
    install_requires=['requests'],
    author="SamiSoft - Yemen",
    url="https://github.com/mr-sami-x/ip_info_ye",
    description="This library is an advanced artificial intelligence to help with advanced and fast software and solutions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # تحديد الإصدار الأدنى من Python المطلوب
)
