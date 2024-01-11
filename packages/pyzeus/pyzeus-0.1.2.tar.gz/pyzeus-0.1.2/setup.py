import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="pyzeus",
    version="0.1.2",
    description="The cors middleware that enables a FastAPI server to handle cors requests, specifically, on the router and individual route level. It also handles preflight requests :)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cerebrusinc/pyzeus.git",
    project_urls={
        "Bug Tracker": "https://github.com/cerebrusinc/pyzeus/issues",
    },
    author="Lewis Mosho Jr | Cerebrus Inc",
    author_email="hello@cerebrus.dev",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Typing :: Typed",
    ],
    packages=[
        "pyzeus",
    ],
    include_package_data=True,
    install_requires=["fastapi"],
    package_dir={"": "src"},
    python_requires=">=3.0",
)