from setuptools import setup, find_packages

setup(
    name="gomind_captchas",
    python_requires=">=3.6",
    version="0.0.2",
    description="GoMind captchas functions",
    url="https://github.com/GrupoDomini/gomind_captchas.git",
    author="JeffersonCarvalhoGD",
    author_email="jefferson.carvalho@grupodomini.com",
    license="unlicense",
    package_dir={'': 'src'},
    packages=["gomind_captchas", find_packages(where="src")],
    zip_safe=False,
    install_requires=[
        'selenium',
        'Pillow',
        'python-dotenv',
        'anticaptchaofficial',
        'pyautogui',
    ],
)
