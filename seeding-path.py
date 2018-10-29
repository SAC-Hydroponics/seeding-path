#!/usr/bin/env python
"""Move Rectangle Farmware"""
#Import libraries
from farmware_tools import device, get_config_value, app

#so far only path of seeding starting at
# Load inputs from Farmware page widget specified in manifest file
pos_x = get_config_value('Seeding Path', 'start_x')
pos_y = get_config_value('Seeding Path', 'start_y')
pos_z = get_config_value('Seeding Path', 'start_z')#later
#X axis is length, Y axis is width
plantLength = get_config_value('Seeding Path', 'plant_l')
plantWidth = get_config_value('Seeding Path', 'plant_w')
cellCountX = get_config_value('Seeding Path', 'cellX')
cellCountY = get_config_value('Seeding Path', 'cellY')

#Define functions
def moveAbs(x, y, z):
    device.log('Moving to ' + str(x) + ', ' + str(y) + ', ' + str(z), 'success', ['toast'])
    device.move_absolute(
        {
            'kind': 'coordinate',
            'args': {'x': x, 'y': y, 'z': z}
        },
        100,
        {
            'kind': 'coordinate',
            'args': {'x': 0, 'y': 0, 'z': 0}
        }
    )

sense = 1
for i in range(cellCountX):
	plant_x = plantWidth*i+pos_x
	if sense:
		for j in range(0,cellCountY+1,1):
			plant_y = plantLength*j+pos_y
			#print('cords',x,y)
			moveAbs(plant_x, plant_y, pos_z)
			#new_plant = app.add_plant(x = x,y = y)
		sense = 0
	else:
		for j in range(cellCountY,-1,-1):
			plant_y = plantLength*j+pos_y
			moveAbs(plant_x, plant_y, pos_z)
			#print('cords',x,y)
		sense = 1

device.log('success!!', 'success', ['toast'])

if __name__ == '__main__':
    farmware_name = 'move_to_safe'
