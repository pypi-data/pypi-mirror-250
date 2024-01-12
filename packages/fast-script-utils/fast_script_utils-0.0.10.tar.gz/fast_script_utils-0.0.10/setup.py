from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fast_script_utils",
    version='0.0.10',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["requests", "lxml"],  # 依赖列表，格式是 ['package>=version']
)
