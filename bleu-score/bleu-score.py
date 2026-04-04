import math

def bleu_score(candidate, reference, max_n):
    """
    Compute the BLEU score for a candidate translation.
    """
    # Write code here
        
    if len(candidate) == 0:
        return 0.0
    else:
        c, r = len(candidate), len(reference)
        BP = 1 if c>=r else math.exp(1-r/c)
        p = []
        for n in range(1,max_n+1):
            c_freq = {} # Tần suất các phần tử candidate n-gram
            r_freq = {} # Tần suất các phần tử reference n-gram
            
            for i in range(c-n+1):
                c_ngram = " ".join(candidate[i:i+n]) # Tạo các phần tử n-gram
                c_freq[c_ngram] = c_freq.get(c_ngram,0) + 1 # Tăng tần suất lên cho phần tử n-gram

            for i in range(r-n+1):
                r_ngram = " ".join(reference[i:i+n]) # Tạo các phần tử n-gram
                r_freq[r_ngram] = r_freq.get(r_ngram,0) + 1 # Tăng tần suất lên cho phần tử n-gra

            deno = sum(c_freq.values())
            if deno <= 0:
                pn = 0.0
            else:
                pn = sum(min(v,r_freq.get(k,0)) for k,v in c_freq.items()) / deno
            if pn == 0.0:
                return 0.0
            p.append(pn)

        bleu = BP * math.exp(sum([math.log(pn) for pn in p])/max_n)

        return bleu