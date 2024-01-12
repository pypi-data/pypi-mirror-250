_q1 = r"""
Пусть X1, X2, . . . , X6 – выборка из равномерного распределения на отрезке [5; 8], Fb(x) – соответствующая выборочная функция распределения. Найдите: а) вероятность P Fb(6) = Fb(8) ; б) вероятность P Fˆ(7) = 1 2  \
Если вероятность значения быть меньше 6 и меньше 8 одинакова, значит нужно найти вероятность, при которой х ни в одном из 6 испытаний не принимает значения в интервале [6;8]

P({^F(6) = ^F(8)}) = [P(X[6;8])]^6 = [1 - P(X[6;8])]^6 = (1 - (8 - 6)/(8 - 5)) ^ 6 = (1/3)^6 = 0,0013717421124828627

б) Рассмотрим с.в. Y = 6 * ^F(7)
n = 6
p= (7-5) / (8 - 5) = ⅔
Y  Bin(6, 2/3)

Таким образом, 
P(^F(7) = 1/2) = P( 6 * ^F(7) = 6 * 1/2) = P(Y = 3) = Cnk * pk * (1-p)n-k

n = 6
p = ⅔
k = 3
#1
P_b = math.comb(n, p) * p ** k * (1 - p) ** (n - k)
#2
Y = sts.binom(n, p)
Y.pmf(k)
"""

_q2 = r"""
. Имеется выборка X1, X2, . . . , Xn объема n из генеральной совокупности с функцией распределения F(x). Найдите функции распределения экстремальных статистик X(1) и X(n) \
X(1) = min{X1, ..., Xn} & X(n) = max{X1, ..., Xn} - экстремальные статистики

Функция распределения X(n) :
FX(n)(x) = P(X(n) x) = P(max{X1, ..., Xn} x) = P(X1 x, ..., Xnx) = P(X1 x) * ... *P(Xn x) =
 F(x) * ... * F(x) = Fn(x)

Функция распределения X(1) :
FX(1)(x) = P(X(1) x) = P(min{X1, ..., Xn} x) = 1 - P(min{X1, ..., Xn} >x) = ... =  
1 - (1 - F(x))n
"""

_q3 = r"""
. Пусть X и Y – две независимые несмещенные оценки параметра θ с дисперсиями σ 2 и 4σ 2 соответственно. a) Является ли X2 несмещенной оценкой параметра θ 2? б) Является ли Z = X · Y несмещенной оценкой параметра θ \
E(X2) = Var(X) + E2(X) = 2 + 2EX2() =E(X2) =2 + 2 не является  
E(Z) = E(X * Y) = E(X) * E(Y) = * = 2является 
"""

_q4 = r"""
Пусть ˆθ = T(X1, . . . , Xn) оценка параметра θ, а b = (E[θb] − θ) – смещение. Доказать формулу ∆ = Var(θb) + b 2 , где ∆ = E[(ˆθ − θ) 2 ] – среднеквадратичная ошибка оценки.\
E[( - )2] = E[2-2** + 2] = E[2] - 2* * E[] + 2 = Var() + E2[]  
- 2* * E[] +2 = Var()  +(E[] - )2 =Var()  +b2 =    
"""

_q5 = r"""
Пусть X1, X2 – выборка объема 2 из некоторого распределения с генеральным средним θ = E(X) и дисперсией σ 2 = Var(X). В качестве оценки параметра θ используется оценка вида θb = aX1+2aX2. Известно отношение σ 2 θ 2 = 3 5 . Найдите оценку с наименьшей среднеквадратической ошибкой. Является ли эта оценка несмещенной? \
^ = aX1+ 2aX2; 2/2 = 3/5
Var(^) = Var(aX1+ 2aX2) = 5a2Var(X) = 3a22
1)E[(^ - )2] = Var(^) + [E(^) - ]2 = 3a22 + ( 3a - )2 = (3a2+ 9a2 - 6a + 1) * 2 = (12a2- 6a + 1) * 2  min;
f = 12a2- 6a + 1  min
f’ = 24a - 6 = 0; fmin = f(1/4) = 1/4
^ = X1/4 + X2/2
2)
^ = X1/4 + X2/2 E(^) = 3/4 *E(X2) = 34    не является несмещенной
"""

