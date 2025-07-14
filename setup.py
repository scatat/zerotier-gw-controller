from setuptools import setup, find_packages

setup(
    name="zerotier-gateway-controller",
    version="1.0.0",
    description="Automated failover controller for ZeroTier network gateways",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Stephen Tan",
    author_email="stephen.tan@example.com",
    url="https://github.com/stephentan/zerotier-gateway-controller",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "PyYAML>=5.4",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
            "mypy",
        ]
    },
    entry_points={
        "console_scripts": [
            "zerotier-gateway-controller=zerotier_gateway_controller.cli:main",
        ]
    },
    include_package_data=True,

)
