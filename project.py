import pygame
import random
import time

pygame.init()

#Color 
WHITE = (255, 255, 255)   #RBG
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (8, 160, 105)
BLUE = (50, 153, 213)

#Constant
block_size = 38
font_letterS = pygame.font.SysFont("arial", 20)
font_letterB = pygame.font.SysFont("arial", 25)
sell_value = [1,2,8,16,64]
wall_list = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9],[0,10],[0,11],[0,12],[0,13],[0,14],[0,15],[0,16],[0,17],[11,0],[11,1],[11,2],[11,3],[11,4],[11,5],[11,6],[11,7],[11,8],[11,9],[11,10],[11,11],[11,12],[11,13],[11,14],[11,15],[11,16],[11,17],[1,17],[2,17],[3,17],[4,17],[5,17],[6,17],[7,17],[8,17],[9,17],[10,17],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],[7,3],[8,3],[9,3],[10,3],[1,5],[2,5],[3,5],[4,5],[7,5],[8,5],[9,5],[10,5],[2,6],[2,7],[2,8],[2,9],[2,10],[2,13],[2,14],[2,15],[3,13],[4,7],[4,8],[4,9],[4,10],[4,11],[4,13],[4,15],[4,16],[5,7],[5,13],[6,7],[6,8],[6,10],[6,12],[6,13],[6,15],[6,16],[7,10],[7,12],[7,15],[8,7],[8,8],[8,9],[8,10],[8,12],[8,13],[8,15],[9,8],[9,10],[9,12],[10,10],[10,14]]
sell_area = [[7,4],[8,4],[9,4]]
shop_area = [[1,4],[2,4],[3,4],[4,4]]

#Variable
score = high_score = 0
stop = 0
money = 0
timeleft = 5*60*10
x_pos, y_pos = 5*block_size, 4*block_size
source_list = []
level = [2,4,5] 
inventory_max = 1
inventory_list = []
inventory_kind_list = [0, 0, 0, 0, 0] 
direction = 2
check_shop_open = 0
capacity_cost = 8
equipment_cost = 16 
Game_run = True
Count = 1

#Load image
MONEY = pygame.transform.scale(pygame.image.load('MONEY.png'),(block_size,block_size))
BAG = pygame.transform.scale(pygame.image.load('BAG.png'),(block_size,block_size))
BACKGROUND = pygame.transform.scale(pygame.image.load('BACKGROUND.png'),(18*block_size,18*block_size))
_3I = pygame.transform.scale(pygame.image.load('3I.png'),(4.5*block_size,2*block_size))
SELLSHOP = pygame.transform.scale(pygame.image.load('SELLSHOP.png'),(4*block_size, 3*block_size))
UPGRADESHOP = pygame.transform.scale(pygame.image.load('UPGRADESHOP.png'),(4*block_size, 3*block_size))
FRONT_SIDE = pygame.transform.scale(pygame.image.load('FRONT.png'), (block_size, block_size))
BACK_SIDE = pygame.transform.scale(pygame.image.load('BACK.png'), (block_size, block_size))
LEFT_SIDE = pygame.transform.scale(pygame.image.load('LEFTSIDE.png'), (block_size, block_size))
RIGHT_SIDE = pygame.transform.scale(pygame.image.load('RIGHTSIDE.png'), (block_size, block_size))
GROUND = pygame.transform.scale(pygame.image.load('GROUND.png'), (block_size, block_size))
COBBLESTONE = pygame.transform.scale(pygame.image.load('COBBLESTONE.png'), (block_size, block_size))
COAL = pygame.transform.scale(pygame.image.load('COAL.png'), (block_size, block_size))
IRON = pygame.transform.scale(pygame.image.load('IRON.png'), (block_size, block_size))
GOLD = pygame.transform.scale(pygame.image.load('GOLD.png'), (block_size, block_size))
EMERALD = pygame.transform.scale(pygame.image.load('EMERALD.png'), (block_size, block_size))
DIAMOND = pygame.transform.scale(pygame.image.load('DIAMOND.png'), (block_size, block_size))
STONE_PICKAXE =pygame.transform.scale(pygame.image.load('STONEPICKAXE.png'), (block_size, block_size))
IRON_PICKAXE =pygame.transform.scale(pygame.image.load('IRONPICKAXE.png'), (block_size, block_size))
DIAMOND_PICKAXE =pygame.transform.scale(pygame.image.load('DIAMONDPICKAXE.png'), (block_size, block_size))

