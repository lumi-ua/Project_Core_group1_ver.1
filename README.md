## ProjectCore-group1-v2
CLI - Command Line Interface assistant

### create pipenv with Pipfile:
```
pipenv --python 3.8.10
```
```
pipenv install path==16.7.1
```
```
pipenv install rich==13.5.2
```
```
pipenv install pyreadline3==3.4.1
```
```
pipenv install pickleshare==0.7.5
```

### Run inside environment:
```
pipenv run python ./src/assistant.py
```

### Create requirements:
```
pipenv requirements > requirements.txt
```

### Build docker-file:
```
sudo docker build . -t pycore-g1-v2
```
