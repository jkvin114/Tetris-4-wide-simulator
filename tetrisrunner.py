#!/usr/bin/python3

from tkinter import Canvas, Label, Tk, StringVar, Button, LEFT
from random import choice, randint
import time
import tetris
import winsound
from tetris import findpath, get_piece_queue
import pygame as pg


pg.mixer.init()
pg.init()

pg.mixer.set_num_channels(50)
combo0 = pg.mixer.Sound("tetris_sound\\combo0.wav")
combo1 = pg.mixer.Sound("tetris_sound\\combo1.wav")
combo2 = pg.mixer.Sound("tetris_sound\\combo2.wav")
combo3 = pg.mixer.Sound("tetris_sound\\combo3.wav")
combo4 = pg.mixer.Sound("tetris_sound\\combo4.wav")
combo5 = pg.mixer.Sound("tetris_sound\\combo5.wav")
combo6 = pg.mixer.Sound("tetris_sound\\combo6.wav")
combo7 = pg.mixer.Sound("tetris_sound\\combo7.wav")


actionlist_right=[]
actionlist_rotate= []
path=None
piece_queue=None
queue_count=-1

tetrimino_name=["I(sky blue)","L(Orange)","J(blue)","T(purple)","Z(red)","N(green)","O(yellow)"]
class GameCanvas(Canvas):
    def clean_line(self, boxes_to_delete):
        time.sleep(0.1)
        
        for box in boxes_to_delete:
            self.delete(box)
            
        self.update()
    def clean_blocks(self,boxes_to_delete):
        
        for box in boxes_to_delete:
                self.delete(box)
                
        self.update()
    def drop_boxes(self, boxes_to_drop):
        for box in boxes_to_drop:
            self.move(box, 0, Tetris.BOX_SIZE)
        self.update()

    def completed_lines(self, y_coords):
        cleaned_lines = 0
        y_coords = sorted(y_coords)
        
        
        
        for y in y_coords:
            if sum(1 for box in self.find_withtag('game') if self.coords(box)[3] == y) >=10:
                
                self.clean_line([box
                                for box in self.find_withtag('game')
                                if self.coords(box)[3] == y])
                
                
                self.drop_boxes([box
                                 for box in self.find_withtag('game')
                                 if self.coords(box)[3] < y])
                cleaned_lines += 1
        return cleaned_lines
    def clear_piece(self,coords):
        for y,x in coords:
            self.clean_blocks([box
                                    for box in self.find_withtag('game')
                                    if self.coords(box)[3] == y and self.coords(box)[2]==x])
       
    
    
    def game_board(self):
        board =[0 for _ in range(Tetris.GAME_HEIGHT // Tetris.BOX_SIZE)]
        for i in range(len(board)):
            board[i]=[0 for _ in range(10)]
        
        
        for box in self.find_withtag('game'):
            x, y, _, _ = self.coords(box)
            board[int(y // Tetris.BOX_SIZE)][int(x // Tetris.BOX_SIZE)] = 1
        return board
    
    def boxes(self):
        return self.find_withtag('game') == self.find_withtag(fill="blue")

class Shape():
    def __init__(self, coords = None):
        global queue_count
        if not coords:
            self.__coords = Tetris.SHAPES[piece_queue[queue_count]]
            self.id=piece_queue[queue_count]
            if queue_count==-1:
                self.__coords = Tetris.SHAPES[0]
                self.id=0
            if not path: 
                quit()
                return
            if len(path)>queue_count and queue_count>0:
                    if path[queue_count-1][2]:
                        print("use hold")
                    print((queue_count),".  case:",path[queue_count-1][0].id,", used :",tetrimino_name[path[queue_count-1][1]],", (",path[queue_count-1][3][0],",",path[queue_count-1][3][1],")")
            queue_count+=1
        else:
            self.__coords = coords

    @property
    def coords(self):
        return self.__coords

    def rotate(self):  
        self.__coords = self.__rotate()

    def rotate_directions(self):
        rotated = self.__rotate()
        directions = [(rotated[i][0] - self.__coords[i][0],
                       rotated[i][1] - self.__coords[i][1]) for i in range(len(self.__coords))]

        return directions

    @property
    def matrix(self):
        return [[1 if (j, i) in self.__coords else 0 \
                 for j in range(max(self.__coords, key=lambda x: x[0])[0] + 1)] \
                 for i in range(max(self.__coords, key=lambda x: x[1])[1] + 1)]

    def drop(self, board, offset):
        # print("\n\n\n")
        # print('\n'.join(''.join(map(str, b)) for b in board))
        # print("\n\n\n")
        off_x, off_y = offset
        # print(off_x,off_y)
        last_level = len(board) - len(self.matrix) + 1
        for level in range(off_y, last_level):
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    if board[level+i][off_x+j] == 1 and self.matrix[i][j] == 1:
                        return level - 1
        return last_level - 1  

    def __rotate(self):
        max_x = max(self.__coords, key=lambda x:x[0])[0]
        new_original = (max_x, 0)

        rotated = [(new_original[0] - coord[1],
                    new_original[1] + coord[0]) for coord in self.__coords]

        min_x = min(rotated, key=lambda x:x[0])[0]
        min_y = min(rotated, key=lambda x:x[1])[1]
        return [(coord[0] - min_x, coord[1] - min_y) for coord in rotated]

class Piece():
    def __init__(self, canvas, start_point, shape = None):
        self.__shape = shape
        if not shape:
            self.__shape = Shape()
        self.canvas = canvas
        self.boxes = self.__create_boxes(start_point)
    
    def erase(self):
        coords = [(self.canvas.coords(box)[3],self.canvas.coords(box)[2] )for box in self.boxes]
        self.canvas.clear_piece(coords)
        
        
    @property
    def shape(self):
        return self.__shape

    def move(self, direction):
        if all(self.__can_move(self.canvas.coords(box), direction) for box in self.boxes):
            x, y = direction
            for box in self.boxes:
                self.canvas.move(box,
                                 x * Tetris.BOX_SIZE,
                                 y * Tetris.BOX_SIZE)
            return True
        return False

    def rotate(self):
        directions = self.__shape.rotate_directions()
        if all(self.__can_move(self.canvas.coords(self.boxes[i]), directions[i]) for i in range(len(self.boxes))):
            self.__shape.rotate()
            for i in range(len(self.boxes)):
                x, y = directions[i]
                self.canvas.move(self.boxes[i],
                                 x * Tetris.BOX_SIZE,
                                 y * Tetris.BOX_SIZE)

    @property
    def offset(self):
        return (min(int(self.canvas.coords(box)[0]) // Tetris.BOX_SIZE for box in self.boxes),
                min(int(self.canvas.coords(box)[1]) // Tetris.BOX_SIZE for box in self.boxes))

    def predict_movement(self, board):
        level = self.__shape.drop(board, self.offset)
        min_y = min([self.canvas.coords(box)[1] for box in self.boxes])
        return (0, level - (min_y // Tetris.BOX_SIZE))

    def predict_drop(self, board):
        level = self.__shape.drop(board, self.offset)
        self.remove_predicts()

        min_y = min([self.canvas.coords(box)[1] for box in self.boxes])
        for box in self.boxes:
            x1, y1, x2, y2 = self.canvas.coords(box)
            box = self.canvas.create_rectangle(x1,
                                               level * Tetris.BOX_SIZE + (y1 - min_y),
                                               x2,
                                               (level + 1) * Tetris.BOX_SIZE + (y1 - min_y),
                                               fill="lightgray",
                                               tags = "predict")
#o   t  h:   t   l  h:o   l   n    h:o    o  n    h:l    n  z  h:l      l   z  h:n       z   t  h:n     t   o  h:n      n  o  h:t           (t o l z  n t  o)



    def remove_predicts(self):
        for i in self.canvas.find_withtag('predict'):
            self.canvas.delete(i) 
        self.canvas.update()

    def __create_boxes(self, start_point):
        boxes = []
        off_x, off_y = start_point
        for coord in self.__shape.coords:
            x, y = coord
            if self.__shape.id==0:
                box = self.canvas.create_rectangle(x * Tetris.BOX_SIZE + off_x,
                                               y * Tetris.BOX_SIZE + off_y,
                                               x * Tetris.BOX_SIZE + Tetris.BOX_SIZE + off_x,
                                               y * Tetris.BOX_SIZE + Tetris.BOX_SIZE + off_y,
                                               fill="skyblue",
                                               tags="game")
            elif self.__shape.id==1:
                box = self.canvas.create_rectangle(x * Tetris.BOX_SIZE + off_x,
                                               y * Tetris.BOX_SIZE + off_y,
                                               x * Tetris.BOX_SIZE + Tetris.BOX_SIZE + off_x,
                                               y * Tetris.BOX_SIZE + Tetris.BOX_SIZE + off_y,
                                               fill="orange",
                                               tags="game")
            elif self.__shape.id==2:
                box = self.canvas.create_rectangle(x * Tetris.BOX_SIZE + off_x,
                                               y * Tetris.BOX_SIZE + off_y,
                                               x * Tetris.BOX_SIZE + Tetris.BOX_SIZE + off_x,
                                               y * Tetris.BOX_SIZE + Tetris.BOX_SIZE + off_y,
                                               fill="blue",
                                               tags="game")
            elif self.__shape.id==3:
                box = self.canvas.create_rectangle(x * Tetris.BOX_SIZE + off_x,
                                               y * Tetris.BOX_SIZE + off_y,
                                               x * Tetris.BOX_SIZE + Tetris.BOX_SIZE + off_x,
                                               y * Tetris.BOX_SIZE + Tetris.BOX_SIZE + off_y,
                                               fill="purple",
                                               tags="game")
            elif self.__shape.id==4:
                box = self.canvas.create_rectangle(x * Tetris.BOX_SIZE + off_x,
                                               y * Tetris.BOX_SIZE + off_y,
                                               x * Tetris.BOX_SIZE + Tetris.BOX_SIZE + off_x,
                                               y * Tetris.BOX_SIZE + Tetris.BOX_SIZE + off_y,
                                               fill="red",
                                               tags="game")
            elif self.__shape.id==5:
                box = self.canvas.create_rectangle(x * Tetris.BOX_SIZE + off_x,
                                               y * Tetris.BOX_SIZE + off_y,
                                               x * Tetris.BOX_SIZE + Tetris.BOX_SIZE + off_x,
                                               y * Tetris.BOX_SIZE + Tetris.BOX_SIZE + off_y,
                                               fill="green",
                                               tags="game")
            elif self.__shape.id==6:
                box = self.canvas.create_rectangle(x * Tetris.BOX_SIZE + off_x,
                                               y * Tetris.BOX_SIZE + off_y,
                                               x * Tetris.BOX_SIZE + Tetris.BOX_SIZE + off_x,
                                               y * Tetris.BOX_SIZE + Tetris.BOX_SIZE + off_y,
                                               fill="yellow",
                                               tags="game")
            
            
            
            
            
            boxes += [box]
        return boxes
    

    def __can_move(self, box_coords, new_pos):
        x, y = new_pos
        x = x * Tetris.BOX_SIZE
        y = y * Tetris.BOX_SIZE
        x_left, y_up, x_right, y_down = box_coords

        overlap = set(self.canvas.find_overlapping((x_left + x_right) / 2 + x, 
                                                   (y_up + y_down) / 2 + y, 
                                                   (x_left + x_right) / 2 + x,
                                                   (y_up + y_down) / 2 + y))
        other_items = set(self.canvas.find_withtag('game')) - set(self.boxes)

        if y_down + y > Tetris.GAME_HEIGHT or \
           x_left + x < 0 or \
           x_right + x > Tetris.GAME_WIDTH or \
           overlap & other_items:
            # print("y_down + y > Tetris.GAME_HEIGHT : {}".format(y_down + y > Tetris.GAME_HEIGHT))
            # print("x_left + x < 0                  : {}".format(x_left + x < 0))
            # print("x_right + x > Tetris.GAME_WIDTH : {}".format(x_right + x > Tetris.GAME_WIDTH))
            # print("overlap & other_items           : {}".format(overlap & other_items))
            return False
        return True        

class Tetris():
    SHAPES = ([(0, 0), (1, 0), (2, 0), (3, 0)],   # I
              [(2, 0), (0, 1), (1, 1), (2, 1)],     # L
              [(0, 0), (0, 1), (1, 1), (2, 1)],     # J
              [(1, 0), (0, 1), (1, 1), (2, 1)],     # T
              [(0, 0), (1, 0), (1, 1), (2, 1)],     # Z
              [(0, 1), (1, 1), (1, 0), (2, 0)],     # N
              [(0, 0), (1, 0), (0, 1), (1, 1)])     # O     
    
    BOX_SIZE = 20

    GAME_WIDTH = 220
    GAME_HEIGHT = 500
    GAME_START_POINT = 130
    
    #GAME_WIDTH / 2 / BOX_SIZE * BOX_SIZE - BOX_SIZE

    def __init__(self, predictable = False):
        self._level = 1
        self._score = 0
        self._blockcount = 0
        self.speed = 200
        self.predictable = predictable

        self.root = Tk()
        self.root.geometry("500x550") 
        self.root.title('Tetris')
        self.root.bind("<Key>", self.game_control)
        
        self.__level_score_label()
        self.__game_canvas()
        self.__next_piece_canvas()
        self.__hold_piece_canvas()
        self.first=True
        
    def fill_six(self):
        for y in range(25):
            for x in range(6):
                self.canvas.create_rectangle(x * Tetris.BOX_SIZE+10,
                                                   y * Tetris.BOX_SIZE,
                                                   x * Tetris.BOX_SIZE + Tetris.BOX_SIZE+10,
                                                   y * Tetris.BOX_SIZE + Tetris.BOX_SIZE,
                                                   fill="gray",
                                                   tags="game")
        for x,y in [(6,24),(6,23),(7,24)]:
            self.canvas.create_rectangle(x * Tetris.BOX_SIZE+10,
                                                       y * Tetris.BOX_SIZE,
                                                       x * Tetris.BOX_SIZE + Tetris.BOX_SIZE+10,
                                                       y * Tetris.BOX_SIZE + Tetris.BOX_SIZE,
                                                       fill="gray",
                                                       tags="game")
        
        self.canvas.pack()
        
    def auto_control(self,event):
        if event==0:   #rotate
            self.current_piece.rotate()
            self.update_predict()
        elif event==1:        #move right
            self.current_piece.move((1, 0))
            self.update_predict()
        elif event==2:       #move left
            self.current_piece.move((-1, 0))
            self.update_predict()
        elif event==3:    #drop
            self.hard_drop()
            
        elif event==4:       #hold
            self.hold()
            self.update_predict()
                
        
    
    def game_control(self, event):
        if event.keysym in ["a", "Left", "\uf702"]:
            self.auto_control(2)
        elif event.keysym in ["d", "Right", "\uf703"]:
            self.auto_control(1)
        elif event.keysym in ["s", "space", "\uf701"]:
            self.auto_control(3)
        elif event.keysym in ["w", "Up", "\uf700"]:
            self.auto_control(0)
        elif event.keysym in ["c", "C"]:
            self.auto_control(4)
    
    def new_game(self):
        self.level = 1
        self.score = 0
        self.blockcount = 0
        self.speed = 200
        self.first=True
        self.canvas.delete("all")
        self.next_canvas.delete("all")
        self.hold_canvas.delete("all")
        
        self.__draw_canvas_frame()
        self.__draw_hold_canvas_frame()
        self.__draw_next_canvas_frame()

        self.current_piece = None
        self.next_piece = None        
        self.hold_piece = None   

        self.game_board =[0 for _ in range(Tetris.GAME_HEIGHT // Tetris.BOX_SIZE)]
        for i in range(len(self.game_board)):
            self.game_board[i]=[0 for _ in range(10)]
        
        
#         [[0] * ((Tetris.GAME_WIDTH - 20) // Tetris.BOX_SIZE)\
#                            for _ in range(Tetris.GAME_HEIGHT // Tetris.BOX_SIZE)]
        self.update_piece()
    def hold(self):
        self.hold_canvas.delete("all")
        if self.hold_piece==None:
            self.next_canvas.delete("all")
            self.hold_piece=self.current_piece
            self.current_piece.erase()
            self.current_piece = Piece(self.canvas, (Tetris.GAME_START_POINT, 0), self.next_piece.shape)
            self.next_piece = Piece(self.next_canvas, (20,20))
            
        else:
            temp=self.current_piece
            self.current_piece.erase()
            self.current_piece = Piece(self.canvas, (Tetris.GAME_START_POINT, 0), self.hold_piece.shape)
            self.hold_piece=temp
            
        self.hold_piece=Piece(self.hold_canvas, (20,20), self.hold_piece.shape)
        
        
        self.__draw_hold_canvas_frame()
        self.__draw_next_canvas_frame()
        
        
    def autodrop(self):
        self.auto_control(3)
        
        
        
    def play_sound(self):
        if queue_count <3:
            combo0.play()
        elif queue_count ==3:
            combo1.play()
        elif queue_count ==4:
            combo2.play()
        elif queue_count ==5:
            combo3.play()
        elif queue_count ==6:
            combo4.play()
        elif queue_count ==7:
            combo5.play()
        elif queue_count ==8:
            combo6.play()
        else:
            combo7.play()
    def update_piece(self):
        global actionlist_right,actionlist_rotate
        
        if len(actionlist_right) <=queue_count-1:
            self.end_game()
            return
        
        if self.first:
            self.fill_six()
            self.first=False
            self.hold_piece = Piece(self.next_canvas, (20,20))
            self.hold_piece=Piece(self.hold_canvas, (20,20), self.hold_piece.shape)
        else:
            print("drop")
            delay=randint(150,210)
            self.canvas.after(delay, self.play_sound)
            self.canvas.after(delay+100,self.autodrop)
            
        if not self.next_piece:
            self.next_piece = Piece(self.next_canvas, (20,20))
        self.current_piece = Piece(self.canvas, (Tetris.GAME_START_POINT, 0), self.next_piece.shape)
        self.next_canvas.delete("all")
        self.__draw_hold_canvas_frame()
        self.__draw_next_canvas_frame()
        self.next_piece = Piece(self.next_canvas, (20,20))
        self.update_predict()
        
        if path[queue_count-2][2]:
            self.auto_control(4)
        
        
        for i in range(actionlist_rotate[queue_count-2]):
            self.auto_control(0)
            
        for i in range(actionlist_right[queue_count-2]):
            self.auto_control(1)
            
        
        

        
    
    def start(self):
        global path,piece_queue,queue_count,actionlist_right,actionlist_rotate
        piece_queue=get_piece_queue()
        path=None
        actionlist_right=[]
        actionlist_rotate=[]
        
        for i in range(10):
            path=findpath(0,piece_queue)
            if not path:
                piece_queue=piece_queue[1:]
            else:
                break;
            
            
        
        
        if path!=False:
            for r in path:
                actionlist_rotate.append(r[3][0])
            for x in path:
                actionlist_right.append(x[3][1])
        print(actionlist_rotate)
            
        queue_count=-1
        self.new_game()
        self.root.after(self.speed, None)
        self.drop()
        
        
        
        
        
        
        self.root.mainloop()

    def drop(self):
        if not self.current_piece.move((0,1)):
            self.current_piece.remove_predicts()
            self.completed_lines()
            self.game_board = self.canvas.game_board()
            self.update_piece()

            if self.is_game_over():
                return
            else:
                self._blockcount += 1
                self.score += 1

        self.root.after(self.speed, self.drop)

    def hard_drop(self):
        self.current_piece.move(self.current_piece.predict_movement(self.game_board))

    def update_predict(self):
        if self.predictable:
            self.current_piece.predict_drop(self.game_board)

    def update_status(self):
        self.status_var.set(f"Level: {self.level}, Score: {self.score}")
        self.status.update()

    def is_game_over(self):
        if not self.current_piece.move((0,1)):

            self.play_again_btn = Button(self.root, text="Play Again", command=self.play_again)
            self.quit_btn = Button(self.root, text="Quit", command=self.quit) 
            self.play_again_btn.place(x = Tetris.GAME_WIDTH + 10, y = 200, width=100, height=25)
            self.quit_btn.place(x = Tetris.GAME_WIDTH + 10, y = 300, width=100, height=25)
            return True
        return False
    
    def end_game(self):
        print("endgame")
        self.play_again_btn = Button(self.root, text="Play Again", command=self.play_again)
        self.quit_btn = Button(self.root, text="Quit", command=self.quit) 
        self.play_again_btn.place(x = Tetris.GAME_WIDTH + 10, y = 200, width=100, height=25)
        self.quit_btn.place(x = Tetris.GAME_WIDTH + 10, y = 300, width=100, height=25)
    
    
    def play_again(self):
        self.play_again_btn.destroy()
        self.quit_btn.destroy()
        self.start()

    def quit(self):
        self.root.quit()     

    def completed_lines(self):
        y_coords = [self.canvas.coords(box)[3] for box in self.current_piece.boxes]
        
        #y_coords=[0]
        completed_line = self.canvas.completed_lines(y_coords)
        if completed_line == 1:
            self.score += 400
        elif completed_line == 2:
            self.score += 1000
        elif completed_line == 3:
            self.score += 3000
        elif completed_line >= 4:
            self.score += 12000

    def __game_canvas(self):
        self.canvas = GameCanvas(self.root, 
                             width = Tetris.GAME_WIDTH, 
                             height = Tetris.GAME_HEIGHT)
        
        
        
        
        self.canvas.pack(padx=5 , pady=10, side=LEFT)


    def __level_score_label(self):
        self.status_var = StringVar()        
        self.status = Label(self.root, 
                            textvariable=self.status_var, 
                            font=("Helvetica", 10, "bold"))
        #self.status.place(x = Tetris.GAME_WIDTH + 10, y = 100, width=100, height=25)
        self.status.pack()

    def __next_piece_canvas(self):
        self.next_canvas = Canvas(self.root,
                                 width = 100,
                                 height = 100)
        self.next_canvas.pack(padx=5 , pady=10)
        
    def __hold_piece_canvas(self):
        self.hold_canvas = Canvas(self.root,
                                 width = 100,
                                 height = 300)
        self.hold_canvas.pack(padx=5 , pady=10)

    def __draw_canvas_frame(self):
        self.canvas.create_line(10, 0, 10, self.GAME_HEIGHT, fill = "red", tags = "line")
        self.canvas.create_line(self.GAME_WIDTH-10, 0, self.GAME_WIDTH-10, self.GAME_HEIGHT, fill = "red", tags = "line")
        self.canvas.create_line(10, self.GAME_HEIGHT, self.GAME_WIDTH-10, self.GAME_HEIGHT, fill = "red", tags = "line")

    def __draw_next_canvas_frame(self):
        self.next_canvas.create_rectangle(10, 10, 90, 90, tags="frame")
    def __draw_hold_canvas_frame(self):
        self.hold_canvas.create_rectangle(10, 10, 90, 90, tags="frame")
    
    #set & get
    def __get_level(self):
        return self._level

    def __set_level(self, level):
        self.speed = 500 - (level - 1) * 25
        self._level = level
        self.update_status()

    def __get_score(self):
        return self._score

    def __set_score(self, score):
        self._score = score
        self.update_status()

    def __get_blockcount(self):
        return self._blockcount

    def __set_blockcount(self, blockcount):
        self.level = blockcount // 5 + 1
        self._blockcount = blockcount

    level = property(__get_level, __set_level)
    score = property(__get_score, __set_score)
    blockcount = property(__get_blockcount, __set_blockcount)

if __name__ == '__main__':
    game = Tetris(predictable = False)
    game.start()