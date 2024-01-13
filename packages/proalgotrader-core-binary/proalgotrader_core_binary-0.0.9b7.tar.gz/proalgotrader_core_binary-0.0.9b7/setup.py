import setuptools

with open("requirements.txt") as fp:
    install_requires = fp.read().strip().split("\n")

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="proalgotrader_core_binary",
    version="0.0.9.beta7",
    description="ProAlgoTrader core",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krunaldodiya/proalgotrader_core_binary",
    author="Krunal Dodiya",
    author_email="kunal.dodiya1@gmail.com",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    package_data={"": ["*"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
