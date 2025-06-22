_B=False
_A=True
import random as rd,time
class Bot:
 WINNING_LINES=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];INF=1000000;turn_number=1;calculated_max=dict();calculated_min=dict();player_num={' ':-1};hashes=[[[rd.randint(1,0x7fffffffffffffff)for A in range(9)]for A in range(4)]for A in range(2)]
 def get_top_cup(A,cell):return cell[-1]
 def parse_pieces(E,pieces_str):
  D=pieces_str;A=[0,0,0,0]
  for B in D.split(',')[0][1:]:A[int(B)]+=1
  C=[0,0,0,0]
  for B in D.split(',')[1][1:]:C[int(B)]+=1
  return[A,C]if E.player=='X'else[C,A]
 def parse_board(E,board_arr):
  C=[]
  for A in board_arr:
   D=[]
   for B in range(len(A),0,-2):D.append((E.player_num[A[B-2]],0 if A[B-1]==' 'else int(A[B-1])))
   C.append(D)
  return C
 def has_piece(A,player,size):return A.pieces[player][size]>0
 def can_place(A,pos,size):B=A.get_top_cup(A.board[pos]);return B[1]<size
 def generate_legal_moves(A,player,maximizing,hash):
  H=maximizing;C=player;E=[];I=[0]*9
  for F in A.WINNING_LINES:
   for B in F:
    J=A.board[B]
    if J[-1][0]==C:I[B]+=4
    elif J[-1][1]>0 and J[-1][0]!=C:I[B]-=3
  M=A.calculated_max if H else A.calculated_min
  for D in[3,2,1]:
   if not A.has_piece(C,D):continue
   for K in range(9):
    if A.can_place(K,D):L=A.hashes[C][D][K];E.append((D,K,L))
  Q=1-C
  for B in range(9):
   N=A.get_top_cup(A.board[B])
   if N[0]!=C:continue
   O=_B
   for F in A.WINNING_LINES:
    if B not in F:continue
    if all(A.board[C][-2 if B==C else-1]==Q for C in F):O=_A
   if O:continue
   D=N[1]
   for G in range(9):
    if B==G:continue
    if A.can_place(G,D):L=A.hashes[C][D][B]^A.hashes[C][D][G];E.append((90+B,G,L))
  P=-1 if H else 1;E.sort(key=lambda x:-P*(I[x[1]]+(2 if x[0]<=3 else 0))+(M[hash^x[2]][0]if hash^x[2]in M else-P*.5*A.INF),reverse=H);return E
 def simulate_move(A,move,player):
  C=player;B,D,G=move
  if B<=3:E=B;A.board[D].append((C,E));A.pieces[C][E]-=1
  else:F=B%10;A.board[D].append(A.board[F].pop())
 def undo_move(A,move,player):
  B,C,F=move
  if B<=3:D=B;A.board[C].pop();A.pieces[player][D]+=1
  else:E=B%10;A.board[E].append(A.board[C].pop())
 def is_end(A,turn_number):
  if turn_number>=30:return _A
  for B in A.WINNING_LINES:
   if A.board[B[0]][-1][0]<0:continue
   C=_A
   for D in B:
    if A.board[B[0]][-1][0]!=A.board[D][-1][0]:C=_B
   if C:return _A
  return _B
 def evaluate(B,cur_player,turn_number):
  P=turn_number;L=cur_player;C=0
  if P>=30 and L==0:return B.INF
  if P>=30 and L==1:return-B.INF
  for G in B.WINNING_LINES:
   S=[B.board[A][-1]for A in G]
   if all(A[0]==0 for A in S):return B.INF-P
   if all(A[0]==1 for A in S):C=-B.INF
  M=[[1,1]for A in range(9)];D=[[0,0,0,0],[0,0,0,0]]
  for G in B.WINNING_LINES:
   H,I=0,0
   for A in G:
    J=B.board[A]
    if J[-1][0]==0:H+=1
    elif J[-1][0]==1:I+=1
   for A in G:
    if J[-1][0]==0:Q=1 if J[-2][0]==1 else 0;M[A][0]*=[1,.85,.3,0][I+Q]
    elif J[-1][0]==1:Q=1 if J[-2][0]==0 else 0;M[A][1]*=[1,.85,.3,0][H+Q]
  for A in range(1,4):D[0][A]=B.pieces[0][A];D[1][A]=B.pieces[1][A]
  for A in range(9):
   E,F=B.board[A][-1]
   if F>0:D[E][F]+=M[A][E]
  K=[[0,0]for A in range(9)];R=2 if 0==L else 1;T=3-R
  for G in B.WINNING_LINES:
   N=R;O=T;I=0;H=0
   for A in G:
    E,F=B.board[A][-1]
    if F>0:D[E][F]-=M[A][E]
   for A in G:
    E,F=B.board[A][-1]
    if E!=1:
     O*=max(0,min(1,sum(D[1][F+1:])-I));I+=1
     if I==2:O*=.1
    if E!=0:
     N*=max(0,min(1,sum(D[0][F+1:])-H));H+=1
     if H==2:N*=.1
   if O>1e-05 and I==1 and L==1:C-=10000
   if N>1e-05 and H==1 and L==0:C+=10000
   for A in G:
    if O>1e-05 and I<3 and B.board[A][-1][0]!=1:K[A][1]+=1
    if N>1e-05 and H<3 and B.board[A][-1][0]!=0:K[A][0]+=1
   C+=100*N;C-=100*O
   for A in G:
    E,F=B.board[A][-1]
    if F>0:D[E][F]+=M[A][E]
  for A in range(9):
   if K[A][0]>=2:C+=R*30*3**(K[A][0]-1)
   if K[A][1]>=2:C-=T*30*3**(K[A][1]-1)
  if B.board[4][-1][0]==0:C+=5*B.board[4][-1][1]
  if B.board[4][-1][0]==1:C-=5*B.board[4][-1][1]
  C+=60*D[0][3];C+=40*D[0][2];C+=20*D[0][1];C-=60*D[1][3];C-=40*D[1][2];C-=20*D[1][1];return C*rd.uniform(.9,1.1)if B.player=='O'else C
 def pvs(A,depth,alpha,beta,maximizing,turn_number,hash):
  I=None;G=maximizing;F=turn_number;E=depth;D=beta;C=alpha;J=A.calculated_max if G else A.calculated_min
  if hash in J:
   P,Q,R=J[hash]
   if R>=E:return P,Q
  if E==0 or A.is_end(F):eval=A.evaluate(0 if G else 1,F);J[hash]=eval,I,E;return eval,I
  M=A.generate_legal_moves(0 if G else 1,G,hash)
  if not M:eval=A.evaluate(0 if G else 1,F);J[hash]=eval,I,E;return eval,I
  K=I;L=_A
  if G:
   N=float('-inf')
   for B in M:
    A.simulate_move(B,0)
    if L:eval,H=A.pvs(E-1,C,D,_B,F+1,hash^B[2]);L=_B
    else:
     eval,H=A.pvs(E-1,C,C+1,_B,F+1,hash^B[2])
     if C<eval<D:eval,H=A.pvs(E-1,C,D,_B,F+1,hash^B[2])
    A.undo_move(B,0)
    if eval>N:N=eval;K=B
    C=max(C,eval)
    if D<=C:break
   return N,K
  else:
   O=float('inf')
   for B in M:
    A.simulate_move(B,1)
    if L:eval,H=A.pvs(E-1,C,D,_A,F+1,hash^B[2]);L=_B
    else:
     eval,H=A.pvs(E-1,D-1,D,_A,F+1,hash^B[2])
     if C<eval<D:eval,H=A.pvs(E-1,C,D,_A,F+1,hash^B[2])
    A.undo_move(B,1)
    if eval<O:O=eval;K=B
    D=min(D,eval)
    if D<=C:break
   return O,K
 def get_move(A,board,peices,player):
  E=peices;C=player;A.player=C;A.player_num[C]=0;A.player_num['O'if C=='X'else'X']=1;A.pieces=A.parse_pieces(E);A.board=A.parse_board(board);A.turn_number=16-len(E)
  if A.turn_number==1:return'3 4'
  B=3;G=time.time()
  while _A:
   eval,D=A.pvs(B,alpha=float('-inf'),beta=float('inf'),maximizing=_A,turn_number=A.turn_number,hash=0);F=time.time()-G
   if F>=.3 or eval>A.INF*.5:break
   B+=1
   if B+A.turn_number>=30:break
  if D:return f"{D[0]} {D[1]}"
  else:return