_q6 = r"""
"""

_q7 = r"""
Пусть X1, X2, X3 – выборка из генерального распределения с математическим ожиданием µ и дисперсией θ = σ 2 . Рассмотрим две оценки параметра θ: a) θb1 = c1(X1 − X2) 2 ; б) θb2 = c2[(X1 − X2) 2 + (X1−X3) 2+(X2−X3) 2 ]. Найдите значения c1 и c2 такие, что оценки θb1 и θb2 являются несмещенными оценками параметра дисперсии σ 2 . \
а) $\hat\theta_1 = c_2 (X_1 - X_2)^2$  

$E[\hat\theta_{1}] = E[c_{1}(X_{1} - X_{2})^{2}] = c_{1}E[(X_{1} - X_{2})^{2}] = c_{1}E[X_{1}^{2} - X_{1}X_{2} + X_{2}^{2}] = c_{1}(E[X_{1}^{2}] - E[X_{1}X_{2}] + E[X_{2}^{2}])$
1) $E[X_{1}^{2}] = Var(X_{1}) + E^{2}[X_{1}] = \sigma^{2}+\mu^{2}$
1) $E[X_{1}X_{2}] = E[X_{1}]\times E[X_{2}] = \mu \times \mu = \mu^{2}$
1) $E[X_{2}^{2}] = Var(X_{2}) + E^{2}[X_{2}] = \sigma^{2}+\mu^{2}$

$c_{1}(E[X_{1}^{2}] + E[X_{1}X_{2}] + E[X_{2}^{2}]) = c_{1}(\sigma^{2}+\mu^{2} - \mu^{2} + \sigma^{2}+\mu^{2}) = c_{1}(\sigma^{2}+\sigma^{2}) = \sigma^{2} \Rightarrow c_{1}=\dfrac{1}{2}$



б) $\hat{\Theta_2} = c_2 [(X_1 - X_2)^2 + (X_1 - X_3)^2 + (X_2 - X_3)^2$  
$E(\hat{\sigma_2^2} = E(c_2[(X_1 - X_2)^2 + (X_1 - X_3)^2 + (X_2 - X_3)^2]) =^{\text{из пункта а}} с_2*[Var(X_1 - X_2) + Var(X_1 - X_3) + Var(X_2 - X_3)] = c_2 * [(\sigma^2 + \sigma^2) + (\sigma^2 + \sigma^2) + (\sigma^2 + \sigma^2)] = 6\sigma^2 c_2 => c_2 = \dfrac{1}{6}$ 
"""

_q8 = r"""
Пусть X1, X2, X3, X4 – выборка из N(θ; σ 2 ). Рассмотрим две оценки параметра θ: θb1 = X1+2X2+3X3+4X4 10 , X1+4X2+4X3+X4 10 . a) Покажите, что обе оценки являются несмещенными для параметра θ; б) Какая из этих оценок является оптимальной?\
$1) \hat{\Theta_1} = \dfrac{x_1+2x_2 + 3x_3 + 4x_4}{10}$  
$2) \hat{\Theta_2} = \dfrac{x_1+4x_2 + 4x_3 + x_4}{10}$  
a) $E(\hat{\Theta_1}) = E(\dfrac{x_1+2x_2 + 3x_3 + 4x_4}{10}) = \dfrac{1}{10}(E(X_1) + 2E(X_2) + 3E(X_3) + 4E(X_4)) = \dfrac{10}{10} * \Theta = \Theta => \text{несмещ. оценка параметра } \Theta$  
$E(\hat{\Theta_2}) = E(\dfrac{x_1+4x_2 + 4x_3 + x_4}{10}) = \dfrac{1}{10}(E(X_1) + 2E(X_2) + 3E(X_3) + 4E(X_4)) = \dfrac{10}{10} * \Theta = \Theta => \text{несмещ. оценка параметра } \Theta$  
б) $\text{т.к. } \hat{\Theta_1} \text{ и } \hat{\Theta_2} \text{ несмещ. } => \text{ оптим. } \hat{\Theta_i} = min$  
1) $Var_{\Theta}(\hat{\Theta_1}) = Var(\dfrac{x_1+2x_2 + 3x_3 + 4x_4}{10}) = \dfrac{1}{100}(Var(X_1) + 4Var(X_2) + 9Var(X_3) + 16Var(X_4) = \dfrac{3\sigma^2}{10}$  
2) $Var_{\Theta}(\hat{\Theta_2}) = Var(\dfrac{x_1+4x_2 + 4x_3 + x_4}{10}) = \dfrac{1}{100}(Var(X_1) + 16Var(X_2) + 16Var(X_3) + Var(X_4) = \dfrac{34\sigma^2}{100}$  
$\text{т.к. } Var(\hat{\Theta_1}) < Var(\hat{\Theta_2}) => \hat{\Theta_1} \text{- оптим. оценка}$
"""

