from setuptools import setup

setup(
    name='Maths Race',
    packages=['mathsrace'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-socketio',
        'eventlet'
    ],
)
