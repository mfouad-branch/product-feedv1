# python 3.5
from urllib import parse
import csv
import json
import os
import errno
import sys

LINK_COL_NAME_TO_REPLACE='link'


class Settings:
    """An object to hold all the data in the settings

    Stores all the data form the settings.json file so it can be accessed globally.

    input_file (str): the filename we want to parse
    output_file (str): the file name we want to write to
    csv_deliminator (str): the delimainator of the values in the input_file
    base_url (str): the base url to append all data to
    templates (List (str)): a list of all the templates
    template_data (dict (dict)): a dictionary with the file name w/o extension as a key and the values are the ones of the file
    eg. {"google_cross_platoform":{ "$3p": "a_google_adwords", ...}}
    active_template: (str) the current template name we will be appending to links
    output_url_list: (List (str)) a list of urls as str to print out
    """

    def __init__(self, input_file=None, output_file=None, csv_deliminator=None, base_url=None, templates=[], templates_folder=None):
        self.input_file = input_file
        self.output_file = output_file
        self.csv_deliminator = csv_deliminator
        self.base_url = base_url
        self.campaign = ''
        self.templates_folder = templates_folder
        self.templates = templates
        self.template_data = {}
        self.active_template = ''
        self.output_url_list = []

    def get_templates(self):
        for x in os.listdir(self.templates_folder):
            self.templates.append(os.path.join(self.templates_folder, x))

        for filename in self.templates:
            with open(filename) as file:
                data = json.load(file)
                self.template_data[os.path.basename(filename).split('.')[0]] = data


settings = Settings()


def merge_dictionaries(row_data, default):
    """Merge d2 into d1, where d1 has priority

    for all values of d2 merge them into d1. If a value exists in d1 and in d2 keep the value from d1

    :param d1: dictionary of values
    :param d2: dictionary of values
    :return: dictionary of unified values
    """
    if default is None:
        return row_data
    if row_data is None:
        return default

    return {**default, **row_data} # this is python 3.5 only



def import_settings():
    # required attributes, fail if missing
    settings.input_file =  sys.argv[2]
    settings.output_file =  sys.argv[3]
    settings.csv_deliminator =  sys.argv[5]
    settings.base_url =  sys.argv[1]
    settings.templates_folder = os.path.join(os.path.dirname(sys.argv[0]),  "templates")
    settings.active_template = sys.argv[4]

    settings.get_templates()

def row_count(settings):
    with open(settings.input_file) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=settings.csv_deliminator)
        return sum(1 for row in csv_reader)


def parse_csv(settings,row_count):
    with open(settings.input_file) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=settings.csv_deliminator)
        write_csv(settings, {str(x): str(x) for x in csv_reader.fieldnames}, 'w') # write header
        current_row = 1
        for row in csv_reader:
            # apply template data to the url
            template_data = settings.template_data.get(settings.active_template, None)

            template_data['$original_url'] = row[LINK_COL_NAME_TO_REPLACE] # keep the original url
            template_data['$fallback_url'] = row[LINK_COL_NAME_TO_REPLACE] # keep original url as fallback

            url = settings.base_url + parse.urlencode(template_data, safe='{}:') # safe characters do not get encoded


            row[LINK_COL_NAME_TO_REPLACE] = url
            write_csv(settings, row.values(), 'a') # write rows to output
            print("Converted %d out of %d" % (current_row,row_count))
            current_row +=1 


def write_csv(settings, row, mode):
    with open(settings.output_file, mode=mode) as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(row)


if __name__ == '__main__':
    import_settings()
    row_count = row_count(settings)
    print("Converting %d entries" % row_count)
    parse_csv(settings,row_count)
    # write_csv(settings)