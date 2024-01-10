from setuptools import setup, find_packages
setup(name='zeahoDateUtil',
      version='0.0.3',
      description='PYPI python util including date parsing and etc.',
      url='https://gitlab.zeaho.com/data/algorithm/zeaho-date-util',
      author='ZhuLingZhi',
      author_email='zhulingzhi917@163.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      platforms="any",
      install_requires=["python-dateutil"],
      zip_safe=False)