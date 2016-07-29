from pgoapi import pgoapi
from Tkinter import *
import sys
from PIL import Image, ImageTk
from getpass import getpass
def log(string):
    print "[PokeHelper] " + string
pokemonTable = []
root = Tk()
root.withdraw()
pokeName = StringVar(root)
pokeCP = StringVar(root)
pokeHeight = StringVar(root)
pokeWeight = StringVar(root)
image = Image.open("icons/pikachu.png")
image = image.resize((80,80), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
pokeImageLbl = Label(root, image=photo)
def quit():
    root.destroy()
def onPokeSelect(event):
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    pokeName.set(str(value))
    pokeCP.set(pokemonTable[index][1])
    pokeHeight.set(pokemonTable[index][2])
    pokeWeight.set(pokemonTable[index][3])
    image = Image.open("icons/" + str(value).lower() + ".png")
    image = image.resize((80,80), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    pokeImageLbl.configure(image = photo)
    pokeImageLbl.image = photo
    root.update_idletasks()
pokemon_list = ["Bulbasaur","Ivysaur","Venusaur","Charmander","Charmeleon","Charizard","Squirtle","Wartortle","Blastoise","Caterpie","Metapod","Butterfree","Weedle","Kakuna","Beedrill","Pidgey","Pidgeotto","Pidgeot","Rattata","Raticate","Spearow","Fearow","Ekans","Arbok","Pikachu","Raichu","Sandshrew","Sandslash","NidoranF","Nidorina","Nidoqueen","NidoranM","Nidorino","Nidoking","Clefairy","Clefable","Vulpix","Ninetales","Jigglypuff","Wigglytuff","Zubat","Golbat","Oddish","Gloom","Vileplume","Paras","Parasect","Venonat","Venomoth","Diglett","Dugtrio","Meowth","Persian","Psyduck","Golduck","Mankey","Primeape","Growlithe","Arcanine","Poliwag","Poliwhirl","Poliwrath","Abra","Kadabra","Alakazam","Machop","Machoke","Machamp","Bellsprout","Weepinbell","Victreebel","Tentacool","Tentacruel","Geodude","Graveler","Golem","Ponyta","Rapidash","Slowpoke","Slowbro","Magnemite","Magneton","Farfetch'd","Doduo","Dodrio","Seel","Dewgong","Grimer","Muk","Shellder","Cloyster","Gastly","Haunter","Gengar","Onix","Drowzee","Hypno","Krabby","Kingler","Voltorb","Electrode","Exeggcute","Exeggutor","Cubone","Marowak","Hitmonlee","Hitmonchan","Lickitung","Koffing","Weezing","Rhyhorn","Rhydon","Chansey","Tangela","Kangaskhan","Horsea","Seadra","Goldeen","Seaking","Staryu","Starmie","Mr. Mime","Scyther","Jynx","Electabuzz","Magmar","Pinsir","Tauros","Magikarp","Gyarados","Lapras","Ditto","Eevee","Vaporeon","Jolteon","Flareon","Porygon","Omanyte","Omastar","Kabuto","Kabutops","Aerodactyl","Snorlax","Articuno","Zapdos","Moltres","Dratini","Dragonair","Dragonite","Mewtwo","Mew"]
log("Authorising account with Pokemon GO servers..")
pokeapi = pgoapi.PGoApi()
login_name = str(raw_input("Username: "))
password = getpass()
service = str(raw_input("Auth Type (google or ptc): "))
if not pokeapi.login(service, login_name, password):
    log("Could not login.")
    sys.exit(0)
log("Authorised.")
log("Getting Inventory...")
pokeapi.get_inventory()
response = pokeapi.call()
items = response['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']
for item in items:
    if 'pokemon_data' in item['inventory_item_data']:
         if 'is_egg' not in item['inventory_item_data']['pokemon_data']:
            pokedata = item['inventory_item_data']['pokemon_data']
            cp = str(pokedata.get('cp', 0))
            weight = float(pokedata.get('weight_kg', 0))
            height = float(pokedata.get('height_m', 0))
            species = pokemon_list[int(pokedata.get('pokemon_id', 0))-1]
            pokemonTable.append((species, int(cp), height, weight))
pokemons = sorted(pokemonTable, key=lambda pokemon: pokemon[1], reverse=True)
pokemonTable = []
pokemonLongestName = 0
for poke in pokemons:
    if(len(poke[0]) > pokemonLongestName):
        pokemonLongestName = len(poke[0])
    pokemonTable.append((poke[0], str(poke[1]) + " CP", str(round(poke[2],2)) + "m", str(round(poke[3],2)) + "kg"))
log("Inventory Got.")
log("Initialising GUI.")
root.wm_title("PokeHelper")
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(800, 600))
root.configure(background="gray9")
listbox = Listbox(root)
listbox.pack(fill=X, padx=20, pady=50)
listbox.bind('<<ListboxSelect>>', onPokeSelect)
listbox.select_set(0)
pokeNameLbl = Label(root, textvariable=pokeName, fg="white", bg="gray9", font=("Helvetica", 24))
pokeNameLbl.pack()
pokeName.set("Pokemon Name")
pokeCPLbl = Label(root, textvariable=pokeCP, fg="white", bg="gray9", font=("Helvetica", 18))
pokeCPLbl.pack()
pokeCP.set("Pokemon CP")
pokeWeightLbl = Label(root, textvariable=pokeWeight, fg="white", bg="gray9", font=("Helvetica", 12))
pokeWeightLbl.pack()
pokeWeight.set("Pokemon Weight")
pokeHeightLbl = Label(root, textvariable=pokeHeight, fg="white", bg="gray9", font=("Helvetica", 12))
pokeHeightLbl.pack()
pokeHeight.set("Pokemon Height")
pokeImageLbl.pack()
menubar = Menu(root)
menubar.add_command(label="Quit!", command=quit)
root.config(menu=menubar)
for poke in pokemonTable:
    listbox.insert(END, poke[0])
log("GUI Initialised.")
root.deiconify()
root.mainloop()