#Load sound
SELL_ITEM_SOUND = pygame.mixer.Sound("SELLITEM.mp3")
UPGRADE_SOUND = pygame.mixer.Sound("UPGRADE.mp3")
EXPLOIT_SOUND = pygame.mixer.Sound("EXPLOITATION.mp3")

#Screen_size... 
dis_width = dis_height = 18*block_size
dis = pygame.display.set_mode((dis_width,dis_height))
pygame.display.set_caption('Mining time')
clock = pygame.time.Clock()

#Proceduce
def add_source():
	while len(source_list)<3:
		source_type = random.randrange(0,level[0])
		source_x_pos = random.randrange(1,11)*block_size
		source_y_pos = random.randrange(6,17)*block_size
		if check_source(source_x_pos, source_y_pos):
			source_list.append((source_type,source_x_pos,source_y_pos))

def check(x,y):
	for i in wall_list:
		if x == i[0]*block_size and y == i[1]*block_size: return False
	return True

def  check_source(x,y):
	for i in wall_list:
		if x == i[0]*block_size and y == i[1]*block_size: return False
	for i in source_list:
		if x == i[1] and y == i[2]: return False
	if x == x_pos and y == y_pos: return False
	return True

def exploit_source():
	for x in source_list:
		if x_pos == x[1] and y_pos  == x[2]:
			if len(inventory_list)<inventory_max:
				inventory_list.append(x[0])
				inventory_kind_list[x[0]] +=1
				source_list.remove(x)		
				EXPLOIT_SOUND.play()		

def sell_source():
	Val = 0
	for x in sell_area:
		if x_pos == x[0]*block_size and y_pos == x[1]*block_size:
			while len(inventory_list)>0:
				i=inventory_list[0]
				Val += sell_value[i]
				inventory_list.remove(i)
				inventory_kind_list[i] -=1
	if Val !=0: SELL_ITEM_SOUND.play()
	return Val

def equipment_shop(check_shop_open):
	for x in shop_area:
		if x_pos  == x[0]*block_size and y_pos == x[1]*block_size:
			return check_shop_open ^1
	return check_shop_open	
	
def write(sentence, color, x, y):
	string = font_letterS.render(sentence, True, color)
	dis.blit(string, [x,y])
def write_2(sentence, color, x, y):
	string = font_letterB.render(sentence, True, color)
	dis.blit(string, [x,y])


