from bs4 import BeautifulSoup
import requests
from rich import print



def mytek_get_products(url):
    content = requests.Session().get(url.format("1"))
    soup = BeautifulSoup(content.text, "lxml")
    try:
        num_pages = int(soup.find("div", class_ = "toolbar toolbar-products").find("div", class_ ="pages").ul.find_all("li")[-2].text.split(" ")[1])
    except:
        num_pages = 1
        
    data = {}
    for i in range(1,num_pages+1):
        content = requests.Session().get(url.format(str(i)))
        soup = BeautifulSoup(content.text, "lxml")
        articles = soup.find("ol", class_ = "products list items product-items").findAll("li")
        for article in articles:
            try:
                promo = article.find("div", class_ = "testLp4x prdtBILCta").find("span", class_="special-price")
                disp = article.find("div", class_ = "testLp4x prdtBILCta").find("div", class_ = "card-body").span.text.strip()
            except:
                promo = "Null"
                disp = "Epuisé"
                
            if str(promo).strip() != "None" and str(disp) != "Epuisé":
                prod_url = article.find("div", class_="prdtBILDetails").a["href"]
                img = article.find("div", class_="prdtBILImg").img["src"]
                title = article.find("div",class_="prdtBILDetails").a.text.strip()
                desc = article.find("div",class_="prdtBILDetails").find("div",class_="product description product-item-description").p.text.strip()
                ref = article.find("div",class_="prdtBILDetails").find("div",class_="skuDesktop").text.strip()[1:-1]
                after_discount = article.find("div",class_="testLp4x prdtBILCta").find("span",class_="special-price").find("span",class_="price").text.strip()
                before_discount = article.find("div",class_="testLp4x prdtBILCta").find("span",class_="old-price").find("span",class_="price").text.strip()
                discount_amount = article.find("div",class_="testLp4x prdtBILCta").find("span",class_="discount-price").text.strip()
                
                data[ref] = {
                    "ref": ref,
                    "url": prod_url,
                    "img": img,
                    "title": title,
                    "description": desc,
                    "after_discount": after_discount,
                    "before_discount": before_discount,
                    "discount_amount": discount_amount,
                    "supplier": "Mytek"
                }

                
    return data

    
    
        
    
    


#print(mytek_get_products("https://www.mytek.tn/informatique/ordinateurs-portables.html?p={}"))
#print(mytek_get_products("https://www.mytek.tn/informatique/ordinateur-de-bureau/pc-de-bureau.html?p={}"))
#print(mytek_get_products("https://www.mytek.tn/informatique/ordinateur-de-bureau/ecran.html?p={}"))
#print(mytek_get_products("https://www.mytek.tn/informatique/peripheriques-accessoires.html?p={}"))
#print(mytek_get_products("https://www.mytek.tn/telephonie-tunisie/smartphone-mobile-tunisie.html?p={}"))
#print(mytek_get_products("https://www.mytek.tn/gaming/console-de-jeux.html?p={}"))
#print(mytek_get_products("https://www.mytek.tn/informatique/composants-informatique.html?p={}"))
