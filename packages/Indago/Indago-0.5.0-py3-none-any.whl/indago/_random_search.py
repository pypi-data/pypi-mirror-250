# -*- coding: utf-8 -*-
"""
RANDOM SEARCH METHODS
"""


import numpy as np
from ._optimizer import Optimizer, CandidateState 


class RS(Optimizer):
    """Random Search method class.
    
    Attributes
    ----------
    variant : str
        Name of the RS variant. Default (and the only available option): ``Vanilla``.
    params : dict
        A dictionary of RS parameters.
        
    Returns
    -------
    optimizer : RS
        RS optimizer instance.
    """
    

    def __init__(self):
        Optimizer.__init__(self)

        self.variant = 'Vanilla'
        self.params = {}


    def _check_params(self):
        """Private method which performs some RS-specific parameter checks
        and prepares the parameters to be validated by Optimizer._check_params.

        Returns
        -------
        None
            Nothing
            
        """
        
        
        defined_params = list(self.params.keys())
        mandatory_params, optional_params = ['batch_size'], []
        
        if 'batch_size' in self.params:
            self.params['batch_size'] = int(self.params['batch_size'])
            assert self.params['batch_size'] > 0, \
                "batch_size parameter should be positive integer"
        else:
            self.params['batch_size'] = self.dimensions
        defined_params += 'batch_size'.split()

        if self.variant == 'Vanilla':
            pass
    
        else:
            assert False, f'Unknown variant! {self.variant}'

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)


    def _init_method(self):
        """Private method for initializing the RS optimizer instance.
        Initializes and evaluates optimizer.max_evaluations number of candidates.

        Returns
        -------
        None
            Nothing
            
        """
        
        self._evaluate_initial_candidates()

        # Generate all candidates
        n0 = 0 if self._cS0 is None else self._cS0.size
        self.cS = np.array([CandidateState(self) for _ in range(self.params['batch_size'] - n0)], dtype=CandidateState)
        self._initialize_X(self.cS[n0:])
        
        # Using specified particles initial positions
        for p in range(np.size(self.cS)):
            if p < n0:
                self.cS[p] = self._cS0[p].copy()
            
        # Evaluate
        if n0 < self.params['batch_size']:
            self._collective_evaluation(self.cS[n0:])

        # if all candidates are NaNs
        if np.isnan([cP.f for cP in self.cS]).all():
            self._err_msg = 'ALL CANDIDATES FAILED TO EVALUATE'

        self._finalize_iteration()
    
        
    def _run(self):
        """Run procedure for the RS method. 

        Returns
        -------
        optimum: CandidateState
            Best solution found during the RS optimization.
            
        """
        
        self._check_params()      
        self._init_method()

        while True:

            self._initialize_X(self.cS)
            self._collective_evaluation(self.cS)

            if self._finalize_iteration():
                break

        return self.best