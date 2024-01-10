# SeaVoice SDK V2

### How to publish this package

#### Prerequisite
1. cd in to this folder `SeaVoice/backend/sdk/v2`
2. pip install build twine

#### publish a version
1. change version in `pyproject.toml`
2. set up env values
   1. set PYPI_USER=...
   2. set PYPI_PASSWORD=...
3. source publish_package.sh
4. python3 -m build
5. python3 -m twine upload --skip-existing dist/* -u {username} -p {password}