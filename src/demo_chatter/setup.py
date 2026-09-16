from glob import glob

from setuptools import find_packages, setup

package_name = 'demo_chatter'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', [f'resource/{package_name}']),
        (f'share/{package_name}', ['package.xml']),
        (f'share/{package_name}/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ricardo Ochoa',
    maintainer_email='tu@correo.com',
    description='Demo ROS 2 para el flujo Docker + Git + GitHub',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'talker = demo_chatter.talker:main',
            'listener = demo_chatter.listener:main',
        ],
    },
)
