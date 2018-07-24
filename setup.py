from setuptools import setup

setup(
    name='httpie-consul',
    description='Consul plugin for HTTPie.',
    long_description=open('README.md').read(),
    version='1.0.2',
    author='Arkadiusz Adamski',
    author_email='arkadiusz.adamski@gmail.com',
    license='BSD',
    url='https://github.com/ar4s/httpie-consul',
    download_url='https://github.com/ar4s/httpie-consul',
    py_modules=['httpie_consul'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.transport.v1': [
            'httpie_consul = httpie_consul:ConsulPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.7.0',
        'consulate>=0.6.0'
    ],
    test_suite='httpie_consul_tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Environment :: Plugins',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
