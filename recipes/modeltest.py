import csv

with open('ingredients.csv', newline='') as csvfile:
    ingredients_list = []
    reader = csv.reader(csvfile)
    for row in reader:
        food = [row[11]]
        ingredients_list.append(tuple(food))
print(tuple(ingredients_list))