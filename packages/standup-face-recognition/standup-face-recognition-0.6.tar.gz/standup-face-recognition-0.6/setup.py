from setuptools import setup, find_packages
print('find packages: ', find_packages())
setup(
    name='standup-face-recognition',
    version='0.6',
    description='Standup helper: Detects and recognizes the person in the team.',
    author='Timo',
    packages=find_packages(),
    install_requires=[
    	'opencv-python',
    	'numpy',
    	'facenet-pytorch',
    	'torch==2.0.0',
    	'torchvision==0.15.1',
    	
    ],
    entry_points={
        'console_scripts': [
            'standup_face_recognition=standup_face_recognition.main:main',
        ],
    },
)
