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


#pridobivanje linkov posamezne pasme       

vzorec = re.compile(
    r'<div class="list-01"><div class="left"><a href="(?P<link>.*?)">.*?',
    re.DOTALL)


def izloci_podatke_linkov(ujemanje_linka):
    podatki_linka = ujemanje_linka.groupdict()
    podatki_linka['link'] = podatki_linka['link'].strip()    
    return podatki_linka




# shranim vse strani dne 27.10.2018 (od 1 do 19, vse skupaj 369 zadetkov)
##for i in range(1, 20):
##    url = (
##        'http://www.dogbreedslist.info/all-dog-breeds/list_1_{}.html'
##    ).format(i)
##    shrani_spletno_stran(url, 'zajete_strani/pasme_psov_{}.html'.format(i))




podatki_linkov = []
for i in range(1, 20):
    vsebina = vsebina_datoteke(
        'zajete_strani/pasme_psov_{}.html'.format(i))
    for ujemanje_linka in vzorec.finditer(vsebina):
        podatki_linkov.append(izloci_podatke_linkov(ujemanje_linka))
zapisi_json(podatki_linkov, 'obdelani-podatki/vsi_psi.json')
zapisi_csv(podatki_linkov, ['link'], 'obdelani-podatki/vsi_psi.csv')

#vsi vzorci

vzorec_ime = re.compile(
    r'<td class="left">Name</td>.*?<td>(?P<ime>.*?)<.*?',
    re.DOTALL)

	
vzorec_drzava = re.compile(
    r'<td class="left">Origin</td>.*?"flag">(<.*?>)?(?P<drzava>.*?)<.*?',
    re.DOTALL)


vzorec_doba = re.compile(
    r'<td class="left">Life span</td>.*?<td>(?P<zivljenska_doba>.*?)<',
    re.DOTALL)


vzorec_velikost = re.compile(
    r'<td class="left">Size</td>.*?/">(?P<velikost>.*?)<.*?',
    re.DOTALL)

vzorec_visina = re.compile(
    r'<td class="left">Height</td>.*?(<td>|<td>Male:)(?P<visina>.*?)(inches.*?)',
    re.DOTALL)


vzorec_popularnost = re.compile(
    r'<td class="left">Popularity(.*?)?</td>.*?<td>2017: (?P<popularnost>.*?)<.*?',
    re.DOTALL)


vzorec_cena = re.compile(
    r'<td class="left">Puppy Price</td>.*?<td>Average (?P<cena>.*?) USD</td>.*?',
    re.DOTALL)



vzorec_znacaj = re.compile(
    r'<td class="left">Temperament</td>.*?<td>(?P<znacaj>.*?)</td>',
    flags=re.DOTALL)

vzorec_lastnost = re.compile(
    r'(?P<lastnost>.*?)(<span>|</span>)',
    flags=re.DOTALL)
    



def izloci_podatke_psov(vsebina):
    podatki_psa = dict()
    podatki_psa['ime'] = vzorec_ime.search(vsebina).group('ime').replace("&rsquo;", "\'")
    podatki_psa['drzava'] = vzorec_drzava.search(vsebina).group('drzava').strip()
    drzava = vzorec_drzava.search(vsebina)
    if drzava['drzava'] == '&nbsp;':
        podatki_psa['drzava'] = '/'
    else:
        podatki_psa['drzava'] = drzava['drzava'].strip(' ')
    podatki_psa['zivljenska_doba'] = vzorec_doba.search(vsebina).group('zivljenska_doba').split('-')[0]
    
    visina = vzorec_visina.search(vsebina)
    if visina:
        podatki_psa['visina'] = visina['visina'].replace('Male: ', '').replace('Female: ','').replace('Standard: ','').replace('&frac12;', '').strip('Small: ').replace('&ndash;', '-').strip('~').strip('Up to ').replace('and under', '').strip('Males: ').replace('Toy:', '').split('-')[0]
    else :
        podatki_psa['visina'] = '/'
    podatki_psa['velikost'] = vzorec_velikost.search(vsebina).group('velikost')
    popularnost = vzorec_popularnost.search(vsebina)
    if popularnost:
        podatki_psa['popularnost'] = popularnost['popularnost'].strip('#')
    else:
        podatki_psa['popularnost'] = '/'
    cena = vzorec_cena.search(vsebina)
    if cena:
        podatki_psa['cena'] = int(cena['cena'].split('-')[1].replace('$', ''))

    else:
        podatki_psa['cena'] = '/'

    seznam_znacajev = []
    znacaji = vzorec_znacaj.search(vsebina).group('znacaj')
    for ujemanje in vzorec_lastnost.finditer(znacaji):
        seznam_znacajev.append(ujemanje.group('lastnost'))
    
    podatki_psa['znacaj'] = seznam_znacajev

   

    return podatki_psa


#print(type(podatki_psa['cena']))

    
#izločeni podatki za posebne tabele 
def izloci_gnezdene_podatke(seznam):
    znacaji = []

    for podatki_psa in seznam_slovarjev:
        for znacaj in podatki_psa.pop('znacaj'):
            znacaji.append({'ime': podatki_psa['ime'], 'znacaj': znacaj})
   
    znacaji.sort(key=lambda znacaj: (podatki_psa['ime'], znacaj['znacaj']))

    return znacaji




#seznam slovarjev vseh psov

seznam_slovarjev = []
for i in range(1, 370):
    datoteka = 'zajete_strani_pasem/pasma_psa_{}.html'.format(i)
    vsebina = vsebina_datoteke(datoteka)
    slovar_psa = izloci_podatke_psov(vsebina)
    seznam_slovarjev.append(slovar_psa)


#za enega psa popravimo na roke
seznam_slovarjev[183]['visina'] = '/'
seznam_slovarjev[233]['ime'] = 'Catilde da Serra de Aires'
seznam_slovarjev[275]['ime'] = 'Jaumlmthund'

#locimo znacaje od ostalih podatkov
znacaji = izloci_gnezdene_podatke(seznam_slovarjev)

#zapisemo podatke
zapisi_json(seznam_slovarjev, 'obdelani-podatki/vse_pasme.json')
zapisi_csv(seznam_slovarjev, ['ime', 'drzava', 'zivljenska_doba', 'visina', 'velikost', 'popularnost', 'cena'], 'obdelani-podatki/vse_pasme.csv') 


zapisi_json(znacaji, 'obdelani-podatki/znacaji_psov.json')
zapisi_csv(znacaji, ['ime', 'znacaj'], 'obdelani-podatki/znacaji_psov.csv')