#MAIN PROGRAM
while Game_run:
	#Lose game/ play again or quit game 
	while stop == 1 and Game_run:
		dis.fill(BLACK)
		write_2("TIME'S UP", RED, 7*block_size +10, 5*block_size)
		write_2('YOUR SCORE:  '+str(score), WHITE, 6*block_size +20, 9*block_size)
		high_score = max(high_score,score)
		write_2('HIGH SCORE:  '+str(high_score), WHITE, 6*block_size +20, 7*block_size)
		write('Press C to play again or Q to quit game', BLUE, 5*block_size, 10*block_size)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Game_run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					stop = 0
					money = score = 0
					timeleft = 5*60*10
					x_change, y_change = 0, block_size
					x_pos, y_pos = 5*block_size, 4*block_size
					source_list=[]
					level = [2,4,5] 
					inventory_max = 1
					inventory_list =[]
					inventory_kind_list = [0, 0, 0, 0, 0] 
					direction = 2
					check_shop_open = 0
					capacity_cost = 8
					equipment_cost = 16 
				if event.key == pygame.K_q:
					Game_run = False
	#Main
	while stop == 0 and Game_run:
		timeleft-=1
		if timeleft == 0: stop = 1
		dis.blit(BACKGROUND,(0,0))
		s = '0'+ str(timeleft//10%60)	
		write_2('Time:   '+str(timeleft//10//60)+':'+s[-2:], WHITE, 13*block_size, 3*block_size)   #Show timeleft
		for i in range(12):
			for j in range(18):
				if j>3:
					dis.blit(GROUND, (i*block_size,j*block_size))
				else:
					dis.blit(COBBLESTONE, (i*block_size,j*block_size))			
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Game_run = False
			#Control and interaction
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					check_shop_open = 0
					y_pos -= block_size 
					direction = 0
					if check(x_pos, y_pos) == False:
						y_pos += block_size
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					check_shop_open = 0
					y_pos += block_size
					direction = 2
					if check(x_pos, y_pos) ==False:
						y_pos -= block_size
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					check_shop_open = 0
					x_pos += block_size
					direction = 1
					if check(x_pos, y_pos) ==False:
						x_pos -= block_size
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					check_shop_open = 0
					x_pos -= block_size
					direction = 3
					if check(x_pos, y_pos) ==False:
						x_pos += block_size
				if event.key == pygame.K_SPACE:
					exploit_source()
					temp = sell_source()
					money += temp
					score += temp
					check_shop_open = equipment_shop(check_shop_open)
				if check_shop_open == 1: 
					if event.key == pygame.K_e and money >= capacity_cost:
						money -= capacity_cost
						capacity_cost *=2
						inventory_max +=1
						UPGRADE_SOUND.play()
					if event.key == pygame.K_q and money >=equipment_cost and level[0] != 5:
						money -= equipment_cost
						equipment_cost *= 5
						level.remove(level[0])
						UPGRADE_SOUND.play()
		add_source()
		#Draw on screen
		for x in source_list:					#Draw ore
			if x[0] == 0:
				dis.blit(COAL, (x[1], x[2]))
			elif x[0] == 1:
				dis.blit(IRON, (x[1], x[2]))
			elif x[0] == 2:
				dis.blit(GOLD, (x[1], x[2]))
			elif x[0] == 3:
				dis.blit(EMERALD, (x[1], x[2]))
			else:
				dis.blit(DIAMOND, (x[1], x[2]))
		if direction == 0:						#Draw MC
			dis.blit(BACK_SIDE, (x_pos, y_pos))
		elif direction == 1:
			dis.blit(RIGHT_SIDE, (x_pos, y_pos))
		elif direction == 2:
			dis.blit(FRONT_SIDE, (x_pos, y_pos))
		else:
			dis.blit(LEFT_SIDE, (x_pos, y_pos))

		for x in wall_list:
			dis.blit(COBBLESTONE, (x[0]*block_size, x[1]*block_size))	#Draw wall
		write_2('UPGRADE', WHITE, 2*block_size-10, 0*block_size)
		write_2('SELL ORE', WHITE, 8*block_size-15, 0*block_size)
		dis.blit(UPGRADESHOP, (block_size, block_size-5))
		dis.blit(SELLSHOP, (7*block_size, block_size-5))
		dis.blit(_3I, (13*block_size,15*block_size))
		#Show shop information
		if check_shop_open == 1: 
			pygame.draw.rect(dis, GREEN, (1*block_size, 0, 10*block_size, 4*block_size-5))
			write('+1 slot inventory', WHITE, 7*block_size + 10,0)
			write(str(inventory_max) + ' → ' + str(inventory_max + 1), WHITE, 8*block_size, block_size)
			if money<capacity_cost:
				write_2('$'+str(capacity_cost), RED, 8*block_size +10,2*block_size)
			else:
				write_2('$'+str(capacity_cost), WHITE, 8*block_size +10,2*block_size)
			write('Press E to update',WHITE, 7*block_size,3*block_size)
			write('Buy new tool', WHITE, block_size + 10,0)
			if level[0] == 2:
				dis.blit(STONE_PICKAXE, (block_size, block_size))
				write('→', WHITE, 2*block_size+10, block_size)
				dis.blit(IRON_PICKAXE, (3*block_size,block_size))
			if level[0] == 4:
				dis.blit(IRON_PICKAXE, (block_size,block_size))
				write('→', WHITE, 2*block_size+5, block_size)
				dis.blit(DIAMOND_PICKAXE, (3*block_size,block_size))
			if level[0] !=5 :
				if money<equipment_cost:
					write_2('$'+str(equipment_cost), RED, 2*block_size,2*block_size)
				else:
					write_2('$'+str(equipment_cost), WHITE, 2*block_size,2*block_size)
				write('Press Q to update',WHITE, block_size,3*block_size)
			else:
				dis.blit(DIAMOND_PICKAXE, (2*block_size,block_size))
				write('MAX', WHITE, 2*block_size, 2*block_size)
		
		#Show money
		write_2('$:'+ str(money), WHITE, 13*block_size+5, 0)
		dis.blit(MONEY,(12*block_size,0))
		
		#Show inventory
		write('Price:', WHITE, 12*block_size, 4*block_size)
		for i in range (5):
			if i == 0:
				dis.blit(COAL, (14*block_size - 5, (5+2*i)*block_size))
				write(str(inventory_kind_list[i]), WHITE, 15*block_size, (5+2*i)*block_size + 5)
				write('$'+str(sell_value[i]), WHITE, 13*block_size - 10, (5+2*i)*block_size + 5)
			elif i == 1:
				dis.blit(IRON, (14*block_size - 5, (5+2*i)*block_size))
				write(str(inventory_kind_list[i]), WHITE, 15*block_size, (5+2*i)*block_size + 5)
				write('$'+str(sell_value[i]), WHITE, 13*block_size - 10, (5+2*i)*block_size + 5)
			elif i == 2 and level[0] > i:
				dis.blit(GOLD, (14*block_size - 5, (5+2*i)*block_size))
				write(str(inventory_kind_list[i]), WHITE, 15*block_size, (5+2*i)*block_size + 5)
				write('$'+str(sell_value[i]), WHITE, 13*block_size - 10, (5+2*i)*block_size + 5)
			elif i == 3 and level[0] >i:
				dis.blit(EMERALD, (14*block_size - 5, (5+2*i)*block_size))
				write(str(inventory_kind_list[i]), WHITE, 15*block_size, (5+2*i)*block_size + 5)
				write('$'+str(sell_value[i]), WHITE, 13*block_size - 10, (5+2*i)*block_size + 5)
			elif i==4 and level[0] > i:
				dis.blit(DIAMOND, (14*block_size - 5, (5+2*i)*block_size))
				write(str(inventory_kind_list[i]), WHITE, 15*block_size, (5+2*i)*block_size + 5)
				write('$'+str(sell_value[i]), WHITE, 13*block_size - 10, (5+2*i)*block_size + 5)
		dis.blit(BAG, (12*block_size, block_size))
		write_2('Score:  '+str(score), WHITE, 12*block_size, 2*block_size)
		if len(inventory_list) == inventory_max:
			Count =(Count + 1) % 2
			if Count ==1:
				write_2('Capacity: '+str(len(inventory_list))+'/'+str(inventory_max), RED, 13*block_size + 5, block_size)
			else:
				write_2('Capacity: '+str(len(inventory_list))+'/'+str(inventory_max), BLACK, 13*block_size + 5, block_size)
		else:
			write_2('Capacity: '+str(len(inventory_list))+'/'+str(inventory_max), WHITE, 13*block_size + 5, block_size)
		pygame.display.update()
		pygame.display.flip()
		clock.tick(10)
pygame.quit()
