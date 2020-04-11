def scrape():
    from bs4 import BeautifulSoup as bs4_BeautifulSoup
    from splinter import Browser as splinter_Browser
    import requests
    import pandas as pd
    import time

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = splinter_Browser('chrome', **executable_path, headless = False)
    mars_info = {}

    ### NASA Mars News: ###
    nasa_mars_news_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_mars_news_url)
    html_response = browser.html
    nasa_mars_news_soup = bs4_BeautifulSoup(html_response, "html.parser")
    news_title = nasa_mars_news_soup.find("div", class_="content_title").text
    news_p = nasa_mars_news_soup.find("div", class_="article_teaser_body").text
    mars_info["news_title"] = news_title
    mars_info["news_p"] = news_p

    ### JPL Mars Space Images - Featured Image: ###
    jpl_mars_space_images__featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_mars_space_images__featured_image_url)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(3)
    browser.click_link_by_partial_text("more info")
    html_response = browser.html
    jpl_mars_space_images__featured_img_soup = bs4_BeautifulSoup(html_response, "html.parser")
    featured_image = jpl_mars_space_images__featured_img_soup.find("figure").find("a")["href"]
    featured_image_url = f"https://www.jpl.nasa.gov{featured_image}"
    #print(featured_image_url)
    mars_info["featured_image_url"] = featured_image_url

    ### Mars Weather (Twitter): ###
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(mars_weather_url)
    mars_weather_soup = bs4_BeautifulSoup(response.text, "html.parser")
    mars_weather = mars_weather_soup.find("div", class_="js-tweet-text-container").text.strip()
    mars_info["mars_weather"] = mars_weather

    ### Mars Facts: ###
    mars_facts_url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(mars_facts_url)
    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = ["description", "value"]
    mars_facts_df = mars_facts_df.set_index("description")
    facts_html = mars_facts_df.to_html().strip()
    mars_info["facts_html"] = facts_html

    ### Mars Hemispheres: ###
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemispheres_url)
    html_response = browser.html
    mars_hemispheres_soup = bs4_BeautifulSoup(html_response, "html.parser")
    hemisphere_image_urls = []
    mars_hemis = mars_hemispheres_soup.find_all("div", class_="description")
    
    for mars_hemi in mars_hemis:
        title = mars_hemi.find("h3").text
        next_page = mars_hemi.find("a")["href"]
        browser.visit(f"https://astrogeology.usgs.gov{next_page}")
        html_response = browser.html
        soup_mars_hemi = bs4_BeautifulSoup(html_response, "html.parser")
        img_url = soup_mars_hemi.find("div", class_="downloads").find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": img_url})
        
    mars_info["hemisphere_image_urls"] = hemisphere_image_urls
    
    browser.quit()
    
    return mars_info