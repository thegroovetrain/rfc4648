import string

_DIGITS = '0123456789'

_alphabets = {}
_alphabets.update({'base64' :    string.ascii_uppercase + string.ascii_lowercase + _DIGITS + '+/'})
_alphabets.update({'base64url' : string.ascii_uppercase + string.ascii_lowercase + _DIGITS + '-_'})
_alphabets.update({'base32' :    string.ascii_uppercase + '234567'})
_alphabets.update({'base32hex' : _DIGITS + string.ascii_uppercase[:22]})
_alphabets.update({'base16' :    _DIGITS + 'ABCDEF'})
_alphabets.update({'hex' :       _alphabets['base16']})

PAD = '='

def binary_encode(n):

    o = ''
    
    while n > 0:
        o = str(n % 2) + o
        n = n // 2
    
    return o if len(o) > 0 else '0'
        


def octet_encode(c):

    n = ord(c)
        
    return format(int(binary_encode(n)), '08')



def binary_decode(b):
    
    return int(b, 2)



def octet_decode(o):
    
    return chr(binary_decode(o))



def bytestring_encode(s):
    
    b = ''
    
    for c in s:
        b += octet_encode(c)
        
    return b



def bytestring_decode(bs):
    
    s = ''
    
    for o in range(0, len(bs), 8):
        s += octet_decode(bs[o:o+8])
        
    return s



def get_b64_chars(bs, a='base64'):
    
    b64 = ''
    
    while len(bs) % 6 != 0:
        bs += '0'
        
    for i in range(0,len(bs),6):
        b64 += _alphabets[a][binary_decode(bs[i:i+6])]
        
    return b64



def base64_encode(s, a='base64'):
    
    b64 = ''
    p = 0
    
    while p < len(s):
        
        if p+3 <= len(s):
            
            bs = bytestring_encode(s[p:p+3])
            b64 += get_b64_chars(bs, a)
            
        else:
            
            bs = bytestring_encode(s[p:])
            
            if len(bs) == 8:
                
                b64 += get_b64_chars(bs, a) + PAD + PAD
                
            else:   # len(bs) == 16
                
                b64 += get_b64_chars(bs, a) + PAD
                
        p += 3
        
    return b64



def base64url_encode(s):

    return base64_encode(s, 'base64url')



def base64_decode(b64, a='base64'):
    
    s = ''

    for q in range(0,len(b64),4):
        bs = ''
        for c in b64[q:q+4]:
            if c != PAD:
                v = _alphabets[a].find(c)
                bs += format(int(binary_encode(v)), '06')

        while len(bs) % 8 != 0:
            bs = bs[0:-1]
        s += bytestring_decode(bs)
    return s

def base64url_decode(b64):
    return base64_decode(b64, 'base64url')

