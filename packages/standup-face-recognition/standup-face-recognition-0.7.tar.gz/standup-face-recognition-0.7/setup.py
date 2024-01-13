from setuptools import setup, find_packages
print('find packages: ', find_packages())
setup(
    name='standup-face-recognition',
    version='0.7',
    description='Standup helper: Detects and recognizes the person in the team.',
    author='Timo',
    packages=find_packages(),
    package_data={'standup-face-recognition': ['standup-face-recognition/20180402-114759-vggface2.pt'], 'standup-face-recognition': ['standup-face-recognition/team_embedding.pth']},
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
