from graphics import *
import time

class Piece:
    def __init__(self,circle,color,location,user):
        self.circle = circle
        self.color = color
        self.location = location
        self.user = user
    def Move(self):
        circle = self.circle
        location = self.location
        center = circle.getCenter()
        while True:
            mouse = win.getMouse()
            m_location = getPieceLocation(getLocationFromMouse(mouse))
            if m_location == location:
                return 0
            x_loc,y_loc = m_location[0] , m_location[1]
            x_pie,y_pie = location[0] , location[1]
            if getPieceFromLocation(m_location) != None:
                continue
            if x_loc != x_pie and y_loc != y_pie:
                print('    不能同时移动两个方向：'+str(location)+','+str(m_location))
                continue
            elif y_loc == y_pie:
                a = 0
                mid_n = abs(x_loc - x_pie) - 1
                mid_loc = [x+1+min(x_loc,x_pie) for x in range(mid_n+1)]
                for x_mid in mid_loc[0:mid_n]:
                    if piece_pan[x_mid][y_loc] != -1:
                    #    print(piece_pan[x_mid][y_mid])
                        print('    不能跨越其他棋子走棋或走棋位置与其他棋子重叠：'+str(location)+','+str(m_location))
                        a = 1
                        break
                if a == 1:
                    continue
            elif x_loc == x_pie:
                a = 0
                mid_n = abs(y_loc - y_pie) - 1
                mid_loc = [x+1+min(y_loc,y_pie) for x in range(mid_n+1)]
                for y_mid in mid_loc[0:mid_n]:
                    if piece_pan[x_loc][y_mid] != -1:
                        print('    不能跨越其他棋子走棋或走棋位置与其他棋子重叠：'+str(location)+','+str(m_location))
                        a = 1
                        break
                if a == 1:
                    continue
            break
        x,y = (x_loc - x_pie)*pts , (y_loc - y_pie)*pts
        self.circle.move(x,y)
        piece_pan[x_pie][y_pie] = -1
        piece_pan[x_loc][y_loc] = self.user
        self.location = m_location
        circle.setOutline(players[self.user])
        print("    移动："+str(location)+"-->"+str(m_location))
        gun(self)
        return 1

def chessBoard(size):
    win = GraphWin('丢方',size*pts+2.25*pts,size*pts)
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
#    user = getPiecePlayer(color)
    loc = getPieceLocation(center)
    piece = Piece(cir,color,loc,player)
    pieces[player].append(piece)
    piece_pan[loc[0]][loc[1]] = player
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

def deletePiece(piece):
    piece.circle.undraw()
    u = piece.user
    loc = piece.location
    i=0
    for x in pieces[u]:
        if x.location==loc:
            del pieces[u][i]
            piece_pan[loc[0]][loc[1]] = -1
            return
        i += 1
            
def selectPieceToDelete(user):
    while True:
        loc = getPieceLocation(getLocationFromMouse(win.getMouse()))
        p = getPieceFromLocation(loc)
        if p != None:
            if not bool(sum(isInSquare(p))) and p.user != user:
                break
            else:
                print("    选择错误，请重新选择")
        else:
            print("    NONE")
    print("    选择删除"+str(p.location))
    return p
    
def deletablePieces(user):
    x = 0
    for p in pieces[user]:
        if sum(isInSquare(p))==0:
            x += 1
    return x

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
        for i in range(k+1):
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
        for i in range(k+1):
            p1 = getPieceFromLocation((x-1-l-i,y))
            todel3.append(p1)
            p2 = getPieceFromLocation((x+1+r+i,y))
            todel4.append(p2)
    todel = []
    for dellist in [todel1,todel2,todel3,todel4]:
        nu = len(dellist)
        if nu>1:
            isdel = True
            for p1 in dellist[0:nu-1]:
                if p1 == None:
                    isdel = False
                    break
                else:
                    if p1.user == user:
                        isdel = False
                        break
            if dellist[-1] != None:
                if dellist[nu-1].user != user:
                    isdel = False
            if isdel == True:
                print('    '+str(nu-1)+' 枪')
                todel += dellist[0:nu-1]
    if len(todel)>1:
        for p1 in todel:
            p1.circle.setFill('red')
            p1.circle.setOutline('red')
        time.sleep(0.25)
        for p1 in todel:
            p1.circle.setFill(players[1 if user==0 else 0])
            p1.circle.setOutline(players[1 if user==0 else 0])
        time.sleep(0.25)
        for p1 in todel:
            p1.circle.setFill('red')
            p1.circle.setOutline('red')
        time.sleep(0.25)
        for p1 in todel:
            deletePiece(p1)

def isFull():
    n = len(pieces[0]) + len(pieces[1])
    if n < size**2:
        return False
    else:
        return True

