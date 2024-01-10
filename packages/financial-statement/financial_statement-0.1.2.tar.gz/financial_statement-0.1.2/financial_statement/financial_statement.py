#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 18:39:22 2023

@author: wenkangng
"""

import requests
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def income_statement(ticket,year):
    url =   f"https://discountingcashflows.com/company/{ticket}/income-statement/"
    header = {
          "User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"}
    response = requests.get(url,headers= header)
    soup = BeautifulSoup(response.text, "html.parser")
    
    all_tag = soup.find_all('span', {'class': 'row-description-text'})
    all_time = soup.find_all('span', {'class': 'text-nowrap'}) # year
    all_value = soup.find_all('td')
    
    error_ticket = soup.find('div',{'class':'error mx-auto'})
    if error_ticket == None:
     pass
    else:
       raise ValueError("Ticket code has not found in dataset")
    
    title = ["Report Filling"]
    years = []
    output = []
    value_1 = []
    
    for time in all_time:
      years.append(time.text)
    
    for tag in all_tag:
      text = tag.text if tag else 'Not found'
      title.append(text)
    
    
    all_value = soup.find_all('td')
    
    start = 3
    end = 3+len(years)
    increase = len(years)+2
    
    
    for i in range(0, len(title),1):
      for value in all_value[start+i*increase:end+i*increase]:  # append calue in container
        text = value.text.replace(",","")
        output.append(text)
        #print(text)
    
    
    
    def find_year_index(year):
      if year in years:
        i = years.index(year)
        return i
      else:
        raise ValueError("Year not found in dataset")
    i = find_year_index(year)
    
    for n in range(i,len(output),len(years)):
      if n >i:
        data = output[n]
        value_1.append(float(data))
      else: 
        data = output[n]
        value_1.append(data)
      #print(data)
    
    title = title
    
    data = {year:value_1}
    result = pd.Series(value_1, index = title)
    
    return result




def balance_sheet(ticket,year):
    url =   f"https://discountingcashflows.com/company/{ticket}/balance-sheet-statement/"
    header = {
        "User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"}
    response = requests.get(url,headers= header)
    soup = BeautifulSoup(response.text, "html.parser")
    
    all_tag = soup.find_all('span', {'class': 'row-description-text'})
    all_value = soup.find_all('td')
    all_time = soup.find_all('th', {'class': "py-0 px-3 text-center"}) # YEAR
    
    error_ticket = soup.find('div',{'class':'error mx-auto'})
    if error_ticket == None:
      pass
    else:
        raise ValueError("Ticket code has not found in dataset")
    
    title = ["Report Filling"]
    years = []
    output = []
    value_1 = []
    
    for time in all_time:
      years.append(time.text[:4])
    
    for tag in all_tag:
      text = tag.text if tag else 'Not found'
      title.append(text)
    
    
    all_value = soup.find_all('td')
    start = 2
    end = 2+len(years)
    increase = len(years)+1
    
    
    for i in range(0, len(title),1):
      for value in all_value[start+i*increase:end+i*increase]:  # append calue in container
        text = value.text.replace(",","")
        output.append(text)
    
    
    def find_year_index(year):
      if year in years:
        i = years.index(year)
        return i
      else:
        raise ValueError("Year not found in dataset")
    i = find_year_index(year)
    
    for n in range(i,len(output),len(years)):
      if n >i:
        data = output[n]
        value_1.append(float(data))
      else: 
        data = output[n]
        value_1.append(data)
    
    title = title
    
    data = {year:value_1}
    result = pd.Series(value_1, index = title)
    
    
    def error_scraping(output, years, title):
      assert len(output) == len(years) == len(title), "The loop function to arrange value has an error."
    
    return result

def cash_flow_statement(ticket,year):
    url =   f"https://discountingcashflows.com/company/{ticket}/cash-flow-statement/"
    header = {
        "User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"}
    response = requests.get(url,headers= header)
    soup = BeautifulSoup(response.text, "html.parser")
    all_tag = soup.find_all('span', {'class': 'row-description-text'})
    all_value = soup.find_all('td')
    all_time = soup.find_all('th', {'class': "py-0 px-3 text-center"}) # YEAR
    error_ticket = soup.find('div',{'class':'error mx-auto'}) # error from ticket
    
    if error_ticket == None:
      pass
    else:
        raise ValueError("Ticket code has not found in dataset")
    
    
    title = ["Report filling"]
    years = []
    output = []
    value_1 = []
    
    for time in all_time[1:]:
      years.append(time.text[:4])
    
    for tag in all_tag:
      text = tag.text if tag else 'Not found'
      title.append(text)
    
    
    
    all_value = soup.find_all('td')
    start = 3
    end = 3+len(years)
    increase = len(years)
    
    
    for i in range(0, len(title),1):
      for value in all_value[start+i*increase+2*i:end+i*increase+2*i]:  # append calue in container
        text = value.text.replace(",","")
        output.append(text)
    
    def find_year_index(year):
      if year in years:
        i = years.index(year)
        return i
      else:
        raise ValueError("Year not found in dataset")
    
    i = find_year_index(year)
    
    for n in range(i,len(output),len(years)):
      if n >i:
        data = output[n]
        value_1.append(float(data))
      else: 
        data = output[n]
        value_1.append(data)
      #print(data)
    
    title = title
    data = {year:value_1}
    
    def error_scraping(output, years, title):
      assert len(output) == len(years) == len(title), "The loop function to arrange value has an error."
    
    #
    result = pd.Series(value_1, index = title)
    
    return result




def get_dividend(ticket,YTM=False):

  url = f"https://discountingcashflows.com/company/{ticket}/dividends/"
  header = {
      "User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"}
  response = requests.get(url,headers= header)
  soup = BeautifulSoup(response.text, "html.parser")
  
  if YTM == True :
    all_year = soup.find_all('th',{'class':"px-3 text-center text-uppercase"})
    years = []
    ytm_dividend = []
    for year in all_year:
      years.append(year.text.replace('\n',''))

    clean_year = [item.strip() for item in years]

    for i in range(0,len(years),1):
      all_annual_dividend = soup.find('td',{'id':f'dividend-cell-{i}'})
      ytm_dividend.append(float(all_annual_dividend.text))

    return pd.Series(ytm_dividend,index = clean_year)

  all_year = soup.find_all('th',{'class':"px-3 text-center text-uppercase"})
  all_date = soup.find_all('td',{'class':'text-center'})

  not_dividend = soup.find("p",{"class":"text-dark text-center"})


  error_ticket = soup.find('div',{'class':'error mx-auto'}) # error from ticket

  if error_ticket == None:
    pass
  else:
      raise ValueError("Ticket code has not found in dataset")

  if not_dividend == None:
    # get Ex -dividend date
    date_dividend = []
    for date in all_date[6:]:
      date = date.string
      date_dividend.append(date.string)
    date_ex_dividend=[]
    for i in range(0,len(date_dividend),4):
      date_ex_dividend.append(date_dividend[i])

    # dividend
    date_dividend = []
    dividend = []
    for i in range(0,len(date_ex_dividend),1):
      value = soup.find('td', {'id': f'reported-dividend-{i}'})
      date_dividend.append( value['date'])
      dividend.append(float(value.text))

    return pd.Series(dividend,index = date_dividend)

  else:
      print("Company does not pay dividends")




def shareholder(ticket,url):
    
  def url(ticket):
    url = f"https://finance.yahoo.com/quote/{ticket}/holders?p={ticket}"
    return url

  header = {
    "User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"}
  response = requests.get(url,headers= header)
  soup = BeautifulSoup(response.text, "html.parser")
  share = soup.find_all("td", attrs={"class": "Ta(end) Pstart(10px)"})
  all_holder = soup.find_all("td", attrs={"class":"Ta(start) Pend(10px)"})
  date = soup.find_all("span", attrs={"class":"Ta(end) Pstart(10px)"})
  name = []
  shares = []
  date = []
  percent =[]

  # shares
  for i,element in zip(range(0,len(share),4),all_holder):
    name.append(element.text)
    shares.append(int(share[i].text.replace(",","")))
    date_object = datetime.strptime(share[i+1].text, '%b %d, %Y')
    date.append(date_object)
    percent.append(round(float(share[i+2].text.replace("%",""))/100,5))


  data = {
  "Shares":shares,
  "Percentage":percent,
  "Date Reported": date
}
     

  df = pd.DataFrame(data, index = name)

  return df

def shareholder(ticket):
    
  url = f"https://finance.yahoo.com/quote/{ticket}/holders?p={ticket}"

  header = {
    "User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"}
  response = requests.get(url,headers= header)
  soup = BeautifulSoup(response.text, "html.parser")
  share = soup.find_all("td", attrs={"class": "Ta(end) Pstart(10px)"})
  all_holder = soup.find_all("td", attrs={"class":"Ta(start) Pend(10px)"})
  date = soup.find_all("span", attrs={"class":"Ta(end) Pstart(10px)"})
  name = []
  shares = []
  date = []
  percent =[]

  # shares
  for i,element in zip(range(0,len(share),4),all_holder):
    name.append(element.text)
    shares.append(int(share[i].text.replace(",","")))
    date_object = datetime.strptime(share[i+1].text, '%b %d, %Y')
    date.append(date_object)
    percent.append(round(float(share[i+2].text.replace("%",""))/100,5))


  data = {
  "Shares":shares,
  "Percentage":percent,
  "Date Reported": date
}
     

  df = pd.DataFrame(data, index = name)

  return df

def current_price(ticket):
    url = f"https://finance.yahoo.com/quote/{ticket}/holders?p={ticket}"

    header = {
          "User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"}
    response = requests.get(url,headers= header)
    soup = BeautifulSoup(response.text, "html.parser")
    current_price = soup.find('fin-streamer',{'class':"Fw(b) Fz(36px) Mb(-4px) D(ib)"})
    current_price = ((float(current_price["value"])))
    return current_price
