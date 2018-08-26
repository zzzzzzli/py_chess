from graphics import *
import time

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
    gun(piece)
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
        for piece in pieces[user]:
            if piece.location == loc:
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
    x1, y1 = 0, 0
    for i in range(10):
        p1 = getPieceFromLocation((i,y))
        p2 = getPieceFromLocation((x,i))
        if p1 != None:
            x1 += p1.user==piece.user
        if p2 != None:
            y1 += p2.user==piece.user
    if x1 == size or y1 == size:
        return 1
    else:
        return 0

def deletablePiece(user):
    piece = []
    for p in pieces[user]:
        if not isInSquare(p):
            piece.append(p)
    return piece


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
    p = getPieceFromLocation(loc)
    while p == None or bool(sum(isInSquare(p))) or p.user==user:
        print("\tan invalid piece to delete, please select another")
#        if p!=None:
#            print(str(p.user)+','+str(user))
#            print(isInSquare(p))
        loc = getPieceLocation(getLocationFromMouse(win.getMouse()))
        p = getPieceFromLocation(loc)
    return p

def deletablePieces(user):
    px = []
    for p in pieces[user]:
        if not sum(isInSquare(p))!=0:
            px.append(p)
    return px

def gun(piece):
    user=piece.user
    (x,y)=piece.location
    u=0
    while True:
        # up
        p=getPieceFromLocation((x,y-1-u))
        if p!=None:
            if p.user == user:
                u += 1
            else:
                break
        else:
            break
    d=0
    while True:
        # down
        p=getPieceFromLocation((x,y+1+d))
        if p!=None:
            if p.user== user:
                d += 1
            else:
                break
        else:
            break
    k = u + d + 1
    todel1 = []
    todel2 = []
    if k>1 and k<=size//2:
        for i in range(k):
            p1 = getPieceFromLocation((x,y-1-u-i))
            todel1.append(p1)
            p2 = getPieceFromLocation((x,y+1+d+i))
            todel2.append(p2)
    ################################################

    l=0
    while True:
        # left
        p=getPieceFromLocation((x-1-l,y))
        if p!=None:
            if p.user == user:
                l += 1
            else:
                break
        else:
            break
    r=0
    while True:
        # right
        p=getPieceFromLocation((x+1+r,y))
        if p!=None:
            if p.user== user:
                r += 1
            else:
                break
        else:
            break
    k = l + r + 1
    todel3 = []
    todel4 = []
    if k>1 and k<=size//2:
        for i in range(k):
            p1 = getPieceFromLocation((x-1-l-i,y))
            todel3.append(p1)
            p2 = getPieceFromLocation((x+1+r+i,y))
            todel4.append(p2)
    todel = []
    for dellist in [todel1,todel2,todel3,todel4]:
        if len(dellist)>0:
            isdel = True
            for p1 in dellist:
                if p1 == None:
                    isdel = False
                    break
                else:
                    if p1.user == user:
                        isdel = False
                        break
            if isdel == True:
                todel += dellist
    if len(todel)>1:
        for p1 in todel:
            p1.circle.setFill('red')
            p1.circle.setOutline('red')
        time.sleep(0.5)
        for p1 in todel:
            p1.circle.setFill(players[1 if user==0 else 0])
            p1.circle.setOutline(players[1 if user==0 else 0])
        time.sleep(0.5)
        for p1 in todel:
            p1.circle.setFill('red')
            p1.circle.setOutline('red')
        time.sleep(0.5)
        for p1 in todel:
            deletePiece(p1)



pts = 30
size = 6
piece_radius = 3*pts//8
players={0:'black',1:'white'}
win = chessBoard(size)
pieces = [[],[]]

while True:
    for user in range(2):
        print(players[user]+' please:')
        while True:
            mouse = win.getMouse()
            if isLocationValid(mouse):
                break
        piece = addPiece(user,getLocationFromMouse(mouse))
        sq = sum(isInSquare(piece))
        le = isAline(piece)
        print('\tlocation: '+str(piece.location))
        print('\tis square' if sq != 0 else '\tis not square')
        print('\tis a line 'if le != 0 else '\tis not a line')
        n = sq + le
        if n>0:
            print('\tyou can put another '+str(n)+(' pieces' if n>1 else ' piece'))
            i=0
            while i<n:
                while True:
                    mouse = win.getMouse()
                    if isLocationValid(mouse):
                        break
                piece = addPiece(user,getLocationFromMouse(mouse))
                i = i +1
                i = i - (sum(isInSquare(piece)) + isAline(piece))
                if n-i>0:
                    print('\tput another '+str(n-i)+(' pieces' if (n-i)>1 else ' piece'))
                
        
#        user2 = 1 if user==0 else 1
#        delpieces=deletablePieces(user2)
#        num = len(delpieces)
#        n=min(sq+le,num)
#        if n>0:
#            if num==0:
#                print('\topponent has no piece to eat')
#            else:
#                print('\tyou have '+str(n)+' opponent pieces to eat')
#                for i in range(n):
#                     print('\tthe '+str(i+1))
#                     p = selectPieceToDelete(user)
#                     deletePiece(p)
        
                
    if len(pieces[0])+len(pieces[1])==size**2:
        for a in range(size**2):
            for u in range(2):
                print(u)
                deletePiece(selectPieceToDelete(u))
        break
win.getMouse()



