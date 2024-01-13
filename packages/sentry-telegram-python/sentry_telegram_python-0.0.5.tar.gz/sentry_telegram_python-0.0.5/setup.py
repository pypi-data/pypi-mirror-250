#!/usr/bin/env pythonPath
# coding: utf-8
from setuptools import setup
from pathlib import Path
from sentry_telegram_python import __version__

# Read the contents of README.rst for the long description
readme_path = Path(__file__).parent / 'README.rst'

with readme_path.open('r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='sentry_telegram_python',
    version=__version__,
    packages=['sentry_telegram_python'],
    url='https://github.com/1Anchor/sentry-telegram',
    author='Yaroslav Romashenko',
    author_email='jaroslav.romashenko1@gmail.com',
    description='Plugin for Sentry which allows sending notification via Telegram messenger.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    license='MIT',
    entry_points={
        'sentry.plugins': [
            'sentry_telegram_python = sentry_telegram_python.plugin:TelegramNotificationsPlugin',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Bug Tracking',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: System :: Monitoring',
    ],
    include_package_data=True,
)
