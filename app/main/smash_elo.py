import pandas as pd
from rating import new_rating

#df = pd.DataFrame(columns=["name", "character", "elo", "confidence"])
df = pd.read_csv("elos.csv", index_col=0)

while True:

    print('Debug Commands:')
    print("-------------------")
    print("0 - List Elos")
    print("1 - Add Game")
    print("2 - Add Player")
    x = int(input("\nEnter: "))
    print("")


    if x == 0:
        # Display Elos in order
        print(df.sort_values(by='Rating', ascending=False))

    elif x == 1:
        # Add a new game
        print(df)
        p1 = int(input("Enter Winner # "))
        p2 = int(input("Enter Loser # "))

        r1 = df.iloc[p1].Rating
        c1 = df.iloc[p1].Confidence
        r2 = df.iloc[p2].Rating
        c2 = df.iloc[p2].Confidence

        p1_ratings = new_rating(r1, c1, r2, c2, 1)
        p2_ratings = new_rating(r2, c2, r1, c1, 0)

        # reassign new ratings

        df.at[p1, 'Rating'] = p1_ratings[0]
        df.at[p1, 'Confidence'] = p1_ratings[1]
        df.at[p2, 'Rating'] = p2_ratings[0]
        df.at[p2, 'Confidence'] = p2_ratings[1]

        df.to_csv("elos.csv")

        pass

    elif x == 2:
        new_name = input("Player Name: ")
        new_character = input("Character: ")
        new_row = {"name":new_name , "character":new_character, "Rating":1500, "Confidence":350}

        if len(df.query("@new_name == Name and @new_character == Character").index) == 0:
            df = df.append(new_row, ignore_index=True)
            df.to_csv("elos.csv")
            print("Added!")
        else:
            print("Duplicate found in list already!")