_q9 = r"""
Пусть X1, X2, . . . , Xn – выборка из генерального распределения и пусть θ = E(X), σ 2 = Var(X) – математическое ожидание и дисперсия. Рассмотрим следующие оценки параметра θ: θb1 = X1+X2 2 , θb2 = X1+Xn 4 + X2+...+Xn−1 2(n−2) , θb3 = X. а) Будут ли эти оценки несмещенными для параметра θ? б) Какая из них является состоятельной для параметра θ? \
a) $E[\hat{\Theta_1}] = \dfrac{1}{2}E[X_1 + X_2] = \dfrac{1}{2}[E[X_1]+E[X_2]] = \dfrac{2 \Theta}{2} = \Theta \text{ - несмещен. оценка}$  
$E[\hat{\Theta_2}] = \dfrac{1}{4}E[X_1 + X_n] + \dfrac{1}{2(n-2)}E[X_2 + \cdots  + X_{n-2}] = \dfrac{1}{4}*2*\Theta + \dfrac{1}{2(n-2)} * (n-2) * \Theta = \dfrac{\Theta}{2} + \dfrac{\Theta}{2} = \Theta \text{ - несмещен.}$  
$E[\hat{\Theta_3}] = \dfrac{1}{n}E[\sum_{k=1}^{n} X_k] = \dfrac{1}{n} * n * \Theta \text{ - несмещ.}$  
б) $Var(\hat{\Theta_1}) = \dfrac{1}{4} * Var(X_1 + X_2) = \text{ независимость } = \dfrac{1}{4} * 2 * \sigma^2 = \dfrac{\sigma^2}{2}$  
$Var({\hat{\Theta_1}}) \underset{n-> ∞}{\rightarrow} \dfrac{\sigma^2}{2} \ne 0 \text{ => оценка не состоятельная} $  
$Var(\hat{\Theta_2}) = \dfrac{1}{16}Var(X_1 + X_2) + \dfrac{1}{4(n-2)^2}Var(X_2 + \cdots + X_{n-1}) = \text{ независимость = } \dfrac{1}{16}*2 \sigma^2 + \dfrac{1}{4(n-2)^2} * (n-2) * \sigma^2$  
$\lim\limits_{n \to \infty}(Var(\hat{\Theta_2})) = \lim\limits_{n \to \infty}(\dfrac{\sigma^2}{8} + \dfrac{\sigma^2}{4(n-2)}) = \dfrac{\sigma^2}{8} \ne 0 \text{ - не сост.}$  
$Var(\hat{\Theta_3}) = \dfrac{1}{n^2} * Var(\sum_{k=1}^{n} X_k) = независиомсть =\dfrac{1}{n^2}*n*\sigma^2=\dfrac{\sigma^2}{n}$  
$Var(\hat{\Theta_3}) = \dfrac{\sigma^2}{n} \underset{n-> ∞}{\rightarrow}0$, а также $E[\hat{\Theta_3}] = \Theta$ => оценка состоятельная.  
Ответ: $\hat\Theta_3$

"""

