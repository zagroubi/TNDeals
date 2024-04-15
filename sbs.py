from bs4 import BeautifulSoup
import requests
from rich import print
import hashlib
import re


def md5_hash(string):
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    return md5_hash.hexdigest()



def sbs_get_products(url):
    content = requests.Session().get(url.format("1"))
    soup = BeautifulSoup(content.text, "lxml")
    try:
        num_pages = int(soup.find("nav", class_ = "pagination").ul.find_all("li")[-2].text.strip())
    except:
        num_pages = 1

    data = {}
    
    for i in range(1,num_pages+1):
        content = requests.Session().get(url.format(str(i)))
        soup = BeautifulSoup(content.text, "lxml")
        articles = soup.find("div", id = "js-product-list").find_all("article")
        for article in articles:
            promo = article.find("div", class_ = "product-price-and-shipping").find("span", class_ = "regular-price")
            if str(promo).strip() != "None":
                prod_url = article.find("div", class_="product_desc").h3.a["href"]
                img = article.find("div", class_="img_block").img["src"]
                title = article.find("div", class_="product_desc").h3.a.text.strip()

                desc = article.find("div", class_ = "product_desc").find("div", itemprop = "description")
                if (desc.find("img")):
                    images = desc.find_all('img')
                    for img_tag in images:
                        img_tag.replace_with("<br>")

                    desc = desc.text[4:]
                elif (desc.find("li")):
                    list_items = desc.find_all('li')
                    for li in list_items:
                        span_tag = soup.new_tag("span")
                        span_tag.string = ", "
                        li.insert_after(span_tag)
                    desc = desc.text[:-1]
                else:
                    desc = desc.text

                ref = md5_hash(title)
                after_discount = article.find("div", class_ = "product-price-and-shipping").find("span", class_ = "price price-sale").text
                before_discount = article.find("div", class_ = "product-price-and-shipping").find("span", class_="regular-price").text
                discount_amount = article.find("span", class_ = "discount-amount discount-product").text

                data[ref] = {
                    "ref": ref,
                    "url": prod_url,
                    "img": img,
                    "title": title,
                    "description": desc,
                    "after_discount": after_discount,
                    "before_discount": before_discount,
                    "discount_amount": discount_amount,
                    "supplier": "SBS Informatique"
                }

    return data
        


#print(sbs_get_products("https://www.sbsinformatique.com/pc-portables-tunisie?page={}"))
#print(sbs_get_products("https://www.sbsinformatique.com/pc-gamer-tunisie?page={}"))
#print(sbs_get_products("https://www.sbsinformatique.com/moniteurs-tunisie?page={}"))
#print(sbs_get_products("https://www.sbsinformatique.com/accessoires-gaming-tunisie?page={}"))
#print(sbs_get_products("https://www.sbsinformatique.com/smartphone-tunisie?page={}"))
#print(sbs_get_products("https://www.sbsinformatique.com/composants-tunisie?page={}"))
