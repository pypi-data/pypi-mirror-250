from setuptools import setup, find_packages

setup(
    name="anime_king_r",
    version='0.1.0',
    author='GhoulKingR',
    author_email='oduahchigozie46@gmail.com',
    description='An anime bot to download your favourite animes',
    url='https://github.com/GhoulKingR/anime-bot',
    # scripts=['./scripts/anime-bot'],
    packages=find_packages(),
    license='MIT',
    install_requires=[
        "requests == 2.31.0",
        "selenium == 4.16.0",
        "tqdm == 4.66.1",
        "setuptools",
    ],
    entry_points={
        "console_scripts": [
            "akr-download = anime_king_r:main"
        ]
    }
)