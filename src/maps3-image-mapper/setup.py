from setuptools import setup

package_name = 'maps3-image-mapper'

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
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jellylapubuntu',
    maintainer_email='eliadwork16@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'image_mapper = maps3_image_mapper.service_run:main',  # Maps the 'image_publisher' command to service_run.py's main()
        ],
    },
)
