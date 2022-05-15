import json
import math

def angle_utils(indices, coordinates):
    p1 = coordinates[indices[0]]
    p2 = coordinates[indices[1]]
    p3 = coordinates[indices[2]]
    
    if p1 and p2 and p3:

        if(p3[0] - p2[0] == 0 and p2[0] - p1[0] == 0):
            return 0
        if(p2[0] - p1[0] == 0):
            m2 = (p3[1] - p2[1])/(p3[0] - p2[0])
            return (90 - math.degrees(math.atan(m2)))
        if(p3[0] - p2[0] == 0):
            m1 = (p2[1] - p1[1])/(p2[0] - p1[0])
            return (90 - math.degrees(math.atan(m1)))
        m1 = (p2[1] - p1[1])/(p2[0] - p1[0])
        m2 = (p3[1] - p2[1])/(p3[0] - p2[0])
        if(m1 * m2 == -1):
            theta = 90
        else:
            tan_theta = (m2-m1)/(1 + m1 * m2)
            theta = math.degrees(math.atan(tan_theta))
            #if abs(theta) > 90:
                #theta = 180 - abs(theta)
        return theta
    else:
        return 1000


def calculate_angle(pose_coordinates):
    f = open("AngleValues/poseIndices.json")
    pose_indices_dict = json.load(f)
    f.close()
    store_dict = {}
    for k in  pose_indices_dict:
        store_dict[k] = angle_utils(pose_indices_dict[k], pose_coordinates)        

        for joint in store_dict:
            if abs(store_dict[joint]) > 90:
                store_dict[joint] = 180 - abs(store_dict[joint])
    return store_dict
