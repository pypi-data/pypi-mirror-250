from setuptools import setup
from setuptools.extension import Extension

if __name__ == "__main__":
    setup(name="pngpy",
          version="1.0.0",
          description="Simple libpng image writing interface",
          author="Mariusz Krzyzok",
          keywords=["png", "libpng"],
          python_requires=">=3.5",
          platforms="All",
          readme="README.md",
          url="https://github.com/damemay/pngpy",
          ext_modules=[Extension("png", sources=['ppm.c'], libraries=["png"])]
          )
