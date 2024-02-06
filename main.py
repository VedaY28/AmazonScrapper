from playwright.sync_api import sync_playwright
from discord import SyncWebhook
from discord import Embed

from datetime import datetime
import sys

# https://discord.com/api/webhooks/1204312751367921665/ozPnLt3OPi1dG2jDLgWwCCX8Wq97Ogob3CYa9c2odPB4oj2zcvImj5A9KgP69-PE65St


def sendToDisc(embed):
    webhook = SyncWebhook.partial('1204312751367921665','ozPnLt3OPi1dG2jDLgWwCCX8Wq97Ogob3CYa9c2odPB4oj2zcvImj5A9KgP69-PE65St')
    webhook.send(username='Amazon Bot', embed=embed)


def main():
    for link_index, link in enumerate(products_links):
        
        print(f'Scraping Product: {link_index}')

        page.goto(link, wait_until='domcontentloaded')
        page.wait_for_timeout(5_000) 

        title_xpath = '//span[@id="productTitle"]'
        original_price_xpath = '//span[contains(@class, "a-price a-text-price")]//span[@class="a-offscreen"]'
        discounted_price_xpath = '//span[contains(@class, "priceToPay")]'

        title = page.locator(title_xpath).inner_text()

        original_price_elements = page.locator(original_price_xpath).all()
        if original_price_elements:
            original_price = original_price_elements[0].inner_text()
            discounted_prices = main2(discounted_price_xpath, link)
            print(discounted_prices)
            print(f'Title: {title}\nOriginal Price: {original_price}\nDiscounted Price: {discounted_prices[0]}\nLink: {link}')
            
            em = Embed(title= title, description='', color=242424)
            em.add_field(name='URL', value= link, inline=False)
            em.add_field(name='Original Price', value= original_price, inline=False)
            em.add_field(name='Discounted Price', value= discounted_prices[0], inline=False)
            em.timestamp = datetime.now()
            em.set_footer(text='Powered By Amazon Bot')

            sendToDisc(em)
        else:
            # If original price is not found, use the discounted price
            discounted_prices = main2(discounted_price_xpath, link)
            if discounted_prices:
                original_price = discounted_prices[0]
                print(f'Title: {title}\nOriginal Price: {original_price}\nDiscounted Price: {"None"}\nLink: {link}')
                em = Embed(title= title, description='', color=242424)
                em.add_field(name='URL', value= link, inline=False)
                em.add_field(name='Original Price', value= original_price, inline=False)
                em.add_field(name='Discounted Price', value= 'None', inline=False)
                em.timestamp = datetime.now()
                em.set_footer(text='Powered By Amazon Bot')

                sendToDisc(em)
        
def main2(path, lin):
    try:
        page.goto(lin, wait_until='domcontentloaded')
        page.wait_for_timeout(5_000)

        raw_discounted_prices = [element.inner_text() for element in page.locator(path).all()]

        formatted_discounted_prices = []
        for raw_discounted_price in raw_discounted_prices:
            discounted_price = ''.join(c for c in raw_discounted_price if c.isdigit() or c in ['.', ','])
            formatted_discounted_price = f"${discounted_price}"
            formatted_discounted_prices.append(formatted_discounted_price)

        unique_discounted_prices = list(set(formatted_discounted_prices))

        # print(f"Formatted Discounted Prices: {unique_discounted_prices}")

        return unique_discounted_prices
    except Exception as e:
        print(f"An error occurred while retrieving Discounted Prices: {e}")
        return None


if __name__ == '__main__':
    
    with open('products_links.txt') as f:
        products_links = f.readlines()

    if len(products_links) == 0:
        print('No links found in products_links.txt')
        sys.exit()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context()
        page = context.new_page()

        main()
        context.close()
        browser.close()

