from setuptools import setup

setup(name='jsonbind',
      description='a better json library',
      url='https://github.com/germanespinosa/jsonbind',
      author='german espinosa',
      author_email='germanespinosa@gmail.com',
      long_description=open('./jsonbind/README.md').read(),
      long_description_content_type='text/markdown',
      packages=['jsonbind'],
      install_requires=['requests'],
      license='MIT',
      include_package_data=True,
      version='0.0.18',
      zip_safe=False)
