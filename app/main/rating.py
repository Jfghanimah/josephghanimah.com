import math

# g helps calculate how impervious a rating is to change. Sort of like its intertial mass.
def g(rd):
    return 1 / math.sqrt(1 + 3 * rd**2 / math.pi**2)


# E calculates expected outcome of a match given two ratings and the rd of the opponent
def E(rating1, rating2, rd2):
    return 1 / (1 + math.exp(-g(rd2) * (rating1 - rating2)))


# Use this to calculate change of a player to another player
def new_rating(rating1, rd1, rating2, rd2, score):
    # step 1
    factor = 173.7178

    # step 2 calculate internal ratings and deviations
    iRating1 = (rating1 - 1500) / factor
    iRating2 = (rating2 - 1500) / factor
    iRd1 = rd1 / factor
    iRd2 = rd2 / factor

    # step 3
    v = (g(iRd2)**2 * E(iRating1, iRating2, iRd2) * (1 - E(iRating1, iRating2, iRd2)))**(-1)

    # no step 4!

    # no step 5!

    # Step 6
    iRd1_star = math.sqrt(iRd1**2 + 0.06**2)

    # Step 7
    iRd1_prime = 1 / math.sqrt(1 / iRd1_star**2 + 1 / v)

    iRating1_prime = iRating1 + iRd1_prime**2 * g(iRd2) * (score - E(iRating1, iRating2, iRd2))

    # step 8 convert back to original scale
    new_rating1 = round(iRating1_prime * factor + 1500)
    new_rd1 = round(iRd1_prime * factor)

    return new_rating1, new_rd1

