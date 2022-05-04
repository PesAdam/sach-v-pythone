# Šach v pythone
## _môj projekt na programovanie do školy_

Tento projekt som si vybral najmä preto aby som sa dostal bližšie k OOP v Pythone. Nebolo to také jednoduché to všetko dať do pohybu, ale zato som sa naučil veľa nových vecí v Pythone o ktorých som nevedel.

## Prečo práve šach?
- Chcel som aby tento projekt bol pre mňa výzva
- Tento projekt obsahuje veľa algoritmov a práve na tomto projekte som si ich vyskúšal v praxi
- ✨oop  ✨

Môj program funguje na 2 súboroch. Jeden je Main ktorý ma nastarosť vykreslovanie a UI pre uživateľa. V tomto programe sa kreslí board, figurky a tiež obsahuje funkciu na vykreslovanie možných krokov a zvolenej figurky. Druhý súbor je o niečo zaujimavejší. Tento súbor má nazov Engine a deje sa v ňom všetko potrebné pre fungovanie hry ako takej. Má 2 triedy. Jedna trieda má nastarosť stav hry ako takej a druhá trieda má nastarosť pohyb ako taký. Princíp pozadia hry je pomocou 2rozmerného poľa v ktorom mám uložené kde je aká figurka. V engine týmto polom manipulujem a už spomínanom Main súbore sa mi tieto zmeny vykresluju na plochu. Pohyb figuriek je riešeny nasledovne. V classe Move mam tkz. mapu klúčov pre lepšie orientovanie po ploche. Každá figurka má svoju funkciu v ktorej má určené smery kam môže ísť. Následne si urči enemy a pre každy smer v smeroch ktoré mam sa spusti for cyklus ktorý zistí posledný riadok a stĺpec na ploche. Následne mam urobenú ochranu ifom aby mi nahodou figurka nevyletela tam kam nemá a potom už ide iba if či je políčko prazdne alebo či je tam enemy (nebudem predsa vyhadzovať svojich). A potom čo sa toto stane zavolam classu Move pomocou ktorej prilepím do listu pohybov tento pohyb. Tak asi takto nejak v skratke :).




## Installation

Tento šach potrebuje pygame.

Inštalácia dependencies.

```sh
cd šach
pip3 install pygame
python3 ChessMain.py
```



## License

MIT

**Free Software, Hell Yeah!**
https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_
