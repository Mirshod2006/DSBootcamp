def data_types():
    age, name, score, male, project_num = 25, "Husniddin", 98.84, True, [1,2,3]
    score_tech = {"Flutter" : 99.70, "Networking Basics" : 96.3}
    fav_color = ('green','black','red')
    book_set = {'Shepher','A Farewell to Arms'}
    personal_info = [age, name, score, male, project_num, score_tech, fav_color, book_set]
    info_types = [type(data).__name__ for data in personal_info]
    print(info_types)

if __name__ == '__main__':
    data_types()