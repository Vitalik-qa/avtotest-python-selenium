import unittest
import sys
import pytest
import os
import time
import datetime
import re
import multiprocessing
import random
import urllib.request
import tracemalloc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class test_1 (unittest.TestCase):

    def test_pucture(self):
        # Подключаем веб браузер
        s = Service('C:/Users/Виталий/Desktop/Autotest/chromedriver/chromedriver.exe')
        self.driver = webdriver.Chrome(service=s)
        driver = self.driver

        # Проверка наличия элемента
        def check(xpath):
            try:
                driver.find_element_by_xpath(xpath)
            except NoSuchElementException:
                return False
            return True

        # Открываем Яндекс
        driver.get("https://yandex.ru/images/")

        # Открываем окно на весь экран
        driver.maximize_window()

        # Проверка
        assert "Яндекс" in driver.title
        assert "No results found." not in driver.page_source
        print("\n")
        arr = []
        for i in range(1, 5):
            # // *[ @class = 'PopularRequestList'] / div[2]
            images = driver.find_element(By.XPATH, "//*[@class ='PopularRequestList']/div[" + str(i) + "]")
            print(i)
            print(images.text)
            arr.append(images.text)
        # Выбираем тему картин
        images_click = driver.find_element(By.XPATH,
                                           "//*[@class ='PopularRequestList']/div[" + str(random.randint(1, 4)) + "]")
        images_click.click()

        # Выбираем картинку
        driver.implicitly_wait(20)
        elem = driver.find_element(By.XPATH,
                                   "//*[@class = 'serp-list serp-list_type_search serp-list_unique_yes serp-list_rum_yes serp-list_justifier_yes serp-controller__list counter__reqid clearfix i-bem serp-list_js_inited']/div[" + str(
                                       random.randint(1, 50)) + "]")
        elem.click()

        # Получаем ссылку на изображение
        open = driver.find_element(By.XPATH,
                                   "//*[@class = 'MMButton MMButton_type_link MMViewerButtons-OpenImage MMViewerButtons-OpenImage_isOtherSizesEnabled MMViewerButtons-OpenImage_theme_primary']")
        link = open.get_attribute('href')
        print(link)

        # Скачиваем изображение
        urllib.request.urlretrieve(link, "C://Users//Виталий//Desktop//Autotest//python.png")
        # Ждем 20 сек
        time.sleep(20)
        # Закрываем браузер
        self.driver.quit()

    def test_wether(self):
        # Подключаем веб браузер
        s = Service('C:/Users/Виталий/Desktop/Autotest/chromedriver/chromedriver.exe')
        self.driver = webdriver.Chrome(service=s)
        driver = self.driver
        # Открываем Яндекс
        driver.get("https://yandex.ru/")
        # Открываем окно на весь экран
        driver.maximize_window()
        # Проверка
        assert "Яндекс" in driver.title
        assert "No results found." not in driver.page_source
        # Находим Поисковую строку
        elem = driver.find_element(By.ID, "text")
        # Вводим слово в поисковую строку
        elem.send_keys("Погода")
        # Нажимаем Enter
        elem.send_keys(Keys.ENTER)
        # Находим элементы с погоддой
        weather = driver.find_element(By.XPATH, "//*[@id='search-result']/li[1]/div/div[2]/div/div/div[1]")
        condition_web = driver.find_element(By.XPATH, "//*[@id='search-result']/li[1]/div/div[2]/div/div/div[2]")
        # Находим элемент с отображением скрости ветра
        flesh_web = driver.find_element(By.XPATH, "//*[@id='search-result']/li[1]/div/div[2]/div/div/div[2]/div/div[1]/div[1]")
        # Обрезаем его,до первого символа
        flesh =flesh_web.text[0]
        # Обрезаем состояния погода до скорости ветра
        condition = condition_web.text.partition(flesh)[0]
        # Создаем элемент сегоднешняя дата
        dt_now = datetime.date.today()
        # Открываем файл
        f = open("C://Users//Виталий//Desktop//Autotest//weather.txt" , "w")
        # Запись погода в файл
        print("\n")
        f.write( 'Погода сейчаc: ' + weather.text + ' ' + condition.rstrip() + "\n")
        # Вывод погоды в  консоль
        print('Погода сейчаc:', weather.text, condition.rstrip())
        # Создаем переменную для увеличение даты погоды
        day_count = 0
        # Цикл для извлечение погоды на 6 дней
        for i in range (1,7):
            # Дата на следующего дня
            tomorrow = dt_now + datetime.timedelta(days=day_count)
            # Температура на день
            day = driver.find_element(By.XPATH, "//*[@id='search-result']/li[1]/div/div[3]/div/div[" + str(i) + "]/div[2]")
            # Температура на ночь
            niht = driver.find_element(By.XPATH, "//*[@id='search-result']/li[1]/div/div[3]/div/div[" + str(i) + "]/div[4]")
            # Запись температуры в файл
            f.write(str(tomorrow) + ' день:' + day.text + ' ночь:' + niht.text+"\n")
            # Вывод температуры в консоль
            print(tomorrow, 'день:', day.text, 'ночь:', niht.text)
            # Увеличение переменной, следующий день
            day_count += 1
        # Закрываем файл
        f.close()
        # Делаем и сохраняем скрин с погодой
        driver.save_screenshot("C://Users//Виталий//Desktop//Autotest//weather.png")
        # Ожидание 5 сек.
        time.sleep(5)
        # Закрываем браузер
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)