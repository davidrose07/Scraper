import sqlite3
import pandas as pd  #pandas are for making dataframes
from selenium import webdriver
from tkinter import *
from selenium.common.exceptions import NoSuchElementException #for exception handling
from selenium.webdriver.common.by import By
from os import mkdir

class Scrape():
    FILENAME = '/price.db'    
    def find_items(search_field,num):      
        # Setup the selenium driver
        driver = webdriver.Chrome("./chromedriver.exe")
        driver.get("https://www.amazon.com/")
        
        #searching on search page by using selenium
        search = driver.find_element(By.ID,"twotabsearchtextbox")
        search.send_keys(search_field)
        search_btn = driver.find_element(By.ID,"nav-search-submit-button")
        search_btn.click()
    
        # Go to each page to extract the above information
        url = []
        for i in driver.find_elements(By.XPATH,"//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']"):    
            url.append(i.get_attribute("href"))
            
        #declaring variables for dataframe and loop
        brand_name = []
        product_name = []
        rating_total = []
        price = []
        num=int(num)
        urls = url[:num]
        x=0
        
        #iterating through the urls in the range selected
        for i in urls:
            if x == num:
                break
            else:
                # Search each element in each url
                driver.get(i) 
                try:
                    #brand = driver.find_element(By.XPATH,"//td[@class='a-span9']/span")
                    brand = driver.find_element(By.ID, 'bylineInfo')
                    brand_name.append(brand.text)
                except NoSuchElementException as exc:
                    print(exc)
                    brand_name.append('-')         
                try:
                    product =  driver.find_element(By.ID,"productTitle")
                    product_name.append(product.text)
                except NoSuchElementException as exc:
                    print(exc)
                    product_name.append('-')   
                try:
                    rate = driver.find_element(By.ID,"acrCustomerReviewText")
                    rating_total.append(rate.text)
                except NoSuchElementException as exc:
                    print(exc)
                    rating_total.append('-')
                try:
                    total_price = driver.find_element(By.CLASS_NAME,"a-price-whole")
                    price.append(total_price.text)
                except NoSuchElementException as exc:
                    print(exc)
                    price.append('-') 
                finally:
                    x+=1      
            
        # making a dataframe
        product_page = pd.DataFrame({})
        product_page['Brand']= brand_name
        product_page['Name_of_the_product']= product_name
        product_page['number_of_ratings']= rating_total
        product_page['price_of_the_item']= price
        product_page['url_of_the_page']= urls
        driver.close()
        
        # Creating the database if not already created
        try:
            con = sqlite3.connect(Scrape.FILENAME)
        except sqlite3.OperationalError:
            mkdir('C:\\Users\\david\\Desktop\\Web Scraping\\amazon-scraper')
        finally:
            con = sqlite3.connect(Scrape.FILENAME)
        
        # Creating tables if not already created and replacing data using pandas dataframe
        cursor=con.cursor()    
        cursor.execute('CREATE TABLE IF NOT EXISTS products (Brand,Name_of_the_product, number_of_ratings, price_of_the_item,url_of_the_page)')
        product_page.to_sql('products',con, index=False, if_exists="replace")
        con.commit()
        con.close()
        
    def filter(mystring):
        # Filters data from database only displaying results
        db=Scrape.FILENAME
        con=sqlite3.connect(db)
        cursor=con.cursor()
        cursor.execute("SELECT * FROM products WHERE Brand LIKE '%" + mystring + "%' OR Name_of_the_product LIKE '%" + mystring + "%' OR number_of_ratings LIKE '%" + mystring + "%'  OR price_of_the_item LIKE '%" + mystring + "%'  OR url_of_the_page LIKE '%" + mystring + "%'")
        rows=cursor.fetchall()
        return rows
          
    def display():
        # Database query to retrieve all information
        db=Scrape.FILENAME
        con=sqlite3.connect(db)
        cursor=con.cursor()    
        cursor.execute('select * from products' )
        rows=cursor.fetchall()
        return rows
    
