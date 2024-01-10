try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(
  name = 'pdf2techX',         # How you named your package folder (MyLib)
  packages=['pdf2techX'],   # Chose the same as "name"
  version = '1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'PDF2TEXT LIBRARY',   # Give a short description about your library
  author = 'TETE',                   # Type in your name
#   author_email = 'your.email@domain.com',      # Type in your E-Mail
#   url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
#   download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['PDF', 'TEXT', 'PDF2TEXT','PDF2TechX'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'PyPDF2',
          'PyMuPDF',
          'pythainlp',
          'bs4',
          'langchain==0.0.208',
          'langchainplus-sdk',
          'openapi-schema-pydantic',
          
      ],
  classifiers=[
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)