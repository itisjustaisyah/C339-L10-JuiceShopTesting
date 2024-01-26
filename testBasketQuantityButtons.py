import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.alert import Alert
from time import *

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 3)


def getSite(url):
    driver.get(url)


def login():
    driver.find_element(By.XPATH,
                        "/html/body/div[3]/div[2]/div/mat-dialog-container/app-welcome-banner/div/div[2]/button[2]").click()
    driver.implicitly_wait(2)
    driver.find_element(By.ID, "navbarAccount").click()

    wait.until(expected_conditions.element_to_be_clickable((By.ID, "navbarLoginButton")))
    driver.find_element(By.ID, "navbarLoginButton").click()

    wait.until(expected_conditions.element_to_be_clickable((By.ID, "email")))
    driver.find_element(By.ID, "email").send_keys("schlorple@gmail.com")
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.ID, "loginButton").click()


@pytest.fixture()
def setup_getSite():
    print("setup")
    siteUrl = "http://localhost:3000/"
    getSite(siteUrl)
    try:
        driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container/app-welcome-banner/div/div[2]/button[2]")
    except:
        print("already logged in")
    else:
        login()
    finally:
        goToBasket()
        deleteFirst()
        deleteFirst()
    getSite(siteUrl)
    sleep(1)
    yield siteUrl
    print("teardown")


def goToBasket():
    driver.find_element(By.XPATH,
                        "/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-navbar/mat-toolbar/mat-toolbar-row/button[4]").click()


def getTotalPrice():
    totalPrice = driver.find_element(By.ID, "price").text
    totalPrice = totalPrice.replace('Total Price: ', '')
    totalPrice = totalPrice.replace('¤', '')
    return float(totalPrice)


def getAJQuantity():
    return int(driver.find_elements(By.CSS_SELECTOR,
                                    "mat-cell:nth-child(3) > span:nth-child(2)")[0].text)


def getAPQuantity():
    return int(driver.find_elements(By.CSS_SELECTOR,
                                    "mat-cell:nth-child(3) > span:nth-child(2)")[1].text)


def getAJPrice():
    return float(driver.find_elements(By.CSS_SELECTOR,
                                      "mat-cell:nth-child(4)")[0].text.replace('¤', ''))


def getAPPrice():
    return float(driver.find_elements(By.CSS_SELECTOR,
                                      "mat-cell:nth-child(4)")[1].text.replace('¤', ''))


def addAJ():
    wait.until(expected_conditions.element_to_be_clickable((By.XPATH,
                                                            "/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-search-result/div/div/div[2]/mat-grid-list/div/mat-grid-tile[1]/div/mat-card/div[2]/button")))
    driver.find_element(By.XPATH,
                        "/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-search-result/div/div/div[2]/mat-grid-list/div/mat-grid-tile[1]/div/mat-card/div[2]/button").click()


def addAP():
    wait.until(expected_conditions.element_to_be_clickable((By.XPATH,
                                                            "/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-search-result/div/div/div[2]/mat-grid-list/div/mat-grid-tile[2]/div/mat-card/div[2]/button")))
    driver.find_element(By.XPATH,
                        "/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-search-result/div/div/div[2]/mat-grid-list/div/mat-grid-tile[2]/div/mat-card/div[2]/button").click()


def deleteFirst():
    try:
        wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,
                                                                "mat-cell:nth-child(5) > button:nth-child(1)")))
    except:
        print("no items in basket")
    else:
        driver.find_element(By.CSS_SELECTOR,
                        "mat-cell:nth-child(5) > button:nth-child(1)").click()


def test_Basket_PlusButton_Happy(setup_getSite):
    addAJ()
    addAP()
    goToBasket()

    assert getAPQuantity() == 1
    assert getAJQuantity() == 1
    assert getTotalPrice() == (getAJQuantity() * getAJPrice() + getAPQuantity() * getAPPrice())

    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,
                                                            "button.mat-focus-indicator:nth-child(3)")))
    driver.find_element(By.CSS_SELECTOR,
                        "button.mat-focus-indicator:nth-child(3)").click()
    sleep(3)

    print(getTotalPrice())

    assert getAJQuantity() == 2
    assert getAPQuantity() == 1
    assert getTotalPrice() == (getAJQuantity() * getAJPrice() + getAPQuantity() * getAPPrice())

    deleteFirst()
    deleteFirst()


def test_Basket_PlusButton_Sad(setup_getSite):
    addAJ()
    addAJ()
    addAJ()
    addAJ()
    addAJ()
    addAJ()


    goToBasket()

    assert getAJQuantity() == 5
    assert getTotalPrice() == (5 * getAJPrice())

    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,
                                                            "button.mat-focus-indicator:nth-child(3)")))
    driver.find_element(By.CSS_SELECTOR,
                        "button.mat-focus-indicator:nth-child(3)").click()
    sleep(3)

    print(getTotalPrice())

    assert getAJQuantity() == 5
    assert getTotalPrice() == (5 * 1.99)

    deleteFirst()


def test_Basket_MinusButton_Happy(setup_getSite):
    addAJ()
    addAJ()
    addAP()
    addAP()
    goToBasket()

    assert getAJQuantity() == 2
    assert getAPQuantity() == 2
    assert getTotalPrice() == (getAJQuantity() * getAJPrice() + getAPQuantity() * getAPPrice())

    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,
                                                            "button.ng-star-inserted:nth-child(1)")))
    driver.find_element(By.CSS_SELECTOR,
                        "button.ng-star-inserted:nth-child(1)").click()
    sleep(3)

    print(getTotalPrice())

    assert getAJQuantity() == 1
    assert getAPQuantity() == 2
    assert getTotalPrice() == (getAJQuantity() * getAJPrice() + getAPQuantity() * getAPPrice())

    deleteFirst()
    deleteFirst()


def test_Basket_MinusButton_Sad(setup_getSite):
    addAJ()

    goToBasket()

    assert getAJQuantity() == 1
    assert getTotalPrice() == (1 * getAJPrice())

    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,
                                                            "button.ng-star-inserted:nth-child(1)")))
    driver.find_element(By.CSS_SELECTOR,
                        "button.ng-star-inserted:nth-child(1)").click()
    sleep(3)

    print(getTotalPrice())
    assert getAJQuantity() == 1
    assert getTotalPrice() == (1 * 1.99)

    deleteFirst()

# Test Case: Plus button
# navigate to product Apple Juice (1.99)
# add to basket button
# navigate to product Apple Pomace (0.89)
# add to basket button
# go to basket
# check AJ quantity = 1 * 1.99
# check AP quantity = 1 * 0.89

#
# assert total price = 2.88
#
# Apple Juice + button
# check AJ quantity = 1 * 1.99
# check AP quantity = 2 * 0.89
# assert total price = 3.77

# Test Case: Minus button
# navigate to product Apple Juice (1.99)
# add to basket button X2
# navigate to product Apple Pomace (0.89)
# add to basket button X2
# go to basket
# check AJ quantity = 2 * 1.99
# check AP quantity = 2 * 0.89
#
# assert total price = 5.76
#
# Apple Juice - button
# check AJ quantity = 1 * 1.99
# check AP quantity = 2 * 0.89
# assert total price = 3.77
