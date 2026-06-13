from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = [
        line.strip()
        for line in f.read().splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="vrikshpath_erpnext",
    version="0.1.0",
    description="VrikshPath custom Frappe/ERPNext app — Prashang Technologies Pvt Ltd",
    author="Prashang Technologies",
    author_email="umesh@satyanamsoft.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
