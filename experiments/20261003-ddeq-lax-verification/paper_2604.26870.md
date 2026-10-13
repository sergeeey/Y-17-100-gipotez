##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHubSubmit in GitHub

![](https://arxiv.org/static/base/1.0.1/images/icons/smileybones-small.svg)arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[![arXiv logo](https://arxiv.org/static/base/1.0.1/images/arxiv-logo-primary-light.svg)Back to arXiv](https://arxiv.org/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [Report Issue](https://arxiv.org/html/2604.26870# "Report an Issue") [Back to Abstract](https://arxiv.org/abs/2604.26870v1 "Back to abstract page") [Download PDF](https://arxiv.org/pdf/2604.26870v1 "Download PDF")

1. [Abstract.](https://arxiv.org/html/2604.26870#abstract1 "In On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")
2. [1 Introduction](https://arxiv.org/html/2604.26870#S1 "In On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")
3. [2 General results on differential-difference matrix Lax representations](https://arxiv.org/html/2604.26870#S2 "In On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")
4. [3 Miura-type transformations and matrix Lax representations](https://arxiv.org/html/2604.26870#S3 "In On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")
   1. [3.1 Non-autonomous examples](https://arxiv.org/html/2604.26870#S3.SS1 "In 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")
   2. [3.2 Other examples](https://arxiv.org/html/2604.26870#S3.SS2 "In 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")
5. [References](https://arxiv.org/html/2604.26870#bib "In On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")

[License: arXiv.org perpetual non-exclusive license](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2604.26870v1 \[nlin.SI\] 29 Apr 2026

# On matrix Lax representations for (1+1)-dimensional    evolutionary differential-difference equations

Sergei Igonin
Address: Center of Integrable Systems, P.G. Demidov Yaroslavl State University, Yaroslavl, Russia
Email address: [s-igonin@yandex.ru](mailto:s-igonin@yandex.ru)

###### Abstract.

Differential-difference matrix Lax representations (Lax pairs),
gauge transformations, and discrete Miura-type transformations (MTs)
belong to the main tools in the theory of (nonlinear) integrable differential-difference equations.

For a given equation, two matrix Lax representations (MLRs)
are said to be gauge equivalent if one of them
can be obtained from the other by applying a matrix gauge transformation.
Generalizing and extending several previous works on MLRs and MTs,
we present new results on the following problems:

- •


When and how can one simplify a given MLR by means of gauge transformations?

- •


How can one use MLRs and gauge transformations for constructing MTs?

- •


A MLR is called fake if it is gauge equivalent to a trivial MLR.
How to determine whether a given MLR is not fake?


We consider the general (1+1)-dimensional evolutionary differential-difference case
when a MLR can depend on any shifts of dependent variables and can be non-autonomous.
As applications and illustrations of the presented general theory,
we construct several new two-component integrable equations (with new MLRs)
connected by new MTs to known integrable equations
from the papers \[S. Konstantinou-Rizos, A.V. Mikhailov, P. Xenitidis, _J. Math. Phys._ 2015\],
\[E. Mansfield, G. Marí Beffa, Jing Ping Wang, _Found. Comput. Math._ 2013\]),
including non-autonomous examples.

###### Key words and phrases:

Integrable differential-difference equations; matrix Lax representations; Lax pairs; gauge transformations; Miura-type transformations

###### 2020 Mathematics Subject Classification

37K60, 37K35

## 1\. Introduction

In this paper we study relations between
(1+1)-dimensional differential-difference matrix Lax representations (Lax pairs),
gauge transformations, and (discrete) Miura-type transformations,
which belong to the main tools in the theory of (1+1)-dimensional
integrable differential-difference equations.
Such equations occupy an important place in the modern theory of integrable systems
and its applications.
In particular, such equations arise in discretizations of integrable
partial differential equations (PDEs),
in discretizations of various differential geometric constructions
and as chains associated with Darboux and Bäcklund transformations of PDEs
(see, e.g., \[ [6](https://arxiv.org/html/2604.26870#bib.bib6 ""), [10](https://arxiv.org/html/2604.26870#bib.bib10 ""), [11](https://arxiv.org/html/2604.26870#bib.bib11 ""), [12](https://arxiv.org/html/2604.26870#bib.bib12 ""), [16](https://arxiv.org/html/2604.26870#bib.bib16 ""), [22](https://arxiv.org/html/2604.26870#bib.bib22 "")\]
and references therein).

In this paper, ℤ>0\\mathbb{Z}\_{>0} and ℤ≥0\\mathbb{Z}\_{\\geq 0} denote the sets of positive and nonnegative integers, respectively.
Let N∈ℤ>0N\\in\\mathbb{Z}\_{>0}. Below we consider an equation for an NN-component vector-function
u=(u1​(n,t),…,uN​(n,t))u=\\big(u^{1}(n,t),\\ldots,u^{N}(n,t)\\big)
of an integer variable nn and a real or complex variable tt.
For any fixed integer ℓ\\ell, we have uℓ=(uℓ1,…,uℓN)u\_{\\ell}=(u^{1}\_{\\ell},\\ldots,u^{N}\_{\\ell}),
where for each ξ=1,…,N\\xi=1,\\ldots,N the component uℓξu\_{\\ell}^{\\xi} is a function
of n,tn,t defined as follows uℓξ​(n,t)=uξ​(n+ℓ,t)u\_{\\ell}^{\\xi}(n,t)=u^{\\xi}(n\\!+\\!\\ell,t).
That is, uℓ​(n,t)=u⁡(n+ℓ,t)u\_{\\ell}(n,t)=u(n\\!+\\!\\ell,t). In particular, u0=uu\_{0}=u.

Let a,b∈ℤ{\\mathrm{a}},{\\mathrm{b}}\\in\\mathbb{Z}, a≤b\\,{\\mathrm{a}}\\leq{\\mathrm{b}}.
Consider a (1+1)-dimensional evolutionary differential-difference equation

|     |     |     |     |
| --- | --- | --- | --- |
| (1) |  | ∂t(u)=𝔽⁡(n,ua,ua+1,…,ub),\\displaystyle\\partial\_{t}(u)=\\mathbb{F}(n,u\_{\\mathrm{a}},u\_{{\\mathrm{a}}+1},\\ldots,u\_{\\mathrm{b}}), |  |

where 𝔽\\mathbb{F} is an NN-component vector-function 𝔽=(𝔽1,…,𝔽N)\\mathbb{F}=(\\mathbb{F}^{1},\\ldots,\\mathbb{F}^{N}),
which may depend on nn and on uℓu\_{\\ell} for ℓ=a,a+1,…,b\\ell={\\mathrm{a}},{{\\mathrm{a}}\\!+\\!1},\\ldots,{\\mathrm{b}}.

The differential-difference equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
is equivalent to the following infinite collection of differential equations

|     |     |     |     |
| --- | --- | --- | --- |
| (2) |  | ∂t(u⁡(n,t))=𝔽⁡(n,u⁡(n+a,t),u⁡(n+a+1,t),…,u⁡(n+b,t)),n∈ℤ.\\displaystyle\\partial\_{t}\\big(u(n,t)\\big)=\\mathbb{F}\\big(n,u(n\\!+\\!{\\mathrm{a}},t),u(n\\!+\\!{\\mathrm{a}}\\!+\\!1,t),\\ldots,u(n\\!+\\!{\\mathrm{b}},t)\\big),\\qquad\\quad n\\in\\mathbb{Z}. |  |

Using the components of u=(u1​(n,t),…,uN​(n,t))u=\\big(u^{1}(n,t),\\ldots,u^{N}(n,t)\\big)
and of 𝔽=(𝔽1,…,𝔽N)\\mathbb{F}=(\\mathbb{F}^{1},\\ldots,\\mathbb{F}^{N}), one can rewrite ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) as

|     |     |     |     |
| --- | --- | --- | --- |
| (3) |  | ∂t(ui)=𝔽i(n,ua,ua+1,…,ub),i=1,…,N.\\displaystyle\\partial\_{t}\\big(u^{i}\\big)=\\mathbb{F}^{i}(n,u\_{\\mathrm{a}},u\_{{\\mathrm{a}}+1},\\ldots,u\_{\\mathrm{b}}),\\qquad\\quad i=1,\\ldots,N. |  |

For each fixed ℓ∈ℤ\\ell\\in\\mathbb{Z}, replacing nn by n+ℓn+\\ell in ( [2](https://arxiv.org/html/2604.26870#S1.E2 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
we see that ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) implies

|     |     |     |     |
| --- | --- | --- | --- |
| (4) |  | ∂t(uℓi)=𝔽i(n+ℓ,ua+ℓ,ua+1+ℓ,…,ub+ℓ),i=1,…,N,ℓ∈ℤ.\\displaystyle\\partial\_{t}\\big(u^{i}\_{\\ell}\\big)=\\mathbb{F}^{i}(n\\!+\\!\\ell,u\_{{\\mathrm{a}}+\\ell},u\_{{\\mathrm{a}}+1+\\ell},\\ldots,u\_{{\\mathrm{b}}+\\ell}),\\qquad\\quad i=1,\\ldots,N,\\qquad\\ell\\in\\mathbb{Z}. |  |

We use the formal theory of (1+1)-dimensional evolutionary differential-difference equations, where one regards

|     |     |     |     |
| --- | --- | --- | --- |
| (5) |  | n,uℓ=(uℓ1,…,uℓN),ℓ∈ℤ,\\displaystyle n,\\qquad\\qquad u\_{\\ell}=(u^{1}\_{\\ell},\\ldots,u^{N}\_{\\ell}),\\quad\\ell\\in\\mathbb{Z}, |  |

as independent quantities.
Note that uℓ=(uℓ1,…,uℓN)u\_{\\ell}=(u^{1}\_{\\ell},\\ldots,u^{N}\_{\\ell})
are sometimes called _dynamical variables_.

In this paper, the notation of the type f=f⁡(n,uℓ,…)f=f(n,u\_{\\ell},\\ldots) means
that a function ff depends on a finite number of the variables ( [5](https://arxiv.org/html/2604.26870#S1.E5 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
The notation of the type f=f⁡(n,uα,…,uβ)f=f(n,u\_{\\upalpha},\\ldots,u\_{\\upbeta})
for some integers α≤β\\upalpha\\leq\\upbeta means that ff
may depend on nn and on uℓξu\_{\\ell}^{\\xi} for ℓ=α,…,β\\ell=\\upalpha,\\ldots,\\upbeta,
ξ=1,…,N\\,\\xi=1,\\ldots,N.

Equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) said to be _non-autonomous_
if its right-hand side 𝔽\\mathbb{F} depends nontrivially on nn.

We denote by 𝐒{\\mathbf{S}} the _shift operator_ with respect to the variable nn.
For any function g=g⁡(n,t)g=g(n,t) one has the function 𝐒⁡(g){\\mathbf{S}}(g)
such that 𝐒⁡(g)​(n,t)=g⁡(n+1,t){\\mathbf{S}}(g)(n,t)=g(n\\!+\\!1,t).
Furthermore, for each k∈ℤk\\in\\mathbb{Z}, we have the kkth power 𝐒k{\\mathbf{S}}^{k}
of the operator 𝐒{\\mathbf{S}} and the formula 𝐒k​(g)​(n,t)=g⁡(n+k,t){\\mathbf{S}}^{k}(g)(n,t)=g(n\\!+\\!k,t).

Since uℓu\_{\\ell} corresponds to u⁡(n+ℓ,t)u(n+\\ell,t), the operator 𝐒{\\mathbf{S}}
and its powers 𝐒k{\\mathbf{S}}^{k} for k∈ℤk\\in\\mathbb{Z} act on functions of
the variables ( [5](https://arxiv.org/html/2604.26870#S1.E5 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) by means of the rules

|     |     |     |
| --- | --- | --- |
|  | 𝐒(n)=n+1,𝐒(uℓ)=uℓ+1,𝐒k(n)=n+k,𝐒k(uℓ)=uℓ+k,𝐒k​(f⁡(n,uℓ,…))=f⁡(n+k,𝐒k​(uℓ),…).\\displaystyle\\begin{gathered}{\\mathbf{S}}(n)=n+1,\\qquad{\\mathbf{S}}(u\_{\\ell})=u\_{\\ell+1},\\qquad{\\mathbf{S}}^{k}(n)=n+k,\\qquad{\\mathbf{S}}^{k}(u\_{\\ell})=u\_{\\ell+k},\\\<br>{\\mathbf{S}}^{k}\\big(f(n,u\_{\\ell},\\ldots)\\big)=f(n\\!+\\!k,{\\mathbf{S}}^{k}(u\_{\\ell}),\\ldots).\\end{gathered} |  |

That is, applying 𝐒k{\\mathbf{S}}^{k} to a function f=f⁡(n,uℓ,…)f=f(n,u\_{\\ell},\\ldots),
we replace nn by n+kn\\!+\\!k in ff
and replace uℓξu\_{\\ell}^{\\xi} by uℓ+kξu\_{\\ell+k}^{\\xi} in ff for all ℓ∈ℤ\\ell\\in\\mathbb{Z},
ξ=1,…,N\\,\\xi=1,\\ldots,N.

The _total derivative operator 𝐃t\\mathbf{D}\_{t} corresponding to equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))_
acts on functions of the variables ( [5](https://arxiv.org/html/2604.26870#S1.E5 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) as follows

|     |     |     |     |
| --- | --- | --- | --- |
| (8) |  | 𝐃t​(f⁡(n,uℓ,…))=∑ℓ,ξ𝐒ℓ​(𝔽ξ)⋅∂f∂uℓξ,\\displaystyle\\mathbf{D}\_{t}\\big(f(n,u\_{\\ell},\\ldots)\\big)=\\sum\_{\\ell,\\xi}{\\mathbf{S}}^{\\ell}(\\mathbb{F}^{\\xi})\\cdot\\frac{\\partial f}{\\partial u\_{\\ell}^{\\xi}}, |  |

where 𝔽ξ=𝔽ξ​(n,ua,…,ub)\\mathbb{F}^{\\xi}=\\mathbb{F}^{\\xi}(n,u\_{\\mathrm{a}},\\ldots,u\_{\\mathrm{b}}), ξ=1,…,N\\,\\xi=1,\\ldots,N,
are the components of the vector-function
𝔽=(𝔽1,…,𝔽N)\\mathbb{F}=(\\mathbb{F}^{1},\\ldots,\\mathbb{F}^{N}) from ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Formula ( [8](https://arxiv.org/html/2604.26870#S1.E8 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) reflects the chain rule for the derivative with respect to tt,
taking into account equations ( [4](https://arxiv.org/html/2604.26870#S1.E4 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
From ( [1](https://arxiv.org/html/2604.26870#S1.EGx6 "1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [8](https://arxiv.org/html/2604.26870#S1.E8 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) it follows that, for any function h=h⁡(n,uℓ,…)h=h(n,u\_{\\ell},\\ldots),
one has 𝐃t​(𝐒⁡(h))=𝐒⁡(𝐃t​(h))\\mathbf{D}\_{t}\\big({\\mathbf{S}}(h)\\big)={\\mathbf{S}}\\big(\\mathbf{D}\_{t}(h)\\big).

In this paper, matrix-functions are sometimes called simply matrices.

###### Remark 1.

In this paper we deal with functions which may depend
on a finite number of the variables ( [5](https://arxiv.org/html/2604.26870#S1.E5 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and a complex parameter λ\\uplambda.
For simplicity of exposition, in order to present the main ideas clearly and concisely,
we consider only functions which depend rationally on
the variables ( [5](https://arxiv.org/html/2604.26870#S1.E5 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and meromorphically on λ\\uplambda, in the sense described below.
Many results of this paper can be extended to more general classes of functions,
but such extension requires more technical and heavy proofs.

A scalar (ℂ\\mathbb{C}-valued) function f=f⁡(n,uℓ,…,λ)f=f(n,u\_{\\ell},\\ldots,\\uplambda)
is said to be _of admissible type_ if ff can be written in the form

|     |     |     |     |
| --- | --- | --- | --- |
| (9) |  | f=g⁡(n,uℓ,…,λ)h⁡(n,uℓ,…,λ),\\displaystyle f=\\frac{g(n,u\_{\\ell},\\ldots,\\uplambda)}{h(n,u\_{\\ell},\\ldots,\\uplambda)}, |  |

where g⁡(n,uℓ,…,λ)g(n,u\_{\\ell},\\ldots,\\uplambda) and h⁡(n,uℓ,…,λ)h(n,u\_{\\ell},\\ldots,\\uplambda) are polynomials in the variables ( [5](https://arxiv.org/html/2604.26870#S1.E5 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
whose coefficients are meromorphic functions of λ∈ℂ\\uplambda\\in\\mathbb{C},
and h⁡(n,uℓ,…,λ)h(n,u\_{\\ell},\\ldots,\\uplambda) is not the zero polynomial.

We denote by ℳ​ℰ​ℛ​(ℂ,λ)\\mathcal{M\\!E\\!R}(\\mathbb{C},\\uplambda) the field of meromorphic functions of λ∈ℂ\\uplambda\\in\\mathbb{C}.
Then ( [9](https://arxiv.org/html/2604.26870#S1.E9 "In Remark 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) can be regarded as a rational function of n,uℓ=(uℓ1,…,uℓN)n,\\,u\_{\\ell}=(u^{1}\_{\\ell},\\ldots,u^{N}\_{\\ell})
with coefficients in ℳ​ℰ​ℛ​(ℂ,λ)\\mathcal{M\\!E\\!R}(\\mathbb{C},\\uplambda).
Thus, a scalar function f=f⁡(n,uℓ,…,λ)f=f(n,u\_{\\ell},\\ldots,\\uplambda) is of admissible type if ff
is a rational function of the variables ( [5](https://arxiv.org/html/2604.26870#S1.E5 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) with coefficients in ℳ​ℰ​ℛ​(ℂ,λ)\\mathcal{M\\!E\\!R}(\\mathbb{C},\\uplambda).

For each d∈ℤ>0\\mathrm{d}\\in\\mathbb{Z}\_{>0}, when we consider a d×d\\mathrm{d}\\times\\mathrm{d} matrix-function
𝐌=𝐌⁡(n,uℓ,…,λ)\\mathbf{M}=\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda), we assume that each entry of the matrix 𝐌\\mathbf{M}
is a scalar function of admissible type.
When we say that such a matrix 𝐌⁡(n,uℓ,…,λ)\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda) is assumed to be invertible,
we mean that the determinant det(𝐌⁡(n,uℓ,…,λ))\\det\\big(\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda)\\big) is not identically zero.
Then (det(𝐌⁡(n,uℓ,…,λ)))−1\\big(\\det\\big(\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda)\\big)\\big)^{-1} is well defined
(as a rational function of n,uℓ=(uℓ1,…,uℓN)n,\\,u\_{\\ell}=(u^{1}\_{\\ell},\\ldots,u^{N}\_{\\ell}) with coefficients in ℳ​ℰ​ℛ​(ℂ,λ)\\mathcal{M\\!E\\!R}(\\mathbb{C},\\uplambda)),
which allows us to compute the inverse matrix 𝐌−1=(𝐌⁡(n,uℓ,…,λ))−1\\mathbf{M}^{-1}=\\big(\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda)\\big)^{-1},
whose entries are of admissible type.

###### Definition 1.

Let d∈ℤ>0\\mathrm{d}\\in\\mathbb{Z}\_{>0}.
Let 𝐌=𝐌⁡(n,uℓ,…,λ)\\mathbf{M}=\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda) and 𝐔=𝐔⁡(n,uℓ,…,λ)\\mathbf{U}=\\mathbf{U}(n,u\_{\\ell},\\ldots,\\uplambda) be d×d\\mathrm{d}\\times\\mathrm{d} matrix-functions
depending on the variables ( [5](https://arxiv.org/html/2604.26870#S1.E5 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and a complex parameter λ\\uplambda.
Suppose that 𝐌\\mathbf{M} is invertible (in the sense of Remark [1](https://arxiv.org/html/2604.26870#Thmremark1 "Remark 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and we have

|     |     |     |     |
| --- | --- | --- | --- |
| (10) |  | 𝐃t​(𝐌)=𝐒⁡(𝐔)⋅𝐌−𝐌⋅𝐔,\\displaystyle\\mathbf{D}\_{t}(\\mathbf{M})={\\mathbf{S}}(\\mathbf{U})\\cdot\\mathbf{M}-\\mathbf{M}\\cdot\\mathbf{U}, |  |

where 𝐃t\\mathbf{D}\_{t} is given by ( [8](https://arxiv.org/html/2604.26870#S1.E8 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Then the pair (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}) is called a _matrix Lax representation_ (MLR) for equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

The connection between ( [10](https://arxiv.org/html/2604.26870#S1.E10 "In Definition 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is as follows.
The components 𝔽ξ\\mathbb{F}^{\\xi}, ξ=1,…,N\\,\\xi=1,\\ldots,N, of the right-hand side 𝔽⁡(n,ua,…,ub)\\mathbb{F}(n,u\_{\\mathrm{a}},\\ldots,u\_{\\mathrm{b}})
of ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) appear in formula ( [8](https://arxiv.org/html/2604.26870#S1.E8 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) for the operator 𝐃t\\mathbf{D}\_{t}, which is used in ( [10](https://arxiv.org/html/2604.26870#S1.E10 "In Definition 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

We say that a MLR (𝐌⁡(n,uℓ,…,λ),𝐔⁡(n,uℓ,…,λ))\\big(\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda),\\,\\mathbf{U}(n,u\_{\\ell},\\ldots,\\uplambda)\\big) is _non-autonomous_
if at least one of the matrix-functions 𝐌,𝐔\\mathbf{M},\\,\\mathbf{U} depends nontrivially on nn.

Correspondingly, a MLR (𝐌,𝐔)\\big(\\mathbf{M},\\mathbf{U}\\big) is called _autonomous_ if 𝐌,𝐔\\mathbf{M},\\,\\mathbf{U} do not depend on nn.

Relation ( [10](https://arxiv.org/html/2604.26870#S1.E10 "In Definition 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) implies that the following (overdetermined) auxiliary linear system

|     |     |     |     |
| --- | --- | --- | --- |
| (11) |  | 𝐒⁡(Ψ)=𝐌⋅Ψ,∂t(Ψ)=𝐔⋅Ψ\\displaystyle{\\mathbf{S}}(\\Psi)=\\mathbf{M}\\cdot\\Psi,\\qquad\\quad\\partial\_{t}(\\Psi)=\\mathbf{U}\\cdot\\Psi |  |

is compatible modulo equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Here Ψ=Ψ⁡(n,t)\\Psi=\\Psi(n,t) is an invertible d×d\\mathrm{d}\\times\\mathrm{d} matrix-function.

We say that the matrix 𝐌=𝐌⁡(n,uℓ,…,λ)\\mathbf{M}=\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda) is the _𝐒{\\mathbf{S}}-part_ of the MLR (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}).

Then for any invertible d×d\\mathrm{d}\\times\\mathrm{d} matrix-function
𝐆=𝐆⁡(n,uℓ,…,λ)\\mathbf{G}=\\mathbf{G}(n,u\_{\\ell},\\ldots,\\uplambda) the matrices

|     |     |     |     |
| --- | --- | --- | --- |
| (12) |  | 𝐌^=𝐒⁡(𝐆)⋅𝐌⋅𝐆−1,𝐔^=𝐃t​(𝐆)⋅𝐆−1+𝐆⋅𝐔⋅𝐆−1\\displaystyle\\widehat{\\mathbf{M}}={\\mathbf{S}}(\\mathbf{G})\\cdot\\mathbf{M}\\cdot\\mathbf{G}^{-1},\\qquad\\quad\\widehat{\\mathbf{U}}=\\mathbf{D}\_{t}(\\mathbf{G})\\cdot\\mathbf{G}^{-1}+\\mathbf{G}\\cdot\\mathbf{U}\\cdot\\mathbf{G}^{-1} |  |

form a MLR for equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) as well.
Here the matrix 𝐆=𝐆⁡(n,uℓ,…,λ)\\mathbf{G}=\\mathbf{G}(n,u\_{\\ell},\\ldots,\\uplambda)
is invertible in the sense of Remark [1](https://arxiv.org/html/2604.26870#Thmremark1 "Remark 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") and is called a _gauge transformation_.
The MLR (𝐌^,𝐔^)\\big(\\widehat{\\mathbf{M}},\\,\\widehat{\\mathbf{U}}\\big) is _gauge equivalent_
to the MLR (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}), and one can say that
(𝐌^,𝐔^)\\big(\\widehat{\\mathbf{M}},\\,\\widehat{\\mathbf{U}}\\big) is obtained from (𝐌,𝐔)(\\mathbf{M},\\mathbf{U})
by means of the gauge transformation 𝐆\\mathbf{G}.

###### Definition 2.

We consider MLRs for a given equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
A MLR (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}) is said to be _trivial_
if 𝐌\\mathbf{M} does not depend on uℓu\_{\\ell} for any ℓ∈ℤ\\ell\\in\\mathbb{Z}.
Then ( [8](https://arxiv.org/html/2604.26870#S1.E8 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) yields 𝐃t​(𝐌)=0\\mathbf{D}\_{t}(\\mathbf{M})=0, and from ( [10](https://arxiv.org/html/2604.26870#S1.E10 "In Definition 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) one derives
𝐒⁡(𝐔)=𝐌⋅𝐔⋅𝐌−1{\\mathbf{S}}(\\mathbf{U})=\\mathbf{M}\\cdot\\mathbf{U}\\cdot\\mathbf{M}^{-1}, which
implies that 𝐔\\mathbf{U} does not depend on uℓu\_{\\ell} either.
(One can show this easily, using the rules ( [1](https://arxiv.org/html/2604.26870#S1.EGx6 "1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))).
Hence a trivial MLR does not provide any information about equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

A MLR is called _fake_ if it is gauge equivalent to a trivial MLR.
That is, fake MLRs are obtained from trivial MLRs by applying gauge transformations,
and this can be done independently of equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

###### Definition 3.

Fix d∈ℤ>0\\mathrm{d}\\in\\mathbb{Z}\_{>0}.
Let 𝕎d\\mathbb{W}\_{\\mathrm{d}} be the vector space of all d×d\\mathrm{d}\\times\\mathrm{d} matrix-functions of the form Q=Q⁡(n,uℓ,…,λ)Q=Q(n,u\_{\\ell},\\ldots,\\uplambda).
Let 𝔹d⊂𝕎d\\mathbb{B}\_{\\mathrm{d}}\\subset\\mathbb{W}\_{\\mathrm{d}} be the subset of all invertible d×d\\mathrm{d}\\times\\mathrm{d} matrix-functions M=M⁡(n,uℓ,…,λ)M=M(n,u\_{\\ell},\\ldots,\\uplambda).
For each M∈𝔹dM\\in\\mathbb{B}\_{\\mathrm{d}}, we consider the operator ∇M:𝕎d→𝕎d\\nabla\_{M}\\colon\\mathbb{W}\_{\\mathrm{d}}\\to\\mathbb{W}\_{\\mathrm{d}} given by the formula

|     |     |     |     |
| --- | --- | --- | --- |
| (13) |  | ∇M(Q)=𝐒⁡(M−1​Q​M).\\displaystyle\\nabla\_{M}(Q)={\\mathbf{S}}(M^{-1}QM). |  |

The operator ∇M\\nabla\_{M} is invertible, and one has

|     |     |     |     |
| --- | --- | --- | --- |
| (14) |  | ∇M−1(Q)=M⋅𝐒−1​(Q)⋅M−1.\\displaystyle\\nabla\_{M}^{-1}(Q)=M\\cdot{\\mathbf{S}}^{-1}(Q)\\cdot M^{-1}. |  |

For each k∈ℤk\\in\\mathbb{Z}, we denote by ∇Mk\\nabla\_{M}^{k} the kkth power
of the operator ∇M\\nabla\_{M}. In particular, one has

|     |     |     |
| --- | --- | --- |
|  | ∇M0(Q)=Q,∇M2(Q)=∇M(∇M(Q))=𝐒⁡(M−1​𝐒​(M−1​Q​M)​M),\\displaystyle\\nabla\_{M}^{0}(Q)=Q,\\qquad\\quad\\nabla\_{M}^{2}(Q)=\\nabla\_{M}(\\nabla\_{M}(Q))={\\mathbf{S}}(M^{-1}{\\mathbf{S}}(M^{-1}QM)M), |  |
|  | ∇M−2(Q)=∇M−1(∇M−1(Q))=M​𝐒−1​(M​𝐒−1​(Q)​M−1)​M−1.\\displaystyle\\nabla\_{M}^{-2}(Q)=\\nabla\_{M}^{-1}(\\nabla\_{M}^{-1}(Q))=M{\\mathbf{S}}^{-1}(M{\\mathbf{S}}^{-1}(Q)M^{-1})M^{-1}. |  |

Furthermore, for each j=1,…,Nj=1,\\ldots,N, we consider the map 𝚫uj:𝔹d→𝕎d\\boldsymbol{\\Delta}^{u^{j}}\\colon\\mathbb{B}\_{\\mathrm{d}}\\to\\mathbb{W}\_{\\mathrm{d}} given by

|     |     |     |     |
| --- | --- | --- | --- |
| (15) |  | 𝚫uj(M)=∑ℓ∈ℤ∇M−ℓ(∂uℓj(M)⋅M−1),M=M(n,uℓ,…,λ)∈𝔹d,j=1,…,N.\\displaystyle\\boldsymbol{\\Delta}^{u^{j}}(M)=\\sum\_{\\ell\\in\\mathbb{Z}}\\nabla\_{M}^{-\\ell}\\big(\\partial\_{u^{j}\_{\\ell}}(M)\\cdot M^{-1}\\big),\\qquad\\quad M=M(n,u\_{\\ell},\\ldots,\\uplambda)\\in\\mathbb{B}\_{\\mathrm{d}},\\qquad j=1,\\ldots,N. |  |

For instance,
if M=M⁡(n,u−1ξ,u0ξ,u1ξ,λ)M=M\\big(n,u^{\\xi}\_{-1},u^{\\xi}\_{0},u^{\\xi}\_{1},\\uplambda\\big) depends only on nn, u−1ξu^{\\xi}\_{-1},
u0ξu^{\\xi}\_{0}, u1ξu^{\\xi}\_{1}, ξ=1,…,N\\,\\xi=1,\\ldots,N, and on λ\\uplambda, then

|     |     |     |
| --- | --- | --- |
|  | 𝚫uj​(M⁡(n,u−1ξ,u0ξ,u1ξ,λ))=∑ℓ∈ℤ∇M−ℓ(∂uℓj(M)⋅M−1)=∑ℓ=−1,0,1∇M−ℓ(∂uℓj(M)⋅M−1)==𝐒⁡(M−1​(∂u−1j(M)⋅M−1)​M)+∂u0j(M)⋅M−1+M​𝐒−1​(∂u1j(M)⋅M−1)​M−1.\\boldsymbol{\\Delta}^{u^{j}}\\big(M\\big(n,u^{\\xi}\_{-1},u^{\\xi}\_{0},u^{\\xi}\_{1},\\uplambda\\big)\\big)=\\sum\_{\\ell\\in\\mathbb{Z}}\\nabla\_{M}^{-\\ell}\\big(\\partial\_{u^{j}\_{\\ell}}(M)\\cdot M^{-1}\\big)=\\sum\_{\\ell=-1,0,1}\\nabla\_{M}^{-\\ell}\\big(\\partial\_{u^{j}\_{\\ell}}(M)\\cdot M^{-1}\\big)=\\\<br>={\\mathbf{S}}\\big(M^{-1}\\big(\\partial\_{u^{j}\_{-1}}(M)\\cdot M^{-1}\\big)M\\big)+\\partial\_{u^{j}\_{0}}(M)\\cdot M^{-1}+M{\\mathbf{S}}^{-1}\\big(\\partial\_{u^{j}\_{1}}(M)\\cdot M^{-1}\\big)M^{-1}. |  |

###### Definition 4.

Let α,β∈ℤ\\upalpha,\\upbeta\\in\\mathbb{Z}, α≤β\\,\\upalpha\\leq\\upbeta. A MLR (𝐌⁡(n,uℓ,…,λ),𝐔⁡(n,uℓ,…,λ))\\big(\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda),\\,\\mathbf{U}(n,u\_{\\ell},\\ldots,\\uplambda)\\big)
is said to be _of class (α,β)(\\upalpha,\\upbeta)_
if its 𝐒{\\mathbf{S}}-part𝐌⁡(n,uℓ,…,λ)\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda) is of the form 𝐌=𝐌⁡(n,uα,…,uβ,λ)\\mathbf{M}=\\mathbf{M}(n,u\_{\\upalpha},\\dots,u\_{\\upbeta},\\uplambda).
That is, a MLR (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}) is of class (α,β)(\\upalpha,\\upbeta) if 𝐌\\mathbf{M} may depend only on n,uα,…,uβ,λn,u\_{\\upalpha},\\dots,u\_{\\upbeta},\\uplambda,
while 𝐔\\mathbf{U} may depend on any finite number of the variables ( [5](https://arxiv.org/html/2604.26870#S1.E5 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and on λ\\uplambda.

Let α,β,q∈ℤ\\upalpha,\\upbeta,q\\in\\mathbb{Z}, α≤β\\,\\upalpha\\leq\\upbeta.
As shown in Lemma [1](https://arxiv.org/html/2604.26870#Thmlemma1 "Lemma 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") in Section [2](https://arxiv.org/html/2604.26870#S2 "2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"),
any MLR (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}) of class (α,β)(\\upalpha,\\upbeta) is gauge equivalent
to some MLR of class (α+q,β+q)(\\upalpha\\!+\\!q,\\upbeta\\!+\\!q)
with 𝐒{\\mathbf{S}}-part equal to 𝐒q​(𝐌){\\mathbf{S}}^{q}(\\mathbf{M}).
Therefore, since we want to study MLRs up to gauge equivalence,
it is sufficient to consider MLRs of class (0,k)(0,k) for k∈ℤ≥0k\\in\\mathbb{Z}\_{\\geq 0}.

In Section [2](https://arxiv.org/html/2604.26870#S2 "2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") we present the following results.

- •


Let p∈ℤ>0p\\in\\mathbb{Z}\_{>0}.
For a given MLR of class (0,p)(0,p) with 𝐒{\\mathbf{S}}-part 𝐌⁡(n,u0,u1,…,up,λ)\\mathbf{M}(n,u\_{0},u\_{1},\\ldots,u\_{p},\\uplambda),
Theorem [1](https://arxiv.org/html/2604.26870#Thmtheorem1 "Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") provides
a necessary and sufficient condition for the possibility to
simplify the MLR by means of gauge transformations in the following sense:


the possibility to eliminate the dependence on upu\_{p} in the 𝐒{\\mathbf{S}}-part
by applying a gauge transformation (i.e. to obtain a gauge equivalent MLR
with 𝐒{\\mathbf{S}}-part of the form 𝐌^​(n,u0,…,up−1,λ)\\widehat{\\mathbf{M}}(n,u\_{0},\\ldots,u\_{p-1},\\uplambda)).
If a MLR satisfies this condition (given in ( [27](https://arxiv.org/html/2604.26870#S2.E27 "In 2nd item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))),
then Theorem [1](https://arxiv.org/html/2604.26870#Thmtheorem1 "Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") provides an explicit formula
for a suitable gauge transformation (see ( [28](https://arxiv.org/html/2604.26870#S2.E28 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))).





In other words, if we have a MLR (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}) of class (0,p)(0,p), then
Theorem [1](https://arxiv.org/html/2604.26870#Thmtheorem1 "Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") gives a necessary and sufficient condition for
existence of a gauge transformation 𝐆=𝐆⁡(n,uℓ,…,λ)\\mathbf{G}=\\mathbf{G}(n,u\_{\\ell},\\ldots,\\uplambda)
such that the corresponding gauge equivalent MLR ( [12](https://arxiv.org/html/2604.26870#S1.E12 "In Definition 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is of class (0,p−1)(0,p\\!-\\!1).
Applications of this theorem are discussed below.





(Note that Theorem [1](https://arxiv.org/html/2604.26870#Thmtheorem1 "Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") in Section [2](https://arxiv.org/html/2604.26870#S2 "2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")
generalizes and extends \[ [7](https://arxiv.org/html/2604.26870#bib.bib7 ""), Theorem 1\],
since \[ [7](https://arxiv.org/html/2604.26870#bib.bib7 ""), Theorem 1\] considers only
autonomous MLRs and gives only a sufficient condition for the described problem
to simplify a MLR by means of gauge transformations.)

- •


For each j=1,…,Nj=1,\\ldots,N, using the map 𝚫uj:𝔹d→𝕎d\\boldsymbol{\\Delta}^{u^{j}}\\colon\\mathbb{B}\_{\\mathrm{d}}\\to\\mathbb{W}\_{\\mathrm{d}} defined by ( [15](https://arxiv.org/html/2604.26870#S1.E15 "In Definition 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
in Theorem [2](https://arxiv.org/html/2604.26870#Thmtheorem2 "Theorem 2. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") we obtain property ( [48](https://arxiv.org/html/2604.26870#S2.E48 "In Theorem 2. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), which essentially says the following:


when an invertible matrix M=M⁡(n,uℓ,…,λ)M=M(n,u\_{\\ell},\\ldots,\\uplambda) is transformed to
M~=𝐒⁡(G)⋅M⋅G−1\\widetilde{M}={\\mathbf{S}}(G)\\cdot M\\cdot G^{-1} by a gauge transformation G=G⁡(n,uℓ,…,λ)G=G(n,u\_{\\ell},\\ldots,\\uplambda),
the corresponding matrix 𝚫uj​(M~)\\boldsymbol{\\Delta}^{u^{j}}\\big(\\widetilde{M}\\big) can be obtained
from 𝚫uj​(M)\\boldsymbol{\\Delta}^{u^{j}}(M) by conjugation as follows
𝚫uj​(M~)=𝐒⁡(G)⋅𝚫uj​(M)⋅𝐒​(G)−1\\boldsymbol{\\Delta}^{u^{j}}\\big(\\widetilde{M}\\big)={\\mathbf{S}}(G)\\cdot\\boldsymbol{\\Delta}^{u^{j}}(M)\\cdot{\\mathbf{S}}(G)^{-1}.





Note that in Remark [2](https://arxiv.org/html/2604.26870#Thmremark2 "Remark 2. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")
we discuss relations of our results on differential-difference MLRs
with the results of S.Yu. Sakovich \[ [21](https://arxiv.org/html/2604.26870#bib.bib21 "")\]
and M. Marvan \[ [17](https://arxiv.org/html/2604.26870#bib.bib17 ""), [18](https://arxiv.org/html/2604.26870#bib.bib18 "")\]
on zero-curvature representations of partial differential equations.





Using Theorems [1](https://arxiv.org/html/2604.26870#Thmtheorem1 "Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"), [2](https://arxiv.org/html/2604.26870#Thmtheorem2 "Theorem 2. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") and Lemmas [1](https://arxiv.org/html/2604.26870#Thmlemma1 "Lemma 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")– [3](https://arxiv.org/html/2604.26870#Thmlemma3 "Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"),
we prove Theorem [3](https://arxiv.org/html/2604.26870#Thmtheorem3 "Theorem 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") described below.
Further applications of Theorem [2](https://arxiv.org/html/2604.26870#Thmtheorem2 "Theorem 2. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") are discussed in Remark [2](https://arxiv.org/html/2604.26870#Thmremark2 "Remark 2. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations").

- •


Theorem [3](https://arxiv.org/html/2604.26870#Thmtheorem3 "Theorem 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") says that a MLR (𝐌⁡(n,uℓ,…,λ),𝐔⁡(n,uℓ,…,λ))\\big(\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda),\\,\\mathbf{U}(n,u\_{\\ell},\\ldots,\\uplambda)\\big)
is gauge equivalent to a trivial MLR if and only if
one has 𝚫uj​(𝐌)=0\\boldsymbol{\\Delta}^{u^{j}}(\\mathbf{M})=0 for all j=1,…,Nj=1,\\ldots,N.
Therefore, a MLR (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}) is not fake (in the sense of Definition [2](https://arxiv.org/html/2604.26870#Thmdefinition2 "Definition 2. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
if and only if there is j∈{1,…,N}j\\in\\{1,\\ldots,N\\} such that 𝚫uj​(𝐌)≠0\\boldsymbol{\\Delta}^{u^{j}}(\\mathbf{M})\\neq 0.





Note that the question “how to determine whether a given MLR is not fake”
was studied in \[ [8](https://arxiv.org/html/2604.26870#bib.bib8 ""), Theorem 2\] for a much smaller class of MLRs
(namely, for MLRs with 𝐒{\\mathbf{S}}-part of the form 𝐌⁡(u0,u1,u2,λ)\\mathbf{M}(u\_{0},u\_{1},u\_{2},\\uplambda)), using a different method.


###### Remark 2.

Using Theorem [2](https://arxiv.org/html/2604.26870#Thmtheorem2 "Theorem 2. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") and other properties of the maps ∇M\\nabla\_{M}, 𝚫uj\\,\\boldsymbol{\\Delta}^{u^{j}}
discussed in Definition [3](https://arxiv.org/html/2604.26870#Thmdefinition3 "Definition 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") and in Section [2](https://arxiv.org/html/2604.26870#S2 "2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"),
in the preprint \[ [9](https://arxiv.org/html/2604.26870#bib.bib9 "")\] we introduce and study invariants
with respect to the action of gauge transformations on MLRs for
(1+1)-dimensional evolutionary differential-difference (semi-discrete) equations.
As explained in \[ [9](https://arxiv.org/html/2604.26870#bib.bib9 "")\],
our approach to gauge invariants for differential-difference (semi-discrete) MLRs
is inspired by the results of S.Yu. Sakovich \[ [21](https://arxiv.org/html/2604.26870#bib.bib21 "")\] and
M. Marvan \[ [17](https://arxiv.org/html/2604.26870#bib.bib17 ""), [18](https://arxiv.org/html/2604.26870#bib.bib18 "")\] on
gauge transformations and gauge invariants
for zero-curvature representations (ZCRs) of partial differential equations.

Also, as discussed in \[ [9](https://arxiv.org/html/2604.26870#bib.bib9 "")\],
our Definition [3](https://arxiv.org/html/2604.26870#Thmdefinition3 "Definition 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") and Theorems [2](https://arxiv.org/html/2604.26870#Thmtheorem2 "Theorem 2. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"), [3](https://arxiv.org/html/2604.26870#Thmtheorem3 "Theorem 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") in the differential-difference setting
are inspired by the approaches of S.Yu. Sakovich \[ [21](https://arxiv.org/html/2604.26870#bib.bib21 "")\]
and M. Marvan \[ [17](https://arxiv.org/html/2604.26870#bib.bib17 ""), [18](https://arxiv.org/html/2604.26870#bib.bib18 "")\] to ZCRs of partial differential equations.

###### Remark 3.

According to Definition [1](https://arxiv.org/html/2604.26870#Thmdefinition1 "Definition 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"),
in a MLR (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}) for equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
the matrix 𝐌=𝐌⁡(n,uℓ,…,λ)\\mathbf{M}=\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda) may depend on nn,
on a finite number of the
dynamical variables uℓ=(uℓ1,…,uℓN)u\_{\\ell}=(u^{1}\_{\\ell},\\ldots,u^{N}\_{\\ell}), ℓ∈ℤ\\,\\ell\\in\\mathbb{Z},
and a parameter λ\\uplambda. For any fixed integers q1,…,qNq\_{1},\\ldots,q\_{N}, we can relabel

|     |     |     |     |
| --- | --- | --- | --- |
| (16) |  | uℓ1↦uℓ+q11,…,uℓN↦uℓ+qNN∀ℓ∈ℤ.\\displaystyle u^{1}\_{\\ell}\\,\\mapsto\\,u^{1}\_{\\ell+q\_{1}},\\,\\quad\\ldots\\,\\quad,\\,\\quad u^{N}\_{\\ell}\\,\\mapsto\\,u^{N}\_{\\ell+q\_{N}}\\qquad\\quad\\forall\\,\\ell\\in\\mathbb{Z}. |  |

Relabeling ( [16](https://arxiv.org/html/2604.26870#S1.E16 "In Remark 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) means that in equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
we make the following invertible change of variables

|     |     |     |
| --- | --- | --- |
|  | u1​(n,t)↦u1​(n+q1,t),…,uN​(n,t)↦uN​(n+qN,t).\\displaystyle u^{1}(n,t)\\,\\mapsto\\,u^{1}(n\\!+\\!q\_{1},t),\\,\\quad\\ldots\\,\\quad,\\,\\quad u^{N}(n,t)\\,\\mapsto\\,u^{N}(n\\!+\\!q\_{N},t). |  |

Applying a relabeling ( [16](https://arxiv.org/html/2604.26870#S1.E16 "In Remark 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) with suitable fixed q1,…,qN∈ℤq\_{1},\\ldots,q\_{N}\\in\\mathbb{Z},
one can transform the matrix 𝐌\\mathbf{M} to the form
𝐌=𝐌⁡(n,u0,…,uk,λ)\\mathbf{M}=\\mathbf{M}(n,u\_{0},\\ldots,u\_{k},\\uplambda) for some k∈ℤ≥0k\\in\\mathbb{Z}\_{\\geq 0}
(so that the MLR becomes of class (0,k)(0,k)).

In what follows, for any function w=w⁡(n,t)w=w(n,t) and each ℓ∈ℤ\\ell\\in\\mathbb{Z},
we denote by wℓw\_{\\ell} the function wℓ​(n,t)=w⁡(n+ℓ,t)w\_{\\ell}(n,t)=w(n+\\ell,t).
That is, wℓ=𝐒ℓ​(w)w\_{\\ell}={\\mathbf{S}}^{\\ell}(w). In particular, w0=ww\_{0}=w.

Now let a~,b~∈ℤ{\\tilde{{\\mathrm{a}}}},{\\tilde{{\\mathrm{b}}}}\\in\\mathbb{Z}, a~≤b~\\,{\\tilde{{\\mathrm{a}}}}\\leq{\\tilde{{\\mathrm{b}}}},
and consider another (1+1)-dimensional evolutionary differential-difference equation

|     |     |     |     |
| --- | --- | --- | --- |
| (17) |  | ∂t(u~)=𝔽~​(n,u~a~,u~a~+1,…,u~b~)\\displaystyle\\partial\_{t}(\\tilde{u})=\\widetilde{\\mathbb{F}}(n,\\tilde{u}\_{\\tilde{{\\mathrm{a}}}},\\tilde{u}\_{{\\tilde{{\\mathrm{a}}}}+1},\\dots,\\tilde{u}\_{\\tilde{{\\mathrm{b}}}}) |  |

for an NN-component vector-function u~=(u~1​(n,t),…,u~N​(n,t))\\tilde{u}=\\big(\\tilde{u}^{1}(n,t),\\dots,\\tilde{u}^{N}(n,t)\\big).
In the right-hand side of ( [17](https://arxiv.org/html/2604.26870#S1.E17 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) one has
an NN-component vector-function 𝔽~=(𝔽~1,…,𝔽~N)\\widetilde{\\mathbb{F}}=\\big(\\widetilde{\\mathbb{F}}^{1},\\dots,\\widetilde{\\mathbb{F}}^{N}\\big).

###### Definition 5.

A _Miura-type transformation_ (MT) from equation ( [17](https://arxiv.org/html/2604.26870#S1.E17 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
to equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is determined by an expression of the form

|     |     |     |     |
| --- | --- | --- | --- |
| (18) |  | u=Φ⁡(n,u~ℓ,…)\\displaystyle u=\\Phi(n,\\tilde{u}\_{\\ell},\\dots) |  |

with the following requirements:

1. (1)


The right-hand side of ( [18](https://arxiv.org/html/2604.26870#S1.E18 "In Definition 5. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
is an NN-component vector-function Φ=(Φ1,…,ΦN)\\Phi=(\\Phi^{1},\\dots,\\Phi^{N})
which may depend on nn and on a finite number of the dynamical variables
u~ℓ=(u~ℓ1,…,u~ℓN)\\tilde{u}\_{\\ell}=\\big(\\tilde{u}^{1}\_{\\ell},\\dots,\\tilde{u}^{N}\_{\\ell}\\big), ℓ∈ℤ\\,\\ell\\in\\mathbb{Z}.

2. (2)


If u~=u~​(n,t)\\tilde{u}=\\tilde{u}(n,t) satisfies equation ( [17](https://arxiv.org/html/2604.26870#S1.E17 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
then u=u⁡(n,t)u=u(n,t) determined by ( [18](https://arxiv.org/html/2604.26870#S1.E18 "In Definition 5. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) satisfies equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).


More precisely, the second requirement means that we must have relations ( [20](https://arxiv.org/html/2604.26870#S1.E20 "In Definition 5. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) explained below.
The components of the vector formula ( [18](https://arxiv.org/html/2604.26870#S1.E18 "In Definition 5. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) are

|     |     |     |     |
| --- | --- | --- | --- |
| (19) |  | ui=Φi(n,u~ℓξ,…),i=1,…,N.\\displaystyle u^{i}=\\Phi^{i}\\big(n,\\tilde{u}^{\\xi}\_{\\ell},\\dots\\big),\\qquad\\quad i=1,\\dots,N. |  |

Recall that ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is equivalent to ( [3](https://arxiv.org/html/2604.26870#S1.E3 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Substituting the right-hand side of ( [19](https://arxiv.org/html/2604.26870#S1.E19 "In Definition 5. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) in place of uiu^{i} in ( [3](https://arxiv.org/html/2604.26870#S1.E3 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (20) |  | 𝐃~t(Φi(n,u~ℓξ,…))=𝔽i(n,𝐒a(Φ),𝐒a+1(Φ),…,𝐒b(Φ)),i=1,…,N,\\displaystyle\\widetilde{\\mathbf{D}}\_{t}\\big(\\Phi^{i}\\big(n,\\tilde{u}^{\\xi}\_{\\ell},\\dots\\big)\\big)=\\mathbb{F}^{i}\\big(n,{\\mathbf{S}}^{\\mathrm{a}}(\\Phi),{\\mathbf{S}}^{{\\mathrm{a}}+1}(\\Phi),\\dots,{\\mathbf{S}}^{\\mathrm{b}}(\\Phi)\\big),\\qquad\\quad i=1,\\dots,N, |  |

which must be valid identically in the variables nn and u~ℓξ\\tilde{u}^{\\xi}\_{\\ell}.
Here 𝐃~t\\widetilde{\\mathbf{D}}\_{t} is the total derivative operator corresponding to ( [17](https://arxiv.org/html/2604.26870#S1.E17 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
so that in the left-hand side of ( [20](https://arxiv.org/html/2604.26870#S1.E20 "In Definition 5. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) we have
𝐃~t​(Φi​(n,u~ℓξ,…))=∑ℓ,ξ𝐒ℓ​(𝔽~ξ)⋅(∂Φi/∂u~ℓξ)\\widetilde{\\mathbf{D}}\_{t}\\big(\\Phi^{i}\\big(n,\\tilde{u}^{\\xi}\_{\\ell},\\dots\\big)\\big)=\\sum\_{\\ell,\\xi}{\\mathbf{S}}^{\\ell}\\big(\\widetilde{\\mathbb{F}}^{\\xi}\\big)\\cdot\\big({\\partial\\Phi^{i}}/{\\partial\\tilde{u}^{\\xi}\_{\\ell}}\\big),
where 𝔽~ξ=𝔽~ξ​(n,u~a~,…,u~b~)\\widetilde{\\mathbb{F}}^{\\xi}=\\widetilde{\\mathbb{F}}^{\\xi}\\big(n,\\tilde{u}\_{\\tilde{{\\mathrm{a}}}},\\dots,\\tilde{u}\_{\\tilde{{\\mathrm{b}}}}\\big),
ξ=1,…,N\\,\\xi=1,\\ldots,N, are the components of the vector-function
𝔽~=(𝔽~1,…,𝔽~N)\\widetilde{\\mathbb{F}}=\\big(\\widetilde{\\mathbb{F}}^{1},\\dots,\\widetilde{\\mathbb{F}}^{N}\\big) from ( [17](https://arxiv.org/html/2604.26870#S1.E17 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

MTs for differential-difference equations
are a discrete analog of MTs for partial differential equations \[ [19](https://arxiv.org/html/2604.26870#bib.bib19 "")\].
MTs for partial differential equations are sometimes called _differential substitutions_.

###### Definition 6.

We consider MLRs for a given equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) imposed
on an NN-component vector-function u=(u1,…,uN)u=(u^{1},\\ldots,u^{N}).
We say that a MLR (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}) is _uu-tame_
if its 𝐒{\\mathbf{S}}-part is of the form 𝐌=𝐌⁡(n,u0,λ)\\mathbf{M}=\\mathbf{M}(n,u\_{0},\\uplambda).
That is, (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}) is uu-tame if 𝐌\\mathbf{M} may depend only on nn,
u0=(u01,…,u0N)u\_{0}=(u^{1}\_{0},\\ldots,u^{N}\_{0}), λ\\uplambda.

###### Remark 4.

Consider a uu-tame MLR (𝐌⁡(n,u0,λ),𝐔⁡(n,uℓ,…,λ))\\big(\\mathbf{M}(n,u\_{0},\\uplambda),\\,\\mathbf{U}(n,u\_{\\ell},\\ldots,\\uplambda)\\big).
Let G=G⁡(n,λ)G=G(n,\\uplambda) be a gauge transformation such that GG may depend only on n,λn,\\,\\uplambda.
Then the corresponding gauge equivalent MLR

|     |     |     |
| --- | --- | --- |
|  | 𝐌ˇ=𝐒⁡(G)⋅𝐌⋅G−1,𝐔ˇ=𝐃t​(G)⋅G−1+G⋅𝐔⋅G−1\\displaystyle\\check{\\mathbf{M}}={\\mathbf{S}}(G)\\cdot\\mathbf{M}\\cdot G^{-1},\\qquad\\quad\\check{\\mathbf{U}}=\\mathbf{D}\_{t}(G)\\cdot G^{-1}+G\\cdot\\mathbf{U}\\cdot G^{-1} |  |

is uu-tame as well, since its 𝐒{\\mathbf{S}}-part is
𝐌ˇ=𝐒⁡(G)⋅𝐌⋅G−1=G⁡(n+1,λ)⋅𝐌⁡(n,u0,λ)⋅G​(n,λ)−1\\check{\\mathbf{M}}={\\mathbf{S}}(G)\\cdot\\mathbf{M}\\cdot G^{-1}=G(n\\!+\\!1,\\uplambda)\\cdot\\mathbf{M}(n,u\_{0},\\uplambda)\\cdot G(n,\\uplambda)^{-1}.

The following observation is well known:

when one makes a classification for some class
of integrable (partial differential, difference or differential-difference)
equations with two independent variables,
it is often possible to select a few basic equations (with some parameters)
such that all the other equations from the considered class can be derived from
the basic ones by means of MTs
(see, e.g., \[ [2](https://arxiv.org/html/2604.26870#bib.bib2 ""), [14](https://arxiv.org/html/2604.26870#bib.bib14 ""), [23](https://arxiv.org/html/2604.26870#bib.bib23 ""), [4](https://arxiv.org/html/2604.26870#bib.bib4 ""), [5](https://arxiv.org/html/2604.26870#bib.bib5 ""), [13](https://arxiv.org/html/2604.26870#bib.bib13 ""), [12](https://arxiv.org/html/2604.26870#bib.bib12 "")\]
and references therein).
Also, it is well known that MTs often help to obtain conservation laws
and Bäcklund transformations for equations of various types
(see, e.g., \[ [20](https://arxiv.org/html/2604.26870#bib.bib20 ""), [22](https://arxiv.org/html/2604.26870#bib.bib22 ""), [6](https://arxiv.org/html/2604.26870#bib.bib6 ""), [12](https://arxiv.org/html/2604.26870#bib.bib12 "")\]).
Hence it is desirable to develop constructions of MTs.

In Section [3](https://arxiv.org/html/2604.26870#S3 "3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") we demonstrate a technique to construct MTs
(including non-autonomous examples)
by means of MLRs and gauge transformations, using the following steps:

- •


Having a MLR, which is not necessarily uu-tame, we first try to bring it
to a uu-tame form, using a relabeling from Remark [3](https://arxiv.org/html/2604.26870#Thmremark3 "Remark 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") and
gauge transformations 𝐆⁡(n,uℓ,…,λ)\\mathbf{G}(n,u\_{\\ell},\\ldots,\\uplambda) from Theorem [1](https://arxiv.org/html/2604.26870#Thmtheorem1 "Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations").

- •


Having obtained a uu-tame MLR
(𝐌⁡(n,u0,λ),𝐔⁡(n,uℓ,…,λ))\\big(\\mathbf{M}(n,u\_{0},\\uplambda),\\,\\mathbf{U}(n,u\_{\\ell},\\ldots,\\uplambda)\\big), we try to simplify it by means of
gauge transformations of the form G⁡(n,λ)G(n,\\uplambda) depending only on n,λn,\\,\\uplambda
in agreement with Remark [4](https://arxiv.org/html/2604.26870#Thmremark4 "Remark 4. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations").

- •


After that, one can often derive MTs
by means of reductions of the auxiliary system ( [11](https://arxiv.org/html/2604.26870#S1.E11 "In Definition 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
corresponding to the obtained simplified MLR.
(Note that, in some examples in Section [3](https://arxiv.org/html/2604.26870#S3 "3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"), we use u~\\tilde{u} instead of uu.)


This technique extends the methods of \[ [7](https://arxiv.org/html/2604.26870#bib.bib7 ""), [8](https://arxiv.org/html/2604.26870#bib.bib8 ""), [1](https://arxiv.org/html/2604.26870#bib.bib1 "")\],
since in \[ [7](https://arxiv.org/html/2604.26870#bib.bib7 ""), [8](https://arxiv.org/html/2604.26870#bib.bib8 ""), [1](https://arxiv.org/html/2604.26870#bib.bib1 "")\] only the autonomous case was considered.

As applications and illustrations of the presented general theory on MLRs,
we construct several new integrable equations (with new MLRs) connected
by new MTs to known integrable equations from \[ [11](https://arxiv.org/html/2604.26870#bib.bib11 ""), [16](https://arxiv.org/html/2604.26870#bib.bib16 "")\].
Namely, in Section [3](https://arxiv.org/html/2604.26870#S3 "3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") we obtain the following results.

- •


We consider the integrable
22-component (non-autonomous differential-difference) equation ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) with
the MLR ( [68](https://arxiv.org/html/2604.26870#S3.E68 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), which were derived by
S. Konstantinou-Rizos, A.V. Mikhailov, P. Xenitidis \[ [11](https://arxiv.org/html/2604.26870#bib.bib11 "")\]
in a study of Darboux transformations for a Lax operator
of the (partial differential) nonlinear Schrödinger equation.
In ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [68](https://arxiv.org/html/2604.26870#S3.E68 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) one has an arbitrary function α⁡(n)\\upalpha(n).
(Equation ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is given in \[ [11](https://arxiv.org/html/2604.26870#bib.bib11 ""), page 7\] in different notation,
using functions p⁡(n,x)p(n,x), q⁡(n,x)q(n,x), instead of u1​(n,t)u^{1}(n,t), u2​(n,t)u^{2}(n,t).)





We construct new integrable 22-component
(non-autonomous differential-difference) equations ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
and new MTs ( [89](https://arxiv.org/html/2604.26870#S3.E89 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [110](https://arxiv.org/html/2604.26870#S3.E110 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
The MT ( [89](https://arxiv.org/html/2604.26870#S3.E89 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is from ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
while the MT ( [110](https://arxiv.org/html/2604.26870#S3.E110 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is from ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
This implies that the composition of the MTs ( [89](https://arxiv.org/html/2604.26870#S3.E89 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [110](https://arxiv.org/html/2604.26870#S3.E110 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
gives a MT from ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).





In formulas ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [89](https://arxiv.org/html/2604.26870#S3.E89 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [110](https://arxiv.org/html/2604.26870#S3.E110 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) we have arbitrary constants c,q∈ℂ\\mathrm{c},\\mathrm{q}\\in\\mathbb{C}.
In ( [110](https://arxiv.org/html/2604.26870#S3.E110 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) we have also functions 𝕏\\mathbb{X}, 𝕐\\mathbb{Y} given by ( [109](https://arxiv.org/html/2604.26870#S3.E109 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Furthermore, in ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) one has the function ℍ\\mathbb{H} obtained by substituting ( [111](https://arxiv.org/html/2604.26870#S3.E111 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
in the right-hand side of the second component of ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
(We do not present the explicit formula for ℍ\\mathbb{H}, since it is rather cumbersome.)

- •


We consider also the integrable equation ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) derived by
E. Mansfield, G. Marí Beffa, Jing Ping Wang \[ [16](https://arxiv.org/html/2604.26870#bib.bib16 ""), Section 5.1.1\]
in a study of invariant time evolutions of polygons in the centro-affine plane.
As shown in \[ [16](https://arxiv.org/html/2604.26870#bib.bib16 ""), Section 5.1.1\], one has the MT ( [115](https://arxiv.org/html/2604.26870#S3.E115 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
from ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to equation ( [116](https://arxiv.org/html/2604.26870#S3.E116 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
which is the Toda lattice in the Flaschka–Manakov coordinates \[ [3](https://arxiv.org/html/2604.26870#bib.bib3 ""), [15](https://arxiv.org/html/2604.26870#bib.bib15 "")\].





We construct a new integrable 22-component equation ( [128](https://arxiv.org/html/2604.26870#S3.E128 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
and a new MT ( [126](https://arxiv.org/html/2604.26870#S3.E126 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) from ( [128](https://arxiv.org/html/2604.26870#S3.E128 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
The composition of the MTs ( [115](https://arxiv.org/html/2604.26870#S3.E115 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [126](https://arxiv.org/html/2604.26870#S3.E126 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) gives a MT from ( [128](https://arxiv.org/html/2604.26870#S3.E128 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
to the Toda lattice ( [116](https://arxiv.org/html/2604.26870#S3.E116 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

- •


Furthermore, we obtain several new MLRs:


the MLR ( [100](https://arxiv.org/html/2604.26870#S3.E100 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) for equation ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), the MLR ( [120](https://arxiv.org/html/2604.26870#S3.E120 "In 3rd item ‣ 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) for equation ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
and the MLRs described in Remarks [6](https://arxiv.org/html/2604.26870#Thmremark6 "Remark 6. ‣ 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"), [7](https://arxiv.org/html/2604.26870#Thmremark7 "Remark 7. ‣ 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") for equations ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [128](https://arxiv.org/html/2604.26870#S3.E128 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Each of these MLRs has a parameter λ∈ℂ\\uplambda\\in\\mathbb{C}.


The constructed equations ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [128](https://arxiv.org/html/2604.26870#S3.E128 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) are integrable
for the following reasons:

- •


As explained above, equations ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) are connected by MTs
to the integrable equation ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) from \[ [11](https://arxiv.org/html/2604.26870#bib.bib11 "")\],
while ( [128](https://arxiv.org/html/2604.26870#S3.E128 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is connected by MTs
to the integrable equation ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) from \[ [16](https://arxiv.org/html/2604.26870#bib.bib16 ""), Section 5.1.1\]
and to the Toda lattice ( [116](https://arxiv.org/html/2604.26870#S3.E116 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

- •


As discussed above, each of equations ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [128](https://arxiv.org/html/2604.26870#S3.E128 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
possesses a MLR with parameter λ∈ℂ\\uplambda\\in\\mathbb{C}.


## 2\. General results on differential-difference matrix Lax representations

Let d∈ℤ>0\\mathrm{d}\\in\\mathbb{Z}\_{>0}.
In this section, all matrix-functions (including gauge transformations)
are of size d×d\\mathrm{d}\\times\\mathrm{d}.

###### Lemma 1.

Let α,β∈ℤ\\upalpha,\\upbeta\\in\\mathbb{Z}, α≤β\\,\\upalpha\\leq\\upbeta.
Let (𝐌⁡(n,uα,…,uβ,λ),𝐔⁡(n,uℓ,…,λ))\\big(\\mathbf{M}(n,u\_{\\upalpha},\\dots,u\_{\\upbeta},\\uplambda),\\,\\mathbf{U}(n,u\_{\\ell},\\ldots,\\uplambda)\\big) be a MLR of class (α,β)(\\upalpha,\\upbeta).
Since the matrix 𝐌=𝐌⁡(n,uα,…,uβ,λ)\\mathbf{M}=\\mathbf{M}(n,u\_{\\upalpha},\\dots,u\_{\\upbeta},\\uplambda) is invertible,
we can consider the gauge transformations

|     |     |     |     |
| --- | --- | --- | --- |
| (21) |  | G:=𝐌,G˘:=𝐒−1​(𝐌−1)\\displaystyle\\mathrm{G}:=\\mathbf{M},\\qquad\\quad\\breve{\\mathrm{G}}:={\\mathbf{S}}^{-1}(\\mathbf{M}^{-1}) |  |

and the corresponding gauge equivalent MLRs

|     |     |     |     |
| --- | --- | --- | --- |
| (22) |  | 𝐌^:=𝐒⁡(G)⋅𝐌⋅G−1,𝐔^:=𝐃t​(G)⋅G−1+G⋅𝐔⋅G−1,\\displaystyle\\widehat{\\mathbf{M}}:={\\mathbf{S}}(\\mathrm{G})\\cdot\\mathbf{M}\\cdot\\mathrm{G}^{-1},\\qquad\\quad\\widehat{\\mathbf{U}}:=\\mathbf{D}\_{t}(\\mathrm{G})\\cdot\\mathrm{G}^{-1}+\\mathrm{G}\\cdot\\mathbf{U}\\cdot\\mathrm{G}^{-1}, |  |
| (23) |  | 𝐌˘:=𝐒⁡(G˘)⋅𝐌⋅G˘−1,𝐔˘:=𝐃t​(G˘)⋅G˘−1+G˘⋅𝐔⋅G˘−1.\\displaystyle\\breve{\\mathbf{M}}:={\\mathbf{S}}\\big(\\breve{\\mathrm{G}}\\big)\\cdot\\mathbf{M}\\cdot\\breve{\\mathrm{G}}^{-1},\\qquad\\quad\\breve{\\mathbf{U}}:=\\mathbf{D}\_{t}\\big(\\breve{\\mathrm{G}}\\big)\\cdot\\breve{\\mathrm{G}}^{-1}+\\breve{\\mathrm{G}}\\cdot\\mathbf{U}\\cdot\\breve{\\mathrm{G}}^{-1}. |  |

Then we have

|     |     |     |     |
| --- | --- | --- | --- |
| (24) |  | 𝐌^=𝐒⁡(𝐌),𝐌˘=𝐒−1​(𝐌),\\displaystyle\\widehat{\\mathbf{M}}={\\mathbf{S}}(\\mathbf{M}),\\qquad\\quad\\breve{\\mathbf{M}}={\\mathbf{S}}^{-1}(\\mathbf{M}), |  |

which implies that the MLR ( [22](https://arxiv.org/html/2604.26870#S2.E22 "In Lemma 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is of class (α+1,β+1)(\\upalpha\\!+\\!1,\\upbeta\\!+\\!1), and
the MLR ( [23](https://arxiv.org/html/2604.26870#S2.E23 "In Lemma 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is of class (α−1,β−1)(\\upalpha\\!-\\!1,\\upbeta\\!-\\!1).

Furthermore, for each q∈ℤq\\in\\mathbb{Z}, the considered MLR (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}) of class (α,β)(\\upalpha,\\upbeta)
is gauge equivalent to some MLR of class (α+q,β+q)(\\upalpha\\!+\\!q,\\upbeta\\!+\\!q)
with 𝐒{\\mathbf{S}}-part equal to 𝐒q​(𝐌){\\mathbf{S}}^{q}(\\mathbf{M}).

###### Proof.

Substituting ( [21](https://arxiv.org/html/2604.26870#S2.E21 "In Lemma 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) in ( [22](https://arxiv.org/html/2604.26870#S2.E22 "In Lemma 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [23](https://arxiv.org/html/2604.26870#S2.E23 "In Lemma 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we get ( [24](https://arxiv.org/html/2604.26870#S2.E24 "In Lemma 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Therefore, the MLR (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}) of class (α,β)(\\upalpha,\\upbeta) is gauge equivalent
to the MLR ( [22](https://arxiv.org/html/2604.26870#S2.E22 "In Lemma 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) of class (α+1,β+1)(\\upalpha\\!+\\!1,\\upbeta\\!+\\!1) with 𝐒{\\mathbf{S}}-part equal to 𝐒⁡(𝐌){\\mathbf{S}}(\\mathbf{M})
and is gauge equivalent to the MLR ( [23](https://arxiv.org/html/2604.26870#S2.E23 "In Lemma 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) of class (α−1,β−1)(\\upalpha\\!-\\!1,\\upbeta\\!-\\!1)
with 𝐒{\\mathbf{S}}-part equal to 𝐒−1​(𝐌){\\mathbf{S}}^{-1}(\\mathbf{M}).

Now, the last statement of the lemma can be proved easily by induction on qq.
∎

###### Remark 5.

In Theorem [1](https://arxiv.org/html/2604.26870#Thmtheorem1 "Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") below,
we consider an invertible d×d\\mathrm{d}\\times\\mathrm{d} matrix-function

|     |     |     |
| --- | --- | --- |
|  | 𝐌=𝐌⁡(n,u0,u1,…,up,λ)\\mathbf{M}=\\mathbf{M}(n,u\_{0},u\_{1},\\ldots,u\_{p},\\uplambda) |  |

with p∈ℤ>0p\\in\\mathbb{Z}\_{>0}, and we need to choose a constant vector a0∈ℂNa\_{0}\\in\\mathbb{C}^{N} so that
the matrix 𝐌⁡(n,a0,u1,…,up,λ)\\mathbf{M}(n,a\_{0},u\_{1},\\ldots,u\_{p},\\uplambda) is well defined and is invertible.
Here 𝐌⁡(n,a0,u1,…,up,λ)\\mathbf{M}(n,a\_{0},u\_{1},\\ldots,u\_{p},\\uplambda) is obtained from 𝐌⁡(n,u0,u1,…,up,λ)\\mathbf{M}(n,u\_{0},u\_{1},\\ldots,u\_{p},\\uplambda)
by substituting u0=a0u\_{0}=a\_{0}.
The term “invertible” is understood in the sense of Remark [1](https://arxiv.org/html/2604.26870#Thmremark1 "Remark 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations").

For a given invertible matrix 𝐌⁡(n,u0,…,up,λ)\\mathbf{M}(n,u\_{0},\\ldots,u\_{p},\\uplambda),
such a vector a0∈ℂNa\_{0}\\in\\mathbb{C}^{N} can be chosen as follows.
For i,j∈{1,…,d}i,j\\in\\{1,\\ldots,\\mathrm{d}\\} the (i,j)(i,j) entry of the matrix 𝐌\\mathbf{M}
is denoted by 𝐦i​j=𝐦i​j​(n,u0,…,up,λ)\\mathbf{m}^{ij}=\\mathbf{m}^{ij}(n,u\_{0},\\ldots,u\_{p},\\uplambda).
Since, according to Remark [1](https://arxiv.org/html/2604.26870#Thmremark1 "Remark 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"), 𝐦i​j​(n,u0,…,up,λ)\\mathbf{m}^{ij}(n,u\_{0},\\ldots,u\_{p},\\uplambda)
is assumed to be a rational function of n,uℓ=(uℓ1,…,uℓN)n,\\,u\_{\\ell}=(u^{1}\_{\\ell},\\ldots,u^{N}\_{\\ell})
with coefficients in ℳ​ℰ​ℛ​(ℂ,λ)\\mathcal{M\\!E\\!R}(\\mathbb{C},\\uplambda), where ℳ​ℰ​ℛ​(ℂ,λ)\\mathcal{M\\!E\\!R}(\\mathbb{C},\\uplambda) is the field of meromorphic functions of λ∈ℂ\\uplambda\\in\\mathbb{C}, we have

|     |     |     |
| --- | --- | --- |
|  | 𝐦i​j​(n,u0,…,up,λ)=fi​j​(n,u0,…,up,λ)gi​j​(n,u0,…,up,λ),i,j=1,…,d,\\displaystyle\\mathbf{m}^{ij}(n,u\_{0},\\ldots,u\_{p},\\uplambda)=\\frac{f^{ij}(n,u\_{0},\\ldots,u\_{p},\\uplambda)}{g^{ij}(n,u\_{0},\\ldots,u\_{p},\\uplambda)},\\quad\\qquad i,j=1,\\ldots,\\mathrm{d}, |  |
|  | det(𝐌⁡(n,u0,…,up,λ))=P⁡(n,u0,…,up,λ)Q⁡(n,u0,…,up,λ),\\displaystyle\\det\\big(\\mathbf{M}(n,u\_{0},\\ldots,u\_{p},\\uplambda)\\big)=\\frac{P(n,u\_{0},\\ldots,u\_{p},\\uplambda)}{Q(n,u\_{0},\\ldots,u\_{p},\\uplambda)}, |  |

where

- •


fi​j​(n,u0,…,up,λ)f^{ij}(n,u\_{0},\\ldots,u\_{p},\\uplambda), gi​j​(n,u0,…,up,λ)\\,g^{ij}(n,u\_{0},\\ldots,u\_{p},\\uplambda),
P⁡(n,u0,…,up,λ)\\,P(n,u\_{0},\\ldots,u\_{p},\\uplambda), Q⁡(n,u0,…,up,λ)\\,Q(n,u\_{0},\\ldots,u\_{p},\\uplambda)
are some polynomials in the variables n,uℓ=(uℓ1,…,uℓN)n,\\,u\_{\\ell}=(u^{1}\_{\\ell},\\ldots,u^{N}\_{\\ell}) with coefficients in ℳ​ℰ​ℛ​(ℂ,λ)\\mathcal{M\\!E\\!R}(\\mathbb{C},\\uplambda),

- •


each of the polynomials



|     |     |     |
| --- | --- | --- |
|  | gi​j​(n,u0,u1,…,up,λ),i,j=1,…,d,P⁡(n,u0,u1,…,up,λ),Q⁡(n,u0,u1,…,up,λ)\\displaystyle g^{ij}(n,u\_{0},u\_{1},\\ldots,u\_{p},\\uplambda),\\qquad i,j=1,\\ldots,\\mathrm{d},\\qquad P(n,u\_{0},u\_{1},\\ldots,u\_{p},\\uplambda),\\qquad Q(n,u\_{0},u\_{1},\\ldots,u\_{p},\\uplambda) |  |



is not the zero polynomial.


Then there is an open dense subset W⊂ℂNW\\subset\\mathbb{C}^{N} such that
for any constant vector a0∈Wa\_{0}\\in W each of the polynomials

|     |     |     |
| --- | --- | --- |
|  | gi​j​(n,a0,u1,…,up,λ),i,j=1,…,d,P⁡(n,a0,u1,…,up,λ),Q⁡(n,a0,u1,…,up,λ)\\displaystyle g^{ij}(n,a\_{0},u\_{1},\\ldots,u\_{p},\\uplambda),\\qquad i,j=1,\\ldots,\\mathrm{d},\\qquad P(n,a\_{0},u\_{1},\\ldots,u\_{p},\\uplambda),\\qquad Q(n,a\_{0},u\_{1},\\ldots,u\_{p},\\uplambda) |  |

is not the zero polynomial (as a polynomial in n,uℓn,\\,u\_{\\ell}).
This implies that for any a0∈Wa\_{0}\\in W
the matrix 𝐌⁡(n,a0,u1,…,up,λ)\\mathbf{M}(n,a\_{0},u\_{1},\\ldots,u\_{p},\\uplambda) is well defined and is invertible
(in the sense of Remark [1](https://arxiv.org/html/2604.26870#Thmremark1 "Remark 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

###### Theorem 1.

Let p∈ℤ>0p\\in\\mathbb{Z}\_{>0}.
Consider an invertible d×d\\mathrm{d}\\times\\mathrm{d} matrix-function 𝐌=𝐌⁡(n,u0,u1,…,up,λ)\\mathbf{M}=\\mathbf{M}(n,u\_{0},u\_{1},\\ldots,u\_{p},\\uplambda).
The following two properties are equivalent.

- •


Property 1.
There is a gauge transformation 𝐆=𝐆⁡(n,uℓ,…,λ)\\mathbf{G}=\\mathbf{G}(n,u\_{\\ell},\\ldots,\\uplambda) such that the matrix



|     |     |     |     |
| --- | --- | --- | --- |
| (25) |  | 𝐌^=𝐒⁡(𝐆)⋅𝐌⁡(n,u0,…,up,λ)⋅𝐆−1\\displaystyle\\widehat{\\mathbf{M}}={\\mathbf{S}}(\\mathbf{G})\\cdot\\mathbf{M}(n,u\_{0},\\ldots,u\_{p},\\uplambda)\\cdot\\mathbf{G}^{-1} |  |



is of the form



|     |     |     |     |
| --- | --- | --- | --- |
| (26) |  | 𝐌^=𝐌^​(n,u0,…,up−1,λ).\\displaystyle\\widehat{\\mathbf{M}}=\\widehat{\\mathbf{M}}(n,u\_{0},\\ldots,u\_{p-1},\\uplambda). |  |

- •


Property 2.
The matrix 𝐌=𝐌⁡(n,u0,u1,…,up,λ)\\mathbf{M}=\\mathbf{M}(n,u\_{0},u\_{1},\\ldots,u\_{p},\\uplambda) obeys



|     |     |     |     |
| --- | --- | --- | --- |
| (27) |  | ∀i,j=1,…,N∂u0i(∂upj(𝐌)⋅𝐌−1)=0.\\displaystyle\\forall\\,i,j=1,\\ldots,N\\qquad\\quad\\partial\_{u^{i}\_{0}}\\big(\\partial\_{u^{j}\_{p}}(\\mathbf{M})\\cdot\\mathbf{M}^{-1}\\big)=0. |  |


Now suppose that 𝐌\\mathbf{M} satisfies ( [27](https://arxiv.org/html/2604.26870#S2.E27 "In 2nd item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Fix a constant vector a0=(a01,…,a0N)∈ℂNa\_{0}=(a^{1}\_{0},\\ldots,a^{N}\_{0})\\in\\mathbb{C}^{N}
and consider the gauge transformation

|     |     |     |     |
| --- | --- | --- | --- |
| (28) |  | 𝐆⁡(n,u0,…,up−1,λ):=𝐒−1​(𝐌​(n,a0,u1,…,up,λ)−1),\\displaystyle\\mathbf{G}(n,u\_{0},\\ldots,u\_{p-1},\\uplambda):={\\mathbf{S}}^{-1}\\big(\\mathbf{M}(n,a\_{0},u\_{1},\\ldots,u\_{p},\\uplambda)^{-1}\\big), |  |

where 𝐌⁡(n,a0,u1,…,up,λ)\\mathbf{M}(n,a\_{0},u\_{1},\\ldots,u\_{p},\\uplambda) is obtained
by substituting u0=a0u\_{0}=a\_{0} in 𝐌⁡(n,u0,u1,…,up,λ)\\mathbf{M}(n,u\_{0},u\_{1},\\ldots,u\_{p},\\uplambda).
Here a vector a0∈ℂNa\_{0}\\in\\mathbb{C}^{N} is chosen so that the matrix
𝐌⁡(n,a0,u1,…,up,λ)\\mathbf{M}(n,a\_{0},u\_{1},\\ldots,u\_{p},\\uplambda) is well defined and is invertible.
(Remark [5](https://arxiv.org/html/2604.26870#Thmremark5 "Remark 5. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") explains how to choose such a vector.)

Then the matrix 𝐌^\\widehat{\\mathbf{M}} determined by ( [25](https://arxiv.org/html/2604.26870#S2.E25 "In 1st item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
is of the form 𝐌^=𝐌^​(n,u0,…,up−1,λ)\\widehat{\\mathbf{M}}=\\widehat{\\mathbf{M}}(n,u\_{0},\\ldots,u\_{p-1},\\uplambda), and we have

|     |     |     |     |
| --- | --- | --- | --- |
| (29) |  | 𝐌^=𝐒⁡(𝐆)⋅𝐌⁡(n,u0,u1,…,up,λ)⋅𝐆−1==𝐌​(n,a0,u1,…,up,λ)−1⋅𝐌⁡(n,u0,u1,…,up,λ)⋅𝐒−1​(𝐌⁡(n,a0,u1,…,up,λ)),\\widehat{\\mathbf{M}}={\\mathbf{S}}(\\mathbf{G})\\cdot\\mathbf{M}(n,u\_{0},u\_{1},\\ldots,u\_{p},\\uplambda)\\cdot\\mathbf{G}^{-1}=\\\<br>=\\mathbf{M}(n,a\_{0},u\_{1},\\ldots,u\_{p},\\uplambda)^{-1}\\cdot\\mathbf{M}(n,u\_{0},u\_{1},\\ldots,u\_{p},\\uplambda)\\cdot{\\mathbf{S}}^{-1}\\big(\\mathbf{M}(n,a\_{0},u\_{1},\\ldots,u\_{p},\\uplambda)\\big), |  |

where the right-hand side of ( [29](https://arxiv.org/html/2604.26870#S2.E29 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) does not depend on upu\_{p}.

Furthermore, the above results imply the following additional statements:

Let (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}) be a MLR of class (0,p)(0,p). Then ( [27](https://arxiv.org/html/2604.26870#S2.E27 "In 2nd item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is a necessary and sufficient condition for
existence of a gauge transformation 𝐆=𝐆⁡(n,uℓ,…,λ)\\mathbf{G}=\\mathbf{G}(n,u\_{\\ell},\\ldots,\\uplambda)
such that the corresponding gauge equivalent MLR

|     |     |     |     |
| --- | --- | --- | --- |
| (30) |  | 𝐌^=𝐒⁡(𝐆)⋅𝐌⋅𝐆−1,𝐔^=𝐃t​(𝐆)⋅𝐆−1+𝐆⋅𝐔⋅𝐆−1\\displaystyle\\widehat{\\mathbf{M}}={\\mathbf{S}}(\\mathbf{G})\\cdot\\mathbf{M}\\cdot\\mathbf{G}^{-1},\\qquad\\quad\\widehat{\\mathbf{U}}=\\mathbf{D}\_{t}(\\mathbf{G})\\cdot\\mathbf{G}^{-1}+\\mathbf{G}\\cdot\\mathbf{U}\\cdot\\mathbf{G}^{-1} |  |

is of class (0,p−1)(0,p\\!-\\!1). If
𝐌\\mathbf{M} satisfies ( [27](https://arxiv.org/html/2604.26870#S2.E27 "In 2nd item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) then one can take
the gauge transformation ( [28](https://arxiv.org/html/2604.26870#S2.E28 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) for this purpose.

###### Proof.

Let us show that Property 1 implies Property 2.
Suppose that there is a gauge transformation 𝐆=𝐆⁡(n,uℓ,…,λ)\\mathbf{G}=\\mathbf{G}(n,u\_{\\ell},\\ldots,\\uplambda)
such that the matrix ( [25](https://arxiv.org/html/2604.26870#S2.E25 "In 1st item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is of the form ( [26](https://arxiv.org/html/2604.26870#S2.E26 "In 1st item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")). We need to prove ( [27](https://arxiv.org/html/2604.26870#S2.E27 "In 2nd item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

Let us first prove the following

|     |     |     |     |
| --- | --- | --- | --- |
| (31) |  | ∀q≥p∀j∈{1,…,N}∂uqj(𝐆)=0.\\displaystyle\\forall\\,q\\geq p\\qquad\\forall\\,j\\in\\{1,\\ldots,N\\}\\qquad\\quad\\partial\_{u^{j}\_{q}}(\\mathbf{G})=0. |  |

Suppose that ( [31](https://arxiv.org/html/2604.26870#S2.E31 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) does not hold.
Let kk be the maximal integer such that
there is j∈{1,…,N}j\\in\\{1,\\ldots,N\\} satisfying ∂ukj(𝐆)≠0\\partial\_{u^{j}\_{k}}(\\mathbf{G})\\neq 0.
By our assumption, k≥pk\\geq p, and one has ∂uk+1ȷ~(𝐆)=0\\partial\_{u^{\\tilde{\\jmath}}\_{k+1}}(\\mathbf{G})=0
for all ȷ~∈{1,…,N}\\tilde{\\jmath}\\in\\{1,\\ldots,N\\}. From ( [25](https://arxiv.org/html/2604.26870#S2.E25 "In 1st item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [26](https://arxiv.org/html/2604.26870#S2.E26 "In 1st item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) we get

|     |     |     |     |
| --- | --- | --- | --- |
| (32) |  | 𝐒⁡(𝐆)=𝐌^​(n,u0,…,up−1,λ)⋅𝐆⋅(𝐌⁡(n,u0,…,up,λ))−1,\\displaystyle{\\mathbf{S}}(\\mathbf{G})=\\widehat{\\mathbf{M}}(n,u\_{0},\\ldots,u\_{p-1},\\uplambda)\\cdot\\mathbf{G}\\cdot\\big(\\mathbf{M}(n,u\_{0},\\ldots,u\_{p},\\uplambda)\\big)^{-1}, |  |
| (33) |  | 𝐆=(𝐌^​(n,u0,…,up−1,λ))−1⋅𝐒⁡(𝐆)⋅𝐌⁡(n,u0,…,up,λ).\\displaystyle\\mathbf{G}=\\big(\\widehat{\\mathbf{M}}(n,u\_{0},\\ldots,u\_{p-1},\\uplambda)\\big)^{-1}\\cdot{\\mathbf{S}}(\\mathbf{G})\\cdot\\mathbf{M}(n,u\_{0},\\ldots,u\_{p},\\uplambda). |  |

Using the rules ( [1](https://arxiv.org/html/2604.26870#S1.EGx6 "1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and the property ∂ukj(𝐆)≠0\\partial\_{u^{j}\_{k}}(\\mathbf{G})\\neq 0,
for the left-hand side of equation ( [32](https://arxiv.org/html/2604.26870#S2.E32 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
we derive ∂uk+1j(𝐒⁡(𝐆))=𝐒⁡(∂ukj(𝐆))≠0\\partial\_{u^{j}\_{k+1}}\\big({\\mathbf{S}}(\\mathbf{G})\\big)={\\mathbf{S}}\\big(\\partial\_{u^{j}\_{k}}(\\mathbf{G})\\big)\\neq 0.
On the other hand, since k≥pk\\geq p and ∂uk+1j(𝐆)=0\\partial\_{u^{j}\_{k+1}}(\\mathbf{G})=0,
the right-hand side of equation ( [32](https://arxiv.org/html/2604.26870#S2.E32 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) does not depend on uk+1ju^{j}\_{k+1}.
The obtained contradiction allows us to conclude that ( [31](https://arxiv.org/html/2604.26870#S2.E31 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) actually holds.

Now let us prove that

|     |     |     |     |
| --- | --- | --- | --- |
| (34) |  | ∀q≤−1∀j∈{1,…,N}∂uqj(𝐆)=0.\\displaystyle\\forall\\,q\\leq-1\\qquad\\forall\\,j\\in\\{1,\\ldots,N\\}\\qquad\\quad\\partial\_{u^{j}\_{q}}(\\mathbf{G})=0. |  |

Suppose that ( [34](https://arxiv.org/html/2604.26870#S2.E34 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) does not hold.
Let rr be the minimal integer such that
there is j∈{1,…,N}j\\in\\{1,\\ldots,N\\} satisfying ∂urj(𝐆)≠0\\partial\_{u^{j}\_{r}}(\\mathbf{G})\\neq 0.
By our assumption, r≤−1r\\leq-1, and one has ∂ur−1ȷ~(𝐆)=0\\partial\_{u^{\\tilde{\\jmath}}\_{r-1}}(\\mathbf{G})=0
for all ȷ~∈{1,…,N}\\tilde{\\jmath}\\in\\{1,\\ldots,N\\}.
Therefore, the right-hand side of ( [33](https://arxiv.org/html/2604.26870#S2.E33 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) does not depend on urju^{j}\_{r}.
On the other hand, for the left-hand side of ( [33](https://arxiv.org/html/2604.26870#S2.E33 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) we have ∂urj(𝐆)≠0\\partial\_{u^{j}\_{r}}(\\mathbf{G})\\neq 0.
This contradiction shows that ( [34](https://arxiv.org/html/2604.26870#S2.E34 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) actually holds.

The obtained properties ( [31](https://arxiv.org/html/2604.26870#S2.E31 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [34](https://arxiv.org/html/2604.26870#S2.E34 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) imply that 𝐆\\mathbf{G} is of the form
𝐆=𝐆⁡(n,u0,…,up−1,λ)\\mathbf{G}=\\mathbf{G}(n,u\_{0},\\dots,u\_{p-1},\\uplambda). Then from ( [25](https://arxiv.org/html/2604.26870#S2.E25 "In 1st item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) one gets

|     |     |     |     |
| --- | --- | --- | --- |
| (35) |  | 𝐌=𝐒⁡(𝐆​(n,u0,…,up−1,λ)−1)⋅𝐌^​(n,u0,…,up−1,λ)⋅𝐆⁡(n,u0,…,up−1,λ).\\displaystyle\\mathbf{M}={\\mathbf{S}}\\big(\\mathbf{G}(n,u\_{0},\\dots,u\_{p-1},\\uplambda)^{-1}\\big)\\cdot\\widehat{\\mathbf{M}}(n,u\_{0},\\dots,u\_{p-1},\\uplambda)\\cdot\\mathbf{G}(n,u\_{0},\\dots,u\_{p-1},\\uplambda). |  |

Using ( [35](https://arxiv.org/html/2604.26870#S2.E35 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), for each j=1,…,Nj=1,\\dots,N we derive

|     |     |     |     |
| --- | --- | --- | --- |
| (36) |  | ∂upj(𝐌)⋅𝐌−1=∂upj(𝐒⁡(𝐆​(n,u0,…,up−1,λ)−1)⋅𝐌^​(n,u0,…,up−1,λ)⋅𝐆⁡(n,u0,…,up−1,λ))⋅𝐌−1==𝐒⁡(∂up−1j(𝐆​(n,u0,…,up−1,λ)−1))⋅𝐌^⋅𝐆⋅(𝐒⁡(𝐆−1)⋅𝐌^⋅𝐆)−1==𝐒⁡(∂up−1j(𝐆​(n,u0,…,up−1,λ)−1))⋅𝐌^⋅𝐆⋅𝐆−1⋅𝐌^−1⋅(𝐒⁡(𝐆−1))−1==𝐒⁡(∂up−1j(𝐆​(n,u0,…,up−1,λ)−1))⋅𝐒⁡(𝐆⁡(n,u0,…,up−1,λ)).\\partial\_{u^{j}\_{p}}(\\mathbf{M})\\cdot\\mathbf{M}^{-1}=\\partial\_{u^{j}\_{p}}\\Big({\\mathbf{S}}\\big(\\mathbf{G}(n,u\_{0},\\dots,u\_{p-1},\\uplambda)^{-1}\\big)\\cdot\\widehat{\\mathbf{M}}(n,u\_{0},\\dots,u\_{p-1},\\uplambda)\\cdot\\mathbf{G}(n,u\_{0},\\dots,u\_{p-1},\\uplambda)\\Big)\\cdot\\mathbf{M}^{-1}=\\\<br>={\\mathbf{S}}\\Big(\\partial\_{u^{j}\_{p-1}}\\big(\\mathbf{G}(n,u\_{0},\\dots,u\_{p-1},\\uplambda)^{-1}\\big)\\Big)\\cdot\\widehat{\\mathbf{M}}\\cdot\\mathbf{G}\\cdot\\big({\\mathbf{S}}(\\mathbf{G}^{-1})\\cdot\\widehat{\\mathbf{M}}\\cdot\\mathbf{G}\\big)^{-1}=\\\<br>={\\mathbf{S}}\\Big(\\partial\_{u^{j}\_{p-1}}\\big(\\mathbf{G}(n,u\_{0},\\dots,u\_{p-1},\\uplambda)^{-1}\\big)\\Big)\\cdot\\widehat{\\mathbf{M}}\\cdot\\mathbf{G}\\cdot\\mathbf{G}^{-1}\\cdot\\widehat{\\mathbf{M}}^{-1}\\cdot\\big({\\mathbf{S}}(\\mathbf{G}^{-1})\\big)^{-1}=\\\<br>={\\mathbf{S}}\\Big(\\partial\_{u^{j}\_{p-1}}\\big(\\mathbf{G}(n,u\_{0},\\dots,u\_{p-1},\\uplambda)^{-1}\\big)\\Big)\\cdot{\\mathbf{S}}\\big(\\mathbf{G}(n,u\_{0},\\dots,u\_{p-1},\\uplambda)\\big). |  |

The rules ( [1](https://arxiv.org/html/2604.26870#S1.EGx6 "1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) imply that the right-hand side of ( [36](https://arxiv.org/html/2604.26870#S2.E36 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) does not depend on u0iu^{i}\_{0}
for any i=1,…,Ni=1,\\dots,N. This yields ( [27](https://arxiv.org/html/2604.26870#S2.E27 "In 2nd item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

Now let us prove that Property 2 implies Property 1,
along with the statement about the gauge transformation ( [28](https://arxiv.org/html/2604.26870#S2.E28 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

Suppose that 𝐌=𝐌⁡(n,u0,u1,…,up,λ)\\mathbf{M}=\\mathbf{M}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda) satisfies ( [27](https://arxiv.org/html/2604.26870#S2.E27 "In 2nd item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
According to Remark [5](https://arxiv.org/html/2604.26870#Thmremark5 "Remark 5. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"),
we can choose a constant vector a0∈ℂNa\_{0}\\in\\mathbb{C}^{N} such that
𝐌​(n,a0,u1,…,up,λ)−1\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1} is well defined.
This allows us to consider the gauge transformation ( [28](https://arxiv.org/html/2604.26870#S2.E28 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
and the corresponding matrix 𝐌^\\widehat{\\mathbf{M}} determined by ( [25](https://arxiv.org/html/2604.26870#S2.E25 "In 1st item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Since for ( [28](https://arxiv.org/html/2604.26870#S2.E28 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) one has

|     |     |     |
| --- | --- | --- |
|  | 𝐒⁡(𝐆)=𝐌​(n,a0,u1,…,up,λ)−1,𝐆−1=𝐒−1​(𝐌⁡(n,a0,u1,…,up,λ)),\\displaystyle{\\mathbf{S}}(\\mathbf{G})=\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1},\\qquad\\quad\\mathbf{G}^{-1}={\\mathbf{S}}^{-1}\\big(\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)\\big), |  |

we obtain ( [29](https://arxiv.org/html/2604.26870#S2.E29 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), which implies that the matrix-function 𝐌^\\widehat{\\mathbf{M}}
may depend only on n,u0,u1,…,up,λn,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda.
In order to show that actually 𝐌^\\widehat{\\mathbf{M}} is of the form ( [26](https://arxiv.org/html/2604.26870#S2.E26 "In 1st item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), it remains to prove that

|     |     |     |     |
| --- | --- | --- | --- |
| (37) |  | ∂upj(𝐌^)=0∀j=1,…,N.\\displaystyle\\partial\_{u^{j}\_{p}}\\big(\\widehat{\\mathbf{M}}\\big)=0\\qquad\\quad\\forall\\,j=1,\\dots,N. |  |

Let j∈{1,…,N}j\\in\\{1,\\dots,N\\}. Set
𝐇:=𝐆−1​(n,u0,…,up−1,λ)=𝐒−1​(𝐌⁡(n,a0,u1,…,up,λ))\\mathbf{H}:=\\mathbf{G}^{-1}(n,u\_{0},\\dots,u\_{p-1},\\uplambda)={\\mathbf{S}}^{-1}\\big(\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)\\big).
Using ( [29](https://arxiv.org/html/2604.26870#S2.E29 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and the property ∂upj(𝐇)=0\\partial\_{u^{j}\_{p}}(\\mathbf{H})=0, we get

|     |     |     |     |
| --- | --- | --- | --- |
| (38) |  | ∂upj(𝐌^)=∂upj(𝐌​(n,a0,u1,…,up,λ)−1⋅𝐌⁡(n,u0,u1,…,up,λ))⋅𝐇==(∂upj(𝐌​(n,a0,u1,…,up,λ)−1)⋅𝐌⁡(n,u0,u1,…,up,λ)+CLOSE+𝐌(n,a0,u1,…,up,λ)−1⋅∂upj(𝐌(n,u0,u1,…,up,λ)))⋅𝐇==(−𝐌(n,a0,u1,…,up,λ)−1⋅∂upj(𝐌(n,a0,u1,…,up,λ)⋅𝐌(n,a0,u1,…,up,λ)−1⋅⋅𝐌(n,u0,u1,…,up,λ)+𝐌(n,a0,u1,…,up,λ)−1⋅∂upj(𝐌(n,u0,u1,…,up,λ)))⋅𝐇==𝐌(n,a0,u1,…,up,λ)−1⋅(−∂upj(𝐌(n,a0,u1,…,up,λ))⋅𝐌(n,a0,u1,…,up,λ)−1++∂upj(𝐌(n,u0,u1,…,up,λ))⋅𝐌(n,u0,u1,…,up,λ)−1)⋅𝐌(n,u0,u1,…,up,λ)⋅𝐇==𝐌​(n,a0,u1,…,up,λ)−1⋅𝐋j​(n,u0,u1,…,up,λ)⋅𝐌⁡(n,u0,u1,…,up,λ)⋅𝐇,\\partial\_{u^{j}\_{p}}\\big(\\widehat{\\mathbf{M}}\\big)=\\partial\_{u^{j}\_{p}}\\Big(\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1}\\cdot\\mathbf{M}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)\\Big)\\cdot\\mathbf{H}=\\\<br>=\\Big(\\partial\_{u^{j}\_{p}}\\big(\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1}\\big)\\cdot\\mathbf{M}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)+\\\<br>+\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1}\\cdot\\partial\_{u^{j}\_{p}}\\big(\\mathbf{M}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)\\big)\\Big)\\cdot\\mathbf{H}=\\\<br>=\\Big(-\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1}\\cdot\\partial\_{u^{j}\_{p}}\\big(\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda\\big)\\cdot\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1}\\cdot\\\<br>\\cdot\\mathbf{M}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)+\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1}\\cdot\\partial\_{u^{j}\_{p}}\\big(\\mathbf{M}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)\\big)\\Big)\\cdot\\mathbf{H}=\\\<br>=\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1}\\cdot\\Big(-\\partial\_{u^{j}\_{p}}\\big(\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)\\big)\\cdot\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1}+\\\<br>+\\partial\_{u^{j}\_{p}}\\big(\\mathbf{M}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)\\big)\\cdot\\mathbf{M}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1}\\Big)\\cdot\\mathbf{M}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)\\cdot\\mathbf{H}=\\\<br>=\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1}\\cdot\\mathbf{L}^{j}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)\\cdot\\mathbf{M}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)\\cdot\\mathbf{H}, |  |

where

|     |     |     |     |
| --- | --- | --- | --- |
| (39) |  | 𝐋j(n,u0,u1,…,up,λ)=−∂upj(𝐌(n,a0,u1,…,up,λ))⋅𝐌(n,a0,u1,…,up,λ)−1++∂upj(𝐌(n,u0,u1,…,up,λ))⋅𝐌(n,u0,u1,…,up,λ)−1.\\mathbf{L}^{j}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)=-\\partial\_{u^{j}\_{p}}\\big(\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)\\big)\\cdot\\mathbf{M}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1}+\\\<br>+\\partial\_{u^{j}\_{p}}\\big(\\mathbf{M}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)\\big)\\cdot\\mathbf{M}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1}. |  |

From ( [39](https://arxiv.org/html/2604.26870#S2.E39 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and ( [27](https://arxiv.org/html/2604.26870#S2.E27 "In 2nd item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) it follows that

|     |     |     |     |
| --- | --- | --- | --- |
|  | ∂u0i(𝐋j​(n,u0,u1,…,up,λ))=∂u0i(∂upj(𝐌⁡(n,u0,u1,…,up,λ))⋅𝐌​(n,u0,u1,…,up,λ)−1)=0∀i=1,…,N,\\displaystyle\\begin{gathered}\\partial\_{u^{i}\_{0}}\\big(\\mathbf{L}^{j}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)\\big)=\\partial\_{u^{i}\_{0}}\\Big(\\partial\_{u^{j}\_{p}}\\big(\\mathbf{M}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)\\big)\\cdot\\mathbf{M}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)^{-1}\\Big)=0\\\<br>\\forall\\,i=1,\\dots,N,\\end{gathered} |  |
| (42) |  | 𝐋j​(n,a0,u1,…,up,λ)=0.\\displaystyle\\mathbf{L}^{j}(n,a\_{0},u\_{1},\\dots,u\_{p},\\uplambda)=0. |  |

Since, according to Remark [1](https://arxiv.org/html/2604.26870#Thmremark1 "Remark 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"), the entries of
the matrix-function 𝐋j​(n,u0,u1,…,up,λ)\\mathbf{L}^{j}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)
depend rationally on n∈ℤn\\in\\mathbb{Z}, u0,u1,…,up∈ℂNu\_{0},u\_{1},\\dots,u\_{p}\\in\\mathbb{C}^{N}
and meromorphically on λ∈ℂ\\uplambda\\in\\mathbb{C},
equations ( [2](https://arxiv.org/html/2604.26870#S2.EGx40 "Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [42](https://arxiv.org/html/2604.26870#S2.E42 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) imply that the matrix-function
𝐋j​(n,u0,u1,…,up,λ)\\mathbf{L}^{j}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda) is identically zero.

Substituting 𝐋j​(n,u0,u1,…,up,λ)=0\\mathbf{L}^{j}(n,u\_{0},u\_{1},\\dots,u\_{p},\\uplambda)=0 in ( [38](https://arxiv.org/html/2604.26870#S2.E38 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), one gets ( [37](https://arxiv.org/html/2604.26870#S2.E37 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Therefore, the matrix-function 𝐌^\\widehat{\\mathbf{M}} given by ( [25](https://arxiv.org/html/2604.26870#S2.E25 "In 1st item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [29](https://arxiv.org/html/2604.26870#S2.E29 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is of the form ( [26](https://arxiv.org/html/2604.26870#S2.E26 "In 1st item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
and the right-hand side of ( [29](https://arxiv.org/html/2604.26870#S2.E29 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) does not depend on upu\_{p}.

Clearly, the obtained results immediately imply the additional statements (about MLRs) in the end of the theorem.
∎

In what follows, we use the notation and formulas from Definition [3](https://arxiv.org/html/2604.26870#Thmdefinition3 "Definition 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations").

###### Lemma 2.

Let M=M⁡(n,uℓ,…,λ)M=M(n,u\_{\\ell},\\ldots,\\uplambda), 𝐆=𝐆⁡(n,uℓ,…,λ)\\,\\mathbf{G}=\\mathbf{G}(n,u\_{\\ell},\\ldots,\\uplambda)
be invertible d×d\\mathrm{d}\\times\\mathrm{d} matrix-functions
and P=P⁡(n,uℓ,…,λ)P=P(n,u\_{\\ell},\\ldots,\\uplambda) be an arbitrary d×d\\mathrm{d}\\times\\mathrm{d} matrix-function.
Set M~=𝐒⁡(𝐆)⋅M⋅𝐆−1\\widetilde{M}={\\mathbf{S}}(\\mathbf{G})\\cdot M\\cdot\\mathbf{G}^{-1}.
Then

|     |     |     |     |
| --- | --- | --- | --- |
| (43) |  | ∇M~k(𝐒⁡(𝐆)⋅P⋅𝐒​(𝐆)−1)=𝐒⁡(𝐆)⋅∇Mk(P)⋅𝐒​(𝐆)−1∀k∈ℤ.\\displaystyle\\nabla\_{\\widetilde{M}}^{k}\\big({\\mathbf{S}}(\\mathbf{G})\\cdot P\\cdot{\\mathbf{S}}(\\mathbf{G})^{-1}\\big)={\\mathbf{S}}(\\mathbf{G})\\cdot\\nabla^{k}\_{M}(P)\\cdot{\\mathbf{S}}(\\mathbf{G})^{-1}\\qquad\\quad\\forall\\,{k}\\in\\mathbb{Z}. |  |

###### Proof.

We have

|     |     |     |     |
| --- | --- | --- | --- |
| (44) |  | M~=𝐒⁡(𝐆)⋅M⋅𝐆−1,M~−1=𝐆⋅M−1⋅𝐒​(𝐆)−1,𝐒⁡(𝐆−1)=𝐒​(𝐆)−1.\\displaystyle\\widetilde{M}={\\mathbf{S}}(\\mathbf{G})\\cdot M\\cdot\\mathbf{G}^{-1},\\qquad\\quad\\widetilde{M}^{-1}=\\mathbf{G}\\cdot M^{-1}\\cdot{\\mathbf{S}}(\\mathbf{G})^{-1},\\qquad\\quad{\\mathbf{S}}(\\mathbf{G}^{-1})={\\mathbf{S}}(\\mathbf{G})^{-1}. |  |

Using ( [13](https://arxiv.org/html/2604.26870#S1.E13 "In Definition 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and ( [44](https://arxiv.org/html/2604.26870#S2.E44 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), one gets

|     |     |     |     |
| --- | --- | --- | --- |
| (45) |  | ∇M~(𝐒⁡(𝐆)⋅P⋅𝐒​(𝐆)−1)=𝐒⁡(M~−1​𝐒​(𝐆)​P​𝐒​(𝐆)−1​M~)=𝐒⁡(𝐆​M−1​𝐒​(𝐆)−1​𝐒​(𝐆)​P​𝐒​(𝐆)−1​𝐒​(𝐆)​M​𝐆−1)==𝐒⁡(𝐆​M−1​P​M​𝐆−1)=𝐒⁡(𝐆)​𝐒​(M−1​P​M)​𝐒​(𝐆−1)=𝐒⁡(𝐆)​∇M(P)​𝐒​(𝐆)−1.\\nabla\_{\\widetilde{M}}\\big({\\mathbf{S}}(\\mathbf{G})\\cdot P\\cdot{\\mathbf{S}}(\\mathbf{G})^{-1}\\big)={\\mathbf{S}}\\big(\\widetilde{M}^{-1}{\\mathbf{S}}(\\mathbf{G})P{\\mathbf{S}}(\\mathbf{G})^{-1}\\widetilde{M}\\big)={\\mathbf{S}}\\big(\\mathbf{G}M^{-1}{\\mathbf{S}}(\\mathbf{G})^{-1}{\\mathbf{S}}(\\mathbf{G})P{\\mathbf{S}}(\\mathbf{G})^{-1}{\\mathbf{S}}(\\mathbf{G})M\\mathbf{G}^{-1}\\big)=\\\<br>={\\mathbf{S}}(\\mathbf{G}M^{-1}PM\\mathbf{G}^{-1})={\\mathbf{S}}(\\mathbf{G}){\\mathbf{S}}(M^{-1}PM){\\mathbf{S}}(\\mathbf{G}^{-1})={\\mathbf{S}}(\\mathbf{G})\\nabla\_{M}(P){\\mathbf{S}}(\\mathbf{G})^{-1}. |  |

Thus we have

|     |     |     |     |
| --- | --- | --- | --- |
| (46) |  | ∇M~(𝐒⁡(𝐆)⋅P⋅𝐒​(𝐆)−1)=𝐒⁡(𝐆)⋅∇M(P)⋅𝐒​(𝐆)−1.\\displaystyle\\nabla\_{\\widetilde{M}}\\big({\\mathbf{S}}(\\mathbf{G})\\cdot P\\cdot{\\mathbf{S}}(\\mathbf{G})^{-1}\\big)={\\mathbf{S}}(\\mathbf{G})\\cdot\\nabla\_{M}(P)\\cdot{\\mathbf{S}}(\\mathbf{G})^{-1}. |  |

Similarly, using ( [14](https://arxiv.org/html/2604.26870#S1.E14 "In Definition 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and ( [44](https://arxiv.org/html/2604.26870#S2.E44 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), one obtains

|     |     |     |     |
| --- | --- | --- | --- |
| (47) |  | ∇M~−1(𝐒⁡(𝐆)⋅P⋅𝐒​(𝐆)−1)=𝐒⁡(𝐆)⋅∇M−1(P)⋅𝐒​(𝐆)−1.\\displaystyle\\nabla\_{\\widetilde{M}}^{-1}\\big({\\mathbf{S}}(\\mathbf{G})\\cdot P\\cdot{\\mathbf{S}}(\\mathbf{G})^{-1}\\big)={\\mathbf{S}}(\\mathbf{G})\\cdot\\nabla\_{M}^{-1}(P)\\cdot{\\mathbf{S}}(\\mathbf{G})^{-1}. |  |

Using ( [46](https://arxiv.org/html/2604.26870#S2.E46 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and ( [47](https://arxiv.org/html/2604.26870#S2.E47 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), one can prove ( [43](https://arxiv.org/html/2604.26870#S2.E43 "In Lemma 2. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) by induction on k{k}.
∎

###### Theorem 2.

For any invertible d×d\\mathrm{d}\\times\\mathrm{d} matrix-functions
M=M⁡(n,uℓ,…,λ)M=M(n,u\_{\\ell},\\ldots,\\uplambda) and G=G⁡(n,uℓ,…,λ)G=G(n,u\_{\\ell},\\ldots,\\uplambda), we have

|     |     |     |     |
| --- | --- | --- | --- |
| (48) |  | 𝚫uj​(𝐒⁡(G)⋅M⋅G−1)=𝐒⁡(G)⋅𝚫uj​(M)⋅𝐒​(G)−1∀j=1,…,N.\\displaystyle\\boldsymbol{\\Delta}^{u^{j}}\\big({\\mathbf{S}}(G)\\cdot M\\cdot G^{-1}\\big)={\\mathbf{S}}(G)\\cdot\\boldsymbol{\\Delta}^{u^{j}}(M)\\cdot{\\mathbf{S}}(G)^{-1}\\qquad\\quad\\forall\\,j=1,\\ldots,N. |  |

###### Proof.

Set M~=𝐒⁡(G)​M​G−1\\widetilde{M}={\\mathbf{S}}(G)MG^{-1}.
To prove ( [48](https://arxiv.org/html/2604.26870#S2.E48 "In Theorem 2. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we need to show that
𝚫uj​(M~)=𝐒⁡(G)⋅𝚫uj​(M)⋅𝐒​(G)−1\\boldsymbol{\\Delta}^{u^{j}}\\big(\\widetilde{M}\\big)={\\mathbf{S}}(G)\\cdot\\boldsymbol{\\Delta}^{u^{j}}(M)\\cdot{\\mathbf{S}}(G)^{-1}.

Using the relations

|     |     |     |
| --- | --- | --- |
|  | M~−1=GM−1𝐒(G)−1,∂uℓj(G−1)=−G−1∂uℓj(G)G−1,∂uℓj(𝐒(G))=𝐒(∂uℓ−1j(G)),\\displaystyle\\widetilde{M}^{-1}=GM^{-1}{\\mathbf{S}}(G)^{-1},\\qquad\\partial\_{u^{j}\_{\\ell}}(G^{-1})=-G^{-1}\\partial\_{u^{j}\_{\\ell}}(G)G^{-1},\\qquad\\partial\_{u^{j}\_{\\ell}}\\big({\\mathbf{S}}(G)\\big)={\\mathbf{S}}\\big(\\partial\_{u^{j}\_{\\ell-1}}(G)\\big), |  |
|  | 𝐒⁡(∂uℓ−1j(G))=𝐒⁡(G)​𝐒​(G−1​∂uℓ−1j(G)),M​G−1​∂uℓj(G)​M−1=∇M−1(𝐒⁡(G−1​∂uℓj(G)))\\displaystyle{\\mathbf{S}}\\big(\\partial\_{u^{j}\_{\\ell-1}}(G)\\big)={\\mathbf{S}}(G){\\mathbf{S}}\\big(G^{-1}\\partial\_{u^{j}\_{\\ell-1}}(G)\\big),\\qquad MG^{-1}\\partial\_{u^{j}\_{\\ell}}(G)M^{-1}=\\nabla\_{M}^{-1}\\big({\\mathbf{S}}\\big(G^{-1}\\partial\_{u^{j}\_{\\ell}}(G)\\big)\\big) |  |

and Lemma [2](https://arxiv.org/html/2604.26870#Thmlemma2 "Lemma 2. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"), one can prove
𝚫uj​(M~)=𝐒⁡(G)⋅𝚫uj​(M)⋅𝐒​(G)−1\\boldsymbol{\\Delta}^{u^{j}}\\big(\\widetilde{M}\\big)={\\mathbf{S}}(G)\\cdot\\boldsymbol{\\Delta}^{u^{j}}(M)\\cdot{\\mathbf{S}}(G)^{-1}
by straightforward (but rather lengthy) computations,
which are presented in the preprint \[ [9](https://arxiv.org/html/2604.26870#bib.bib9 "")\].
∎

###### Lemma 3.

Let p∈ℤ≥0p\\in\\mathbb{Z}\_{\\geq 0}.
Consider an invertible d×d\\mathrm{d}\\times\\mathrm{d} matrix-function M=M⁡(n,u0,…,up,λ)M=M(n,u\_{0},\\ldots,u\_{p},\\uplambda).
Suppose that

|     |     |     |     |
| --- | --- | --- | --- |
| (49) |  | 𝚫uj​(M)=0∀j=1,…,N.\\displaystyle\\boldsymbol{\\Delta}^{u^{j}}(M)=0\\qquad\\quad\\forall\\,j=1,\\ldots,N. |  |

Then there is a gauge transformation 𝐆=𝐆⁡(n,u0,…,up−1,λ)\\mathbf{G}=\\mathbf{G}(n,u\_{0},\\ldots,u\_{p-1},\\uplambda)
such that the matrix

|     |     |     |     |
| --- | --- | --- | --- |
| (50) |  | M˘=𝐒⁡(𝐆)⋅M⁡(n,u0,…,up,λ)⋅𝐆−1\\displaystyle\\breve{M}={\\mathbf{S}}(\\mathbf{G})\\cdot M(n,u\_{0},\\ldots,u\_{p},\\uplambda)\\cdot\\mathbf{G}^{-1} |  |

obeys

|     |     |     |     |
| --- | --- | --- | --- |
| (51) |  | ∂uℓj(M˘)=0∀ℓ∈ℤ,∀j=1,…,N.\\displaystyle\\partial\_{u^{j}\_{\\ell}}(\\breve{M})=0\\qquad\\quad\\forall\\,\\ell\\in\\mathbb{Z},\\qquad\\forall\\,j=1,\\ldots,N. |  |

###### Proof.

We prove this by induction on p∈ℤ≥0p\\in\\mathbb{Z}\_{\\geq 0}. First, consider the case p=0p=0, where M=M⁡(n,u0,λ)M=M(n,u\_{0},\\uplambda).
According to ( [15](https://arxiv.org/html/2604.26870#S1.E15 "In Definition 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), for M=M⁡(n,u0,λ)M=M(n,u\_{0},\\uplambda) we have 𝚫uj​(M)=∂u0j(M)⋅M−1\\boldsymbol{\\Delta}^{u^{j}}(M)=\\partial\_{u^{j}\_{0}}(M)\\cdot M^{-1}.
Then ( [49](https://arxiv.org/html/2604.26870#S2.E49 "In Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) implies that MM is of the form M=M⁡(n,λ)M=M(n,\\uplambda).
We take 𝐆=𝐈𝐝\\mathbf{G}=\\mathbf{Id}, where 𝐈𝐝\\mathbf{Id} is the identity matrix of size d×d\\mathrm{d}\\times\\mathrm{d}.
Then M˘=M⁡(n,λ)\\breve{M}=M(n,\\uplambda) satisfies ( [50](https://arxiv.org/html/2604.26870#S2.E50 "In Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [51](https://arxiv.org/html/2604.26870#S2.E51 "In Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

To make the induction step, we consider a number k∈ℤ≥0k\\in\\mathbb{Z}\_{\\geq 0} such that
the statement of Lemma [3](https://arxiv.org/html/2604.26870#Thmlemma3 "Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") is valid for p=kp=k.
We need to prove the statement in the case p=k+1p=k+1, where M=M⁡(n,u0,…,uk+1,λ)M=M(n,u\_{0},\\ldots,u\_{k+1},\\uplambda).
According to ( [15](https://arxiv.org/html/2604.26870#S1.E15 "In Definition 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), for such MM equation ( [49](https://arxiv.org/html/2604.26870#S2.E49 "In Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) reads
∑ℓ=0,…,k+1∇M−ℓ(∂uℓj(M)​M−1)=0\\sum\_{\\ell=0,\\ldots,k+1}\\nabla\_{M}^{-\\ell}\\big(\\partial\_{u^{j}\_{\\ell}}(M)M^{-1}\\big)=0, which yields

|     |     |     |     |
| --- | --- | --- | --- |
| (52) |  | ∇M−(k+1)(∂uk+1j(M)M−1)=−∑ℓ=0,…,k∇M−ℓ(∂uℓj(M)M−1)∀j=1,…,N.\\displaystyle\\nabla\_{M}^{-(k+1)}\\big(\\partial\_{u^{j}\_{k+1}}(M)M^{-1}\\big)=-\\sum\_{\\ell=0,\\ldots,k}\\nabla\_{M}^{-\\ell}\\big(\\partial\_{u^{j}\_{\\ell}}(M)M^{-1}\\big)\\qquad\\quad\\forall\\,j=1,\\ldots,N. |  |

Applying the operator ∇Mk+1\\nabla\_{M}^{k+1} to equation ( [52](https://arxiv.org/html/2604.26870#S2.E52 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and using ( [13](https://arxiv.org/html/2604.26870#S1.E13 "In Definition 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we derive

|     |     |     |     |
| --- | --- | --- | --- |
| (53) |  | ∂uk+1j(M)⋅M−1=−∑ℓ=0,…,k∇Mk+1−ℓ(∂uℓj(M)M−1)=−∇M(∑ℓ=0,…,k∇Mk−ℓ(∂uℓj(M)M−1))==−𝐒(M−1(∑ℓ=0,…,k∇Mk−ℓ(∂uℓj(M)M−1))M)∀j=1,…,N.\\partial\_{u^{j}\_{k+1}}(M)\\cdot M^{-1}=-\\sum\_{\\ell=0,\\ldots,k}\\nabla\_{M}^{k+1-\\ell}\\big(\\partial\_{u^{j}\_{\\ell}}(M)M^{-1}\\big)=-\\nabla\_{M}\\Big(\\sum\_{\\ell=0,\\ldots,k}\\nabla\_{M}^{k-\\ell}\\big(\\partial\_{u^{j}\_{\\ell}}(M)M^{-1}\\big)\\Big)=\\\<br>=-{\\mathbf{S}}\\Big(M^{-1}\\Big(\\sum\_{\\ell=0,\\ldots,k}\\nabla\_{M}^{k-\\ell}\\big(\\partial\_{u^{j}\_{\\ell}}(M)M^{-1}\\big)\\Big)M\\Big)\\qquad\\quad\\forall\\,j=1,\\ldots,N. |  |

Let Y=M−1​(∑ℓ=0,…,k∇Mk−ℓ(∂uℓj(M)​M−1))​MY=M^{-1}\\Big(\\sum\_{\\ell=0,\\ldots,k}\\nabla\_{M}^{k-\\ell}\\big(\\partial\_{u^{j}\_{\\ell}}(M)M^{-1}\\big)\\Big)M.
The formulas M=M⁡(n,u0,…,uk+1,λ)M=M(n,u\_{0},\\ldots,u\_{k+1},\\uplambda) and ( [13](https://arxiv.org/html/2604.26870#S1.E13 "In Definition 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
imply that YY does not depend on uaiu^{i}\_{a} for any a<0a<0 and i=1,…,Ni=1,\\ldots,N.
Since the right-hand side of ( [53](https://arxiv.org/html/2604.26870#S2.E53 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is equal to −𝐒⁡(Y)-{\\mathbf{S}}(Y),
it does not depend on u0iu^{i}\_{0}, i=1,…,N\\,i=1,\\ldots,N.
Therefore, from ( [53](https://arxiv.org/html/2604.26870#S2.E53 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) we get

|     |     |     |     |
| --- | --- | --- | --- |
| (54) |  | ∀i,j=1,…,N∂u0i(∂uk+1j(M⁡(n,u0,…,uk+1,λ))⋅M​(n,u0,…,uk+1,λ)−1)=0.\\displaystyle\\forall\\,i,j=1,\\ldots,N\\qquad\\quad\\partial\_{u^{i}\_{0}}\\Big(\\partial\_{u^{j}\_{k+1}}\\big(M(n,u\_{0},\\ldots,u\_{k+1},\\uplambda)\\big)\\cdot M(n,u\_{0},\\ldots,u\_{k+1},\\uplambda)^{-1}\\Big)=0. |  |

By Theorem [1](https://arxiv.org/html/2604.26870#Thmtheorem1 "Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") in the case p=k+1p=k+1,
from property ( [54](https://arxiv.org/html/2604.26870#S2.E54 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) it follows that there is a gauge transformation G=G⁡(n,u0,…,uk,λ)G=G(n,u\_{0},\\ldots,u\_{k},\\uplambda)
such that the matrix

|     |     |     |     |
| --- | --- | --- | --- |
| (55) |  | M^=𝐒⁡(G)⋅M⁡(n,u0,…,uk+1,λ)⋅G−1\\displaystyle\\widehat{M}={\\mathbf{S}}(G)\\cdot M(n,u\_{0},\\ldots,u\_{k+1},\\uplambda)\\cdot G^{-1} |  |

is of the form M^=M^​(n,u0,…,uk,λ)\\widehat{M}=\\widehat{M}(n,u\_{0},\\ldots,u\_{k},\\uplambda).
Using ( [48](https://arxiv.org/html/2604.26870#S2.E48 "In Theorem 2. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and ( [49](https://arxiv.org/html/2604.26870#S2.E49 "In Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), one obtains

|     |     |     |     |
| --- | --- | --- | --- |
| (56) |  | 𝚫uj​(M^)=𝚫uj​(𝐒⁡(G)⋅M⋅G−1)=𝐒⁡(G)⋅𝚫uj​(M)⋅𝐒​(G)−1=0∀j=1,…,N.\\displaystyle\\boldsymbol{\\Delta}^{u^{j}}\\big(\\widehat{M}\\big)=\\boldsymbol{\\Delta}^{u^{j}}\\big({\\mathbf{S}}(G)\\cdot M\\cdot G^{-1}\\big)={\\mathbf{S}}(G)\\cdot\\boldsymbol{\\Delta}^{u^{j}}(M)\\cdot{\\mathbf{S}}(G)^{-1}=0\\qquad\\quad\\forall\\,j=1,\\ldots,N. |  |

Since, by the induction assumption, the statement of Lemma [3](https://arxiv.org/html/2604.26870#Thmlemma3 "Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") is valid for p=kp=k,
equation ( [56](https://arxiv.org/html/2604.26870#S2.E56 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) for M^=M^​(n,u0,…,uk,λ)\\widehat{M}=\\widehat{M}(n,u\_{0},\\ldots,u\_{k},\\uplambda) implies that
there is a gauge transformation 𝔾=𝔾⁡(n,u0,…,uk−1,λ)\\mathbb{G}=\\mathbb{G}(n,u\_{0},\\ldots,u\_{k-1},\\uplambda) such that the matrix

|     |     |     |     |
| --- | --- | --- | --- |
| (57) |  | M˘=𝐒⁡(𝔾)⋅M^​(n,u0,…,uk,λ)⋅𝔾−1\\displaystyle\\breve{M}={\\mathbf{S}}(\\mathbb{G})\\cdot\\widehat{M}(n,u\_{0},\\ldots,u\_{k},\\uplambda)\\cdot\\mathbb{G}^{-1} |  |

obeys ( [51](https://arxiv.org/html/2604.26870#S2.E51 "In Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")). Now we set

|     |     |     |     |
| --- | --- | --- | --- |
| (58) |  | 𝐆⁡(n,u0,…,uk,λ)=𝔾⁡(n,u0,…,uk−1,λ)⋅G⁡(n,u0,…,uk,λ).\\displaystyle\\mathbf{G}(n,u\_{0},\\ldots,u\_{k},\\uplambda)=\\mathbb{G}(n,u\_{0},\\ldots,u\_{k-1},\\uplambda)\\cdot G(n,u\_{0},\\ldots,u\_{k},\\uplambda). |  |

Formulas ( [55](https://arxiv.org/html/2604.26870#S2.E55 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [57](https://arxiv.org/html/2604.26870#S2.E57 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [58](https://arxiv.org/html/2604.26870#S2.E58 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) imply that M˘\\breve{M} satisfies ( [50](https://arxiv.org/html/2604.26870#S2.E50 "In Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
with p=k+1p=k+1. Furthermore, as said above, M˘\\breve{M} obeys ( [51](https://arxiv.org/html/2604.26870#S2.E51 "In Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Therefore, we have proved the statement of Lemma [3](https://arxiv.org/html/2604.26870#Thmlemma3 "Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") in the case p=k+1p=k+1.
∎

###### Theorem 3.

A MLR (𝐌⁡(n,uℓ,…,λ),𝐔⁡(n,uℓ,…,λ))\\big(\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda),\\,\\mathbf{U}(n,u\_{\\ell},\\ldots,\\uplambda)\\big)
is gauge equivalent to a trivial MLR if and only if
𝐌=𝐌⁡(n,uℓ,…,λ)\\mathbf{M}=\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda) satisfies

|     |     |     |     |
| --- | --- | --- | --- |
| (59) |  | 𝚫uj​(𝐌)=0∀j=1,…,N,\\displaystyle\\boldsymbol{\\Delta}^{u^{j}}(\\mathbf{M})=0\\qquad\\quad\\forall\\,j=1,\\ldots,N, |  |

where 𝚫uj​(𝐌)\\boldsymbol{\\Delta}^{u^{j}}(\\mathbf{M}) is determined by formula ( [15](https://arxiv.org/html/2604.26870#S1.E15 "In Definition 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

###### Proof.

Suppose that a MLR (𝐌⁡(n,uℓ,…,λ),𝐔⁡(n,uℓ,…,λ))\\big(\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda),\\,\\mathbf{U}(n,u\_{\\ell},\\ldots,\\uplambda)\\big)
is gauge equivalent to a trivial MLR. This means that there is a
gauge transformation 𝐆=𝐆⁡(n,uℓ,…,λ)\\mathbf{G}=\\mathbf{G}(n,u\_{\\ell},\\ldots,\\uplambda) such that the matrix

|     |     |     |     |
| --- | --- | --- | --- |
| (60) |  | 𝐌^=𝐒⁡(𝐆)⋅𝐌⁡(n,uℓ,…,λ)⋅𝐆−1\\displaystyle\\widehat{\\mathbf{M}}={\\mathbf{S}}(\\mathbf{G})\\cdot\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda)\\cdot\\mathbf{G}^{-1} |  |

obeys

|     |     |     |     |
| --- | --- | --- | --- |
| (61) |  | ∂uℓj(𝐌^)=0∀ℓ∈ℤ,∀j=1,…,N.\\displaystyle\\partial\_{u^{j}\_{\\ell}}(\\widehat{\\mathbf{M}})=0\\qquad\\quad\\forall\\,\\ell\\in\\mathbb{Z},\\qquad\\forall\\,j=1,\\ldots,N. |  |

According to ( [15](https://arxiv.org/html/2604.26870#S1.E15 "In Definition 3. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), property ( [61](https://arxiv.org/html/2604.26870#S2.E61 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) yields

|     |     |     |     |
| --- | --- | --- | --- |
| (62) |  | 𝚫uj​(𝐌^)=0∀j=1,…,N.\\displaystyle\\boldsymbol{\\Delta}^{u^{j}}(\\widehat{\\mathbf{M}})=0\\qquad\\quad\\forall\\,j=1,\\ldots,N. |  |

From ( [60](https://arxiv.org/html/2604.26870#S2.E60 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) one derives

|     |     |     |     |
| --- | --- | --- | --- |
| (63) |  | 𝐌=𝐒​(𝐆)−1⋅𝐌^⋅𝐆=𝐒⁡(𝐆−1)⋅𝐌^⋅𝐆.\\displaystyle\\mathbf{M}={\\mathbf{S}}(\\mathbf{G})^{-1}\\cdot\\widehat{\\mathbf{M}}\\cdot\\mathbf{G}={\\mathbf{S}}\\big(\\mathbf{G}^{-1}\\big)\\cdot\\widehat{\\mathbf{M}}\\cdot\\mathbf{G}. |  |

Using ( [63](https://arxiv.org/html/2604.26870#S2.E63 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [62](https://arxiv.org/html/2604.26870#S2.E62 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and property ( [48](https://arxiv.org/html/2604.26870#S2.E48 "In Theorem 2. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) for M=𝐌^M=\\widehat{\\mathbf{M}} and G=𝐆−1G=\\mathbf{G}^{-1}, we get

|     |     |     |
| --- | --- | --- |
|  | 𝚫uj​(𝐌)=𝚫uj​(𝐒⁡(𝐆−1)⋅𝐌^⋅𝐆)=𝐒⁡(𝐆−1)⋅𝚫uj​(𝐌^)⋅𝐒⁡(𝐆)=0∀j=1,…,N,\\displaystyle\\boldsymbol{\\Delta}^{u^{j}}(\\mathbf{M})=\\boldsymbol{\\Delta}^{u^{j}}\\big({\\mathbf{S}}\\big(\\mathbf{G}^{-1}\\big)\\cdot\\widehat{\\mathbf{M}}\\cdot\\mathbf{G}\\big)={\\mathbf{S}}\\big(\\mathbf{G}^{-1}\\big)\\cdot\\boldsymbol{\\Delta}^{u^{j}}(\\widehat{\\mathbf{M}})\\cdot{\\mathbf{S}}(\\mathbf{G})=0\\qquad\\quad\\forall\\,j=1,\\ldots,N, |  |

thus we obtain ( [59](https://arxiv.org/html/2604.26870#S2.E59 "In Theorem 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

Now, conversely, consider a MLR (𝐌,𝐔)(\\mathbf{M},\\mathbf{U})
with 𝐒{\\mathbf{S}}-part 𝐌=𝐌⁡(n,uℓ,…,λ)\\mathbf{M}=\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda) satisfying ( [59](https://arxiv.org/html/2604.26870#S2.E59 "In Theorem 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
We need to prove that this MLR is gauge equivalent to a trivial MLR.

The rules ( [1](https://arxiv.org/html/2604.26870#S1.EGx6 "1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) imply that there are q∈ℤq\\in\\mathbb{Z} and p∈ℤ≥0p\\in\\mathbb{Z}\_{\\geq 0} such that
the matrix-function 𝐌~=𝐒q​(𝐌)\\widetilde{\\mathbf{M}}={\\mathbf{S}}^{q}(\\mathbf{M}) may depend only on n,u0,…,up,λn,u\_{0},\\ldots,u\_{p},\\uplambda.
By Lemma [1](https://arxiv.org/html/2604.26870#Thmlemma1 "Lemma 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"), the MLR (𝐌,𝐔)(\\mathbf{M},\\mathbf{U})
is gauge equivalent to some MLR (𝐌~,𝐔~)\\big(\\widetilde{\\mathbf{M}},\\widetilde{\\mathbf{U}}\\big) with 𝐒{\\mathbf{S}}-part equal to
𝐒q​(𝐌)=𝐌~​(n,u0,…,up,λ){\\mathbf{S}}^{q}(\\mathbf{M})=\\widetilde{\\mathbf{M}}(n,u\_{0},\\ldots,u\_{p},\\uplambda).
Therefore, there is a gauge transformation G=G⁡(n,uℓ,…,λ)G=G(n,u\_{\\ell},\\ldots,\\uplambda)
such that 𝐌~=𝐒⁡(G)⋅𝐌⋅G−1\\widetilde{\\mathbf{M}}={\\mathbf{S}}(G)\\cdot\\mathbf{M}\\cdot G^{-1}.
Using ( [48](https://arxiv.org/html/2604.26870#S2.E48 "In Theorem 2. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and ( [59](https://arxiv.org/html/2604.26870#S2.E59 "In Theorem 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (64) |  | 𝚫uj​(𝐌~)=𝚫uj​(𝐒⁡(G)⋅𝐌⋅G−1)=𝐒⁡(G)⋅𝚫uj​(𝐌)⋅𝐒​(G)−1=0∀j=1,…,N.\\displaystyle\\boldsymbol{\\Delta}^{u^{j}}\\big(\\widetilde{\\mathbf{M}}\\big)=\\boldsymbol{\\Delta}^{u^{j}}\\big({\\mathbf{S}}(G)\\cdot\\mathbf{M}\\cdot G^{-1}\\big)={\\mathbf{S}}(G)\\cdot\\boldsymbol{\\Delta}^{u^{j}}(\\mathbf{M})\\cdot{\\mathbf{S}}(G)^{-1}=0\\qquad\\quad\\forall\\,j=1,\\ldots,N. |  |

By Lemma [3](https://arxiv.org/html/2604.26870#Thmlemma3 "Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") for 𝐌~=𝐌~​(n,u0,…,up,λ)\\widetilde{\\mathbf{M}}=\\widetilde{\\mathbf{M}}(n,u\_{0},\\ldots,u\_{p},\\uplambda),
property ( [64](https://arxiv.org/html/2604.26870#S2.E64 "In Proof. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) implies that there is a gauge transformation 𝐆=𝐆⁡(u0,…,up−1,λ)\\mathbf{G}=\\mathbf{G}(u\_{0},\\ldots,u\_{p-1},\\uplambda)
such that the matrix M˘=𝐒⁡(𝐆)⋅𝐌~⋅𝐆−1\\breve{M}={\\mathbf{S}}(\\mathbf{G})\\cdot\\widetilde{\\mathbf{M}}\\cdot\\mathbf{G}^{-1} obeys ( [51](https://arxiv.org/html/2604.26870#S2.E51 "In Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

The relations M˘=𝐒⁡(𝐆)⋅𝐌~⋅𝐆−1\\breve{M}={\\mathbf{S}}(\\mathbf{G})\\cdot\\widetilde{\\mathbf{M}}\\cdot\\mathbf{G}^{-1} and
𝐌~=𝐒⁡(G)⋅𝐌⋅G−1\\widetilde{\\mathbf{M}}={\\mathbf{S}}(G)\\cdot\\mathbf{M}\\cdot G^{-1} yield
M˘=𝐒⁡(𝐆​G)⋅𝐌⋅(𝐆​G)−1\\breve{M}={\\mathbf{S}}(\\mathbf{G}G)\\cdot\\mathbf{M}\\cdot(\\mathbf{G}G)^{-1}.
Therefore, applying the gauge transformation 𝐆​G\\mathbf{G}G to the MLR (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}),
we get a MLR with 𝐒{\\mathbf{S}}-part M˘\\breve{M} obeying ( [51](https://arxiv.org/html/2604.26870#S2.E51 "In Lemma 3. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Hence (𝐌,𝐔)(\\mathbf{M},\\mathbf{U}) is gauge equivalent to a trivial MLR.
∎

## 3\. Miura-type transformations and matrix Lax representations

The following lemma is proved easily by a direct calculation.

###### Lemma 4.

Suppose that matrices

|     |     |     |     |
| --- | --- | --- | --- |
| (65) |  | 𝐌=𝐌⁡(n,uℓ,…,λ),𝐔=𝐔⁡(n,uℓ,…,λ)\\displaystyle\\mathbf{M}=\\mathbf{M}(n,u\_{\\ell},\\ldots,\\uplambda),\\qquad\\quad\\mathbf{U}=\\mathbf{U}(n,u\_{\\ell},\\ldots,\\uplambda) |  |

form a MLR for equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Let ( [18](https://arxiv.org/html/2604.26870#S1.E18 "In Definition 5. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) be a MT from equation ( [17](https://arxiv.org/html/2604.26870#S1.E17 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to equation ( [1](https://arxiv.org/html/2604.26870#S1.E1 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
As explained in Definition [5](https://arxiv.org/html/2604.26870#Thmdefinition5 "Definition 5. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"), in formula ( [18](https://arxiv.org/html/2604.26870#S1.E18 "In Definition 5. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) one has
an NN-component vector-function Φ=(Φ1,…,ΦN)\\Phi=(\\Phi^{1},\\dots,\\Phi^{N})
which may depend on nn and on a finite number of the dynamical variables
u~ℓ=(u~ℓ1,…,u~ℓN)\\tilde{u}\_{\\ell}=(\\tilde{u}^{1}\_{\\ell},\\dots,\\tilde{u}^{N}\_{\\ell}), ℓ∈ℤ\\,\\ell\\in\\mathbb{Z}.

Motivated by formula ( [18](https://arxiv.org/html/2604.26870#S1.E18 "In Definition 5. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we substitute uℓ=𝐒ℓ​(Φ)u\_{\\ell}={\\mathbf{S}}^{\\ell}(\\Phi), ℓ∈ℤ\\,\\ell\\in\\mathbb{Z},
in ( [65](https://arxiv.org/html/2604.26870#S3.E65 "In Lemma 4. ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and obtain the matrices

|     |     |     |     |
| --- | --- | --- | --- |
| (66) |  | 𝐌=𝐌⁡(n,𝐒ℓ​(Φ),…,λ),𝐔=𝐔⁡(n,𝐒ℓ​(Φ),…,λ).\\displaystyle\\mathbf{M}=\\mathbf{M}\\big(n,{\\mathbf{S}}^{\\ell}(\\Phi),\\ldots,\\uplambda\\big),\\qquad\\quad\\mathbf{U}=\\mathbf{U}\\big(n,{\\mathbf{S}}^{\\ell}(\\Phi),\\ldots,\\uplambda\\big). |  |

Then ( [66](https://arxiv.org/html/2604.26870#S3.E66 "In Lemma 4. ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is a MLR for equation ( [17](https://arxiv.org/html/2604.26870#S1.E17 "In 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

### 3.1. Non-autonomous examples

The following 22-component non-autonomous equation
was introduced in \[ [11](https://arxiv.org/html/2604.26870#bib.bib11 ""), page 7\] in a study of Darboux transformations

|     |     |     |     |
| --- | --- | --- | --- |
| (67) |  | {∂t(u1)=2​(u12​(u01)2+α⁡(n)​u01−u11),∂t(u2)=2​(u−12−u−11​(u02)2−α⁡(n−1)​u02).\\displaystyle\\left\\{\\begin{aligned} \\partial\_{t}(u^{1})&=2\\big(u^{2}\_{1}(u^{1}\_{0})^{2}+\\upalpha(n)u^{1}\_{0}-u^{1}\_{1}\\big),\\\<br>\\partial\_{t}(u^{2})&=2\\big(u^{2}\_{-1}-u^{1}\_{-1}(u^{2}\_{0})^{2}-\\upalpha(n-1)u^{2}\_{0}\\big).\\end{aligned}\\right. |  |

Here α⁡(n)\\upalpha(n) is an arbitrary function.
(This equation is given in \[ [11](https://arxiv.org/html/2604.26870#bib.bib11 ""), page 7\] in different notation,
using functions p⁡(n,x)p(n,x), q⁡(n,x)q(n,x), instead of u1​(n,t)u^{1}(n,t), u2​(n,t)u^{2}(n,t).)

The results of \[ [11](https://arxiv.org/html/2604.26870#bib.bib11 "")\] imply
that the following matrices form a MLR for ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))

|     |     |     |     |
| --- | --- | --- | --- |
| (68) |  | 𝐌~=(λ+α⁡(n)+u01​u12u01u121),𝐔~=(−λ−2​u01−2​u02λ).\\displaystyle\\widetilde{\\mathbf{M}}=\\begin{pmatrix}{\\uplambda}+\\upalpha(n)+u^{1}\_{0}u^{2}\_{1}&u^{1}\_{0}\\\<br>u^{2}\_{1}&1\\\<br>\\end{pmatrix},\\qquad\\quad\\widetilde{\\mathbf{U}}=\\begin{pmatrix}-{\\uplambda}&-2u^{1}\_{0}\\\<br>-2u^{2}\_{0}&{\\uplambda}\\\<br>\\end{pmatrix}. |  |

The MLR ( [68](https://arxiv.org/html/2604.26870#S3.E68 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is not uu-tame (in the sense of Definition [6](https://arxiv.org/html/2604.26870#Thmdefinition6 "Definition 6. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
In order to obtain a uu-tame MLR, we relabel

|     |     |     |     |
| --- | --- | --- | --- |
| (69) |  | uℓ1↦uℓ1,uℓ2↦uℓ−12∀ℓ∈ℤ.\\displaystyle u^{1}\_{\\ell}\\,\\mapsto\\,u^{1}\_{\\ell},\\qquad\\quad u^{2}\_{\\ell}\\,\\mapsto\\,u^{2}\_{\\ell-1}\\qquad\\quad\\forall\\,\\ell\\in\\mathbb{Z}. |  |

This means that we make the following invertible change of variables

|     |     |     |
| --- | --- | --- |
|  | u1​(n,t)↦u1​(n,t),u2​(n,t)↦u2​(n−1,t).\\displaystyle u^{1}(n,t)\\,\\mapsto\\,u^{1}(n,t),\\qquad u^{2}(n,t)\\,\\mapsto\\,u^{2}(n\\!-\\!1,t). |  |

Applying the (invertible) change ( [69](https://arxiv.org/html/2604.26870#S3.E69 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [68](https://arxiv.org/html/2604.26870#S3.E68 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (70) |  | {∂t(u1)=2​(u02​(u01)2+α⁡(n)​u01−u11),∂t(u−12)=2​(u−22−u−11​(u−12)2−α⁡(n−1)​u−12),\\displaystyle\\left\\{\\begin{aligned} \\partial\_{t}(u^{1})&=2\\big(u^{2}\_{0}(u^{1}\_{0})^{2}+\\upalpha(n)u^{1}\_{0}-u^{1}\_{1}\\big),\\\<br>\\partial\_{t}(u^{2}\_{-1})&=2\\big(u^{2}\_{-2}-u^{1}\_{-1}(u^{2}\_{-1})^{2}-\\upalpha(n-1)u^{2}\_{-1}\\big),\\end{aligned}\\right. |  |
| (71) |  | 𝐌˘=(λ+α⁡(n)+u01​u02u01u021),𝐔˘=(−λ−2​u01−2​u−12λ).\\displaystyle\\breve{\\mathbf{M}}=\\begin{pmatrix}{\\uplambda}+\\upalpha(n)+u^{1}\_{0}u^{2}\_{0}&u^{1}\_{0}\\\<br>u^{2}\_{0}&1\\\<br>\\end{pmatrix},\\qquad\\quad\\breve{\\mathbf{U}}=\\begin{pmatrix}-{\\uplambda}&-2u^{1}\_{0}\\\<br>-2u^{2}\_{-1}&{\\uplambda}\\\<br>\\end{pmatrix}. |  |

Applying the (invertible) operator 𝐒{\\mathbf{S}} to the second component in ( [70](https://arxiv.org/html/2604.26870#S3.E70 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), one obtains

|     |     |     |     |
| --- | --- | --- | --- |
| (72) |  | {∂t(u1)=2​(u02​(u01)2+α⁡(n)​u01−u11),∂t(u2)=2​(u−12−u01​(u02)2−α⁡(n)​u02).\\displaystyle\\left\\{\\begin{aligned} \\partial\_{t}(u^{1})&=2\\big(u^{2}\_{0}(u^{1}\_{0})^{2}+\\upalpha(n)u^{1}\_{0}-u^{1}\_{1}\\big),\\\<br>\\partial\_{t}(u^{2})&=2\\big(u^{2}\_{-1}-u^{1}\_{0}(u^{2}\_{0})^{2}-\\upalpha(n)u^{2}\_{0}\\big).\\end{aligned}\\right. |  |

Since ( [68](https://arxiv.org/html/2604.26870#S3.E68 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is a MLR for equation ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
the described way of deriving ( [71](https://arxiv.org/html/2604.26870#S3.E71 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
from ( [68](https://arxiv.org/html/2604.26870#S3.E68 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) implies that ( [71](https://arxiv.org/html/2604.26870#S3.E71 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is a MLR for equation ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Furthermore, equation ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is equivalent to equation ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
as ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is obtained from ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) by means of invertible operations, as described above.
The MLR ( [71](https://arxiv.org/html/2604.26870#S3.E71 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is uu-tame, and this will allow us to construct a MT, as shown below.

Fix a constant c∈ℂ\\mathrm{c}\\in\\mathbb{C}.
In what follows, we use the matrices ( [71](https://arxiv.org/html/2604.26870#S3.E71 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) with λ\\uplambda replaced by c\\mathrm{c}.
According to Definition [1](https://arxiv.org/html/2604.26870#Thmdefinition1 "Definition 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"), since the matrices ( [71](https://arxiv.org/html/2604.26870#S3.E71 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
form a MLR for equation ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we can consider the auxiliary system

|     |     |     |     |
| --- | --- | --- | --- |
| (73) |  | 𝐒⁡(Ψ)=(c+α⁡(n)+u01​u02u01u021)⋅Ψ,∂t(Ψ)=(−c−2​u01−2​u−12c)⋅Ψ,\\displaystyle{\\mathbf{S}}(\\Psi)=\\begin{pmatrix}{\\mathrm{c}}+\\upalpha(n)+u^{1}\_{0}u^{2}\_{0}&u^{1}\_{0}\\\<br>u^{2}\_{0}&1\\\<br>\\end{pmatrix}\\cdot\\Psi,\\qquad\\quad\\partial\_{t}(\\Psi)=\\begin{pmatrix}-{\\mathrm{c}}&-2u^{1}\_{0}\\\<br>-2u^{2}\_{-1}&{\\mathrm{c}}\\\<br>\\end{pmatrix}\\cdot\\Psi, |  |

which is compatible modulo equation ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Here Ψ=Ψ⁡(n,t)\\Psi=\\Psi(n,t) is an invertible 2×22\\times 2 matrix
whose elements we denote by ψi​j=ψi​j​(n,t)\\uppsi^{ij}=\\uppsi^{ij}(n,t), i,j=1,2\\,i,j=1,2.

Substituting Ψ=(ψ11ψ12ψ21ψ22)\\Psi=\\begin{pmatrix}\\uppsi^{11}&\\uppsi^{12}\\\
\\uppsi^{21}&\\uppsi^{22}\\end{pmatrix} in ( [73](https://arxiv.org/html/2604.26870#S3.E73 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and considering the first columns
in the matrix equations ( [73](https://arxiv.org/html/2604.26870#S3.E73 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), one gets

|     |     |     |     |
| --- | --- | --- | --- |
| (74) |  | 𝐒⁡(ψ11)=(c+α⁡(n)+u01​u02)​ψ11+u01​ψ21,𝐒⁡(ψ21)=u02​ψ11+ψ21,\\displaystyle{\\mathbf{S}}(\\uppsi^{11})=({\\mathrm{c}}+\\upalpha(n)+u^{1}\_{0}u^{2}\_{0})\\uppsi^{11}+u^{1}\_{0}\\uppsi^{21},\\qquad\\quad{\\mathbf{S}}(\\uppsi^{21})=u^{2}\_{0}\\uppsi^{11}+\\uppsi^{21}, |  |
| (75) |  | ∂t(ψ11)=−c​ψ11−2​u01​ψ21,∂t(ψ21)=−2​u−12​ψ11+c​ψ21.\\displaystyle\\partial\_{t}(\\uppsi^{11})=-{\\mathrm{c}}\\uppsi^{11}-2u^{1}\_{0}\\uppsi^{21},\\qquad\\quad\\partial\_{t}(\\uppsi^{21})=-2u^{2}\_{-1}\\uppsi^{11}+{\\mathrm{c}}\\uppsi^{21}. |  |

Now we employ the standard idea to consider the function w=ψ11/ψ21w={\\uppsi^{11}}/{\\uppsi^{21}}.
Using ( [74](https://arxiv.org/html/2604.26870#S3.E74 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [75](https://arxiv.org/html/2604.26870#S3.E75 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we derive

|     |     |     |     |
| --- | --- | --- | --- |
| (76) |  | 𝐒⁡(w)=𝐒⁡(ψ11)𝐒⁡(ψ21)=(c+α⁡(n)+u01​u02)​ψ11+u01​ψ21u02​ψ11+ψ21==(c+α⁡(n)+u01​u02)​(ψ11/ψ21)+u01u02​(ψ11/ψ21)+1=(c+α⁡(n)+u01​u02)​w+u01u02​w+1,\\displaystyle\\begin{split}{\\mathbf{S}}(w)&=\\frac{{\\mathbf{S}}(\\uppsi^{11})}{{\\mathbf{S}}(\\uppsi^{21})}=\\frac{({\\mathrm{c}}+\\upalpha(n)+u^{1}\_{0}u^{2}\_{0})\\uppsi^{11}+u^{1}\_{0}\\uppsi^{21}}{u^{2}\_{0}\\uppsi^{11}+\\uppsi^{21}}=\\\<br>&=\\frac{({\\mathrm{c}}+\\upalpha(n)+u^{1}\_{0}u^{2}\_{0})(\\uppsi^{11}/\\uppsi^{21})+u^{1}\_{0}}{u^{2}\_{0}(\\uppsi^{11}/{\\uppsi^{21}})+1}=\\frac{({\\mathrm{c}}+\\upalpha(n)+u^{1}\_{0}u^{2}\_{0})w+u^{1}\_{0}}{u^{2}\_{0}w+1},\\end{split} |  |
| (77) |  | ∂t(w)=∂t(ψ11ψ21)=∂t(ψ11)ψ21−ψ11​∂t(ψ21)(ψ21)2=−c​ψ11−2​u01​ψ21ψ21−ψ11​(−2​u−12​ψ11+c​ψ21)(ψ21)2==−c​ψ11ψ21−2​u01+2​u−12​(ψ11ψ21)2−c​ψ11ψ21=2​u−12​(w)2−2​c​w−2​u01.\\displaystyle\\begin{split}\\partial\_{t}(w)&=\\partial\_{t}\\Big(\\frac{\\uppsi^{11}}{\\uppsi^{21}}\\Big)=\\frac{\\partial\_{t}(\\uppsi^{11})}{\\uppsi^{21}}-\\frac{\\uppsi^{11}\\partial\_{t}(\\uppsi^{21})}{(\\uppsi^{21})^{2}}=\\frac{-{\\mathrm{c}}\\uppsi^{11}-2u^{1}\_{0}\\uppsi^{21}}{\\uppsi^{21}}-\\frac{\\uppsi^{11}(-2u^{2}\_{-1}\\uppsi^{11}+{\\mathrm{c}}\\uppsi^{21})}{(\\uppsi^{21})^{2}}=\\\<br>&=-{\\mathrm{c}}\\frac{\\uppsi^{11}}{\\uppsi^{21}}-2u^{1}\_{0}+2u^{2}\_{-1}\\Big(\\frac{\\uppsi^{11}}{\\uppsi^{21}}\\Big)^{2}-{\\mathrm{c}}\\frac{\\uppsi^{11}}{\\uppsi^{21}}=2u^{2}\_{-1}(w)^{2}-2{\\mathrm{c}}w-2u^{1}\_{0}.\\end{split} |  |

From ( [76](https://arxiv.org/html/2604.26870#S3.E76 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [77](https://arxiv.org/html/2604.26870#S3.E77 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) one gets

|     |     |     |     |
| --- | --- | --- | --- |
| (78) |  | 𝐒⁡(w)=(c+α⁡(n)+u01​u02)​w+u01u02​w+1,\\displaystyle{\\mathbf{S}}(w)=\\frac{({\\mathrm{c}}+\\upalpha(n)+u^{1}\_{0}u^{2}\_{0})w+u^{1}\_{0}}{u^{2}\_{0}w+1}, |  |
| (79) |  | ∂t(w)=2​u−12​(w)2−2​c​w−2​u01.\\displaystyle\\partial\_{t}(w)=2u^{2}\_{-1}(w)^{2}-2{\\mathrm{c}}w-2u^{1}\_{0}. |  |

We have derived equations ( [78](https://arxiv.org/html/2604.26870#S3.E78 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [79](https://arxiv.org/html/2604.26870#S3.E79 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) from system ( [73](https://arxiv.org/html/2604.26870#S3.E73 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
which is compatible modulo equation ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
The described procedure of deriving ( [78](https://arxiv.org/html/2604.26870#S3.E78 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [79](https://arxiv.org/html/2604.26870#S3.E79 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) implies that
system ( [78](https://arxiv.org/html/2604.26870#S3.E78 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [79](https://arxiv.org/html/2604.26870#S3.E79 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) as well.

From ( [78](https://arxiv.org/html/2604.26870#S3.E78 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) one obtains

|     |     |     |     |
| --- | --- | --- | --- |
| (80) |  | u1=u01=𝐒⁡(w)​u02​w+𝐒⁡(w)−c​w−α⁡(n)​ww​u02+1.\\displaystyle u^{1}=u^{1}\_{0}=\\frac{{\\mathbf{S}}(w)u^{2}\_{0}w+{\\mathbf{S}}(w)-{\\mathrm{c}}w-\\upalpha(n)w}{wu^{2}\_{0}+1}. |  |

We set

|     |     |     |     |
| --- | --- | --- | --- |
| (81) |  | u~1:=w,u~2:=u2.\\displaystyle\\tilde{u}^{1}:=w,\\qquad\\qquad\\tilde{u}^{2}:=u^{2}. |  |

From ( [81](https://arxiv.org/html/2604.26870#S3.E81 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) one derives 𝐒⁡(w)=𝐒⁡(u~1)=u~11{\\mathbf{S}}(w)={\\mathbf{S}}(\\tilde{u}^{1})=\\tilde{u}^{1}\_{1}.
As usual, we have u0i=uiu^{i}\_{0}=u^{i}, u~0i=u~i\\,\\tilde{u}^{i}\_{0}=\\tilde{u}^{i} for i=1,2i=1,2.
Now we substitute w=u~01w=\\tilde{u}^{1}\_{0}, 𝐒⁡(w)=u~11\\,{\\mathbf{S}}(w)=\\tilde{u}^{1}\_{1}, u02=u~02\\,u^{2}\_{0}=\\tilde{u}^{2}\_{0}
in ( [80](https://arxiv.org/html/2604.26870#S3.E80 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and consider the obtained equation along with u2=u~02u^{2}=\\tilde{u}^{2}\_{0}, which gives

|     |     |     |     |
| --- | --- | --- | --- |
| (82) |  | {u1=u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01u~01​u~02+1,u2=u~02.\\displaystyle\\left\\{\\begin{aligned} u^{1}&=\\frac{\\tilde{u}^{1}\_{1}\\tilde{u}^{2}\_{0}\\tilde{u}^{1}\_{0}+\\tilde{u}^{1}\_{1}-{\\mathrm{c}}\\tilde{u}^{1}\_{0}-\\upalpha(n)\\tilde{u}^{1}\_{0}}{\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1},\\\<br>u^{2}&=\\tilde{u}^{2}\_{0}.\\end{aligned}\\right. |  |

For each ℓ∈ℤ\\ell\\in\\mathbb{Z}, applying the operator 𝐒ℓ{\\mathbf{S}}^{\\ell} to ( [82](https://arxiv.org/html/2604.26870#S3.E82 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (83) |  | {uℓ1=u~ℓ+11​u~ℓ2​u~ℓ1+u~ℓ+11−c​u~ℓ1−α⁡(n+ℓ)​u~ℓ1u~ℓ1​u~ℓ2+1,uℓ2=u~2ℓ,ℓ∈ℤ.\\displaystyle\\left\\{\\begin{aligned} u^{1}\_{\\ell}&=\\frac{\\tilde{u}^{1}\_{\\ell+1}\\tilde{u}^{2}\_{\\ell}\\tilde{u}^{1}\_{\\ell}+\\tilde{u}^{1}\_{\\ell+1}-{\\mathrm{c}}\\tilde{u}^{1}\_{\\ell}-\\upalpha(n+\\ell)\\tilde{u}^{1}\_{\\ell}}{\\tilde{u}^{1}\_{\\ell}\\tilde{u}^{2}\_{\\ell}+1},\\\<br>u^{2}\_{\\ell}&=\\tilde{u}^{2}\_{\\ell},\\qquad\\qquad\\qquad\\qquad\\ell\\in\\mathbb{Z}.\\end{aligned}\\right. |  |

Substituting w=u~1w=\\tilde{u}^{1} and ( [83](https://arxiv.org/html/2604.26870#S3.E83 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) in ( [79](https://arxiv.org/html/2604.26870#S3.E79 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we derive

|     |     |     |     |
| --- | --- | --- | --- |
| (84) |  | ∂t(u~1)=2​u~−12​(u~01)2−2​c​u~01−2​(u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01)u~01​u~02+1.\\displaystyle\\partial\_{t}(\\tilde{u}^{1})=2\\tilde{u}^{2}\_{-1}(\\tilde{u}^{1}\_{0})^{2}-2{\\mathrm{c}}\\tilde{u}^{1}\_{0}-\\frac{2(\\tilde{u}^{1}\_{1}\\tilde{u}^{2}\_{0}\\tilde{u}^{1}\_{0}+\\tilde{u}^{1}\_{1}-{\\mathrm{c}}\\tilde{u}^{1}\_{0}-\\upalpha(n)\\tilde{u}^{1}\_{0})}{\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1}. |  |

Now we consider ( [84](https://arxiv.org/html/2604.26870#S3.E84 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) along with the equation obtained
by means of substituting ( [83](https://arxiv.org/html/2604.26870#S3.E83 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) in the second component of ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
This gives the 22-component non-autonomous equation

|     |     |     |     |
| --- | --- | --- | --- |
| (85) |  | {∂t(u~1)=2​u~−12​(u~01)2−2​c​u~01−2​(u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01)u~01​u~02+1,∂t(u~2)=2​u~−12−2​α​(n)​u~02−2​(u~02)2​(u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01)u~01​u~02+1.\\displaystyle\\left\\{\\begin{aligned} \\partial\_{t}(\\tilde{u}^{1})&=2\\tilde{u}^{2}\_{-1}(\\tilde{u}^{1}\_{0})^{2}-2{\\mathrm{c}}\\tilde{u}^{1}\_{0}-\\frac{2\\big(\\tilde{u}^{1}\_{1}\\tilde{u}^{2}\_{0}\\tilde{u}^{1}\_{0}+\\tilde{u}^{1}\_{1}-{\\mathrm{c}}\\tilde{u}^{1}\_{0}-\\upalpha(n)\\tilde{u}^{1}\_{0}\\big)}{\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1},\\\<br>\\partial\_{t}(\\tilde{u}^{2})&=2\\tilde{u}^{2}\_{-1}-2\\upalpha(n)\\tilde{u}^{2}\_{0}-\\frac{2(\\tilde{u}^{2}\_{0})^{2}\\big(\\tilde{u}^{1}\_{1}\\tilde{u}^{2}\_{0}\\tilde{u}^{1}\_{0}+\\tilde{u}^{1}\_{1}-{\\mathrm{c}}\\tilde{u}^{1}\_{0}-\\upalpha(n)\\tilde{u}^{1}\_{0}\\big)}{\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1}.\\end{aligned}\\right. |  |

As discussed above,
system ( [78](https://arxiv.org/html/2604.26870#S3.E78 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [79](https://arxiv.org/html/2604.26870#S3.E79 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Since equations ( [82](https://arxiv.org/html/2604.26870#S3.E82 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
are derived from ( [78](https://arxiv.org/html/2604.26870#S3.E78 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [79](https://arxiv.org/html/2604.26870#S3.E79 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) (by means of introducing ( [81](https://arxiv.org/html/2604.26870#S3.E81 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))),
system ( [82](https://arxiv.org/html/2604.26870#S3.E82 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) as well.
This implies that ( [82](https://arxiv.org/html/2604.26870#S3.E82 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is a MT from ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
(This fact can also be checked independently by a straightforward computation.)

Thus ( [82](https://arxiv.org/html/2604.26870#S3.E82 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is a MT for equation ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
As explained above, ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is obtained from ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
by means of an invertible transformation involving ( [69](https://arxiv.org/html/2604.26870#S3.E69 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
In order to return from ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and to derive a MT for equation ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
we are going to use the relabeling

|     |     |     |     |
| --- | --- | --- | --- |
| (86) |  | uℓ1↦uℓ1,uℓ2↦uℓ+12∀ℓ∈ℤ,\\displaystyle u^{1}\_{\\ell}\\,\\mapsto\\,u^{1}\_{\\ell},\\qquad u^{2}\_{\\ell}\\,\\mapsto\\,u^{2}\_{\\ell+1}\\qquad\\quad\\forall\\,\\ell\\in\\mathbb{Z}, |  |

which is the inverse of ( [69](https://arxiv.org/html/2604.26870#S3.E69 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
That is, we make the change u1​(n,t)↦u1​(n,t)u^{1}(n,t)\\mapsto u^{1}(n,t),
u2​(n,t)↦u2​(n+1,t)\\,u^{2}(n,t)\\mapsto u^{2}(n\\!+\\!1,t).

Applying the relabeling ( [86](https://arxiv.org/html/2604.26870#S3.E86 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and ( [82](https://arxiv.org/html/2604.26870#S3.E82 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we obtain

|     |     |     |     |
| --- | --- | --- | --- |
| (87) |  | {∂t(u1)=2​(u12​(u01)2+α⁡(n)​u01−u11),∂t(u12)=2​(u02−u01​(u12)2−α⁡(n)​u12).\\displaystyle\\left\\{\\begin{aligned} \\partial\_{t}(u^{1})&=2\\big(u^{2}\_{1}(u^{1}\_{0})^{2}+\\upalpha(n)u^{1}\_{0}-u^{1}\_{1}\\big),\\\<br>\\partial\_{t}(u^{2}\_{1})&=2\\big(u^{2}\_{0}-u^{1}\_{0}(u^{2}\_{1})^{2}-\\upalpha(n)u^{2}\_{1}\\big).\\end{aligned}\\right. |  |
| (88) |  | {u1=u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01u~01​u~02+1,u12=u~02.\\displaystyle\\left\\{\\begin{aligned} u^{1}&=\\frac{\\tilde{u}^{1}\_{1}\\tilde{u}^{2}\_{0}\\tilde{u}^{1}\_{0}+\\tilde{u}^{1}\_{1}-{\\mathrm{c}}\\tilde{u}^{1}\_{0}-\\upalpha(n)\\tilde{u}^{1}\_{0}}{\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1},\\\<br>u^{2}\_{1}&=\\tilde{u}^{2}\_{0}.\\end{aligned}\\right. |  |

Applying the operator 𝐒−1{\\mathbf{S}}^{-1} to the second component in ( [87](https://arxiv.org/html/2604.26870#S3.E87 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and in ( [88](https://arxiv.org/html/2604.26870#S3.E88 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
one gets ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and

|     |     |     |     |
| --- | --- | --- | --- |
| (89) |  | {u1=u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01u~01​u~02+1,u2=u~−12.\\displaystyle\\left\\{\\begin{aligned} u^{1}&=\\frac{\\tilde{u}^{1}\_{1}\\tilde{u}^{2}\_{0}\\tilde{u}^{1}\_{0}+\\tilde{u}^{1}\_{1}-{\\mathrm{c}}\\tilde{u}^{1}\_{0}-\\upalpha(n)\\tilde{u}^{1}\_{0}}{\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1},\\\<br>u^{2}&=\\tilde{u}^{2}\_{-1}.\\end{aligned}\\right. |  |

Thus ( [89](https://arxiv.org/html/2604.26870#S3.E89 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is a MT from ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [67](https://arxiv.org/html/2604.26870#S3.E67 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

In what follows, we use the dynamical variables
u~ℓ=(u~ℓ1,u~ℓ2)\\tilde{u}\_{\\ell}=(\\tilde{u}^{1}\_{\\ell},\\tilde{u}^{2}\_{\\ell}), ℓ∈ℤ\\,\\ell\\in\\mathbb{Z}.
Recall that ( [71](https://arxiv.org/html/2604.26870#S3.E71 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is a MLR for equation ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
and formulas ( [83](https://arxiv.org/html/2604.26870#S3.E83 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) are obtained by applying the operator 𝐒ℓ{\\mathbf{S}}^{\\ell} to ( [82](https://arxiv.org/html/2604.26870#S3.E82 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Then, applying Lemma [4](https://arxiv.org/html/2604.26870#Thmlemma4 "Lemma 4. ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") to the MLR ( [71](https://arxiv.org/html/2604.26870#S3.E71 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and
to the MT ( [82](https://arxiv.org/html/2604.26870#S3.E82 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) from ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [72](https://arxiv.org/html/2604.26870#S3.E72 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
we substitute ( [83](https://arxiv.org/html/2604.26870#S3.E83 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) in ( [71](https://arxiv.org/html/2604.26870#S3.E71 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and obtain the following MLR for equation ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))

|     |     |     |     |
| --- | --- | --- | --- |
| (90) |  | 𝐌⁡(n,u~0,u~1,λ)=(λ+α⁡(n)+u~02​(u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01)u~01​u~02+1u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01u~01​u~02+1u~021),\\displaystyle\\mathbf{M}(n,\\tilde{u}\_{0},\\tilde{u}\_{1},\\uplambda)=\\begin{pmatrix}{\\uplambda}+\\upalpha(n)+\\frac{\\tilde{u}^{2}\_{0}(\\tilde{u}^{1}\_{1}\\tilde{u}^{2}\_{0}\\tilde{u}^{1}\_{0}+\\tilde{u}^{1}\_{1}-{\\mathrm{c}}\\tilde{u}^{1}\_{0}-\\upalpha(n)\\tilde{u}^{1}\_{0})}{\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1}&\\frac{\\tilde{u}^{1}\_{1}\\tilde{u}^{2}\_{0}\\tilde{u}^{1}\_{0}+\\tilde{u}^{1}\_{1}-{\\mathrm{c}}\\tilde{u}^{1}\_{0}-\\upalpha(n)\\tilde{u}^{1}\_{0}}{\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1}\\\<br>\\tilde{u}^{2}\_{0}&1\\\<br>\\end{pmatrix}, |  |
| (91) |  | 𝐔⁡(n,u~−1,u~0,u~1,λ)=(−λ−2​(u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01)u~01​u~02+1−2​u~−12λ).\\displaystyle\\mathbf{U}(n,\\tilde{u}\_{-1},\\tilde{u}\_{0},\\tilde{u}\_{1},\\uplambda)=\\begin{pmatrix}-{\\uplambda}&-\\frac{2(\\tilde{u}^{1}\_{1}\\tilde{u}^{2}\_{0}\\tilde{u}^{1}\_{0}+\\tilde{u}^{1}\_{1}-{\\mathrm{c}}\\tilde{u}^{1}\_{0}-\\upalpha(n)\\tilde{u}^{1}\_{0})}{\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1}\\\<br>-2\\tilde{u}^{2}\_{-1}&{\\uplambda}\\\<br>\\end{pmatrix}. |  |

In order to simplify the MLR ( [90](https://arxiv.org/html/2604.26870#S3.E90 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [91](https://arxiv.org/html/2604.26870#S3.E91 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) by means of gauge transformations,
we consider Theorem [1](https://arxiv.org/html/2604.26870#Thmtheorem1 "Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")
in the case N=2N=2, d=2\\,\\mathrm{d}=2, p=1\\,p=1 with u~ℓ\\tilde{u}\_{\\ell} instead of uℓu\_{\\ell}.
The matrix ( [90](https://arxiv.org/html/2604.26870#S3.E90 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) satisfies condition ( [27](https://arxiv.org/html/2604.26870#S2.E27 "In 2nd item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) with p=1p=1.
Therefore, we can apply Theorem [1](https://arxiv.org/html/2604.26870#Thmtheorem1 "Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") to the MLR ( [90](https://arxiv.org/html/2604.26870#S3.E90 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [91](https://arxiv.org/html/2604.26870#S3.E91 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
To this end, we need to do the following.

- •


Choose a constant vector a0=(a01,a02)∈ℂ2a\_{0}=(a^{1}\_{0},a^{2}\_{0})\\in\\mathbb{C}^{2}.

- •


Substitute u~0=a0\\tilde{u}\_{0}=a\_{0} in 𝐌⁡(n,u~0,u~1,λ)\\mathbf{M}(n,\\tilde{u}\_{0},\\tilde{u}\_{1},\\uplambda)
given by ( [90](https://arxiv.org/html/2604.26870#S3.E90 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) (i.e., substitute u~0i=a0i\\tilde{u}^{i}\_{0}=a^{i}\_{0} for i=1,2i=1,2 in ( [90](https://arxiv.org/html/2604.26870#S3.E90 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))).

- •


Compute 𝐆⁡(n,u~0,λ)\\mathbf{G}(n,\\tilde{u}\_{0},\\uplambda) given by formula ( [28](https://arxiv.org/html/2604.26870#S2.E28 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
which involves the matrix



|     |     |     |
| --- | --- | --- |
|  | 𝐌​(n,a0,u~1,λ)−1=(λ+α⁡(n)+a02​(u~11​a02​a01+u~11−c​a01−α⁡(n)​a01)a01​a02+1u~11​a02​a01+u~11−c​a01−α⁡(n)​a01a01​a02+1a021)−1==(1λ+α⁡(n)a01​α​(n)+a01​c−a01​a02​u~11−u~11(a01​a02+1)​(λ+α⁡(n))−a02λ+α⁡(n)a01​u~11​(a02)2+a01​λ​a02−a01​c​a02+u~11​a02+λ+α⁡(n)(a01​a02+1)​(λ+α⁡(n))).\\displaystyle\\begin{gathered}\\mathbf{M}(n,a\_{0},\\tilde{u}\_{1},\\uplambda)^{-1}=\\begin{pmatrix}{\\uplambda}+\\upalpha(n)+\\frac{a^{2}\_{0}(\\tilde{u}^{1}\_{1}a^{2}\_{0}a^{1}\_{0}+\\tilde{u}^{1}\_{1}-{\\mathrm{c}}a^{1}\_{0}-\\upalpha(n)a^{1}\_{0})}{a^{1}\_{0}a^{2}\_{0}+1}&\\frac{\\tilde{u}^{1}\_{1}a^{2}\_{0}a^{1}\_{0}+\\tilde{u}^{1}\_{1}-{\\mathrm{c}}a^{1}\_{0}-\\upalpha(n)a^{1}\_{0}}{a^{1}\_{0}a^{2}\_{0}+1}\\\<br>a^{2}\_{0}&1\\\<br>\\end{pmatrix}^{-1}=\\\<br>=\\begin{pmatrix}\\frac{1}{{\\uplambda}+\\upalpha(n)}&\\frac{a^{1}\_{0}\\upalpha(n)+a^{1}\_{0}{\\mathrm{c}}-a^{1}\_{0}a^{2}\_{0}\\tilde{u}^{1}\_{1}-\\tilde{u}^{1}\_{1}}{(a^{1}\_{0}a^{2}\_{0}+1)({\\uplambda}+\\upalpha(n))}\\\<br>-\\frac{a^{2}\_{0}}{{\\uplambda}+\\upalpha(n)}&\\frac{a^{1}\_{0}\\tilde{u}^{1}\_{1}(a^{2}\_{0})^{2}+a^{1}\_{0}{\\uplambda}a^{2}\_{0}-a^{1}\_{0}{\\mathrm{c}}a^{2}\_{0}+\\tilde{u}^{1}\_{1}a^{2}\_{0}+{\\uplambda}+\\upalpha(n)}{(a^{1}\_{0}a^{2}\_{0}+1)({\\uplambda}+\\upalpha(n))}\\\<br>\\end{pmatrix}.\\end{gathered} |  |

- •


Apply the obtained gauge transformation 𝐆=𝐆⁡(n,u~0,λ)\\mathbf{G}=\\mathbf{G}(n,\\tilde{u}\_{0},\\uplambda)
to the MLR ( [90](https://arxiv.org/html/2604.26870#S3.E90 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [91](https://arxiv.org/html/2604.26870#S3.E91 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and compute
the gauge equivalent MLR (𝐌^,𝐔^)\\big(\\widehat{\\mathbf{M}},\\,\\widehat{\\mathbf{U}}\\big) given by ( [30](https://arxiv.org/html/2604.26870#S2.E30 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).


We can choose for a0=(a01,a02)a\_{0}=(a^{1}\_{0},a^{2}\_{0}) any constant vector
such that ( [• ‣ 3.1](https://arxiv.org/html/2604.26870#S3.EGx85 "3rd item ‣ 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is well defined.
In order to make formula ( [• ‣ 3.1](https://arxiv.org/html/2604.26870#S3.EGx85 "3rd item ‣ 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) as simple as possible, we take

|     |     |     |     |
| --- | --- | --- | --- |
| (94) |  | a01=0,a02=0.\\displaystyle a^{1}\_{0}=0,\\qquad a^{2}\_{0}=0. |  |

Then, using ( [• ‣ 3.1](https://arxiv.org/html/2604.26870#S3.EGx85 "3rd item ‣ 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) with ( [94](https://arxiv.org/html/2604.26870#S3.E94 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we see that ( [28](https://arxiv.org/html/2604.26870#S2.E28 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) reads

|     |     |     |     |
| --- | --- | --- | --- |
| (95) |  | 𝐆⁡(n,u~0,λ)=𝐒−1​(𝐌​(n,a0,u~1,λ)−1)=𝐒−1​((1λ+α⁡(n)−u~11λ+α⁡(n)01))=(1λ+α⁡(n−1)−u~01λ+α⁡(n−1)01).\\displaystyle\\mathbf{G}(n,\\tilde{u}\_{0},\\uplambda)={\\mathbf{S}}^{-1}\\big(\\mathbf{M}(n,a\_{0},\\tilde{u}\_{1},\\uplambda)^{-1}\\big)={\\mathbf{S}}^{-1}\\left(\\begin{pmatrix}\\frac{1}{{\\uplambda}+\\upalpha(n)}&-\\frac{\\tilde{u}^{1}\_{1}}{{\\uplambda}+\\upalpha(n)}\\\<br>0&1\\\<br>\\end{pmatrix}\\right)=\\begin{pmatrix}\\frac{1}{{\\uplambda}+\\upalpha(n-1)}&-\\frac{\\tilde{u}^{1}\_{0}}{{\\uplambda}+\\upalpha(n-1)}\\\<br>0&1\\\<br>\\end{pmatrix}. |  |

Applying the obtained gauge transformation ( [95](https://arxiv.org/html/2604.26870#S3.E95 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to the MLR ( [90](https://arxiv.org/html/2604.26870#S3.E90 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [91](https://arxiv.org/html/2604.26870#S3.E91 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
and computing the MLR (𝐌^,𝐔^)\\big(\\widehat{\\mathbf{M}},\\,\\widehat{\\mathbf{U}}\\big) given by ( [30](https://arxiv.org/html/2604.26870#S2.E30 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (96) |  | 𝐌^​(n,u~0,λ)=𝐒⁡(𝐆)⋅𝐌⋅𝐆−1=((λ+α⁡(n−1))​(u~01​u~02​λ+λ+α⁡(n)−c​u~01​u~02)(λ+α⁡(n))​(u~01​u~02+1)(λ−c)​u~01λ+α⁡(n)(λ+α⁡(n−1))​u~02u~01​u~02+1),\\displaystyle\\widehat{\\mathbf{M}}(n,\\tilde{u}\_{0},\\uplambda)={\\mathbf{S}}(\\mathbf{G})\\cdot\\mathbf{M}\\cdot\\mathbf{G}^{-1}=\\begin{pmatrix}\\frac{({\\uplambda}+\\upalpha(n-1))(\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}{\\uplambda}+{\\uplambda}+\\upalpha(n)-{\\mathrm{c}}\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0})}{({\\uplambda}+\\upalpha(n))(\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1)}&\\frac{({\\uplambda}-{\\mathrm{c}})\\tilde{u}^{1}\_{0}}{{\\uplambda}+\\upalpha(n)}\\\<br>({\\uplambda}+\\upalpha(n-1))\\tilde{u}^{2}\_{0}&\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1\\\<br>\\end{pmatrix}, |  |
| (97) |  | 𝐔^​(n,u~−1,u~0,λ)=𝐃t​(𝐆)⋅𝐆−1+𝐆⋅𝐔⋅𝐆−1=(2​u~01​u~−12−λ2​(c−λ)​u~01λ+α⁡(n−1)−2​(λ+α⁡(n−1))​u~−12λ−2​u~01​u~−12).\\displaystyle\\widehat{\\mathbf{U}}(n,\\tilde{u}\_{-1},\\tilde{u}\_{0},\\uplambda)=\\mathbf{D}\_{t}(\\mathbf{G})\\cdot\\mathbf{G}^{-1}+\\mathbf{G}\\cdot\\mathbf{U}\\cdot\\mathbf{G}^{-1}=\\left(\\!\\begin{smallmatrix}2\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{-1}-{\\uplambda}&\\frac{2({\\mathrm{c}}-{\\uplambda})\\tilde{u}^{1}\_{0}}{{\\uplambda}+\\upalpha(n-1)}\\\<br>-2({\\uplambda}+\\upalpha(n-1))\\tilde{u}^{2}\_{-1}&{\\uplambda}-2\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{-1}\\\<br>\\end{smallmatrix}\\!\\right). |  |

In agreement with Theorem [1](https://arxiv.org/html/2604.26870#Thmtheorem1 "Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"), we see that
the matrix ( [96](https://arxiv.org/html/2604.26870#S3.E96 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) depends only on n,u~0,λn,\\,\\tilde{u}\_{0},\\,\\uplambda,
in contrast to the matrix ( [90](https://arxiv.org/html/2604.26870#S3.E90 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) depending on n,u~0,u~1,λn,\\,\\tilde{u}\_{0},\\,\\tilde{u}\_{1},\\,\\uplambda.

Now, using Definition [6](https://arxiv.org/html/2604.26870#Thmdefinition6 "Definition 6. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") and Remark [4](https://arxiv.org/html/2604.26870#Thmremark4 "Remark 4. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") with u~\\tilde{u}
instead of uu, we see that the MLR ( [96](https://arxiv.org/html/2604.26870#S3.E96 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [97](https://arxiv.org/html/2604.26870#S3.E97 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is u~\\tilde{u}-tame,
and we can try to simplify it by applying a gauge transformation G=G⁡(n,λ)G=G(n,\\uplambda)
depending only on n,λn,\\,\\uplambda.
To avoid cumbersome formulas, we take a diagonal gauge transformation
G=(g11​(n,λ)00g22​(n,λ))G=\\left(\\begin{smallmatrix}g^{11}(n,\\uplambda)&0\\\
0&g^{22}(n,\\uplambda)\\end{smallmatrix}\\right), where g11​(n,λ)g^{11}(n,\\uplambda) and g22​(n,λ)g^{22}(n,\\uplambda) are nonzero scalar functions.
Then 𝐒⁡(G)=(g11​(n+1,λ)00g22​(n+1,λ)){\\mathbf{S}}(G)=\\left(\\begin{smallmatrix}g^{11}(n+1,\\uplambda)&0\\\
0&g^{22}(n+1,\\uplambda)\\end{smallmatrix}\\right) and 𝐃t​(G)=0\\mathbf{D}\_{t}(G)=0.
Applying GG to the MLR ( [96](https://arxiv.org/html/2604.26870#S3.E96 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [97](https://arxiv.org/html/2604.26870#S3.E97 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we get the corresponding gauge equivalent MLR

|     |     |     |     |
| --- | --- | --- | --- |
| (98) |  | 𝐌^^=𝐒⁡(G)⋅𝐌^​(n,u~0,λ)⋅G−1=(g11​(n+1,λ)​(λ+α⁡(n−1))​(u~01​u~02​λ+λ+α⁡(n)−c​u~01​u~02)(λ+α⁡(n))​(u~01​u~02+1)​g11​(n,λ)g11​(n+1,λ)​(λ−c)​u~01(λ+α⁡(n))​g22​(n,λ)g22​(n+1,λ)​(λ+α⁡(n−1))​u~02g11​(n,λ)g22​(n+1,λ)​u~01​u~02+1g22​(n,λ)),\\displaystyle\\widehat{\\widehat{\\mathbf{M}}}={\\mathbf{S}}(G)\\cdot\\widehat{\\mathbf{M}}(n,\\tilde{u}\_{0},\\uplambda)\\cdot G^{-1}=\\begin{pmatrix}\\frac{g^{11}(n+1,\\uplambda)({\\uplambda}+\\upalpha(n-1))(\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}{\\uplambda}+{\\uplambda}+\\upalpha(n)-{\\mathrm{c}}\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0})}{({\\uplambda}+\\upalpha(n))(\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1)g^{11}(n,\\uplambda)}&\\frac{g^{11}(n+1,\\uplambda)({\\uplambda}-{\\mathrm{c}})\\tilde{u}^{1}\_{0}}{({\\uplambda}+\\upalpha(n))g^{22}(n,\\uplambda)}\\\<br>\\frac{g^{22}(n+1,\\uplambda)({\\uplambda}+\\upalpha(n-1))\\tilde{u}^{2}\_{0}}{g^{11}(n,\\uplambda)}&\\frac{g^{22}(n+1,\\uplambda)\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1}{g^{22}(n,\\uplambda)}\\\<br>\\end{pmatrix}, |  |
| (99) |  | 𝐔^^=𝐃t​(G)⋅G−1+G⋅𝐔^​(n,u~−1,u~0,λ)⋅G−1=(2​u~01​u~−12−λ2​g11​(n,λ)​(c−λ)​u~01(λ+α⁡(n−1))​g22​(n,λ)−2​g22​(n,λ)​(λ+α⁡(n−1))​u~−12g11​(n,λ)λ−2​u~01​u~−12).\\displaystyle\\widehat{\\widehat{\\mathbf{U}}}=\\mathbf{D}\_{t}(G)\\cdot G^{-1}+G\\cdot\\widehat{\\mathbf{U}}(n,\\tilde{u}\_{-1},\\tilde{u}\_{0},\\uplambda)\\cdot G^{-1}=\\left(\\!\\begin{smallmatrix}2\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{-1}-{\\uplambda}&\\frac{2g^{11}(n,\\uplambda)({\\mathrm{c}}-{\\uplambda})\\tilde{u}^{1}\_{0}}{({\\uplambda}+\\upalpha(n-1))g^{22}(n,\\uplambda)}\\\<br>\\frac{-2g^{22}(n,\\uplambda)({\\uplambda}+\\upalpha(n-1))\\tilde{u}^{2}\_{-1}}{g^{11}(n,\\uplambda)}&{\\uplambda}-2\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{-1}\\\<br>\\end{smallmatrix}\\!\\right). |  |

We want to choose G=(g11​(n,λ)00g22​(n,λ))G=\\left(\\begin{smallmatrix}g^{11}(n,\\uplambda)&0\\\
0&g^{22}(n,\\uplambda)\\end{smallmatrix}\\right) such that the matrices ( [98](https://arxiv.org/html/2604.26870#S3.E98 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [99](https://arxiv.org/html/2604.26870#S3.E99 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) become simpler than
the matrices ( [96](https://arxiv.org/html/2604.26870#S3.E96 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [97](https://arxiv.org/html/2604.26870#S3.E97 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
The formulas in the right-hand sides of ( [98](https://arxiv.org/html/2604.26870#S3.E98 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [99](https://arxiv.org/html/2604.26870#S3.E99 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) suggest
to take g11​(n,λ)=λ+α⁡(n−1)g^{11}(n,\\uplambda)={\\uplambda}+\\upalpha(n-1), g22​(n,λ)=1\\,g^{22}(n,\\uplambda)=1.
Then ( [98](https://arxiv.org/html/2604.26870#S3.E98 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [99](https://arxiv.org/html/2604.26870#S3.E99 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) become

|     |     |     |     |
| --- | --- | --- | --- |
| (100) |  | 𝐌^^=(u~01​u~02​λ+λ+α⁡(n)−c​u~01​u~02u~01​u~02+1(λ−c)​u~01u~02u~01​u~02+1),𝐔^^=(2​u~01​u~−12−λ2​(c−λ)​u~01−2​u~−12λ−2​u~01​u~−12).\\displaystyle\\widehat{\\widehat{\\mathbf{M}}}=\\begin{pmatrix}\\frac{\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}{\\uplambda}+{\\uplambda}+\\upalpha(n)-{\\mathrm{c}}\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}}{\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1}&({\\uplambda}-{\\mathrm{c}})\\tilde{u}^{1}\_{0}\\\<br>\\tilde{u}^{2}\_{0}&\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1\\\<br>\\end{pmatrix},\\qquad\\quad\\widehat{\\widehat{\\mathbf{U}}}=\\begin{pmatrix}2\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{-1}-{\\uplambda}&2({\\mathrm{c}}-{\\uplambda})\\tilde{u}^{1}\_{0}\\\<br>-2\\tilde{u}^{2}\_{-1}&{\\uplambda}-2\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{-1}\\\<br>\\end{pmatrix}. |  |

Fix a constant q∈ℂ\\mathrm{q}\\in\\mathbb{C}.
Below we use the matrices ( [100](https://arxiv.org/html/2604.26870#S3.E100 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) with λ\\uplambda replaced by q\\mathrm{q}.
According to Definition [1](https://arxiv.org/html/2604.26870#Thmdefinition1 "Definition 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"), since the matrices ( [100](https://arxiv.org/html/2604.26870#S3.E100 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
form a MLR for equation ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), one can consider the auxiliary system

|     |     |     |     |
| --- | --- | --- | --- |
| (101) |  | 𝐒⁡(Ψ~)=(u~01​u~02​q+q+α⁡(n)−c​u~01​u~02u~01​u~02+1(q−c)​u~01u~02u~01​u~02+1)⋅Ψ~,∂t(Ψ~)=(2​u~01​u~−12−q2​(c−q)​u~01−2​u~−12q−2​u~01​u~−12)⋅Ψ~,\\displaystyle{\\mathbf{S}}(\\tilde{\\Psi})=\\begin{pmatrix}\\frac{\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}{\\mathrm{q}}+{\\mathrm{q}}+\\upalpha(n)-{\\mathrm{c}}\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}}{\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1}&({\\mathrm{q}}-{\\mathrm{c}})\\tilde{u}^{1}\_{0}\\\<br>\\tilde{u}^{2}\_{0}&\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1\\\<br>\\end{pmatrix}\\cdot\\tilde{\\Psi},\\qquad\\qquad\\partial\_{t}(\\tilde{\\Psi})=\\begin{pmatrix}2\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{-1}-{\\mathrm{q}}&2({\\mathrm{c}}-{\\mathrm{q}})\\tilde{u}^{1}\_{0}\\\<br>-2\\tilde{u}^{2}\_{-1}&{\\mathrm{q}}-2\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{-1}\\\<br>\\end{pmatrix}\\cdot\\tilde{\\Psi}, |  |

which is compatible modulo equation ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Here Ψ~=Ψ~​(n,t)\\tilde{\\Psi}=\\tilde{\\Psi}(n,t) is an invertible 2×22\\times 2 matrix
with elements ψ~i​j=ψ~i​j​(n,t)\\tilde{\\uppsi}^{ij}=\\tilde{\\uppsi}^{ij}(n,t), i,j=1,2\\,i,j=1,2.

Substituting Ψ~=(ψ~11ψ~12ψ~21ψ~22)\\tilde{\\Psi}=\\begin{pmatrix}\\tilde{\\uppsi}^{11}&\\tilde{\\uppsi}^{12}\\\
\\tilde{\\uppsi}^{21}&\\tilde{\\uppsi}^{22}\\end{pmatrix} in ( [101](https://arxiv.org/html/2604.26870#S3.E101 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and considering the first columns
in the matrix equations ( [101](https://arxiv.org/html/2604.26870#S3.E101 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we obtain

|     |     |     |     |
| --- | --- | --- | --- |
| (102) |  | 𝐒⁡(ψ~11)=(u~01​u~02​q+q+α⁡(n)−c​u~01​u~02)u~01​u~02+1​ψ~11+(q−c)​u~01​ψ~21,𝐒⁡(ψ~21)=u~02​ψ~11+(u~01​u~02+1)​ψ~21,\\displaystyle{\\mathbf{S}}(\\tilde{\\uppsi}^{11})=\\frac{(\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}{\\mathrm{q}}+{\\mathrm{q}}+\\upalpha(n)-{\\mathrm{c}}\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0})}{\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1}\\tilde{\\uppsi}^{11}+({\\mathrm{q}}-{\\mathrm{c}})\\tilde{u}^{1}\_{0}\\tilde{\\uppsi}^{21},\\qquad\\quad{\\mathbf{S}}(\\tilde{\\uppsi}^{21})=\\tilde{u}^{2}\_{0}\\tilde{\\uppsi}^{11}+(\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1)\\tilde{\\uppsi}^{21}, |  |
| (103) |  | ∂t(ψ~11)=(2​u~01​u~−12−q)​ψ~11+2​(c−q)​u~01​ψ~21,∂t(ψ~21)=−2​u~−12​ψ~11+(q−2​u~01​u~−12)​ψ~21.\\displaystyle\\partial\_{t}(\\tilde{\\uppsi}^{11})=(2\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{-1}-{\\mathrm{q}})\\tilde{\\uppsi}^{11}+2({\\mathrm{c}}-{\\mathrm{q}})\\tilde{u}^{1}\_{0}\\tilde{\\uppsi}^{21},\\qquad\\quad\\partial\_{t}(\\tilde{\\uppsi}^{21})=-2\\tilde{u}^{2}\_{-1}\\tilde{\\uppsi}^{11}+({\\mathrm{q}}-2\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{-1})\\tilde{\\uppsi}^{21}. |  |

We set w~=ψ~11/ψ~21\\tilde{w}={\\tilde{\\uppsi}^{11}}/{\\tilde{\\uppsi}^{21}}.
Similarly to the computations ( [76](https://arxiv.org/html/2604.26870#S3.E76 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [77](https://arxiv.org/html/2604.26870#S3.E77 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) based on ( [74](https://arxiv.org/html/2604.26870#S3.E74 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [75](https://arxiv.org/html/2604.26870#S3.E75 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
now we compute 𝐒⁡(w~)=𝐒⁡(ψ~11/ψ~21){\\mathbf{S}}(\\tilde{w})={\\mathbf{S}}\\big({\\tilde{\\uppsi}^{11}}/{\\tilde{\\uppsi}^{21}}\\big) and
∂t(w~)=∂t(ψ~11/ψ~21)\\partial\_{t}(\\tilde{w})=\\partial\_{t}\\big({\\tilde{\\uppsi}^{11}}/{\\tilde{\\uppsi}^{21}}\\big),
using ( [102](https://arxiv.org/html/2604.26870#S3.E102 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [103](https://arxiv.org/html/2604.26870#S3.E103 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), and get

|     |     |     |     |
| --- | --- | --- | --- |
| (104) |  | 𝐒⁡(w~)=(u~01​u~02​q+q+α⁡(n)−c​u~01​u~02)​w~+(q−c)​u~01​(u~01​u~02+1)(u~01​u~02+1)​(u~02​w~+u~01​u~02+1),\\displaystyle{\\mathbf{S}}(\\tilde{w})=\\frac{(\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}{\\mathrm{q}}+{\\mathrm{q}}+\\upalpha(n)-{\\mathrm{c}}\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0})\\tilde{w}+({\\mathrm{q}}-{\\mathrm{c}})\\tilde{u}^{1}\_{0}(\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1)}{(\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1)(\\tilde{u}^{2}\_{0}\\tilde{w}+\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}+1)}, |  |
| (105) |  | ∂t(w~)=2​u~−12​(w~)2+(4​u~01​u~−12−2​q)​w~+2​(c−q)​u~01.\\displaystyle\\partial\_{t}(\\tilde{w})=2\\tilde{u}^{2}\_{-1}(\\tilde{w})^{2}+(4\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{-1}-2{\\mathrm{q}})\\tilde{w}+2({\\mathrm{c}}-{\\mathrm{q}})\\tilde{u}^{1}\_{0}. |  |

The described way of deriving equations ( [104](https://arxiv.org/html/2604.26870#S3.E104 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [105](https://arxiv.org/html/2604.26870#S3.E105 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
from system ( [101](https://arxiv.org/html/2604.26870#S3.E101 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), which is compatible modulo equation ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
implies that system ( [104](https://arxiv.org/html/2604.26870#S3.E104 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [105](https://arxiv.org/html/2604.26870#S3.E105 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is compatible modulo ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) as well.

Now we set

|     |     |     |     |
| --- | --- | --- | --- |
| (106) |  | u~~1:=w~,u~~2:=u~2.\\displaystyle\\tilde{\\tilde{u}}^{1}:=\\tilde{w},\\qquad\\qquad\\tilde{\\tilde{u}}^{2}:=\\tilde{u}^{2}. |  |

One has 𝐒⁡(w~)=𝐒⁡(u~~1)=u~~11{\\mathbf{S}}(\\tilde{w})={\\mathbf{S}}(\\tilde{\\tilde{u}}^{1})=\\tilde{\\tilde{u}}^{1}\_{1}, u~0i=u~i\\,\\tilde{u}^{i}\_{0}=\\tilde{u}^{i}, u~~0i=u~i\\,\\tilde{\\tilde{u}}^{i}\_{0}=\\tilde{u}^{i}, i=1,2\\,i=1,2.
Substituting 𝐒⁡(w~)=u~~11{\\mathbf{S}}(\\tilde{w})=\\tilde{\\tilde{u}}^{1}\_{1}, w~=u~~01\\,\\tilde{w}=\\tilde{\\tilde{u}}^{1}\_{0}, u~01=u~1\\,\\tilde{u}^{1}\_{0}=\\tilde{u}^{1}, u~02=u~~02\\,\\tilde{u}^{2}\_{0}=\\tilde{\\tilde{u}}^{2}\_{0}
in ( [104](https://arxiv.org/html/2604.26870#S3.E104 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (107) |  | u~~11=(u~1​u~~02​q+q+α⁡(n)−c​u~1​u~~02)​u~~01+(q−c)​u~1​(u~1​u~~02+1)(u~1​u~~02+1)​(u~~02​u~~01+u~1​u~~02+1).\\displaystyle\\tilde{\\tilde{u}}^{1}\_{1}=\\frac{(\\tilde{u}^{1}\\tilde{\\tilde{u}}^{2}\_{0}{\\mathrm{q}}+{\\mathrm{q}}+\\upalpha(n)-{\\mathrm{c}}\\tilde{u}^{1}\\tilde{\\tilde{u}}^{2}\_{0})\\tilde{\\tilde{u}}^{1}\_{0}+({\\mathrm{q}}-{\\mathrm{c}})\\tilde{u}^{1}(\\tilde{u}^{1}\\tilde{\\tilde{u}}^{2}\_{0}+1)}{(\\tilde{u}^{1}\\tilde{\\tilde{u}}^{2}\_{0}+1)(\\tilde{\\tilde{u}}^{2}\_{0}\\tilde{\\tilde{u}}^{1}\_{0}+\\tilde{u}^{1}\\tilde{\\tilde{u}}^{2}\_{0}+1)}. |  |

Equation ( [107](https://arxiv.org/html/2604.26870#S3.E107 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) can be resolved with respect to u~1\\tilde{u}^{1} as follows

|     |     |     |     |
| --- | --- | --- | --- |
| (108) |  | u~1=𝕏+(𝕏)2+2​(q​u~~01+α⁡(n)​u~~01−u~~11​u~~02​u~~01−u~~11)​𝕐𝕐,\\displaystyle\\tilde{u}^{1}=\\frac{\\mathbb{X}+\\sqrt{(\\mathbb{X})^{2}+2\\big({\\mathrm{q}}\\tilde{\\tilde{u}}^{1}\_{0}+\\upalpha(n)\\tilde{\\tilde{u}}^{1}\_{0}-\\tilde{\\tilde{u}}^{1}\_{1}\\tilde{\\tilde{u}}^{2}\_{0}\\tilde{\\tilde{u}}^{1}\_{0}-\\tilde{\\tilde{u}}^{1}\_{1}\\big)\\mathbb{Y}}}{\\mathbb{Y}}, |  |

where 𝕏\\mathbb{X}, 𝕐\\mathbb{Y} are given by

|     |     |     |     |
| --- | --- | --- | --- |
| (109) |  | 𝕏:=u~~02​(u~~01​(q−u~~11​u~~02−c)−2​u~~11)−c+q,𝕐:=2​u~~02​(u~~11​u~~02+c−q).\\displaystyle\\mathbb{X}:=\\tilde{\\tilde{u}}^{2}\_{0}(\\tilde{\\tilde{u}}^{1}\_{0}({\\mathrm{q}}-\\tilde{\\tilde{u}}^{1}\_{1}\\tilde{\\tilde{u}}^{2}\_{0}-{\\mathrm{c}})-2\\tilde{\\tilde{u}}^{1}\_{1})-{\\mathrm{c}}+{\\mathrm{q}},\\qquad\\quad\\mathbb{Y}:=2\\tilde{\\tilde{u}}^{2}\_{0}(\\tilde{\\tilde{u}}^{1}\_{1}\\tilde{\\tilde{u}}^{2}\_{0}+{\\mathrm{c}}-{\\mathrm{q}}). |  |

Now consider equation ( [108](https://arxiv.org/html/2604.26870#S3.E108 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) along with u~2=u~~02\\tilde{u}^{2}=\\tilde{\\tilde{u}}^{2}\_{0}, which gives

|     |     |     |     |
| --- | --- | --- | --- |
| (110) |  | {u~1=𝕏+(𝕏)2+2​(q​u~~01+α⁡(n)​u~~01−u~~11​u~~02​u~~01−u~~11)​𝕐𝕐,u~2=u~~02.\\displaystyle\\left\\{\\begin{aligned} \\tilde{u}^{1}&=\\frac{\\mathbb{X}+\\sqrt{(\\mathbb{X})^{2}+2\\big({\\mathrm{q}}\\tilde{\\tilde{u}}^{1}\_{0}+\\upalpha(n)\\tilde{\\tilde{u}}^{1}\_{0}-\\tilde{\\tilde{u}}^{1}\_{1}\\tilde{\\tilde{u}}^{2}\_{0}\\tilde{\\tilde{u}}^{1}\_{0}-\\tilde{\\tilde{u}}^{1}\_{1}\\big)\\mathbb{Y}}}{\\mathbb{Y}},\\\<br>\\tilde{u}^{2}&=\\tilde{\\tilde{u}}^{2}\_{0}.\\end{aligned}\\right. |  |

For each ℓ∈ℤ\\ell\\in\\mathbb{Z}, applying the operator 𝐒ℓ{\\mathbf{S}}^{\\ell} to ( [110](https://arxiv.org/html/2604.26870#S3.E110 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (111) |  | {u~ℓ1=𝐒ℓ​(𝕏)+(𝐒ℓ​(𝕏))2+2​(q​u~~ℓ1+α⁡(n+ℓ)​u~~ℓ1−u~~ℓ+11​u~~ℓ2​u~~ℓ1−u~~ℓ+11)​𝐒ℓ​(𝕐)𝐒ℓ​(𝕐),u~ℓ2=u~~2ℓ,ℓ∈ℤ.\\displaystyle\\left\\{\\begin{aligned} \\tilde{u}^{1}\_{\\ell}&=\\frac{{\\mathbf{S}}^{\\ell}(\\mathbb{X})+\\sqrt{({\\mathbf{S}}^{\\ell}(\\mathbb{X}))^{2}+2\\big({\\mathrm{q}}\\tilde{\\tilde{u}}^{1}\_{\\ell}+\\upalpha(n+\\ell)\\tilde{\\tilde{u}}^{1}\_{\\ell}-\\tilde{\\tilde{u}}^{1}\_{\\ell+1}\\tilde{\\tilde{u}}^{2}\_{\\ell}\\tilde{\\tilde{u}}^{1}\_{\\ell}-\\tilde{\\tilde{u}}^{1}\_{\\ell+1}\\big){\\mathbf{S}}^{\\ell}(\\mathbb{Y})}}{{\\mathbf{S}}^{\\ell}(\\mathbb{Y})},\\\<br>\\tilde{u}^{2}\_{\\ell}&=\\tilde{\\tilde{u}}^{2}\_{\\ell},\\qquad\\qquad\\qquad\\qquad\\ell\\in\\mathbb{Z}.\\end{aligned}\\right. |  |

Substituting w~=u~~1\\tilde{w}=\\tilde{\\tilde{u}}^{1} and ( [111](https://arxiv.org/html/2604.26870#S3.E111 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) in ( [105](https://arxiv.org/html/2604.26870#S3.E105 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we derive

|     |     |     |     |
| --- | --- | --- | --- |
| (112) |  | ∂t(u~~1)=2​u~~−12​(u~~01)2−2​q​u~~01+(4​u~~−12​u~~01+2​(c−q))​(𝕏+(𝕏)2+2​(q​u~~01+α⁡(n)​u~~01−u~~11​u~~02​u~~01−u~~11)​𝕐)𝕐.\\displaystyle\\partial\_{t}(\\tilde{\\tilde{u}}^{1})=2\\tilde{\\tilde{u}}^{2}\_{-1}(\\tilde{\\tilde{u}}^{1}\_{0})^{2}-2{\\mathrm{q}}\\tilde{\\tilde{u}}^{1}\_{0}+\\frac{\\big(4\\tilde{\\tilde{u}}^{2}\_{-1}\\tilde{\\tilde{u}}^{1}\_{0}+2({\\mathrm{c}}-{\\mathrm{q}})\\big)\\left(\\mathbb{X}\\!+\\!\\sqrt{(\\mathbb{X})^{2}\\!+\\!2\\big({\\mathrm{q}}\\tilde{\\tilde{u}}^{1}\_{0}\\!+\\!\\upalpha(n)\\tilde{\\tilde{u}}^{1}\_{0}\\!-\\!\\tilde{\\tilde{u}}^{1}\_{1}\\tilde{\\tilde{u}}^{2}\_{0}\\tilde{\\tilde{u}}^{1}\_{0}\\!-\\!\\tilde{\\tilde{u}}^{1}\_{1}\\big)\\mathbb{Y}}\\right)}{\\mathbb{Y}}. |  |

Now we consider ( [112](https://arxiv.org/html/2604.26870#S3.E112 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) along with the equation obtained
by means of substituting ( [111](https://arxiv.org/html/2604.26870#S3.E111 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) in the second component of ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
This gives the 22-component non-autonomous equation

|     |     |     |     |
| --- | --- | --- | --- |
| (113) |  | {∂t(u~~1)=2​u~~−12​(u~~01)2−2​q​u~~01+(4​u~~−12​u~~01+2​(c−q))​(𝕏+(𝕏)2+2​(q​u~~01+α⁡(n)​u~~01−u~~11​u~~02​u~~01−u~~11)​𝕐)𝕐,∂t(u~~2)=ℍ⁡(n,u~~01,u~~11,u~~21,u~~−12,u~~02,u~~12,c,q),\\displaystyle\\left\\{\\begin{aligned} \\partial\_{t}(\\tilde{\\tilde{u}}^{1})&=2\\tilde{\\tilde{u}}^{2}\_{-1}(\\tilde{\\tilde{u}}^{1}\_{0})^{2}-2{\\mathrm{q}}\\tilde{\\tilde{u}}^{1}\_{0}+\\frac{\\big(4\\tilde{\\tilde{u}}^{2}\_{-1}\\tilde{\\tilde{u}}^{1}\_{0}+2({\\mathrm{c}}-{\\mathrm{q}})\\big)\\left(\\mathbb{X}\\!+\\!\\sqrt{(\\mathbb{X})^{2}\\!+\\!2\\big({\\mathrm{q}}\\tilde{\\tilde{u}}^{1}\_{0}\\!+\\!\\upalpha(n)\\tilde{\\tilde{u}}^{1}\_{0}\\!-\\!\\tilde{\\tilde{u}}^{1}\_{1}\\tilde{\\tilde{u}}^{2}\_{0}\\tilde{\\tilde{u}}^{1}\_{0}\\!-\\!\\tilde{\\tilde{u}}^{1}\_{1}\\big)\\mathbb{Y}}\\right)}{\\mathbb{Y}},\\\<br>\\partial\_{t}(\\tilde{\\tilde{u}}^{2})&=\\mathbb{H}\\big(n,\\tilde{\\tilde{u}}^{1}\_{0},\\tilde{\\tilde{u}}^{1}\_{1},\\tilde{\\tilde{u}}^{1}\_{2},\\tilde{\\tilde{u}}^{2}\_{-1},\\tilde{\\tilde{u}}^{2}\_{0},\\tilde{\\tilde{u}}^{2}\_{1},\\mathrm{c},\\mathrm{q}\\big),\\end{aligned}\\right. |  |

where the function
ℍ=ℍ⁡(n,u~~01,u~~11,u~~21,u~~−12,u~~02,u~~12,c,q)\\mathbb{H}=\\mathbb{H}\\big(n,\\tilde{\\tilde{u}}^{1}\_{0},\\tilde{\\tilde{u}}^{1}\_{1},\\tilde{\\tilde{u}}^{1}\_{2},\\tilde{\\tilde{u}}^{2}\_{-1},\\tilde{\\tilde{u}}^{2}\_{0},\\tilde{\\tilde{u}}^{2}\_{1},\\mathrm{c},\\mathrm{q}\\big)
is obtained by substituting ( [111](https://arxiv.org/html/2604.26870#S3.E111 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) in the right-hand side of the second component of ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
(We do not present the explicit formula for ℍ\\mathbb{H}, since it is rather cumbersome.)

As discussed above,
system ( [104](https://arxiv.org/html/2604.26870#S3.E104 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [105](https://arxiv.org/html/2604.26870#S3.E105 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Since equations ( [110](https://arxiv.org/html/2604.26870#S3.E110 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
are derived from ( [104](https://arxiv.org/html/2604.26870#S3.E104 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [105](https://arxiv.org/html/2604.26870#S3.E105 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) (by means of introducing ( [106](https://arxiv.org/html/2604.26870#S3.E106 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))),
system ( [110](https://arxiv.org/html/2604.26870#S3.E110 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) as well.
This implies that ( [110](https://arxiv.org/html/2604.26870#S3.E110 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is a MT from ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
(This fact can also be verified by a direct calculation.)

###### Remark 6.

Recall that ( [100](https://arxiv.org/html/2604.26870#S3.E100 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is a MLR for equation ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
and formulas ( [111](https://arxiv.org/html/2604.26870#S3.E111 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) are derived by applying the operator 𝐒ℓ{\\mathbf{S}}^{\\ell} to ( [110](https://arxiv.org/html/2604.26870#S3.E110 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Using Lemma [4](https://arxiv.org/html/2604.26870#Thmlemma4 "Lemma 4. ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") for the MLR ( [100](https://arxiv.org/html/2604.26870#S3.E100 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and
the MT ( [110](https://arxiv.org/html/2604.26870#S3.E110 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) from ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [85](https://arxiv.org/html/2604.26870#S3.E85 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
we can substitute ( [111](https://arxiv.org/html/2604.26870#S3.E111 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) in ( [100](https://arxiv.org/html/2604.26870#S3.E100 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), and this gives a MLR for equation ( [113](https://arxiv.org/html/2604.26870#S3.E113 "In 3.1. Non-autonomous examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

### 3.2. Other examples

The following 22-component equation
was derived in \[ [16](https://arxiv.org/html/2604.26870#bib.bib16 ""), Section 5.1.1\]
in a study of invariant time evolutions of polygons in the centro-affine plane

|     |     |     |     |
| --- | --- | --- | --- |
| (114) |  | {∂t(u1)=u01​u02,∂t(u2)=u−11u01−u01u11.\\displaystyle\\left\\{\\begin{aligned} \\partial\_{t}(u^{1})&=u^{1}\_{0}u^{2}\_{0},\\\<br>\\partial\_{t}(u^{2})&=\\frac{u^{1}\_{-1}}{u^{1}\_{0}}-\\frac{u^{1}\_{0}}{u^{1}\_{1}}.\\end{aligned}\\right. |  |

It is shown in \[ [16](https://arxiv.org/html/2604.26870#bib.bib16 ""), Section 5.1.1\] that one has the MT

|     |     |     |     |
| --- | --- | --- | --- |
| (115) |  | {w1=u01/u11,w2=u02\\displaystyle\\left\\{\\begin{aligned} w^{1}&=u^{1}\_{0}/u^{1}\_{1},\\\<br>w^{2}&=u^{2}\_{0}\\end{aligned}\\right. |  |

from ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to the equation

|     |     |     |     |
| --- | --- | --- | --- |
| (116) |  | {∂t(w1)=w01​(w02−w12),∂t(w2)=w−11−w01,\\displaystyle\\left\\{\\begin{aligned} \\partial\_{t}(w^{1})&=w^{1}\_{0}(w^{2}\_{0}-w^{2}\_{1}),\\\<br>\\partial\_{t}(w^{2})&=w^{1}\_{-1}-w^{1}\_{0},\\end{aligned}\\right. |  |

which is the Toda lattice in the Flaschka–Manakov coordinates \[ [3](https://arxiv.org/html/2604.26870#bib.bib3 ""), [15](https://arxiv.org/html/2604.26870#bib.bib15 "")\].

It is known (see, e.g., \[ [10](https://arxiv.org/html/2604.26870#bib.bib10 "")\]) that the following matrices form a MLR for ( [116](https://arxiv.org/html/2604.26870#S3.E116 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))

|     |     |     |     |
| --- | --- | --- | --- |
| (117) |  | 𝐌˘=(λ−w12w01−10),𝐔˘=(0−w011λ−w02).\\displaystyle\\breve{\\mathbf{M}}=\\begin{pmatrix}{\\uplambda}-w^{2}\_{1}&w^{1}\_{0}\\\<br>-1&0\\\<br>\\end{pmatrix},\\qquad\\quad\\breve{\\mathbf{U}}=\\begin{pmatrix}0&-w^{1}\_{0}\\\<br>1&{\\uplambda}-w^{2}\_{0}\\\<br>\\end{pmatrix}. |  |

Applying Lemma [4](https://arxiv.org/html/2604.26870#Thmlemma4 "Lemma 4. ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") to the MLR ( [117](https://arxiv.org/html/2604.26870#S3.E117 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and
to the MT ( [115](https://arxiv.org/html/2604.26870#S3.E115 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) from ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [116](https://arxiv.org/html/2604.26870#S3.E116 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
we substitute ( [115](https://arxiv.org/html/2604.26870#S3.E115 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) in ( [117](https://arxiv.org/html/2604.26870#S3.E117 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and obtain the following MLR for equation ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))

|     |     |     |     |
| --- | --- | --- | --- |
| (118) |  | 𝐌=(λ−u12u01/u11−10),\\displaystyle\\mathbf{M}=\\begin{pmatrix}{\\uplambda}-u^{2}\_{1}&u^{1}\_{0}/u^{1}\_{1}\\\<br>-1&0\\\<br>\\end{pmatrix}, |  |
| (119) |  | 𝐔=(0−u10/u111λ−u02).\\displaystyle\\mathbf{U}=\\begin{pmatrix}0&-u^{1}\_{0}/u^{1}\_{1}\\\<br>1&{\\uplambda}-u^{2}\_{0}\\\<br>\\end{pmatrix}. |  |

In order to simplify the MLR ( [118](https://arxiv.org/html/2604.26870#S3.E118 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [119](https://arxiv.org/html/2604.26870#S3.E119 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) by means of gauge transformations,
we consider Theorem [1](https://arxiv.org/html/2604.26870#Thmtheorem1 "Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") in the case N=2N=2, d=2\\,\\mathrm{d}=2, p=1\\,p=1.
The matrix ( [118](https://arxiv.org/html/2604.26870#S3.E118 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) obeys condition ( [27](https://arxiv.org/html/2604.26870#S2.E27 "In 2nd item ‣ Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) with p=1p=1.
Therefore, one can apply Theorem [1](https://arxiv.org/html/2604.26870#Thmtheorem1 "Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") to the MLR ( [118](https://arxiv.org/html/2604.26870#S3.E118 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [119](https://arxiv.org/html/2604.26870#S3.E119 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
To this end, we need to do the following.

- •


Choose a constant vector a0=(a01,a02)∈ℂ2a\_{0}=(a^{1}\_{0},a^{2}\_{0})\\in\\mathbb{C}^{2}.

- •


Substitute u0=a0u\_{0}=a\_{0} in 𝐌\\mathbf{M}
given by ( [118](https://arxiv.org/html/2604.26870#S3.E118 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) (i.e., substitute u0i=a0iu^{i}\_{0}=a^{i}\_{0} for i=1,2i=1,2 in ( [118](https://arxiv.org/html/2604.26870#S3.E118 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")))
and compute the corresponding gauge transformation ( [28](https://arxiv.org/html/2604.26870#S2.E28 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
which gives 𝐆=(0−1u01/a01u01​(λ−u02)/a01)\\mathbf{G}=\\begin{pmatrix}0&-1\\\
u^{1}\_{0}/a^{1}\_{0}&u^{1}\_{0}({\\uplambda}-u^{2}\_{0})/a^{1}\_{0}\\end{pmatrix}.
Here it is convenient to take a01=1a^{1}\_{0}=1, and then 𝐆\\mathbf{G} takes the form
𝐆=(0−1u01u01​(λ−u02))\\mathbf{G}=\\begin{pmatrix}0&-1\\\
u^{1}\_{0}&u^{1}\_{0}({\\uplambda}-u^{2}\_{0})\\end{pmatrix}.

- •


Now we apply the obtained gauge transformation 𝐆\\mathbf{G}
to the MLR ( [118](https://arxiv.org/html/2604.26870#S3.E118 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [119](https://arxiv.org/html/2604.26870#S3.E119 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and compute
the gauge equivalent MLR (𝐌^,𝐔^)\\big(\\widehat{\\mathbf{M}},\\,\\widehat{\\mathbf{U}}\\big) given by ( [30](https://arxiv.org/html/2604.26870#S2.E30 "In Theorem 1. ‣ 2. General results on differential-difference matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), which gives



|     |     |     |     |
| --- | --- | --- | --- |
| (120) |  | 𝐌^=𝐒⁡(𝐆)⋅𝐌⋅𝐆−1=(λ−u021/u01−u010),𝐔^=𝐃t​(𝐆)⋅𝐆−1+𝐆⋅𝐔⋅𝐆−1=(0−1/u10u−11λ).\\displaystyle\\widehat{\\mathbf{M}}={\\mathbf{S}}(\\mathbf{G})\\cdot\\mathbf{M}\\cdot\\mathbf{G}^{-1}=\\begin{pmatrix}{\\uplambda}-u^{2}\_{0}&1/u^{1}\_{0}\\\<br>-u^{1}\_{0}&0\\\<br>\\end{pmatrix},\\qquad\\widehat{\\mathbf{U}}=\\mathbf{D}\_{t}(\\mathbf{G})\\cdot\\mathbf{G}^{-1}+\\mathbf{G}\\cdot\\mathbf{U}\\cdot\\mathbf{G}^{-1}=\\begin{pmatrix}0&-1/u^{1}\_{0}\\\<br>u^{1}\_{-1}&{\\uplambda}\\\<br>\\end{pmatrix}. |  |


Fix a constant c∈ℂ\\mathrm{c}\\in\\mathbb{C}.
Below we use the matrices ( [120](https://arxiv.org/html/2604.26870#S3.E120 "In 3rd item ‣ 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) with λ\\uplambda replaced by c\\mathrm{c}.
According to Definition [1](https://arxiv.org/html/2604.26870#Thmdefinition1 "Definition 1. ‣ 1. Introduction ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"), since ( [120](https://arxiv.org/html/2604.26870#S3.E120 "In 3rd item ‣ 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
is a MLR for equation ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we can consider the auxiliary system

|     |     |     |     |
| --- | --- | --- | --- |
| (121) |  | 𝐒⁡(Ψ)=(c−u021/u01−u010)⋅Ψ,∂t(Ψ)=(0−1/u10u−11c)⋅Ψ,\\displaystyle{\\mathbf{S}}(\\Psi)=\\begin{pmatrix}{\\mathrm{c}}-u^{2}\_{0}&1/u^{1}\_{0}\\\<br>-u^{1}\_{0}&0\\\<br>\\end{pmatrix}\\cdot\\Psi,\\qquad\\quad\\partial\_{t}(\\Psi)=\\begin{pmatrix}0&-1/u^{1}\_{0}\\\<br>u^{1}\_{-1}&{\\mathrm{c}}\\\<br>\\end{pmatrix}\\cdot\\Psi, |  |

which is compatible modulo equation ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Here Ψ=Ψ⁡(n,t)\\Psi=\\Psi(n,t) is an invertible 2×22\\times 2 matrix
with elements ψi​j=ψi​j​(n,t)\\uppsi^{ij}=\\uppsi^{ij}(n,t), i,j=1,2\\,i,j=1,2.

Substituting Ψ=(ψ11ψ12ψ21ψ22)\\Psi=\\begin{pmatrix}\\uppsi^{11}&\\uppsi^{12}\\\
\\uppsi^{21}&\\uppsi^{22}\\end{pmatrix} in ( [121](https://arxiv.org/html/2604.26870#S3.E121 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and considering the first columns
in the matrix equations ( [121](https://arxiv.org/html/2604.26870#S3.E121 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), one gets

|     |     |     |     |
| --- | --- | --- | --- |
| (122) |  | 𝐒⁡(ψ11)=(c−u02)​ψ11+1u01​ψ21,𝐒⁡(ψ21)=−u01​ψ11,\\displaystyle{\\mathbf{S}}(\\uppsi^{11})=({\\mathrm{c}}-u^{2}\_{0})\\uppsi^{11}+\\frac{1}{u^{1}\_{0}}\\uppsi^{21},\\qquad\\quad{\\mathbf{S}}(\\uppsi^{21})=-u^{1}\_{0}\\uppsi^{11}, |  |
| (123) |  | ∂t(ψ11)=−1u01​ψ21,∂t(ψ21)=u−11​ψ11+c​ψ21.\\displaystyle\\partial\_{t}(\\uppsi^{11})=-\\frac{1}{u^{1}\_{0}}\\uppsi^{21},\\qquad\\quad\\partial\_{t}(\\uppsi^{21})=u^{1}\_{-1}\\uppsi^{11}+{\\mathrm{c}}\\uppsi^{21}. |  |

Since the matrix system ( [121](https://arxiv.org/html/2604.26870#S3.E121 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
the corresponding system ( [122](https://arxiv.org/html/2604.26870#S3.E122 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [123](https://arxiv.org/html/2604.26870#S3.E123 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
obtained from the first columns in ( [121](https://arxiv.org/html/2604.26870#S3.E121 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is compatible modulo ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) as well.
We set

|     |     |     |     |
| --- | --- | --- | --- |
| (124) |  | u~1:=ψ11,u~2:=ψ21.\\displaystyle\\tilde{u}^{1}:=\\uppsi^{11},\\qquad\\qquad\\tilde{u}^{2}:=\\uppsi^{21}. |  |

For i=1,2i=1,2 one has 𝐒⁡(ψi​1)=𝐒⁡(u~i)=u~1i{\\mathbf{S}}(\\uppsi^{i1})={\\mathbf{S}}(\\tilde{u}^{i})=\\tilde{u}^{i}\_{1},
u0i=ui\\,u^{i}\_{0}=u^{i}, u~0i=u~i\\,\\tilde{u}^{i}\_{0}=\\tilde{u}^{i}.
Substituting 𝐒⁡(ψi​1)=u~1i{\\mathbf{S}}(\\uppsi^{i1})=\\tilde{u}^{i}\_{1}, ψi​1=u~0i\\,\\uppsi^{i1}=\\tilde{u}^{i}\_{0}, u0i=ui\\,u^{i}\_{0}=u^{i}
in ( [122](https://arxiv.org/html/2604.26870#S3.E122 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (125) |  | u~11=(c−u2)​u~01+1u1​u~02,u~12=−u1​u~01.\\displaystyle\\tilde{u}^{1}\_{1}=({\\mathrm{c}}-u^{2})\\tilde{u}^{1}\_{0}+\\frac{1}{u^{1}}\\tilde{u}^{2}\_{0},\\qquad\\quad\\tilde{u}^{2}\_{1}=-u^{1}\\tilde{u}^{1}\_{0}. |  |

Equations ( [125](https://arxiv.org/html/2604.26870#S3.E125 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) can be resolved with respect to u1u^{1}, u2u^{2} as follows

|     |     |     |     |
| --- | --- | --- | --- |
| (126) |  | {u1=−u~21/u~10,u2=(c​u~01​u~12−u~01​u~02−u~11​u~12)/(u~01​u~12).\\displaystyle\\left\\{\\begin{aligned} u^{1}&=-\\tilde{u}^{2}\_{1}/\\tilde{u}^{1}\_{0},\\\<br>u^{2}&=({\\mathrm{c}}\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{1}-\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}-\\tilde{u}^{1}\_{1}\\tilde{u}^{2}\_{1})/(\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{1}).\\end{aligned}\\right. |  |

For each ℓ∈ℤ\\ell\\in\\mathbb{Z}, applying the operator 𝐒ℓ{\\mathbf{S}}^{\\ell} to ( [126](https://arxiv.org/html/2604.26870#S3.E126 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (127) |  | {uℓ1=−u~2ℓ+1/u~1ℓ,uℓ2=(cu~1ℓu~2ℓ+1−u~1ℓu~2ℓ−u~1ℓ+1u~2ℓ+1)/(u~1ℓu~2ℓ+1),ℓ∈ℤ.\\displaystyle\\left\\{\\begin{aligned} u^{1}\_{\\ell}&=-\\tilde{u}^{2}\_{\\ell+1}/\\tilde{u}^{1}\_{\\ell},\\\<br>u^{2}\_{\\ell}&=({\\mathrm{c}}\\tilde{u}^{1}\_{\\ell}\\tilde{u}^{2}\_{\\ell+1}-\\tilde{u}^{1}\_{\\ell}\\tilde{u}^{2}\_{\\ell}-\\tilde{u}^{1}\_{\\ell+1}\\tilde{u}^{2}\_{\\ell+1})/(\\tilde{u}^{1}\_{\\ell}\\tilde{u}^{2}\_{\\ell+1}),\\qquad\\qquad\\qquad\\qquad\\ell\\in\\mathbb{Z}.\\end{aligned}\\right. |  |

Substituting ψ11=u~1\\uppsi^{11}=\\tilde{u}^{1}, ψ21=u~2\\,\\uppsi^{21}=\\tilde{u}^{2}
and ( [127](https://arxiv.org/html/2604.26870#S3.E127 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) in ( [123](https://arxiv.org/html/2604.26870#S3.E123 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), we obtain 22-component equation

|     |     |     |     |
| --- | --- | --- | --- |
| (128) |  | {∂t(u~1)=u~01​u~02/u~12,∂t(u~2)=u~02​(c​u~−11−u~01)/u~−11.\\displaystyle\\left\\{\\begin{aligned} \\partial\_{t}(\\tilde{u}^{1})&=\\tilde{u}^{1}\_{0}\\tilde{u}^{2}\_{0}/\\tilde{u}^{2}\_{1},\\\<br>\\partial\_{t}(\\tilde{u}^{2})&=\\tilde{u}^{2}\_{0}({\\mathrm{c}}\\tilde{u}^{1}\_{-1}-\\tilde{u}^{1}\_{0})/\\tilde{u}^{1}\_{-1}.\\end{aligned}\\right. |  |

As discussed above,
system ( [122](https://arxiv.org/html/2604.26870#S3.E122 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [123](https://arxiv.org/html/2604.26870#S3.E123 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Since equations ( [126](https://arxiv.org/html/2604.26870#S3.E126 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [128](https://arxiv.org/html/2604.26870#S3.E128 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))
are derived from ( [122](https://arxiv.org/html/2604.26870#S3.E122 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [123](https://arxiv.org/html/2604.26870#S3.E123 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) (by means of introducing ( [124](https://arxiv.org/html/2604.26870#S3.E124 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations"))),
system ( [126](https://arxiv.org/html/2604.26870#S3.E126 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), ( [128](https://arxiv.org/html/2604.26870#S3.E128 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) as well.
This implies that ( [126](https://arxiv.org/html/2604.26870#S3.E126 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is a MT from ( [128](https://arxiv.org/html/2604.26870#S3.E128 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
which can also be verified by a straightforward computation.

###### Remark 7.

Recall that ( [120](https://arxiv.org/html/2604.26870#S3.E120 "In 3rd item ‣ 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) is a MLR for equation ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
and formulas ( [127](https://arxiv.org/html/2604.26870#S3.E127 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) are obtained by applying the operator 𝐒ℓ{\\mathbf{S}}^{\\ell} to ( [126](https://arxiv.org/html/2604.26870#S3.E126 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).
Using Lemma [4](https://arxiv.org/html/2604.26870#Thmlemma4 "Lemma 4. ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations") for the MLR ( [120](https://arxiv.org/html/2604.26870#S3.E120 "In 3rd item ‣ 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) and
the MT ( [126](https://arxiv.org/html/2604.26870#S3.E126 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) from ( [128](https://arxiv.org/html/2604.26870#S3.E128 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) to ( [114](https://arxiv.org/html/2604.26870#S3.E114 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")),
we can substitute ( [127](https://arxiv.org/html/2604.26870#S3.E127 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")) in ( [120](https://arxiv.org/html/2604.26870#S3.E120 "In 3rd item ‣ 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")), and this gives a MLR for equation ( [128](https://arxiv.org/html/2604.26870#S3.E128 "In 3.2. Other examples ‣ 3. Miura-type transformations and matrix Lax representations ‣ On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations")).

## Acknowledgments

The author would like to thank S. Konstantinou-Rizos and A.V. Mikhailov for useful discussions.

This work was supported by the Russian Science Foundation (grant No. 25-21-00454,
https://rscf.ru/en/project/25-21-00454/ ).

## References

- \[1\]
E. Chistov, S. Igonin.
On matrix Lax representations and constructions
of Miura-type transformations for differential-difference equations.
_Partial Differential Equations in Applied Mathematics_ 13 (2025), 101014.
arXiv:2410.01474 \[nlin.SI\]

- \[2\]
V.G. Drinfeld and V.V. Sokolov.
On equations related to the Korteweg–de Vries equation.
_Soviet Math. Dokl._ 32 (1985), 361–365.

- \[3\]
H. Flaschka. The Toda lattice. II. Existence of integrals. _Phys. Rev. B_ 9 (1974), 1924–1925.

- \[4\]
R.N. Garifullin, R.I. Yamilov, and D. Levi.
Classification of five-point differential–difference equations.
_J. Phys. A_ 50 (2017), 125201.
arXiv:1610.07342 \[nlin.SI\]

- \[5\]
R.N. Garifullin, R.I. Yamilov, and D. Levi.
Classification of five-point differential–difference equations II.
_J. Phys. A_ 51 (2018), 065204.
arXiv:1708.02456 \[nlin.SI\]

- \[6\]
J. Hietarinta, N. Joshi, and F.W. Nijhoff.
_Discrete systems and integrability._
Cambridge University Press, Cambridge, 2016.

- \[7\]
S. Igonin.
Simplifications of Lax pairs for differential-difference equations by gauge transformations
and (doubly) modified integrable equations.
_Partial Differential Equations in Applied Mathematics_ 11 (2024), 100821.
arXiv:2403.12022 \[nlin.SI\]

- \[8\]
S. Igonin.
Matrix Lax pairs under the gauge equivalence relation induced by the gauge group action
and Miura-type transformations for lattice equations.
_J. Geom. Phys._ 216 (2025), 105585.
arXiv:2405.08579 \[nlin.SI\]

- \[9\]
S. Igonin.
The gauge action on semi-discrete Lax representations and its invariants.
arXiv:2604.20830 \[nlin.SI\]

- \[10\]
F. Khanizadeh, A.V. Mikhailov, and Jing Ping Wang.
Darboux transformations and recursion operators for differential-difference equations.
_Theor. Math. Phys._ 177 (2013), 1606–1654.
arXiv:1305.0588 \[nlin.SI\]

- \[11\]
S. Konstantinou-Rizos, A.V. Mikhailov, and P. Xenitidis.
Reduction groups and related integrable difference systems of nonlinear Schrödinger type.
_J. Math. Phys._ 56 (2015), 082701.

- \[12\]
D. Levi, P. Winternitz, and R.I. Yamilov.
Continuous symmetries and integrability of discrete equations.
_CRM Monograph Series_ 38.
Providence, RI: American Mathematical Society, 2022.

- \[13\]
A.G. Meshkov and M.Ju. Balakhnev.
Two-field integrable evolutionary systems of the third order and their differential substitutions.
_SIGMA_ 4 (2008), Paper 018.
arXiv:0802.1253 \[nlin.SI\]

- \[14\] A.V. Mikhailov, A.B. Shabat, and V.V. Sokolov.
The symmetry approach to classification of integrable equations.
In: _What is integrability?_, edited by V. E. Zakharov, Springer–Verlag, 1991.

- \[15\]
S.V. Manakov. Complete integrability and stochastization in discrete dynamical systems.
_Sov. Phys. JETP_ 40 (1975), 269–274.

- \[16\]
E. Mansfield, G. Marí Beffa, Jing Ping Wang.
Discrete moving frames and discrete integrable systems.
_Foundations of Computational Mathematics_ 13 (2013), 545–582.

- \[17\]
M. Marvan. On zero-curvature representations of partial differential equations.
_Differential geometry and its applications (Opava, 1992)_, 103–122.
Silesian Univ. Opava, 1993.
http://emis.maths.tcd.ie/proceedings/5ICDGA
- \[18\]
M. Marvan.
A direct procedure to compute zero-curvature representations. The case s​l2sl\_{2}.
_Secondary Calculus and Cohomological Physics (Moscow, 1997)_, 9 pp.
http://emis.maths.tcd.ie/proceedings/SCCP97
- \[19\]
R. Miura. Korteweg – de Vries equation and
generalizations. I. A remarkable explicit nonlinear transformation.
_J. Math. Phys._ 9 (1968), 1202–1204.

- \[20\]
R.M. Miura, C.S. Gardner, and M.D. Kruskal.
Korteweg-de Vries equation and generalizations. II.
Existence of conservation laws and constants of motion.
_J. Math. Phys._ 9 (1968), 1204–1209.

- \[21\]
S.Yu. Sakovich.
On zero-curvature representations of evolution equations.
_J. Phys. A_ 28 (1995), 2861–2869.

- \[22\]
Yu.B. Suris.
_The Problem of Integrable Discretization: Hamiltonian Approach._
Progress in Mathematics, 219. Birkhäuser Verlag, Basel, 2003.

- \[23\]
R. Yamilov.
Symmetries as integrability criteria for differential difference equations.
_J. Phys. A_ 39 (2006), R541–R623.


Experimental support, please
[view the build logs](https://arxiv.org/html/2604.26870v1/__stdout.txt)
for errors. Generated by
[L\\
A\\
T\\
Exml![[LOGO]](<Base64-Image-Removed>)](https://math.nist.gov/~BMiller/LaTeXML/).


## Instructions for reporting errors

We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile
support. To report errors in the HTML that will help us improve conversion and rendering, choose any of the
methods listed below:

- Click the "Report Issue" () button, located in the page header.

**Tip:** You can select the relevant text first, to include it in your report.

Our team has already identified [the following issues](https://github.com/arXiv/html_feedback/issues). We appreciate your time reviewing and reporting rendering errors we
may not have found yet. Your efforts will help us improve the HTML versions for all readers, because disability
should not be a barrier to accessing research. Thank you for your continued support in championing open access for
all.

Have a free development cycle? Help support accessibility at arXiv! Our collaborators at LaTeXML maintain a [list of packages that need conversion](https://github.com/brucemiller/LaTeXML/wiki/Porting-LaTeX-packages-for-LaTeXML), and welcome [developer contributions](https://github.com/brucemiller/LaTeXML/issues).

We gratefully acknowledge support from
our **major funders**,
[**member institutions**](https://info.arxiv.org/about/ourmembers.html), ,
and all contributors.


[About](https://info.arxiv.org/about)· [Help](https://info.arxiv.org/help)· [Contact](https://info.arxiv.org/help/contact.html)· [Subscribe](https://info.arxiv.org/help/subscribe)· [Copyright](https://info.arxiv.org/help/license/index.html)· [Privacy](https://info.arxiv.org/help/policies/privacy_policy.html)· [Accessibility](https://info.arxiv.org/help/web_accessibility.html)· [Operational Status (opens in new tab)](https://status.arxiv.org/)

Major funding support from

[![Simons Foundation](https://arxiv.org/static/base/1.0.1/images/funders/simons-foundation.png)](https://www.simonsfoundation.org/)[![Simons Foundation International](https://arxiv.org/static/base/1.0.1/images/funders/simons-foundation-international.png)](https://www.sfi.org.bm/)[![Schmidt Sciences](https://arxiv.org/static/base/1.0.1/images/funders/schmidt-sciences.png)](https://www.schmidtsciences.org/)