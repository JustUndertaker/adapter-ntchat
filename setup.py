import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot-adapter-ntchat",
    version="0.3.4",
    author="JustUndertaker",
    author_email="806792561@qq.com",
    description="a wechat adapter for nonebot2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JustUndertaker/adapter-ntchat",
    packages=["nonebot.adapters.ntchat"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
    install_requires=["httpx==0.23.0"],
)
