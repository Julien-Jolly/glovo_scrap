from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs
import json

towns = ["rabat", "casablanca"]
BASE_URL = "https://glovoapp.com"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    url = "https://glovoapp.com/ma/en/rabat/"

    page.goto(url)
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Login").click()
    page.locator('[data-test-id="email-button"]').click()
    page.get_by_test_id("input").click()
    page.get_by_test_id("input").fill("jul.jolly@hotmail.com")

    page.locator('[data-test-id="submit-button"]').click()
    page.wait_for_timeout(3000)
    page.get_by_test_id("input").click()
    page.get_by_test_id("input").fill("Zoiuzou2017")
    page.get_by_test_id("input").press("Enter")
    # page.locator("[data-test-id=\"submit-button\"]").click()
    page.wait_for_timeout(3000)
    page.get_by_test_id("input").click()
    page.get_by_test_id("input").fill("rabat")
    page.get_by_text("RABAT CENTRE").click()

    # FOOD
    # page.locator("[data-test-id=\"category-bubble-food\"] [data-test-id=\"category-bubble\"]").click()

    # ?
    # page.goto("https://glovoapp.com/ma/en/rabat/")

    # CHOIX GROCERY
    page.locator(
        '[data-test-id="category-bubble-groceries"] [data-test-id="category-bubble-image"]'
    ).click()
    page.wait_for_timeout(3000)
    print("accessing sector...")
    content_sector = page.content()
    soup = bs(content_sector, "html.parser")
    urls = [link["href"] for link in soup.find_all("a", class_="category-bubble__link")]
    categories = list(set(urls))
    print(categories)

    # temp_url=(['/ma/en/rabat/groceries_4/'])

    category_store_dict = {}
    for url in categories:
        active_url = BASE_URL + url
        page.goto(active_url)
        sub_store_code = page.content()
        soup = bs(sub_store_code, "html.parser")
        stores = [link["href"] for link in soup.find_all("a", class_="store-card")]
        print(f"dans {active_url} : {stores}")
        category_store_dict[url] = stores

    filename = "category_store_data.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(category_store_dict, f, ensure_ascii=False, indent=4)

    print(f"Le dictionnaire a été enregistré dans le fichier {filename}")

"""
        for _ in stores:
            active_url = BASE_URL + _
            page.goto(active_url)
            store_detail = page.content()
            sections = soup.find_all('a', class_='section-link')
            for section in sections:
                section_name = section.find('p').text.strip()  # Nom de la section
                section_url = section['href']  # URL de la section
                print(f"Section: {section_name} | URL: {section_url}")

            # Extraction des éléments dans les sous-sections (accordion)
            subsections = soup.find_all('button', class_='accordion__item__trigger')
            for subsection in subsections:
                subsection_name = subsection.find('span').text.strip()  # Nom de la sous-section
                print(f"Sous-section: {subsection_name}")




        sub_store_list = soup.find(attrs={'data-test-id': 'category-store-list'})
        sub_store_url_list = sub_store_list.find_all('a', class_='category-bubble__link')
        sub_store_urls = [link['href'] for link in sub_store_url_list]
        print(f'pour {active_url} : {sub_store_urls}')



    # CHOIX MAGASIN
    page.locator("[data-test-id=\"category-store-list\"]").get_by_role("link", name="89% (347) Carrefour Market").click()
    print("accessing store...")

    # CHOIX CATEGORIE
    page.locator("[data-test-id=\"side-menu-element-top-sellers-ts\"] [data-test-id=\"accordion-item-button\"]").click()
    page.wait_for_timeout(3000)
    content_store = page.content()
    print("accessing category...")


    soup = bs(content_store, "lxml")
    sector = soup.find('div', attrs={'class': 'address-picker__address__text'}).string.strip()
    store = soup.find(attrs={'data-test-id': 'store-info-title'}).string.strip()
    prod = soup.find(attrs={'data-test-id': 'tile__highlighter'}).string.strip()
    n_price = soup.find(attrs={'data-test-id': 'product-price-effective'}).string.strip()
    if soup.find(attrs={'data-test-id': 'product-price-original'}):
        o_price = soup.find(attrs={'data-test-id': 'product-price-original'}).string.strip()
    else:
        o_price=0

    print(sector)
    print(store)
    print(prod)
    print(n_price)
    print(o_price)





"""
