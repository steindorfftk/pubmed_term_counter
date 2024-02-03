from bs4 import BeautifulSoup
import requests
import os

def term_names_reader(): #returns term names from term_list.txt file 
	terms = []
	with open('term_list.txt', 'r') as texto:
		for line in texto:
			linha = line.split()
			if len(linha) > 0:
				terms.append(linha[0])
	return terms

def output_maker():
	if 'output.csv' not in os.listdir():	
		with open('output.csv','w') as data_text:
			data_text.write('Term;Counts')


def get_website_content(url): #Gets url content
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def extract_counts(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        div_results = soup.find('div', class_='results-amount')
        value = div_results.find('span', class_='value').text.strip()
        return value
    except Exception as e:
        print(f"Error extracting value: {e}")
        return 'Not found'

def save_data(term, count):
	with open('output.csv','a') as data_text:
		data_text.write('\n' + term + ';' + count)

def done_terms_counter():
	done_terms = []
	with open('output.csv','r') as data_text:
		for line in data_text:
			if 'Term' not in line:
				linha = line.replace(';',' ').split()
				done_terms.append(linha[0])
	return done_terms			
	
def main():
	output_maker()
	a=0
	terms = term_names_reader()
	terms = [x for x in terms if x not in done_terms_counter()]
	a+=len(done_terms_counter())
	for term in terms:
		link = 'https://pubmed.ncbi.nlm.nih.gov/?term=' + term
		page = get_website_content(link)	
		count = extract_counts(page)
		save_data(term, count)
		a+=1
		print(str(a) + '/20675')

main()	