_q10 = r"""
Пусть X1, X2, . . . , Xn – выборка из равномерного распределения U([0; θ]) c неизвестным параметром θ > 0. Требуется оценить параметр θ. В качестве оценка параметра θ рассматриваются: θb1 = 2X, θb2 = n+1 n X(n) . а) Будут ли оценки несмещенными?; б) состоятельными? в) найдите среди них оптимальную.\
а) $E[\hat{\Theta_1}] = E[2\overline{X}] = 2E[X] = 2\dfrac{\Theta - 0}{2}=\theta$ - несмещен.  
$X_{(n)}: F_{(n)}(X) = P(X_{(n)} \le X) = R(X-1 \le X; \cdots; X_n \le X) = P(X_1 \le X) * \cdots * P(X_n \le X) = \dfrac{(x-0)^n}{\Theta^n} = \dfrac{x^n}{\Theta^n}$  
$\oint_{X_(n)}X = \dfrac{d}{dx}F_{X_(n)}(X) = n* \dfrac{X^{n-1}}{\Theta^n}$  
 $E[\hat{\Theta_2}] = \dfrac{n+1}{n}E[X_{(n)}] = \dfrac{n+1}{n}* \int\limits_0^\Theta X*n*\dfrac{x^{n-1}}{\Theta^n}dx = \dfrac{n+1}{\Theta^n}\int\limits_0^\Theta x^ndx = \dfrac{n+1}{\Theta^n}*\dfrac{1}{n+1}*x^{n+1}\left|_\text{0}^\Theta\right. = \Theta$ - несмещенная  
 б) $Var(\hat\Theta_1) = Var(2\overline{X}) = 4Var(\overline{X}) = \dfrac{4}{n}Var(X) = \dfrac{4\Theta^2}{12n}=\dfrac{\Theta^2}{3n} * Var(\hat\Theta_1) = \dfrac{\Theta^2}{3n}\underset{n-> ∞}{\rightarrow}0$ а также $E[\hat{\Theta_1}] = \Theta$ => $\hat\Theta_1$ состоятельная  
 $Var(\hat\Theta_2) = Var(\dfrac{n+1}{n}*X_{(n)})=\dfrac{(n+1)^2}{n^2}Var(X_{(n)})= E[X_{(n)}] = \int\limits_0^\Theta x* \dfrac{nx^{n+1}}{(n+1)\Theta^n}dx = \dfrac{nx^{n+1}}{(n+1)*\Theta^n}\left|_\text{0}^\Theta\right. = \dfrac{n\Theta}{n+1}$  
$E[X_{(n)}^2] = \int\limits_0^\Theta X^2*n*\dfrac{x^{n-1}}{\Theta^n}dx = \dfrac{nx^{n+2}}{(n+2)\Theta^n}\left|_\text{0}^\Theta\right. = \dfrac{n\Theta^2}{n+2}$  
$Var(X_{(n)}) = \dfrac{n\Theta^2}{n+2}-\dfrac{n^2\Theta^2}{(n+1)^2} = \dfrac{\Theta^2n((n+1)^2-n^2-2n)}{(n+2)(n+1)^2} = \dfrac{\Theta^2n}{(n+2)(n+1)^2}$  
$\dfrac{(n+1)^2}{n^2} * \dfrac{\Theta^2n}{(n+2)(n+1)^2} = \Theta^2 * \dfrac{1}{n(n+2)}\underset{n-> ∞}{\rightarrow}0$  
$E[\hat\Theta_2] = \Theta$ а также $Var(\hat\Theta_2)\underset{n-> ∞}{\rightarrow}0$ => оценка состоятельная

"""

_q11 = r"""
a) $E(\hat θ_1) = E(2 \overline{X}) = 2E(\overline{X}) = 2 E(X) = 2\frac{θ}{2} = θ$ - несмещённ.

$X_{(1)} = θ - X_{(n)}$

$E(\hat θ_2) = (n + 1) \cdot E(X_{(1)}) = (n+1)E(θ - X_{(n)}) = nθ + θ - (n+1)E(X_{(n)}) = n*θ + θ - nθ = θ$ - несмещённая

б) $Var(\hat θ_1) = Var(2 \overline{X}) = 4Var(\overline{X}) = \frac{4}{n}Var(X) = \frac{4θ^2}{12n} = \frac{θ^2}{3n} \rightarrow_{n→∞} 0$ - состоятельная

$Var(\hat θ_2) = Var((n+1)θ - X_{(n)}) = (n+1)^2 Var(X_{(n)}) = \dfrac{(n+1)^2 θ^2n}{(n+2)(n+1)^2} =$

$= \dfrac{θ^2n}{(n+2)} \rightarrow_{n→∞} θ^2$ - не состоятельна

в) Оптимальной оценкой является оценка с наименьшей дисперсией $⇒ т.к. \dfrac{θ^2n}{(n+2)} > \dfrac{θ^2}{3n} ⇒$ оптимальной является $\hat θ_1$

"""

