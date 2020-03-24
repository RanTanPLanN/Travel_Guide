import pandas as pd
import numpy as np
import os
import random
import matplotlib
import webbrowser
import urllib3

class Country:
    def __init__(self, name, willingness,continent):
        self.name = name
        self.willingness = willingness
        self.continent = continent

    # test function
    def status(self):
        print('I want to go to ' + self.name + ', ' + self.continent + ' ' + str(self.willingness))



def NextDestinations():
    # read excel sheet with countries
    basePath = r'C:\Users\nico\Dropbox\World_Travel_app'
    fileName = 'World_Travel_nikos.xlsx'

    loadFile = os.path.normpath(basePath + '/' + fileName)

    # load all the countries into dataframe
    countries = pd.read_excel(loadFile, skiprows=0, header=0,sheet_name=0, usecols="A:E")
    countries.set_index(keys='country', drop=False, inplace=True)

    countries.set_index(keys='country', drop=True, inplace=True)

    # create random durations for couontries. This will be removed when deciding on a duration for each country.
    countries['duration'] = random.sample(range(1,1000000),len(countries))
    countries['duration'] = countries['duration']%4

    # loop to suggest countries to user, based on the duration of their vacation.
    dur = -1
    while dur < 2:
        # ask for input. If it is not a number throw a warning and repeat the loop.
        try:
            # ask user how many days they want to travel
            dur = int(input('How many days maximum do you want to go on vacation? \n'))
            if dur < 2: print('Stay home you lazy mothefucka!')
        except ValueError:
            print('Eeem...You know you need to type in a number right??! Try again you dumbass!\n')

    # create duration bins. The duration bins are <4, 5-10, 11-17, 18>
    durBins = np.array([4, 10, 17])

    # find in which 'duration group' belong the days the user suggested
    durGroup = np.digitize(dur,durBins, right=True)

    # search only in the countries that belong in the duration bins that are lower or equal to the duration input
    # from the user.
    countries = countries[countries['duration'] <= dur]

    # group countries based on their 'continent'
    continents = countries.groupby(by='continent')

    options = []
    for cont, contData in continents:

        # pick a random number that corresponds to the country
        iindx = random.randint(0,len(contData)-1)
        selectCountry = contData.iloc[iindx:iindx+1, :]

        # this is just a test that the class object works fine. It will be removed.
        tempCountry = Country(name=selectCountry.index[0], willingness=selectCountry['willingness'], continent=selectCountry['continent'])
        tempCountry.status()

        # append selected countries in a list
        options.append(selectCountry)

    # concat list with selected countries and sort them based on 'willingness'
    SixCountries = pd.concat(options,axis='index')
    SixCountries.sort_values(by='willingness', inplace=True, ascending=False)

    # print the 6 selected countries.
    print(SixCountries.index.tolist())

    # pick winner
    winner = SixCountries.iloc[:1,:]

    # check if website exists for this country exists in Lonely Planet
    searchStr = winner.index[0].replace(" ", "-").lower()
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://www.lonelyplanet.com/' + searchStr)

    # if it exists, re-direct user to the lonely planet website about the country
    if r.status == 200:
        webbrowser.open('https://www.lonelyplanet.com/' + searchStr)

    # if it doesnt exist, search lonely planet for threads related to the country
    else:
        webbrowser.open('https://www.lonelyplanet.com/search?q=' + searchStr)


    print('end')


if __name__ == '__main__':
    NextDestinations()
