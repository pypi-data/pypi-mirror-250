from setuptools import setup, find_packages

setup(
        name='color_with_tools',
        version='0.0.1',
        packages=find_packages(),
        entry_points={
                'console_scripts': [
                        # Add any command-line scripts here
                ],
        },
        author='菜鸟东',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown'
        # Add other metadata like author, author_email, description, etc.
)