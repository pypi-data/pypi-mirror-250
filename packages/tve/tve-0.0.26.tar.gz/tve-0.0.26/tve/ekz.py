from PIL import Image
from IPython.display import display
import os


main_path = os.path.join(os.path.dirname(__file__), 'pic')

def show(num):
    if num == 0:
        image_path_1 = os.path.join(main_path, 'all_1.png')
        image_path_2 = os.path.join(main_path, 'all_2.png')
        image_path_3 = os.path.join(main_path, 'all_3.png')
        # Открываем изображение
        img1 = Image.open(image_path_1)
        img2 = Image.open(image_path_2)
        img3 = Image.open(image_path_3)

        # Отображаем изображение
        display(img1)
        display(img2)
        display(img3)
    if num != 0:
        # Определяем путь к изображению
        image_path_1 = os.path.join(main_path, f'usl_{num}.png')
        image_path_2 = os.path.join(main_path, f"resh_{num}.png")

        # Открываем изображение
        img1 = Image.open(image_path_1)
        img2 = Image.open(image_path_2)

        # Отображаем изображение
        display(img1)
        display(img2)

        # Выводим текст в зависимости от значения num
        if num == 1:
            print('''
grades = np.array([64, 41, 83, 41, 83, 53, 0, 63, 84, 98, 2, 42, 98, 57, 63, 53, 91, 28, 76, 63, 78, 83])
n=len(grades)
# 1
A = grades[grades>0].mean()
print(A)
# 2
M = np.median(grades[grades>0])
print(M)
# 3
H = hmean(grades[grades>=M])
G = gmean(grades[grades>=M])
print(H, G)
# 4
Q = np.median(grades[grades>=M])
print(Q)
# 5
N = len(grades[(grades>=H) & (grades<=Q)])
print(N)
            ''')
        elif num == 2:
            print('''
pd = np.array([-956, 744, 1024, -794, 17, -252, -1122, -853, 65, -200, 991, 277, 59, -105, -95, 729, 20, 584, -832, -232, -490, -590, 197, -20, -278, -123, -275, -72, -416, -165])
n = len(pd)
# 1
E = pd.mean()
print(E)
# 2 
std = pd.std()
print(std)
# 3
X = norm(E, std) 
L=X.ppf(0.25)
H=X.ppf(0.75)
print(L,H)
# 4
N = len(pd[(pd>=L) & (pd<=H)])
print(N)
# 5
mx=-10**100
for i in range(n):
    temp = abs((i+1)/n - X.cdf(sorted(pd))[i])
    mx = max(temp,mx)
    
print(mx)
            ''')
        elif num == 3:
            print('''
import re

s = 'x1 = 73, y1 = 69 x2 = 39, y2 = 43 x3 = 87, y3 = 88 x4 = 60, y4 = 41
x5 = 79, y5 = 95 x6 = 86, y6 = 98 x7 = 47, y7 = 46 x8 = 42, y8 = 58 x9 = 44, y9 = 43 x10 = 66, y10 = 56
x11 = 47, y11 = 47 x12 = 80, y12 = 85 x13 = 39, y13 = 35 x14 = 73, y14 = 65 x15 = 62, y15 = 77
x16 = 44, y16 = 55 x17 = 44, y17 = 60 x18 = 56, y18 = 43 x19 = 39, y19 = 44 x20 = 86, y20 = 64
x21 = 40, y21 = 39 x22 = 84, y22 = 82 x23 = 74, y23 = 56 x24 = 73, y24 = 68 x25 = 51, y25 = 34
x26 = 38, y26 = 52 x27 = 65, y27 = 65 x28 = 57, y28 = 53 x29 = 33, y29 = 50 x30 = 72, y30 = 94

nums = np.array([int(i) for i in re.findall(r'\b\d+\b', s)])
x = nums[::2]
y = nums[1::2]
x50 = []
y50 = []
for i in range(len(x)):
    if x[i]>=50 and y[i]>=50:
        x50.append(x[i])
        y50.append(y[i])
        
x50 = np.array(x50)
y50 = np.array(y50)
# 1
cov = (x50*y50).mean() - x50.mean()*y50.mean()
print(cov)
# 2
ro = cov/(x50.std()*y50.std())
print(ro)
            ''')
        elif num == 4:
            print('''
k=5 # кол-во групп на потоке
n=np.array([22, 29, 28, 25, 20])
x=np.array([74, 73, 72, 79, 80])
s=np.array([9, 4, 7, 3, 8])
# 1
E = sum(n*x)/sum(n)
print(E)
# 2
sig2 = sum(n*(x-E)**2)/sum(n)
s2 = sum(n*s**2)/sum(n)
std = np.sqrt(sig2+s2)
print(std)
            ''')
        elif num == 5:
            print('''
g = np.array([95, 12, 0, 3, 63, 64, 0, 63, 100, 96, 54, 79, 0, 98, 71, 68, 95, 97, 89, 78, 79, 89, 100, 67, 0, 63, 80, 64])
k=6
n=len(g)
# 1
var = g.var()/k
print(var)
# 2
m3=moment(g,3)/k**2
# m3 = np.sum((g-g.mean())**3)/(n*k**2)
print(m3)
            ''')
        elif num == 6:
            print('''
n = 27 #количество студентов в группе 
k = 7 #количество выбранных студентов 
# повторный выбор не допускается!
marks = np.array([86, 62, 66, 100, 26, 0, 73, 87, 80, 78, 65, 55, 9, 3, 31, 79, 86, 73, 19, 89, 74, 88, 63, 55, 51, 77, 63])
# 1
mean_mean_x = np.mean(marks)
print(mean_mean_x)
# 2
var_mean_x = (np.var(marks)/k) * ((n - k)/(n -1))
print(var_mean_x)
            ''')
        elif num == 7:
            print('''
score = [2,3,4,5]
number = [80, 12, 55, 56]
n = 7 # кол-во преподавателей

N = sum(number)
n1 = N/n
e = sum([score[i] * number[i] for i in range(4)])/N

v = 1/N*sum([(score[i]**2 * number[i]) for i in range(4)]) - e**2
var = v* (N-n1) / (n1*(N-1))
e = str(round(e, 5)).replace('.', ',')
var = str (round(var**0.5,5)).replace('.', ',')

print( 'Мат ожидание: ' , e)
print ('Стандартное отклонение: ', var)
            ''')
        elif num == 8:
            print('''
combs = np.array([(r,b) for r in range(1,7) for b in range(1,7)])
n=len(combs)
k=11 # кол-во различных комбинаций

mean, var = combs.mean(axis=0), combs.var(axis=0)
# с.в. Xi задаются соотношениями Xi = 15Ri - 7Bi
E = 15*mean[0]-7*mean[1]
Var = (15**2) * var[0] + ((-7)**2)*var[1]
VAR = (Var/k)*((n-k)/(n-1))

E, np.sqrt(VAR)
            ''')
        elif num == 9:
            print('''
q=11
k=257
lst = np.array(list(itertools.product([0,1],repeat=q)))
n=len(lst)
# 1 
E = lst.mean()*q
print(E)
# 2 
var = lst.var()*q
var = var/k*(n-k)/(n-1)
print(var)
            ''')
        elif num == 10:
            print('''
# 1 вариант решения
import scipy.stats as stats
import numpy as np
N = 100
n = 14

table = [
    [18, 13, 17],
    [13, 16, 23]
]
X_x = [200, 400]
Y_y = [1, 2, 4]

X = stats.rv_discrete(
    values=(X_x, [(table[0][0] + table[0][1] + table[0][2]) / N, (table[1][0] + table[1][1] + table[1][2]) / N]))

Y = stats.rv_discrete(
    values=(Y_y, [(table[0][0] + table[1][0]) / N, (table[0][1] + table[1][1]) / N, (table[0][2] + table[1][2]) / N]))

XY = stats.rv_discrete(
    values=([x * y for x in X_x for y in Y_y], [table[i][j] / N for i in range(2) for j in range(3)]))

# Бесповторная выборка (т.к. без возвращений)
# E(Y_hat) = E(Y)
print("Математическое ожидание", X.mean())

# sigma(X_hat) = sqrt(Var(X_hat)) = sqrt(Var(X)/n * (N-n) / (N-1))
print("Дисперсия", (Y.var() / n) * ((N - n) / (N - 1)))

# Cov(X_hat, Y_hat) = Cov(X, Y) / n * (N-n) / (N-1)
CovXY = XY.mean() - X.mean() * Y.mean()
CovXY_ans = (CovXY / n) * ((N - n) / (N - 1))
print("Ковариация", CovXY_ans)

# 
sigmaX = np.sqrt(X.var())
sigmaY = np.sqrt(Y.var())
ro = CovXY / (sigmaX*sigmaY)
print('Коэффициент корреляции ', ro)

# 2 вариант
vals = [(200, 1)] * 18 + [(200, 2)] * 13 + [(200, 4)] * 17 + \
[(400, 1)] * 13 + [(400, 2)] * 16 + [(400, 4)] * 23
vals = np.array(vals)
k = 14
n = len(vals)

# мат ожидание
# если E(X) - 0, E(Y) - 1 
E = vals.mean(axis=0)[0]
print(E)

# дисперсия
# если Var(X) - 0, Var(Y) - 1 
vary = vals.var(axis=0)[1]
vary = (vary/k)*((n-k)/(n-1))
print(vary)

# стандартное отклонение
# просто np.sqrt(дисперсия)
# если sigma(X) - 0, sigma(Y) - 1 
vary = vals.var(axis=0)[1]
vary = (vary/k)*((n-k)/(n-1))
sigma = np.sqrt(vary)
print(sigma)
 
# ковариация
cov = np.cov(vals[:,0], vals[:,1],ddof=0)[0,1]/k*(n-k)/(n-1)
print(cov)

# коэф корреляции
sigmaX = np.sqrt(vals.var(axis=0)[0])
sigmaY = np.sqrt(vals.var(axis=0)[1])
cov = np.cov(vals[:,0], vals[:,1],ddof=0)[0,1]
ro = cov / (sigmaX*sigmaY)
print(ro)
            ''')
        elif num == 11:
            print('''
q = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
1, 1, 3, 3, 2, 4, 2, 3, 8, 10, 6, 7, 14, 13, 15, 14, 17, 15, 24, 22, 34, 35, 34, 44, 45, 55, 36, 48, 38, 46, 40, 49, 48, 39, 39, 21, 18, 18, 10,
5, 6, 4, 1, 0, 1, 0, 0, 0, 0, 0, 0]
quantil = 0.2


sample=[]
for i in range(len(q)):
    temp = [i]*q[i]
    sample.extend(temp)
sample=np.array(sample)/100

def f(x,a,b):
    return a*b*x**(a-1)*(1-x**a)**(b-1)

def lnL(p,data):
    n=len(data)
    a,b=p
    return n*np.log(a*b)+(a-1)*np.sum(np.log(data))+(b-1)*np.sum(np.log(1-data**a))

mx,mxa,mxb=0,0,0
# максимизируем функцию правдоподобия
for a in range(1,21):
    for b in range(1,21):
        prod = lnL([a,b],sample)
        if prod>mx:
            mx=prod
            mxa=a
            mxb=b
from scipy import integrate
E = integrate.quad(lambda x: x * f(x, mxa, mxb), 0, 1)[0]
current_quantil = (1 - (1 - quantil) ** (1 / mxb)) ** (1 / mxa)
mxa,mxb,E,current_quantil 
            ''')
        elif num == 12:
            print('''
# x = x.replace(',', '.')
# x = x.replace(';', ',')
x = np.array([-1.377, -0.664, 0.544, -0.259, -0.162, -0.065, -1.324, 0.561, 0.382, 1.482, -1.113, -0.68, 0.536, -0.541, -1.348, -0.287, 0.964, 1.353, -0.095, -0.008, -0.505, 2.807, 1.258, -0.517, 2.763, 0.285, -0.836, 0.891, 0.785, 0.811, 0.08, -0.09, 1.637, 2.165, 0.911, -2.165])
y = np.array([-1.466, -0.554, 0.575, 0.284, -0.779, 0.179, -1.809, 0.707, 0.108, 1.174, -1.672, -0.654, -0.187, -0.643, -0.995, 0.489, 0.69, 1.612, 0.176, 0.275, -0.217, 2.311, 1.107, -0.395, 2.467, 0.362, -0.978, 0.975, 0.439, 0.765, 0.154, -0.308, 1.404, 1.674, 0.816, -1.418])
gamma = 0.73

n=len(x)
Z=norm()
alpha=1-gamma

# выборочный коэф корреляции
ro_hat = np.cov(x,y,ddof=0)[0,1]/x.std()/y.std()
print(ro_hat)

# границы доверительного интервала
u_left = np.arctanh(ro_hat) - 1 / np.sqrt(n - 3) * Z.isf((1 - gamma) / 2)
u_right = np.arctanh(ro_hat) + 1 / np.sqrt(n - 3) * Z.isf((1 - gamma) / 2)

print(np.tanh(u_left), np.tanh(u_right))
            ''')
        elif num == 13:
            print('''
# дисперсия не известна
s = '1,494; 0,274; 10,106; 1,165; 1,411; -0,809; 0,617; 4,121; 6,242; -3,752; 0,98; 0,884; 6,619; 1,781; 6,055; -3,969; 1,481; 4,778; -4,171; 1,672'
s = s.replace(',', '.').replace(';', ',')
data = list(map(float, s.split(',')))
x = np.array(data)
n = len(x)

alpha = 0.04
mu0 = 1.45
mu1 = 1.34

T = np.sqrt(n - 1) * (x.mean() - mu0) / x.std(ddof=0)

A = t(n - 1).isf(alpha / 2)

P = 2 * min(t(n - 1).cdf(T), t(n - 1).sf(T))

delta = np.sqrt(n - 1) * (mu1 - mu0) / x.std()
t2 = t(n - 1).isf(alpha / 2)

beta = nct(n - 1, delta).cdf(t2) - nct(n - 1, delta).cdf(-t2)
W = 1 - beta

print(T, A, P, W)
            ''')
        elif num == 14:
            print('''
s = '1,943; -1,37; 0,323; 3,293; 1,332; 3,173; 2,409; 4,521; 5,488; 2,914; 4,19; 4,483; 3,192; 7,648; 0,835; 2,648; 2,264; -5,505; -0,958; 5,399'
s = s.replace(',', '.').replace(';', ',')
data = list(map(float, s.split(',')))
x = np.array(data)
n = len(x)

s = 3.6
alpha = 0.01
mu0 = 1.91
mu1 = 1.78

Z = norm()
def Phi0(x):
    return Z.cdf(x) - 1 / 2

z = np.sqrt(n) * (x.mean() - mu0) / s

A = Z.isf(alpha / 2)

P = 2 * min(Z.cdf(z), Z.sf(z))

beta = Phi0(A - np.sqrt(n) * (mu1 - mu0) / s) + Phi0(A + np.sqrt(n) * (mu1 - mu0) / s)
W = 1 - beta

z, A, P, W
            ''')
        elif num == 15:
            print('''
# mu известно ищем sigma
s = '0,889; 1,514; 2,846; 2,811; 0,84; 0,945; 0,02; -0,441; -0,796; 3,739; 0,688; 0,777; -0,233; 2,284; -0,681; 1,056; 0,21; 1,8; 0,687; -0,144; 1,285; 1,851; 1,402; 1,695; 0,533; 0,87; 0,486; 0,874; 0,312; -0,821'
s = s.replace(',', '.').replace(';', ',')
data = list(map(float, s.split(',')))
x = np.array(data)
n = len(x)

alpha = 0.02
mu = 1.18
s0 = 1.14
s1 = 1.24

s2 = np.sum((x - mu) ** 2) / n

CHI = n * s2 / s0 ** 2

A = chi2(n).isf(1 - alpha / 2)
B = chi2(n).isf(alpha / 2)

P = 2 * min(chi2(n).cdf(CHI), chi2(n).sf(CHI))

beta = chi2(n).cdf(s0 ** 2 / s1 ** 2 * B) - chi2(n).cdf(s0 ** 2 / s1 ** 2 * A)

CHI, A, B, P, beta
            ''')
        elif num == 16:
            print('''
# сигма и мю не известны
s = '0,889; 1,514; 2,846; 2,811; 0,84; 0,945; 0,02; -0,441; -0,796; 3,739; 0,688; 0,777; -0,233; 2,284; -0,681; 1,056; 0,21; 1,8; 0,687; -0,144; 1,285; 1,851; 1,402; 1,695; 0,533; 0,87; 0,486; 0,874; 0,312; -0,821'
s = s.replace(',', '.').replace(';', ',')
data = list(map(float, s.split(',')))
x = np.array(data)


alpha = 0.02
s0 = 1.14
s1 = 1.24

CHI = (n - 1) * x.var(ddof=1) / s0 ** 2

A = chi2(n - 1).isf(1 - alpha / 2)
B = chi2(n - 1).isf(alpha / 2)

P = 2 * min(chi2(n - 1).cdf(CHI), chi2(n - 1).sf(CHI))

beta = chi2(n - 1).cdf(s0 ** 2 / s1 ** 2 * B) - chi2(n - 1).cdf(s0 ** 2 / s1 ** 2 * A)

CHI, A, B, P, beta
            ''')
        elif num == 17:
            print('''
s1 = '4,837; 2,78; 4,868; 5,183; 2,87; 1,781; 2,421; 2,683; 2,7; 3,764; 2,697; 3,572; 5,147; 4,114; 5,962; 3,183; 3,25; 5,03; 3,894; 4,279; 3,05; 4,855; 4,243; 5,05; 4,536'
s1 = s1.replace(',', '.').replace(';', ',')
data1 = list(map(float, s1.split(',')))
x = np.array(data1)
n = len(x)


s2 = '3,539; 5,746; 2,145; 3,284; 4,602; 3,135; 3,417; 3,694; 0,047; 4,838; 2,735; 4,183; 4,738; 2,781; 4,129; 4,695; 4,016; 3,517; 4,747; 1,872; 5,439; 0,861; 2,821; 4,437; 4,006; 7,154; 4,244; 4,083; 5,911; 2,052; 4,124; 3,738; 4,555; 1,084; 3,996'
s2 = s2.replace(',', '.').replace(';', ',')
data2 = list(map(float, s2.split(',')))
y = np.array(data2)
m = len(y)

sx = 0.8
sy = 1.4
alpha = 0.03
delta = 0.6 #mu_x - mu_y


Z = norm()
def Phi0(x):
    return Z.cdf(x) - 1 / 2

z = (x.mean() - y.mean()) / np.sqrt(sx ** 2 / n + sy ** 2 / m)

P = Z.sf(z)

A = Z.isf(alpha)


beta = 1 / 2 + Phi0(A - np.sqrt(m * n) / np.sqrt(m * sx ** 2 + n * sy ** 2) * delta)
W = 1 - beta

z, P, A, W
            ''')
        elif num == 18:
            print('''
from scipy.stats import f
x = convert('0,616; 1,046; 2,575; -0,344; 2,339; -0,68; 3,739; 2,251; -1,252; 3,536; -0,491; 5,556; 4,856; -1,68; 2,33; 1,345; 2,829; 2,539; 3,304; 3,497; 0,211; 3,563; 0,94; 3,642; 1,956; 3,919; 3,568')
x = np.array(x)
n1 = len(x)

y = convert('2,834; 1,504; -0,678; 5,619; 0,97; 1,617; 3,768; -1,309; 3,343; -1,778; -0,854; 1,04; 2,83; -2,335; 4,853; 5,6; 4,341; 4,362; 3,52; 1,151; -0,621; -2,88; 1,697; 1,753; 0,211; 2,157; 1,989; 2,457; 1,399; 1,61; -0,558; 2,132; 2,293')
y = np.array(y)
n2 = len(y)

z = convert('2,398; -2,77; 4,679; 1,924; 0,574; 5,329; 0,699; 4,457; -0,3; 1,682; -1,34; 0,046; -1,096; 1,935; 2,411; 4,134; 5,643; 3,071; 6,526; 4,941; 2,844; -0,43; -2,066; 0,22; 0,317; -1,923; 1,38; -2,485; 0,111; -0,542; 4,78; 1,93; 0,462; 5,487; -3,547; 2,933; -0,987; -0,21; 3,955')
z = np.array(z)
n3 = len(z)

xyz = pd.DataFrame([x, y, z]).T
xyz_all = np.concatenate([x, y, z])
n = [n1, n2, n3]
N = sum(n)
k = 3
alpha = 0.01
d2 = np.sum((xyz.mean() - xyz_all.mean()) ** 2 * n) / N
meanvar = np.sum(xyz.var(ddof=0) * n) / N
SSE = N * meanvar
MSE = SSE / (N - k)
SSTR = N * d2
MSTR = SSTR / (k - 1)
F = MSTR / MSE
#f(k - 1, N - k).isf(alpha)
P = f(k - 1, N - k).sf(F)

d2, meanvar, F, P
            ''')
        else:
            print('Такого задания нет')
