from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from minutos import colors_bets
import datetime
import time
import pyodbc


server = 'DESKTOP-JJO8LEQ;'
database = 'scrapper_blaze;'


def sqlconnect():
    try:
        return pyodbc.connect('DRIVER={SQL Server};'
                              'SERVER='+server+';'
                              'DATABASE='+database+';'
                              'Trusted_Connection=yes')
    except:
        print ("Conexão falhou. Reveja os parametros passados.")


def insert(color, number, time):
    mydb = sqlconnect()
    query = mydb.cursor()
    query.execute("SELECT id FROM rolldice_tbo WHERE number = %s AND datetime = '%s'" % (number, str(time)))
    result = query.fetchone()
    print(result)

    if result == None:
        sql = "INSERT INTO rolldice_tbo (color,number,datetime) VALUES (?, ?, ?)"
        val = (color, number, str(time))
        query.execute(sql, val)
        mydb.commit()

    elif result == None:
        sql = "INSERT INTO rolldice_tbo (color,number,datetime) VALUES (?, ?, ?)"
        val = (color, number, str(time))
        query.execute(sql, val)
        mydb.commit()



browser = Firefox(executable_path=r"C:\selenium\geckodriver.exe")
browser.get("https://blaze.com/pt/games/double")
first = True


time.sleep(3)
while True:
    roulette_timer = (By.CSS_SELECTOR, "#roulette-timer")
    roulette = browser.find_element(*roulette_timer).get_attribute('innerHTML')
    qtd = len(roulette.split('"time-left">Blaze Girou <b>'))

    if qtd == 2:
        time.sleep(3)
        colors_bets()
        if first:
            time.sleep(2)
            locator = (By.CSS_SELECTOR, ".roulette-previous")
            numbers = (browser.find_element(*locator).get_attribute('innerHTML'))
            now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

            numbers = numbers.split('class="roulette-tile"><div class="sm-box ')
            num = numbers[1]
            color = (num.split('">'))[0]
            if color == "white":
                number = 0
            else:
                number = (num.split('class="number">'))
                number = number[1].split("</div>")
                number = number[0]
                print(color, number, now)
            first = False
    else:
        first = True
