#!/usr/bin/env python3

import argparse
import rauth
import requests
import sys
import json
from pprint import pprint
import logging

class DatasetCreator:

    def __init__(self, settings_file, auth_file):
        self.__settings_dict = self.read_json(settings_file)
        self.__auth_dict = self.read_json(auth_file)

        self.city_dict = self.__settings_dict["city_dict"]
        self.city_filename = self.__settings_dict["city_file"]
        self.shelter_filename = self.__settings_dict["shelter_file"]
        self.shelter_count = self.__settings_dict["shelter_count"]
        self.pet_count = self.__settings_dict["pet_count"]

    def create_cities_file(self):
        """
        Queries various web APIs for city information and stores it in a file.
        """
        fixture_list = []
        pk = 1
        logging.debug("Creating city file '{}'...".format(self.city_filename))

        for city_name_urlized in self.city_dict:
            city_name = self.city_dict[city_name_urlized]
            logging.debug(" Processing '{}'...".format(city_name_urlized))
            query_dict = {  "city_urlized" : city_name_urlized,
                            "city_name" : city_name,
                            "city_state" : "BOGUS",
                            "city_country" : "US",
                            "city_vet_url" : self.yelp_query(city_name, "veterinarian", "url"),
                            "city_groomer_url" : self.yelp_query(city_name, "pet+groomer", "url"),
                            "city_park_url" : self.yelp_query(city_name, "dog+park", "url"),
                            "city_pic" : self.yelp_query(city_name, "city", "image_url"),
                            "city_park_pic" : self.yelp_query(city_name, "dog+park", "image_url"),
                            "city_vet_pic" : self.yelp_query(city_name, "veterinarian", "image_url"),
                            "city_groomer_pic" : self.yelp_query(city_name, "pet+groomer", "image_url"),
                            "city_url" : city_name_urlized,
                            "city_blurb" : self.yelp_query(city_name, "city", "snippet_text")
                         }
            fields = {}
            for query in query_dict:
                try:
                    fields[query] = query_dict[query]
                except:
                    # For now, it's fine to have empty strings for yelp queries that fail or come up empty. The database
                    # doesn't need to have meaningful values for -every- column in a row.
                    logging.info("Nonfatal error attempting to populate fields[{}] with '{}'...".format(query, query_dict[query]))
                    fields[query] = ""
            fixture_element = {"model" : "nsaid.City", "pk" : pk, "fields" : fields}
            fixture_list.append(fixture_element)
            pk += 1

        city_file = open(self.city_filename, "w")
        json.dump(fixture_list, city_file, indent = 4)
        city_file.close()
        logging.info("City file created.")
        
    def create_shelters_file(self):
        """
        Iterating over a city dict, find information on several shelters in each city. Print to file.
        """
        fixture_superlist = []
        pk = 1

        logging.debug("Creating shelters file '{}'...".format(self.shelter_filename))
        for city_urlized in self.city_dict:
            city = self.city_dict[city_urlized]
            logging.info("Processing '{}'...".format(city_urlized))
            petfinder_url = "http://api.petfinder.com/shelter.find"
            payload = {"key" : "2933122e170793b4d4b60358e67ecb65", "location" : city, "count" : self.shelter_count, "format" : "json"}
            r = requests.get(petfinder_url, params=payload)
            fixture_list = []
            #print(json.dumps(r.json(), indent = 4))
            for sh in r.json()["petfinder"]["shelters"]["shelter"]:
                #print(str(sh))
                try:
                    logging.info("       attempting to create shelter " + sh["id"]["$t"] + " " + sh["name"]["$t"])
                    shelter_fields = {"shelter_id" : "", "shelter_name" : "", "shelter_city_urlized" : "", "shelter_hours" : "", 
                                      "shelter_address" : "", "shelter_phone" : "", "shelter_email" : "", "shelter_city" : "",
                                      "shelter_state" : "", "shelter_lattitude" : "", "shelter_longitude" : "",
                                      "shelter_pic" : "", "shelter_url" : "", "shelter_blurb" : ""
                                     }
                    try:
                        shelter_fields["shelter_id"] = sh["id"]["$t"]
                    except:
                        logging.error("\nshelter_id\n")
                    try:
                        shelter_fields["shelter_name"] = sh["name"]["$t"]
                    except:
                        logging.error("\nshelter_name\n")
                    try:
                        shelter_fields["shelter_city_urlized"] = city_urlized
                    except:
                       logging.error("\nshelter_city_urlized\n")
                    try:
                        shelter_fields["shelter_hours"] = ""
                    except:
                        logging.error("\nshelter_hours\n")
                    try:
                        shelter_fields["shelter_address"] = sh["address1"]["$t"]
                    except:
                        logging.info("\nshelter_address\n")
                    try:
                        shelter_fields["shelter_phone"] = sh["phone"]["$t"]
                    except:
                        logging.error("\nshelter_phone\n")
                    try:
                        shelter_fields["shelter_email"] = sh["email"]["$t"]
                    except:
                        logging.info("\nshelter_email\n")
                    try:
                        shelter_fields["shelter_city"] = sh["city"]["$t"]
                    except:
                        logging.info("\nshelter_city\n")
                    try:
                        shelter_fields["shelter_state"] = sh["state"]["$t"]
                    except:
                        logging.info("\nshelter_state\n")
                    try:
                        shelter_fields["shelter_lattitude"] = sh["latitude"]["$t"]
                    except:
                        logging.info("\nshelter_lattitude\n")
                    try:
                        shelter_fields["shelter_longitude"] = sh["longitude"]["$t"]
                    except:
                        logging.info("\nshelter_longitude\n")
                    try:
                        shelter_fields["shelter_pic"] = self.yelp_query(city, sh["name"]["$t"], "image_url", self.__auth_dict)
                    except:
                        logging.info("\nshelter_pic\n")
                    try:
                        shelter_fields["shelter_external_url"] = google_query(sh["name"]["$t"])
                    except:
                        logging.info("\nshelter_url\n")
                    try:
                        shelter_fields["shelter_url"] = sh["id"]["$t"]
                    except:
                        logging.info("\nshelter_url\n")
                    try:
                        shelter_fields["shelter_blurb"] = self.yelp_query(city, sh["name"]["$t"], "snippet_text", self.__auth_dict)
                    except:
                        logging.info("\nshelter_blurb\n")
                 
                except Exception as e:
                    #pass
                    logging.info("\ncreating shelter " + sh["name"]["$t"] + "\n" + str(e) + "\n" + str(json.dumps(sh, indent = 4)))
                else:
                    fixture_element = {"model" : "nsaid.Shelter", "pk" : pk, "fields" : shelter_fields}
                    fixture_list.append(fixture_element)
                    pk += 1
            fixture_superlist += fixture_list
        shelter_file = open("../../nsaid/fixtures/shelters_fixture_2.json", "w")
        json.dump(fixture_superlist, shelter_file, indent = 4)
        shelter_file.close()
        logging.info("Shelter file created.")

    def create_pets_file(self):
        """
        given a shelter (json object)
        query for all pets associated with a shelter
        return a list of pets (json objects)
        costs one request per shelter (4) in EACH city
        """
        fixture_superlist = []
        pk = 1

        logging.debug("count is " + str(self.pet_count))
        shelters_file = json.loads(open("../../nsaid/fixtures/shelters_fixture_2.json").read())
        master_pets = []
        for shelter in shelters_file:
            #pets = pet_validate(city.city_name, city.city_state, "pet_city", "pet_state", pets_per_shelter(shelter))
            #print(shelter["fields"]["shelter_id"] + " " + shelter["fields"]["shelter_city"])
            petfinder_url = "http://api.petfinder.com/shelter.getPets"
            payload = {"key" : "2933122e170793b4d4b60358e67ecb65", "id" : shelter["fields"]["shelter_id"], "count" : self.pet_count, "format" : "json"}
            logging.info("\ncreating pets for shelter " + shelter["fields"]["shelter_id"])
            r = requests.get(petfinder_url, params = payload)
            fixture_list = []
            #print("*** " + json.dumps(r.json()["petfinder"]["pets"], indent = 4))
            try:
                pet_list = r.json()["petfinder"]["pets"]["pet"]
                #print("pet_list " + json.dumps(pet_list, indent = 4))
                logging.debug("type of pet list is " + str(type(pet_list)) + " and len of pet_list is " + str(len(pet_list)))
                assert type(pet_list) == list
                assert len(pet_list) > 1
                for p in pet_list:
                    logging.debug("\n   about to create a pet: " + p["name"]["$t"] + " from shelter " + p["shelterId"]["$t"] + " " + shelter["fields"]["shelter_name"])
                    try:
                        thumb = ""
                        big = ""
                        pet_pic_list = []
                        photo_list = p["media"]["photos"]["photo"]
                        for photo in photo_list:
                            if photo["@id"] == "1":
                                if photo["@size"] == "pnt":
                                    thumb = photo["$t"]
                                elif photo["@size"] == "x":
                                    big = photo["$t"]
                            if photo["@size"] == "x" and photo["@id"] in ["1","2","3"]:
                                pet_pic_list.append(photo["$t"])
                        #print("thumb = " + thumb + " big = " + big + "\n" + str(json.dumps(p, indent = 4)))
                        pet_fields = {}
                        try:
                            pet_fields["pet_id"] = p["id"]["$t"]
                        except:
                            logging.error("pet_id")
                        try:
                            pet_fields["pet_name"] = p["name"]["$t"]
                        except:
                            logging.debug("pet_name")
                        try:
                            pet_fields["pet_age"] = p["age"]["$t"]
                        except:
                            logging.debug("pet_age")
                        try:
                            pet_fields["pet_sex"] = p["sex"]["$t"]
                        except:
                            logging.debug("pet_sex")
                        try:
                            pet_fields["pet_size"] = p["size"]["$t"]
                        except:
                            logging.debug("pet_size")
                        try:
                            pet_fields["pet_breed"] = p["breeds"]["breed"]["$t"]
                        except:
                            logging.debug("pet_breed")
                        try:
                            pet_fields["pet_shelter"] = p["shelterId"]["$t"]
                        except:
                            logging.debug("pet_shelter")
                        try:
                            pet_fields["pet_city"] = shelter["fields"]["shelter_city"]
                        except:
                            logging.debug("pet_city")
                        try:
                            pet_fields["pet_city_urlized"] = shelter["fields"]["shelter_city_urlized"]
                        except:
                            logging.debug("pet_city_urlized")
                        try:
                            pet_fields["pet_state"] = shelter["fields"]["shelter_state"]
                        except:
                            logging.debug("pet_state")
                        try:
                            pet_fields["pet_pic_url"] = thumb
                        except:
                            logging.debug("pet_pic_url")
                        try:
                            pet_fields["pet_pic_large"] = big
                        except:
                            logging.debug("pet_pic_large")
                        try:
                            pet_fields["pet_pic_list"] = pet_pic_list
                        except:
                            logging.debug("pet_pic_list")
                        try:
                            pet_fields["pet_url"] = "id" + p["id"]["$t"]
                        except:
                            logging.debug("pet_url")
                        try:
                            pet_fields["pet_shelter_url"] = p["shelterId"]["$t"]
                        except:
                            logging.debug("pet_shelter_url")
                        try:
                            pet_fields["pet_city_url"] = shelter["fields"]["shelter_city_urlized"]
                        except:
                            logging.debug("pet_city_url")
                        try:
                            pet_fields["pet_shelter_name"] = shelter["fields"]["shelter_name"]
                        except:
                            logging.debug("pet_shelter_name")
                        try:
                            pet_fields["pet_bio"] = petfinder_query(p["id"]["$t"], "description")
                        except:
                            logging.debug("pet_bio")
                    except Exception as e:
                        #pass
                        logging.debug("   problem creating pet " + p["id"]["$t"] + " no photos")
                    else:
                        fixture_element = {"model" : "nsaid.Pet", "pk" : pk, "fields" : pet_fields}
                        fixture_list.append(fixture_element)
                        pk += 1
                    #break
            except Exception as e:
                #pass
                logging.debug("*** Exception creating pets from shelter " + shelter["fields"]["shelter_id"]  + " " + shelter["fields"]["shelter_name"]);
                #print(json.dumps(r.json()["petfinder"]["pets"]["pet"], indent = 4))
            fixture_superlist += fixture_list
            #break
        pet_file = open("../../nsaid/fixtures/pets_fixture_2.json", "w")
        json.dump(fixture_superlist, pet_file, indent = 4)    
        #rint(json.dumps(fixture_superlist, indent = 4))
        #return fixture_superlist

    def yelp_query(self, city, term, field_name):
        """
        Make a query to the yelp API.
        """
        consumer_key    = self.__auth_dict["yelp"]["consumer_key"]
        consumer_secret = self.__auth_dict["yelp"]["consumer_secret"]
        token           = self.__auth_dict["yelp"]["token"]
        token_secret    = self.__auth_dict["yelp"]["token_secret"]
        session = rauth.OAuth1Session(consumer_key = consumer_key, consumer_secret = consumer_secret, access_token = token, access_token_secret = token_secret)
        yelp_params = {}
        yelp_params["location"] = city 
        yelp_params["term"] = term
        yelp_params["limit"] = 1

        yelp_response = session.get("http://api.yelp.com/v2/search", params = yelp_params)
        d = yelp_response.json()
        result = str(d["businesses"][0][field_name])
        if sys.flags.debug:
            #print(json.dumps(d, indent = 4))
            logging.debug("yelp_query: " + field_name + " " + result)
        #session.close()
        return result

    def google_query(term):
        """
        Make a query to the google web search ajax API.
        """
        url = 'http://ajax.googleapis.com/ajax/services/search/web'
        payload = {"v" : 1.0, "q" : term}
        r = requests.get(url, params = payload)
        result = str(r.json()["responseData"]["results"][0]["visibleUrl"])
        #logging.debug(json.dumps(r.json(), indent = 4))
        #logging.debug("google " + r.json()["responseData"]["results"][0]["visibleUrl"])
        logging.debug("google_query: " + term + " " + result)
        return result 

    def petfinder_query(identifier, attribute):
        """
        Make a query to the petfinder API.
        To run a manual/test query against the petfinder API in a browser, try a URL something like this:
          http://api.petfinder.com/shelter.find?key=2933122e170793b4d4b60358e67ecb65&location=78723&format=json
        Full petfinder API docs here:
          https://www.petfinder.com/developers/api-docs
        """
        petfinder_url = "http://api.petfinder.com/pet.get"
        payload = {"key" : "2933122e170793b4d4b60358e67ecb65", "id" : identifier, "format" : "json"}
        r = requests.get(petfinder_url, params = payload)
        result = r.json()["petfinder"]["pet"][attribute]["$t"]
        sanitized_result = result.replace('\u00e2\u0080\u0099', "'").replace('\u00e2\u0080\u00a6', '').replace('\u00c2\u00bd', '').replace('\n','')
        return sanitized_result

    def read_json(self, filename):
        """
        Open a json file, parse it, and return it as a dict object.
        """
        with open(filename) as f:
            data = json.loads(f.read())
        logging.info("read from file {0}".format(filename))
        logging.debug(data)
        return data
        
if __name__ == "__main__":

    # DEBUG, INFO, WARNING, ERROR, CRITICAL
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("--auth", help="json config file, specifically containing developer keys", required=True)
    parser.add_argument("--settings", help="json settings file", required=True)

    parser.add_argument("--skipcity", help="skip city file creation and instead read from city_file", action="store_true")
    parser.add_argument("--skipshelter", help="skip city file creation and instead read from shelter_file", action="store_true")
    parser.add_argument("--skippet", help="skip city file creation and instead read from pet_file", action="store_true")

    args = parser.parse_args()

    dc = DatasetCreator(args.settings, args.auth)

    if not args.skipcity:
        dc.create_cities_file()
    if not args.skipshelter:
        dc.create_shelters_file()
    if not args.skippet:
        dc.create_pets_file()
