from selenium import webdriver
from bs4 import BeautifulSoup
import requests, ast

class scraper:

	searchUrl = 'https://www.freshdirect.com/srch.jsp?pageType=search&searchParams=%s&pageSize=30&all=false&activePage=1&sortBy=Sort_Relevancy&orderAsc=true&activeTab=product'
	
	def __init__(self):
		self.driver = webdriver.PhantomJS()

	def closeDriver(self):
		self.driver.close()

	# url = "http://allrecipes.com/Recipe/Scrumptious-Salmon-Cakes/Detail.aspx?soid=recs_recipe_1"
	# returned in [(quantity,ingredient),(quantity2,ingredient2),...]
	def getRecipeIngredients(self, url):
		response = requests.get(url)

		soup = BeautifulSoup(response.text)
		ingredients_full = soup.findAll('p', attrs =  {'class':'fl-ing'})
		ingredients = []	
		for ingred in ingredients_full:
			pieces = ingred.findAll('span')
			ingredients.append((pieces[0].text,pieces[1].text))

		return ingredients

	'''
	Given ingredient name, find the info necessary, first search with webdriver.phantomJS, parse with bs
	"items": [
        {
            "salesUnit": "EA",
            "quantity": "1",
            "atcItemId": "atc_mea_pid_3342133_MEA3342133_cbrstbnin",
            "productId": "mea_pid_3342133",
            "categoryId": "cbrstbnin",
            "skuCode": "MEA3342133",
            "pageType": "SEARCH"
        }*/
    '''

    #Returns the whole html that we need in a bs4 tag object
	def getFoodData(self,ingredient_name):
		searchUrl_item = self.searchUrl % ingredient_name
		self.driver.get(searchUrl_item)
		response = self.driver.page_source
		soup = BeautifulSoup(response)
		return soup.find('input', attrs={'data-component':'productData'})

	#Returns the unit of the item from the item html
	def getFoodUnit(self,itemData):
		subtotalDiv = itemData.find('div', attrs={'class':'subtotal'})
		unitDictString = subtotalDiv['data-suratio']
		unitDict = ast.literal_eval(unitDictString)
		return unitDict[0]['unit']

	#Returns a dictionary of product parameters for post request
	def getFoodParams(self,itemData):
		params = itemData.findAll('input',attrs={'data-component':'productData'})
		paramsDict = {'atcItemId':params[0]['value'],
					  'productId':params[1]['value'],
					  'categoryId':params[2]['value'],
					  'skuCode':params[3]['value'],
					  'pageType':params[4]['value']}
		return paramsDict

	#Returns the dictionary with all the essential params
	def getFoodJson(self,ingredient_name):
		itemData = self.getFoodData(ingredient_name)
		itemDict = self.getFoodParams(itemData)
		itemDict['salesUnit'] = self.getFoodUnit(itemData)
		itemDict['quantity'] = '1'
		return itemDict

	#Returns a list of the all the json for all the ingredients in a recipe
	def getRecipeIngredientsJson(self, url):
		print 'Getting ingredients'
		ingredients = self.getRecipeIngredients(url)
		print 'Obtained ingredients:'
		print ingredients
		ingredientsJson = []
		for (quantity,ingredient) in ingredients:
			print 'Obtaining Json for ingredient ' + ingredient
			json = self.getFoodJson(ingredient)
			print 'Obtained Json successfully'
			print json
		return ingredientsJson






