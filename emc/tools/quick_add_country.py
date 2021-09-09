tag = input("(Tag):")
name = input("(Name):")

with open(f"common/countries/{name}.txt", "w") as f: 
    f.write("""
graphical_culture = southamerican_gfx
graphical_culture_2d = southamerican_2d

color = { 45  101  79 }""")

with open(f"common/countries/colors.txt", "a") as f: 
    f.write(f"""
{tag} = {{
  color = rgb {{ 2  10  222 }}
  color_ui = rgb {{ 255 255 155}}
}}""")


with open(f"history/countries/{tag} - {name}.txt", "w") as f: 
    f.write("""
set_convoys = 20
set_politics = {
    ruling_party = neutrality
    last_election = "2019.1.1"
    election_frequency = 72
    elections_allowed = no
}
set_popularities = {
    democratic = 0
    fascism = 0
    communism = 0
    neutrality = 100
}""")


with open(f"common/country_tags/{tag}.txt", "w") as f: 
    f.write(f'{tag} = "countries/{name}.txt"')