import pyperclip as pc
def amhgqn():
    s = '''
data = np.array(list(map(int, "цифры".split(', '))))
A = data[data != 0].mean()
M = np.median(data[data != 0])
H = hmean(data[data >= M])
G = gmean(data[data >= M])
Q = np.median(data[data >= M])
N = len(data[(data >= H) & (data <= Q)])
    '''
    return pc.copy(s)
    
def zpawxy():
    s = '''
x = np.array((...))
y = np.array((...))
stdX = 0.8
stdY = 1.4
alpha = 0.03
d = 0.6
z = (X.mean() - Y.mean()) / (stdX**2 / len(X) + stdY**2 / len(Y))**0.5
Z = norm(0, 1)
P = Z.sf(z)
A = Z.isf(alpha) # (1.88; inf) => H0 не отвергается
def F0(x):
    return norm(0, 1).cdf(x) - 1/2
W = 1/2 - F0(Z.isf(alpha) - (len(X)*len(Y))**0.5 / (len(Y)*stdX**2 + stdY**2*len(X))**0.5 * d)
    '''
    return pc.copy(s)
    
def lnl(): #ответ хз
    s = '''
data = pd.read_csv('ds6.4.12.csv', header=None, decimal=',', sep=';',encoding='cp1251')
X = data[0]
Y = data[1]
m1 = X.mean()
m2 = Y.mean()
n = len(data[0])
ro, s = symbols('rho sigma')
f = -n*log(2*pi) - n/2*log(1 - ro**2) - n*log(s**2) - np.sum((X - m1)**2 - 2*ro*(X - m1)*(Y - m2) + (Y - m2)**2) / (2 * s**2 * (1 - ro**2))
print(f)
f1 = simplify(diff(f, ro))
f2 = simplify(diff(f, s))
solve([f1, f2], [ro, s])
    '''
    return pc.copy(s)

def tabl_chast():
    s = '''
xk = np.array([200, 400])
xp = np.array([18+13+17, 13+16+23])/100
X = rv_discrete(name='custm', values=(xk, xp))
yk = np.array([1, 2, 4])
yp = np.array([18+13, 13+16, 17+23])/100
Y = rv_discrete(name='custm', values=(yk, yp))
xyk = np.array([200, 400, 800, 1600])
xyp = np.array([18, 13+13, 17+16, 23])/100
XY = rv_discrete(name='custm', values=(xyk, xyp))
N = 100
n = 14
print(X.mean())
print(VarY = (Y.var()/n * (N-n)/(N-1)))
covXY = XY.mean() - X.mean()*Y.mean()
covXY_hat = covXY/n * (N-n)/(N-1)
stdX = (X.var()/n * (N-n)/(N-1))**0.5
stdY = (Y.var()/n * (N-n)/(N-1))**0.5
print(covXY_hat/(stdX*stdY))
    '''
    return pc.copy(s)

def tapw():
    s = '''
X = np.array((...))
mu0 = 1.45
alpha = 0.04
mu1 = 1.34
n = len(X)
t_stat = (X.mean() - mu0)/X.std(ddof=1) * n**0.5
print(t_stat)
T = t(n-1)
print(T.isf(alpha/2)) # (-inf; -2.204) U (2.204; inf)
print(min(T.cdf(t_stat), T.sf(t_stat))*2) # PV
delta = n**0.5 * (mu1 - mu0) / X.std(ddof=1)
NCT = nct(n-1, delta)
print(1 - (NCT.cdf(T.isf(alpha/2)) - NCT.cdf(-T.isf(alpha/2)))) # W
    '''
    return pc.copy(s)


def ro_theta():
    s = '''
X = np.array((...))
Y = np.array((...))
alpha = 1 - 0.73
n = len(X)
covXY = np.cov(X, Y)[0, 1]
ro = covXY/(X.var(ddof=1) * Y.var(ddof=1))**0.5
print(ro)
tetha1 = math.tanh(math.atanh(ro) - 1/(n-3)**0.5 * norm(0, 1).isf(alpha/2))
tetha2 = math.tanh(math.atanh(ro) + 1/(n-3)**0.5 * norm(0, 1).isf(alpha/2))
print(tetha2)
    '''
    return pc.copy(s)

