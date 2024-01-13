from bs4 import BeautifulSoup
import requests


north_american_countries = ["USA", "Canada", "Puerto Rico", "The Dominican Republic", "Costa Rica", "Mexico",
                            "Guatemala", "US Virgin Islands", "Bermuda"]
european_countries = ["Ireland", "The U.K.", "The Isle of Man", "Jersey", "Portugal", "Spain", "The Canary Islands",
                      "Andorra", "Gibraltar", "France", "Belgium", "The Netherlands", "Luxembourg", "Italy",
                      "San Marino", "Norway", "Svalbard", "Sweden", "Finland", "Denmark", "The Faroe Islands",
                      "Iceland", "Greenland", "Germany", "Austria", "Switzerland", "Poland", "Lithuania",
                      "Latvia", "Estonia", "Czechia", "Slovakia", "Slovenia", "Hungary", "Croatia", "Albania",
                      "Greece", "Romania", "Montenegro", "Serbia", "North Macedonia", "Bulgaria", "Ukraine", "Russia",
                      "Malta"]
oceanic_countries = ["Australia", "New Zealand", "American Samoa", "Northern Mariana Islands", "Guam", "Midway Atoll",
                     "Christmas Island"]
african_countries = ["South Africa", "Botswana", "Eswatini", "Lesotho", "Uganda", "Kenya", "Rwanda", "Ghana",
                        "Nigeria", "Senegal", "Tunisia", "Reunion", "Madagascar"]
asian_countries = ["Bhutan", "Hong Kong", "Macau", "Japan", "Cambodia", "Thailand", "Taiwan", "South Korea",
                   "The United Arab Emirates", "Jordan", "Qatar", "Israel", "Palestine", "Lebanon", "Kyrgyzstan",
                   "Mongolia", "Indonesia", "Malaysia", "Vietnam", "Laos", "The Philippines", "Sri Lanka",
                   "Bangladesh", "India", "Pakistan", "Singapore", "Turkey"]
south_american_countries = ["Brazil", "Argentina", "Uruguay", "Ecuador", "Colombia", "Peru", "Bolivia", "Chile",
                            "Curacao"]

country_list = north_american_countries + european_countries + oceanic_countries + african_countries + asian_countries + south_american_countries
r = requests.get("https://somerandomstuff1.wordpress.com/2019/02/08/geoguessr-the-top-tips-tricks-and-techniques/")
soup = BeautifulSoup(r.content)

for header in soup.find_all("h3"):
    if header.text in country_list:
        file_name = ("_").join(header.text.split())
        print(file_name)
        with open("countries/" + file_name + ".txt", "w") as f:
            for elem in header.next_siblings:
                # stop at next header
                if elem.name == "h3":
                    break
                if elem.name == 'p':
                    f.write(elem.get_text() + " ")
                if elem.name == "div":
                    # find wp-caption-text
                    for caption in elem.find_all("p", {"class": "wp-caption-text"}):
                        f.write(caption.get_text() + " ")


