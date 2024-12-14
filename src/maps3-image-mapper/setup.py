from setuptools import find_packages, setup

package_name = 'maps3-image-mapper'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jellylapubuntu',
    maintainer_email='eliadwork16@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'image_mapper = maps3_image_mapper.service_run:main',  # Maps the 'image_publisher' command to service_run.py's main()
        ],
    },
)
