import os
import json

def main():
    directories = os.listdir()
    write_file = open("works.txt", "a")
    without_abstract = 0
    without_location = 0
    total = 0
    for dir in directories:
        if 'updated_date' in dir:
            print(dir)
            subdir = os.listdir(dir)
            for sd in subdir:
                if '.gz' not in sd:
                    print(sd)
                    f = open(f'{dir}/{sd}', "r")
                    lines = f.readlines()
                    for content in lines:
                        j = json.loads(content)
                        print(j)
                        total += 1
                        if j['abstract_inverted_index'] is not None and j['primary_location'] is not None and j['primary_location']['source'] is not None:
                            new_json = {}
                            new_json['id'] = j['id']
                            new_json['abstract_inverted_index'] = j['abstract_inverted_index']
                            new_json['primary_location'] = j['primary_location']['source']['id']
                            new_json['']
                            write_file.write(str(new_json))
                        elif j['abstract_inverted_index'] is None:
                            without_abstract += 1
                        elif j['primary_location'] is None or j['primary_location']['source'] is None:
                            without_location += 1
                    f.close()
    write_file.close()
    print(f'Total: {total} - Without Abstract: {without_abstract} - Without Location: {without_location}')

if __name__ == "__main__":
    main()