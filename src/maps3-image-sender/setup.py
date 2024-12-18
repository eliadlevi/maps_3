from setuptools import find_packages, setup

package_name = 'maps3-image-sender'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name.replace('-', '_')],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_dir={'': 'src'},  # Map the package to 'src/'
    maintainer='jellylapubuntu',
    maintainer_email='eliadwork16@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'image_sender = maps3_image_sender.service_run:main',  # Maps the 'image_publisher' command to service_run.py's main()
        ],
    },

)
