# -*- coding: utf-8 -*-
""" FIREWORKS ALGORITHM method"""

import numpy as np
from ._optimizer import Optimizer, CandidateState 


class FWA(Optimizer):
    """Fireworks Algorithm method class.
    
    Attributes
    ----------
    variant : str
        Name of the FWA variant (``Vanilla`` or ``Rank``). Default: ``Rank``.
    params : dict
        A dictionary of FWA parameters.
        
    Returns
    -------
    optimizer : FWA
        FWA optimizer instance.
        
    """

    def __init__(self):
        Optimizer.__init__(self)

        self.variant = 'Rank'
        self.params = {}

    def _check_params(self):
        """Private method which performs some FWA-specific parameter checks
        and prepares the parameters to be validated by Optimizer._check_params.

        Returns
        -------
        None
            Nothing
            
        """
        
        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []
        
        if 'n' in self.params:
            self.params['n'] = int(self.params['n'])
        if 'm1' in self.params:
            self.params['m1'] = int(self.params['m1'])
        if 'm2' in self.params:
            self.params['m2'] = int(self.params['m2'])

        if self.variant == 'Vanilla':
            mandatory_params = 'n m1 m2'.split()
            if 'n' not in self.params:
                self.params['n'] = self.dimensions
                defined_params += 'n'.split()
            if 'm1' not in self.params:
                self.params['m1'] = self.dimensions // 2
                defined_params += 'm1'.split()
            if 'm2' not in self.params:
                self.params['m2'] = self.dimensions // 2
                defined_params += 'm2'.split()                
            optional_params = ''.split()
        elif self.variant == 'Rank':
            mandatory_params = 'n m1 m2'.split()
            if 'n' not in self.params:
                self.params['n'] = self.dimensions
                defined_params += 'n'.split()
            if 'm1' not in self.params:
                self.params['m1'] = self.dimensions // 2
                defined_params += 'm1'.split()
            if 'm2' not in self.params:
                self.params['m2'] = self.dimensions // 2
                defined_params += 'm2'.split()
            optional_params = ''.split()
        else:
            assert False, f'Unknown variant \'{self.variant}\''
        
        if self.constraints > 0:
            assert self.variant == 'Rank', f"Variant '{self.variant}' does not support constraints! Use 'Rank' variant instead"

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)

    def _init_method(self):
        """Private method for initializing the FWA optimizer instance.
        Initializes and evaluates the swarm.

        Returns
        -------
        None
            Nothing
            
        """

        self._evaluate_initial_candidates()

        self.cX = np.array([CandidateState(self) for p in range(self.params['n'])])
        
        # Generate initial positions
        n0 = 0 if self._cS0 is None else self._cS0.size
        
        self._initialize_X(self.cX)
        
        # Using specified initial positions
        for p in range(self.params['n']):
            if p < n0:
                self.cX[p] = self._cS0[p].copy()

        # Evaluate all
        if n0 < self.params['n']:
            self._collective_evaluation(self.cX[n0:])

        # if all candidates are NaNs       
        if np.isnan([p.f for p in self.cX]).all():
            self._err_msg = 'ALL CANDIDATES FAILED TO EVALUATE'

        # Sort
        self.cX = np.sort(self.cX)
        
        self._finalize_iteration()


    def _run(self):
        """Main loop of FWA method.

        Returns
        -------
        optimum: CandidateState
            Best solution found during the FWA optimization.
            
        """
        
        self._check_params()      
        self._init_method()
        
        n = self.params['n']

        while True:

            explosion_sparks = self._explosion()
            mutation_sparks = self._gaussian_mutation()

            # self.cX = np.array([], dtype=CandidateState)
            #self.__mapping_rule(sparks, self.lb, self.ub, self.dimensions)
            for cS in (explosion_sparks + mutation_sparks):
                
                ilb = cS.X < self.lb
                cS.X[ilb] = self.lb[ilb]
                iub = cS.X > self.ub
                cS.X[iub] = self.ub[iub]

                self.cX = np.append(self.cX, [cS])

            self._collective_evaluation(self.cX[n:])

            self.cX = np.sort(self.cX)[:n]

            if self._finalize_iteration():
                break
        
        return self.best


    def _explosion(self):
        """Private method for computing explosion sparks.

        Returns
        -------
        explosion_sparks : list of CandidateState
            FWA explosion sparks.
        """
        
        eps=0.001
        amp=10
        a=0.01
        b=10
        F = np.array([cP.f for cP in self.cX])
        fmin = np.nanmin(F)
        fmax = np.nanmax(F)
        
        explosion_sparks = []
        for p in range(self.params['n']):
               
            cFw = self.cX[p].copy()
            #print(cFw.X)
            
            if self.variant == 'Vanilla':
                # Number of sparks
                n1 = self.params['m1'] * (fmax - cFw.f + eps) / np.sum(fmax - F + eps)
                n1 = self._min_max_round(n1, self.params['m1'] * a, self.params['m2'] * b)
                
                # Amplitude
                A = amp * (cFw.f - fmin + eps) /  (np.sum(F - fmin) + eps)

                for j in range(n1):
                    for k in range(self.dimensions):
                        if (np.random.choice([True, False])):
                            cFw.X[k] += np.random.uniform(-A, A)
                    explosion_sparks.append(cFw.copy())
                
            if self.variant == 'Rank':
                
                # Number of sparks
                #vn1 = self.params['m1'] * (fmax - cFw.f + eps) / np.sum(fmax - F + eps)
                #vn1 = self._min_max_round(vn1, self.params['m1'] * a, self.params['m2'] * b)
                
                n1 = self.params['m1'] * (self.params['n'] - p)**1 / np.sum(np.arange(self.params['n']+1)**1)
                n1 = np.random.choice([int(np.floor(n1)), int(np.ceil(n1))])
                #print(self.cX[p].f, vn1, n1)
                
                # Amplitude
                #Ac = amp * (cFw.f - fmin + eps) / (np.sum(F - fmin) + eps)
                    
                #print('n1:', n1, 'A:', A)
                XX = np.array([cP.X for cP in self.cX])
                #print(XX.shape)
                
                # Uniform
                dev = np.std(XX, 0)
                avg_scale = np.average(np.sqrt(np.arange(self.params['n']) + 1))
                scale = np.sqrt(p + 1) / avg_scale
                
                #avg_scale = np.average(np.arange(self.params['n']) + 1)
                #scale = (p + 1) / avg_scale
                
                
                A = np.sqrt(12) / 2 * dev * scale
                A *= 1.5

                
                #cS = cFw.copy()
                for j in range(n1):
                    cFw.X = cFw.X + np.random.uniform(-A, A) * np.random.randint(0, 1, A.size)
                    
                    for k in range(self.dimensions):
                        if (np.random.choice([True, False])):
                            # Uniform
                            cFw.X[k] += np.random.uniform(-A[k], A[k])
                            # Normal
                            # cFw.X[k] += np.random.normal(-A[k], A[k])
                    
                    #print(cS.X)
                    explosion_sparks.append(cFw.copy())  

        #print('expl sparks:', len(explosion_sparks))
        #input(' > Press return to continue.')
        return explosion_sparks
    
    def _gaussian_mutation(self):
        """Private method for computing mutation sparks.

        Returns
        -------
        mutation_sparks : list of CandidateState
            FWA mutation sparks.
        """
        
        mutation_sparks = []
        for j in range(self.params['m2']):
            cFw = self.cX[np.random.randint(self.params['n'])].copy()
            g = np.random.normal(1, 1)
            for k in range(self.dimensions):
                if(np.random.choice([True, False])):
                    cFw.X[k] *= g
            mutation_sparks.append(cFw)

        #print('mut sparks:', np.sort([p.f for p in mutation_sparks]))
        #print('mut sparks:', len(mutation_sparks))
        return mutation_sparks
    
    def _min_max_round(self, s, smin, smax):
        """Private method for calculating round of min of max of input parameters.

        Parameters
        ----------
        s : float
            Preliminary population size.
        smin : float
            Preliminary population size.
        smax : float
            Preliminary population size.
             
        Returns
        -------
        min_max_round : int
            Round of min of max of input parameters.
        """
        
        return int(np.round(np.min([np.max([s, smin]), smax])))
    
    """
    def __explosion_operator(self, sparks, fw, function,
                             dimension, m, eps, amp, Ymin, Ymax, a, b):
        
        sparks_num = self.__round(m * (Ymax - function(fw) + eps) /
                                  (sum([Ymax - function(fwk) for fwk in self.X]) + eps), m, a, b)
        #print(sparks_num)

        amplitude = amp * (function(fw) - Ymax + eps) / \
            (sum([function(fwk) - Ymax for fwk in self.X]) + eps)

        for j in range(int(sparks_num)):
            sparks.append(np.array(fw))
            for k in range(dimension):
                if (np.random.choice([True, False])):
                    sparks[-1][k] += np.random.uniform(-amplitude, amplitude)
                    
    def __mapping_rule(self, sparks, lb, ub, dimension):
        for i in range(len(sparks)):
            for j in range(dimension):
                if(sparks[i].X[j] > ub[j] or sparks[i].X[j] < lb[j]):
                    sparks[i].X[j] = lb[j] + \
                        (sparks[i].X[j] - lb[j]) % (ub[j] - lb[j])

    def __selection(self, sparks, n, function):        
        self._collective_evaluation(sparks)
        self.cX = np.append(self.cX, sparks)

    def __round(self, s, m, a, b):
        if (s < a * m):
            return round(a * m)
        elif (s > b * m):
            return round(b * m)
        else:
            return round(s)
    """
