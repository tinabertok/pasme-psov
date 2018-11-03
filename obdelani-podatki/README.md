# Obdelava podatkov


S spletne strani sem najprej uvozila podatke o vseh pasmah psov(19 strani). Nato sem ugotovila, da moram, če hočem pridobiti vse podatke o določeni pasmi, klikniti na link, zato sem uvozila še vse linke pasem, in jih shranila v datoteko **vsi_psi**.
Nato sem se lotila zajema podatkov, v katerem sem ustvarila dodatno datoteko **vse_pasme**, v katero sem shranila podatke o vseh pasmah psov in njihovih značilnostih. 
Za kasnejšo analizo pa bo potrebno imeti podatke v pravi obliki, zato sem ustvarila še eno datoteko **znacaji**, v kateri so zajeti vsi značaji pasem. 

Datoteka **vse_pasme** vsebuje:
• ime pasme
• državo porekla: od kod pasma izvira
• življensko dobo: kakšna je povprečna življenska doba te pasme
• višino: višina v centimetrih in inčih
• velikost: velikost pasme (Small, Medium, Large, Giant)
• popularnost: na katerem mestu po priljubljenosti je bila pasma v letu 2017
• ceno: kakšna je povprečna cena mladička
• značaj: glavne značajske lastnosti pasme

Datoteka **vsi_psi** vsebuje le linke do posamezne pasme psa.

Datoteka **znacaji** pa vsebuje:
• ime pasme
• značaj pasme
Ker je značajskih lastnosti za eno pasmo več, se ime pasme v stolpcu ponovi večkrat. 
Prav tako ima več psov isto značajsko lastnost, zato se te ponavljajo v drugem stolpcu. 
