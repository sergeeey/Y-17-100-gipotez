##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHubSubmit in GitHub

![](https://arxiv.org/static/base/1.0.1/images/icons/smileybones-small.svg)arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[![arXiv logo](https://arxiv.org/static/base/1.0.1/images/arxiv-logo-primary-light.svg)Back to arXiv](https://arxiv.org/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [Back to Abstract](https://arxiv.org/abs/2604.26870v1 "Back to abstract page") [Download PDF](https://arxiv.org/pdf/2604.26870v1 "Download PDF")

1. Abstract.-dimensional evolutionary differential-difference equations")
2. 1 Introduction-dimensional evolutionary differential-difference equations")
3. 2 General results on differential-difference matrix Lax representations-dimensional evolutionary differential-difference equations")
4. 3 Miura-type transformations and matrix Lax representations-dimensional evolutionary differential-difference equations")
   1. 3.1 Non-autonomous examples-dimensional evolutionary differential-difference equations")
   2. 3.2 Other examples-dimensional evolutionary differential-difference equations")
5. References-dimensional evolutionary differential-difference equations")

[License: arXiv.org perpetual non-exclusive license](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2604.26870v1 [nlin.SI] 29 Apr 2026

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
from the papers [S. Konstantinou-Rizos, A.V. Mikhailov, P. Xenitidis, _J. Math. Phys._ 2015],
[E. Mansfield, G. Marí Beffa, Jing Ping Wang, _Found. Comput. Math._ 2013]),
including non-autonomous examples.

###### Key words and phrases:

Integrable differential-difference equations; matrix Lax representations; Lax pairs; gauge transformations; Miura-type transformations

###### 2020 Mathematics Subject Classification

37K60, 37K35

## 1. Introduction

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
(see, e.g.,  [6, 10, 11, 12, 16, 22]
and references therein).

In this paper, ℤ>0mathbb{Z}_{>0} and ℤ≥0mathbb{Z}_{geq 0} denote the sets of positive and nonnegative integers, respectively.
Let N∈ℤ>0Ninmathbb{Z}_{>0}. Below we consider an equation for an NN-component vector-function
u=(u1​(n,t),…,uN​(n,t))u=big(u^{1}(n,t),ldots,u^{N}(n,t)big)
of an integer variable nn and a real or complex variable tt.
For any fixed integer ℓell, we have uℓ=(uℓ1,…,uℓN)u_{ell}=(u^{1}_{ell},ldots,u^{N}_{ell}),
where for each ξ=1,…,Nxi=1,ldots,N the component uℓξu_{ell}^{xi} is a function
of n,tn,t defined as follows uℓξ​(n,t)=uξ​(n+ℓ,t)u_{ell}^{xi}(n,t)=u^{xi}(n!+!ell,t).
That is, uℓ​(n,t)=u⁡(n+ℓ,t)u_{ell}(n,t)=u(n!+!ell,t). In particular, u0=uu_{0}=u.

Let a,b∈ℤ{mathrm{a}},{mathrm{b}}inmathbb{Z}, a≤b,{mathrm{a}}leq{mathrm{b}}.
Consider a (1+1)-dimensional evolutionary differential-difference equation

|     |     |     |     |
| --- | --- | --- | --- |
| (1) |  | ∂t(u)=𝔽⁡(n,ua,ua+1,…,ub),displaystylepartial_{t}(u)=mathbb{F}(n,u_{mathrm{a}},u_{{mathrm{a}}+1},ldots,u_{mathrm{b}}), |  |

where 𝔽mathbb{F} is an NN-component vector-function 𝔽=(𝔽1,…,𝔽N)mathbb{F}=(mathbb{F}^{1},ldots,mathbb{F}^{N}),
which may depend on nn and on uℓu_{ell} for ℓ=a,a+1,…,bell={mathrm{a}},{{mathrm{a}}!+!1},ldots,{mathrm{b}}.

The differential-difference equation ( 1-dimensional evolutionary differential-difference equations"))
is equivalent to the following infinite collection of differential equations

|     |     |     |     |
| --- | --- | --- | --- |
| (2) |  | ∂t(u⁡(n,t))=𝔽⁡(n,u⁡(n+a,t),u⁡(n+a+1,t),…,u⁡(n+b,t)),n∈ℤ.displaystylepartial_{t}big(u(n,t)big)=mathbb{F}big(n,u(n!+!{mathrm{a}},t),u(n!+!{mathrm{a}}!+!1,t),ldots,u(n!+!{mathrm{b}},t)big),qquadquad ninmathbb{Z}. |  |

Using the components of u=(u1​(n,t),…,uN​(n,t))u=big(u^{1}(n,t),ldots,u^{N}(n,t)big)
and of 𝔽=(𝔽1,…,𝔽N)mathbb{F}=(mathbb{F}^{1},ldots,mathbb{F}^{N}), one can rewrite ( 1-dimensional evolutionary differential-difference equations")) as

|     |     |     |     |
| --- | --- | --- | --- |
| (3) |  | ∂t(ui)=𝔽i(n,ua,ua+1,…,ub),i=1,…,N.displaystylepartial_{t}big(u^{i}big)=mathbb{F}^{i}(n,u_{mathrm{a}},u_{{mathrm{a}}+1},ldots,u_{mathrm{b}}),qquadquad i=1,ldots,N. |  |

For each fixed ℓ∈ℤellinmathbb{Z}, replacing nn by n+ℓn+ell in ( 2-dimensional evolutionary differential-difference equations")),
we see that ( 1-dimensional evolutionary differential-difference equations")) implies

|     |     |     |     |
| --- | --- | --- | --- |
| (4) |  | ∂t(uℓi)=𝔽i(n+ℓ,ua+ℓ,ua+1+ℓ,…,ub+ℓ),i=1,…,N,ℓ∈ℤ.displaystylepartial_{t}big(u^{i}_{ell}big)=mathbb{F}^{i}(n!+!ell,u_{{mathrm{a}}+ell},u_{{mathrm{a}}+1+ell},ldots,u_{{mathrm{b}}+ell}),qquadquad i=1,ldots,N,qquadellinmathbb{Z}. |  |

We use the formal theory of (1+1)-dimensional evolutionary differential-difference equations, where one regards

|     |     |     |     |
| --- | --- | --- | --- |
| (5) |  | n,uℓ=(uℓ1,…,uℓN),ℓ∈ℤ,displaystyle n,qquadqquad u_{ell}=(u^{1}_{ell},ldots,u^{N}_{ell}),quadellinmathbb{Z}, |  |

as independent quantities.
Note that uℓ=(uℓ1,…,uℓN)u_{ell}=(u^{1}_{ell},ldots,u^{N}_{ell})
are sometimes called _dynamical variables_.

In this paper, the notation of the type f=f⁡(n,uℓ,…)f=f(n,u_{ell},ldots) means
that a function ff depends on a finite number of the variables ( 5-dimensional evolutionary differential-difference equations")).
The notation of the type f=f⁡(n,uα,…,uβ)f=f(n,u_{upalpha},ldots,u_{upbeta})
for some integers α≤βupalphalequpbeta means that ff
may depend on nn and on uℓξu_{ell}^{xi} for ℓ=α,…,βell=upalpha,ldots,upbeta,
ξ=1,…,N,xi=1,ldots,N.

Equation ( 1-dimensional evolutionary differential-difference equations")) said to be _non-autonomous_
if its right-hand side 𝔽mathbb{F} depends nontrivially on nn.

We denote by 𝐒{mathbf{S}} the _shift operator_ with respect to the variable nn.
For any function g=g⁡(n,t)g=g(n,t) one has the function 𝐒⁡(g){mathbf{S}}(g)
such that 𝐒⁡(g)​(n,t)=g⁡(n+1,t){mathbf{S}}(g)(n,t)=g(n!+!1,t).
Furthermore, for each k∈ℤkinmathbb{Z}, we have the kkth power 𝐒k{mathbf{S}}^{k}
of the operator 𝐒{mathbf{S}} and the formula 𝐒k​(g)​(n,t)=g⁡(n+k,t){mathbf{S}}^{k}(g)(n,t)=g(n!+!k,t).

Since uℓu_{ell} corresponds to u⁡(n+ℓ,t)u(n+ell,t), the operator 𝐒{mathbf{S}}
and its powers 𝐒k{mathbf{S}}^{k} for k∈ℤkinmathbb{Z} act on functions of
the variables ( 5-dimensional evolutionary differential-difference equations")) by means of the rules

|     |     |     |
| --- | --- | --- |
|  | 𝐒(n)=n+1,𝐒(uℓ)=uℓ+1,𝐒k(n)=n+k,𝐒k(uℓ)=uℓ+k,𝐒k​(f⁡(n,uℓ,…))=f⁡(n+k,𝐒k​(uℓ),…).displaystylebegin{gathered}{mathbf{S}}(n)=n+1,qquad{mathbf{S}}(u_{ell})=u_{ell+1},qquad{mathbf{S}}^{k}(n)=n+k,qquad{mathbf{S}}^{k}(u_{ell})=u_{ell+k},<br>{mathbf{S}}^{k}big(f(n,u_{ell},ldots)big)=f(n!+!k,{mathbf{S}}^{k}(u_{ell}),ldots).end{gathered} |  |

That is, applying 𝐒k{mathbf{S}}^{k} to a function f=f⁡(n,uℓ,…)f=f(n,u_{ell},ldots),
we replace nn by n+kn!+!k in ff
and replace uℓξu_{ell}^{xi} by uℓ+kξu_{ell+k}^{xi} in ff for all ℓ∈ℤellinmathbb{Z},
ξ=1,…,N,xi=1,ldots,N.

The _total derivative operator 𝐃tmathbf{D}_{t} corresponding to equation ( 1-dimensional evolutionary differential-difference equations"))_
acts on functions of the variables ( 5-dimensional evolutionary differential-difference equations")) as follows

|     |     |     |     |
| --- | --- | --- | --- |
| (8) |  | 𝐃t​(f⁡(n,uℓ,…))=∑ℓ,ξ𝐒ℓ​(𝔽ξ)⋅∂f∂uℓξ,displaystylemathbf{D}_{t}big(f(n,u_{ell},ldots)big)=sum_{ell,xi}{mathbf{S}}^{ell}(mathbb{F}^{xi})cdotfrac{partial f}{partial u_{ell}^{xi}}, |  |

where 𝔽ξ=𝔽ξ​(n,ua,…,ub)mathbb{F}^{xi}=mathbb{F}^{xi}(n,u_{mathrm{a}},ldots,u_{mathrm{b}}), ξ=1,…,N,xi=1,ldots,N,
are the components of the vector-function
𝔽=(𝔽1,…,𝔽N)mathbb{F}=(mathbb{F}^{1},ldots,mathbb{F}^{N}) from ( 1-dimensional evolutionary differential-difference equations")).
Formula ( 8-dimensional evolutionary differential-difference equations")) reflects the chain rule for the derivative with respect to tt,
taking into account equations ( 4-dimensional evolutionary differential-difference equations")).
From ( 1-dimensional evolutionary differential-difference equations")), ( 8-dimensional evolutionary differential-difference equations")) it follows that, for any function h=h⁡(n,uℓ,…)h=h(n,u_{ell},ldots),
one has 𝐃t​(𝐒⁡(h))=𝐒⁡(𝐃t​(h))mathbf{D}_{t}big({mathbf{S}}(h)big)={mathbf{S}}big(mathbf{D}_{t}(h)big).

In this paper, matrix-functions are sometimes called simply matrices.

###### Remark 1.

In this paper we deal with functions which may depend
on a finite number of the variables ( 5-dimensional evolutionary differential-difference equations")) and a complex parameter λuplambda.
For simplicity of exposition, in order to present the main ideas clearly and concisely,
we consider only functions which depend rationally on
the variables ( 5-dimensional evolutionary differential-difference equations")) and meromorphically on λuplambda, in the sense described below.
Many results of this paper can be extended to more general classes of functions,
but such extension requires more technical and heavy proofs.

A scalar (ℂmathbb{C}-valued) function f=f⁡(n,uℓ,…,λ)f=f(n,u_{ell},ldots,uplambda)
is said to be _of admissible type_ if ff can be written in the form

|     |     |     |     |
| --- | --- | --- | --- |
| (9) |  | f=g⁡(n,uℓ,…,λ)h⁡(n,uℓ,…,λ),displaystyle f=frac{g(n,u_{ell},ldots,uplambda)}{h(n,u_{ell},ldots,uplambda)}, |  |

where g⁡(n,uℓ,…,λ)g(n,u_{ell},ldots,uplambda) and h⁡(n,uℓ,…,λ)h(n,u_{ell},ldots,uplambda) are polynomials in the variables ( 5-dimensional evolutionary differential-difference equations"))
whose coefficients are meromorphic functions of λ∈ℂuplambdainmathbb{C},
and h⁡(n,uℓ,…,λ)h(n,u_{ell},ldots,uplambda) is not the zero polynomial.

We denote by ℳ​ℰ​ℛ​(ℂ,λ)mathcal{M!E!R}(mathbb{C},uplambda) the field of meromorphic functions of λ∈ℂuplambdainmathbb{C}.
Then ( 9-dimensional evolutionary differential-difference equations")) can be regarded as a rational function of n,uℓ=(uℓ1,…,uℓN)n,,u_{ell}=(u^{1}_{ell},ldots,u^{N}_{ell})
with coefficients in ℳ​ℰ​ℛ​(ℂ,λ)mathcal{M!E!R}(mathbb{C},uplambda).
Thus, a scalar function f=f⁡(n,uℓ,…,λ)f=f(n,u_{ell},ldots,uplambda) is of admissible type if ff
is a rational function of the variables ( 5-dimensional evolutionary differential-difference equations")) with coefficients in ℳ​ℰ​ℛ​(ℂ,λ)mathcal{M!E!R}(mathbb{C},uplambda).

For each d∈ℤ>0mathrm{d}inmathbb{Z}_{>0}, when we consider a d×dmathrm{d}timesmathrm{d} matrix-function
𝐌=𝐌⁡(n,uℓ,…,λ)mathbf{M}=mathbf{M}(n,u_{ell},ldots,uplambda), we assume that each entry of the matrix 𝐌mathbf{M}
is a scalar function of admissible type.
When we say that such a matrix 𝐌⁡(n,uℓ,…,λ)mathbf{M}(n,u_{ell},ldots,uplambda) is assumed to be invertible,
we mean that the determinant det(𝐌⁡(n,uℓ,…,λ))detbig(mathbf{M}(n,u_{ell},ldots,uplambda)big) is not identically zero.
Then (det(𝐌⁡(n,uℓ,…,λ)))−1big(detbig(mathbf{M}(n,u_{ell},ldots,uplambda)big)big)^{-1} is well defined
(as a rational function of n,uℓ=(uℓ1,…,uℓN)n,,u_{ell}=(u^{1}_{ell},ldots,u^{N}_{ell}) with coefficients in ℳ​ℰ​ℛ​(ℂ,λ)mathcal{M!E!R}(mathbb{C},uplambda)),
which allows us to compute the inverse matrix 𝐌−1=(𝐌⁡(n,uℓ,…,λ))−1mathbf{M}^{-1}=big(mathbf{M}(n,u_{ell},ldots,uplambda)big)^{-1},
whose entries are of admissible type.

###### Definition 1.

Let d∈ℤ>0mathrm{d}inmathbb{Z}_{>0}.
Let 𝐌=𝐌⁡(n,uℓ,…,λ)mathbf{M}=mathbf{M}(n,u_{ell},ldots,uplambda) and 𝐔=𝐔⁡(n,uℓ,…,λ)mathbf{U}=mathbf{U}(n,u_{ell},ldots,uplambda) be d×dmathrm{d}timesmathrm{d} matrix-functions
depending on the variables ( 5-dimensional evolutionary differential-difference equations")) and a complex parameter λuplambda.
Suppose that 𝐌mathbf{M} is invertible (in the sense of Remark 1-dimensional evolutionary differential-difference equations")) and we have

|     |     |     |     |
| --- | --- | --- | --- |
| (10) |  | 𝐃t​(𝐌)=𝐒⁡(𝐔)⋅𝐌−𝐌⋅𝐔,displaystylemathbf{D}_{t}(mathbf{M})={mathbf{S}}(mathbf{U})cdotmathbf{M}-mathbf{M}cdotmathbf{U}, |  |

where 𝐃tmathbf{D}_{t} is given by ( 8-dimensional evolutionary differential-difference equations")).
Then the pair (𝐌,𝐔)(mathbf{M},mathbf{U}) is called a _matrix Lax representation_ (MLR) for equation ( 1-dimensional evolutionary differential-difference equations")).

The connection between ( 10-dimensional evolutionary differential-difference equations")) and ( 1-dimensional evolutionary differential-difference equations")) is as follows.
The components 𝔽ξmathbb{F}^{xi}, ξ=1,…,N,xi=1,ldots,N, of the right-hand side 𝔽⁡(n,ua,…,ub)mathbb{F}(n,u_{mathrm{a}},ldots,u_{mathrm{b}})
of ( 1-dimensional evolutionary differential-difference equations")) appear in formula ( 8-dimensional evolutionary differential-difference equations")) for the operator 𝐃tmathbf{D}_{t}, which is used in ( 10-dimensional evolutionary differential-difference equations")).

We say that a MLR (𝐌⁡(n,uℓ,…,λ),𝐔⁡(n,uℓ,…,λ))big(mathbf{M}(n,u_{ell},ldots,uplambda),,mathbf{U}(n,u_{ell},ldots,uplambda)big) is _non-autonomous_
if at least one of the matrix-functions 𝐌,𝐔mathbf{M},,mathbf{U} depends nontrivially on nn.

Correspondingly, a MLR (𝐌,𝐔)big(mathbf{M},mathbf{U}big) is called _autonomous_ if 𝐌,𝐔mathbf{M},,mathbf{U} do not depend on nn.

Relation ( 10-dimensional evolutionary differential-difference equations")) implies that the following (overdetermined) auxiliary linear system

|     |     |     |     |
| --- | --- | --- | --- |
| (11) |  | 𝐒⁡(Ψ)=𝐌⋅Ψ,∂t(Ψ)=𝐔⋅Ψdisplaystyle{mathbf{S}}(Psi)=mathbf{M}cdotPsi,qquadquadpartial_{t}(Psi)=mathbf{U}cdotPsi |  |

is compatible modulo equation ( 1-dimensional evolutionary differential-difference equations")).
Here Ψ=Ψ⁡(n,t)Psi=Psi(n,t) is an invertible d×dmathrm{d}timesmathrm{d} matrix-function.

We say that the matrix 𝐌=𝐌⁡(n,uℓ,…,λ)mathbf{M}=mathbf{M}(n,u_{ell},ldots,uplambda) is the _𝐒{mathbf{S}}-part_ of the MLR (𝐌,𝐔)(mathbf{M},mathbf{U}).

Then for any invertible d×dmathrm{d}timesmathrm{d} matrix-function
𝐆=𝐆⁡(n,uℓ,…,λ)mathbf{G}=mathbf{G}(n,u_{ell},ldots,uplambda) the matrices

|     |     |     |     |
| --- | --- | --- | --- |
| (12) |  | 𝐌^=𝐒⁡(𝐆)⋅𝐌⋅𝐆−1,𝐔^=𝐃t​(𝐆)⋅𝐆−1+𝐆⋅𝐔⋅𝐆−1displaystylewidehat{mathbf{M}}={mathbf{S}}(mathbf{G})cdotmathbf{M}cdotmathbf{G}^{-1},qquadquadwidehat{mathbf{U}}=mathbf{D}_{t}(mathbf{G})cdotmathbf{G}^{-1}+mathbf{G}cdotmathbf{U}cdotmathbf{G}^{-1} |  |

form a MLR for equation ( 1-dimensional evolutionary differential-difference equations")) as well.
Here the matrix 𝐆=𝐆⁡(n,uℓ,…,λ)mathbf{G}=mathbf{G}(n,u_{ell},ldots,uplambda)
is invertible in the sense of Remark 1-dimensional evolutionary differential-difference equations") and is called a _gauge transformation_.
The MLR (𝐌^,𝐔^)big(widehat{mathbf{M}},,widehat{mathbf{U}}big) is _gauge equivalent_
to the MLR (𝐌,𝐔)(mathbf{M},mathbf{U}), and one can say that
(𝐌^,𝐔^)big(widehat{mathbf{M}},,widehat{mathbf{U}}big) is obtained from (𝐌,𝐔)(mathbf{M},mathbf{U})
by means of the gauge transformation 𝐆mathbf{G}.

###### Definition 2.

We consider MLRs for a given equation ( 1-dimensional evolutionary differential-difference equations")).
A MLR (𝐌,𝐔)(mathbf{M},mathbf{U}) is said to be _trivial_
if 𝐌mathbf{M} does not depend on uℓu_{ell} for any ℓ∈ℤellinmathbb{Z}.
Then ( 8-dimensional evolutionary differential-difference equations")) yields 𝐃t​(𝐌)=0mathbf{D}_{t}(mathbf{M})=0, and from ( 10-dimensional evolutionary differential-difference equations")) one derives
𝐒⁡(𝐔)=𝐌⋅𝐔⋅𝐌−1{mathbf{S}}(mathbf{U})=mathbf{M}cdotmathbf{U}cdotmathbf{M}^{-1}, which
implies that 𝐔mathbf{U} does not depend on uℓu_{ell} either.
(One can show this easily, using the rules ( 1-dimensional evolutionary differential-difference equations"))).
Hence a trivial MLR does not provide any information about equation ( 1-dimensional evolutionary differential-difference equations")).

A MLR is called _fake_ if it is gauge equivalent to a trivial MLR.
That is, fake MLRs are obtained from trivial MLRs by applying gauge transformations,
and this can be done independently of equation ( 1-dimensional evolutionary differential-difference equations")).

###### Definition 3.

Fix d∈ℤ>0mathrm{d}inmathbb{Z}_{>0}.
Let 𝕎dmathbb{W}_{mathrm{d}} be the vector space of all d×dmathrm{d}timesmathrm{d} matrix-functions of the form Q=Q⁡(n,uℓ,…,λ)Q=Q(n,u_{ell},ldots,uplambda).
Let 𝔹d⊂𝕎dmathbb{B}_{mathrm{d}}subsetmathbb{W}_{mathrm{d}} be the subset of all invertible d×dmathrm{d}timesmathrm{d} matrix-functions M=M⁡(n,uℓ,…,λ)M=M(n,u_{ell},ldots,uplambda).
For each M∈𝔹dMinmathbb{B}_{mathrm{d}}, we consider the operator ∇M:𝕎d→𝕎dnabla_{M}colonmathbb{W}_{mathrm{d}}tomathbb{W}_{mathrm{d}} given by the formula

|     |     |     |     |
| --- | --- | --- | --- |
| (13) |  | ∇M(Q)=𝐒⁡(M−1​Q​M).displaystylenabla_{M}(Q)={mathbf{S}}(M^{-1}QM). |  |

The operator ∇Mnabla_{M} is invertible, and one has

|     |     |     |     |
| --- | --- | --- | --- |
| (14) |  | ∇M−1(Q)=M⋅𝐒−1​(Q)⋅M−1.displaystylenabla_{M}^{-1}(Q)=Mcdot{mathbf{S}}^{-1}(Q)cdot M^{-1}. |  |

For each k∈ℤkinmathbb{Z}, we denote by ∇Mknabla_{M}^{k} the kkth power
of the operator ∇Mnabla_{M}. In particular, one has

|     |     |     |
| --- | --- | --- |
|  | ∇M0(Q)=Q,∇M2(Q)=∇M(∇M(Q))=𝐒⁡(M−1​𝐒​(M−1​Q​M)​M),displaystylenabla_{M}^{0}(Q)=Q,qquadquadnabla_{M}^{2}(Q)=nabla_{M}(nabla_{M}(Q))={mathbf{S}}(M^{-1}{mathbf{S}}(M^{-1}QM)M), |  |
|  | ∇M−2(Q)=∇M−1(∇M−1(Q))=M​𝐒−1​(M​𝐒−1​(Q)​M−1)​M−1.displaystylenabla_{M}^{-2}(Q)=nabla_{M}^{-1}(nabla_{M}^{-1}(Q))=M{mathbf{S}}^{-1}(M{mathbf{S}}^{-1}(Q)M^{-1})M^{-1}. |  |

Furthermore, for each j=1,…,Nj=1,ldots,N, we consider the map 𝚫uj:𝔹d→𝕎dboldsymbol{Delta}^{u^{j}}colonmathbb{B}_{mathrm{d}}tomathbb{W}_{mathrm{d}} given by

|     |     |     |     |
| --- | --- | --- | --- |
| (15) |  | 𝚫uj(M)=∑ℓ∈ℤ∇M−ℓ(∂uℓj(M)⋅M−1),M=M(n,uℓ,…,λ)∈𝔹d,j=1,…,N.displaystyleboldsymbol{Delta}^{u^{j}}(M)=sum_{ellinmathbb{Z}}nabla_{M}^{-ell}big(partial_{u^{j}_{ell}}(M)cdot M^{-1}big),qquadquad M=M(n,u_{ell},ldots,uplambda)inmathbb{B}_{mathrm{d}},qquad j=1,ldots,N. |  |

For instance,
if M=M⁡(n,u−1ξ,u0ξ,u1ξ,λ)M=Mbig(n,u^{xi}_{-1},u^{xi}_{0},u^{xi}_{1},uplambdabig) depends only on nn, u−1ξu^{xi}_{-1},
u0ξu^{xi}_{0}, u1ξu^{xi}_{1}, ξ=1,…,N,xi=1,ldots,N, and on λuplambda, then

|     |     |     |
| --- | --- | --- |
|  | 𝚫uj​(M⁡(n,u−1ξ,u0ξ,u1ξ,λ))=∑ℓ∈ℤ∇M−ℓ(∂uℓj(M)⋅M−1)=∑ℓ=−1,0,1∇M−ℓ(∂uℓj(M)⋅M−1)==𝐒⁡(M−1​(∂u−1j(M)⋅M−1)​M)+∂u0j(M)⋅M−1+M​𝐒−1​(∂u1j(M)⋅M−1)​M−1.boldsymbol{Delta}^{u^{j}}big(Mbig(n,u^{xi}_{-1},u^{xi}_{0},u^{xi}_{1},uplambdabig)big)=sum_{ellinmathbb{Z}}nabla_{M}^{-ell}big(partial_{u^{j}_{ell}}(M)cdot M^{-1}big)=sum_{ell=-1,0,1}nabla_{M}^{-ell}big(partial_{u^{j}_{ell}}(M)cdot M^{-1}big)=<br>={mathbf{S}}big(M^{-1}big(partial_{u^{j}_{-1}}(M)cdot M^{-1}big)Mbig)+partial_{u^{j}_{0}}(M)cdot M^{-1}+M{mathbf{S}}^{-1}big(partial_{u^{j}_{1}}(M)cdot M^{-1}big)M^{-1}. |  |

###### Definition 4.

Let α,β∈ℤupalpha,upbetainmathbb{Z}, α≤β,upalphalequpbeta. A MLR (𝐌⁡(n,uℓ,…,λ),𝐔⁡(n,uℓ,…,λ))big(mathbf{M}(n,u_{ell},ldots,uplambda),,mathbf{U}(n,u_{ell},ldots,uplambda)big)
is said to be _of class (α,β)(upalpha,upbeta)_
if its 𝐒{mathbf{S}}-part𝐌⁡(n,uℓ,…,λ)mathbf{M}(n,u_{ell},ldots,uplambda) is of the form 𝐌=𝐌⁡(n,uα,…,uβ,λ)mathbf{M}=mathbf{M}(n,u_{upalpha},dots,u_{upbeta},uplambda).
That is, a MLR (𝐌,𝐔)(mathbf{M},mathbf{U}) is of class (α,β)(upalpha,upbeta) if 𝐌mathbf{M} may depend only on n,uα,…,uβ,λn,u_{upalpha},dots,u_{upbeta},uplambda,
while 𝐔mathbf{U} may depend on any finite number of the variables ( 5-dimensional evolutionary differential-difference equations")) and on λuplambda.

Let α,β,q∈ℤupalpha,upbeta,qinmathbb{Z}, α≤β,upalphalequpbeta.
As shown in Lemma 1-dimensional evolutionary differential-difference equations") in Section 2-dimensional evolutionary differential-difference equations"),
any MLR (𝐌,𝐔)(mathbf{M},mathbf{U}) of class (α,β)(upalpha,upbeta) is gauge equivalent
to some MLR of class (α+q,β+q)(upalpha!+!q,upbeta!+!q)
with 𝐒{mathbf{S}}-part equal to 𝐒q​(𝐌){mathbf{S}}^{q}(mathbf{M}).
Therefore, since we want to study MLRs up to gauge equivalence,
it is sufficient to consider MLRs of class (0,k)(0,k) for k∈ℤ≥0kinmathbb{Z}_{geq 0}.

In Section 2-dimensional evolutionary differential-difference equations") we present the following results.

- •


Let p∈ℤ>0pinmathbb{Z}_{>0}.
For a given MLR of class (0,p)(0,p) with 𝐒{mathbf{S}}-part 𝐌⁡(n,u0,u1,…,up,λ)mathbf{M}(n,u_{0},u_{1},ldots,u_{p},uplambda),
Theorem 1-dimensional evolutionary differential-difference equations") provides
a necessary and sufficient condition for the possibility to
simplify the MLR by means of gauge transformations in the following sense:


the possibility to eliminate the dependence on upu_{p} in the 𝐒{mathbf{S}}-part
by applying a gauge transformation (i.e. to obtain a gauge equivalent MLR
with 𝐒{mathbf{S}}-part of the form 𝐌^​(n,u0,…,up−1,λ)widehat{mathbf{M}}(n,u_{0},ldots,u_{p-1},uplambda)).
If a MLR satisfies this condition (given in ( 27-dimensional evolutionary differential-difference equations"))),
then Theorem 1-dimensional evolutionary differential-difference equations") provides an explicit formula
for a suitable gauge transformation (see ( 28-dimensional evolutionary differential-difference equations"))).





In other words, if we have a MLR (𝐌,𝐔)(mathbf{M},mathbf{U}) of class (0,p)(0,p), then
Theorem 1-dimensional evolutionary differential-difference equations") gives a necessary and sufficient condition for
existence of a gauge transformation 𝐆=𝐆⁡(n,uℓ,…,λ)mathbf{G}=mathbf{G}(n,u_{ell},ldots,uplambda)
such that the corresponding gauge equivalent MLR ( 12-dimensional evolutionary differential-difference equations")) is of class (0,p−1)(0,p!-!1).
Applications of this theorem are discussed below.





(Note that Theorem 1-dimensional evolutionary differential-difference equations") in Section 2-dimensional evolutionary differential-difference equations")
generalizes and extends  [7, Theorem 1],
since  [7, Theorem 1] considers only
autonomous MLRs and gives only a sufficient condition for the described problem
to simplify a MLR by means of gauge transformations.)

- •


For each j=1,…,Nj=1,ldots,N, using the map 𝚫uj:𝔹d→𝕎dboldsymbol{Delta}^{u^{j}}colonmathbb{B}_{mathrm{d}}tomathbb{W}_{mathrm{d}} defined by ( 15-dimensional evolutionary differential-difference equations")),
in Theorem 2-dimensional evolutionary differential-difference equations") we obtain property ( 48-dimensional evolutionary differential-difference equations")), which essentially says the following:


when an invertible matrix M=M⁡(n,uℓ,…,λ)M=M(n,u_{ell},ldots,uplambda) is transformed to
M~=𝐒⁡(G)⋅M⋅G−1widetilde{M}={mathbf{S}}(G)cdot Mcdot G^{-1} by a gauge transformation G=G⁡(n,uℓ,…,λ)G=G(n,u_{ell},ldots,uplambda),
the corresponding matrix 𝚫uj​(M~)boldsymbol{Delta}^{u^{j}}big(widetilde{M}big) can be obtained
from 𝚫uj​(M)boldsymbol{Delta}^{u^{j}}(M) by conjugation as follows
𝚫uj​(M~)=𝐒⁡(G)⋅𝚫uj​(M)⋅𝐒​(G)−1boldsymbol{Delta}^{u^{j}}big(widetilde{M}big)={mathbf{S}}(G)cdotboldsymbol{Delta}^{u^{j}}(M)cdot{mathbf{S}}(G)^{-1}.





Note that in Remark 2-dimensional evolutionary differential-difference equations")
we discuss relations of our results on differential-difference MLRs
with the results of S.Yu. Sakovich  [21]
and M. Marvan  [17, 18]
on zero-curvature representations of partial differential equations.





Using Theorems 1-dimensional evolutionary differential-difference equations"), 2-dimensional evolutionary differential-difference equations") and Lemmas 1-dimensional evolutionary differential-difference equations")– 3-dimensional evolutionary differential-difference equations"),
we prove Theorem 3-dimensional evolutionary differential-difference equations") described below.
Further applications of Theorem 2-dimensional evolutionary differential-difference equations") are discussed in Remark 2-dimensional evolutionary differential-difference equations").

- •


Theorem 3-dimensional evolutionary differential-difference equations") says that a MLR (𝐌⁡(n,uℓ,…,λ),𝐔⁡(n,uℓ,…,λ))big(mathbf{M}(n,u_{ell},ldots,uplambda),,mathbf{U}(n,u_{ell},ldots,uplambda)big)
is gauge equivalent to a trivial MLR if and only if
one has 𝚫uj​(𝐌)=0boldsymbol{Delta}^{u^{j}}(mathbf{M})=0 for all j=1,…,Nj=1,ldots,N.
Therefore, a MLR (𝐌,𝐔)(mathbf{M},mathbf{U}) is not fake (in the sense of Definition 2-dimensional evolutionary differential-difference equations"))
if and only if there is j∈{1,…,N}jin{1,ldots,N} such that 𝚫uj​(𝐌)≠0boldsymbol{Delta}^{u^{j}}(mathbf{M})neq 0.





Note that the question “how to determine whether a given MLR is not fake”
was studied in  [8, Theorem 2] for a much smaller class of MLRs
(namely, for MLRs with 𝐒{mathbf{S}}-part of the form 𝐌⁡(u0,u1,u2,λ)mathbf{M}(u_{0},u_{1},u_{2},uplambda)), using a different method.


###### Remark 2.

Using Theorem 2-dimensional evolutionary differential-difference equations") and other properties of the maps ∇Mnabla_{M}, 𝚫uj,boldsymbol{Delta}^{u^{j}}
discussed in Definition 3-dimensional evolutionary differential-difference equations") and in Section 2-dimensional evolutionary differential-difference equations"),
in the preprint  [9] we introduce and study invariants
with respect to the action of gauge transformations on MLRs for
(1+1)-dimensional evolutionary differential-difference (semi-discrete) equations.
As explained in  [9],
our approach to gauge invariants for differential-difference (semi-discrete) MLRs
is inspired by the results of S.Yu. Sakovich  [21] and
M. Marvan  [17, 18] on
gauge transformations and gauge invariants
for zero-curvature representations (ZCRs) of partial differential equations.

Also, as discussed in  [9],
our Definition 3-dimensional evolutionary differential-difference equations") and Theorems 2-dimensional evolutionary differential-difference equations"), 3-dimensional evolutionary differential-difference equations") in the differential-difference setting
are inspired by the approaches of S.Yu. Sakovich  [21]
and M. Marvan  [17, 18] to ZCRs of partial differential equations.

###### Remark 3.

According to Definition 1-dimensional evolutionary differential-difference equations"),
in a MLR (𝐌,𝐔)(mathbf{M},mathbf{U}) for equation ( 1-dimensional evolutionary differential-difference equations"))
the matrix 𝐌=𝐌⁡(n,uℓ,…,λ)mathbf{M}=mathbf{M}(n,u_{ell},ldots,uplambda) may depend on nn,
on a finite number of the
dynamical variables uℓ=(uℓ1,…,uℓN)u_{ell}=(u^{1}_{ell},ldots,u^{N}_{ell}), ℓ∈ℤ,ellinmathbb{Z},
and a parameter λuplambda. For any fixed integers q1,…,qNq_{1},ldots,q_{N}, we can relabel

|     |     |     |     |
| --- | --- | --- | --- |
| (16) |  | uℓ1↦uℓ+q11,…,uℓN↦uℓ+qNN∀ℓ∈ℤ.displaystyle u^{1}_{ell},mapsto,u^{1}_{ell+q_{1}},,quadldots,quad,,quad u^{N}_{ell},mapsto,u^{N}_{ell+q_{N}}qquadquadforall,ellinmathbb{Z}. |  |

Relabeling ( 16-dimensional evolutionary differential-difference equations")) means that in equation ( 1-dimensional evolutionary differential-difference equations"))
we make the following invertible change of variables

|     |     |     |
| --- | --- | --- |
|  | u1​(n,t)↦u1​(n+q1,t),…,uN​(n,t)↦uN​(n+qN,t).displaystyle u^{1}(n,t),mapsto,u^{1}(n!+!q_{1},t),,quadldots,quad,,quad u^{N}(n,t),mapsto,u^{N}(n!+!q_{N},t). |  |

Applying a relabeling ( 16-dimensional evolutionary differential-difference equations")) with suitable fixed q1,…,qN∈ℤq_{1},ldots,q_{N}inmathbb{Z},
one can transform the matrix 𝐌mathbf{M} to the form
𝐌=𝐌⁡(n,u0,…,uk,λ)mathbf{M}=mathbf{M}(n,u_{0},ldots,u_{k},uplambda) for some k∈ℤ≥0kinmathbb{Z}_{geq 0}
(so that the MLR becomes of class (0,k)(0,k)).

In what follows, for any function w=w⁡(n,t)w=w(n,t) and each ℓ∈ℤellinmathbb{Z},
we denote by wℓw_{ell} the function wℓ​(n,t)=w⁡(n+ℓ,t)w_{ell}(n,t)=w(n+ell,t).
That is, wℓ=𝐒ℓ​(w)w_{ell}={mathbf{S}}^{ell}(w). In particular, w0=ww_{0}=w.

Now let a~,b~∈ℤ{tilde{{mathrm{a}}}},{tilde{{mathrm{b}}}}inmathbb{Z}, a~≤b~,{tilde{{mathrm{a}}}}leq{tilde{{mathrm{b}}}},
and consider another (1+1)-dimensional evolutionary differential-difference equation

|     |     |     |     |
| --- | --- | --- | --- |
| (17) |  | ∂t(u~)=𝔽~​(n,u~a~,u~a~+1,…,u~b~)displaystylepartial_{t}(tilde{u})=widetilde{mathbb{F}}(n,tilde{u}_{tilde{{mathrm{a}}}},tilde{u}_{{tilde{{mathrm{a}}}}+1},dots,tilde{u}_{tilde{{mathrm{b}}}}) |  |

for an NN-component vector-function u~=(u~1​(n,t),…,u~N​(n,t))tilde{u}=big(tilde{u}^{1}(n,t),dots,tilde{u}^{N}(n,t)big).
In the right-hand side of ( 17-dimensional evolutionary differential-difference equations")) one has
an NN-component vector-function 𝔽~=(𝔽~1,…,𝔽~N)widetilde{mathbb{F}}=big(widetilde{mathbb{F}}^{1},dots,widetilde{mathbb{F}}^{N}big).

###### Definition 5.

A _Miura-type transformation_ (MT) from equation ( 17-dimensional evolutionary differential-difference equations"))
to equation ( 1-dimensional evolutionary differential-difference equations")) is determined by an expression of the form

|     |     |     |     |
| --- | --- | --- | --- |
| (18) |  | u=Φ⁡(n,u~ℓ,…)displaystyle u=Phi(n,tilde{u}_{ell},dots) |  |

with the following requirements:

1. (1)


The right-hand side of ( 18-dimensional evolutionary differential-difference equations"))
is an NN-component vector-function Φ=(Φ1,…,ΦN)Phi=(Phi^{1},dots,Phi^{N})
which may depend on nn and on a finite number of the dynamical variables
u~ℓ=(u~ℓ1,…,u~ℓN)tilde{u}_{ell}=big(tilde{u}^{1}_{ell},dots,tilde{u}^{N}_{ell}big), ℓ∈ℤ,ellinmathbb{Z}.

2. (2)


If u~=u~​(n,t)tilde{u}=tilde{u}(n,t) satisfies equation ( 17-dimensional evolutionary differential-difference equations"))
then u=u⁡(n,t)u=u(n,t) determined by ( 18-dimensional evolutionary differential-difference equations")) satisfies equation ( 1-dimensional evolutionary differential-difference equations")).


More precisely, the second requirement means that we must have relations ( 20-dimensional evolutionary differential-difference equations")) explained below.
The components of the vector formula ( 18-dimensional evolutionary differential-difference equations")) are

|     |     |     |     |
| --- | --- | --- | --- |
| (19) |  | ui=Φi(n,u~ℓξ,…),i=1,…,N.displaystyle u^{i}=Phi^{i}big(n,tilde{u}^{xi}_{ell},dotsbig),qquadquad i=1,dots,N. |  |

Recall that ( 1-dimensional evolutionary differential-difference equations")) is equivalent to ( 3-dimensional evolutionary differential-difference equations")).
Substituting the right-hand side of ( 19-dimensional evolutionary differential-difference equations")) in place of uiu^{i} in ( 3-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (20) |  | 𝐃~t(Φi(n,u~ℓξ,…))=𝔽i(n,𝐒a(Φ),𝐒a+1(Φ),…,𝐒b(Φ)),i=1,…,N,displaystylewidetilde{mathbf{D}}_{t}big(Phi^{i}big(n,tilde{u}^{xi}_{ell},dotsbig)big)=mathbb{F}^{i}big(n,{mathbf{S}}^{mathrm{a}}(Phi),{mathbf{S}}^{{mathrm{a}}+1}(Phi),dots,{mathbf{S}}^{mathrm{b}}(Phi)big),qquadquad i=1,dots,N, |  |

which must be valid identically in the variables nn and u~ℓξtilde{u}^{xi}_{ell}.
Here 𝐃~twidetilde{mathbf{D}}_{t} is the total derivative operator corresponding to ( 17-dimensional evolutionary differential-difference equations")),
so that in the left-hand side of ( 20-dimensional evolutionary differential-difference equations")) we have
𝐃~t​(Φi​(n,u~ℓξ,…))=∑ℓ,ξ𝐒ℓ​(𝔽~ξ)⋅(∂Φi/∂u~ℓξ)widetilde{mathbf{D}}_{t}big(Phi^{i}big(n,tilde{u}^{xi}_{ell},dotsbig)big)=sum_{ell,xi}{mathbf{S}}^{ell}big(widetilde{mathbb{F}}^{xi}big)cdotbig({partialPhi^{i}}/{partialtilde{u}^{xi}_{ell}}big),
where 𝔽~ξ=𝔽~ξ​(n,u~a~,…,u~b~)widetilde{mathbb{F}}^{xi}=widetilde{mathbb{F}}^{xi}big(n,tilde{u}_{tilde{{mathrm{a}}}},dots,tilde{u}_{tilde{{mathrm{b}}}}big),
ξ=1,…,N,xi=1,ldots,N, are the components of the vector-function
𝔽~=(𝔽~1,…,𝔽~N)widetilde{mathbb{F}}=big(widetilde{mathbb{F}}^{1},dots,widetilde{mathbb{F}}^{N}big) from ( 17-dimensional evolutionary differential-difference equations")).

MTs for differential-difference equations
are a discrete analog of MTs for partial differential equations  [19].
MTs for partial differential equations are sometimes called _differential substitutions_.

###### Definition 6.

We consider MLRs for a given equation ( 1-dimensional evolutionary differential-difference equations")) imposed
on an NN-component vector-function u=(u1,…,uN)u=(u^{1},ldots,u^{N}).
We say that a MLR (𝐌,𝐔)(mathbf{M},mathbf{U}) is _uu-tame_
if its 𝐒{mathbf{S}}-part is of the form 𝐌=𝐌⁡(n,u0,λ)mathbf{M}=mathbf{M}(n,u_{0},uplambda).
That is, (𝐌,𝐔)(mathbf{M},mathbf{U}) is uu-tame if 𝐌mathbf{M} may depend only on nn,
u0=(u01,…,u0N)u_{0}=(u^{1}_{0},ldots,u^{N}_{0}), λuplambda.

###### Remark 4.

Consider a uu-tame MLR (𝐌⁡(n,u0,λ),𝐔⁡(n,uℓ,…,λ))big(mathbf{M}(n,u_{0},uplambda),,mathbf{U}(n,u_{ell},ldots,uplambda)big).
Let G=G⁡(n,λ)G=G(n,uplambda) be a gauge transformation such that GG may depend only on n,λn,,uplambda.
Then the corresponding gauge equivalent MLR

|     |     |     |
| --- | --- | --- |
|  | 𝐌ˇ=𝐒⁡(G)⋅𝐌⋅G−1,𝐔ˇ=𝐃t​(G)⋅G−1+G⋅𝐔⋅G−1displaystylecheck{mathbf{M}}={mathbf{S}}(G)cdotmathbf{M}cdot G^{-1},qquadquadcheck{mathbf{U}}=mathbf{D}_{t}(G)cdot G^{-1}+Gcdotmathbf{U}cdot G^{-1} |  |

is uu-tame as well, since its 𝐒{mathbf{S}}-part is
𝐌ˇ=𝐒⁡(G)⋅𝐌⋅G−1=G⁡(n+1,λ)⋅𝐌⁡(n,u0,λ)⋅G​(n,λ)−1check{mathbf{M}}={mathbf{S}}(G)cdotmathbf{M}cdot G^{-1}=G(n!+!1,uplambda)cdotmathbf{M}(n,u_{0},uplambda)cdot G(n,uplambda)^{-1}.

The following observation is well known:

when one makes a classification for some class
of integrable (partial differential, difference or differential-difference)
equations with two independent variables,
it is often possible to select a few basic equations (with some parameters)
such that all the other equations from the considered class can be derived from
the basic ones by means of MTs
(see, e.g.,  [2, 14, 23, 4, 5, 13, 12]
and references therein).
Also, it is well known that MTs often help to obtain conservation laws
and Bäcklund transformations for equations of various types
(see, e.g.,  [20, 22, 6, 12]).
Hence it is desirable to develop constructions of MTs.

In Section 3-dimensional evolutionary differential-difference equations") we demonstrate a technique to construct MTs
(including non-autonomous examples)
by means of MLRs and gauge transformations, using the following steps:

- •


Having a MLR, which is not necessarily uu-tame, we first try to bring it
to a uu-tame form, using a relabeling from Remark 3-dimensional evolutionary differential-difference equations") and
gauge transformations 𝐆⁡(n,uℓ,…,λ)mathbf{G}(n,u_{ell},ldots,uplambda) from Theorem 1-dimensional evolutionary differential-difference equations").

- •


Having obtained a uu-tame MLR
(𝐌⁡(n,u0,λ),𝐔⁡(n,uℓ,…,λ))big(mathbf{M}(n,u_{0},uplambda),,mathbf{U}(n,u_{ell},ldots,uplambda)big), we try to simplify it by means of
gauge transformations of the form G⁡(n,λ)G(n,uplambda) depending only on n,λn,,uplambda
in agreement with Remark 4-dimensional evolutionary differential-difference equations").

- •


After that, one can often derive MTs
by means of reductions of the auxiliary system ( 11-dimensional evolutionary differential-difference equations"))
corresponding to the obtained simplified MLR.
(Note that, in some examples in Section 3-dimensional evolutionary differential-difference equations"), we use u~tilde{u} instead of uu.)


This technique extends the methods of  [7, 8, 1],
since in  [7, 8, 1] only the autonomous case was considered.

As applications and illustrations of the presented general theory on MLRs,
we construct several new integrable equations (with new MLRs) connected
by new MTs to known integrable equations from  [11, 16].
Namely, in Section 3-dimensional evolutionary differential-difference equations") we obtain the following results.

- •


We consider the integrable
22-component (non-autonomous differential-difference) equation ( 67-dimensional evolutionary differential-difference equations")) with
the MLR ( 68-dimensional evolutionary differential-difference equations")), which were derived by
S. Konstantinou-Rizos, A.V. Mikhailov, P. Xenitidis  [11]
in a study of Darboux transformations for a Lax operator
of the (partial differential) nonlinear Schrödinger equation.
In ( 67-dimensional evolutionary differential-difference equations")), ( 68-dimensional evolutionary differential-difference equations")) one has an arbitrary function α⁡(n)upalpha(n).
(Equation ( 67-dimensional evolutionary differential-difference equations")) is given in  [11, page 7] in different notation,
using functions p⁡(n,x)p(n,x), q⁡(n,x)q(n,x), instead of u1​(n,t)u^{1}(n,t), u2​(n,t)u^{2}(n,t).)





We construct new integrable 22-component
(non-autonomous differential-difference) equations ( 85-dimensional evolutionary differential-difference equations")), ( 113-dimensional evolutionary differential-difference equations"))
and new MTs ( 89-dimensional evolutionary differential-difference equations")), ( 110-dimensional evolutionary differential-difference equations")).
The MT ( 89-dimensional evolutionary differential-difference equations")) is from ( 85-dimensional evolutionary differential-difference equations")) to ( 67-dimensional evolutionary differential-difference equations")),
while the MT ( 110-dimensional evolutionary differential-difference equations")) is from ( 113-dimensional evolutionary differential-difference equations")) to ( 85-dimensional evolutionary differential-difference equations")).
This implies that the composition of the MTs ( 89-dimensional evolutionary differential-difference equations")), ( 110-dimensional evolutionary differential-difference equations"))
gives a MT from ( 113-dimensional evolutionary differential-difference equations")) to ( 67-dimensional evolutionary differential-difference equations")).





In formulas ( 85-dimensional evolutionary differential-difference equations")), ( 113-dimensional evolutionary differential-difference equations")), ( 89-dimensional evolutionary differential-difference equations")), ( 110-dimensional evolutionary differential-difference equations")) we have arbitrary constants c,q∈ℂmathrm{c},mathrm{q}inmathbb{C}.
In ( 110-dimensional evolutionary differential-difference equations")), ( 113-dimensional evolutionary differential-difference equations")) we have also functions 𝕏mathbb{X}, 𝕐mathbb{Y} given by ( 109-dimensional evolutionary differential-difference equations")).
Furthermore, in ( 113-dimensional evolutionary differential-difference equations")) one has the function ℍmathbb{H} obtained by substituting ( 111-dimensional evolutionary differential-difference equations"))
in the right-hand side of the second component of ( 85-dimensional evolutionary differential-difference equations")).
(We do not present the explicit formula for ℍmathbb{H}, since it is rather cumbersome.)

- •


We consider also the integrable equation ( 114-dimensional evolutionary differential-difference equations")) derived by
E. Mansfield, G. Marí Beffa, Jing Ping Wang  [16, Section 5.1.1]
in a study of invariant time evolutions of polygons in the centro-affine plane.
As shown in  [16, Section 5.1.1], one has the MT ( 115-dimensional evolutionary differential-difference equations"))
from ( 114-dimensional evolutionary differential-difference equations")) to equation ( 116-dimensional evolutionary differential-difference equations")),
which is the Toda lattice in the Flaschka–Manakov coordinates  [3, 15].





We construct a new integrable 22-component equation ( 128-dimensional evolutionary differential-difference equations"))
and a new MT ( 126-dimensional evolutionary differential-difference equations")) from ( 128-dimensional evolutionary differential-difference equations")) to ( 114-dimensional evolutionary differential-difference equations")).
The composition of the MTs ( 115-dimensional evolutionary differential-difference equations")), ( 126-dimensional evolutionary differential-difference equations")) gives a MT from ( 128-dimensional evolutionary differential-difference equations"))
to the Toda lattice ( 116-dimensional evolutionary differential-difference equations")).

- •


Furthermore, we obtain several new MLRs:


the MLR ( 100-dimensional evolutionary differential-difference equations")) for equation ( 85-dimensional evolutionary differential-difference equations")), the MLR ( 120-dimensional evolutionary differential-difference equations")) for equation ( 114-dimensional evolutionary differential-difference equations")),
and the MLRs described in Remarks 6-dimensional evolutionary differential-difference equations"), 7-dimensional evolutionary differential-difference equations") for equations ( 113-dimensional evolutionary differential-difference equations")), ( 128-dimensional evolutionary differential-difference equations")).
Each of these MLRs has a parameter λ∈ℂuplambdainmathbb{C}.


The constructed equations ( 85-dimensional evolutionary differential-difference equations")), ( 113-dimensional evolutionary differential-difference equations")), ( 128-dimensional evolutionary differential-difference equations")) are integrable
for the following reasons:

- •


As explained above, equations ( 85-dimensional evolutionary differential-difference equations")), ( 113-dimensional evolutionary differential-difference equations")) are connected by MTs
to the integrable equation ( 67-dimensional evolutionary differential-difference equations")) from  [11],
while ( 128-dimensional evolutionary differential-difference equations")) is connected by MTs
to the integrable equation ( 114-dimensional evolutionary differential-difference equations")) from  [16, Section 5.1.1]
and to the Toda lattice ( 116-dimensional evolutionary differential-difference equations")).

- •


As discussed above, each of equations ( 85-dimensional evolutionary differential-difference equations")), ( 113-dimensional evolutionary differential-difference equations")), ( 128-dimensional evolutionary differential-difference equations"))
possesses a MLR with parameter λ∈ℂuplambdainmathbb{C}.


## 2. General results on differential-difference matrix Lax representations

Let d∈ℤ>0mathrm{d}inmathbb{Z}_{>0}.
In this section, all matrix-functions (including gauge transformations)
are of size d×dmathrm{d}timesmathrm{d}.

###### Lemma 1.

Let α,β∈ℤupalpha,upbetainmathbb{Z}, α≤β,upalphalequpbeta.
Let (𝐌⁡(n,uα,…,uβ,λ),𝐔⁡(n,uℓ,…,λ))big(mathbf{M}(n,u_{upalpha},dots,u_{upbeta},uplambda),,mathbf{U}(n,u_{ell},ldots,uplambda)big) be a MLR of class (α,β)(upalpha,upbeta).
Since the matrix 𝐌=𝐌⁡(n,uα,…,uβ,λ)mathbf{M}=mathbf{M}(n,u_{upalpha},dots,u_{upbeta},uplambda) is invertible,
we can consider the gauge transformations

|     |     |     |     |
| --- | --- | --- | --- |
| (21) |  | G:=𝐌,G˘:=𝐒−1​(𝐌−1)displaystylemathrm{G}:=mathbf{M},qquadquadbreve{mathrm{G}}:={mathbf{S}}^{-1}(mathbf{M}^{-1}) |  |

and the corresponding gauge equivalent MLRs

|     |     |     |     |
| --- | --- | --- | --- |
| (22) |  | 𝐌^:=𝐒⁡(G)⋅𝐌⋅G−1,𝐔^:=𝐃t​(G)⋅G−1+G⋅𝐔⋅G−1,displaystylewidehat{mathbf{M}}:={mathbf{S}}(mathrm{G})cdotmathbf{M}cdotmathrm{G}^{-1},qquadquadwidehat{mathbf{U}}:=mathbf{D}_{t}(mathrm{G})cdotmathrm{G}^{-1}+mathrm{G}cdotmathbf{U}cdotmathrm{G}^{-1}, |  |
| (23) |  | 𝐌˘:=𝐒⁡(G˘)⋅𝐌⋅G˘−1,𝐔˘:=𝐃t​(G˘)⋅G˘−1+G˘⋅𝐔⋅G˘−1.displaystylebreve{mathbf{M}}:={mathbf{S}}big(breve{mathrm{G}}big)cdotmathbf{M}cdotbreve{mathrm{G}}^{-1},qquadquadbreve{mathbf{U}}:=mathbf{D}_{t}big(breve{mathrm{G}}big)cdotbreve{mathrm{G}}^{-1}+breve{mathrm{G}}cdotmathbf{U}cdotbreve{mathrm{G}}^{-1}. |  |

Then we have

|     |     |     |     |
| --- | --- | --- | --- |
| (24) |  | 𝐌^=𝐒⁡(𝐌),𝐌˘=𝐒−1​(𝐌),displaystylewidehat{mathbf{M}}={mathbf{S}}(mathbf{M}),qquadquadbreve{mathbf{M}}={mathbf{S}}^{-1}(mathbf{M}), |  |

which implies that the MLR ( 22-dimensional evolutionary differential-difference equations")) is of class (α+1,β+1)(upalpha!+!1,upbeta!+!1), and
the MLR ( 23-dimensional evolutionary differential-difference equations")) is of class (α−1,β−1)(upalpha!-!1,upbeta!-!1).

Furthermore, for each q∈ℤqinmathbb{Z}, the considered MLR (𝐌,𝐔)(mathbf{M},mathbf{U}) of class (α,β)(upalpha,upbeta)
is gauge equivalent to some MLR of class (α+q,β+q)(upalpha!+!q,upbeta!+!q)
with 𝐒{mathbf{S}}-part equal to 𝐒q​(𝐌){mathbf{S}}^{q}(mathbf{M}).

###### Proof.

Substituting ( 21-dimensional evolutionary differential-difference equations")) in ( 22-dimensional evolutionary differential-difference equations")), ( 23-dimensional evolutionary differential-difference equations")), we get ( 24-dimensional evolutionary differential-difference equations")).
Therefore, the MLR (𝐌,𝐔)(mathbf{M},mathbf{U}) of class (α,β)(upalpha,upbeta) is gauge equivalent
to the MLR ( 22-dimensional evolutionary differential-difference equations")) of class (α+1,β+1)(upalpha!+!1,upbeta!+!1) with 𝐒{mathbf{S}}-part equal to 𝐒⁡(𝐌){mathbf{S}}(mathbf{M})
and is gauge equivalent to the MLR ( 23-dimensional evolutionary differential-difference equations")) of class (α−1,β−1)(upalpha!-!1,upbeta!-!1)
with 𝐒{mathbf{S}}-part equal to 𝐒−1​(𝐌){mathbf{S}}^{-1}(mathbf{M}).

Now, the last statement of the lemma can be proved easily by induction on qq.
∎

###### Remark 5.

In Theorem 1-dimensional evolutionary differential-difference equations") below,
we consider an invertible d×dmathrm{d}timesmathrm{d} matrix-function

|     |     |     |
| --- | --- | --- |
|  | 𝐌=𝐌⁡(n,u0,u1,…,up,λ)mathbf{M}=mathbf{M}(n,u_{0},u_{1},ldots,u_{p},uplambda) |  |

with p∈ℤ>0pinmathbb{Z}_{>0}, and we need to choose a constant vector a0∈ℂNa_{0}inmathbb{C}^{N} so that
the matrix 𝐌⁡(n,a0,u1,…,up,λ)mathbf{M}(n,a_{0},u_{1},ldots,u_{p},uplambda) is well defined and is invertible.
Here 𝐌⁡(n,a0,u1,…,up,λ)mathbf{M}(n,a_{0},u_{1},ldots,u_{p},uplambda) is obtained from 𝐌⁡(n,u0,u1,…,up,λ)mathbf{M}(n,u_{0},u_{1},ldots,u_{p},uplambda)
by substituting u0=a0u_{0}=a_{0}.
The term “invertible” is understood in the sense of Remark 1-dimensional evolutionary differential-difference equations").

For a given invertible matrix 𝐌⁡(n,u0,…,up,λ)mathbf{M}(n,u_{0},ldots,u_{p},uplambda),
such a vector a0∈ℂNa_{0}inmathbb{C}^{N} can be chosen as follows.
For i,j∈{1,…,d}i,jin{1,ldots,mathrm{d}} the (i,j)(i,j) entry of the matrix 𝐌mathbf{M}
is denoted by 𝐦i​j=𝐦i​j​(n,u0,…,up,λ)mathbf{m}^{ij}=mathbf{m}^{ij}(n,u_{0},ldots,u_{p},uplambda).
Since, according to Remark 1-dimensional evolutionary differential-difference equations"), 𝐦i​j​(n,u0,…,up,λ)mathbf{m}^{ij}(n,u_{0},ldots,u_{p},uplambda)
is assumed to be a rational function of n,uℓ=(uℓ1,…,uℓN)n,,u_{ell}=(u^{1}_{ell},ldots,u^{N}_{ell})
with coefficients in ℳ​ℰ​ℛ​(ℂ,λ)mathcal{M!E!R}(mathbb{C},uplambda), where ℳ​ℰ​ℛ​(ℂ,λ)mathcal{M!E!R}(mathbb{C},uplambda) is the field of meromorphic functions of λ∈ℂuplambdainmathbb{C}, we have

|     |     |     |
| --- | --- | --- |
|  | 𝐦i​j​(n,u0,…,up,λ)=fi​j​(n,u0,…,up,λ)gi​j​(n,u0,…,up,λ),i,j=1,…,d,displaystylemathbf{m}^{ij}(n,u_{0},ldots,u_{p},uplambda)=frac{f^{ij}(n,u_{0},ldots,u_{p},uplambda)}{g^{ij}(n,u_{0},ldots,u_{p},uplambda)},quadqquad i,j=1,ldots,mathrm{d}, |  |
|  | det(𝐌⁡(n,u0,…,up,λ))=P⁡(n,u0,…,up,λ)Q⁡(n,u0,…,up,λ),displaystyledetbig(mathbf{M}(n,u_{0},ldots,u_{p},uplambda)big)=frac{P(n,u_{0},ldots,u_{p},uplambda)}{Q(n,u_{0},ldots,u_{p},uplambda)}, |  |

where

- •


fi​j​(n,u0,…,up,λ)f^{ij}(n,u_{0},ldots,u_{p},uplambda), gi​j​(n,u0,…,up,λ),g^{ij}(n,u_{0},ldots,u_{p},uplambda),
P⁡(n,u0,…,up,λ),P(n,u_{0},ldots,u_{p},uplambda), Q⁡(n,u0,…,up,λ),Q(n,u_{0},ldots,u_{p},uplambda)
are some polynomials in the variables n,uℓ=(uℓ1,…,uℓN)n,,u_{ell}=(u^{1}_{ell},ldots,u^{N}_{ell}) with coefficients in ℳ​ℰ​ℛ​(ℂ,λ)mathcal{M!E!R}(mathbb{C},uplambda),

- •


each of the polynomials



|     |     |     |
| --- | --- | --- |
|  | gi​j​(n,u0,u1,…,up,λ),i,j=1,…,d,P⁡(n,u0,u1,…,up,λ),Q⁡(n,u0,u1,…,up,λ)displaystyle g^{ij}(n,u_{0},u_{1},ldots,u_{p},uplambda),qquad i,j=1,ldots,mathrm{d},qquad P(n,u_{0},u_{1},ldots,u_{p},uplambda),qquad Q(n,u_{0},u_{1},ldots,u_{p},uplambda) |  |



is not the zero polynomial.


Then there is an open dense subset W⊂ℂNWsubsetmathbb{C}^{N} such that
for any constant vector a0∈Wa_{0}in W each of the polynomials

|     |     |     |
| --- | --- | --- |
|  | gi​j​(n,a0,u1,…,up,λ),i,j=1,…,d,P⁡(n,a0,u1,…,up,λ),Q⁡(n,a0,u1,…,up,λ)displaystyle g^{ij}(n,a_{0},u_{1},ldots,u_{p},uplambda),qquad i,j=1,ldots,mathrm{d},qquad P(n,a_{0},u_{1},ldots,u_{p},uplambda),qquad Q(n,a_{0},u_{1},ldots,u_{p},uplambda) |  |

is not the zero polynomial (as a polynomial in n,uℓn,,u_{ell}).
This implies that for any a0∈Wa_{0}in W
the matrix 𝐌⁡(n,a0,u1,…,up,λ)mathbf{M}(n,a_{0},u_{1},ldots,u_{p},uplambda) is well defined and is invertible
(in the sense of Remark 1-dimensional evolutionary differential-difference equations")).

###### Theorem 1.

Let p∈ℤ>0pinmathbb{Z}_{>0}.
Consider an invertible d×dmathrm{d}timesmathrm{d} matrix-function 𝐌=𝐌⁡(n,u0,u1,…,up,λ)mathbf{M}=mathbf{M}(n,u_{0},u_{1},ldots,u_{p},uplambda).
The following two properties are equivalent.

- •


Property 1.
There is a gauge transformation 𝐆=𝐆⁡(n,uℓ,…,λ)mathbf{G}=mathbf{G}(n,u_{ell},ldots,uplambda) such that the matrix



|     |     |     |     |
| --- | --- | --- | --- |
| (25) |  | 𝐌^=𝐒⁡(𝐆)⋅𝐌⁡(n,u0,…,up,λ)⋅𝐆−1displaystylewidehat{mathbf{M}}={mathbf{S}}(mathbf{G})cdotmathbf{M}(n,u_{0},ldots,u_{p},uplambda)cdotmathbf{G}^{-1} |  |



is of the form



|     |     |     |     |
| --- | --- | --- | --- |
| (26) |  | 𝐌^=𝐌^​(n,u0,…,up−1,λ).displaystylewidehat{mathbf{M}}=widehat{mathbf{M}}(n,u_{0},ldots,u_{p-1},uplambda). |  |

- •


Property 2.
The matrix 𝐌=𝐌⁡(n,u0,u1,…,up,λ)mathbf{M}=mathbf{M}(n,u_{0},u_{1},ldots,u_{p},uplambda) obeys



|     |     |     |     |
| --- | --- | --- | --- |
| (27) |  | ∀i,j=1,…,N∂u0i(∂upj(𝐌)⋅𝐌−1)=0.displaystyleforall,i,j=1,ldots,Nqquadquadpartial_{u^{i}_{0}}big(partial_{u^{j}_{p}}(mathbf{M})cdotmathbf{M}^{-1}big)=0. |  |


Now suppose that 𝐌mathbf{M} satisfies ( 27-dimensional evolutionary differential-difference equations")).
Fix a constant vector a0=(a01,…,a0N)∈ℂNa_{0}=(a^{1}_{0},ldots,a^{N}_{0})inmathbb{C}^{N}
and consider the gauge transformation

|     |     |     |     |
| --- | --- | --- | --- |
| (28) |  | 𝐆⁡(n,u0,…,up−1,λ):=𝐒−1​(𝐌​(n,a0,u1,…,up,λ)−1),displaystylemathbf{G}(n,u_{0},ldots,u_{p-1},uplambda):={mathbf{S}}^{-1}big(mathbf{M}(n,a_{0},u_{1},ldots,u_{p},uplambda)^{-1}big), |  |

where 𝐌⁡(n,a0,u1,…,up,λ)mathbf{M}(n,a_{0},u_{1},ldots,u_{p},uplambda) is obtained
by substituting u0=a0u_{0}=a_{0} in 𝐌⁡(n,u0,u1,…,up,λ)mathbf{M}(n,u_{0},u_{1},ldots,u_{p},uplambda).
Here a vector a0∈ℂNa_{0}inmathbb{C}^{N} is chosen so that the matrix
𝐌⁡(n,a0,u1,…,up,λ)mathbf{M}(n,a_{0},u_{1},ldots,u_{p},uplambda) is well defined and is invertible.
(Remark 5-dimensional evolutionary differential-difference equations") explains how to choose such a vector.)

Then the matrix 𝐌^widehat{mathbf{M}} determined by ( 25-dimensional evolutionary differential-difference equations"))
is of the form 𝐌^=𝐌^​(n,u0,…,up−1,λ)widehat{mathbf{M}}=widehat{mathbf{M}}(n,u_{0},ldots,u_{p-1},uplambda), and we have

|     |     |     |     |
| --- | --- | --- | --- |
| (29) |  | 𝐌^=𝐒⁡(𝐆)⋅𝐌⁡(n,u0,u1,…,up,λ)⋅𝐆−1==𝐌​(n,a0,u1,…,up,λ)−1⋅𝐌⁡(n,u0,u1,…,up,λ)⋅𝐒−1​(𝐌⁡(n,a0,u1,…,up,λ)),widehat{mathbf{M}}={mathbf{S}}(mathbf{G})cdotmathbf{M}(n,u_{0},u_{1},ldots,u_{p},uplambda)cdotmathbf{G}^{-1}=<br>=mathbf{M}(n,a_{0},u_{1},ldots,u_{p},uplambda)^{-1}cdotmathbf{M}(n,u_{0},u_{1},ldots,u_{p},uplambda)cdot{mathbf{S}}^{-1}big(mathbf{M}(n,a_{0},u_{1},ldots,u_{p},uplambda)big), |  |

where the right-hand side of ( 29-dimensional evolutionary differential-difference equations")) does not depend on upu_{p}.

Furthermore, the above results imply the following additional statements:

Let (𝐌,𝐔)(mathbf{M},mathbf{U}) be a MLR of class (0,p)(0,p). Then ( 27-dimensional evolutionary differential-difference equations")) is a necessary and sufficient condition for
existence of a gauge transformation 𝐆=𝐆⁡(n,uℓ,…,λ)mathbf{G}=mathbf{G}(n,u_{ell},ldots,uplambda)
such that the corresponding gauge equivalent MLR

|     |     |     |     |
| --- | --- | --- | --- |
| (30) |  | 𝐌^=𝐒⁡(𝐆)⋅𝐌⋅𝐆−1,𝐔^=𝐃t​(𝐆)⋅𝐆−1+𝐆⋅𝐔⋅𝐆−1displaystylewidehat{mathbf{M}}={mathbf{S}}(mathbf{G})cdotmathbf{M}cdotmathbf{G}^{-1},qquadquadwidehat{mathbf{U}}=mathbf{D}_{t}(mathbf{G})cdotmathbf{G}^{-1}+mathbf{G}cdotmathbf{U}cdotmathbf{G}^{-1} |  |

is of class (0,p−1)(0,p!-!1). If
𝐌mathbf{M} satisfies ( 27-dimensional evolutionary differential-difference equations")) then one can take
the gauge transformation ( 28-dimensional evolutionary differential-difference equations")) for this purpose.

###### Proof.

Let us show that Property 1 implies Property 2.
Suppose that there is a gauge transformation 𝐆=𝐆⁡(n,uℓ,…,λ)mathbf{G}=mathbf{G}(n,u_{ell},ldots,uplambda)
such that the matrix ( 25-dimensional evolutionary differential-difference equations")) is of the form ( 26-dimensional evolutionary differential-difference equations")). We need to prove ( 27-dimensional evolutionary differential-difference equations")).

Let us first prove the following

|     |     |     |     |
| --- | --- | --- | --- |
| (31) |  | ∀q≥p∀j∈{1,…,N}∂uqj(𝐆)=0.displaystyleforall,qgeq pqquadforall,jin{1,ldots,N}qquadquadpartial_{u^{j}_{q}}(mathbf{G})=0. |  |

Suppose that ( 31-dimensional evolutionary differential-difference equations")) does not hold.
Let kk be the maximal integer such that
there is j∈{1,…,N}jin{1,ldots,N} satisfying ∂ukj(𝐆)≠0partial_{u^{j}_{k}}(mathbf{G})neq 0.
By our assumption, k≥pkgeq p, and one has ∂uk+1ȷ~(𝐆)=0partial_{u^{tilde{jmath}}_{k+1}}(mathbf{G})=0
for all ȷ~∈{1,…,N}tilde{jmath}in{1,ldots,N}. From ( 25-dimensional evolutionary differential-difference equations")), ( 26-dimensional evolutionary differential-difference equations")) we get

|     |     |     |     |
| --- | --- | --- | --- |
| (32) |  | 𝐒⁡(𝐆)=𝐌^​(n,u0,…,up−1,λ)⋅𝐆⋅(𝐌⁡(n,u0,…,up,λ))−1,displaystyle{mathbf{S}}(mathbf{G})=widehat{mathbf{M}}(n,u_{0},ldots,u_{p-1},uplambda)cdotmathbf{G}cdotbig(mathbf{M}(n,u_{0},ldots,u_{p},uplambda)big)^{-1}, |  |
| (33) |  | 𝐆=(𝐌^​(n,u0,…,up−1,λ))−1⋅𝐒⁡(𝐆)⋅𝐌⁡(n,u0,…,up,λ).displaystylemathbf{G}=big(widehat{mathbf{M}}(n,u_{0},ldots,u_{p-1},uplambda)big)^{-1}cdot{mathbf{S}}(mathbf{G})cdotmathbf{M}(n,u_{0},ldots,u_{p},uplambda). |  |

Using the rules ( 1-dimensional evolutionary differential-difference equations")) and the property ∂ukj(𝐆)≠0partial_{u^{j}_{k}}(mathbf{G})neq 0,
for the left-hand side of equation ( 32-dimensional evolutionary differential-difference equations"))
we derive ∂uk+1j(𝐒⁡(𝐆))=𝐒⁡(∂ukj(𝐆))≠0partial_{u^{j}_{k+1}}big({mathbf{S}}(mathbf{G})big)={mathbf{S}}big(partial_{u^{j}_{k}}(mathbf{G})big)neq 0.
On the other hand, since k≥pkgeq p and ∂uk+1j(𝐆)=0partial_{u^{j}_{k+1}}(mathbf{G})=0,
the right-hand side of equation ( 32-dimensional evolutionary differential-difference equations")) does not depend on uk+1ju^{j}_{k+1}.
The obtained contradiction allows us to conclude that ( 31-dimensional evolutionary differential-difference equations")) actually holds.

Now let us prove that

|     |     |     |     |
| --- | --- | --- | --- |
| (34) |  | ∀q≤−1∀j∈{1,…,N}∂uqj(𝐆)=0.displaystyleforall,qleq-1qquadforall,jin{1,ldots,N}qquadquadpartial_{u^{j}_{q}}(mathbf{G})=0. |  |

Suppose that ( 34-dimensional evolutionary differential-difference equations")) does not hold.
Let rr be the minimal integer such that
there is j∈{1,…,N}jin{1,ldots,N} satisfying ∂urj(𝐆)≠0partial_{u^{j}_{r}}(mathbf{G})neq 0.
By our assumption, r≤−1rleq-1, and one has ∂ur−1ȷ~(𝐆)=0partial_{u^{tilde{jmath}}_{r-1}}(mathbf{G})=0
for all ȷ~∈{1,…,N}tilde{jmath}in{1,ldots,N}.
Therefore, the right-hand side of ( 33-dimensional evolutionary differential-difference equations")) does not depend on urju^{j}_{r}.
On the other hand, for the left-hand side of ( 33-dimensional evolutionary differential-difference equations")) we have ∂urj(𝐆)≠0partial_{u^{j}_{r}}(mathbf{G})neq 0.
This contradiction shows that ( 34-dimensional evolutionary differential-difference equations")) actually holds.

The obtained properties ( 31-dimensional evolutionary differential-difference equations")), ( 34-dimensional evolutionary differential-difference equations")) imply that 𝐆mathbf{G} is of the form
𝐆=𝐆⁡(n,u0,…,up−1,λ)mathbf{G}=mathbf{G}(n,u_{0},dots,u_{p-1},uplambda). Then from ( 25-dimensional evolutionary differential-difference equations")) one gets

|     |     |     |     |
| --- | --- | --- | --- |
| (35) |  | 𝐌=𝐒⁡(𝐆​(n,u0,…,up−1,λ)−1)⋅𝐌^​(n,u0,…,up−1,λ)⋅𝐆⁡(n,u0,…,up−1,λ).displaystylemathbf{M}={mathbf{S}}big(mathbf{G}(n,u_{0},dots,u_{p-1},uplambda)^{-1}big)cdotwidehat{mathbf{M}}(n,u_{0},dots,u_{p-1},uplambda)cdotmathbf{G}(n,u_{0},dots,u_{p-1},uplambda). |  |

Using ( 35-dimensional evolutionary differential-difference equations")), for each j=1,…,Nj=1,dots,N we derive

|     |     |     |     |
| --- | --- | --- | --- |
| (36) |  | ∂upj(𝐌)⋅𝐌−1=∂upj(𝐒⁡(𝐆​(n,u0,…,up−1,λ)−1)⋅𝐌^​(n,u0,…,up−1,λ)⋅𝐆⁡(n,u0,…,up−1,λ))⋅𝐌−1==𝐒⁡(∂up−1j(𝐆​(n,u0,…,up−1,λ)−1))⋅𝐌^⋅𝐆⋅(𝐒⁡(𝐆−1)⋅𝐌^⋅𝐆)−1==𝐒⁡(∂up−1j(𝐆​(n,u0,…,up−1,λ)−1))⋅𝐌^⋅𝐆⋅𝐆−1⋅𝐌^−1⋅(𝐒⁡(𝐆−1))−1==𝐒⁡(∂up−1j(𝐆​(n,u0,…,up−1,λ)−1))⋅𝐒⁡(𝐆⁡(n,u0,…,up−1,λ)).partial_{u^{j}_{p}}(mathbf{M})cdotmathbf{M}^{-1}=partial_{u^{j}_{p}}Big({mathbf{S}}big(mathbf{G}(n,u_{0},dots,u_{p-1},uplambda)^{-1}big)cdotwidehat{mathbf{M}}(n,u_{0},dots,u_{p-1},uplambda)cdotmathbf{G}(n,u_{0},dots,u_{p-1},uplambda)Big)cdotmathbf{M}^{-1}=<br>={mathbf{S}}Big(partial_{u^{j}_{p-1}}big(mathbf{G}(n,u_{0},dots,u_{p-1},uplambda)^{-1}big)Big)cdotwidehat{mathbf{M}}cdotmathbf{G}cdotbig({mathbf{S}}(mathbf{G}^{-1})cdotwidehat{mathbf{M}}cdotmathbf{G}big)^{-1}=<br>={mathbf{S}}Big(partial_{u^{j}_{p-1}}big(mathbf{G}(n,u_{0},dots,u_{p-1},uplambda)^{-1}big)Big)cdotwidehat{mathbf{M}}cdotmathbf{G}cdotmathbf{G}^{-1}cdotwidehat{mathbf{M}}^{-1}cdotbig({mathbf{S}}(mathbf{G}^{-1})big)^{-1}=<br>={mathbf{S}}Big(partial_{u^{j}_{p-1}}big(mathbf{G}(n,u_{0},dots,u_{p-1},uplambda)^{-1}big)Big)cdot{mathbf{S}}big(mathbf{G}(n,u_{0},dots,u_{p-1},uplambda)big). |  |

The rules ( 1-dimensional evolutionary differential-difference equations")) imply that the right-hand side of ( 36-dimensional evolutionary differential-difference equations")) does not depend on u0iu^{i}_{0}
for any i=1,…,Ni=1,dots,N. This yields ( 27-dimensional evolutionary differential-difference equations")).

Now let us prove that Property 2 implies Property 1,
along with the statement about the gauge transformation ( 28-dimensional evolutionary differential-difference equations")).

Suppose that 𝐌=𝐌⁡(n,u0,u1,…,up,λ)mathbf{M}=mathbf{M}(n,u_{0},u_{1},dots,u_{p},uplambda) satisfies ( 27-dimensional evolutionary differential-difference equations")).
According to Remark 5-dimensional evolutionary differential-difference equations"),
we can choose a constant vector a0∈ℂNa_{0}inmathbb{C}^{N} such that
𝐌​(n,a0,u1,…,up,λ)−1mathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)^{-1} is well defined.
This allows us to consider the gauge transformation ( 28-dimensional evolutionary differential-difference equations"))
and the corresponding matrix 𝐌^widehat{mathbf{M}} determined by ( 25-dimensional evolutionary differential-difference equations")).
Since for ( 28-dimensional evolutionary differential-difference equations")) one has

|     |     |     |
| --- | --- | --- |
|  | 𝐒⁡(𝐆)=𝐌​(n,a0,u1,…,up,λ)−1,𝐆−1=𝐒−1​(𝐌⁡(n,a0,u1,…,up,λ)),displaystyle{mathbf{S}}(mathbf{G})=mathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)^{-1},qquadquadmathbf{G}^{-1}={mathbf{S}}^{-1}big(mathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)big), |  |

we obtain ( 29-dimensional evolutionary differential-difference equations")), which implies that the matrix-function 𝐌^widehat{mathbf{M}}
may depend only on n,u0,u1,…,up,λn,u_{0},u_{1},dots,u_{p},uplambda.
In order to show that actually 𝐌^widehat{mathbf{M}} is of the form ( 26-dimensional evolutionary differential-difference equations")), it remains to prove that

|     |     |     |     |
| --- | --- | --- | --- |
| (37) |  | ∂upj(𝐌^)=0∀j=1,…,N.displaystylepartial_{u^{j}_{p}}big(widehat{mathbf{M}}big)=0qquadquadforall,j=1,dots,N. |  |

Let j∈{1,…,N}jin{1,dots,N}. Set
𝐇:=𝐆−1​(n,u0,…,up−1,λ)=𝐒−1​(𝐌⁡(n,a0,u1,…,up,λ))mathbf{H}:=mathbf{G}^{-1}(n,u_{0},dots,u_{p-1},uplambda)={mathbf{S}}^{-1}big(mathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)big).
Using ( 29-dimensional evolutionary differential-difference equations")) and the property ∂upj(𝐇)=0partial_{u^{j}_{p}}(mathbf{H})=0, we get

|     |     |     |     |
| --- | --- | --- | --- |
| (38) |  | ∂upj(𝐌^)=∂upj(𝐌​(n,a0,u1,…,up,λ)−1⋅𝐌⁡(n,u0,u1,…,up,λ))⋅𝐇==(∂upj(𝐌​(n,a0,u1,…,up,λ)−1)⋅𝐌⁡(n,u0,u1,…,up,λ)+CLOSE+𝐌(n,a0,u1,…,up,λ)−1⋅∂upj(𝐌(n,u0,u1,…,up,λ)))⋅𝐇==(−𝐌(n,a0,u1,…,up,λ)−1⋅∂upj(𝐌(n,a0,u1,…,up,λ)⋅𝐌(n,a0,u1,…,up,λ)−1⋅⋅𝐌(n,u0,u1,…,up,λ)+𝐌(n,a0,u1,…,up,λ)−1⋅∂upj(𝐌(n,u0,u1,…,up,λ)))⋅𝐇==𝐌(n,a0,u1,…,up,λ)−1⋅(−∂upj(𝐌(n,a0,u1,…,up,λ))⋅𝐌(n,a0,u1,…,up,λ)−1++∂upj(𝐌(n,u0,u1,…,up,λ))⋅𝐌(n,u0,u1,…,up,λ)−1)⋅𝐌(n,u0,u1,…,up,λ)⋅𝐇==𝐌​(n,a0,u1,…,up,λ)−1⋅𝐋j​(n,u0,u1,…,up,λ)⋅𝐌⁡(n,u0,u1,…,up,λ)⋅𝐇,partial_{u^{j}_{p}}big(widehat{mathbf{M}}big)=partial_{u^{j}_{p}}Big(mathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)^{-1}cdotmathbf{M}(n,u_{0},u_{1},dots,u_{p},uplambda)Big)cdotmathbf{H}=<br>=Big(partial_{u^{j}_{p}}big(mathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)^{-1}big)cdotmathbf{M}(n,u_{0},u_{1},dots,u_{p},uplambda)+<br>+mathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)^{-1}cdotpartial_{u^{j}_{p}}big(mathbf{M}(n,u_{0},u_{1},dots,u_{p},uplambda)big)Big)cdotmathbf{H}=<br>=Big(-mathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)^{-1}cdotpartial_{u^{j}_{p}}big(mathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambdabig)cdotmathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)^{-1}cdot<br>cdotmathbf{M}(n,u_{0},u_{1},dots,u_{p},uplambda)+mathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)^{-1}cdotpartial_{u^{j}_{p}}big(mathbf{M}(n,u_{0},u_{1},dots,u_{p},uplambda)big)Big)cdotmathbf{H}=<br>=mathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)^{-1}cdotBig(-partial_{u^{j}_{p}}big(mathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)big)cdotmathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)^{-1}+<br>+partial_{u^{j}_{p}}big(mathbf{M}(n,u_{0},u_{1},dots,u_{p},uplambda)big)cdotmathbf{M}(n,u_{0},u_{1},dots,u_{p},uplambda)^{-1}Big)cdotmathbf{M}(n,u_{0},u_{1},dots,u_{p},uplambda)cdotmathbf{H}=<br>=mathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)^{-1}cdotmathbf{L}^{j}(n,u_{0},u_{1},dots,u_{p},uplambda)cdotmathbf{M}(n,u_{0},u_{1},dots,u_{p},uplambda)cdotmathbf{H}, |  |

where

|     |     |     |     |
| --- | --- | --- | --- |
| (39) |  | 𝐋j(n,u0,u1,…,up,λ)=−∂upj(𝐌(n,a0,u1,…,up,λ))⋅𝐌(n,a0,u1,…,up,λ)−1++∂upj(𝐌(n,u0,u1,…,up,λ))⋅𝐌(n,u0,u1,…,up,λ)−1.mathbf{L}^{j}(n,u_{0},u_{1},dots,u_{p},uplambda)=-partial_{u^{j}_{p}}big(mathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)big)cdotmathbf{M}(n,a_{0},u_{1},dots,u_{p},uplambda)^{-1}+<br>+partial_{u^{j}_{p}}big(mathbf{M}(n,u_{0},u_{1},dots,u_{p},uplambda)big)cdotmathbf{M}(n,u_{0},u_{1},dots,u_{p},uplambda)^{-1}. |  |

From ( 39-dimensional evolutionary differential-difference equations")) and ( 27-dimensional evolutionary differential-difference equations")) it follows that

|     |     |     |     |
| --- | --- | --- | --- |
|  | ∂u0i(𝐋j​(n,u0,u1,…,up,λ))=∂u0i(∂upj(𝐌⁡(n,u0,u1,…,up,λ))⋅𝐌​(n,u0,u1,…,up,λ)−1)=0∀i=1,…,N,displaystylebegin{gathered}partial_{u^{i}_{0}}big(mathbf{L}^{j}(n,u_{0},u_{1},dots,u_{p},uplambda)big)=partial_{u^{i}_{0}}Big(partial_{u^{j}_{p}}big(mathbf{M}(n,u_{0},u_{1},dots,u_{p},uplambda)big)cdotmathbf{M}(n,u_{0},u_{1},dots,u_{p},uplambda)^{-1}Big)=0<br>forall,i=1,dots,N,end{gathered} |  |
| (42) |  | 𝐋j​(n,a0,u1,…,up,λ)=0.displaystylemathbf{L}^{j}(n,a_{0},u_{1},dots,u_{p},uplambda)=0. |  |

Since, according to Remark 1-dimensional evolutionary differential-difference equations"), the entries of
the matrix-function 𝐋j​(n,u0,u1,…,up,λ)mathbf{L}^{j}(n,u_{0},u_{1},dots,u_{p},uplambda)
depend rationally on n∈ℤninmathbb{Z}, u0,u1,…,up∈ℂNu_{0},u_{1},dots,u_{p}inmathbb{C}^{N}
and meromorphically on λ∈ℂuplambdainmathbb{C},
equations ( 2-dimensional evolutionary differential-difference equations")), ( 42-dimensional evolutionary differential-difference equations")) imply that the matrix-function
𝐋j​(n,u0,u1,…,up,λ)mathbf{L}^{j}(n,u_{0},u_{1},dots,u_{p},uplambda) is identically zero.

Substituting 𝐋j​(n,u0,u1,…,up,λ)=0mathbf{L}^{j}(n,u_{0},u_{1},dots,u_{p},uplambda)=0 in ( 38-dimensional evolutionary differential-difference equations")), one gets ( 37-dimensional evolutionary differential-difference equations")).
Therefore, the matrix-function 𝐌^widehat{mathbf{M}} given by ( 25-dimensional evolutionary differential-difference equations")), ( 29-dimensional evolutionary differential-difference equations")) is of the form ( 26-dimensional evolutionary differential-difference equations")),
and the right-hand side of ( 29-dimensional evolutionary differential-difference equations")) does not depend on upu_{p}.

Clearly, the obtained results immediately imply the additional statements (about MLRs) in the end of the theorem.
∎

In what follows, we use the notation and formulas from Definition 3-dimensional evolutionary differential-difference equations").

###### Lemma 2.

Let M=M⁡(n,uℓ,…,λ)M=M(n,u_{ell},ldots,uplambda), 𝐆=𝐆⁡(n,uℓ,…,λ),mathbf{G}=mathbf{G}(n,u_{ell},ldots,uplambda)
be invertible d×dmathrm{d}timesmathrm{d} matrix-functions
and P=P⁡(n,uℓ,…,λ)P=P(n,u_{ell},ldots,uplambda) be an arbitrary d×dmathrm{d}timesmathrm{d} matrix-function.
Set M~=𝐒⁡(𝐆)⋅M⋅𝐆−1widetilde{M}={mathbf{S}}(mathbf{G})cdot Mcdotmathbf{G}^{-1}.
Then

|     |     |     |     |
| --- | --- | --- | --- |
| (43) |  | ∇M~k(𝐒⁡(𝐆)⋅P⋅𝐒​(𝐆)−1)=𝐒⁡(𝐆)⋅∇Mk(P)⋅𝐒​(𝐆)−1∀k∈ℤ.displaystylenabla_{widetilde{M}}^{k}big({mathbf{S}}(mathbf{G})cdot Pcdot{mathbf{S}}(mathbf{G})^{-1}big)={mathbf{S}}(mathbf{G})cdotnabla^{k}_{M}(P)cdot{mathbf{S}}(mathbf{G})^{-1}qquadquadforall,{k}inmathbb{Z}. |  |

###### Proof.

We have

|     |     |     |     |
| --- | --- | --- | --- |
| (44) |  | M~=𝐒⁡(𝐆)⋅M⋅𝐆−1,M~−1=𝐆⋅M−1⋅𝐒​(𝐆)−1,𝐒⁡(𝐆−1)=𝐒​(𝐆)−1.displaystylewidetilde{M}={mathbf{S}}(mathbf{G})cdot Mcdotmathbf{G}^{-1},qquadquadwidetilde{M}^{-1}=mathbf{G}cdot M^{-1}cdot{mathbf{S}}(mathbf{G})^{-1},qquadquad{mathbf{S}}(mathbf{G}^{-1})={mathbf{S}}(mathbf{G})^{-1}. |  |

Using ( 13-dimensional evolutionary differential-difference equations")) and ( 44-dimensional evolutionary differential-difference equations")), one gets

|     |     |     |     |
| --- | --- | --- | --- |
| (45) |  | ∇M~(𝐒⁡(𝐆)⋅P⋅𝐒​(𝐆)−1)=𝐒⁡(M~−1​𝐒​(𝐆)​P​𝐒​(𝐆)−1​M~)=𝐒⁡(𝐆​M−1​𝐒​(𝐆)−1​𝐒​(𝐆)​P​𝐒​(𝐆)−1​𝐒​(𝐆)​M​𝐆−1)==𝐒⁡(𝐆​M−1​P​M​𝐆−1)=𝐒⁡(𝐆)​𝐒​(M−1​P​M)​𝐒​(𝐆−1)=𝐒⁡(𝐆)​∇M(P)​𝐒​(𝐆)−1.nabla_{widetilde{M}}big({mathbf{S}}(mathbf{G})cdot Pcdot{mathbf{S}}(mathbf{G})^{-1}big)={mathbf{S}}big(widetilde{M}^{-1}{mathbf{S}}(mathbf{G})P{mathbf{S}}(mathbf{G})^{-1}widetilde{M}big)={mathbf{S}}big(mathbf{G}M^{-1}{mathbf{S}}(mathbf{G})^{-1}{mathbf{S}}(mathbf{G})P{mathbf{S}}(mathbf{G})^{-1}{mathbf{S}}(mathbf{G})Mmathbf{G}^{-1}big)=<br>={mathbf{S}}(mathbf{G}M^{-1}PMmathbf{G}^{-1})={mathbf{S}}(mathbf{G}){mathbf{S}}(M^{-1}PM){mathbf{S}}(mathbf{G}^{-1})={mathbf{S}}(mathbf{G})nabla_{M}(P){mathbf{S}}(mathbf{G})^{-1}. |  |

Thus we have

|     |     |     |     |
| --- | --- | --- | --- |
| (46) |  | ∇M~(𝐒⁡(𝐆)⋅P⋅𝐒​(𝐆)−1)=𝐒⁡(𝐆)⋅∇M(P)⋅𝐒​(𝐆)−1.displaystylenabla_{widetilde{M}}big({mathbf{S}}(mathbf{G})cdot Pcdot{mathbf{S}}(mathbf{G})^{-1}big)={mathbf{S}}(mathbf{G})cdotnabla_{M}(P)cdot{mathbf{S}}(mathbf{G})^{-1}. |  |

Similarly, using ( 14-dimensional evolutionary differential-difference equations")) and ( 44-dimensional evolutionary differential-difference equations")), one obtains

|     |     |     |     |
| --- | --- | --- | --- |
| (47) |  | ∇M~−1(𝐒⁡(𝐆)⋅P⋅𝐒​(𝐆)−1)=𝐒⁡(𝐆)⋅∇M−1(P)⋅𝐒​(𝐆)−1.displaystylenabla_{widetilde{M}}^{-1}big({mathbf{S}}(mathbf{G})cdot Pcdot{mathbf{S}}(mathbf{G})^{-1}big)={mathbf{S}}(mathbf{G})cdotnabla_{M}^{-1}(P)cdot{mathbf{S}}(mathbf{G})^{-1}. |  |

Using ( 46-dimensional evolutionary differential-difference equations")) and ( 47-dimensional evolutionary differential-difference equations")), one can prove ( 43-dimensional evolutionary differential-difference equations")) by induction on k{k}.
∎

###### Theorem 2.

For any invertible d×dmathrm{d}timesmathrm{d} matrix-functions
M=M⁡(n,uℓ,…,λ)M=M(n,u_{ell},ldots,uplambda) and G=G⁡(n,uℓ,…,λ)G=G(n,u_{ell},ldots,uplambda), we have

|     |     |     |     |
| --- | --- | --- | --- |
| (48) |  | 𝚫uj​(𝐒⁡(G)⋅M⋅G−1)=𝐒⁡(G)⋅𝚫uj​(M)⋅𝐒​(G)−1∀j=1,…,N.displaystyleboldsymbol{Delta}^{u^{j}}big({mathbf{S}}(G)cdot Mcdot G^{-1}big)={mathbf{S}}(G)cdotboldsymbol{Delta}^{u^{j}}(M)cdot{mathbf{S}}(G)^{-1}qquadquadforall,j=1,ldots,N. |  |

###### Proof.

Set M~=𝐒⁡(G)​M​G−1widetilde{M}={mathbf{S}}(G)MG^{-1}.
To prove ( 48-dimensional evolutionary differential-difference equations")), we need to show that
𝚫uj​(M~)=𝐒⁡(G)⋅𝚫uj​(M)⋅𝐒​(G)−1boldsymbol{Delta}^{u^{j}}big(widetilde{M}big)={mathbf{S}}(G)cdotboldsymbol{Delta}^{u^{j}}(M)cdot{mathbf{S}}(G)^{-1}.

Using the relations

|     |     |     |
| --- | --- | --- |
|  | M~−1=GM−1𝐒(G)−1,∂uℓj(G−1)=−G−1∂uℓj(G)G−1,∂uℓj(𝐒(G))=𝐒(∂uℓ−1j(G)),displaystylewidetilde{M}^{-1}=GM^{-1}{mathbf{S}}(G)^{-1},qquadpartial_{u^{j}_{ell}}(G^{-1})=-G^{-1}partial_{u^{j}_{ell}}(G)G^{-1},qquadpartial_{u^{j}_{ell}}big({mathbf{S}}(G)big)={mathbf{S}}big(partial_{u^{j}_{ell-1}}(G)big), |  |
|  | 𝐒⁡(∂uℓ−1j(G))=𝐒⁡(G)​𝐒​(G−1​∂uℓ−1j(G)),M​G−1​∂uℓj(G)​M−1=∇M−1(𝐒⁡(G−1​∂uℓj(G)))displaystyle{mathbf{S}}big(partial_{u^{j}_{ell-1}}(G)big)={mathbf{S}}(G){mathbf{S}}big(G^{-1}partial_{u^{j}_{ell-1}}(G)big),qquad MG^{-1}partial_{u^{j}_{ell}}(G)M^{-1}=nabla_{M}^{-1}big({mathbf{S}}big(G^{-1}partial_{u^{j}_{ell}}(G)big)big) |  |

and Lemma 2-dimensional evolutionary differential-difference equations"), one can prove
𝚫uj​(M~)=𝐒⁡(G)⋅𝚫uj​(M)⋅𝐒​(G)−1boldsymbol{Delta}^{u^{j}}big(widetilde{M}big)={mathbf{S}}(G)cdotboldsymbol{Delta}^{u^{j}}(M)cdot{mathbf{S}}(G)^{-1}
by straightforward (but rather lengthy) computations,
which are presented in the preprint  [9].
∎

###### Lemma 3.

Let p∈ℤ≥0pinmathbb{Z}_{geq 0}.
Consider an invertible d×dmathrm{d}timesmathrm{d} matrix-function M=M⁡(n,u0,…,up,λ)M=M(n,u_{0},ldots,u_{p},uplambda).
Suppose that

|     |     |     |     |
| --- | --- | --- | --- |
| (49) |  | 𝚫uj​(M)=0∀j=1,…,N.displaystyleboldsymbol{Delta}^{u^{j}}(M)=0qquadquadforall,j=1,ldots,N. |  |

Then there is a gauge transformation 𝐆=𝐆⁡(n,u0,…,up−1,λ)mathbf{G}=mathbf{G}(n,u_{0},ldots,u_{p-1},uplambda)
such that the matrix

|     |     |     |     |
| --- | --- | --- | --- |
| (50) |  | M˘=𝐒⁡(𝐆)⋅M⁡(n,u0,…,up,λ)⋅𝐆−1displaystylebreve{M}={mathbf{S}}(mathbf{G})cdot M(n,u_{0},ldots,u_{p},uplambda)cdotmathbf{G}^{-1} |  |

obeys

|     |     |     |     |
| --- | --- | --- | --- |
| (51) |  | ∂uℓj(M˘)=0∀ℓ∈ℤ,∀j=1,…,N.displaystylepartial_{u^{j}_{ell}}(breve{M})=0qquadquadforall,ellinmathbb{Z},qquadforall,j=1,ldots,N. |  |

###### Proof.

We prove this by induction on p∈ℤ≥0pinmathbb{Z}_{geq 0}. First, consider the case p=0p=0, where M=M⁡(n,u0,λ)M=M(n,u_{0},uplambda).
According to ( 15-dimensional evolutionary differential-difference equations")), for M=M⁡(n,u0,λ)M=M(n,u_{0},uplambda) we have 𝚫uj​(M)=∂u0j(M)⋅M−1boldsymbol{Delta}^{u^{j}}(M)=partial_{u^{j}_{0}}(M)cdot M^{-1}.
Then ( 49-dimensional evolutionary differential-difference equations")) implies that MM is of the form M=M⁡(n,λ)M=M(n,uplambda).
We take 𝐆=𝐈𝐝mathbf{G}=mathbf{Id}, where 𝐈𝐝mathbf{Id} is the identity matrix of size d×dmathrm{d}timesmathrm{d}.
Then M˘=M⁡(n,λ)breve{M}=M(n,uplambda) satisfies ( 50-dimensional evolutionary differential-difference equations")), ( 51-dimensional evolutionary differential-difference equations")).

To make the induction step, we consider a number k∈ℤ≥0kinmathbb{Z}_{geq 0} such that
the statement of Lemma 3-dimensional evolutionary differential-difference equations") is valid for p=kp=k.
We need to prove the statement in the case p=k+1p=k+1, where M=M⁡(n,u0,…,uk+1,λ)M=M(n,u_{0},ldots,u_{k+1},uplambda).
According to ( 15-dimensional evolutionary differential-difference equations")), for such MM equation ( 49-dimensional evolutionary differential-difference equations")) reads
∑ℓ=0,…,k+1∇M−ℓ(∂uℓj(M)​M−1)=0sum_{ell=0,ldots,k+1}nabla_{M}^{-ell}big(partial_{u^{j}_{ell}}(M)M^{-1}big)=0, which yields

|     |     |     |     |
| --- | --- | --- | --- |
| (52) |  | ∇M−(k+1)(∂uk+1j(M)M−1)=−∑ℓ=0,…,k∇M−ℓ(∂uℓj(M)M−1)∀j=1,…,N.displaystylenabla_{M}^{-(k+1)}big(partial_{u^{j}_{k+1}}(M)M^{-1}big)=-sum_{ell=0,ldots,k}nabla_{M}^{-ell}big(partial_{u^{j}_{ell}}(M)M^{-1}big)qquadquadforall,j=1,ldots,N. |  |

Applying the operator ∇Mk+1nabla_{M}^{k+1} to equation ( 52-dimensional evolutionary differential-difference equations")) and using ( 13-dimensional evolutionary differential-difference equations")), we derive

|     |     |     |     |
| --- | --- | --- | --- |
| (53) |  | ∂uk+1j(M)⋅M−1=−∑ℓ=0,…,k∇Mk+1−ℓ(∂uℓj(M)M−1)=−∇M(∑ℓ=0,…,k∇Mk−ℓ(∂uℓj(M)M−1))==−𝐒(M−1(∑ℓ=0,…,k∇Mk−ℓ(∂uℓj(M)M−1))M)∀j=1,…,N.partial_{u^{j}_{k+1}}(M)cdot M^{-1}=-sum_{ell=0,ldots,k}nabla_{M}^{k+1-ell}big(partial_{u^{j}_{ell}}(M)M^{-1}big)=-nabla_{M}Big(sum_{ell=0,ldots,k}nabla_{M}^{k-ell}big(partial_{u^{j}_{ell}}(M)M^{-1}big)Big)=<br>=-{mathbf{S}}Big(M^{-1}Big(sum_{ell=0,ldots,k}nabla_{M}^{k-ell}big(partial_{u^{j}_{ell}}(M)M^{-1}big)Big)MBig)qquadquadforall,j=1,ldots,N. |  |

Let Y=M−1​(∑ℓ=0,…,k∇Mk−ℓ(∂uℓj(M)​M−1))​MY=M^{-1}Big(sum_{ell=0,ldots,k}nabla_{M}^{k-ell}big(partial_{u^{j}_{ell}}(M)M^{-1}big)Big)M.
The formulas M=M⁡(n,u0,…,uk+1,λ)M=M(n,u_{0},ldots,u_{k+1},uplambda) and ( 13-dimensional evolutionary differential-difference equations"))
imply that YY does not depend on uaiu^{i}_{a} for any a<0a<0 and i=1,…,Ni=1,ldots,N.
Since the right-hand side of ( 53-dimensional evolutionary differential-difference equations")) is equal to −𝐒⁡(Y)-{mathbf{S}}(Y),
it does not depend on u0iu^{i}_{0}, i=1,…,N,i=1,ldots,N.
Therefore, from ( 53-dimensional evolutionary differential-difference equations")) we get

|     |     |     |     |
| --- | --- | --- | --- |
| (54) |  | ∀i,j=1,…,N∂u0i(∂uk+1j(M⁡(n,u0,…,uk+1,λ))⋅M​(n,u0,…,uk+1,λ)−1)=0.displaystyleforall,i,j=1,ldots,Nqquadquadpartial_{u^{i}_{0}}Big(partial_{u^{j}_{k+1}}big(M(n,u_{0},ldots,u_{k+1},uplambda)big)cdot M(n,u_{0},ldots,u_{k+1},uplambda)^{-1}Big)=0. |  |

By Theorem 1-dimensional evolutionary differential-difference equations") in the case p=k+1p=k+1,
from property ( 54-dimensional evolutionary differential-difference equations")) it follows that there is a gauge transformation G=G⁡(n,u0,…,uk,λ)G=G(n,u_{0},ldots,u_{k},uplambda)
such that the matrix

|     |     |     |     |
| --- | --- | --- | --- |
| (55) |  | M^=𝐒⁡(G)⋅M⁡(n,u0,…,uk+1,λ)⋅G−1displaystylewidehat{M}={mathbf{S}}(G)cdot M(n,u_{0},ldots,u_{k+1},uplambda)cdot G^{-1} |  |

is of the form M^=M^​(n,u0,…,uk,λ)widehat{M}=widehat{M}(n,u_{0},ldots,u_{k},uplambda).
Using ( 48-dimensional evolutionary differential-difference equations")) and ( 49-dimensional evolutionary differential-difference equations")), one obtains

|     |     |     |     |
| --- | --- | --- | --- |
| (56) |  | 𝚫uj​(M^)=𝚫uj​(𝐒⁡(G)⋅M⋅G−1)=𝐒⁡(G)⋅𝚫uj​(M)⋅𝐒​(G)−1=0∀j=1,…,N.displaystyleboldsymbol{Delta}^{u^{j}}big(widehat{M}big)=boldsymbol{Delta}^{u^{j}}big({mathbf{S}}(G)cdot Mcdot G^{-1}big)={mathbf{S}}(G)cdotboldsymbol{Delta}^{u^{j}}(M)cdot{mathbf{S}}(G)^{-1}=0qquadquadforall,j=1,ldots,N. |  |

Since, by the induction assumption, the statement of Lemma 3-dimensional evolutionary differential-difference equations") is valid for p=kp=k,
equation ( 56-dimensional evolutionary differential-difference equations")) for M^=M^​(n,u0,…,uk,λ)widehat{M}=widehat{M}(n,u_{0},ldots,u_{k},uplambda) implies that
there is a gauge transformation 𝔾=𝔾⁡(n,u0,…,uk−1,λ)mathbb{G}=mathbb{G}(n,u_{0},ldots,u_{k-1},uplambda) such that the matrix

|     |     |     |     |
| --- | --- | --- | --- |
| (57) |  | M˘=𝐒⁡(𝔾)⋅M^​(n,u0,…,uk,λ)⋅𝔾−1displaystylebreve{M}={mathbf{S}}(mathbb{G})cdotwidehat{M}(n,u_{0},ldots,u_{k},uplambda)cdotmathbb{G}^{-1} |  |

obeys ( 51-dimensional evolutionary differential-difference equations")). Now we set

|     |     |     |     |
| --- | --- | --- | --- |
| (58) |  | 𝐆⁡(n,u0,…,uk,λ)=𝔾⁡(n,u0,…,uk−1,λ)⋅G⁡(n,u0,…,uk,λ).displaystylemathbf{G}(n,u_{0},ldots,u_{k},uplambda)=mathbb{G}(n,u_{0},ldots,u_{k-1},uplambda)cdot G(n,u_{0},ldots,u_{k},uplambda). |  |

Formulas ( 55-dimensional evolutionary differential-difference equations")), ( 57-dimensional evolutionary differential-difference equations")), ( 58-dimensional evolutionary differential-difference equations")) imply that M˘breve{M} satisfies ( 50-dimensional evolutionary differential-difference equations"))
with p=k+1p=k+1. Furthermore, as said above, M˘breve{M} obeys ( 51-dimensional evolutionary differential-difference equations")).
Therefore, we have proved the statement of Lemma 3-dimensional evolutionary differential-difference equations") in the case p=k+1p=k+1.
∎

###### Theorem 3.

A MLR (𝐌⁡(n,uℓ,…,λ),𝐔⁡(n,uℓ,…,λ))big(mathbf{M}(n,u_{ell},ldots,uplambda),,mathbf{U}(n,u_{ell},ldots,uplambda)big)
is gauge equivalent to a trivial MLR if and only if
𝐌=𝐌⁡(n,uℓ,…,λ)mathbf{M}=mathbf{M}(n,u_{ell},ldots,uplambda) satisfies

|     |     |     |     |
| --- | --- | --- | --- |
| (59) |  | 𝚫uj​(𝐌)=0∀j=1,…,N,displaystyleboldsymbol{Delta}^{u^{j}}(mathbf{M})=0qquadquadforall,j=1,ldots,N, |  |

where 𝚫uj​(𝐌)boldsymbol{Delta}^{u^{j}}(mathbf{M}) is determined by formula ( 15-dimensional evolutionary differential-difference equations")).

###### Proof.

Suppose that a MLR (𝐌⁡(n,uℓ,…,λ),𝐔⁡(n,uℓ,…,λ))big(mathbf{M}(n,u_{ell},ldots,uplambda),,mathbf{U}(n,u_{ell},ldots,uplambda)big)
is gauge equivalent to a trivial MLR. This means that there is a
gauge transformation 𝐆=𝐆⁡(n,uℓ,…,λ)mathbf{G}=mathbf{G}(n,u_{ell},ldots,uplambda) such that the matrix

|     |     |     |     |
| --- | --- | --- | --- |
| (60) |  | 𝐌^=𝐒⁡(𝐆)⋅𝐌⁡(n,uℓ,…,λ)⋅𝐆−1displaystylewidehat{mathbf{M}}={mathbf{S}}(mathbf{G})cdotmathbf{M}(n,u_{ell},ldots,uplambda)cdotmathbf{G}^{-1} |  |

obeys

|     |     |     |     |
| --- | --- | --- | --- |
| (61) |  | ∂uℓj(𝐌^)=0∀ℓ∈ℤ,∀j=1,…,N.displaystylepartial_{u^{j}_{ell}}(widehat{mathbf{M}})=0qquadquadforall,ellinmathbb{Z},qquadforall,j=1,ldots,N. |  |

According to ( 15-dimensional evolutionary differential-difference equations")), property ( 61-dimensional evolutionary differential-difference equations")) yields

|     |     |     |     |
| --- | --- | --- | --- |
| (62) |  | 𝚫uj​(𝐌^)=0∀j=1,…,N.displaystyleboldsymbol{Delta}^{u^{j}}(widehat{mathbf{M}})=0qquadquadforall,j=1,ldots,N. |  |

From ( 60-dimensional evolutionary differential-difference equations")) one derives

|     |     |     |     |
| --- | --- | --- | --- |
| (63) |  | 𝐌=𝐒​(𝐆)−1⋅𝐌^⋅𝐆=𝐒⁡(𝐆−1)⋅𝐌^⋅𝐆.displaystylemathbf{M}={mathbf{S}}(mathbf{G})^{-1}cdotwidehat{mathbf{M}}cdotmathbf{G}={mathbf{S}}big(mathbf{G}^{-1}big)cdotwidehat{mathbf{M}}cdotmathbf{G}. |  |

Using ( 63-dimensional evolutionary differential-difference equations")), ( 62-dimensional evolutionary differential-difference equations")) and property ( 48-dimensional evolutionary differential-difference equations")) for M=𝐌^M=widehat{mathbf{M}} and G=𝐆−1G=mathbf{G}^{-1}, we get

|     |     |     |
| --- | --- | --- |
|  | 𝚫uj​(𝐌)=𝚫uj​(𝐒⁡(𝐆−1)⋅𝐌^⋅𝐆)=𝐒⁡(𝐆−1)⋅𝚫uj​(𝐌^)⋅𝐒⁡(𝐆)=0∀j=1,…,N,displaystyleboldsymbol{Delta}^{u^{j}}(mathbf{M})=boldsymbol{Delta}^{u^{j}}big({mathbf{S}}big(mathbf{G}^{-1}big)cdotwidehat{mathbf{M}}cdotmathbf{G}big)={mathbf{S}}big(mathbf{G}^{-1}big)cdotboldsymbol{Delta}^{u^{j}}(widehat{mathbf{M}})cdot{mathbf{S}}(mathbf{G})=0qquadquadforall,j=1,ldots,N, |  |

thus we obtain ( 59-dimensional evolutionary differential-difference equations")).

Now, conversely, consider a MLR (𝐌,𝐔)(mathbf{M},mathbf{U})
with 𝐒{mathbf{S}}-part 𝐌=𝐌⁡(n,uℓ,…,λ)mathbf{M}=mathbf{M}(n,u_{ell},ldots,uplambda) satisfying ( 59-dimensional evolutionary differential-difference equations")).
We need to prove that this MLR is gauge equivalent to a trivial MLR.

The rules ( 1-dimensional evolutionary differential-difference equations")) imply that there are q∈ℤqinmathbb{Z} and p∈ℤ≥0pinmathbb{Z}_{geq 0} such that
the matrix-function 𝐌~=𝐒q​(𝐌)widetilde{mathbf{M}}={mathbf{S}}^{q}(mathbf{M}) may depend only on n,u0,…,up,λn,u_{0},ldots,u_{p},uplambda.
By Lemma 1-dimensional evolutionary differential-difference equations"), the MLR (𝐌,𝐔)(mathbf{M},mathbf{U})
is gauge equivalent to some MLR (𝐌~,𝐔~)big(widetilde{mathbf{M}},widetilde{mathbf{U}}big) with 𝐒{mathbf{S}}-part equal to
𝐒q​(𝐌)=𝐌~​(n,u0,…,up,λ){mathbf{S}}^{q}(mathbf{M})=widetilde{mathbf{M}}(n,u_{0},ldots,u_{p},uplambda).
Therefore, there is a gauge transformation G=G⁡(n,uℓ,…,λ)G=G(n,u_{ell},ldots,uplambda)
such that 𝐌~=𝐒⁡(G)⋅𝐌⋅G−1widetilde{mathbf{M}}={mathbf{S}}(G)cdotmathbf{M}cdot G^{-1}.
Using ( 48-dimensional evolutionary differential-difference equations")) and ( 59-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (64) |  | 𝚫uj​(𝐌~)=𝚫uj​(𝐒⁡(G)⋅𝐌⋅G−1)=𝐒⁡(G)⋅𝚫uj​(𝐌)⋅𝐒​(G)−1=0∀j=1,…,N.displaystyleboldsymbol{Delta}^{u^{j}}big(widetilde{mathbf{M}}big)=boldsymbol{Delta}^{u^{j}}big({mathbf{S}}(G)cdotmathbf{M}cdot G^{-1}big)={mathbf{S}}(G)cdotboldsymbol{Delta}^{u^{j}}(mathbf{M})cdot{mathbf{S}}(G)^{-1}=0qquadquadforall,j=1,ldots,N. |  |

By Lemma 3-dimensional evolutionary differential-difference equations") for 𝐌~=𝐌~​(n,u0,…,up,λ)widetilde{mathbf{M}}=widetilde{mathbf{M}}(n,u_{0},ldots,u_{p},uplambda),
property ( 64-dimensional evolutionary differential-difference equations")) implies that there is a gauge transformation 𝐆=𝐆⁡(u0,…,up−1,λ)mathbf{G}=mathbf{G}(u_{0},ldots,u_{p-1},uplambda)
such that the matrix M˘=𝐒⁡(𝐆)⋅𝐌~⋅𝐆−1breve{M}={mathbf{S}}(mathbf{G})cdotwidetilde{mathbf{M}}cdotmathbf{G}^{-1} obeys ( 51-dimensional evolutionary differential-difference equations")).

The relations M˘=𝐒⁡(𝐆)⋅𝐌~⋅𝐆−1breve{M}={mathbf{S}}(mathbf{G})cdotwidetilde{mathbf{M}}cdotmathbf{G}^{-1} and
𝐌~=𝐒⁡(G)⋅𝐌⋅G−1widetilde{mathbf{M}}={mathbf{S}}(G)cdotmathbf{M}cdot G^{-1} yield
M˘=𝐒⁡(𝐆​G)⋅𝐌⋅(𝐆​G)−1breve{M}={mathbf{S}}(mathbf{G}G)cdotmathbf{M}cdot(mathbf{G}G)^{-1}.
Therefore, applying the gauge transformation 𝐆​Gmathbf{G}G to the MLR (𝐌,𝐔)(mathbf{M},mathbf{U}),
we get a MLR with 𝐒{mathbf{S}}-part M˘breve{M} obeying ( 51-dimensional evolutionary differential-difference equations")).
Hence (𝐌,𝐔)(mathbf{M},mathbf{U}) is gauge equivalent to a trivial MLR.
∎

## 3. Miura-type transformations and matrix Lax representations

The following lemma is proved easily by a direct calculation.

###### Lemma 4.

Suppose that matrices

|     |     |     |     |
| --- | --- | --- | --- |
| (65) |  | 𝐌=𝐌⁡(n,uℓ,…,λ),𝐔=𝐔⁡(n,uℓ,…,λ)displaystylemathbf{M}=mathbf{M}(n,u_{ell},ldots,uplambda),qquadquadmathbf{U}=mathbf{U}(n,u_{ell},ldots,uplambda) |  |

form a MLR for equation ( 1-dimensional evolutionary differential-difference equations")).
Let ( 18-dimensional evolutionary differential-difference equations")) be a MT from equation ( 17-dimensional evolutionary differential-difference equations")) to equation ( 1-dimensional evolutionary differential-difference equations")).
As explained in Definition 5-dimensional evolutionary differential-difference equations"), in formula ( 18-dimensional evolutionary differential-difference equations")) one has
an NN-component vector-function Φ=(Φ1,…,ΦN)Phi=(Phi^{1},dots,Phi^{N})
which may depend on nn and on a finite number of the dynamical variables
u~ℓ=(u~ℓ1,…,u~ℓN)tilde{u}_{ell}=(tilde{u}^{1}_{ell},dots,tilde{u}^{N}_{ell}), ℓ∈ℤ,ellinmathbb{Z}.

Motivated by formula ( 18-dimensional evolutionary differential-difference equations")), we substitute uℓ=𝐒ℓ​(Φ)u_{ell}={mathbf{S}}^{ell}(Phi), ℓ∈ℤ,ellinmathbb{Z},
in ( 65-dimensional evolutionary differential-difference equations")) and obtain the matrices

|     |     |     |     |
| --- | --- | --- | --- |
| (66) |  | 𝐌=𝐌⁡(n,𝐒ℓ​(Φ),…,λ),𝐔=𝐔⁡(n,𝐒ℓ​(Φ),…,λ).displaystylemathbf{M}=mathbf{M}big(n,{mathbf{S}}^{ell}(Phi),ldots,uplambdabig),qquadquadmathbf{U}=mathbf{U}big(n,{mathbf{S}}^{ell}(Phi),ldots,uplambdabig). |  |

Then ( 66-dimensional evolutionary differential-difference equations")) is a MLR for equation ( 17-dimensional evolutionary differential-difference equations")).

### 3.1. Non-autonomous examples

The following 22-component non-autonomous equation
was introduced in  [11, page 7] in a study of Darboux transformations

|     |     |     |     |
| --- | --- | --- | --- |
| (67) |  | {∂t(u1)=2​(u12​(u01)2+α⁡(n)​u01−u11),∂t(u2)=2​(u−12−u−11​(u02)2−α⁡(n−1)​u02).displaystyleleft{begin{aligned} partial_{t}(u^{1})&=2big(u^{2}_{1}(u^{1}_{0})^{2}+upalpha(n)u^{1}_{0}-u^{1}_{1}big),<br>partial_{t}(u^{2})&=2big(u^{2}_{-1}-u^{1}_{-1}(u^{2}_{0})^{2}-upalpha(n-1)u^{2}_{0}big).end{aligned}right. |  |

Here α⁡(n)upalpha(n) is an arbitrary function.
(This equation is given in  [11, page 7] in different notation,
using functions p⁡(n,x)p(n,x), q⁡(n,x)q(n,x), instead of u1​(n,t)u^{1}(n,t), u2​(n,t)u^{2}(n,t).)

The results of  [11] imply
that the following matrices form a MLR for ( 67-dimensional evolutionary differential-difference equations"))

|     |     |     |     |
| --- | --- | --- | --- |
| (68) |  | 𝐌~=(λ+α⁡(n)+u01​u12u01u121),𝐔~=(−λ−2​u01−2​u02λ).displaystylewidetilde{mathbf{M}}=begin{pmatrix}{uplambda}+upalpha(n)+u^{1}_{0}u^{2}_{1}&u^{1}_{0}<br>u^{2}_{1}&1<br>end{pmatrix},qquadquadwidetilde{mathbf{U}}=begin{pmatrix}-{uplambda}&-2u^{1}_{0}<br>-2u^{2}_{0}&{uplambda}<br>end{pmatrix}. |  |

The MLR ( 68-dimensional evolutionary differential-difference equations")) is not uu-tame (in the sense of Definition 6-dimensional evolutionary differential-difference equations")).
In order to obtain a uu-tame MLR, we relabel

|     |     |     |     |
| --- | --- | --- | --- |
| (69) |  | uℓ1↦uℓ1,uℓ2↦uℓ−12∀ℓ∈ℤ.displaystyle u^{1}_{ell},mapsto,u^{1}_{ell},qquadquad u^{2}_{ell},mapsto,u^{2}_{ell-1}qquadquadforall,ellinmathbb{Z}. |  |

This means that we make the following invertible change of variables

|     |     |     |
| --- | --- | --- |
|  | u1​(n,t)↦u1​(n,t),u2​(n,t)↦u2​(n−1,t).displaystyle u^{1}(n,t),mapsto,u^{1}(n,t),qquad u^{2}(n,t),mapsto,u^{2}(n!-!1,t). |  |

Applying the (invertible) change ( 69-dimensional evolutionary differential-difference equations")) to ( 67-dimensional evolutionary differential-difference equations")), ( 68-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (70) |  | {∂t(u1)=2​(u02​(u01)2+α⁡(n)​u01−u11),∂t(u−12)=2​(u−22−u−11​(u−12)2−α⁡(n−1)​u−12),displaystyleleft{begin{aligned} partial_{t}(u^{1})&=2big(u^{2}_{0}(u^{1}_{0})^{2}+upalpha(n)u^{1}_{0}-u^{1}_{1}big),<br>partial_{t}(u^{2}_{-1})&=2big(u^{2}_{-2}-u^{1}_{-1}(u^{2}_{-1})^{2}-upalpha(n-1)u^{2}_{-1}big),end{aligned}right. |  |
| (71) |  | 𝐌˘=(λ+α⁡(n)+u01​u02u01u021),𝐔˘=(−λ−2​u01−2​u−12λ).displaystylebreve{mathbf{M}}=begin{pmatrix}{uplambda}+upalpha(n)+u^{1}_{0}u^{2}_{0}&u^{1}_{0}<br>u^{2}_{0}&1<br>end{pmatrix},qquadquadbreve{mathbf{U}}=begin{pmatrix}-{uplambda}&-2u^{1}_{0}<br>-2u^{2}_{-1}&{uplambda}<br>end{pmatrix}. |  |

Applying the (invertible) operator 𝐒{mathbf{S}} to the second component in ( 70-dimensional evolutionary differential-difference equations")), one obtains

|     |     |     |     |
| --- | --- | --- | --- |
| (72) |  | {∂t(u1)=2​(u02​(u01)2+α⁡(n)​u01−u11),∂t(u2)=2​(u−12−u01​(u02)2−α⁡(n)​u02).displaystyleleft{begin{aligned} partial_{t}(u^{1})&=2big(u^{2}_{0}(u^{1}_{0})^{2}+upalpha(n)u^{1}_{0}-u^{1}_{1}big),<br>partial_{t}(u^{2})&=2big(u^{2}_{-1}-u^{1}_{0}(u^{2}_{0})^{2}-upalpha(n)u^{2}_{0}big).end{aligned}right. |  |

Since ( 68-dimensional evolutionary differential-difference equations")) is a MLR for equation ( 67-dimensional evolutionary differential-difference equations")),
the described way of deriving ( 71-dimensional evolutionary differential-difference equations")), ( 72-dimensional evolutionary differential-difference equations"))
from ( 68-dimensional evolutionary differential-difference equations")), ( 67-dimensional evolutionary differential-difference equations")) implies that ( 71-dimensional evolutionary differential-difference equations")) is a MLR for equation ( 72-dimensional evolutionary differential-difference equations")).
Furthermore, equation ( 72-dimensional evolutionary differential-difference equations")) is equivalent to equation ( 67-dimensional evolutionary differential-difference equations")),
as ( 72-dimensional evolutionary differential-difference equations")) is obtained from ( 67-dimensional evolutionary differential-difference equations")) by means of invertible operations, as described above.
The MLR ( 71-dimensional evolutionary differential-difference equations")) is uu-tame, and this will allow us to construct a MT, as shown below.

Fix a constant c∈ℂmathrm{c}inmathbb{C}.
In what follows, we use the matrices ( 71-dimensional evolutionary differential-difference equations")) with λuplambda replaced by cmathrm{c}.
According to Definition 1-dimensional evolutionary differential-difference equations"), since the matrices ( 71-dimensional evolutionary differential-difference equations"))
form a MLR for equation ( 72-dimensional evolutionary differential-difference equations")), we can consider the auxiliary system

|     |     |     |     |
| --- | --- | --- | --- |
| (73) |  | 𝐒⁡(Ψ)=(c+α⁡(n)+u01​u02u01u021)⋅Ψ,∂t(Ψ)=(−c−2​u01−2​u−12c)⋅Ψ,displaystyle{mathbf{S}}(Psi)=begin{pmatrix}{mathrm{c}}+upalpha(n)+u^{1}_{0}u^{2}_{0}&u^{1}_{0}<br>u^{2}_{0}&1<br>end{pmatrix}cdotPsi,qquadquadpartial_{t}(Psi)=begin{pmatrix}-{mathrm{c}}&-2u^{1}_{0}<br>-2u^{2}_{-1}&{mathrm{c}}<br>end{pmatrix}cdotPsi, |  |

which is compatible modulo equation ( 72-dimensional evolutionary differential-difference equations")).
Here Ψ=Ψ⁡(n,t)Psi=Psi(n,t) is an invertible 2×22times 2 matrix
whose elements we denote by ψi​j=ψi​j​(n,t)uppsi^{ij}=uppsi^{ij}(n,t), i,j=1,2,i,j=1,2.

Substituting Ψ=(ψ11ψ12ψ21ψ22)Psi=begin{pmatrix}uppsi^{11}&uppsi^{12}
uppsi^{21}&uppsi^{22}end{pmatrix} in ( 73-dimensional evolutionary differential-difference equations")) and considering the first columns
in the matrix equations ( 73-dimensional evolutionary differential-difference equations")), one gets

|     |     |     |     |
| --- | --- | --- | --- |
| (74) |  | 𝐒⁡(ψ11)=(c+α⁡(n)+u01​u02)​ψ11+u01​ψ21,𝐒⁡(ψ21)=u02​ψ11+ψ21,displaystyle{mathbf{S}}(uppsi^{11})=({mathrm{c}}+upalpha(n)+u^{1}_{0}u^{2}_{0})uppsi^{11}+u^{1}_{0}uppsi^{21},qquadquad{mathbf{S}}(uppsi^{21})=u^{2}_{0}uppsi^{11}+uppsi^{21}, |  |
| (75) |  | ∂t(ψ11)=−c​ψ11−2​u01​ψ21,∂t(ψ21)=−2​u−12​ψ11+c​ψ21.displaystylepartial_{t}(uppsi^{11})=-{mathrm{c}}uppsi^{11}-2u^{1}_{0}uppsi^{21},qquadquadpartial_{t}(uppsi^{21})=-2u^{2}_{-1}uppsi^{11}+{mathrm{c}}uppsi^{21}. |  |

Now we employ the standard idea to consider the function w=ψ11/ψ21w={uppsi^{11}}/{uppsi^{21}}.
Using ( 74-dimensional evolutionary differential-difference equations")), ( 75-dimensional evolutionary differential-difference equations")), we derive

|     |     |     |     |
| --- | --- | --- | --- |
| (76) |  | 𝐒⁡(w)=𝐒⁡(ψ11)𝐒⁡(ψ21)=(c+α⁡(n)+u01​u02)​ψ11+u01​ψ21u02​ψ11+ψ21==(c+α⁡(n)+u01​u02)​(ψ11/ψ21)+u01u02​(ψ11/ψ21)+1=(c+α⁡(n)+u01​u02)​w+u01u02​w+1,displaystylebegin{split}{mathbf{S}}(w)&=frac{{mathbf{S}}(uppsi^{11})}{{mathbf{S}}(uppsi^{21})}=frac{({mathrm{c}}+upalpha(n)+u^{1}_{0}u^{2}_{0})uppsi^{11}+u^{1}_{0}uppsi^{21}}{u^{2}_{0}uppsi^{11}+uppsi^{21}}=<br>&=frac{({mathrm{c}}+upalpha(n)+u^{1}_{0}u^{2}_{0})(uppsi^{11}/uppsi^{21})+u^{1}_{0}}{u^{2}_{0}(uppsi^{11}/{uppsi^{21}})+1}=frac{({mathrm{c}}+upalpha(n)+u^{1}_{0}u^{2}_{0})w+u^{1}_{0}}{u^{2}_{0}w+1},end{split} |  |
| (77) |  | ∂t(w)=∂t(ψ11ψ21)=∂t(ψ11)ψ21−ψ11​∂t(ψ21)(ψ21)2=−c​ψ11−2​u01​ψ21ψ21−ψ11​(−2​u−12​ψ11+c​ψ21)(ψ21)2==−c​ψ11ψ21−2​u01+2​u−12​(ψ11ψ21)2−c​ψ11ψ21=2​u−12​(w)2−2​c​w−2​u01.displaystylebegin{split}partial_{t}(w)&=partial_{t}Big(frac{uppsi^{11}}{uppsi^{21}}Big)=frac{partial_{t}(uppsi^{11})}{uppsi^{21}}-frac{uppsi^{11}partial_{t}(uppsi^{21})}{(uppsi^{21})^{2}}=frac{-{mathrm{c}}uppsi^{11}-2u^{1}_{0}uppsi^{21}}{uppsi^{21}}-frac{uppsi^{11}(-2u^{2}_{-1}uppsi^{11}+{mathrm{c}}uppsi^{21})}{(uppsi^{21})^{2}}=<br>&=-{mathrm{c}}frac{uppsi^{11}}{uppsi^{21}}-2u^{1}_{0}+2u^{2}_{-1}Big(frac{uppsi^{11}}{uppsi^{21}}Big)^{2}-{mathrm{c}}frac{uppsi^{11}}{uppsi^{21}}=2u^{2}_{-1}(w)^{2}-2{mathrm{c}}w-2u^{1}_{0}.end{split} |  |

From ( 76-dimensional evolutionary differential-difference equations")), ( 77-dimensional evolutionary differential-difference equations")) one gets

|     |     |     |     |
| --- | --- | --- | --- |
| (78) |  | 𝐒⁡(w)=(c+α⁡(n)+u01​u02)​w+u01u02​w+1,displaystyle{mathbf{S}}(w)=frac{({mathrm{c}}+upalpha(n)+u^{1}_{0}u^{2}_{0})w+u^{1}_{0}}{u^{2}_{0}w+1}, |  |
| (79) |  | ∂t(w)=2​u−12​(w)2−2​c​w−2​u01.displaystylepartial_{t}(w)=2u^{2}_{-1}(w)^{2}-2{mathrm{c}}w-2u^{1}_{0}. |  |

We have derived equations ( 78-dimensional evolutionary differential-difference equations")), ( 79-dimensional evolutionary differential-difference equations")) from system ( 73-dimensional evolutionary differential-difference equations")),
which is compatible modulo equation ( 72-dimensional evolutionary differential-difference equations")).
The described procedure of deriving ( 78-dimensional evolutionary differential-difference equations")), ( 79-dimensional evolutionary differential-difference equations")) implies that
system ( 78-dimensional evolutionary differential-difference equations")), ( 79-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( 72-dimensional evolutionary differential-difference equations")) as well.

From ( 78-dimensional evolutionary differential-difference equations")) one obtains

|     |     |     |     |
| --- | --- | --- | --- |
| (80) |  | u1=u01=𝐒⁡(w)​u02​w+𝐒⁡(w)−c​w−α⁡(n)​ww​u02+1.displaystyle u^{1}=u^{1}_{0}=frac{{mathbf{S}}(w)u^{2}_{0}w+{mathbf{S}}(w)-{mathrm{c}}w-upalpha(n)w}{wu^{2}_{0}+1}. |  |

We set

|     |     |     |     |
| --- | --- | --- | --- |
| (81) |  | u~1:=w,u~2:=u2.displaystyletilde{u}^{1}:=w,qquadqquadtilde{u}^{2}:=u^{2}. |  |

From ( 81-dimensional evolutionary differential-difference equations")) one derives 𝐒⁡(w)=𝐒⁡(u~1)=u~11{mathbf{S}}(w)={mathbf{S}}(tilde{u}^{1})=tilde{u}^{1}_{1}.
As usual, we have u0i=uiu^{i}_{0}=u^{i}, u~0i=u~i,tilde{u}^{i}_{0}=tilde{u}^{i} for i=1,2i=1,2.
Now we substitute w=u~01w=tilde{u}^{1}_{0}, 𝐒⁡(w)=u~11,{mathbf{S}}(w)=tilde{u}^{1}_{1}, u02=u~02,u^{2}_{0}=tilde{u}^{2}_{0}
in ( 80-dimensional evolutionary differential-difference equations")) and consider the obtained equation along with u2=u~02u^{2}=tilde{u}^{2}_{0}, which gives

|     |     |     |     |
| --- | --- | --- | --- |
| (82) |  | {u1=u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01u~01​u~02+1,u2=u~02.displaystyleleft{begin{aligned} u^{1}&=frac{tilde{u}^{1}_{1}tilde{u}^{2}_{0}tilde{u}^{1}_{0}+tilde{u}^{1}_{1}-{mathrm{c}}tilde{u}^{1}_{0}-upalpha(n)tilde{u}^{1}_{0}}{tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1},<br>u^{2}&=tilde{u}^{2}_{0}.end{aligned}right. |  |

For each ℓ∈ℤellinmathbb{Z}, applying the operator 𝐒ℓ{mathbf{S}}^{ell} to ( 82-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (83) |  | {uℓ1=u~ℓ+11​u~ℓ2​u~ℓ1+u~ℓ+11−c​u~ℓ1−α⁡(n+ℓ)​u~ℓ1u~ℓ1​u~ℓ2+1,uℓ2=u~2ℓ,ℓ∈ℤ.displaystyleleft{begin{aligned} u^{1}_{ell}&=frac{tilde{u}^{1}_{ell+1}tilde{u}^{2}_{ell}tilde{u}^{1}_{ell}+tilde{u}^{1}_{ell+1}-{mathrm{c}}tilde{u}^{1}_{ell}-upalpha(n+ell)tilde{u}^{1}_{ell}}{tilde{u}^{1}_{ell}tilde{u}^{2}_{ell}+1},<br>u^{2}_{ell}&=tilde{u}^{2}_{ell},qquadqquadqquadqquadellinmathbb{Z}.end{aligned}right. |  |

Substituting w=u~1w=tilde{u}^{1} and ( 83-dimensional evolutionary differential-difference equations")) in ( 79-dimensional evolutionary differential-difference equations")), we derive

|     |     |     |     |
| --- | --- | --- | --- |
| (84) |  | ∂t(u~1)=2​u~−12​(u~01)2−2​c​u~01−2​(u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01)u~01​u~02+1.displaystylepartial_{t}(tilde{u}^{1})=2tilde{u}^{2}_{-1}(tilde{u}^{1}_{0})^{2}-2{mathrm{c}}tilde{u}^{1}_{0}-frac{2(tilde{u}^{1}_{1}tilde{u}^{2}_{0}tilde{u}^{1}_{0}+tilde{u}^{1}_{1}-{mathrm{c}}tilde{u}^{1}_{0}-upalpha(n)tilde{u}^{1}_{0})}{tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1}. |  |

Now we consider ( 84-dimensional evolutionary differential-difference equations")) along with the equation obtained
by means of substituting ( 83-dimensional evolutionary differential-difference equations")) in the second component of ( 72-dimensional evolutionary differential-difference equations")).
This gives the 22-component non-autonomous equation

|     |     |     |     |
| --- | --- | --- | --- |
| (85) |  | {∂t(u~1)=2​u~−12​(u~01)2−2​c​u~01−2​(u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01)u~01​u~02+1,∂t(u~2)=2​u~−12−2​α​(n)​u~02−2​(u~02)2​(u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01)u~01​u~02+1.displaystyleleft{begin{aligned} partial_{t}(tilde{u}^{1})&=2tilde{u}^{2}_{-1}(tilde{u}^{1}_{0})^{2}-2{mathrm{c}}tilde{u}^{1}_{0}-frac{2big(tilde{u}^{1}_{1}tilde{u}^{2}_{0}tilde{u}^{1}_{0}+tilde{u}^{1}_{1}-{mathrm{c}}tilde{u}^{1}_{0}-upalpha(n)tilde{u}^{1}_{0}big)}{tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1},<br>partial_{t}(tilde{u}^{2})&=2tilde{u}^{2}_{-1}-2upalpha(n)tilde{u}^{2}_{0}-frac{2(tilde{u}^{2}_{0})^{2}big(tilde{u}^{1}_{1}tilde{u}^{2}_{0}tilde{u}^{1}_{0}+tilde{u}^{1}_{1}-{mathrm{c}}tilde{u}^{1}_{0}-upalpha(n)tilde{u}^{1}_{0}big)}{tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1}.end{aligned}right. |  |

As discussed above,
system ( 78-dimensional evolutionary differential-difference equations")), ( 79-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( 72-dimensional evolutionary differential-difference equations")).
Since equations ( 82-dimensional evolutionary differential-difference equations")), ( 85-dimensional evolutionary differential-difference equations"))
are derived from ( 78-dimensional evolutionary differential-difference equations")), ( 79-dimensional evolutionary differential-difference equations")), ( 72-dimensional evolutionary differential-difference equations")) (by means of introducing ( 81-dimensional evolutionary differential-difference equations"))),
system ( 82-dimensional evolutionary differential-difference equations")), ( 85-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( 72-dimensional evolutionary differential-difference equations")) as well.
This implies that ( 82-dimensional evolutionary differential-difference equations")) is a MT from ( 85-dimensional evolutionary differential-difference equations")) to ( 72-dimensional evolutionary differential-difference equations")).
(This fact can also be checked independently by a straightforward computation.)

Thus ( 82-dimensional evolutionary differential-difference equations")) is a MT for equation ( 72-dimensional evolutionary differential-difference equations")).
As explained above, ( 72-dimensional evolutionary differential-difference equations")) is obtained from ( 67-dimensional evolutionary differential-difference equations"))
by means of an invertible transformation involving ( 69-dimensional evolutionary differential-difference equations")).
In order to return from ( 72-dimensional evolutionary differential-difference equations")) to ( 67-dimensional evolutionary differential-difference equations")) and to derive a MT for equation ( 67-dimensional evolutionary differential-difference equations")),
we are going to use the relabeling

|     |     |     |     |
| --- | --- | --- | --- |
| (86) |  | uℓ1↦uℓ1,uℓ2↦uℓ+12∀ℓ∈ℤ,displaystyle u^{1}_{ell},mapsto,u^{1}_{ell},qquad u^{2}_{ell},mapsto,u^{2}_{ell+1}qquadquadforall,ellinmathbb{Z}, |  |

which is the inverse of ( 69-dimensional evolutionary differential-difference equations")).
That is, we make the change u1​(n,t)↦u1​(n,t)u^{1}(n,t)mapsto u^{1}(n,t),
u2​(n,t)↦u2​(n+1,t),u^{2}(n,t)mapsto u^{2}(n!+!1,t).

Applying the relabeling ( 86-dimensional evolutionary differential-difference equations")) to ( 72-dimensional evolutionary differential-difference equations")) and ( 82-dimensional evolutionary differential-difference equations")), we obtain

|     |     |     |     |
| --- | --- | --- | --- |
| (87) |  | {∂t(u1)=2​(u12​(u01)2+α⁡(n)​u01−u11),∂t(u12)=2​(u02−u01​(u12)2−α⁡(n)​u12).displaystyleleft{begin{aligned} partial_{t}(u^{1})&=2big(u^{2}_{1}(u^{1}_{0})^{2}+upalpha(n)u^{1}_{0}-u^{1}_{1}big),<br>partial_{t}(u^{2}_{1})&=2big(u^{2}_{0}-u^{1}_{0}(u^{2}_{1})^{2}-upalpha(n)u^{2}_{1}big).end{aligned}right. |  |
| (88) |  | {u1=u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01u~01​u~02+1,u12=u~02.displaystyleleft{begin{aligned} u^{1}&=frac{tilde{u}^{1}_{1}tilde{u}^{2}_{0}tilde{u}^{1}_{0}+tilde{u}^{1}_{1}-{mathrm{c}}tilde{u}^{1}_{0}-upalpha(n)tilde{u}^{1}_{0}}{tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1},<br>u^{2}_{1}&=tilde{u}^{2}_{0}.end{aligned}right. |  |

Applying the operator 𝐒−1{mathbf{S}}^{-1} to the second component in ( 87-dimensional evolutionary differential-difference equations")) and in ( 88-dimensional evolutionary differential-difference equations")),
one gets ( 67-dimensional evolutionary differential-difference equations")) and

|     |     |     |     |
| --- | --- | --- | --- |
| (89) |  | {u1=u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01u~01​u~02+1,u2=u~−12.displaystyleleft{begin{aligned} u^{1}&=frac{tilde{u}^{1}_{1}tilde{u}^{2}_{0}tilde{u}^{1}_{0}+tilde{u}^{1}_{1}-{mathrm{c}}tilde{u}^{1}_{0}-upalpha(n)tilde{u}^{1}_{0}}{tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1},<br>u^{2}&=tilde{u}^{2}_{-1}.end{aligned}right. |  |

Thus ( 89-dimensional evolutionary differential-difference equations")) is a MT from ( 85-dimensional evolutionary differential-difference equations")) to ( 67-dimensional evolutionary differential-difference equations")).

In what follows, we use the dynamical variables
u~ℓ=(u~ℓ1,u~ℓ2)tilde{u}_{ell}=(tilde{u}^{1}_{ell},tilde{u}^{2}_{ell}), ℓ∈ℤ,ellinmathbb{Z}.
Recall that ( 71-dimensional evolutionary differential-difference equations")) is a MLR for equation ( 72-dimensional evolutionary differential-difference equations")),
and formulas ( 83-dimensional evolutionary differential-difference equations")) are obtained by applying the operator 𝐒ℓ{mathbf{S}}^{ell} to ( 82-dimensional evolutionary differential-difference equations")).
Then, applying Lemma 4-dimensional evolutionary differential-difference equations") to the MLR ( 71-dimensional evolutionary differential-difference equations")) and
to the MT ( 82-dimensional evolutionary differential-difference equations")) from ( 85-dimensional evolutionary differential-difference equations")) to ( 72-dimensional evolutionary differential-difference equations")),
we substitute ( 83-dimensional evolutionary differential-difference equations")) in ( 71-dimensional evolutionary differential-difference equations")) and obtain the following MLR for equation ( 85-dimensional evolutionary differential-difference equations"))

|     |     |     |     |
| --- | --- | --- | --- |
| (90) |  | 𝐌⁡(n,u~0,u~1,λ)=(λ+α⁡(n)+u~02​(u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01)u~01​u~02+1u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01u~01​u~02+1u~021),displaystylemathbf{M}(n,tilde{u}_{0},tilde{u}_{1},uplambda)=begin{pmatrix}{uplambda}+upalpha(n)+frac{tilde{u}^{2}_{0}(tilde{u}^{1}_{1}tilde{u}^{2}_{0}tilde{u}^{1}_{0}+tilde{u}^{1}_{1}-{mathrm{c}}tilde{u}^{1}_{0}-upalpha(n)tilde{u}^{1}_{0})}{tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1}&frac{tilde{u}^{1}_{1}tilde{u}^{2}_{0}tilde{u}^{1}_{0}+tilde{u}^{1}_{1}-{mathrm{c}}tilde{u}^{1}_{0}-upalpha(n)tilde{u}^{1}_{0}}{tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1}<br>tilde{u}^{2}_{0}&1<br>end{pmatrix}, |  |
| (91) |  | 𝐔⁡(n,u~−1,u~0,u~1,λ)=(−λ−2​(u~11​u~02​u~01+u~11−c​u~01−α⁡(n)​u~01)u~01​u~02+1−2​u~−12λ).displaystylemathbf{U}(n,tilde{u}_{-1},tilde{u}_{0},tilde{u}_{1},uplambda)=begin{pmatrix}-{uplambda}&-frac{2(tilde{u}^{1}_{1}tilde{u}^{2}_{0}tilde{u}^{1}_{0}+tilde{u}^{1}_{1}-{mathrm{c}}tilde{u}^{1}_{0}-upalpha(n)tilde{u}^{1}_{0})}{tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1}<br>-2tilde{u}^{2}_{-1}&{uplambda}<br>end{pmatrix}. |  |

In order to simplify the MLR ( 90-dimensional evolutionary differential-difference equations")), ( 91-dimensional evolutionary differential-difference equations")) by means of gauge transformations,
we consider Theorem 1-dimensional evolutionary differential-difference equations")
in the case N=2N=2, d=2,mathrm{d}=2, p=1,p=1 with u~ℓtilde{u}_{ell} instead of uℓu_{ell}.
The matrix ( 90-dimensional evolutionary differential-difference equations")) satisfies condition ( 27-dimensional evolutionary differential-difference equations")) with p=1p=1.
Therefore, we can apply Theorem 1-dimensional evolutionary differential-difference equations") to the MLR ( 90-dimensional evolutionary differential-difference equations")), ( 91-dimensional evolutionary differential-difference equations")).
To this end, we need to do the following.

- •


Choose a constant vector a0=(a01,a02)∈ℂ2a_{0}=(a^{1}_{0},a^{2}_{0})inmathbb{C}^{2}.

- •


Substitute u~0=a0tilde{u}_{0}=a_{0} in 𝐌⁡(n,u~0,u~1,λ)mathbf{M}(n,tilde{u}_{0},tilde{u}_{1},uplambda)
given by ( 90-dimensional evolutionary differential-difference equations")) (i.e., substitute u~0i=a0itilde{u}^{i}_{0}=a^{i}_{0} for i=1,2i=1,2 in ( 90-dimensional evolutionary differential-difference equations"))).

- •


Compute 𝐆⁡(n,u~0,λ)mathbf{G}(n,tilde{u}_{0},uplambda) given by formula ( 28-dimensional evolutionary differential-difference equations")),
which involves the matrix



|     |     |     |
| --- | --- | --- |
|  | 𝐌​(n,a0,u~1,λ)−1=(λ+α⁡(n)+a02​(u~11​a02​a01+u~11−c​a01−α⁡(n)​a01)a01​a02+1u~11​a02​a01+u~11−c​a01−α⁡(n)​a01a01​a02+1a021)−1==(1λ+α⁡(n)a01​α​(n)+a01​c−a01​a02​u~11−u~11(a01​a02+1)​(λ+α⁡(n))−a02λ+α⁡(n)a01​u~11​(a02)2+a01​λ​a02−a01​c​a02+u~11​a02+λ+α⁡(n)(a01​a02+1)​(λ+α⁡(n))).displaystylebegin{gathered}mathbf{M}(n,a_{0},tilde{u}_{1},uplambda)^{-1}=begin{pmatrix}{uplambda}+upalpha(n)+frac{a^{2}_{0}(tilde{u}^{1}_{1}a^{2}_{0}a^{1}_{0}+tilde{u}^{1}_{1}-{mathrm{c}}a^{1}_{0}-upalpha(n)a^{1}_{0})}{a^{1}_{0}a^{2}_{0}+1}&frac{tilde{u}^{1}_{1}a^{2}_{0}a^{1}_{0}+tilde{u}^{1}_{1}-{mathrm{c}}a^{1}_{0}-upalpha(n)a^{1}_{0}}{a^{1}_{0}a^{2}_{0}+1}<br>a^{2}_{0}&1<br>end{pmatrix}^{-1}=<br>=begin{pmatrix}frac{1}{{uplambda}+upalpha(n)}&frac{a^{1}_{0}upalpha(n)+a^{1}_{0}{mathrm{c}}-a^{1}_{0}a^{2}_{0}tilde{u}^{1}_{1}-tilde{u}^{1}_{1}}{(a^{1}_{0}a^{2}_{0}+1)({uplambda}+upalpha(n))}<br>-frac{a^{2}_{0}}{{uplambda}+upalpha(n)}&frac{a^{1}_{0}tilde{u}^{1}_{1}(a^{2}_{0})^{2}+a^{1}_{0}{uplambda}a^{2}_{0}-a^{1}_{0}{mathrm{c}}a^{2}_{0}+tilde{u}^{1}_{1}a^{2}_{0}+{uplambda}+upalpha(n)}{(a^{1}_{0}a^{2}_{0}+1)({uplambda}+upalpha(n))}<br>end{pmatrix}.end{gathered} |  |

- •


Apply the obtained gauge transformation 𝐆=𝐆⁡(n,u~0,λ)mathbf{G}=mathbf{G}(n,tilde{u}_{0},uplambda)
to the MLR ( 90-dimensional evolutionary differential-difference equations")), ( 91-dimensional evolutionary differential-difference equations")) and compute
the gauge equivalent MLR (𝐌^,𝐔^)big(widehat{mathbf{M}},,widehat{mathbf{U}}big) given by ( 30-dimensional evolutionary differential-difference equations")).


We can choose for a0=(a01,a02)a_{0}=(a^{1}_{0},a^{2}_{0}) any constant vector
such that ( • ‣ 3.1-dimensional evolutionary differential-difference equations")) is well defined.
In order to make formula ( • ‣ 3.1-dimensional evolutionary differential-difference equations")) as simple as possible, we take

|     |     |     |     |
| --- | --- | --- | --- |
| (94) |  | a01=0,a02=0.displaystyle a^{1}_{0}=0,qquad a^{2}_{0}=0. |  |

Then, using ( • ‣ 3.1-dimensional evolutionary differential-difference equations")) with ( 94-dimensional evolutionary differential-difference equations")), we see that ( 28-dimensional evolutionary differential-difference equations")) reads

|     |     |     |     |
| --- | --- | --- | --- |
| (95) |  | 𝐆⁡(n,u~0,λ)=𝐒−1​(𝐌​(n,a0,u~1,λ)−1)=𝐒−1​((1λ+α⁡(n)−u~11λ+α⁡(n)01))=(1λ+α⁡(n−1)−u~01λ+α⁡(n−1)01).displaystylemathbf{G}(n,tilde{u}_{0},uplambda)={mathbf{S}}^{-1}big(mathbf{M}(n,a_{0},tilde{u}_{1},uplambda)^{-1}big)={mathbf{S}}^{-1}left(begin{pmatrix}frac{1}{{uplambda}+upalpha(n)}&-frac{tilde{u}^{1}_{1}}{{uplambda}+upalpha(n)}<br>0&1<br>end{pmatrix}right)=begin{pmatrix}frac{1}{{uplambda}+upalpha(n-1)}&-frac{tilde{u}^{1}_{0}}{{uplambda}+upalpha(n-1)}<br>0&1<br>end{pmatrix}. |  |

Applying the obtained gauge transformation ( 95-dimensional evolutionary differential-difference equations")) to the MLR ( 90-dimensional evolutionary differential-difference equations")), ( 91-dimensional evolutionary differential-difference equations"))
and computing the MLR (𝐌^,𝐔^)big(widehat{mathbf{M}},,widehat{mathbf{U}}big) given by ( 30-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (96) |  | 𝐌^​(n,u~0,λ)=𝐒⁡(𝐆)⋅𝐌⋅𝐆−1=((λ+α⁡(n−1))​(u~01​u~02​λ+λ+α⁡(n)−c​u~01​u~02)(λ+α⁡(n))​(u~01​u~02+1)(λ−c)​u~01λ+α⁡(n)(λ+α⁡(n−1))​u~02u~01​u~02+1),displaystylewidehat{mathbf{M}}(n,tilde{u}_{0},uplambda)={mathbf{S}}(mathbf{G})cdotmathbf{M}cdotmathbf{G}^{-1}=begin{pmatrix}frac{({uplambda}+upalpha(n-1))(tilde{u}^{1}_{0}tilde{u}^{2}_{0}{uplambda}+{uplambda}+upalpha(n)-{mathrm{c}}tilde{u}^{1}_{0}tilde{u}^{2}_{0})}{({uplambda}+upalpha(n))(tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1)}&frac{({uplambda}-{mathrm{c}})tilde{u}^{1}_{0}}{{uplambda}+upalpha(n)}<br>({uplambda}+upalpha(n-1))tilde{u}^{2}_{0}&tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1<br>end{pmatrix}, |  |
| (97) |  | 𝐔^​(n,u~−1,u~0,λ)=𝐃t​(𝐆)⋅𝐆−1+𝐆⋅𝐔⋅𝐆−1=(2​u~01​u~−12−λ2​(c−λ)​u~01λ+α⁡(n−1)−2​(λ+α⁡(n−1))​u~−12λ−2​u~01​u~−12).displaystylewidehat{mathbf{U}}(n,tilde{u}_{-1},tilde{u}_{0},uplambda)=mathbf{D}_{t}(mathbf{G})cdotmathbf{G}^{-1}+mathbf{G}cdotmathbf{U}cdotmathbf{G}^{-1}=left(!begin{smallmatrix}2tilde{u}^{1}_{0}tilde{u}^{2}_{-1}-{uplambda}&frac{2({mathrm{c}}-{uplambda})tilde{u}^{1}_{0}}{{uplambda}+upalpha(n-1)}<br>-2({uplambda}+upalpha(n-1))tilde{u}^{2}_{-1}&{uplambda}-2tilde{u}^{1}_{0}tilde{u}^{2}_{-1}<br>end{smallmatrix}!right). |  |

In agreement with Theorem 1-dimensional evolutionary differential-difference equations"), we see that
the matrix ( 96-dimensional evolutionary differential-difference equations")) depends only on n,u~0,λn,,tilde{u}_{0},,uplambda,
in contrast to the matrix ( 90-dimensional evolutionary differential-difference equations")) depending on n,u~0,u~1,λn,,tilde{u}_{0},,tilde{u}_{1},,uplambda.

Now, using Definition 6-dimensional evolutionary differential-difference equations") and Remark 4-dimensional evolutionary differential-difference equations") with u~tilde{u}
instead of uu, we see that the MLR ( 96-dimensional evolutionary differential-difference equations")), ( 97-dimensional evolutionary differential-difference equations")) is u~tilde{u}-tame,
and we can try to simplify it by applying a gauge transformation G=G⁡(n,λ)G=G(n,uplambda)
depending only on n,λn,,uplambda.
To avoid cumbersome formulas, we take a diagonal gauge transformation
G=(g11​(n,λ)00g22​(n,λ))G=left(begin{smallmatrix}g^{11}(n,uplambda)&0
0&g^{22}(n,uplambda)end{smallmatrix}right), where g11​(n,λ)g^{11}(n,uplambda) and g22​(n,λ)g^{22}(n,uplambda) are nonzero scalar functions.
Then 𝐒⁡(G)=(g11​(n+1,λ)00g22​(n+1,λ)){mathbf{S}}(G)=left(begin{smallmatrix}g^{11}(n+1,uplambda)&0
0&g^{22}(n+1,uplambda)end{smallmatrix}right) and 𝐃t​(G)=0mathbf{D}_{t}(G)=0.
Applying GG to the MLR ( 96-dimensional evolutionary differential-difference equations")), ( 97-dimensional evolutionary differential-difference equations")), we get the corresponding gauge equivalent MLR

|     |     |     |     |
| --- | --- | --- | --- |
| (98) |  | 𝐌^^=𝐒⁡(G)⋅𝐌^​(n,u~0,λ)⋅G−1=(g11​(n+1,λ)​(λ+α⁡(n−1))​(u~01​u~02​λ+λ+α⁡(n)−c​u~01​u~02)(λ+α⁡(n))​(u~01​u~02+1)​g11​(n,λ)g11​(n+1,λ)​(λ−c)​u~01(λ+α⁡(n))​g22​(n,λ)g22​(n+1,λ)​(λ+α⁡(n−1))​u~02g11​(n,λ)g22​(n+1,λ)​u~01​u~02+1g22​(n,λ)),displaystylewidehat{widehat{mathbf{M}}}={mathbf{S}}(G)cdotwidehat{mathbf{M}}(n,tilde{u}_{0},uplambda)cdot G^{-1}=begin{pmatrix}frac{g^{11}(n+1,uplambda)({uplambda}+upalpha(n-1))(tilde{u}^{1}_{0}tilde{u}^{2}_{0}{uplambda}+{uplambda}+upalpha(n)-{mathrm{c}}tilde{u}^{1}_{0}tilde{u}^{2}_{0})}{({uplambda}+upalpha(n))(tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1)g^{11}(n,uplambda)}&frac{g^{11}(n+1,uplambda)({uplambda}-{mathrm{c}})tilde{u}^{1}_{0}}{({uplambda}+upalpha(n))g^{22}(n,uplambda)}<br>frac{g^{22}(n+1,uplambda)({uplambda}+upalpha(n-1))tilde{u}^{2}_{0}}{g^{11}(n,uplambda)}&frac{g^{22}(n+1,uplambda)tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1}{g^{22}(n,uplambda)}<br>end{pmatrix}, |  |
| (99) |  | 𝐔^^=𝐃t​(G)⋅G−1+G⋅𝐔^​(n,u~−1,u~0,λ)⋅G−1=(2​u~01​u~−12−λ2​g11​(n,λ)​(c−λ)​u~01(λ+α⁡(n−1))​g22​(n,λ)−2​g22​(n,λ)​(λ+α⁡(n−1))​u~−12g11​(n,λ)λ−2​u~01​u~−12).displaystylewidehat{widehat{mathbf{U}}}=mathbf{D}_{t}(G)cdot G^{-1}+Gcdotwidehat{mathbf{U}}(n,tilde{u}_{-1},tilde{u}_{0},uplambda)cdot G^{-1}=left(!begin{smallmatrix}2tilde{u}^{1}_{0}tilde{u}^{2}_{-1}-{uplambda}&frac{2g^{11}(n,uplambda)({mathrm{c}}-{uplambda})tilde{u}^{1}_{0}}{({uplambda}+upalpha(n-1))g^{22}(n,uplambda)}<br>frac{-2g^{22}(n,uplambda)({uplambda}+upalpha(n-1))tilde{u}^{2}_{-1}}{g^{11}(n,uplambda)}&{uplambda}-2tilde{u}^{1}_{0}tilde{u}^{2}_{-1}<br>end{smallmatrix}!right). |  |

We want to choose G=(g11​(n,λ)00g22​(n,λ))G=left(begin{smallmatrix}g^{11}(n,uplambda)&0
0&g^{22}(n,uplambda)end{smallmatrix}right) such that the matrices ( 98-dimensional evolutionary differential-difference equations")), ( 99-dimensional evolutionary differential-difference equations")) become simpler than
the matrices ( 96-dimensional evolutionary differential-difference equations")), ( 97-dimensional evolutionary differential-difference equations")).
The formulas in the right-hand sides of ( 98-dimensional evolutionary differential-difference equations")), ( 99-dimensional evolutionary differential-difference equations")) suggest
to take g11​(n,λ)=λ+α⁡(n−1)g^{11}(n,uplambda)={uplambda}+upalpha(n-1), g22​(n,λ)=1,g^{22}(n,uplambda)=1.
Then ( 98-dimensional evolutionary differential-difference equations")), ( 99-dimensional evolutionary differential-difference equations")) become

|     |     |     |     |
| --- | --- | --- | --- |
| (100) |  | 𝐌^^=(u~01​u~02​λ+λ+α⁡(n)−c​u~01​u~02u~01​u~02+1(λ−c)​u~01u~02u~01​u~02+1),𝐔^^=(2​u~01​u~−12−λ2​(c−λ)​u~01−2​u~−12λ−2​u~01​u~−12).displaystylewidehat{widehat{mathbf{M}}}=begin{pmatrix}frac{tilde{u}^{1}_{0}tilde{u}^{2}_{0}{uplambda}+{uplambda}+upalpha(n)-{mathrm{c}}tilde{u}^{1}_{0}tilde{u}^{2}_{0}}{tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1}&({uplambda}-{mathrm{c}})tilde{u}^{1}_{0}<br>tilde{u}^{2}_{0}&tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1<br>end{pmatrix},qquadquadwidehat{widehat{mathbf{U}}}=begin{pmatrix}2tilde{u}^{1}_{0}tilde{u}^{2}_{-1}-{uplambda}&2({mathrm{c}}-{uplambda})tilde{u}^{1}_{0}<br>-2tilde{u}^{2}_{-1}&{uplambda}-2tilde{u}^{1}_{0}tilde{u}^{2}_{-1}<br>end{pmatrix}. |  |

Fix a constant q∈ℂmathrm{q}inmathbb{C}.
Below we use the matrices ( 100-dimensional evolutionary differential-difference equations")) with λuplambda replaced by qmathrm{q}.
According to Definition 1-dimensional evolutionary differential-difference equations"), since the matrices ( 100-dimensional evolutionary differential-difference equations"))
form a MLR for equation ( 85-dimensional evolutionary differential-difference equations")), one can consider the auxiliary system

|     |     |     |     |
| --- | --- | --- | --- |
| (101) |  | 𝐒⁡(Ψ~)=(u~01​u~02​q+q+α⁡(n)−c​u~01​u~02u~01​u~02+1(q−c)​u~01u~02u~01​u~02+1)⋅Ψ~,∂t(Ψ~)=(2​u~01​u~−12−q2​(c−q)​u~01−2​u~−12q−2​u~01​u~−12)⋅Ψ~,displaystyle{mathbf{S}}(tilde{Psi})=begin{pmatrix}frac{tilde{u}^{1}_{0}tilde{u}^{2}_{0}{mathrm{q}}+{mathrm{q}}+upalpha(n)-{mathrm{c}}tilde{u}^{1}_{0}tilde{u}^{2}_{0}}{tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1}&({mathrm{q}}-{mathrm{c}})tilde{u}^{1}_{0}<br>tilde{u}^{2}_{0}&tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1<br>end{pmatrix}cdottilde{Psi},qquadqquadpartial_{t}(tilde{Psi})=begin{pmatrix}2tilde{u}^{1}_{0}tilde{u}^{2}_{-1}-{mathrm{q}}&2({mathrm{c}}-{mathrm{q}})tilde{u}^{1}_{0}<br>-2tilde{u}^{2}_{-1}&{mathrm{q}}-2tilde{u}^{1}_{0}tilde{u}^{2}_{-1}<br>end{pmatrix}cdottilde{Psi}, |  |

which is compatible modulo equation ( 85-dimensional evolutionary differential-difference equations")).
Here Ψ~=Ψ~​(n,t)tilde{Psi}=tilde{Psi}(n,t) is an invertible 2×22times 2 matrix
with elements ψ~i​j=ψ~i​j​(n,t)tilde{uppsi}^{ij}=tilde{uppsi}^{ij}(n,t), i,j=1,2,i,j=1,2.

Substituting Ψ~=(ψ~11ψ~12ψ~21ψ~22)tilde{Psi}=begin{pmatrix}tilde{uppsi}^{11}&tilde{uppsi}^{12}
tilde{uppsi}^{21}&tilde{uppsi}^{22}end{pmatrix} in ( 101-dimensional evolutionary differential-difference equations")) and considering the first columns
in the matrix equations ( 101-dimensional evolutionary differential-difference equations")), we obtain

|     |     |     |     |
| --- | --- | --- | --- |
| (102) |  | 𝐒⁡(ψ~11)=(u~01​u~02​q+q+α⁡(n)−c​u~01​u~02)u~01​u~02+1​ψ~11+(q−c)​u~01​ψ~21,𝐒⁡(ψ~21)=u~02​ψ~11+(u~01​u~02+1)​ψ~21,displaystyle{mathbf{S}}(tilde{uppsi}^{11})=frac{(tilde{u}^{1}_{0}tilde{u}^{2}_{0}{mathrm{q}}+{mathrm{q}}+upalpha(n)-{mathrm{c}}tilde{u}^{1}_{0}tilde{u}^{2}_{0})}{tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1}tilde{uppsi}^{11}+({mathrm{q}}-{mathrm{c}})tilde{u}^{1}_{0}tilde{uppsi}^{21},qquadquad{mathbf{S}}(tilde{uppsi}^{21})=tilde{u}^{2}_{0}tilde{uppsi}^{11}+(tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1)tilde{uppsi}^{21}, |  |
| (103) |  | ∂t(ψ~11)=(2​u~01​u~−12−q)​ψ~11+2​(c−q)​u~01​ψ~21,∂t(ψ~21)=−2​u~−12​ψ~11+(q−2​u~01​u~−12)​ψ~21.displaystylepartial_{t}(tilde{uppsi}^{11})=(2tilde{u}^{1}_{0}tilde{u}^{2}_{-1}-{mathrm{q}})tilde{uppsi}^{11}+2({mathrm{c}}-{mathrm{q}})tilde{u}^{1}_{0}tilde{uppsi}^{21},qquadquadpartial_{t}(tilde{uppsi}^{21})=-2tilde{u}^{2}_{-1}tilde{uppsi}^{11}+({mathrm{q}}-2tilde{u}^{1}_{0}tilde{u}^{2}_{-1})tilde{uppsi}^{21}. |  |

We set w~=ψ~11/ψ~21tilde{w}={tilde{uppsi}^{11}}/{tilde{uppsi}^{21}}.
Similarly to the computations ( 76-dimensional evolutionary differential-difference equations")), ( 77-dimensional evolutionary differential-difference equations")) based on ( 74-dimensional evolutionary differential-difference equations")), ( 75-dimensional evolutionary differential-difference equations")),
now we compute 𝐒⁡(w~)=𝐒⁡(ψ~11/ψ~21){mathbf{S}}(tilde{w})={mathbf{S}}big({tilde{uppsi}^{11}}/{tilde{uppsi}^{21}}big) and
∂t(w~)=∂t(ψ~11/ψ~21)partial_{t}(tilde{w})=partial_{t}big({tilde{uppsi}^{11}}/{tilde{uppsi}^{21}}big),
using ( 102-dimensional evolutionary differential-difference equations")), ( 103-dimensional evolutionary differential-difference equations")), and get

|     |     |     |     |
| --- | --- | --- | --- |
| (104) |  | 𝐒⁡(w~)=(u~01​u~02​q+q+α⁡(n)−c​u~01​u~02)​w~+(q−c)​u~01​(u~01​u~02+1)(u~01​u~02+1)​(u~02​w~+u~01​u~02+1),displaystyle{mathbf{S}}(tilde{w})=frac{(tilde{u}^{1}_{0}tilde{u}^{2}_{0}{mathrm{q}}+{mathrm{q}}+upalpha(n)-{mathrm{c}}tilde{u}^{1}_{0}tilde{u}^{2}_{0})tilde{w}+({mathrm{q}}-{mathrm{c}})tilde{u}^{1}_{0}(tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1)}{(tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1)(tilde{u}^{2}_{0}tilde{w}+tilde{u}^{1}_{0}tilde{u}^{2}_{0}+1)}, |  |
| (105) |  | ∂t(w~)=2​u~−12​(w~)2+(4​u~01​u~−12−2​q)​w~+2​(c−q)​u~01.displaystylepartial_{t}(tilde{w})=2tilde{u}^{2}_{-1}(tilde{w})^{2}+(4tilde{u}^{1}_{0}tilde{u}^{2}_{-1}-2{mathrm{q}})tilde{w}+2({mathrm{c}}-{mathrm{q}})tilde{u}^{1}_{0}. |  |

The described way of deriving equations ( 104-dimensional evolutionary differential-difference equations")), ( 105-dimensional evolutionary differential-difference equations"))
from system ( 101-dimensional evolutionary differential-difference equations")), which is compatible modulo equation ( 85-dimensional evolutionary differential-difference equations")),
implies that system ( 104-dimensional evolutionary differential-difference equations")), ( 105-dimensional evolutionary differential-difference equations")) is compatible modulo ( 85-dimensional evolutionary differential-difference equations")) as well.

Now we set

|     |     |     |     |
| --- | --- | --- | --- |
| (106) |  | u~~1:=w~,u~~2:=u~2.displaystyletilde{tilde{u}}^{1}:=tilde{w},qquadqquadtilde{tilde{u}}^{2}:=tilde{u}^{2}. |  |

One has 𝐒⁡(w~)=𝐒⁡(u~~1)=u~~11{mathbf{S}}(tilde{w})={mathbf{S}}(tilde{tilde{u}}^{1})=tilde{tilde{u}}^{1}_{1}, u~0i=u~i,tilde{u}^{i}_{0}=tilde{u}^{i}, u~~0i=u~i,tilde{tilde{u}}^{i}_{0}=tilde{u}^{i}, i=1,2,i=1,2.
Substituting 𝐒⁡(w~)=u~~11{mathbf{S}}(tilde{w})=tilde{tilde{u}}^{1}_{1}, w~=u~~01,tilde{w}=tilde{tilde{u}}^{1}_{0}, u~01=u~1,tilde{u}^{1}_{0}=tilde{u}^{1}, u~02=u~~02,tilde{u}^{2}_{0}=tilde{tilde{u}}^{2}_{0}
in ( 104-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (107) |  | u~~11=(u~1​u~~02​q+q+α⁡(n)−c​u~1​u~~02)​u~~01+(q−c)​u~1​(u~1​u~~02+1)(u~1​u~~02+1)​(u~~02​u~~01+u~1​u~~02+1).displaystyletilde{tilde{u}}^{1}_{1}=frac{(tilde{u}^{1}tilde{tilde{u}}^{2}_{0}{mathrm{q}}+{mathrm{q}}+upalpha(n)-{mathrm{c}}tilde{u}^{1}tilde{tilde{u}}^{2}_{0})tilde{tilde{u}}^{1}_{0}+({mathrm{q}}-{mathrm{c}})tilde{u}^{1}(tilde{u}^{1}tilde{tilde{u}}^{2}_{0}+1)}{(tilde{u}^{1}tilde{tilde{u}}^{2}_{0}+1)(tilde{tilde{u}}^{2}_{0}tilde{tilde{u}}^{1}_{0}+tilde{u}^{1}tilde{tilde{u}}^{2}_{0}+1)}. |  |

Equation ( 107-dimensional evolutionary differential-difference equations")) can be resolved with respect to u~1tilde{u}^{1} as follows

|     |     |     |     |
| --- | --- | --- | --- |
| (108) |  | u~1=𝕏+(𝕏)2+2​(q​u~~01+α⁡(n)​u~~01−u~~11​u~~02​u~~01−u~~11)​𝕐𝕐,displaystyletilde{u}^{1}=frac{mathbb{X}+sqrt{(mathbb{X})^{2}+2big({mathrm{q}}tilde{tilde{u}}^{1}_{0}+upalpha(n)tilde{tilde{u}}^{1}_{0}-tilde{tilde{u}}^{1}_{1}tilde{tilde{u}}^{2}_{0}tilde{tilde{u}}^{1}_{0}-tilde{tilde{u}}^{1}_{1}big)mathbb{Y}}}{mathbb{Y}}, |  |

where 𝕏mathbb{X}, 𝕐mathbb{Y} are given by

|     |     |     |     |
| --- | --- | --- | --- |
| (109) |  | 𝕏:=u~~02​(u~~01​(q−u~~11​u~~02−c)−2​u~~11)−c+q,𝕐:=2​u~~02​(u~~11​u~~02+c−q).displaystylemathbb{X}:=tilde{tilde{u}}^{2}_{0}(tilde{tilde{u}}^{1}_{0}({mathrm{q}}-tilde{tilde{u}}^{1}_{1}tilde{tilde{u}}^{2}_{0}-{mathrm{c}})-2tilde{tilde{u}}^{1}_{1})-{mathrm{c}}+{mathrm{q}},qquadquadmathbb{Y}:=2tilde{tilde{u}}^{2}_{0}(tilde{tilde{u}}^{1}_{1}tilde{tilde{u}}^{2}_{0}+{mathrm{c}}-{mathrm{q}}). |  |

Now consider equation ( 108-dimensional evolutionary differential-difference equations")) along with u~2=u~~02tilde{u}^{2}=tilde{tilde{u}}^{2}_{0}, which gives

|     |     |     |     |
| --- | --- | --- | --- |
| (110) |  | {u~1=𝕏+(𝕏)2+2​(q​u~~01+α⁡(n)​u~~01−u~~11​u~~02​u~~01−u~~11)​𝕐𝕐,u~2=u~~02.displaystyleleft{begin{aligned} tilde{u}^{1}&=frac{mathbb{X}+sqrt{(mathbb{X})^{2}+2big({mathrm{q}}tilde{tilde{u}}^{1}_{0}+upalpha(n)tilde{tilde{u}}^{1}_{0}-tilde{tilde{u}}^{1}_{1}tilde{tilde{u}}^{2}_{0}tilde{tilde{u}}^{1}_{0}-tilde{tilde{u}}^{1}_{1}big)mathbb{Y}}}{mathbb{Y}},<br>tilde{u}^{2}&=tilde{tilde{u}}^{2}_{0}.end{aligned}right. |  |

For each ℓ∈ℤellinmathbb{Z}, applying the operator 𝐒ℓ{mathbf{S}}^{ell} to ( 110-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (111) |  | {u~ℓ1=𝐒ℓ​(𝕏)+(𝐒ℓ​(𝕏))2+2​(q​u~~ℓ1+α⁡(n+ℓ)​u~~ℓ1−u~~ℓ+11​u~~ℓ2​u~~ℓ1−u~~ℓ+11)​𝐒ℓ​(𝕐)𝐒ℓ​(𝕐),u~ℓ2=u~~2ℓ,ℓ∈ℤ.displaystyleleft{begin{aligned} tilde{u}^{1}_{ell}&=frac{{mathbf{S}}^{ell}(mathbb{X})+sqrt{({mathbf{S}}^{ell}(mathbb{X}))^{2}+2big({mathrm{q}}tilde{tilde{u}}^{1}_{ell}+upalpha(n+ell)tilde{tilde{u}}^{1}_{ell}-tilde{tilde{u}}^{1}_{ell+1}tilde{tilde{u}}^{2}_{ell}tilde{tilde{u}}^{1}_{ell}-tilde{tilde{u}}^{1}_{ell+1}big){mathbf{S}}^{ell}(mathbb{Y})}}{{mathbf{S}}^{ell}(mathbb{Y})},<br>tilde{u}^{2}_{ell}&=tilde{tilde{u}}^{2}_{ell},qquadqquadqquadqquadellinmathbb{Z}.end{aligned}right. |  |

Substituting w~=u~~1tilde{w}=tilde{tilde{u}}^{1} and ( 111-dimensional evolutionary differential-difference equations")) in ( 105-dimensional evolutionary differential-difference equations")), we derive

|     |     |     |     |
| --- | --- | --- | --- |
| (112) |  | ∂t(u~~1)=2​u~~−12​(u~~01)2−2​q​u~~01+(4​u~~−12​u~~01+2​(c−q))​(𝕏+(𝕏)2+2​(q​u~~01+α⁡(n)​u~~01−u~~11​u~~02​u~~01−u~~11)​𝕐)𝕐.displaystylepartial_{t}(tilde{tilde{u}}^{1})=2tilde{tilde{u}}^{2}_{-1}(tilde{tilde{u}}^{1}_{0})^{2}-2{mathrm{q}}tilde{tilde{u}}^{1}_{0}+frac{big(4tilde{tilde{u}}^{2}_{-1}tilde{tilde{u}}^{1}_{0}+2({mathrm{c}}-{mathrm{q}})big)left(mathbb{X}!+!sqrt{(mathbb{X})^{2}!+!2big({mathrm{q}}tilde{tilde{u}}^{1}_{0}!+!upalpha(n)tilde{tilde{u}}^{1}_{0}!-!tilde{tilde{u}}^{1}_{1}tilde{tilde{u}}^{2}_{0}tilde{tilde{u}}^{1}_{0}!-!tilde{tilde{u}}^{1}_{1}big)mathbb{Y}}right)}{mathbb{Y}}. |  |

Now we consider ( 112-dimensional evolutionary differential-difference equations")) along with the equation obtained
by means of substituting ( 111-dimensional evolutionary differential-difference equations")) in the second component of ( 85-dimensional evolutionary differential-difference equations")).
This gives the 22-component non-autonomous equation

|     |     |     |     |
| --- | --- | --- | --- |
| (113) |  | {∂t(u~~1)=2​u~~−12​(u~~01)2−2​q​u~~01+(4​u~~−12​u~~01+2​(c−q))​(𝕏+(𝕏)2+2​(q​u~~01+α⁡(n)​u~~01−u~~11​u~~02​u~~01−u~~11)​𝕐)𝕐,∂t(u~~2)=ℍ⁡(n,u~~01,u~~11,u~~21,u~~−12,u~~02,u~~12,c,q),displaystyleleft{begin{aligned} partial_{t}(tilde{tilde{u}}^{1})&=2tilde{tilde{u}}^{2}_{-1}(tilde{tilde{u}}^{1}_{0})^{2}-2{mathrm{q}}tilde{tilde{u}}^{1}_{0}+frac{big(4tilde{tilde{u}}^{2}_{-1}tilde{tilde{u}}^{1}_{0}+2({mathrm{c}}-{mathrm{q}})big)left(mathbb{X}!+!sqrt{(mathbb{X})^{2}!+!2big({mathrm{q}}tilde{tilde{u}}^{1}_{0}!+!upalpha(n)tilde{tilde{u}}^{1}_{0}!-!tilde{tilde{u}}^{1}_{1}tilde{tilde{u}}^{2}_{0}tilde{tilde{u}}^{1}_{0}!-!tilde{tilde{u}}^{1}_{1}big)mathbb{Y}}right)}{mathbb{Y}},<br>partial_{t}(tilde{tilde{u}}^{2})&=mathbb{H}big(n,tilde{tilde{u}}^{1}_{0},tilde{tilde{u}}^{1}_{1},tilde{tilde{u}}^{1}_{2},tilde{tilde{u}}^{2}_{-1},tilde{tilde{u}}^{2}_{0},tilde{tilde{u}}^{2}_{1},mathrm{c},mathrm{q}big),end{aligned}right. |  |

where the function
ℍ=ℍ⁡(n,u~~01,u~~11,u~~21,u~~−12,u~~02,u~~12,c,q)mathbb{H}=mathbb{H}big(n,tilde{tilde{u}}^{1}_{0},tilde{tilde{u}}^{1}_{1},tilde{tilde{u}}^{1}_{2},tilde{tilde{u}}^{2}_{-1},tilde{tilde{u}}^{2}_{0},tilde{tilde{u}}^{2}_{1},mathrm{c},mathrm{q}big)
is obtained by substituting ( 111-dimensional evolutionary differential-difference equations")) in the right-hand side of the second component of ( 85-dimensional evolutionary differential-difference equations")).
(We do not present the explicit formula for ℍmathbb{H}, since it is rather cumbersome.)

As discussed above,
system ( 104-dimensional evolutionary differential-difference equations")), ( 105-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( 85-dimensional evolutionary differential-difference equations")).
Since equations ( 110-dimensional evolutionary differential-difference equations")), ( 113-dimensional evolutionary differential-difference equations"))
are derived from ( 104-dimensional evolutionary differential-difference equations")), ( 105-dimensional evolutionary differential-difference equations")), ( 85-dimensional evolutionary differential-difference equations")) (by means of introducing ( 106-dimensional evolutionary differential-difference equations"))),
system ( 110-dimensional evolutionary differential-difference equations")), ( 113-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( 85-dimensional evolutionary differential-difference equations")) as well.
This implies that ( 110-dimensional evolutionary differential-difference equations")) is a MT from ( 113-dimensional evolutionary differential-difference equations")) to ( 85-dimensional evolutionary differential-difference equations")).
(This fact can also be verified by a direct calculation.)

###### Remark 6.

Recall that ( 100-dimensional evolutionary differential-difference equations")) is a MLR for equation ( 85-dimensional evolutionary differential-difference equations")),
and formulas ( 111-dimensional evolutionary differential-difference equations")) are derived by applying the operator 𝐒ℓ{mathbf{S}}^{ell} to ( 110-dimensional evolutionary differential-difference equations")).
Using Lemma 4-dimensional evolutionary differential-difference equations") for the MLR ( 100-dimensional evolutionary differential-difference equations")) and
the MT ( 110-dimensional evolutionary differential-difference equations")) from ( 113-dimensional evolutionary differential-difference equations")) to ( 85-dimensional evolutionary differential-difference equations")),
we can substitute ( 111-dimensional evolutionary differential-difference equations")) in ( 100-dimensional evolutionary differential-difference equations")), and this gives a MLR for equation ( 113-dimensional evolutionary differential-difference equations")).

### 3.2. Other examples

The following 22-component equation
was derived in  [16, Section 5.1.1]
in a study of invariant time evolutions of polygons in the centro-affine plane

|     |     |     |     |
| --- | --- | --- | --- |
| (114) |  | {∂t(u1)=u01​u02,∂t(u2)=u−11u01−u01u11.displaystyleleft{begin{aligned} partial_{t}(u^{1})&=u^{1}_{0}u^{2}_{0},<br>partial_{t}(u^{2})&=frac{u^{1}_{-1}}{u^{1}_{0}}-frac{u^{1}_{0}}{u^{1}_{1}}.end{aligned}right. |  |

It is shown in  [16, Section 5.1.1] that one has the MT

|     |     |     |     |
| --- | --- | --- | --- |
| (115) |  | {w1=u01/u11,w2=u02displaystyleleft{begin{aligned} w^{1}&=u^{1}_{0}/u^{1}_{1},<br>w^{2}&=u^{2}_{0}end{aligned}right. |  |

from ( 114-dimensional evolutionary differential-difference equations")) to the equation

|     |     |     |     |
| --- | --- | --- | --- |
| (116) |  | {∂t(w1)=w01​(w02−w12),∂t(w2)=w−11−w01,displaystyleleft{begin{aligned} partial_{t}(w^{1})&=w^{1}_{0}(w^{2}_{0}-w^{2}_{1}),<br>partial_{t}(w^{2})&=w^{1}_{-1}-w^{1}_{0},end{aligned}right. |  |

which is the Toda lattice in the Flaschka–Manakov coordinates  [3, 15].

It is known (see, e.g.,  [10]) that the following matrices form a MLR for ( 116-dimensional evolutionary differential-difference equations"))

|     |     |     |     |
| --- | --- | --- | --- |
| (117) |  | 𝐌˘=(λ−w12w01−10),𝐔˘=(0−w011λ−w02).displaystylebreve{mathbf{M}}=begin{pmatrix}{uplambda}-w^{2}_{1}&w^{1}_{0}<br>-1&0<br>end{pmatrix},qquadquadbreve{mathbf{U}}=begin{pmatrix}0&-w^{1}_{0}<br>1&{uplambda}-w^{2}_{0}<br>end{pmatrix}. |  |

Applying Lemma 4-dimensional evolutionary differential-difference equations") to the MLR ( 117-dimensional evolutionary differential-difference equations")) and
to the MT ( 115-dimensional evolutionary differential-difference equations")) from ( 114-dimensional evolutionary differential-difference equations")) to ( 116-dimensional evolutionary differential-difference equations")),
we substitute ( 115-dimensional evolutionary differential-difference equations")) in ( 117-dimensional evolutionary differential-difference equations")) and obtain the following MLR for equation ( 114-dimensional evolutionary differential-difference equations"))

|     |     |     |     |
| --- | --- | --- | --- |
| (118) |  | 𝐌=(λ−u12u01/u11−10),displaystylemathbf{M}=begin{pmatrix}{uplambda}-u^{2}_{1}&u^{1}_{0}/u^{1}_{1}<br>-1&0<br>end{pmatrix}, |  |
| (119) |  | 𝐔=(0−u10/u111λ−u02).displaystylemathbf{U}=begin{pmatrix}0&-u^{1}_{0}/u^{1}_{1}<br>1&{uplambda}-u^{2}_{0}<br>end{pmatrix}. |  |

In order to simplify the MLR ( 118-dimensional evolutionary differential-difference equations")), ( 119-dimensional evolutionary differential-difference equations")) by means of gauge transformations,
we consider Theorem 1-dimensional evolutionary differential-difference equations") in the case N=2N=2, d=2,mathrm{d}=2, p=1,p=1.
The matrix ( 118-dimensional evolutionary differential-difference equations")) obeys condition ( 27-dimensional evolutionary differential-difference equations")) with p=1p=1.
Therefore, one can apply Theorem 1-dimensional evolutionary differential-difference equations") to the MLR ( 118-dimensional evolutionary differential-difference equations")), ( 119-dimensional evolutionary differential-difference equations")).
To this end, we need to do the following.

- •


Choose a constant vector a0=(a01,a02)∈ℂ2a_{0}=(a^{1}_{0},a^{2}_{0})inmathbb{C}^{2}.

- •


Substitute u0=a0u_{0}=a_{0} in 𝐌mathbf{M}
given by ( 118-dimensional evolutionary differential-difference equations")) (i.e., substitute u0i=a0iu^{i}_{0}=a^{i}_{0} for i=1,2i=1,2 in ( 118-dimensional evolutionary differential-difference equations")))
and compute the corresponding gauge transformation ( 28-dimensional evolutionary differential-difference equations")),
which gives 𝐆=(0−1u01/a01u01​(λ−u02)/a01)mathbf{G}=begin{pmatrix}0&-1
u^{1}_{0}/a^{1}_{0}&u^{1}_{0}({uplambda}-u^{2}_{0})/a^{1}_{0}end{pmatrix}.
Here it is convenient to take a01=1a^{1}_{0}=1, and then 𝐆mathbf{G} takes the form
𝐆=(0−1u01u01​(λ−u02))mathbf{G}=begin{pmatrix}0&-1
u^{1}_{0}&u^{1}_{0}({uplambda}-u^{2}_{0})end{pmatrix}.

- •


Now we apply the obtained gauge transformation 𝐆mathbf{G}
to the MLR ( 118-dimensional evolutionary differential-difference equations")), ( 119-dimensional evolutionary differential-difference equations")) and compute
the gauge equivalent MLR (𝐌^,𝐔^)big(widehat{mathbf{M}},,widehat{mathbf{U}}big) given by ( 30-dimensional evolutionary differential-difference equations")), which gives



|     |     |     |     |
| --- | --- | --- | --- |
| (120) |  | 𝐌^=𝐒⁡(𝐆)⋅𝐌⋅𝐆−1=(λ−u021/u01−u010),𝐔^=𝐃t​(𝐆)⋅𝐆−1+𝐆⋅𝐔⋅𝐆−1=(0−1/u10u−11λ).displaystylewidehat{mathbf{M}}={mathbf{S}}(mathbf{G})cdotmathbf{M}cdotmathbf{G}^{-1}=begin{pmatrix}{uplambda}-u^{2}_{0}&1/u^{1}_{0}<br>-u^{1}_{0}&0<br>end{pmatrix},qquadwidehat{mathbf{U}}=mathbf{D}_{t}(mathbf{G})cdotmathbf{G}^{-1}+mathbf{G}cdotmathbf{U}cdotmathbf{G}^{-1}=begin{pmatrix}0&-1/u^{1}_{0}<br>u^{1}_{-1}&{uplambda}<br>end{pmatrix}. |  |


Fix a constant c∈ℂmathrm{c}inmathbb{C}.
Below we use the matrices ( 120-dimensional evolutionary differential-difference equations")) with λuplambda replaced by cmathrm{c}.
According to Definition 1-dimensional evolutionary differential-difference equations"), since ( 120-dimensional evolutionary differential-difference equations"))
is a MLR for equation ( 114-dimensional evolutionary differential-difference equations")), we can consider the auxiliary system

|     |     |     |     |
| --- | --- | --- | --- |
| (121) |  | 𝐒⁡(Ψ)=(c−u021/u01−u010)⋅Ψ,∂t(Ψ)=(0−1/u10u−11c)⋅Ψ,displaystyle{mathbf{S}}(Psi)=begin{pmatrix}{mathrm{c}}-u^{2}_{0}&1/u^{1}_{0}<br>-u^{1}_{0}&0<br>end{pmatrix}cdotPsi,qquadquadpartial_{t}(Psi)=begin{pmatrix}0&-1/u^{1}_{0}<br>u^{1}_{-1}&{mathrm{c}}<br>end{pmatrix}cdotPsi, |  |

which is compatible modulo equation ( 114-dimensional evolutionary differential-difference equations")).
Here Ψ=Ψ⁡(n,t)Psi=Psi(n,t) is an invertible 2×22times 2 matrix
with elements ψi​j=ψi​j​(n,t)uppsi^{ij}=uppsi^{ij}(n,t), i,j=1,2,i,j=1,2.

Substituting Ψ=(ψ11ψ12ψ21ψ22)Psi=begin{pmatrix}uppsi^{11}&uppsi^{12}
uppsi^{21}&uppsi^{22}end{pmatrix} in ( 121-dimensional evolutionary differential-difference equations")) and considering the first columns
in the matrix equations ( 121-dimensional evolutionary differential-difference equations")), one gets

|     |     |     |     |
| --- | --- | --- | --- |
| (122) |  | 𝐒⁡(ψ11)=(c−u02)​ψ11+1u01​ψ21,𝐒⁡(ψ21)=−u01​ψ11,displaystyle{mathbf{S}}(uppsi^{11})=({mathrm{c}}-u^{2}_{0})uppsi^{11}+frac{1}{u^{1}_{0}}uppsi^{21},qquadquad{mathbf{S}}(uppsi^{21})=-u^{1}_{0}uppsi^{11}, |  |
| (123) |  | ∂t(ψ11)=−1u01​ψ21,∂t(ψ21)=u−11​ψ11+c​ψ21.displaystylepartial_{t}(uppsi^{11})=-frac{1}{u^{1}_{0}}uppsi^{21},qquadquadpartial_{t}(uppsi^{21})=u^{1}_{-1}uppsi^{11}+{mathrm{c}}uppsi^{21}. |  |

Since the matrix system ( 121-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( 114-dimensional evolutionary differential-difference equations")),
the corresponding system ( 122-dimensional evolutionary differential-difference equations")), ( 123-dimensional evolutionary differential-difference equations"))
obtained from the first columns in ( 121-dimensional evolutionary differential-difference equations")) is compatible modulo ( 114-dimensional evolutionary differential-difference equations")) as well.
We set

|     |     |     |     |
| --- | --- | --- | --- |
| (124) |  | u~1:=ψ11,u~2:=ψ21.displaystyletilde{u}^{1}:=uppsi^{11},qquadqquadtilde{u}^{2}:=uppsi^{21}. |  |

For i=1,2i=1,2 one has 𝐒⁡(ψi​1)=𝐒⁡(u~i)=u~1i{mathbf{S}}(uppsi^{i1})={mathbf{S}}(tilde{u}^{i})=tilde{u}^{i}_{1},
u0i=ui,u^{i}_{0}=u^{i}, u~0i=u~i,tilde{u}^{i}_{0}=tilde{u}^{i}.
Substituting 𝐒⁡(ψi​1)=u~1i{mathbf{S}}(uppsi^{i1})=tilde{u}^{i}_{1}, ψi​1=u~0i,uppsi^{i1}=tilde{u}^{i}_{0}, u0i=ui,u^{i}_{0}=u^{i}
in ( 122-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (125) |  | u~11=(c−u2)​u~01+1u1​u~02,u~12=−u1​u~01.displaystyletilde{u}^{1}_{1}=({mathrm{c}}-u^{2})tilde{u}^{1}_{0}+frac{1}{u^{1}}tilde{u}^{2}_{0},qquadquadtilde{u}^{2}_{1}=-u^{1}tilde{u}^{1}_{0}. |  |

Equations ( 125-dimensional evolutionary differential-difference equations")) can be resolved with respect to u1u^{1}, u2u^{2} as follows

|     |     |     |     |
| --- | --- | --- | --- |
| (126) |  | {u1=−u~21/u~10,u2=(c​u~01​u~12−u~01​u~02−u~11​u~12)/(u~01​u~12).displaystyleleft{begin{aligned} u^{1}&=-tilde{u}^{2}_{1}/tilde{u}^{1}_{0},<br>u^{2}&=({mathrm{c}}tilde{u}^{1}_{0}tilde{u}^{2}_{1}-tilde{u}^{1}_{0}tilde{u}^{2}_{0}-tilde{u}^{1}_{1}tilde{u}^{2}_{1})/(tilde{u}^{1}_{0}tilde{u}^{2}_{1}).end{aligned}right. |  |

For each ℓ∈ℤellinmathbb{Z}, applying the operator 𝐒ℓ{mathbf{S}}^{ell} to ( 126-dimensional evolutionary differential-difference equations")), we get

|     |     |     |     |
| --- | --- | --- | --- |
| (127) |  | {uℓ1=−u~2ℓ+1/u~1ℓ,uℓ2=(cu~1ℓu~2ℓ+1−u~1ℓu~2ℓ−u~1ℓ+1u~2ℓ+1)/(u~1ℓu~2ℓ+1),ℓ∈ℤ.displaystyleleft{begin{aligned} u^{1}_{ell}&=-tilde{u}^{2}_{ell+1}/tilde{u}^{1}_{ell},<br>u^{2}_{ell}&=({mathrm{c}}tilde{u}^{1}_{ell}tilde{u}^{2}_{ell+1}-tilde{u}^{1}_{ell}tilde{u}^{2}_{ell}-tilde{u}^{1}_{ell+1}tilde{u}^{2}_{ell+1})/(tilde{u}^{1}_{ell}tilde{u}^{2}_{ell+1}),qquadqquadqquadqquadellinmathbb{Z}.end{aligned}right. |  |

Substituting ψ11=u~1uppsi^{11}=tilde{u}^{1}, ψ21=u~2,uppsi^{21}=tilde{u}^{2}
and ( 127-dimensional evolutionary differential-difference equations")) in ( 123-dimensional evolutionary differential-difference equations")), we obtain 22-component equation

|     |     |     |     |
| --- | --- | --- | --- |
| (128) |  | {∂t(u~1)=u~01​u~02/u~12,∂t(u~2)=u~02​(c​u~−11−u~01)/u~−11.displaystyleleft{begin{aligned} partial_{t}(tilde{u}^{1})&=tilde{u}^{1}_{0}tilde{u}^{2}_{0}/tilde{u}^{2}_{1},<br>partial_{t}(tilde{u}^{2})&=tilde{u}^{2}_{0}({mathrm{c}}tilde{u}^{1}_{-1}-tilde{u}^{1}_{0})/tilde{u}^{1}_{-1}.end{aligned}right. |  |

As discussed above,
system ( 122-dimensional evolutionary differential-difference equations")), ( 123-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( 114-dimensional evolutionary differential-difference equations")).
Since equations ( 126-dimensional evolutionary differential-difference equations")), ( 128-dimensional evolutionary differential-difference equations"))
are derived from ( 122-dimensional evolutionary differential-difference equations")), ( 123-dimensional evolutionary differential-difference equations")) (by means of introducing ( 124-dimensional evolutionary differential-difference equations"))),
system ( 126-dimensional evolutionary differential-difference equations")), ( 128-dimensional evolutionary differential-difference equations")) is compatible modulo equation ( 114-dimensional evolutionary differential-difference equations")) as well.
This implies that ( 126-dimensional evolutionary differential-difference equations")) is a MT from ( 128-dimensional evolutionary differential-difference equations")) to ( 114-dimensional evolutionary differential-difference equations")),
which can also be verified by a straightforward computation.

###### Remark 7.

Recall that ( 120-dimensional evolutionary differential-difference equations")) is a MLR for equation ( 114-dimensional evolutionary differential-difference equations")),
and formulas ( 127-dimensional evolutionary differential-difference equations")) are obtained by applying the operator 𝐒ℓ{mathbf{S}}^{ell} to ( 126-dimensional evolutionary differential-difference equations")).
Using Lemma 4-dimensional evolutionary differential-difference equations") for the MLR ( 120-dimensional evolutionary differential-difference equations")) and
the MT ( 126-dimensional evolutionary differential-difference equations")) from ( 128-dimensional evolutionary differential-difference equations")) to ( 114-dimensional evolutionary differential-difference equations")),
we can substitute ( 127-dimensional evolutionary differential-difference equations")) in ( 120-dimensional evolutionary differential-difference equations")), and this gives a MLR for equation ( 128-dimensional evolutionary differential-difference equations")).

## Acknowledgments

The author would like to thank S. Konstantinou-Rizos and A.V. Mikhailov for useful discussions.

This work was supported by the Russian Science Foundation (grant No. 25-21-00454,
https://rscf.ru/en/project/25-21-00454/ ).

## References

- [1]
E. Chistov, S. Igonin.
On matrix Lax representations and constructions
of Miura-type transformations for differential-difference equations.
_Partial Differential Equations in Applied Mathematics_ 13 (2025), 101014.
arXiv:2410.01474 [nlin.SI]

- [2]
V.G. Drinfeld and V.V. Sokolov.
On equations related to the Korteweg–de Vries equation.
_Soviet Math. Dokl._ 32 (1985), 361–365.

- [3]
H. Flaschka. The Toda lattice. II. Existence of integrals. _Phys. Rev. B_ 9 (1974), 1924–1925.

- [4]
R.N. Garifullin, R.I. Yamilov, and D. Levi.
Classification of five-point differential–difference equations.
_J. Phys. A_ 50 (2017), 125201.
arXiv:1610.07342 [nlin.SI]

- [5]
R.N. Garifullin, R.I. Yamilov, and D. Levi.
Classification of five-point differential–difference equations II.
_J. Phys. A_ 51 (2018), 065204.
arXiv:1708.02456 [nlin.SI]

- [6]
J. Hietarinta, N. Joshi, and F.W. Nijhoff.
_Discrete systems and integrability._
Cambridge University Press, Cambridge, 2016.

- [7]
S. Igonin.
Simplifications of Lax pairs for differential-difference equations by gauge transformations
and (doubly) modified integrable equations.
_Partial Differential Equations in Applied Mathematics_ 11 (2024), 100821.
arXiv:2403.12022 [nlin.SI]

- [8]
S. Igonin.
Matrix Lax pairs under the gauge equivalence relation induced by the gauge group action
and Miura-type transformations for lattice equations.
_J. Geom. Phys._ 216 (2025), 105585.
arXiv:2405.08579 [nlin.SI]

- [9]
S. Igonin.
The gauge action on semi-discrete Lax representations and its invariants.
arXiv:2604.20830 [nlin.SI]

- [10]
F. Khanizadeh, A.V. Mikhailov, and Jing Ping Wang.
Darboux transformations and recursion operators for differential-difference equations.
_Theor. Math. Phys._ 177 (2013), 1606–1654.
arXiv:1305.0588 [nlin.SI]

- [11]
S. Konstantinou-Rizos, A.V. Mikhailov, and P. Xenitidis.
Reduction groups and related integrable difference systems of nonlinear Schrödinger type.
_J. Math. Phys._ 56 (2015), 082701.

- [12]
D. Levi, P. Winternitz, and R.I. Yamilov.
Continuous symmetries and integrability of discrete equations.
_CRM Monograph Series_ 38.
Providence, RI: American Mathematical Society, 2022.

- [13]
A.G. Meshkov and M.Ju. Balakhnev.
Two-field integrable evolutionary systems of the third order and their differential substitutions.
_SIGMA_ 4 (2008), Paper 018.
arXiv:0802.1253 [nlin.SI]

- [14] A.V. Mikhailov, A.B. Shabat, and V.V. Sokolov.
The symmetry approach to classification of integrable equations.
In: _What is integrability?_, edited by V. E. Zakharov, Springer–Verlag, 1991.

- [15]
S.V. Manakov. Complete integrability and stochastization in discrete dynamical systems.
_Sov. Phys. JETP_ 40 (1975), 269–274.

- [16]
E. Mansfield, G. Marí Beffa, Jing Ping Wang.
Discrete moving frames and discrete integrable systems.
_Foundations of Computational Mathematics_ 13 (2013), 545–582.

- [17]
M. Marvan. On zero-curvature representations of partial differential equations.
_Differential geometry and its applications (Opava, 1992)_, 103–122.
Silesian Univ. Opava, 1993.
http://emis.maths.tcd.ie/proceedings/5ICDGA
- [18]
M. Marvan.
A direct procedure to compute zero-curvature representations. The case s​l2sl_{2}.
_Secondary Calculus and Cohomological Physics (Moscow, 1997)_, 9 pp.
http://emis.maths.tcd.ie/proceedings/SCCP97
- [19]
R. Miura. Korteweg – de Vries equation and
generalizations. I. A remarkable explicit nonlinear transformation.
_J. Math. Phys._ 9 (1968), 1202–1204.

- [20]
R.M. Miura, C.S. Gardner, and M.D. Kruskal.
Korteweg-de Vries equation and generalizations. II.
Existence of conservation laws and constants of motion.
_J. Math. Phys._ 9 (1968), 1204–1209.

- [21]
S.Yu. Sakovich.
On zero-curvature representations of evolution equations.
_J. Phys. A_ 28 (1995), 2861–2869.

- [22]
Yu.B. Suris.
_The Problem of Integrable Discretization: Hamiltonian Approach._
Progress in Mathematics, 219. Birkhäuser Verlag, Basel, 2003.

- [23]
R. Yamilov.
Symmetries as integrability criteria for differential difference equations.
_J. Phys. A_ 39 (2006), R541–R623.


Experimental support, please
[view the build logs](https://arxiv.org/html/2604.26870v1/__stdout.txt)
for errors. Generated by
[L
A
T
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