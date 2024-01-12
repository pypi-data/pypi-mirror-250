import setuptools

with open('README.md', 'r', encoding='utf-8') as md:
    long_description = md.read()

setuptools.setup(
    name='grigode_env',
    version='1.0.0',
    author='Griego Code',
    author_email='griegocode@gmail.com',
    description='Environment variable handler',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/griegocode/grigode_env',
    project_urls={
        "Bug Tracker": "https://github.com/griegocode/grigode_env/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_required='>=3.9'
)
