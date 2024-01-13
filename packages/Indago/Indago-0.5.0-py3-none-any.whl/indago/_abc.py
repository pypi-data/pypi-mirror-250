# -*- coding: utf-8 -*-
"""
ARTIFICIAL BEE COLONY algorithm
"""


import numpy as np
from ._optimizer import Optimizer, CandidateState 


Bee = CandidateState


class ABC(Optimizer):
    """Artificial Bee Colony Algorithm class method class.
    
    Attributes
    ----------
    variant : str
        Name of the ABC variant (``Vanilla`` or ``FullyEmployed``). Default: ``Vanilla``.
    params : dict
        A dictionary of ABC parameters.
        
    Returns
    -------
    optimizer : ABC
        ABC optimizer instance.
    """

    def __init__(self):
        Optimizer.__init__(self)

        self.variant = 'Vanilla'
        self.params = {}


    def _check_params(self):
        """Private method which performs some ABC-specific parameter checks
        and prepares the parameters to be validated by Optimizer._check_params.

        Returns
        -------
        None
            Nothing
            
        """
        
        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.variant == 'Vanilla':
            mandatory_params += 'pop_size trial_limit'.split()
            
            if 'pop_size' in self.params:
                self.params['pop_size'] = int(self.params['pop_size'])
            else:
                self.params['pop_size'] = max(10, self.dimensions * 2)
            defined_params += 'pop_size'.split()
            
            if 'trial_limit' in self.params:
                self.params['trial_limit'] = int(self.params['trial_limit'])            
            else:
                self.params['trial_limit'] = int(self.params['pop_size'] * self.dimensions / 2) # Karaboga and Gorkemli 2014 - "A quick artificial bee colony (qabc) algorithm and its performance on optimization problems"
                defined_params += 'trial_limit'.split()
        
        elif self.variant == 'FullyEmployed':
            mandatory_params += 'pop_size trial_limit'.split()
            
            if 'pop_size' in self.params:
                self.params['pop_size'] = int(self.params['pop_size'])
            else:
                self.params['pop_size'] = max(10, self.dimensions * 2)
            defined_params += 'pop_size'.split()
            
            if 'trial_limit' in self.params:
                self.params['trial_limit'] = int(self.params['trial_limit'])            
            else:
                self.params['trial_limit'] = int(self.params['pop_size'] * self.dimensions / 2) # Karaboga and Gorkemli 2014 - "A quick artificial bee colony (qabc) algorithm and its performance on optimization problems"
                defined_params += 'trial_limit'.split()
    
        else:
            assert False, f'Unknown variant! {self.variant}'

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)


    def _init_method(self):
        """Private method for initializing the ABC optimizer instance.
        Initializes and evaluates the population.

        Returns
        -------
        None
            Nothing
            
        """

        # Generate employed bees
        if self.variant == 'FullyEmployed':
            self.cS_em = np.array([Bee(self) for _ in range(self.params['pop_size'])], dtype=Bee)
        else:
            self.cS_em = np.array([Bee(self) for _ in range(self.params['pop_size']//2)], dtype=Bee)
        self.cS_em_v = np.copy(self.cS_em)
        self.trials_em = np.zeros(np.size(self.cS_em), dtype=np.int32)
        self.probability = np.zeros(np.size(self.cS_em))
        
        # Generate onlooker bees
        if not self.variant == 'FullyEmployed':
            self.cS_on = np.array([Bee(self) for _ in range(self.params['pop_size']//2)], dtype=Bee)
            self.cS_on_v = np.copy(self.cS_on)
            self.trials_on = np.zeros(np.size(self.cS_on), dtype=np.int32)
        
        self._evaluate_initial_candidates()
        n0 = 0 if self._cS0 is None else self._cS0.size
        
        self._initialize_X(self.cS_em)
        if not self.variant == 'FullyEmployed':
            self._initialize_X(self.cS_on)
        
        # Using specified particles initial positions
        for p in range(np.size(self.cS_em)):     
            if p < n0:
                self.cS_em[p] = self._cS0[p].copy()
            
        # Evaluate
        if n0 < np.size(self.cS_em):
            self._collective_evaluation(self.cS_em[n0:])
        if not self.variant == 'FullyEmployed':
            self._collective_evaluation(self.cS_on)

        # if all candidates are NaNs       
        if np.isnan([cP.f for cP in self.cS_em]).all():
            self._err_msg = 'ALL CANDIDATES FAILED TO EVALUATE'

        self._finalize_iteration()
    
        
    def _run(self):
        """Main loop of ABC method.

        Returns
        -------
        optimum: CandidateState
            Best solution found during the ABC optimization.
        """
        
        self._check_params()      
        self._init_method()

        while True:
            
            """employed bees phase"""                 
            for p, cP in enumerate(self.cS_em):
                
                self.cS_em_v[p] = cP.copy()
                
                informer = np.random.choice(np.delete(self.cS_em, p))
                d = np.random.randint(0, self.dimensions)
                phi = np.random.uniform(-1, 1)
                
                self.cS_em_v[p].X[d] = cP.X[d] + phi*(cP.X[d] - informer.X[d])
                
                self.cS_em_v[p].clip(self)

            self._collective_evaluation(self.cS_em_v)
            
            for p, cP in enumerate(self.cS_em_v):
                
                if cP < self.cS_em[p]:
                    self.cS_em[p] = cP.copy()
                    self.trials_em[p] = 0
                else:
                    self.trials_em[p] += 1
            
            if not self.variant == 'FullyEmployed':
            
                """probability update"""
                ranks = np.argsort(np.argsort(self.cS_em))
                self.probability = (np.max(ranks) - ranks) / np.sum(np.max(ranks) - ranks)
                
                # # original probability (fitness based)
                # fits = np.array([c.f for c in self.cS_em])
                # self.probability = (np.max(fits) - fits) / np.sum(np.max(fits) - fits)

                """onlooker bee phase"""
                for p, cP in enumerate(self.cS_on):
                    
                    self.cS_on_v[p] = cP.copy()
                    
                    informer = np.random.choice(self.cS_em, p=self.probability) 
                    d = np.random.randint(0, self.dimensions)
                    phi = np.random.uniform(-1, 1)
                    
                    self.cS_on_v[p].X[d] = cP.X[d] + phi*(cP.X[d] - informer.X[d])
                    
                    self.cS_on_v[p].clip(self)
    
                self._collective_evaluation(self.cS_on_v)
                
                for p, cP in enumerate(self.cS_on_v):
                    
                    if cP < self.cS_on[p]:
                        self.cS_on[p] = cP.copy()
                        self.trials_on[p] = 0
                    else:
                        self.trials_on[p] += 1

            """scout bee phase"""
            for p, cP in enumerate(self.cS_em):
                if self.trials_em[p] > self.params['trial_limit']:
                    cP.X = np.random.uniform(self.lb, self.ub)
                    self.trials_em[p] = 0
            
            if not self.variant == 'FullyEmployed':
                for p, cP in enumerate(self.cS_on):
                    if self.trials_on[p] > self.params['trial_limit']:
                        cP.X = np.random.uniform(self.lb, self.ub)
                        self.trials_on[p] = 0
            
            if self._finalize_iteration():
                break
        
        return self.best