_q12 = r"""
$X_1, X_2, \dots, X_n$ из $U([0, θ])$, $\hat θ = c·\overline{X}$

a) $E(\hat θ) = c·E(\overline{X}) = c·E(X) = c·\frac{θ}{2} \Rightarrow$ при с = 2, $\hat θ$ - несмещённая

б) $Δ = E[(\hat θ - θ)^2] = E(\hat θ^2) - 2θE(\hat θ) + θ^2 = c^2·E(\overline{X^2}) - c·θ^2 + θ^2 …$

$Var(\overline{X}) = \frac{\sigma^2}{3} = \frac{\theta^2}{12·3} = \frac{\theta^2}{36}$

$E(\overline{X^2}) = \frac{\theta^2}{36} + \frac{\theta^2}{4} = \theta^2(\frac{1}{36} + \frac{1}{4}) = \theta^2\frac{5}{18}$

$… c^2·\theta^2\frac{5}{18} - c·θ^2 + θ^2 = θ^2(c^2\frac{5}{18} - c + 1) \rightarrow min$

$⇒$ при $c = \frac{5}{9}$ оценка эффективная в рассм. классе

"""

_q13 = r"""
1) $E(X^2) = Var(X) + E(X)^2 = \frac{(θ + θ)^2}{12} + \frac{-θ + θ}{2} = \frac{θ^2}{3}$

2) $E(\hat θ) = \frac{3}{n}E(\Sigma{X^2_i}) = \frac{3}{n}\Sigma{E(X^2_i)} = \frac{3}{n}n\frac{θ^2}{3} = θ^2 \Rightarrow$ несмещённая

3) $-\sqrt{E(\hat θ)} \le E(-\sqrt{\hat θ})$ - неравенство Йенсена

  $-\sqrt{E(\hat θ)} \le -E(-\sqrt{θ})$

  $E(\sqrt{\hat θ}) \le \sqrt{E(\hat θ)} = \sqrt{θ^2} = θ$

  $E(\sqrt{\hat θ}) \le θ$ Необходимо чтобы $E(\sqrt{\hat θ}) = θ^2$, но $θ^2 \le θ$, при $0 \le θ \le 1$, но не для всех θ => смещённая

"""

_q14 = r"""
$Y_k = \beta x_k + ε_k$

$E(\hat θ) = E(\dfrac{\Sigma{Y_k}}{\Sigma{x_k}}) = \frac{1}{\Sigma{x_k}}⋅E(\beta \cdot \Sigma{ε_k}) = \dfrac{E(\beta \Sigma{x_k})}{\Sigma{x_k}} + \dfrac{E(\Sigma{ε_k})}{\Sigma{x_k}} = \dfrac{\beta \cdot \Sigma{x_k}}{\Sigma{x_k}} = \beta$ - несмещённая

"""

_q15 = r"""
$Y_k = \beta x_k + ε_k$

$\hat \beta = \frac{1}{n} \Sigma{(\frac{Y_k}{x_k})} = \frac{1}{n} \Sigma{(\beta + \frac{ε_k}{x_k})}$

$E(\hat θ) = E(\frac{1}{n} \Sigma{(\beta + \frac{ε_k}{x_k})}) = \frac{1}{n}E(n \cdot \beta) + \frac{1}{n}E(\Sigma{\frac{ε_k}{x_k}}) = \beta + \frac{1}{n} \Sigma{\frac{1}{x_k} \cdot E(ε_k)} = \beta$ - несмещённая

"""

_q16 = r"""
$X \sim П(\lambda), \lambda = \hat \nu_1$

$\hat \nu_1 = \overline{X}$

$\overline{X} = \lambda$

a) $P(X \ge 3) = 1 - P(X \le 3) = 1 - (P(X=0) + P(X=1) + P(X=2))$

$P(X = k) = \dfrac{λ^k \cdot e^{-λ}}{k!}$

б) $X \ge 3: \frac{84}{400} = 0.21$

"""

