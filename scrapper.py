import os
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logger

def scrape(searchString, log_writer, file_object):
    #log_writer = logger.App_Logger()
    #file = searchString
    #file_object = open("logs/xyz.txt", 'a+')

    flipkart_url = "https://www.flipkart.com/search?q=" + searchString
    log_writer.log(file_object, 'received flipkart link')
    uClient = uReq(flipkart_url)
    flipkartPage = uClient.read()
    uClient.close()
    flipkart_html = bs(flipkartPage, "html.parser")
    log_writer.log(file_object, 'Parsed html')
    bigboxes = flipkart_html.findAll("div", {"class": "bhgxx2 col-12-12"})
    del bigboxes[0:3]
    box = bigboxes[0]
    productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
    log_writer.log(file_object, 'Received product link')
    prodRes = requests.get(productLink)
    prodRes.encoding = 'utf-8'
    prod_html = bs(prodRes.text, "html.parser")
    log_writer.log(file_object, 'parsed product html')
    commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})
    reviews = []
    log_writer.log(file_object, 'Start of getting tag details')
    for commentbox in commentboxes:
        try:
            # name.encode(encoding='utf-8')
            name = commentbox.div.div.find_all('p', {'class': '_3LYOAd _3sxSiS'})[0].text
        except:
            name = 'No Name'

        try:
            # rating.encode(encoding='utf-8')
            rating = commentbox.div.div.div.div.text
        except:
            rating = 'No Rating'

        try:
            # commentHead.encode(encoding='utf-8')
            commentHead = commentbox.div.div.div.p.text
        except:
            commentHead = 'No Comment Heading'

        try:
            comtag = commentbox.div.div.find_all('div', {'class': ''})
            # custComment.encode(encoding='utf-8')
            custComment = comtag[0].div.text
        except Exception as e:
            log_writer.log(file_object, "Exception occurred: {}".format(e))

        mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                  "Comment": custComment}
        reviews.append(mydict)

        print('FROM SCRAPE')
        print(type(reviews))
        print(reviews)
    log_writer.log(file_object, 'End of getting tag details')
    log_writer.log(file_object, 'returning reviews')
    return reviews














