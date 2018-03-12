from bs4 import BeautifulSoup
import requests
import os



def get_price_list(url):
	html = requests.get(url)
	soup = BeautifulSoup(html.content, "html.parser")  # 'BeautifulSoup' gets only 'html' file/content.
	all_tables = soup.find_all("table")  # get data from table tag "<table>".
	price_table = all_tables[1]
	table_rows = price_table.find_all("tr")
	price_list = []

	for row in table_rows:
		name_and_quantity = row.find_all("td")[1].text[:-3]  # find simple text from <td> tag.
		price = row.find_all("td")[2].text
		add = name_and_quantity+', '+price
		price_list.append(add)

	return price_list


def create_file_path(url):
	html = requests.get(url)
	soup = BeautifulSoup(html.content, "html.parser")
	file_name = soup.find_all("h1")[1].text.replace('/','-')
	dir_path = "./Data"
	
	if not os.path.exists(dir_path):
		os.mkdir(dir_path)
	
	file_path = dir_path+"/"+file_name+".csv"
	return file_path


def create_CSV_file(url):
	link = url
	file_path = create_file_path(link)

	if not os.path.isfile(file_path):
		content_as_list = get_price_list(link)[1:]
		file_object = open(file_path, "w+")
		file_object.write("Name and Quantity, Price in Rs\n")
		for row in content_as_list:
			file_object.write(row + '\n')
		file_object.close()



url = "http://www.livechennai.com/Vegetable_price_chennai.asp"
create_CSV_file(url)

