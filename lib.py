from xml.etree.ElementTree import Element, SubElement, tostring, fromstring, dump
from uuid import uuid4
from random import randint
from pathlib import Path
from os import listdir
from zipfile import ZipFile
import asyncio
import sys
import csv
import pandas as pd

def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped


def print_error(e: Exception) -> None:
    '''
        Общий обработчик ошибок
    '''
    sys.exit(str(e))


@background
def create_tmp_folders() -> None:
    '''
        Создает пустые временные директории для того, чтобы потом их содержимое закинуть в zip-архивы

        Особо сейчас нет времени, чтобы узнать как делать файлы на лету, не сохраняя. Гугл же показал только реализации через django-методы
    '''
    try:
        Path("tmp").mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print_error(e)

    for i in range(1, 51):
        try:
            Path("tmp/"+str(i)).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print_error(e)


def make_xml_string() -> str:
    '''
        Создает и возвращает xml-строку 
    '''
    root = Element('root')

    SubElement(root, "var", name='id', value=str(uuid4()))
    SubElement(root, "var", name='level', value=str(randint(1, 100)))
    root_objects = SubElement(root, 'objects')

    for _ in range(1, randint(1, 11)):
        SubElement(root_objects, 'object', value=str(uuid4()))

    return tostring(root, encoding='unicode', method='xml')

@background
def make_archive(name_tmp_folder: str) -> None:
    '''
        Генерирует xml-файлы во временных директориях и объединяет их в архив
    '''
    archive = ZipFile(f"res/{name_tmp_folder}.zip", mode='w')

    for xml_num in range(1, 101):
        try:
            with open(f"tmp/{name_tmp_folder}/{xml_num}.xml", 'w+') as f:
                f.write(make_xml_string())
        except Exception as e:
            print_error(e)

    xmls = [f for f in listdir(f"tmp/{name_tmp_folder}")]

    for filename in xmls:
        archive.write(f"tmp/{name_tmp_folder}/{filename}")
    
    archive.close()