_q17 = r"""
$X \sim U([0, 4θ])$

$θ = \hat \nu_1 = E(\overline{X}) = E(X) = \overline{X} = 2θ$

$\hat θ = \frac{\overline{X}}{2}$

a) $E(\hat θ) = E(\frac{\overline{X}}{2}) = \frac{1}{2} \cdot 2θ = θ$ - несмещённая

б) $Var(\hat θ) = Var(\frac{\overline{X}}{2}) = \frac{(4θ)^2}{4 \cdot 12} = \frac{θ^2}{3n} \rightarrow_{n→∞} 0$ - состоятельна

"""

_q18 = r"""
$ν_1 = \hat{\nu}_1$




$\nu = E(X) = \frac{a+b}{2} = \bar{x} ⇒ a+b = 2\bar{x} = 2M_1$




$\nu_2 = E(x^2)=\overline{x^2}$




$Var(X) = E(x^2) -[E(x)]^2 ⇒ \frac{(b-a)^2}{12} + \frac{(a+b)^2}{4}=\frac{4b^2+4ab+4a^2}{12}=\frac{b^2+ab+a^2}{3}=\overline{x^2}=M_2$




\begin{cases}
a = 2M_1-b \\
b^2+(2M_1-b)b+(2M_1-b)^2=3M_2
\end{cases}
$b^2+2M_1b-b^2+4M_1^2-4M_1b+b^2-3M_2=0$




$b^2-2M_1b+4M_1^2-3M_2=0$




$D = 4M^2_1-4(4M_1^2-3M_2)=12M_2-12M_1^2$


$b = \frac{2M_1+\sqrt{12M_2-12M_1^2}}{2}=M_1+\sqrt{3(M_2-M_1^2)}$


$a=M_1-\sqrt{3(M_2-M_1^2)}$


\begin{cases}
a = \bar{x} - \sqrt{3(\overline{x^2}-(\bar{x})^2)}\\
b = \bar{x} + \sqrt{3(\overline{x^2}-(\bar{x})^2)}\\
\end{cases}

"""

_q19 = r"""
$E(x) = \int^{+∞}_τxλe^{-λ(x-τ)}dx=τ+\frac{1}{λ}=\bar{x}$


$E(x^2) = \int^{+∞}_τx^2λe^{-λ(x-τ)}dx=τ^2+\frac{2τ}{λ}+\frac{2}{λ^2}=\overline{x^2}$


\begin{cases}
τ + \frac{1}{λ} = \bar{x} \\
τ^2 + \frac{2τ}{λ} + \frac{2}{λ^2} = \overline{x^2} (1)
\end{cases}


$(1) (τ + \frac{1}{λ})^2 + \frac{1}{λ^2} = \overline{x^2}$


$\frac{1}{λ^2} = \overline{x^2} - (\bar{x})^2$


$λ = \frac{1}{\sqrt{\overline{x^2} - (\bar{x})^2}}$


$τ=\bar{x} - \sqrt{ \overline{x^2} - (\bar{x})^2}$

from scipy.stats import *
from sympy import *
import numpy as np
n = 423
sample = np.array([4.55]*219 + [11.55]*98 + [18.55]*50 + [25.55]*25 + [32.55]*17  + [39.55]*7 + [46.55]*2 + [53.55]*4 + [60.55])
sample_2 = sample**2
x = Symbol('x')
t = Symbol('t')
lamda_hat = 1/(sample_2.mean() - sample.mean()2)0.5
tau_hat = sample.mean() - 1/lamda_hat
print(lamda_hat, tau_hat)

f = lamda_hat*exp(-lamda_hat*(x - tau_hat))
integrate(f, (x, tau_hat, t)) - 0.9066

X = expon(loc = tau_hat, scale = 1/lamda_hat)
print(log(0.0934/1.159)/-0.099214, X.ppf(0.9066))

"""

