import dynet as dy
from antu.nn.dynet.initializer import orthonormal_initializer
from . import dy_model


@dy_model
class MLP(object):
    """docstring for MLP"""

    def __init__(
            self,
            model: dy.ParameterCollection,
            sizes: List[int],
            f: 'nonlinear' = dy.tanh, 
            p: float = 0.0,
            bias: bool = True, 
            init: dy.PyInitializer = dy.GlorotInitializer()):
        
        pc = model.add_subcollection()
        self.W = [
            pc.add_parameters((x, y), init)
            for x, y in zip(sizes[1:], sizes[:-1])]
        '''
        self.W = [
            pc.parameters_from_numpy(orthonormal_initializer(x, y))
            for x, y in zip(sizes[1:], sizes[:-1])]
        '''
        if bias:
            self.b = [pc.add_parameters((y,), init=0) for y in sizes[1:]]

        self.pc, self.f, self.p, self.bias = pc, f, p, bias
        self.spec = (sizes, f, p, bias, init)

    def __call__(self, x, train=False):
        h = x
        # for W, b in zip(self.W[:-1], self.b[:-1]):
        for i in range(len(self.W[:-1])):
            h = self.f(self.W[i]*h + (self.b[i] if self.bias else 0))
            if train:
                if len(h.dim()[0]) > 1:
                    h = dy.dropout_dim(h, 1, self.p)
                else:
                    h = dy.dropout(h, self.p)
        return self.W[-1]*h + (self.b[-1] if self.bias else 0)

