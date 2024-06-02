from setuptools import setup, find_packages

# Charge les dépendances à partir de requirements.txt
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="django-community-forum",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",  # Exemple de licence
    description="A Django package to manage a community forum.",
    long_description=open("README.md").read(),
    url="https://github.com/Django-Niger/django-community-forum.git",
    author="ISSAKA HAMA Barhamou",
    author_email="hamabarhamou@gmail.com",
    install_requires=required,
)
