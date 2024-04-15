from bs4 import BeautifulSoup
import requests
from rich import print



def tnet_get_products(url):
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
                card = article.find("div", class_="thumbnail-container text-xs-center")
                prod_url = card.find("h2", class_="h3 product-title").a["href"]
                img = card.find("img")["src"]
                title = card.find("h2", class_="h3 product-title").a.text.strip()
                desc = card.find("div", class_ = "listds").a.text.strip()
                ref = card.find("span", class_ = "product-reference").text[1:-1]
                after_discount = card.find("div", class_ = "product-price-and-shipping").find("span", class_="price").text
                before_discount = card.find("div", class_ = "product-price-and-shipping").find("span", class_="regular-price").text
                discount_amount = card.find("span", class_ = "discount-amount discount-product").text

                data[ref] = {
                    "ref": ref,
                    "url": prod_url,
                    "img": img,
                    "title": title,
                    "description": desc,
                    "after_discount": after_discount,
                    "before_discount": before_discount,
                    "discount_amount": discount_amount,
                    "supplier": "Tunisianet"
                }

    return data
        

#print(get_products("https://www.tunisianet.com.tn/681-pc-portable-gamer?page={}"))
#print(get_products("https://www.tunisianet.com.tn/682-pc-de-bureau-gamer?page={}"))
#print(get_products("https://www.tunisianet.com.tn/667-ecran-pc-tunisie?page={}"))
#print(get_products("https://www.tunisianet.com.tn/700-accessoires-et-peripheriques?page={}"))
#print(get_products("https://www.tunisianet.com.tn/596-smartphone-tunisie?page={}"))
#print(get_products("https://www.tunisianet.com.tn/466-console-de-jeux?page={}"))
#print(get_products("https://www.tunisianet.com.tn/406-composant-informatique?page={}"))