def raspr_ballov():
    s = '''
N = sum([80, 12, 55, 56])
n = N/7
X = rv_discrete(values=([2, 3, 4, 5], np.array([80, 12, 55, 56])/N))
print(X.mean())
print((X.var()/n * (N-n)/(N-1))**0.5)
    '''
    return pc.copy(s)

def red_blue():
    s = '''
X = np.array([15*r - 7*b for r in range(1, 7) for b in range(1, 7)])
print(X.mean())
N = X.shape[0]
n = 11
print((X.var()/n * (N-n)/(N-1))**0.5)
    '''
    return pc.copy(s)

def omega_var_m3():
    s = '''
X = np.array(list(map(int, "...".split(', '))))
N = len(X)
n = 6
print(X.var()/n)
print(np.sum((X-X.mean())**3)/n**2/N)
    '''
    return pc.copy(s)
def f_f():
    s = '''
sample = np.array((157, 1170, 149, -305, 1120, 410, 645, -453, -141, 306, -294, -284, -509, 408, -726, -425, 410, 271, 331, 81, 135, -488, 866, -561, 302, 240, -211, -328, -192, 573, -34, -125, 720, -916, 572, 547, 37, 482))
print(sample.mean(), sample.std())
N = norm(sample.mean(), sample.std())
L = N.ppf(0.25)
H = N.isf(0.25)
print(L, H)
print(len(sample[(sample >= L) & (sample <= H)]))
xk, xp = np.unique(sample, return_counts=True)
xp = xp/sum(xp)
F = rv_discrete(values=(xk, xp))
print(max([abs(F.cdf(x) - N.cdf(x)) for x in sample]))    
    '''
    return pc.copy(s)
def omega_e_var():
    s = '''
X = np.array((86, 62, 66, 100, 26, 0, 73, 87, 80, 78, 65, 55, 9, 3, 31, 79, 86, 73, 19, 89, 74, 88, 63, 55, 51, 77, 63))
N = 27
n = 7
print(X.mean())
print(X.var()/n * (N-n)/(N-1))
    '''
    return pc.copy(s)
def fin_pok():
    s = '''
A = np.array()
B = np.array()
C = np.array()
na = len(A)
nb = len(B)
nc = len(C)
ABC = np.concatenate([A, B, C])
n = [na, nb, nc]
N = sum(n)
k = 3
alpha = 0.01
muabc = data.mean()
varabc = data.var(ddof=0)
mu0 = np.concatenate([A, B, C]).mean()
d2 = ((A.mean() - ABC.mean())**2 * len(A) + (B.mean() - ABC.mean())**2 * len(B) + (C.mean() - ABC.mean())**2 * len(C))/len(ABC)
meanvar = (A.var(ddof=0) * len(A) + B.var(ddof=0) * len(B) + C.var(ddof=0) * len(C)) / len(ABC)
SSE = N * meanvar
MSE = SSE / (N - k)
SSTR = N * d2
MSTR = SSTR / (k - 1)
F = MSTR / MSE
K = f(k - 1, N - k).isf(alpha)#Ka=(K,+inf)
pv = f(k - 1, N - k).sf(F)
d2, meanvar,F,K,pv
    '''
    return pc.copy(s)
