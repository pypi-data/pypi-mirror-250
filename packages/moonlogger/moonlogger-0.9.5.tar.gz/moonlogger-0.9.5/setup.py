import os
import subprocess

try:
    import requests
except ImportError as err:
    pip_cmd = 'pip' if os.name == 'nt' else 'pip3'
    installation_cmd = f'{pip_cmd} install {err.name}'
    installation_result = subprocess.run(installation_cmd, shell=True)

    if installation_result.returncode == 0:
        import requests
    else:
        print(f"Failed to install {err.name}. Please install it manually.")


from setuptools import setup, find_packages


def get_readme_content(owner, repo, branch='main'):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents'
    response = requests.get(url)

    if response.status_code == 200:
        contents = response.json()
        readme_content = None

        for content in contents:
            if content['name'].lower() == 'readme.md':
                readme_url = content['download_url']
                readme_response = requests.get(readme_url)

                if readme_response.status_code == 200:
                    readme_content = readme_response.text
                    break

        return readme_content

    else:
        return None

setup(
    name='moonlogger',
    version='0.9.5',
    packages=find_packages(),
    install_requires=[
        'PyYAML',
        'prettytable',
        'avro',
        'protobuf'
    ],
    license='MIT License',
    author='Artem Reslaid',
    description='moon-logger, a Python logging library',
    long_description=get_readme_content('reslaid', 'moon'),
    long_description_content_type='text/markdown',
    url='https://github.com/reslaid/moon',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)