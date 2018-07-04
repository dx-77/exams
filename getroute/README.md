# GetRoute
 Скрипт для определения маршрута движения автомобиля между N ≤ 4 точек. 
 Входная информация (наименования городов\населенных пунктов), вывод должен содержать:
* координаты всех внесенных точек;
* дистанцию на маршруте в км;
* ориентировочное время в пути;


Для получения геоданных можно пользоваться любыми бесплатными веб-сервисами,
для получения данных о маршруте – open-source проектом project-osrm.org.

A script for seartching car route between 4 localities


For run use must use Python 3.6+

pip install -r requirements.txt
python getroute.py

on Linux:
python3 getroute.py