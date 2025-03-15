
# coding: utf-8

# # Basic algorithms for cryptography

# ### ECM3726 Cryptography

# ### *Dr Gihan Marasingha*, University of Exeter, 2017

# ## Euclid's algorithm

# Given integers $a$ and $b$, we write a simple algorithm that computes the gcd of $a$ and $b$.
# The algorithm is recursive. In the base case, $\gcd(a,0)=0$. Recursively, write $a=qb+r$ with $0\le r < b$, then $\gcd(a,b)=\gcd(b,r)$. The remainder $r$ is denoted by `a % b` in Python.

# In[1]:


def gcd_slow(a,b):
    """A recursive function that returns the greatest common divisor of a and b."""
    if b==0:
        return a;
    else:
        return gcd_slow(b,a%b);





# We improve the performance of the function by writing it non-recursively.

# In[3]:


def gcd(a,b):
    r0, r1 = a, b;
    while r1 != 0:
        r0, r1 = r1, r0 % r1
    return r0


# The speed difference can be observed by comparing `timeit(gcd_slow(6765, 10946))` with `timeit(gcd(6765, 10946))`. This is left to the reader.

# We write an extended Euclid's algorithm. Initially, we write the algorithm in a recursive manner, then rewrite the algorithm procedurally.
# 
# The recursive algorithm takes as input two numbers $a$ and $b$ and returns a list `[d,s,t]`, where $d=\gcd(a,b)$ and $d=sa+tb$.
# 
# Suppose that $a=qb + r$ with $0\le r < b$. 
# If $\gcd(b,r)=s_1 b + t_1 r$, then $\gcd(a,b) = s_1 b + t_1 r = s_1 b + t_1 (a - qb) = t_1 a + (s_1 - t_1 q) b$.
# It follows that $s=t_1$ and $t = (s_1 - t_1 q)$.

# In[4]:


def ergcd(a,b):
    """A recursive function that returns [d,a,b] where d=gcd(a,b) and d = s*a + t*b"""
    if b==0:
        return [a,1,0];
    else:
        r = a % b;
        q = (a-r)//b; # The double // indicates integer division
        [d,s1,t1]=ergcd(b,r);
        return [d,t1,s1-t1*q];

# With a bit more work, we can write this an an imperative algorithm.
# 
# Write $r_0 = a$, $r_1 = b$, $q_1 = q$ and $r_2 = r$, so that the equation $a = qb + r$ becomes $r_0 = q_1 r_1 + r_2$.
# Inductively, define $r_i = q_{i+1} r_{i+1} + r_{i+2}$. We defined integers $s_i$ and $t_i$ so that $r_i = s_i a + t_i b$ for each $i$.
# 
# Then, for each $i\ge 0$,
# $$
# \begin{align}
# r_{i+2} &= r_i - q_{i+1} r_{i+1} = (s_i a + t_i b) - q_{i+1} (s_{i+1} a + t_{i+1} b) \\
# &= (s_i - q_{i+1} s_{i+1}) a + (t_i - q_{i+1} t_{i+1}) b.
# \end{align}
# $$
# 
# This gives the recurrence relations $s_{i+2} = s_i - q_{i+1} s_{i+1}$ and $t_{i+2} = t_i - q_{i+1} t_{i+1}$, for $i\ge 0$.
# To find the initial values, first observe $r_0 = a = 1\cdot a + 0\cdot b$, so $s_0 = 1$ and $t_0 = 0$. Second note
# $r_1 = b = 0\cdot a + 1 \cdot b$, so $s_1 = 0$ and $t_1 = 1$.
# 
# Finally, a clever observation is that we don't need to keep track of the $t_i$ variables as the final value of $t_i$ can be determined from the equation $d = sa + tb$ to be $t = (d-sa)/b$.

# In[6]:


def egcd(a,b):
    """A prodedural function that returns [d,s,t] where d = gcd(a,b) and d = s*a + t*b"""
    if b == 0:
        return [a,1,0]
    s0, s1 = 1, 0;
    r0, r1 = a, b;
    while r1 != 0:
        r2 = r0 % r1;
        q1 = (r0-r2)//r1;
        s2 = s0 - q1*s1;
        s0=s1; s1=s2;
        r0=r1; r1=r2;
    t0 = (r0-s0*a)//b;
    return [r0,s0,t0]




def invmod(a,m):
    """Compute the inverse of a modulo m. We need m>0."""
    [r,s,t] = egcd(m,a)
    if r==1:
        return t % m
    elif r==-1:
        return (m-t) % m
    else:
        raise ValueError("Argument must be coprime. The inverse does not exist.",a,m)


# ## Binary numbers

# Our next function recursively computes the binary expression of an integer $a$. Exceptionally, the empty string is used to denote $0$.

# In[7]:


def binary(a):
    """Returns a string that expresses a in binary notation"""
    if a==0:
        return "";
    if (a%2 == 0):
        return binary(a/2) + "0";
    else:
        return binary((a-1)/2) + "1";


# Essentially the same function can be expressed procedurally. This time, "0" represents $0$.

# In[10]:


def binaryrep(a):
    if a==0:
        return "0";
    s = "";
    while a>0:
        if (a%2==0):
            s = "0" + s;
        else:
            s = "1" + s;
        a = a //2
    return s;


