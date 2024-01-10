from lazylinop import LazyLinearOp, aslazylinearoperator, isLazyLinearOp
import numpy as np

def block_diag(*lops, mt=False):
    """
    Returns the block diagonal LazyLinearOp formed of operators in lops.

    Args:
        lops:
             the objects defining the diagonal blocks as a list of LazyLinearOp-s or other compatible linear operator.
        mt:
             True to active the multithread experimental mode (not advisable, so far it's not faster than sequential execution).

    Returns:
        The diagonal block LazyLinearOp.

    Example:
        >>> import numpy as np
        >>> from lazylinop import block_diag, aslazylinearoperator
        >>> from scipy.sparse import diags
        >>> nt = 10
        >>> d = 64
        >>> v = np.random.rand(d)
        >>> terms = [np.random.rand(64, 64) for _ in range(10)]
        >>> ls = block_diag(*terms) # ls is the block diagonal LazyLinearOp


    <b>See also:</b> `scipy.linalg.block_diag <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.block_diag.html>`_.
    """
    lAx = lambda A, x: A @ x
    lAHx = lambda A, x: A.T.conj() @ x
    roffsets =  [0]
    coffsets =  [0] # needed for transpose case
    for i in range(len(lops)):
        roffsets += [roffsets[i] + lops[i].shape[1]]
        coffsets += [coffsets[i] + lops[i].shape[0]]
    def matmat(x, lmul, offsets):
        from threading import Thread
        from multiprocessing import cpu_count
        if len(x.shape) == 1:
            x_is_1d = True
            x = x.reshape(x.size, 1)
        else:
            x_is_1d = False
        Ps = [None for _ in range(len(lops))]
        n = len(lops)
        class Mul(Thread):
            def __init__(self, As, x, out, i):
                self.As = As
                self.x = x
                self.out = out
                self.i = i
                super(Mul, self).__init__(target=self.run)

            def run(self):
                for i, A in enumerate(self.As):
                    ipi = self.i + i
                    self.out[ipi] = lmul(A,
                                         self.x[offsets[ipi]:offsets[ipi+1]])

        if mt:
            ths = []
            nths = min(cpu_count(), n)
            share = [n // nths for _ in range(nths)]
            rem = n - share[0] * nths
            if rem > 0:
                while rem > 0:
                    share[rem-1] += 1
                    rem -= 1
            for i in range(1, len(share)):
                share[i] += share[i-1]
            share = [0] + share
            for i in range(nths):
                start = share[i]
                end = share[i+1]
                ths += [Mul(lops[start:end], x, Ps, start)]
                ths[-1].start()
            for i in range(nths):
                ths[i].join()
        else:
            for i, A in enumerate(lops):
                Ps[i] = lmul(A, x[offsets[i]:offsets[i+1]])
        S = Ps[0]
        conv_to_lop = isLazyLinearOp(S)
        vcat = vstack if conv_to_lop else np.vstack
        for i in range(1, n):
            if conv_to_lop:
                Ps[i] = aslazylinearoperator(Ps[i])
            elif isLazyLinearOp(Ps[i]):
                S = aslazylinearoperator(S)
                conv_to_lop = True
                vcat = vstack
            S = vcat((S, Ps[i]))
        if x_is_1d:
            S = S.ravel()
        return S
    return LazyLinearOp((coffsets[-1], roffsets[-1]), matmat=lambda x:
                              matmat(x, lAx, roffsets),
                              rmatmat=lambda x: matmat(x, lAHx, coffsets))

