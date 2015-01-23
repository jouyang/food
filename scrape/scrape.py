from bs4 import BeautifulSoup
import requests

# url = "http://allrecipes.com/Recipe/Scrumptious-Salmon-Cakes/Detail.aspx?soid=recs_recipe_1"
# returned in [(quantity,ingredient),(quantity2,ingredient2),...]
def ingredients(url):
	response = requests.get(url)

	soup = BeautifulSoup(response.text)

	ingredients_full = soup.findAll('p', attrs =  {'class':'fl-ing'})
	ingredients = []
	for ingred in ingredients_full:
		pieces = ingred.findAll('span')
		ingredients.append((pieces[0].text,pieces[1].text))

	return ingredients
