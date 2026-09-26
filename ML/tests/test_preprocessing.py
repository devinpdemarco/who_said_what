from src import ng_train

# outputting the list of sample topics
print(f'Topics: {list(ng_train.target_names)}')

# outputting the different topics and article distribution
med_count = 0
space_count = 0
chris_count = 0

for doc in ng_train.target:
    match doc:
        case 0:
            med_count += 1
        case 1:
            space_count += 1
        case 2:
            chris_count += 1

print(f'Med: {med_count}\nSpace: {space_count}\nChristian: {chris_count}')


ng_train.filenames.shape
print(len(ng_train.data))
list(ng_train.data[:3])