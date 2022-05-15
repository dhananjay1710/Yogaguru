def calculate_score(diff_matrix):
    diff_avg = sum(diff_matrix)/len(diff_matrix)
    if diff_avg < 5:
        return '10'
    elif diff_avg < 10:
        return '9'
    elif diff_avg < 15:
        return '8'
    elif diff_avg < 20:
        return '7'
    else:
        return "Please make a better attempt !"