def fin_pok_file():
    s = '''
data = pd.read_csv('ds5.9.8.csv', header=None, decimal=',', sep=';',encoding='cp1251')
A, B, C = data[0], data[1], data[2]
A,B,C = A.dropna(),B.dropna(), C.dropna()
ABC = np.concatenate([A, B, C])
na,nb,nc = len(A),len(B),len(C)
n = [na, nb, nc]
N = sum(n)
k = 3
alpha = 0.03
mu0 = np.concatenate([A, B, C]).mean()
d2 = ((A.mean() - ABC.mean())**2 * len(A) + (B.mean() - ABC.mean())**2 * len(B) + (C.mean() - ABC.mean())**2 * len(C))/len(ABC)
meanvar = (A.var(ddof=0) * len(A) + B.var(ddof=0) * len(B) + C.var(ddof=0) * len(C)) / len(ABC)
SSE = N * meanvar
MSE = SSE / (N - k)
SSTR = N * d2
MSTR = SSTR / (k - 1)
F = MSTR / MSE
K = f(k - 1, N - k).isf(alpha)#Ka=(K,+inf)
pv = f(k - 1, N - k).sf(F)
left_A = A.mean() - t(N - k).isf((1 - 0.91) / 2) * np.sqrt(MSE / na)
right_A = A.mean() + t(N - k).isf((1 - 0.91) / 2) * np.sqrt(MSE / na)
left_B = B.mean() - t(N - k).isf((1 - 0.91) / 2) * np.sqrt(MSE / nb)
right_B = B.mean() + t(N - k).isf((1 - 0.91) / 2) * np.sqrt(MSE / nb)
left_C = C.mean() - t(N - k).isf((1 - 0.91) / 2) * np.sqrt(MSE / nc)
right_C= C.mean() + t(N - k).isf((1 - 0.91) / 2) * np.sqrt(MSE / nc)
d2, meanvar, (left_A, right_A),(left_B, right_B),(left_C, right_C),F,K,pv
    '''
    return pc.copy(s)
def lek_prep():
    s = '''
q = []
quantile = 0.2
sample = np.array([k for k in range(len(q)) for j in range(q[k])]) / 100
def f(x, a, b):
    return a * b * x ** (a - 1) * (1 - x ** a) ** (b - 1)
def lnL(p, data):
    n = len(data)
    a, b = p
    return n * np.log(a * b) + (a - 1) * np.sum(np.log(data)) + (b - 1) * np.sum(np.log(1 - data ** a))
mx, mx_a, mx_b = 0, 0, 0
for a in range(1, 21):
    for b in range(1, 21):
        prod = lnL([a, b], sample)
        if prod > mx:
            mx = prod
            mx_a = a
            mx_b = b
E_X = integrate.quad(lambda x: x * f(x, mx_a, mx_b), 0, 1)
x = symbols('x')
q = (1 - (1 - x)**(1/mx_b))**(1/mx_a)
quant = q.subs(x, 0.2)
mx_a,mx_b, E_X[0], quant    
    '''
    return pc.copy(s)
def omega_cov_corr():
    s = '''
ds = "..."
data = np.array(list(map(lambda x: list(map(lambda y: int(y[y.index('=')+2: y.index('=')+4]), x.split(','))), s.split('x')[1:])))
data = data[(data[:, 0] >= 50) & (data[:, 1] >= 50)]
X = data[:, 0]
Y = data[:, 1]
covXY = np.sum((X-X.mean())*(Y - Y.mean())) / len(X)
np.cov(X, Y, ddof=0)[0, 1]
corr = covXY / (X.std() * Y.std())
np.corrcoef(X, Y)[0, 1]
covXY, corr 
    '''
    return pc.copy(s)
def omega_sr_std():
    s = '''
xk = np.array([74, 73, 72, 79, 80])
sk = np.array([9, 4, 7, 3, 8])
xp = np.array([22, 29, 28, 25, 20]) / sum([22, 29, 28, 25, 20])
X = rv_discrete(values=(xk, xp))
X2 = rv_discrete(values=(xk**2, xp))
S = rv_discrete(values=(sk**2, xp))
sr = X.mean()
std = (X2.mean() - X.mean()**2 + ((sk**2) * xp).sum())**0.5 #(X.var() + S.mean())**0.5
sr, std
    '''
    return pc.copy(s)

def zapw():
    s = '''
X = np.array(())
n = len(X)
alpha = 0.01
mu0 = 1.91
mu1 = 1.78
stdX = 3.6
z = (X.mean() - mu0)*n**0.5 / stdX
print(z)
Z = norm(0, 1)
A = Z.isf(alpha/2) # H0 не отвергается
print(A)
P = 2 * min(Z.cdf(z), Z.sf(z))
print(P)
def F0(x):
    return norm(0, 1).cdf(x) - 1/2
W = (1 - (F0(Z.isf(alpha/2) - n**0.5 / stdX * (mu1 - mu0)) + F0(Z.isf(alpha/2) + n**0.5 / stdX * (mu1 - mu0)))) # W
print(W)
    '''
    return pc.copy(s)




