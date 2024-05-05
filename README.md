## PythonCore-Assistant-v2
CLI - Command Line Interface assistant

### Creating virtual environment:
Create virtual environment using pipenv (Pipfile, Pipefile.lock will be create automatically):
```
pipenv --python 3.8.10
```
Follow to add all packages versions from **pip list**:
```
pipenv install django==4.2.8
pipenv install matplotlib==3.7.1
pipenv install scikit-learn==1.2.2
pipenv install tensorflow==2.13.0
pipenv install path==16.7.1
```

### Run app in environment:
```
pipenv run python ./src/assistant.py
```

### Create requirements.txt:
This necessary file required by Docker
```
pipenv requirements > requirements.txt
```

### Build docker-file:
```
sudo docker build . -t pycore-g1-v2
```

### Run docker-file:
To avoid Python error **"EOFError: EOF when reading a line"** occurs when you use the **input()** function: run image in **interactive mode** with the terminal attached:
```
sudo docker run -ti pycore-g1-v2
```

### Save docker-image to file by ID:
```
sudo docker save cf36593ab3a8 --output pycore-g1-v2.tar
```

### Load image from tar-archive (optional):
Using import:
```
sudo docker image import filename.tar image_name:image_tag
```

Linux version:
```
docker load < filename.tar
```

Windows version:
```
docker load -i filename.tar
```
