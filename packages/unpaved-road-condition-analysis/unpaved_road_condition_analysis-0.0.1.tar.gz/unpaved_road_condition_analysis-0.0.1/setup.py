from setuptools import setup, find_packages

setup(
    name='unpaved_road_condition_analysis',
    version='0.0.1',
    author='Zhao Wang',
    author_email='wangzhao0217@gmail.com',
    description='A Python package for analyzing the condition of unpaved roads using machine learning and image processing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wangzhao0217/unpaved_road_condition_analysis.git',
    license='LICENSE',  # Replace 'LICENSE' with the name of your license file
    packages=find_packages(),
    install_requires=[
        'pandas==1.5.3',
        'imagecodecs',
        'autokeras==1.0.20',
        'tensorflow==2.15.0',
        'pycaret==3.2.0',
        'numpy==1.23.5',
        'opencv-python==4.9.0.80',
        'scikit-image==0.22.0',
        'seaborn==0.13.1'
        
        # 'pandas==1.5.3'
        # 'scikit-learn==1.2.2',  # Add the specific version if needed
        # 'opencv-python==4.9.0.80',
        # 'pillow==10.2.0',  # Add the specific version if needed
        # 'matplotlib',  # Add the specific version if needed
        # 'seaborn==0.13.1',
        # 'tensorflow==2.15.0',  # Add the specific version if needed       
        # 'tensorboard==2.15.1',
        # 'pycaret==3.2.0',
        # 'scikit-image==0.22.0',
        # 'protobuf==4.23.4'
        
        # Add any other dependencies your package needs
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # Update the license as needed
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.9',
)