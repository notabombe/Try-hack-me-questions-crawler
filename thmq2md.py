#!/bin/python3
from selenium import webdriver
from bs4 import BeautifulSoup
import re, sys



style ="<style>answers{color:lawngreen;} questions{color:LightSeaGreen;}task{color:Tomato;} note{color:Orchid;} header{color:Gainsboro;}</style>\n"
T=[" <task> "," </task> "]
A=[" <answers> "," </answers> "]
Q=[" <questions> "," </questions> "]
H=[" <header> "," </header> "]
N=[" <note> "," </note> "]





def getTotalQ(data):
	return re.finditer(r"task-\d+", data)


def getData(url):
	fireFoxOptions = webdriver.FirefoxOptions()
	fireFoxOptions.headless = True
	brower = webdriver.Firefox(options=fireFoxOptions, executable_path = './geckodriver')
	brower.get(url)
	r = brower.page_source
	brower.quit()
	return r

def extractData(tag, data="", clas="", url="", id1=""):
	if data == "":
		html = getData(url)
		contents = BeautifulSoup(html, 'html5lib')
	else:
		contents = BeautifulSoup(data, 'html5lib')
	if clas == "" and id1 == "":
		return contents.find_all(tag)
	elif id1 != "" and clas== "":
		return contents.find_all(tag, {"id":id1})
	elif id1 == "":
		return contents.find_all(tag, {"class":clas})
	else:
		return contents.find_all(tag, {"id":id1},{"class":clas})


def filtering(data, tag):
	return re.finditer(r"<p>(.*)</p>", data)

def cleanH(raw):
	cleanr = re.compile('<.*?>')
	return re.sub(cleanr, '', raw)

def main():

	url = ""
	file = ""
	raw = False
	if len(sys.argv) == 1:
		url = input("enter URL for the room :" )
		file = input("enter output file name with path :")
	else :
		for arg in sys.argv[1:]:
			if arg.find("http") > -1:
				url = arg
			elif arg.find("-raw") > -1:
				raw = True
			else :
				file = arg

	if raw:
		T[:]=[" "," "]
		A[:]=[" "," "]
		Q[:]=[" "," "]
		H[:]=[" "," "]
		N[:]=[" "," "]
		style=""
	source = getData(url)
	tasks = getTotalQ(source)
	room = extractData(data=source, id1="title", tag='h1')
	with open(file, 'w') as f:
		f.write(style)
		f.write(f"#{H[0]} {room[0].get_text()}{H[1]}\n\n")
		for task in tasks:
			questions = str(extractData(data=source, id1=task.group(0), tag='div'))
			question = str(extractData(data=questions, tag='div', clas='room-task-question-details'))
			title = extractData(data=questions, clas="card-link", tag='a')
			for ti in title:
				f.write(f"##{T[0]}{str(ti.get_text()).strip()}" + f"{T[1]}\n")
			da = filtering(question, "p")
			for num, i in enumerate(da, start=1):
				f.write(
					f"\t{num}. **{cleanH(i.group(1).strip())}"
					+ f'**\n\t\t*{A[0]} answer here {A[1]}\n'
				)
			f.write("\n<br>\n")
	print("done")

if __name__ == '__main__':
	main()
