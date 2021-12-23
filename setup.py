import setuptools

CDK_VERSION = ""
with open(".cdk_version") as f:
    CDK_VERSION = str(f.read())

setuptools.setup(
    name="cdk-template",
    version="0.0.1",
    description="An empty CDK Python app",
    long_description_content_type="text/markdown",
    author="author",
    package_dir={"": "cdk_template"},  # 存在するディレクトリを指定する必要がある
    packages=setuptools.find_packages(where="cdk-template"),
    install_requires=[
        f"aws-cdk.core=={CDK_VERSION}",
        f"aws-cdk.aws_iam=={CDK_VERSION}",
        f"aws-cdk.aws_sqs=={CDK_VERSION}",
        f"aws-cdk.aws_sns=={CDK_VERSION}",
        f"aws-cdk.aws_sns_subscriptions=={CDK_VERSION}",
        f"aws-cdk.aws_s3=={CDK_VERSION}",
        f"aws-cdk.assertions=={CDK_VERSION}",
        "boto3==1.20.5",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
