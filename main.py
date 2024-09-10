
# Categories: Laptops - Desktops - Monitors - Phones - Accessories 

from scrapers.tunisianet import tnet_get_products
from scrapers.sbs import sbs_get_products
from scrapers.mytek import mytek_get_products
import pymysql


# Main containers
laptops = {}
desktops = {}
monitors = {}
components = {}
phones = {} 
consoles = {}
accessories = {}

# Get data: Tunisianet
tnet_laptops = tnet_get_products("https://www.tunisianet.com.tn/681-pc-portable-gamer?page={}") 
tnet_desktops = tnet_get_products("https://www.tunisianet.com.tn/682-pc-de-bureau-gamer?page={}")
tnet_monitors = tnet_get_products("https://www.tunisianet.com.tn/667-ecran-pc-tunisie?page={}")
tnet_accessories = tnet_get_products("https://www.tunisianet.com.tn/700-accessoires-et-peripheriques?page={}")
tnet_phones = tnet_get_products("https://www.tunisianet.com.tn/596-smartphone-tunisie?page={}")
tnet_consoles = tnet_get_products("https://www.tunisianet.com.tn/466-console-de-jeux?page={}")
tnet_components = tnet_get_products("https://www.tunisianet.com.tn/406-composant-informatique?page={}")

# Get data: SBS Informatique
sbs_laptops = sbs_get_products("https://www.sbsinformatique.com/pc-portables-tunisie?page={}")
sbs_desktops = sbs_get_products("https://www.sbsinformatique.com/pc-gamer-tunisie?page={}")
sbs_monitors = sbs_get_products("https://www.sbsinformatique.com/moniteurs-tunisie?page={}")
sbs_accessories = sbs_get_products("https://www.sbsinformatique.com/accessoires-gaming-tunisie?page={}")
sbs_phones = sbs_get_products("https://www.sbsinformatique.com/smartphone-tunisie?page={}")
sbs_components = sbs_get_products("https://www.sbsinformatique.com/composants-tunisie?page={}")

# Get data: Mytek
mytek_laptops = mytek_get_products("https://www.mytek.tn/informatique/ordinateurs-portables.html?p={}")
mytek_desktops = mytek_get_products("https://www.mytek.tn/informatique/ordinateur-de-bureau/pc-de-bureau.html?p={}")
mytek_monitors = mytek_get_products("https://www.mytek.tn/informatique/ordinateur-de-bureau/ecran.html?p={}")
mytek_accessories = mytek_get_products("https://www.mytek.tn/informatique/peripheriques-accessoires.html?p={}")
mytek_phones = mytek_get_products("https://www.mytek.tn/telephonie-tunisie/smartphone-mobile-tunisie.html?p={}")
mytek_consoles = mytek_get_products("https://www.mytek.tn/gaming/console-de-jeux.html?p={}")
mytek_components = mytek_get_products("https://www.mytek.tn/informatique/composants-informatique.html?p={}")

# Add all data to the main container
laptops = {**tnet_laptops, **sbs_laptops, **mytek_laptops} # add more from other suppliers
desktops = {**tnet_desktops, **sbs_desktops, **mytek_desktops}
monitors = {**tnet_monitors, **sbs_monitors, **mytek_monitors}
phones = {**tnet_phones, **sbs_phones, **mytek_phones}
accessories = {**tnet_accessories, **sbs_accessories, **mytek_accessories}
consoles = {**tnet_consoles, **mytek_consoles}
components = {**tnet_components, **sbs_components, **mytek_components}

all_cat = [laptops, desktops, monitors, phones, accessories, consoles, components]

# Connect to the database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='helloalaa',
    db='TNDeals',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Create tables:

def table_exists(cursor, table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None

tables = ['laptops', 'desktops', 'monitors','phones','accessories','consoles','components']
try:
    with conn.cursor() as cursor:
        for table in tables:
            if not table_exists(cursor, table):
                sql = f'''CREATE TABLE `TNDeals`.`{table}` (`ref` text,`url` text DEFAULT '',`title` text DEFAULT '',`description` text DEFAULT '',`image` text DEFAULT '',`after_discount` text DEFAULT '',`before_discount` text DEFAULT '',`discount_amount` text DEFAULT '',`supplier` text DEFAULT '', PRIMARY KEY (`ref`(255),`supplier`(255)));'''
                cursor.execute(sql)
                print(table," created")

    conn.commit()  
    print("Tables created successfully")  

except Exception as e:
    print(f"Error: {e}")               

# Insert - Update - Delete

try:
    with conn.cursor() as cursor:
        # Delete  (search in the dictionary from the database)
        for table, products in zip(tables, all_cat):
            query = f"SELECT ref,supplier FROM {table};"
            cursor.execute(query)
            all_products = cursor.fetchall()
            for row in all_products:
                found = False
                for key,value in products.items():
                    if (value['ref']==row['ref'] and value['supplier']==row['supplier']):
                        found = True
                        break
                
                if (not found): # product from the db not found in the products in discount (dictionary)
                    cursor.execute(f"DELETE FROM {table} WHERE ref = %s AND supplier = %s;", (row['ref'], row['supplier']))
        
        conn.commit()
        print("Not in disount items deleted successfully")


        # Insert - Update (search in the database from the dictionary)
        for table, products in zip(tables, all_cat):
            for key, value in products.items():
                query = f"INSERT INTO `{table}` (`ref`, `url`, `title`, `description`, `image`, `after_discount`, `before_discount`, `discount_amount`, `supplier`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) \
                        ON DUPLICATE KEY UPDATE `title` = VALUES(`title`), `description` = VALUES(`description`), `after_discount` = VALUES(`after_discount`), `before_discount` = VALUES(`before_discount`), `discount_amount` = VALUES(`discount_amount`);"

                cursor.execute(query, (value.get("ref", ""), value.get("url", ""), value.get("title", ""), value.get("description", ""), value.get("img", ""), value.get("after_discount", ""), value.get("before_discount", ""), value.get("discount_amount", ""), value.get("supplier", "")))

    
    
        conn.commit()
        print("New items Inserted/Updated successfully")

except Exception as e:
    print(f"Error: {e}")

finally:
    conn.close()




"""" I think more efficient Insert-Update : if product found and the discount is the same, don't do anything

for table, products in zip(tables, all_cat):
    query = f"SELECT ref,supplier,discount_amount FROM {table}"
    cursor.execute(query)
    all_products = cursor.fetchall()

    for key,value in products.items():
        updated = False
        found = False
        for row in all_products:
            if (value['ref']==row['ref'] and value['supplier']==row['supplier']):
                found = True
            if (value['ref']==row['ref'] and value['supplier']==row['supplier'] and row['discount_amount']!=value['discount_amount']):
                cursor.execute("UPDATE products SET price = ? WHERE ref = ? AND supplier = ?", (value['discount_amount'], value['ref'], value['supplier']))
                updated = True
                break
                
        if not (updated and found):
            query = f"INSERT INTO `{table}` (`ref`, `url`,`title`, `description`,`image`, `after_discount`, `before_discount`, `discount_amount`,`supplier`) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s)"
            cursor.execute(query, (value.get("ref", ""),value.get("url", ""), value.get("title", ""), value.get("description", ""), value.get("img", ""), value.get("after_discount", ""), value.get("before_discount", ""), value.get("discount_amount", ""), value.get("supplier", "")))


"""

