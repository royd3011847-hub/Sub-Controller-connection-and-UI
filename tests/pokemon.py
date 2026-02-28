import requests

base_url = "https://pokeapi.co/api/v2/"



def get_pokemon_data(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)
    print(response)
    
    #200 means response is ok
    if response.status_code == 200:
        data = response.json()
        print(f"data: {data}")
        pokemon_info = {
            "name": data["name"],
            "id": data["id"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"]],
        }
        print(pokemon_info)
        return pokemon_info
    else:
        print(f"error! code: {response.status_code}")
        return None
    
name = "pikachu"
get_pokemon_data(name)