from distutils.core import setup
setup(name='duckduckgo',
	  version='0.1.0',
      install_requires=['requests>=1.4.0', 'lxml>=3.2.0'],
	  py_modules=['duckduckgo'],
	  data_files=[('/usr/bin', ['ddg'])])

