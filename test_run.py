import lxml
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from requests import get

url1 = "https://www.imdb.com/search/title?count=100&title_type=feature,tv_series&ref_=nv_wl_img_2" # for testing

class IMDB(object):
    
    def __init__(self, url):
        super(IMDB, self).__init__()
        page = get(url)

        self.soup = BeautifulSoup(page.content, 'lxml')

    def articleTitle(self):
        return self.soup.find("h1", class_="header").text.replace("\n","")

    def bodyContent(self):
        content = self.soup.find(id="main")
        return content.find_all("div", class_="lister-item mode-advanced")

    def movieData(self):
        movieFrame = self.bodyContent()
        movieTitle = []
        movieDescription = []
        movieDate = []
        movieRunTime = []
        movieGenre = []
        movieRating = []
        
        for movie in movieFrame:
            movieFirstLine = movie.find("h3", class_="lister-item-header")
            movieTitle.append(movieFirstLine.find("a").text)
            movieDate.append(re.sub(r"[()]","", movieFirstLine.find_all("span")[-1].text))
            try:
                movieRunTime.append(movie.find("span", class_="runtime").text[:-4])
            except:
                movieRunTime.append(np.nan)
            try:
                movieGenre.append(movie.find("span", class_="genre").text.rstrip().replace("\n","").split(","))
            except:
                movieGenre.append(np.nan)
            try:
                movieRating.append(movie.find("strong").text)
            except:
                movieRating.append(np.nan)
                
            movieDescription.append(movie.find_all("p", class_="text-muted")[-1].text.lstrip())

            movieNumbers = movie.find_all("span", attrs={"name": "nv"})

        movieData = [movieTitle,movieDescription, movieDate, movieRunTime, movieGenre, movieRating]
        return movieData
        

def imdb_url(index):
    idx = index + 1
    url = "https://www.imdb.com/search/title/?title_type=feature,tv_series&count=100&start={}&ref_=adv_nxt".format(idx)
    return url

def treat_name(title):
    new_title = ""
    for letter in title:
        if letter == "/":
            new_title = new_title + ""
        else:
            new_title = new_title + letter
    return new_title
    
    
def run(numberOfMovies):
    for num in range(1,numberOfMovies,100):
	    try:
			url = imdb_url(num)
			id1 = IMDB(url)
			movieData = id1.movieData()
            print(num)

            for i in range(100):
				title = movieData[0][i]
                new_title = treat_name(title)
                descr = movieData[1][i]
                with open("IMDB/{}.txt".format(new_title), 'w') as f:
                    print(descr, file=f)
        except:
			print("Error found")
        
def test_run():
	run(1000)
