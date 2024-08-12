from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

import numpy
import statistics
import plotly.graph_objects as po
import plotly.express as px
import pandas as pd

options1 = Options()
options1.add_experimental_option("detach", True)

query = input ("Enter search query: ")
querytransformed = query.replace(' ','+')

driver = webdriver.Chrome(options=options1)
driver.maximize_window()
driver.implicitly_wait(10)
driver.get("https://www.amazon.com/s?k="+querytransformed)
driver.minimize_window()

# Find all elements that have an 'aria-label' attribute containing star ratings
rating_elements2 = driver.find_elements(By.XPATH, "//div[@class='a-section a-spacing-small a-spacing-top-small']")
ratings2 = []
values = []
fractions = []

ratings2priceRatingPresent = [False]*len(rating_elements2)
i=0
for element2 in rating_elements2:
    try:
        element3 = element2.find_element(By.XPATH, ".//span[contains(@aria-label, 'out of 5 stars')]")
        rating = element3.get_attribute('aria-label')
        rating = rating.replace(' out of 5 stars','')
        rating = float(rating)
        ratings2.append(rating)
        element4 = element2.find_element(By.XPATH, ".//span[contains(@class, 'a-price-whole')]")
        if(element4.text!=""):
            val = int(element4.text.replace(',',''))
            values.append(val)
        element5 = element2.find_element(By.XPATH, ".//span[contains(@class, 'a-price-fraction')]")
        if(element5.text!=""):
            frac = int(element5.text.replace(',',''))/100
            fractions.append(frac)
        ratings2priceRatingPresent[i]=True
    except NoSuchElementException:
        # Handle the case where the inner div is not found within the current 'a-section'
        pass
    i = i+1
#combine fractions with values
values = [ values[x] + fractions[x] for x in range (len (values))]

mean = numpy.mean(values)
median = numpy.mean(values)
print("Mean Price: ")
print(numpy.mean(values))
print("Standard Deviation of Price: ")
print(numpy.sqrt(numpy.var(values)))
fig = px.histogram(values,nbins=30)

mean_trace = po.Scatter(x=[mean, mean], y=[0, max(fig.data[0])], mode='lines', name='Mean', line=dict(color='red', width=2))
fig.add_trace(mean_trace)

fig.update_layout(
    title="Price of \""+query+"\" on Amazon:",
    xaxis_title="Price",
    font=dict(
        family="Courier New",
        size=18,
        color="black"
    ),
    shapes= [{'line': {'color': 'red', 'dash': 'solid', 'width': 1},
    'type': 'line',
    'x0': mean,
    'x1': mean,
    'xref': 'x',
    'y0': -0.1,
    'y1': 1,
    'yref': 'paper'}]
)

fig.show()

# fig2 = px.scatter(values,ratings2)
# fig2.show()

df = pd.DataFrame({'Values': values, 'Ratings': ratings2})

# Plot using Plotly Express
fig = px.scatter(df, x='Values', y='Ratings', trendline="ols", labels={'Values': 'Price', 'Ratings': 'Rating'}, title='Values vs Ratings: '+query)
fig.show()