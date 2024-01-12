from setuptools import setup, find_packages

setup(
    name='toolnvt',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'google-api-python-client',
        'PyQt5',
        'pytube',
        # Các thư viện khác cần thiết
    ],
    entry_points={
        'console_scripts': [
            'toolnvt = toolnvt.__main__:main'
        ]
    },
)
