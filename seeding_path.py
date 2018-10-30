#!/usr/bin/env python
"""Move Rectangle Farmware"""
#Import libraries
from farmware_tools import device, get_config_value, app

#Find arm position at start of program
start_arm_x = device.get_current_position('x')
start_arm_y = device.get_current_position('y')
start_arm_z = device.get_current_position('z')

#Load inputs from Farmware page widget specified in manifest file. X axis is length, Y axis is width.
pos_x = get_config_value('Seeding Path', 'start_x')
pos_y = get_config_value('Seeding Path', 'start_y')
pos_z = get_config_value('Seeding Path', 'start_z')
plantLength = get_config_value('Seeding Path', 'plant_l')
plantWidth = get_config_value('Seeding Path', 'plant_w')
cellCountX = get_config_value('Seeding Path', 'cellX')
cellCountY = get_config_value('Seeding Path', 'cellY')

#Define additional varialbes
safeZ = -200
plantingRetract = 5
seedToolX = 1330
seedToolY = 136
seedToolZ = -325
toolExtractX = 1240
plant_x = 0
plant_y = 0

#Define functions
def moveAbs(x, y, z):
    #device.log('Moving to ' + str(x) + ', ' + str(y) + ', ' + str(z), 'success', ['toast'])
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

#If needed rertract to safe Z, then pick up seed tool.
if start_arm_z > safeZ:
	moveAbs(seedToolX, seedToolY, start_arm_z)
	moveAbs(seedToolX, seedToolY, seedToolZ)
	moveAbs(toolExtractX, seedToolY, seedToolZ)
	moveAbs(pos_x, pos_y, seedToolZ)
	moveAbs(pos_x, pos_y, pos_z)
else:
	moveAbs(start_arm_x, start_arm_y, safeZ)
	moveAbs(seedToolX, seedToolY, safeZ)
	moveAbs(seedToolX, seedToolY, seedToolZ)
	moveAbs(toolExtractX, seedToolY, seedToolZ)
	moveAbs(pos_x, pos_y, seedToolZ)
	moveAbs(pos_x, pos_y, pos_z)

#Deposit seeds by moving from hole to hole.
sense = 1
for i in range(cellCountX):
	plant_x = plantWidth*i+pos_x
	if sense:
		for j in range(0,cellCountY+1,1):
			plant_y = plantLength*j+pos_y
			#print('cords',x,y)
			moveAbs(plant_x, plant_y, pos_z+plantingRetract)
			moveAbs(plant_x, plant_y, pos_z)
			#new_plant = app.add_plant(x = x,y = y)
			moveAbs(plant_x, plant_y, pos_z+plantingRetract)
		sense = 0
	else:
		for j in range(cellCountY,-1,-1):
			plant_y = plantLength*j+pos_y
			moveAbs(plant_x, plant_y, pos_z)
			#print('cords',x,y)
		sense = 1
		
#Return seed tool to toolbay.
moveAbs(plant_x, plant_y, seedToolZ)
moveAbs(plant_x, seedToolY, seedToolZ)
moveAbs(seedToolX, seedToolY, seedToolZ)

#Seperate seed tool from arm.
moveAbs(seedToolX, seedToolY, seedToolZ+60)

#Move to arm storage position.
moveAbs(seedToolX, 300, safeZ)


device.log('success!!', 'success', ['toast'])

if __name__ == '__main__':
    farmware_name = 'seeding_path'
