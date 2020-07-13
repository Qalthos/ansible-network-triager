from setuptools import setup

setup(
    name="ansible-network-tools",
    version="1.0.0",
    description="A set of utility tools for the Ansible Network Team",
    url="http://github.com/ansible-network/ansible-network-triager",
    author="Ansible Network Team",
    license="GPLv3",
    packages=["triager"],
    install_requires=["pTable", "requests", "PyYAML"],
    entry_points={"console_scripts": ["triager=triager.__main__:main"]},
    zip_safe=False,
)