def show_list(num):
    if num == 0:
        image_path_4 = os.path.join(main_path, 'all_4.png')
        img4 = Image.open(image_path_4)
        display(img4)
    if num != 0:
        # Определяем путь к изображению
        if num != 4:
            image_path_1 = os.path.join(main_path, f"usl_list_{num}.png")
            image_path_2 = os.path.join(main_path,f"resh_list_{num}.png")

            # Открываем изображение
            img1 = Image.open(image_path_1)
            img2 = Image.open(image_path_2)

            # Отображаем изображение
            display(img1)
            display(img2)

        # Выводим текст в зависимости от значения num
    if num == 1 or num == 2 or num == 3 or num == 5 or num == 7:
        print('''No code''')
    elif num == 4:
        print('''

import numpy as np
from scipy.stats import *
import sympy as sp
import math
x_arr = []
x, a, b, k, beta, tau, mu1, mu2, lambd, xmean, alpha, teta = sp.symbols('x a b k beta tau mu1 mu2 lambda \overline{x} alpha teta')


xi = np.linspace(4, 60, 9) + 0.55
ni = [219, 98, 50, 25, 17, 7, 2, 4, 1]

for i in range(len(xi)):
    x_arr.extend([xi[i]] * ni[i])
    
x_arr = np.array(x_arr)


fx = lambd * sp.E ** (-lambd * (x - tau))

p1 = sp.integrate(x * fx, (x, tau, math.inf))
p1

# wolfram
p1 = lambd * sp.E ** (lambd * tau) * (sp.E ** (-lambd * tau) * (lambd * tau + 1) / lambd ** 2)
p1

p2 = sp.integrate(x ** 2 * fx, (x, tau, math.inf))
p2

p2 = lambd * sp.E ** (lambd * tau) * (sp.E ** (-lambd * tau) * (lambd * tau * (lambd * tau + 2) + 2) / lambd ** 3)
p2
m1 = x_arr.mean()
m2 = x_arr.var() + m1 ** 2
m1, m2

res = sp.solve([p1 - m1, p2 - m2])
res  #ответы на lambda и тао, берем нижнюю строку
r = sp.integrate(fx, x)#0.0992 * np.e ** (-0.0992 * (x - 1.4873)))
r
(0.0992 * np.e ** (-0.0992 * (x - 1.4873))).simplify()
class distr(rv_continuous):
    def _pdf(self, x):
        if x >= 1.48732514522262:
            return 0.0992139938204183 * np.e ** (-0.0992139938204183 * (x - 1.48732514522262))
        return 0
#     def _cdf(self, x):
#         if x >= 1.4873:
#             return 1 -np.e ** (-0.0992 * (-1.4873 + x))
#         return 0

X = distr()

X.ppf(0.9066)  #ответ T

res, X.ppf(0.9066)  #итого ответы на задание
                  ''')
    elif num == 6:
        print('''
import numpy as np
from scipy.stats import *
import sympy as sp
import math
x, a, b, k, beta, tau, mu1, mu2, lambd, xmean, alpha, teta = sp.symbols('x a b k beta tau mu1 mu2 lambda \overline{x} alpha teta')
Fx = x ** beta
fx = sp.Derivative(Fx, x, evaluate=True)
m1 = 0.78
fx
res = sp.integrate(x * fx, (x, 0, 1)).args[0].args[0].simplify()
res



sp.solve(res - m1)[0] #отдельно вывести и подставить в степень в строку return x ** , это первый ответ



class distr(rv_continuous):
    def _cdf(self, x):
        if 0 <= x <= 1:
            return x ** 3.54545454545455
        return 0
X = distr()
X.cdf(0.67)  #ответ
''')
