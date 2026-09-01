from setuptools import setup, find_packages

with open("requirements.txt") as f:
    lines = f.read().strip().split("\n")
    install_requires = [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]

setup(
    name="petrol_pump_management",
    version="1.0.0",
    description="Petrol Pump Management Application for Frappe/ERPNext",
    author="Bizaxl Optimisations LLP",
    author_email="markcom@bizaxl.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
