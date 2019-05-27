## MIYU API
- MIYU Project's Server side
- framework : `Django 2.2.1`
- language : `python 3.6.7`
- IDE : Pycharm community ver.
- packages :
    - 가상환경 : `virtualvenv`
    - rest api 작성을 위한 library : `djangorestframework 3.9.4`
    - `swagger-ui/redoc` custom을 위한 library : `drf-yasg 1.15.0`
    - For machine-learning
        - `Keras==2.2.4`
        - `tensorflow==1.13.1`
    - For data handling
        - `librosa==0.6.3`
        - `numpy==1.16.3`
        - `pandas==0.24.2`

### API Doc
- `swagger-ui` : <a href="http://13.125.247.188/swagger/">http://13.125.247.188/swagger/</a>
- `redoc` : <a href="http://13.125.247.188/redoc/">http://13.125.247.188/redoc/</a>

### Deploy

- AWS EC2 Linux t2.micro instance
- Server : `Nginx` 
- WSGI : `uWSGI`