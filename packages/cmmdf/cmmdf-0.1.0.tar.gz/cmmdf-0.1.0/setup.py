from setuptools import setup, find_packages

setup(
    name='cmmdf',
    version='0.1.0',  # パッケージのバージョン
    author='Hiromu Abe',  # パッケージ作者の名前
    author_email='s2122072@stu.musashino-u.ac.jp',  # パッケージ作者のメールアドレス
    description='A short description of the package',  # パッケージの短い説明
    long_description=open('README.md').read(),  # パッケージ
    long_description_content_type='text/markdown', # long_descriptionのタイプ
    packages=find_packages(where='cmmdf'), # パッケージを探すディレクトリ
    package_dir={'': 'cmmdf'}, # パッケージのソースがあるディレクトリ
    install_requires=[ # 依存関係
    'numpy',
    'pandas',
    'torch',
    'scikit-learn',
    'torchvision',
    'Pillow'
    ],
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', # サポートするPythonのバージョン
    include_package_data=True, # パッケージデータを含むかどうか
    keywords='data fusion, multimodal, text, image', # パッケージに関連するキーワード
        # パッケージのコマンドラインインターフェースを定義します（もし提供する場合）
    entry_points={
        'console_scripts': [
            'cmmdf=cmmdf.cli:main',  # 'cromdf'コマンドで実行される関数
        ],
    },
)

