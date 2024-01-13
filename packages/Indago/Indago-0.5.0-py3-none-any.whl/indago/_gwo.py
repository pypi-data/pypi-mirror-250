# -*- coding: utf-8 -*-
"""
GRAY WOLF OPTIMIZER algorithm
"""


import numpy as np
from ._optimizer import Optimizer, CandidateState 


class GWO(Optimizer):
    """Grey Wolf Optimizer class method class.
    
    Reference: S. Mirjalili, S. M. Mirjalili, A. Lewis, Grey Wolf Optimizer, 
    Advances in Engineering Software, vol. 69, pp. 46-61, 2014, 
    DOI: http://dx.doi.org/10.1016/j.advengsoft.2013.12.007
    
    Attributes
    ----------
    variant : str
        Name of the GWO variant (``Vanilla`` or ``HSA``). Default: ``Vanilla``.
    params : dict
        A dictionary of GWO parameters.
        
    Returns
    -------
    optimizer : GWO
        GWO optimizer instance.
    """

    def __init__(self):
        Optimizer.__init__(self)

        self.variant = 'Vanilla'
        self.params = {}


    def _check_params(self):
        """Private method which performs some GWO-specific parameter checks
        and prepares the parameters to be validated by Optimizer._check_params.

        Returns
        -------
        None
            Nothing
        """
        
        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.variant == 'Vanilla' or self.variant == 'HSA':
            mandatory_params += 'pop_size'.split()
            
            if 'pop_size' in self.params:
                self.params['pop_size'] = int(self.params['pop_size'])
            else:
                self.params['pop_size'] = max(10, self.dimensions)
            defined_params += 'pop_size'.split()
          
        else:
            assert False, f'Unknown variant! {self.variant}'

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)


    def _init_method(self):
        """Private method for initializing the GWO optimizer instance.
        Initializes and evaluates the population.
        
        Returns
        -------
        None
            Nothing
        """

        assert self.max_iterations or self.max_evaluations or self.max_elapsed_time, \
            'optimizer.max_iteration, optimizer.max_evaluations, or optimizer.max_elapsed_time should be provided for this method/variant'

        assert self.params['pop_size'] >= 5, \
            'population size (pop_size param) should be greater than or equal to 5'

        # Generate population
        self.cS = np.array([CandidateState(self) for _ in range(self.params['pop_size'])])
        self._initialize_X(self.cS)
        
        self._evaluate_initial_candidates()
        n0 = 0 if self._cS0 is None else self._cS0.size    
        # Using specified particles initial positions
        for p in range(np.size(self.cS)):     
            if p < n0:
                self.cS[p] = self._cS0[p].copy()
            
        # Evaluate
        if n0 < np.size(self.cS):
            self._collective_evaluation(self.cS[n0:])

        # If all candidates are NaNs       
        if np.isnan([cP.f for cP in self.cS]).all():
            self._err_msg = 'ALL CANDIDATES FAILED TO EVALUATE'

        self._finalize_iteration()
    
        
    def _run(self):
        """Main loop of GWO method.

        Returns
        -------
        optimum: CandidateState
            Best solution found during the GWO optimization.
            
        """
        
        self._check_params()      
        self._init_method()

        while True:
            
            # find alpha, beta, delta
            alpha, beta, delta = np.sort(self.cS)[:3]
            
            # calculate a
            if self.variant == 'Vanilla':
                # linearly decreasing (2->0)
                a = 2 * (1 - self._progress_factor()) 
            elif self.variant == 'HSA':
                # changing in a (3/4 of a) half sinusoid (2*sin(pi/4)->0)
                a = 2 * np.sin(np.pi/4 + self._progress_factor() * (np.pi - np.pi/4))
            
            # move wolves
            for cP in self.cS:
            
                r1 = np.random.uniform(-1, 1, self.dimensions)
                r2 = np.random.uniform(0, 2, self.dimensions)
                X1 = alpha.X - a * r1 * np.abs(r2 * alpha.X - cP.X)

                r1 = np.random.uniform(-1, 1, self.dimensions)
                r2 = np.random.uniform(0, 2, self.dimensions)            
                X2 = beta.X - a * r1 * np.abs(r2 * beta.X - cP.X)
                
                r1 = np.random.uniform(-1, 1, self.dimensions)
                r2 = np.random.uniform(0, 2, self.dimensions)               
                X3 = delta.X - a * r1 * np.abs(r2 * delta.X - cP.X)

                cP.X = (X1 + X2 + X3) / 3

                cP.clip(self)
            
            # evaluate
            self._collective_evaluation(self.cS)

            if self._finalize_iteration():
                break
        
        return self.best
