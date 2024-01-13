#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._optimizer import Optimizer, CandidateState
import numpy as np


class GD(Optimizer):
    """Gradient descent method class.

    Returns
    -------
    optimizer : GD
        Gradient descent optimizer instance.
    """

    def __init__(self):
        """Private method which prepares the parameters to be validated by Optimizer._check_params.

        Returns
        -------
        None
            Nothing
            
        """
        
        Optimizer.__init__(self)

        self.X = None
        self.X0 = 1
        self.variant = 'Vanilla'
        self.params = {}

    def _check_params(self):
        """Private method which prepares the parameters to be validated by Optimizer._check_params.

        Returns
        -------
        None
            Nothing
            
        """

        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.variant == 'Vanilla':
            mandatory_params = 'dx'.split()

            if 'dx' not in self.params:
                self.params['dx'] = 1e-6
                defined_params += 'dx'.split()

        else:
            assert False, f'Unknown variant! {self.variant}'

        for param in mandatory_params:
            # if param not in defined_params:
            #    print('Missing parameter (%s)' % param)
            assert param in defined_params, f'Missing parameter {param}'

        for param in defined_params:
            if param not in mandatory_params and param not in optional_params:
                self.log(f'Warning: Excessive parameter {param}')

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)

    def _init_method(self):
        """Private method for initializing the NelderMead optimizer instance.
        Evaluates given initial candidates, selects starting point, constructs initial polytope/simplex.

        Returns
        -------
        None
            Nothing
            
        """

        self._evaluate_initial_candidates()

        # Generate set of points
        self.cS = np.array([CandidateState(self) for _ in range(self.dimensions + 1)],
                           dtype=CandidateState)

        n0 = 0 if self._cS0 is None else self._cS0.size
        self.log(f'{n0=}')
        # Generate initial positions
        self.cS[0] = self._cS0[0].copy()

        # Evaluate
        #self._collective_evaluation(self.cS[:1])

        # if all candidates are NaNs       
        if np.isnan([cP.f for cP in self.cS]).all():
            self._err_msg = 'ALL CANDIDATES FAILED TO EVALUATE'

        self._finalize_iteration()

    def _run(self):
        """Main loop of GD method.

        Returns
        -------
        optimum: CandidateState
            Best solution found during the NelderMead optimization.
            
        """
        
        self._check_params()
        self._init_method()

        dx = np.full(self.dimensions, self.params['dx'])
        DX = np.diag(dx)
        alpha = 1e-6
        delta = 1e1

        hist_x = np.full((2, self.dimensions), np.nan)
        hist_grad = np.full((2, self.dimensions), np.nan)
        grad = np.full(self.dimensions, np.nan)

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 10))

        while True:

            ax.plot(self.cS[0].X[0], self.cS[0].X[1], 'b+')
            for p in range(self.dimensions):
                # Random position
                self.cS[p + 1].X = self.cS[0].X + DX[p, :]
                self.cS[p + 1].X = np.clip(self.cS[p + 1].X, self.lb, self.ub)
                ax.plot(self.cS[0].X[0], self.cS[0].X[1], '.', c='grey')

            self._collective_evaluation(self.cS[1:])

            for p in range(0, self.dimensions):
                grad[p] = (self.cS[p + 1].f - self.cS[0].f) / dx[p]
            if np.linalg.norm(grad) == 0:
                self.log('Zero gradient')
                break

            hist_x[-2, :] = hist_x[-1, :]
            hist_x[-1, :] = self.cS[0].X.copy()
            hist_grad[-2, :] = hist_grad[-1, :]
            hist_grad[-1, :] = grad.copy()

            if self.it > 1:
                s = hist_x[-1, :] - hist_x[-2, :]
                y = hist_grad[-1, :] - hist_grad[-2, :]
                ss = np.dot(s, s)
                sy = np.dot(s, y)
                alpha = ss / sy

                if alpha <= 0 or np.isnan(alpha):
                    # eq 4.2
                    # Although the paper says this correction for nonconvex
                    # problems depends on sk for the current iteration,
                    # it's not available up to this point. Will use k-1
                    # regardless
                    alpha = np.linalg.norm(s) / np.linalg.norm(y)

                alpha = np.min([alpha, delta / np.linalg.norm(grad)])

                self.log(f'x={self.cS[0].X}')
                self.log(f'{grad=}')
                # self.log(f'{s=}')
                # self.log(f'{y=}')
                # self.log(f'{alpha=}')


            self.cS[0].X -= alpha * grad
            self.cS[0].X = np.clip(self.cS[0].X, self.lb, self.ub)
            self._collective_evaluation(self.cS[:1])

            if self._finalize_iteration():
                break

        ax.plot(self.cS[0].X[0], self.cS[0].X[1], 'ro')
        ax.axis('equal')
        plt.savefig('gd.png')
        plt.close(fig)

        return self.best