# ## Fast modular exponentiation

# We start again with a recursive algorithm for computing $b^e \pmod{n}$. If $e=0$, the answer is $1$. Else, write the $e=2d+r$ where $r=0$ or $r=1$. Then $a^e=(a^d)^2a^r\pmod n$, reducing the problem to the computatin of $a^d \pmod n$.

# In[12]:


def fmodrec(a,e,n):
    """Recursive algorithm for computing a^e modulo n."""
    if e==0:
        return 1;
    r = e%2; d = e//2;
    if r==0:
        return fmodrec(a,d,n)**2 % n;
    else:
        return (fmodrec(a,d,n)**2 * a) % n;


# We write the same algorithm procedurally.

# In[14]:


def fmod(a,e,n):
    """Procedural algorithm for computing a^e modulo n."""
    s = 1; b = a;
    while True:
        if (e%2==1):
            s=s*b % n;
        e = e // 2
        if e==0:
            return s
        b=b*b %n;
        
# ## Chinese remainder theorem

# Let $m_1,\ldots m_k$ be a set of mutually pairwise coprime natural numbers.
# 
# Given a set of simultaneous congruences $x\equiv a_i \pmod{m_i}$, for $i=1,\ldots,k$, we build up the solution inductively. If $k=1$, the solution is $x\equiv a_1\pmod{m_1}$.
# 
# Suppose we already have a solution $x_{k-1}$ modulo $M_{k-1} = m_1 \cdots m_{k-1}$ to the congruences $x\equiv a_i \pmod{m_i}$, for $i=1,\ldots,k-1$.
# 
# Then $x$ is a solution to the full set of congruences if and only if $x\equiv x_{k-1} \pmod{M_{k-1}}$ and $x\equiv a_l \pmod m_k$. It remains to find $x$.
# 
# We start by using the extended Euclidean algorithm to write $1 = sM_{k-1} + t m_k$, so $1 \equiv t m_k \pmod{M_{k-1}}$ and $1\equiv s M_{k-1} \pmod{m_k}$. Write
# $x = s M_{k-1} a_k + t m_k x_{k-1}$. Then $x\equiv a_k \pmod {m_k}$ and $x\equiv x_k\pmod{M_{k-1}}$, as required.

# In[16]:


def crt(alist,modlist):
    x=alist[0]; m=modlist[0]; k = len(alist);
    for i in range(1,k): # i takes values in the range 1, 2, ..., k-1
        mi=modlist[i];
        [d,s,t]=egcd(m,mi); # we don't use d
        x = s*m*alist[i]+t*mi*x;
        m=m*mi;
        x=x%m;
    return x;

# ## Jacobi symbol

# First we have a function $\operatorname{oddpart}(n)$ that returns a pair
# `[k,q]` where $n=2^k q$ with $q$ an odd integer and $k\ge 0$ an integer.


def oddpart(n):
    """Given n, find q and k such that n=2^k q, where q is odd."""
    k = 0; q = n
    while q%2 == 0:
        q=q//2
        k = k +1
    return [k,q]

# Using this idea, we write a function that computes the Jacobi symbol
# $\left(\frac{n}{m}\right)$ for an integer $n$ and an odd natural number $m$.


def jac(n,m):
    """Computes the Jacobi symbol (n/m) for an integer n and an odd natural number m.""" 
    if n==1 or m==1:
        return 1
    if (n>=m) or (n<0):
        return jac(n % m,m)
    if n==0:
        return 0
    k = 0; q = n  # Copying the code from the "oddpart" function above to save a function call
    while q%2 == 0:
        q=q//2
        k = k +1
    if (k%2 == 0) or (m % 8 ==1) or (m%8 == 7): # finding the Jacobi symbol (2/m)^k
        jac2 = 1
    else: 
        jac2 = -1
    if (q % 4 == 3) and (m % 4 == 3):
        sign = -1
    else:
        sign = 1
    return jac2*sign*jac(m,q)


# An implementation of the Sieve of Eratosthenes

def sieve(B,verbose=False):
    """The sieve of Eratosthenes. It returns a list of primes that are less than B, assuming B >= 3
    In the implementation, we save about half the effort by only considering odd numbers up to B.
    
    If `verbose` is `True`, then detailed information is printed."""
    xslen = B//2-1
    xs = [1]*xslen # each '1' in this list represents an odd number up to B
    plist=[2] # the output list of primes.
    i = 0 # the index into the list xs
    n = 3 # the current number
    while n*n < B:
        if verbose:
            print("Current number is %i. Current index is %i." % (n,i))
        if xs[i] != 0:
            plist.append(n)
            if verbose:
                print("  Found a prime %i." % (n))
            for j in range(i+n,xslen,n):
                if verbose:
                    print("  Zeroing the entry %i at index %i." % (2*j+3,j))                
                xs[j]=0
        i=i+1
        n=n+2
    if verbose:
        print("Sieved up to sqrt(%i)." % B)
    while i<xslen:
        if xs[i] != 0:
            if verbose:
                print("Found a prime %i." % (2*i+3))
            plist.append(2*i+3)
        i=i+1
    return(plist)
