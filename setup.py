import io

from setuptools import setup, find_packages

# with io.open("README.rst", "rt", encoding="utf8") as f:
#     readme = f.read()

setup(
    name="activity",
    version="0.1.0",
    license="BSD",
    maintainer="Remigijus Bauzys",
    description="Activity logging API.",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"],
    extras_require={"test": ["pytest", "coverage"]},
)
