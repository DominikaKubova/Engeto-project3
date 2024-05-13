##Elections Scraper
#https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ
"""
projekt_3.py: tretí projekt do Engeto Online Python Akademie
author: Dominika Kubová
email: dominika.kubova@kbc.com
discord: dominika_50263
"""

import requests
from bs4 import BeautifulSoup
import sys
import csv

def check_arguments():
    """Check if both arguments are valid for the program to proceed further. 
    If not, specific error message is printed.
    """

    forbidden_characters = ["\\", "/", ":", "*", "?", ",", "<", ">", "|", " "]
    for i in forbidden_characters:
        if  i in file_name:
            print("You are using a name with forbidden character.\n"\
                  "Please rename the file!")
            break
        else:
            continue

    if url == "" or  file_name == "":
        print("We are missing one of requred arguments! Start over.")
        sys.exit()

    file_name_end = file_name[-4:]

    if file_name_end != ".csv":
        print("You are missing a correct format type in the file name.")
        sys.exit()

    url_beginning = "https://volby.cz/pls/ps2017nss/"
    if  url[:31] != url_beginning or len(url) != 67:
        print("You have not used correct format of url for chosen territorial unit.")
        sys.exit()
  

def url_download(url: str) -> BeautifulSoup: 
    """Downloading data from url provided as a 1st argument when starting a programme
    
    Keyword arguments:
    url -- mandatory argument allocating url for specific territorial district     
    """
    url_downloaded = url
    data = requests.get(url_downloaded)

    soup = BeautifulSoup(data.content, "html.parser")
    return soup

def find_sub_urls(soup: BeautifulSoup) -> BeautifulSoup:
    """Downloading additional data from 1st parameter url - for every parameter "cislo" -
    containing all data from each sub-site
    
    Keyword arguments:
    soup -- downloaded data from 1 argument url     
    """
    sub_results = soup.find_all("td", class_="cislo")
    sub_soups = []
    for i in sub_results:
        get_url = "https://volby.cz/pls/ps2017nss/" + i.find("a")["href"]
        sub_data = requests.get(get_url)
        sub_soup = BeautifulSoup(sub_data.content,"html.parser")
        sub_soups.append(sub_soup) 
    return sub_soups

def district_code(all_district_codes_data: BeautifulSoup) -> list:
    """Returns all district codes under 1st argument based on "ahref" and amends to correct format by slicing.

    Keyword arguments:
    all_district_codes_data -- downloaded data for all district codes under 1st argument  
    """
    find_code = all_district_codes_data.find("div", attrs={"class" : "tab_full_ps311"}).a["href"]
    code = find_code[30:36]
    return code

def district_name(all_district_codes_data: BeautifulSoup) -> list:
    """Returns name of every district under 1st argument based on "h3" on the 3rd place.
    Format is amended to contain only the name.
    
    Keyword arguments:
    all_district_codes_data -- downloaded data for all district codes under 1st argument
    """
    code_name = (all_district_codes_data.find_all("h3"))[2]
    name = (code_name.get_text())[7:].strip()
    return name

def table_1(all_district_codes_data: BeautifulSoup) -> list:
    """Returns number of voters, envelopes and valid votes from 1st table for every district code based
    on found id "ps311_t1" and "td" and position in the table on 4th, 5th and 8th column.
    
    Keyword arguments:
    all_district_codes_data -- downloaded data for all district codes under 1st argument
    """
    table_1 =  all_district_codes_data.find(id="ps311_t1")
    table_row = table_1.find_all("td")
    voters = table_row[3].get_text().replace(u"\xa0", u"")
    envelopes = table_row[4].get_text().replace(u"\xa0", u"")
    valid_votes = table_row[7].get_text().replace(u"\xa0", u"")
    return voters, envelopes, valid_votes

def table_2(all_district_codes_data: BeautifulSoup) -> dict:
    """Returns a dictionary with the name of party as a key and number of votes as a value.
    Data are located for every district code for all tables starting from the 2nd, with "tr" starting from 3rd position.
    Values on the 2nd and 3rd column are returned with corrected format.
    
    Keyword arguments:
    all_district_codes_data -- downloaded data for all district codes under 1st argument
    """
    table_2 = all_district_codes_data.find_all(class_="table" )[1:]
    party_total_votes = dict()
    for table in table_2:
        tr_data = table.find_all("tr")[2:]
        for tr in tr_data:
            td_data = tr.find_all("td")
            party = td_data[1].get_text()
            votes_party = td_data[2].get_text().replace(u"\xa0", u"")
            party_total_votes.update({party : votes_party})
    return party_total_votes
    
def full_data(url: str) -> list | dict:
    """Returns data for every district code.
    
    Keyword arguments:
    url -- mandatory argument allocating url for specific territorial district 
    """
    district_url_data = url_download(url)
    all_district_codes_data = find_sub_urls(district_url_data)
    rows = []
    for code in all_district_codes_data:
        found_district_code = district_code(code)
        found_district_name = district_name(code)
        voters, envelopes, valid_votes = table_1(code)
        table_2_data = table_2(code)
        row_for_code = [found_district_code ,found_district_name, voters , envelopes, valid_votes] + list(table_2_data.values())
        rows.append(row_for_code)
    return rows, table_2_data

def creating_csv(party_total_votes: dict, rows: list): 
    """Creates a csv file based on predefined names of colums. Data for every district code 
    are written to each row.
    
    Keyword arguments:
    party_total_votes -- dictionary cotaining all party names as a key and number of votes 
    for party as value for every district code
    rows -- data for each district code saved to each row in csv file 
    """
    fields_1 = ["Code", "Name", "Voters", "Total envelopes", "Valid votes"]
    fields = fields_1 + list(party_total_votes.keys())
    
    with open (file_name, "w", newline='') as f:

        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)

## MAIN CODE ##

if __name__ == "__main__":

    url = sys.argv[1] 
    file_name = sys.argv[2]
    #print(sys.argv[1])
    #print(sys.argv[2])
    check_arguments()

    rows, party_total_votes = full_data(url)
    creating_csv(party_total_votes, rows)
    print("Requested file .csv created!")
    

