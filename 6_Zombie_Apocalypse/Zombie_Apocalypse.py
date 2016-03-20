"""
Student portion of Zombie Apocalypse mini-project
"""
# @author  ouyangxinrong
# @email  ouyangxinrong@gmail.com
# @ I am small bird
# @ I like play football game the second delete
# @ 2016.3.20

import random
import poc_grid
import poc_queue
import poc_zombie_gui
#import user41_93dx5BUCT7_0
#import user41_XAVRsZqXCg_4 as poc_zombie_gui
# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)     
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """ 
        visited = poc_grid.Grid(self.get_grid_height(),
                                      self.get_grid_width())
        # for test
        #print self._visited.get_grid_height()
        #print self._visited.get_grid_width()
        distance_field = [[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)]\
                                    for dummy_row in range(self._grid_height)]
        #print self._distance_field
        boundary = poc_queue.Queue()
        
        if entity_type == HUMAN:
            for human in self._human_list:
                boundary.enqueue((human[0], human[1]))
        else:
            for zombie in self._zombie_list:
                boundary.enqueue((zombie[0], zombie[1]))
        for bound in boundary:
            visited.set_full(bound[0], bound[1])
            distance_field[bound[0]][bound[1]] = 0
        while boundary.__len__() != 0:
            
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]) and visited.is_empty(neighbor[0], neighbor[1]) :
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)                          
                    distance_field[neighbor[0]][neighbor[1]]= \
                           distance_field[current_cell[0]][current_cell[1]] + 1
        #for col in distance_field:
            #print col
        return  distance_field   
        

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        #print zombie_distance_field
        #print 
        #print self._human_list
        height = len(zombie_distance_field)
        width  = len(zombie_distance_field[0])
        for idx  in range(len(self._human_list)):
            dic = {}
            dummy_row = self._human_list[idx][0]
            dummy_col = self._human_list[idx][1]
            if dummy_row > 0 and self.is_empty(dummy_row - 1, dummy_col):
                dic[(dummy_row - 1, dummy_col)] = zombie_distance_field[dummy_row-1][dummy_col]
                
            if dummy_row < height - 1 and self.is_empty(dummy_row + 1, dummy_col):
                dic[(dummy_row + 1, dummy_col)] = zombie_distance_field[dummy_row+1][dummy_col]
                
            if dummy_col > 0 and self.is_empty(dummy_row, dummy_col - 1):
                dic[(dummy_row, dummy_col - 1)] = zombie_distance_field[dummy_row][dummy_col-1]
                
            if dummy_col < width - 1 and self.is_empty(dummy_row, dummy_col + 1):
                dic[(dummy_row, dummy_col + 1)] = zombie_distance_field[dummy_row][dummy_col+1]
                
            if (dummy_row > 0) and (dummy_col > 0) and self.is_empty(dummy_row - 1, dummy_col - 1):
                dic[(dummy_row - 1, dummy_col - 1)] = zombie_distance_field[dummy_row-1][dummy_col-1]
                
            if (dummy_row > 0) and (dummy_col < width - 1) and self.is_empty(dummy_row - 1 ,dummy_col + 1):
                dic[(dummy_row - 1 ,dummy_col + 1)] = zombie_distance_field[dummy_row-1][dummy_col+1]
                
            if (dummy_row < height - 1) and (dummy_col > 0)and self.is_empty(dummy_row + 1 ,dummy_col - 1):
                dic[(dummy_row + 1 ,dummy_col - 1)] = zombie_distance_field[dummy_row+1][dummy_col-1]
                
            if (dummy_row < height - 1) and (dummy_col < width - 1)and self.is_empty(dummy_row - 1 ,dummy_col + 1):
                dic[(dummy_row - 1 ,dummy_col + 1)] = zombie_distance_field[dummy_row-1][dummy_col+1]
           # print dic 
            dic[(dummy_row, dummy_col)] = zombie_distance_field[dummy_row][dummy_col]
            #print dic
            
            ##print "len" + str(len(dic))
            max_distance = max(dic.values())
            #print max_distance
            max_distance_list = []
            for item in dic:
                if dic[item] == max_distance:
                    max_distance_list.append(item)
           
            self._human_list[idx] = random.choice(max_distance_list)
            #print self._human_list 
          
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        height = len(human_distance_field)
        width  = len(human_distance_field[0])
        for idx  in range(len(self._zombie_list)):
            dic = {}
            dummy_row = self._zombie_list[idx][0]
            dummy_col = self._zombie_list[idx][1]
            if dummy_row > 0 and self.is_empty(dummy_row - 1, dummy_col):
                dic[(dummy_row - 1, dummy_col)] = human_distance_field[dummy_row-1][dummy_col]
                
            if dummy_row < height - 1 and self.is_empty(dummy_row + 1, dummy_col):
                dic[(dummy_row + 1, dummy_col)] = human_distance_field[dummy_row+1][dummy_col]
                
            if dummy_col > 0 and self.is_empty(dummy_row, dummy_col - 1):
                dic[(dummy_row, dummy_col - 1)] = human_distance_field[dummy_row][dummy_col-1]
                
            if dummy_col < width - 1 and self.is_empty(dummy_row, dummy_col + 1):
                dic[(dummy_row, dummy_col + 1)] = human_distance_field[dummy_row][dummy_col+1]
                
            
            dic[(dummy_row, dummy_col)] = human_distance_field[dummy_row][dummy_col]
            #print dic
            
            #print "len" + str(len(dic))
            min_distance = min(dic.values())
            #print min_distance
            min_distance_list = []
            for item in dic:
                if dic[item] == min_distance:
                    min_distance_list.append(item)
           
            self._zombie_list[idx] = random.choice(min_distance_list)
        

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
#user41_93dx5BUCT7_0.run_gui(Apocalypse(30, 40))
#obj = Apocalypse(3, 3, [(2,2)], [(2,2)], [(2, 1)])

#print obj.compute_distance_field(ZOMBIE)
#obj = Apocalypse(3, 3, [(1,2),(0,0)], [(2, 2)], [(1, 1)])
#print obj
#obj.clear()
#print obj
#dist = [[4, 3, 2], [3, 2, 1], [2, 1, 0]]
#obj.move_humans(dist) 
#obj = Apocalypse(3, 3, [(0, 0), (1, 0), (1, 1), (1, 2)], [(0, 2)], [(0, 1)])
#print obj.compute_distance_field(HUMAN)