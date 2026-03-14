def dict_sorter():
    list_of_tuples = [
  ('Russia', '25'),
  ('France', '132'),
  ('Germany', '132'),
  ('Spain', '178'),
  ('Italy', '162'),
  ('Portugal', '17'),
  ('Finland', '3'),
  ('Hungary', '2'),
  ('The Netherlands', '28'),
  ('The USA', '610'),
  ('The United Kingdom', '95'),
  ('China', '83'),
  ('Iran', '76'),
  ('Turkey', '65'),
  ('Belgium', '34'),
  ('Canada', '28'),
  ('Switzerland', '26'),
  ('Brazil', '25'),
  ('Austria', '14'),
  ('Israel', '12')
  ]
    dict_of_countries = {country : int(number) for country, number in list_of_tuples}
    sorted_country = sorted(dict_of_countries.keys(), key=lambda c: (-dict_of_countries[c],c))
    for country in sorted_country:
        print(country)
    

if __name__ == '__main__':
    dict_sorter()