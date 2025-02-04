#### this program handles the lidar driver ####

# Lidar model : UST-10lx

from hokuyolx import HokuyoLX

# Angle : 270 degrés
# Résolution: 0,25 degrés

LIDAR_DRIVER = HokuyoLX()

bannedAngles=[]

def get_distance_at_angle(angle): # angle en degré
        assert angle>=0 and angle<=270 and (angle not in bannedAngles)
        timestamp, scan=LIDAR_DRIVER.get_dist()
	return scan[angle*4]


def get_closest_point_angle():
        timestamp, scan=LIDAR_DRIVER.get_dist()
        L=[]
        for i in range(len(scan)):
                if i*4 not in bannedAngles:
                        L.append(scan[i])
        return L.index(min(scan))
	# Return the angle to the closest point


def remove_unusable_point(angle):
        bannedAngles.append(angle)
	return bannedAngles
