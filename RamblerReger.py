import time
import ctypes
import os
from settings import domaincount, imap_activate, captcha_service
import random
from colorama import init
from colorama import Fore, Style
from selenium import webdriver
from multiprocessing import Process
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from passlib import pwd
domains = ['@autorambler.ru', '@myrambler.ru', '@rambler.ru', '@rambler.ua', '@ro.ru']
init()
another = True


def start(): #запуск chromedriver
    global driver, wait
    driver_path = r'.\chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument('--disable-logging')
    if captcha_service == 2:
        chrome_options.add_extension(r".\api.crx")
    elif captcha_service == 1: # пока только 1 сервис
        pass
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)
    rega()


def rega():
    global mail, secret, password, domain_text
    if domaincount == 6:
        domain_text = domains[random.randint(0, 4)]
    else:
        domain_text = domains[domaincount - 1]
    mail = pwd.genword(length=32)
    password = pwd.genword(length=random.randint(16, 32))
    secret = pwd.genword(length=8)
    wait.until(EC.number_of_windows_to_be(2))
    windows = driver.window_handles
    for window in windows:
        driver.switch_to.window(window)
        if driver.current_url == 'chrome-extension://ifibfemgeogfhoebkmokieepdoobkbpo/options/options.html':
            driver.switch_to.window(window)
            time.sleep(0.5)
            driver.close()
            break
    windows = driver.window_handles
    driver.switch_to.window(windows[0])
    driver.get('https://id.rambler.ru/login-20/mail-registration')
    time.sleep(1)
    driver.minimize_window()
    try:
        WebDriverWait(driver, 5).until(presence_of_element_located((By.XPATH, '//*[@data-cerber-id="registration_form::mail::step_1::verification_type::question"]'))).click()
    except (NoSuchElementException, TimeoutException):
        pass
    while True:
        try:
            wait.until(presence_of_element_located((By.CSS_SELECTOR, '[data-state="solving"]')))
        except (NoSuchElementException, TimeoutException):
            driver.refresh()
            driver.set_window_size(800, 600)
            time.sleep(1)
            driver.minimize_window()
        else:
            break
    wait.until(presence_of_element_located((By.XPATH, '//*[@autocomplete="username"]')))
    if domaincount != 3:
        driver.find_element(By.XPATH, '//*[@class="rui-Tooltip-anchor"]').click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, f'.rui-Menu-content > :nth-child({domaincount})').click()
        time.sleep(3)
    driver.find_element(By.XPATH, '//*[@theme="[object Object]"][4]').click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, f'.rui-Menu-content > :nth-child(1)').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@data-cerber-id="registration_form::mail::step_1::mailbox_name"]').send_keys(mail + Keys.TAB + Keys.TAB + password + Keys.TAB + password)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@data-cerber-id="registration_form::mail::step_1::answer"]').send_keys(secret)
    butttton_complete = WebDriverWait(driver, 75).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-cerber-id="login_form::main::login_button"]')))
    butttton_complete.click()
    secret = f':{secret}'
    wait.until(presence_of_element_located((By.XPATH, '//*[@data-cerber-id="registration_form::step_2::add_later"]'))).click()
    time.sleep(0.5)
    if imap_activate:
        driver.set_page_load_timeout(5)
        try:
            driver.get('https://mail.rambler.ru/settings/mailapps/change')
        except TimeoutException:
            pass
        driver.set_window_size(800, 600)
        time.sleep(1)
        driver.minimize_window()
        while True:
            try:
                WebDriverWait(driver, 3).until(presence_of_element_located((By.CSS_SELECTOR, '[data-state="solving"]')))
            except (NoSuchElementException, TimeoutException):
                try:
                    driver.get('https://mail.rambler.ru/settings/mailapps/change')
                except TimeoutException:
                    pass
            else:
                break
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.MailAppsChange-submitWrapper-JZ > button'))).click()
        time.sleep(0.5)
    driver.quit()
    zapis()


def zapis():
    if another:
        with open('result.txt', 'a', encoding='utf-8') as file:
            file.write(f'{mail}{domain_text}:{password}{secret}\n')
        print(Style.RESET_ALL + Fore.BLUE + f'{mail}{domain_text}:{password}{secret}' + Style.RESET_ALL + Fore.BLUE)
    else:
        return f'{mail}{domain_text}:{password}'


def another_service():#если нужно создать 1 почту для другой программы и не записывать в result.txt
    global another
    another = False
    return start()


if __name__ == '__main__':
    text = (Fore.GREEN + '''
    ██████╗░░█████╗░███╗░░░███╗██████╗░██╗░░░░░███████╗██████╗░
    ██╔══██╗██╔══██╗████╗░████║██╔══██╗██║░░░░░██╔════╝██╔══██╗
    ██████╔╝███████║██╔████╔██║██████╦╝██║░░░░░█████╗░░██████╔╝
    ██╔══██╗██╔══██║██║╚██╔╝██║██╔══██╗██║░░░░░██╔══╝░░██╔══██╗
    ██║░░██║██║░░██║██║░╚═╝░██║██████╦╝███████╗███████╗██║░░██║
    ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═════╝░╚══════╝╚══════╝╚═╝░░╚═╝

        ██████╗░███████╗░██████╗░███████╗██████╗░
        ██╔══██╗██╔════╝██╔════╝░██╔════╝██╔══██╗
        ██████╔╝█████╗░░██║░░██╗░█████╗░░██████╔╝
        ██╔══██╗██╔══╝░░██║░░╚██╗██╔══╝░░██╔══██╗
        ██║░░██║███████╗╚██████╔╝███████╗██║░░██║
        ╚═╝░░╚═╝╚══════╝░╚═════╝░╚══════╝╚═╝░░╚═╝
        '''
            + "by GosMachine" + Style.RESET_ALL)
    print(text)
    threading = int(input(Style.RESET_ALL + Fore.BLUE + 'Threading: ' + Style.BRIGHT))
    count = int(input(Style.RESET_ALL + Fore.BLUE + 'Count: ' + Style.BRIGHT))
    counter = 0
    processes = []
    while counter < count:
        for _ in range(threading):
            try:
                p = Process(target=start)
                p.start()
                processes.append(p)
                time.sleep(2)
            except TimeoutException as e:
                print('Ошибка')
        counter += threading
        for p in processes:
            p.join()
