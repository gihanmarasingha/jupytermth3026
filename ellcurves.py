
# coding: utf-8

# # Elliptic curve class

# ## ECM3726 Cryptography

# ### *Dr Gihan Marasingha*, University of Exeter, 2019

# In[708]:


from crypto_basic import invmod, jac, oddpart
from random import randint


# We need a function for finding a square root modulo $p$.


def squarerootmodp(a,p):
    """Returns the square root of a modulo p. This only works if (a/p)=1"""
    a = a % p
    if (p % 8 == 3) or (p % 8 == 7):
        a = a % p
        x = pow(a,(p+1)//4,p)
        return x
    if p % 8 == 5:
        x = pow(a,(p+3)//8,p)
        c = (x*x) % p
        if c != a:
            x = x*pow(2,(p-1)//4,p)
        return x
    d = 2
    while jac(d,p) != -1:
        d = randint(2,p-1)
    [s,t]=oddpart(p-1)
    A = pow(a,t,p)
    D = pow(d,t,p)
    m = 0
    for i in range(s):
        if pow(A*pow(D,m,p),2**(s-1-i),p) == p-1:
            m = m + 2**i
    x = (pow(a,(t+1)//2,p)*pow(D,m//2,p)) % p
    return x  


# In[710]:


class EllipticCurve():
    """Elliptic curves over a finite field of prime order."""
    def __init__(self,a,b,p,test=True):
        """Create an elliptic curve with Weierstrass equation y^2 = x^3 + ax + b
        over the field of order p."""
        self.a = a % p; self.b = b % p; self.p = p
        self.test = test
        if (4*a**3+27*b**2) % p ==0:
            raise ValueError("Discriminant is zero modulo p.")
    def __repr__(self):
        return f"Elliptic curve with equation y^2 = x^3 + {self.a}x + {self.b} over Z/{self.p}Z."
    def __call__(self,P):
        return Point(self,P)
    def neutral(self):
        return Neutral(self)  
    def points(self):
        """A generator for points on the curve."""
        p = self.p; a = self.a; b = self.b
        yield Neutral(self)
        for x in range(p):
            z = (x**3 + a*x + b) % p
            if z%p == 0:
                yield Point(self,(x,0))
            elif jac(z,p)==1:
                y = squarerootmodp(z,p)
                yield Point(self,(x,y))
                yield Point(self,(x,p-y))
    def order(self):
        """The number of elements in the elliptic curve group."""
        a, b, p = self.a, self.b, self.p
        jacs = [jac((x**3+a*x+b) % p,p) for x in range(p)]
        return (sum(jacs)+p+1)


# In[711]:


class Point():
    """Finite points on an elliptic curve."""
    def __init__(self,curve,P):
        p = curve.p
        self.x = P[0] % p ; self.y = P[1] % p
        self.curve = curve
        if (curve.test):
            self.__test__()
    def __test__(self):
        """Tests if the point really is on the curve."""
        x = self.x; y = self.y
        curve = self.curve
        if ((x**3+curve.a*x+curve.b -y*y) % curve.p) != 0:
            raise ValueError("The specified point is not on the curve.")
    def __repr__(self):
        return f"({self.x},{self.y})"
    def __hash__(self):
        return hash(str(self))
    def __eq__(self,other):
        if self.curve == other.curve and self.x == other.x and self.y == other.y:
            return True
        return False
    def dbl(self):
        """Returns 2*self"""
        x, y, p, a = self.x, self.y, self.curve.p, self.curve.a
        if(y==0):
            return Neutral(self.curve)
        den = invmod(2*y,p)
        m = ((3*x*x+a)*den) % p
        xd = (m*m-2*x) % p
        yd = (-m*(xd-x)-y) % p
        return Point(self.curve,(xd,yd))
    def __add__(self,Q):
        """Returns self + Q."""
        if isinstance(Q,Neutral):
            return self
        x1, y1, x2, y2 = self.x, self.y, Q.x, Q.y
        p = self.curve.p; a = self.curve.a
        if x1 == x2:
            if ((y1+y2)%p)==0:  # if P = -Q
                return Neutral(self.curve)
            else:         # if P = Q
                den = invmod(2*y1,p)
                m = ((3*x1*x1+a)*den) % p # the 'gradient'
        else: # P and Q have different x coordinates
            den = invmod(x2-x1,p)
            m = ((y2-y1)*den) % p
        x3 = ((m*m-x1-x2)) % p
        y3 = (-m*(x3-x1)-y1)  % p
        return Point(self.curve,(x3,y3))
    def __neg__(self):
        """Returns the additive inverse of self."""
        return Point(self.curve,(self.x,self.curve.p-self.y))
    def __sub__(self,Q):
        return self + (-Q)
    def __rmul__(self,n):
        """Compute n*self, for an integer n."""
        if n<0:
            return ((-n)*self).__neg__()
        if n==0:
            return Neutral(self.curve)
        Q = Neutral(self.curve) # start with Q being the point at infinity
        R = self
        while n > 0:
            if (n%2==1):
                Q = Q+R
                n=n-1
            n=n//2
            if (n>0): # avoids an unecessary doubling
                R = R.dbl()
        return Q




# In[712]:


class Neutral(Point):
    """The neutral point on an elliptic curve"""
    def __init__(self,curve):
        self.curve = curve
    def __repr__(self):
        return "O"
    def __hash__(self):
        return hash(str(self))
    def __eq__(self,Q):
        if isinstance(Q,Neutral):
            return True
        return False
    def dbl(self):
        return self
    def __add__(self,Q):
        return Q
    def __sub__(self,Q):
        return Q.__neg__()
    def __neg__(self):
        return self
    def __rmul__(self,n):
        return self
