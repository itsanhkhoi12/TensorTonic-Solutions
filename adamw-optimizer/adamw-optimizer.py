import numpy as np

def adamw_step(w, m, v, grad, lr=0.001, beta1=0.9, beta2=0.999, weight_decay=0.01, eps=1e-8):
    """
    Perform one AdamW update step.
    """
    # Write code here
    w,m,v,grad = np.array(w),np.array(m),np.array(v),np.array(grad)
    m_t = (beta1*m)+(1-beta1)*grad
    v_t = (beta2*v)+(1-beta2)*np.square(grad)
    w_t = w-(lr*(weight_decay*w))-((lr*m_t)/(np.sqrt(v_t)+eps))
    return w_t,m_t,v_t