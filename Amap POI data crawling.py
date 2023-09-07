import requests
import pandas as pd
import os

# This programme is designed to collect coordinates of different kinds of POI data in multiple cities by calling API of Amap.
# key
map_api_key = 'e9e5ecba1e606f37e7aa3f56e2bd6408'

# prefix of the request URL
req_url_pref = 'https://restapi.amap.com/v3/place/text?parameters'

# set the number of data in each page (25 in maximum)
page_size = 25


# the function of creating a new folder
def create_folder(city):
    folder_path = f'F:/data/{city}'  # name the folder path
    os.makedirs(folder_path)  # create the folder according to the new path


# the function of data crawling
def get_poi_from_map(keyword, city):
    # keyword: the kind of POI data you need
    # city: the city where the data is located in

    # header
    req_params = {
        'keywords': keyword,
        'city': city,
        'offset': page_size,
        'page': 1,
        'extensions': 'all',
        'key': map_api_key,
        'children': 1,
        'citylimit': 'true'
    }

    result = pd.DataFrame()  # initialization

    i = 1
    while True:
        print("i", i)
        req_params["page"] = i
        response = requests.get(req_url_pref, params=req_params)  # use the header to get data
        data = response.json()  # return data as json
        count = data["count"]
        print("count", count)
        if count == "0":  # condition of ending the loop
            break

        for j in range(0, len(data["pois"])):
            name = data["pois"][j]["name"]  # name of the POI
            address = data["pois"][j]["address"]  # address of the POI
            lon = data["pois"][j]["location"].split(",")[0]  # longitude of the POI
            lat = data["pois"][j]["location"].split(",")[1]  # latitude of the POI
            busi_data = [
                {
                    "name": name,
                    "address": address,
                    "lon": lon,
                    "lat": lat
                }
            ]

            df = pd.DataFrame(busi_data)  # store the data in a pandas data frame
            result = result.append(df)  # store the data of single POI in the general data frame

        # reset the index
        result.reset_index(drop=True, inplace=True)
        print(result)

        i += 1

    # save the data frame as a csv file
    output_path = f'F:/data/{city}/{keyword}.csv'  # set the path of the csv file
    result.to_csv(output_path)  # save the file according to the path


list_keyword = ["大学", "大专", "商业", "酒店"]  # the list of the POI kinds (universities, colleges, business, hotels)
list_city = ["南京", "苏州", "扬州", "徐州"]  # the list of the cities (Nanjing, Suzhou, Yangzhou, Xuzhou)

# function call
for x in list_city:
    create_folder(x)  # create folders

    for y in list_keyword:
        get_poi_from_map(y, x)  # POI data crawling
