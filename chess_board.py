from graphics import *

class Piece:
    def __init__(self,circle,color,location,user):
        self.circle = circle
        self.color = color
        self.location = location
        self.user = user
        

def chessBoard(size):
    win = GraphWin('chess_board',size*pts+2.25*pts,size*pts)
    win.setBackground('#CD853F')
    for i in range(size):
        x_line = Line(Point(0+pts/2,i*pts+pts/2),Point((size-1)*pts+pts/2,i*pts+pts/2))
        y_line = Line(Point(i*pts+pts/2,0+pts/2),Point(i*pts+pts/2,(size-1)*pts+pts/2))
        x_line.draw(win)
        y_line.draw(win)
        p1 = Point((size+1)*pts,pts)
        p2 = Point((size+1)*pts,(size-1)*pts)
        rec1 = Rectangle(Point(p1.x-pts/2-pts/4,p1.y-pts/2+pts/8),Point(p1.x+pts/2+pts/4,p1.y+pts/2-pts/8))
        rec2 = Rectangle(Point(p2.x-pts/2-pts/4,p2.y-pts/2+pts/8),Point(p2.x+pts/2+pts/4,p2.y+pts/2-pts/8))
        rec1.draw(win)
        rec2.draw(win)
        reput = Text(p1,'结束')
        reput.draw(win)
        renshu = Text(p2,'认输')
        renshu.draw(win)
    return win

def addPiece(player,center):
    color = players[player]
    cir = Circle(center,piece_radius)
    cir.setFill(color)
    cir.setOutline(color)
    cir.draw(win)
    user = getPiecePlayer(color)
    piece = Piece(cir,color,getPieceLocation(center),user)
    pieces[user].append(piece)
    return piece

def getLocationFromMouse(mouse):
    l = []
    for n in [mouse.x,mouse.y]:
        a = n//pts
        p = 0
        i = (n-pts/2)//pts
        if n>i*pts and n<(i+1)*pts:
            p = i*pts+pts/2
        else:
            p = (i+1)*pts+pts/2
        l.append(p)
    point = Point(l[0],l[1])
    return point

