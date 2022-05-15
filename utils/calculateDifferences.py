def calculate_differences(ip_angles, id_angles):
    diff_matrix_curr = []
    for joint in ip_angles:
        diff_matrix_curr.append(abs(abs(id_angles[joint]) - abs(ip_angles[joint])))
    return diff_matrix_curr