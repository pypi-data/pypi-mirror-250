from setuptools import setup,find_packages

setup(
    name='happymath',
    version='0.0.1',
    author="Zou",
    author_email='1514117376@qq.com',
    description='Test vsrsion for happymath',
    classifiers=[# 分类索引 ，pip 对所属包的分类
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.8',
    ],
    license='MIT',
    # 需要安装的依赖
    install_requires=[
        'sympy', 'IPython', 'latex2sympy2', 'importlib',
    ]
)
