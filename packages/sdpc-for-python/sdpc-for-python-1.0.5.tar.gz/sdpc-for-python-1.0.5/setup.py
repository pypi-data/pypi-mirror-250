from setuptools import setup, find_packages


setup(
    name='sdpc-for-python',
    version='1.0.5',
    description='Python library for processing whole slide images (WSIs) in sdpc format',
    license='MIT License',

    url='https://github.com/WonderLandxD/sdpc-for-python',
    author='Jiawen Li',
    author_email='lijiawen21@mails.tsinghua.edu.cn',

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['numpy', 'opencv-python', 'Pillow']
)