def isSomeoneWin():
    n0 = len(pieces[0])
    n1 = len(pieces[1])
    iswin = False
    winner = -1
    if n0*n1==0:
        iswin = True
    if n0 == 0:
        winner = 1
    else:
        winner = 0
    return iswin,winner

def isMovable(user):
    ismovable = 0
    for p in pieces[user]:
        x,y = p.location
        for loc in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if loc[0] < 0 or loc[1] < 0 or loc[0] >= size or loc[1] >= size:
                continue
            p0 = getPieceFromLocation(loc)
            
            if p0 == None:
                ismovable = 1
                break
        if ismovable ==1:
            break
    print('    '+str(ismovable))
    return ismovable

def main():
    '''
    ------------------------------------------------------------
    |                    第一阶段，落子阶段                    |
    ------------------------------------------------------------
    '''
    first_square = -1
    print('开始下棋')
    user = 0
    while True:
        print(('黑' if user==0 else '白')+'请:')
        if isFull():
            break
        while True:
            mouse = win.getMouse()
            if isLocationValid(mouse):
                break
        piece = addPiece(user,getLocationFromMouse(mouse))
    
        sq = sum(isInSquare(piece))
        le = isAline(piece)
        if first_square==-1:
            if sq!=0:
                first_square = user
        print('    位置: '+str(piece.location))
        print('    成方' if sq != 0 else '    未成方')
        print('    成行' if le != 0 else '    未成行')
        n = sq + le

        if isFull():
            break
        else:
            if n>0:
                print('    请继续下 '+str(n)+' 颗棋子')
                i=0
                while i<n:
                    if isFull():
                        break
                    while True:
                        mouse = win.getMouse()
                        if isLocationValid(mouse):
                            break
                    piece = addPiece(user,getLocationFromMouse(mouse))
                    i = i + 1
                    i = i - (sum(isInSquare(piece)) + isAline(piece))
                    if n-i>0:
                        print('    请继续下 '+str(n-i)+' 颗棋子')
        user = user ^ 1
    '''
    -------------------------------------------------------------------
    |                       第二阶段，走子阶段                        |
    -------------------------------------------------------------------
    '''
    print('双方各先吃掉对方一颗未成方的棋子')
    if first_square == -1:
        first_square = 0
    iswin = 0
    for user in [first_square,first_square ^ 1]:
        print(('黑' if user==0 else '白')+'请:')
        user2 = 1 if user==0 else 1
        num = deletablePieces(user2)
        if num==0:
            iswin = 1
            print("黑棋" if user2==0 else "白棋"+"获胜")
            break
        else:
            p = selectPieceToDelete(user)
            deletePiece(p)
    if iswin ==1:
        return

    print('开始走棋')
    user = first_square
    while True:
        user2 = user ^ 1
        print(('黑' if user==0 else '白')+'请:')
        if isMovable(user)<1:
            print("黑棋" if user2==0 else "白棋"+"获胜")
            break
        while True:
            mouse = win.getMouse()
            loc = getPieceLocation(getLocationFromMouse(mouse))
            piece = getPieceFromLocation(loc)
            if piece == None:
                continue
            else:
                if piece.user != user:
                    print('    不能移动对方的棋子')
                    continue
            piece.circle.setOutline('red')
            if piece.Move()==0:
                piece.circle.setOutline(players[user])
                continue
            else:
                break
        sq = sum(isInSquare(piece))
        le = isAline(piece)
        print('    成方' if sq != 0 else '    未成方')
        print('    成行' if le != 0 else '    未成行')
        num=deletablePieces(user2)
        n=min(sq+le,num)
        if n>0:
            if num==0:
                print('    对方没有可以吃掉的棋子')
            else:
                print('    请吃掉对方 '+str(n)+' 颗棋子')
                for i in range(n):
                    print('    第 '+str(i+1)+' 颗')
                    p = selectPieceToDelete(user)
                    deletePiece(p)
        iswin , winner = isSomeoneWin()
        if iswin:
            print(('黑棋' if winner==0 else '白棋')+'获胜')
            break
        user = user ^ 1


#        '''
#        -----------------------------------------------------------------
#        |                         清空棋盘                              |
#        -----------------------------------------------------------------
#        '''
#    for piece in pieces[winner]:
#        deletePiece(piece)
#
#win.getMouse()

pts = 50
size = 6
piece_radius = 3*pts//8
players={0:'black',1:'white'}
win = chessBoard(size)
pieces = [[],[]]
piece_pan = [[-1 for x in range(size)] for x in range(size)]
 
while True:
    print(str(pieces))
    print(str(piece_pan))
    main()
    for user in range(2):
        for piece in pieces[user]:
            print(piece.user)
            print(piece.color)
            deletePiece(piece)





