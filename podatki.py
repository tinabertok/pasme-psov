#uvoz_podatkov

import csv
import json
import os
import re
import sys
import requests


#URL glavne strani 
fp_url = 'http://www.dogbreedslist.info/Popular-Puppy-Names.html#.W9Qpj5MzbMU'
# mapa
dog_directory = 'dog_data'
# ime datoteke v katero bomo shranili glavno stran
fp_filename = 'fp.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'dog_data.csv'


def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)


def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print('Shranjujem {} ...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')


def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return datoteka.read()


def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)


def zapisi_json(objekt, ime_datoteke):
    '''Iz danega objekta ustvari JSON datoteko.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as json_datoteka:
        json.dump(objekt, json_datoteka, indent=4, ensure_ascii=False)


# shranim vse strani dne 27.10.2018 (od 1 do 19, vse skupaj 369 zadetkov)
for i in range(1, 20):
    url = (
        'http://www.dogbreedslist.info/Popular-Puppy-Names.html#.W9Qpj5MzbMU'
    ).format(i)
    shrani_spletno_stran(url, 'zajete_strani/pasme_psov_{}.html'.format(i))

