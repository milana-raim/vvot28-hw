# ВВОТ ДЗ №2


## Райманова Милана, 11-002


### Запуск приложения 

1. ```git clone https://github.com/milana-raim/vvot28-hw.git```
2. ```cd vvot28-hw/hw2```
3. ```pip install -r requirements.txt```
4. По пути .config/cloudphoto создать конфигурационный файл cloudphotorc
5. Добавить в cloudphotorc:

```
bucket = INPUT_BUCKET_NAME 
aws_access_key_id = INPUT_AWS_ACCESS_KEY_ID 
aws_secret_access_key = INPUT_AWS_SECRET_ACCESS_KEY 
region = ru-central1 
endpoint_url = https://storage.yandexcloud.net
```

6. ```python3 cloudphoto.py COMMAND [OPTIONS]```

COMMAND = {init,upload,download,list,delete,mksite}

Описание команд:

```python3 cloudphoto.py --help``` 
