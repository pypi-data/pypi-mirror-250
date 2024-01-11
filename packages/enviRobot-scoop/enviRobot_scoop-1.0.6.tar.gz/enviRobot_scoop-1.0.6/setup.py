import setuptools
# 若Discription.md中有中文 須加上 encoding="utf-8"
with open("README.md", "r",encoding="utf-8") as f:
    long_description = f.read()
    
setuptools.setup(
    name = "enviRobot_scoop",
    version = "1.0.6",
    author = "JcXGTcW",
    author_email="jcxgtcw@cameo.tw",
    description="enviRobot service that can be held by Scoop.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bohachu/ask_enviRobot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
    'fastapi>=0.99.1',
    'uvicorn>=0.23.2',
    'openai==1.6.1',
    'geocoder==1.38.1',
    'line-bot-sdk==2.4.2',
    'pandas>=2.1.4',
    'geopy==2.3.0',
    'selenium==4.7.2',
    'pyimgur==0.6.0',
    'pyyaml>=6.0',
    'python-dotenv==1.0.0',
    "plotly==5.16.1",
    "kaleido",
    "cameo-eco-query==1.0.8",
    "opencc==1.1.7",
    "cameo_geo_query>=1.0.2"]
    )