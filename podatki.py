#uvoz_podatkov

import csv
import json
import os
import re
import sys
import requests


#URL glavne strani 
fp_url = 'http://www.dogbreedslist.info/all-dog-breeds/'
# mapa
dog_directory = 'dog_data'
# ime datoteke v katero bomo shranili glavno stran
fp_filename = 'fp.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'dog_data.csv'



def download_url_to_string(url):
    '''This function takes a URL as argument and tries to download it
    using requests. Upon success, it returns the page contents as string.'''
    try:
        # del kode, ki morda sproži napako
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        # koda, ki se izvede pri napaki
        print("Could not access page" + url)
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        return ""
        #ne vrnemo nic, izprintamo da ni slo 
    # nadaljujemo s kodo če ni prišlo do napake
    return r.text

fp_text = download_url_to_string(fp_url)

def save_string_to_file(text, directory, filename):
    '''Write "text" to the file "filename" located in directory "directory",
    creating "directory" if necessary. If "directory" is the empty string, use
    the current directory.'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None


def save_frontpage(url, ime_datoteke):
    r = requests.get(url)
    with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')
'''Save "cats_frontpage_url" to the file
"cat_directory"/"frontpage_filename"'''


def read_file_to_string(directory, filename):
    print(filename)
    with open(filename, encoding='utf-8') as datoteka:
         return datoteka.read()
'''Return the contents of the file "directory"/"filename" as a string.'''


def razlicne_pasme(directory, filename):
    '''Split "page" to a list of advertisement blocks.'''
    datoteka = read_file_to_string(directory, filename)
    seznam_psov = []
    pes = r'<div class="list-01">' + r'.*?' + r'<span>Rank</span></div>'
    for ujemanje in re.finditer(pes, datoteka, re.DOTALL):
        nas_pes = ujemanje.group(0)
        seznam_psov.append(nas_pes)
    return seznam_psov



def get_dict_from_ad_block(directory, filename):
    '''Build a dictionary containing the name, description and price
    of an ad block.'''
    vzorec = re.compile(
    r'<div class="list">'
    r'.*?'
    r'alt="(?P<ime>)"/></a></div><div'
    r'.*?'
    r'<div class="list-03"><p>(?P<lasnosti>)</p><p>(?P<lastnosti>)' #A lahko tako naredimo?
    r'<div class="pop"><p>(?P<popularnost>)</p><span>Popularity</span></div><div'
    r'.*?'
    r'<b>Origin:</b> (?P <drzava>)</p><span><a'
    r'.*?'
    r'</span</div>',
    re.DOTALL)
    seznam_psov = razlicne_pasme(directory, filename)
    podatki_psov = []
    for pes in seznam_psov:
        for ujemanje in vzorec.finditer(pes):
            podatki_psa = ujemanje.groupdict()
            podatki_psov.append(podatki_psa)
    return podatki_psov



def pasme_file(filename, directory):
    '''Parse the ads in filename/directory into a dictionary list.'''
    vsebina = read_file_to_string(directory, filename)
    oglasi = razlicne_pasme(directory, filename)
    seznam_slovarjev = get_dict_from_ad_block(directory, filename)
    return seznam_slovarjev


def write_cat_ads_to_csv(seznam_slovarjev):
    write_csv(['ime', 'popularnost', 'drzava'], seznam_slovarjev, dog_directory, csv_filename)
    return None


def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)





##def pripravi_imenik(ime_datoteke):
##    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
##    imenik = os.path.dirname(ime_datoteke)
##    if imenik:
##        os.makedirs(imenik, exist_ok=True)
##
##
##def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
##    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
##    try:
##        print('Shranjujem {} ...'.format(url), end='')
##        sys.stdout.flush()
##        if os.path.isfile(ime_datoteke) and not vsili_prenos:
##            print('shranjeno že od prej!')
##            return
##        r = requests.get(url)
##    except requests.exceptions.ConnectionError:
##        print('stran ne obstaja!')
##    else:
##        pripravi_imenik(ime_datoteke)
##        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
##            datoteka.write(r.text)
##            print('shranjeno!')
##
##
##def vsebina_datoteke(ime_datoteke):
##    '''Vrne niz z vsebino datoteke z danim imenom.'''
##    with open(ime_datoteke, encoding='utf-8') as datoteka:
##        return datoteka.read()
##
##
##def zapisi_csv(slovarji, imena_polj, ime_datoteke):
##    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
##    pripravi_imenik(ime_datoteke)
##    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
##        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
##        writer.writeheader()
##        for slovar in slovarji:
##            writer.writerow(slovar)
##
##
##def zapisi_json(objekt, ime_datoteke):
##    '''Iz danega objekta ustvari JSON datoteko.'''
##    pripravi_imenik(ime_datoteke)
##    with open(ime_datoteke, 'w', encoding='utf-8') as json_datoteka:
##        json.dump(objekt, json_datoteka, indent=4, ensure_ascii=False)
##
##
##
###sestavim vzorec
##    
##vzorec = re.compile(
##    r'<div class="list">'
##    r'.*?'
##    r'alt="(?P<ime>)"/></a></div><div'
##    r'.*?'
##    r'<div class="pop"><p>(?P<popularnost>)</p><span>Popularity</span></div><div'
##    r'.*?'
##    r'<b>Origin:</b> (?P <drzava>)</p><span><a'
##    r'.*?'
##    r'</span</div>',
##    re.DOTALL)
##
##
##def izloci_podatke_psa(ujemanje_psa):
##    podatki_psa = ujemanje_psa.groupdict()
##    podatki_psa['ime'] = podatki_psa['ime']
##    podatki_psa['popularnost'] = podatki_psa['popularnost']
##    podatki_psa['drzava'] = podatki_psa['drzava']    
##    return podatki_psa
##
##
### shranim vse strani dne 27.10.2018 (od 1 do 19, vse skupaj 369 zadetkov)
##for i in range(1, 20):
##    url = (
##        'http://www.dogbreedslist.info/Popular-Puppy-Names.html#.W9Qpj5MzbMU'
##    ).format(i)
##    shrani_spletno_stran(url, 'zajete_strani/pasme_psov_{}.html'.format(i))
##
##
##
##
##podatki_psov = []
##for i in range(1, 20):
##    vsebina = vsebina_datoteke(
##        'zajete-strani/pasme_psov{}.html'.format(i))
##    for ujemanje_psa in vzorec.finditer(vsebina):
##        podatki_psov.append(izloci_podatke_psa(ujemanje_psa))
##zapisi_json(podatki_psov, 'obdelani-podatki/vsi-psi.json')
##zapisi_csv(podatki_psov, ['ime', 'popularnost', 'drzava'], 'obdelani-podatki/vsi-psi.csv')