def getPieceLocation(p):
    l = []
    for x in [p.x,p.y]:
        l.append(int((x-pts/2)//pts))
    return tuple(l)

def getPiecePlayer(color):
    if color == 'black':
        return 0
    elif color == 'white':
        return 1
    else:
        return 'unknown'

def isLocationValid(mouse):
    if mouse.x>=(size)*pts:
        return False
    c = getPieceLocation(getLocationFromMouse(mouse))
    for user in pieces:
        for piece in user:
            if c == piece.location:
                return False
    return True

#def ifreput(m):
#    if m.x > (size+1)*pts-3*pts/4 and m.x < (size+1)*pts+3*pts/4 and m.y > 5*pts/8 and m.y < 11*pts/8:
#        return True
#    else:
#        return False

#def reput(user,np):
#    c = pieces[user][-1].circle.getCenter()
#    pieces[user][-1].circle.move(np.x-c.x,np.y-c.y)

def getPieceFromLocation(loc):
    for user in range(2):
     #   print(len(pieces[user]))
        for piece in pieces[user]:
         #   print(str(piece.location)+', '+str(loc))
            if piece.location == loc:
               # print(pieces[user].index(piece))
                return piece
    return None


def isInSquare(piece):
    x,y = piece.location[0],piece.location[1]
    user = piece.user
    neb = [
        getPieceFromLocation((x,y-1)),
        getPieceFromLocation((x,y+1)),
        getPieceFromLocation((x+1,y)),
        getPieceFromLocation((x-1,y)),
        getPieceFromLocation((x-1,y-1)),
        getPieceFromLocation((x+1,y-1)),
        getPieceFromLocation((x-1,y+1)),
        getPieceFromLocation((x+1,y+1)),
        ]
    if x==0:
        if y==0:
        # 左上角
            ifsquare = [1,7,2]
            s = user
            for i in ifsquare:
                if neb[i]==None:
                    return 0,0
                else:
                    s += neb[i].user
                #    print("s="+str(s/4))
            return int(bool(s/4==user)),0
        elif y==size-1:
        # 左下角
            ifsquare = [0,5,2]
            s = user
            for i in ifsquare:
                if neb[i]==None:
                   return 0,0
                else:
                    s += neb[i].user
                  #  print("s="+str(s))
            return int(bool(s/4==user)),0

        else:
        # 左边
            ifsquare = [0,5,2,7,1]
            s1,s2 = user,user
            for i in range(3):
                s1 += 5 if neb[ifsquare[i]]==None else neb[ifsquare[i]].user
                s2 += 5 if neb[ifsquare[-i-1]]==None else neb[ifsquare[-(i+1)]].user
            s1 = s1/4
            s2 = s2/4
          #  print("s1="+str(s1)+",s2="+str(s2))
            if s1==user and s2==user:
                return 1,1
            elif s1==user or s2==user:
                return 1,0
            else:
                return 0,0
    elif x==size-1:
        if y==0:
        # 右上角
            ifsquare = [3,6,1]
            s = user
            for i in ifsquare:
                if neb[i]==None:
                    return 0,0
                else:
                    s += neb[i].user
         #   print("s="+str(s))
            return int(bool(s/4==user)),0
        elif y==size-1:
        # 右下角
            ifsquare = [0,4,3]
            s = user
            for i in ifsquare:
                if neb[i]==None:
                    return 0,0
                else:
                    s += neb[i].user
             #   print("s="+str(s))
            return int(bool(s/4==user)),0

        else:
        # 右边
            ifsquare = [0,4,3,6,1]
            s1,s2 = user,user
            for i in range(3):
                s1 += 5 if neb[ifsquare[i]]==None else neb[ifsquare[i]].user
                s2 += 5 if neb[ifsquare[i+2]]==None else neb[ifsquare[i+2]].user
            s1 = s1/4
            s2 = s2/4
          #  print("s1="+str(s1)+",s2="+str(s2))
            if s1==user and s2==user:
                return 1,1
            elif s1==user or s2==user:
                return 1,0
            else:
                return 0,0
    else:
        if y==0:
        # 上边
            ifsquare = [3,6,1,7,2]
            s1,s2 = user,user
            for i in range(3):
                s1 += 5 if neb[ifsquare[i]]==None else neb[ifsquare[i]].user
                s2 += 5 if neb[ifsquare[i+2]]==None else neb[ifsquare[i+2]].user
            s1 = s1/4
            s2 = s2/4
         #   print("s1="+str(s1)+",s2="+str(s2))
            if s1==user and s2==user:
                return 1,1
            elif s1==user or s2==user:
                return 1,0
            else:
                return 0,0
        elif y==size-1:
        # 下边
            ifsquare = [3,4,0,5,2]
            s1,s2 = user,user
            for i in range(3):
                s1 += 5 if neb[ifsquare[i]]==None else neb[ifsquare[i]].user
                s2 += 5 if neb[ifsquare[-i-1]]==None else neb[ifsquare[-(i+1)]].user
            s1 = s1/4
            s2 = s2/4
         #   print("s1="+str(s1)+",s2="+str(s2))
            if s1==user and s2==user:
                return 1,1
            elif s1==user or s2==user:
                return 1,0
            else:
                return 0,0
        else:
            ifsquare = [0,4,3,6,1,7,2,5,0]
            s1,s2,s3,s4 = user,user,user,user
            for i in range(3):
                s1 += 5 if neb[ifsquare[i]]==None else neb[ifsquare[i]].user
                s2 += 5 if neb[ifsquare[i+2]]==None else neb[ifsquare[i+2]].user
                s3 += 5 if neb[ifsquare[i+4]]==None else neb[ifsquare[i+4]].user
                s4 += 5 if neb[ifsquare[i+6]]==None else neb[ifsquare[i+6]].user
            s1 = s1/4
            s2 = s2/4
            s3 = s3/4
            s4 = s4/4
        #    print("s1="+str(s1)+",s2="+str(s2)+",s3="+str(s3)+",s4="+str(s4))
            if (s1==user and s2==user) or (s2==user and s3==user) or (s3==user and s4==user) or (s4==user and s1==user):
                return 1,1
            elif s1==user or s2==user or s3==user or s4==user:
                return 1,0
            else:
                return 0,0

def isAline(piece):
    x,y = piece.location
    for i in range(10):
        l1 = (i,y)
        l2 = (x,i)
        for l in [l1,l2]:
            p = getPieceFromLocation(l)
            if p==None:
                return 0
            elif p.user!=piece.user:
                return 0
            else:
                pass
    return 1

def deletePiece(piece):
    piece.circle.undraw()
    u = piece.user
    i=0
    for x in pieces[u]:
        if x.location==piece.location:
            del pieces[u][i]
            return
        i += 1
            
def selectPieceToDelete(user):
    loc = getPieceLocation(getLocationFromMouse(win.getMouse()))
    print(loc)
    p = getPieceFromLocation(loc)
    while p == None or bool(sum(isInSquare(p))) or p.user==user:
        print("an invalid piece to delete, please select another")
        print(p)
        if p!=None:
            print(str(p.user)+','+str(user))
            print(isInSquare(p))
        loc = getPieceLocation(getLocationFromMouse(win.getMouse()))
        p = getPieceFromLocation(loc)
    return p


pts = 30
size = 6
piece_radius = 3*pts//8
players={0:'black',1:'white'}
win = chessBoard(size)
pieces = [[],[]]

while True:
    for user in range(2):
        mouse = win.getMouse()
        while not isLocationValid(mouse):
            mouse = win.getMouse()
        piece = addPiece(user,getLocationFromMouse(mouse))
      #  print('location: '+str(piece.location)+', player: '+str(user))
      #  print(str(isInSquare(piece)))
        n = sum(isInSquare(piece))+isAline(piece)
#        for i in range(n):
#            print("Plise select "+str(n)+" pieces of opponent to delete")
#            p = selectPieceToDelete(user)
#            deletePiece(p)
        
                
    if len(pieces[0])+len(pieces[1])==size**2:
        for a in range(size**2):
            for u in range(2):
                print(u)
                deletePiece(selectPieceToDelete(u))
        break
win.getMouse()