_q20 = r"""
$\nu_1=\hat{\nu_1}; f(x)=F'(x)=\beta x^{\beta-1}$


$\nu_1=E(x)=\int^1_0x f(x) dx = \beta \int^1_0x^\beta dx = \frac{\beta x^{\beta+1}}{\beta+1} |^1_0 = \frac{\beta}{\beta+1}=\bar{x}=0.78$


⇒ $\beta = 3.54545$


$P(x < x) = 0.67^{3.54545}=0.2417$
"""

_q21 = r"""
$X \sim Pois(λ)$


$P(X = k) = \frac{λ^ke^{-λ}}{k!}, k = 0,1,2,...$


$L(\vec{x}, λ) = П^n_{i=1}\frac{λ^{x_i}e^{-λ}}{x_i!}$


$\ln L = ∑^n_{i=1}[x_i\ln λ - λ - \ln(x_i!)] = \ln(λ) n \bar{x} - nλ - ∑\ln(x_i!)$


$\frac{∂L}{∂λ} = \frac{n\bar{x}}{λ} - n = 0$


$\text{Ответ: }λ  = \bar{x}$

"""

_q22 = r"""
$L = λe^{-λx_1} ⋅ ... ⋅ λe^{-λx_n}=λ^n e^{-λ(x_1+...+x_n)}=λ^n\cdot e^{-λn\bar{x}}$


$\ln L = n lnλ - λn\bar{x}$


$(\ln L)'_λ = \frac{n}{λ} - n\bar{x} = 0 | : n$


$\frac{1}{λ} - \bar{x} = 0$


$\hat{λ}=\frac{1}{\bar{x}}$

"""

_q23 = r"""
$X_{\overline{1, n}} - выборка, P(X = -1) = θ, P(X = 1) = 4θ, P(X = 2) = 2θ, P(X = 0) = 1-7θ$

Пусть a, b, c, d - кол-во появлений каждого значения x (a+b+c+d) = n

$L = θ^a \cdot (4θ)^b \cdot (2θ)^c \cdot (1 - 7θ)^d = 4^b 2^c θ^{a+b+c}(1-7θ)^d$

$lnL = bln4 + cln2 + (a+b+c)lnθ + dln(1-7θ)$

$\frac{\partial{lnL}}{\partial{θ}} = \dfrac{a+b+c}{θ} - \dfrac{7d}{1 - 7θ}$ далее выразить $θ$ надо

$\hat θ = \dfrac{n-d}{7n}, d \sim Bin(n; 1-7θ), E(d) = np, Var(d) = npq$

a) $\hat θ = E(\dfrac{n-d}{7n}) = \dfrac{1}{7} - \dfrac{1}{7n}\cdot E(d) = θ$ - несмещённая

б) $Var(\hat θ) = Var(\frac{1}{7} - \frac{d}{7n}) = \frac{1}{49n^2}Var(d) = \frac{pq}{49n} →_{n→∞} 0$ - состоят.

"""

_q24 = r"""
"""

_q25 = r"""
"""

_q26 = r"""
$P(F > f_\alpha(1;m)) = P(\dfrac{\chi^2(1)\cdot m}{\chi^2(m)} > f_\alpha(1;m)) = P(\dfrac{Z^2}{\frac{\chi^2(m)}{m}} > f_\alpha(1;m)) = P(\dfrac{|Z|}{\sqrt{\frac{\chi^2(m)}{m}}} > f_\alpha(1;m)) = P(-\sqrt{f_\alpha(1;m)} < \dfrac{Z}{\sqrt{\frac{\chi^2(m)}{m}}} > \sqrt{f_\alpha(1;m)}) = P(-\sqrt{f_\alpha(1;m)} < t(m) > \sqrt{f_\alpha(1;m)})$

$P(-t_{\frac{\alpha}{2}}(m) < t(m) > t_{\frac{\alpha}{2}}(m)) ⇒ \sqrt{f_\alpha(1;m)} = t_{\frac{\alpha}{2}}(m) ⇒ f_\alpha(1;m) = t_{\frac{\alpha}{2}}^2(m)$

"""


mas = []

loc = locals()
count = 1
while True:
    name = f"_q{count}"
    if name not in loc:
        break
    mas.append(loc[name])
    count += 1
