# -*- coding: utf-8 -*-
"""
Mutualistic Multi-Optimization
"""

import numpy as np
from ._optimizer import Optimizer, CandidateState 
from scipy.interpolate import interp1d # need this for akb_model
from scipy.stats import cauchy

"""PSO Particle class"""
class Particle(CandidateState):
    def __init__(self, optimizer: Optimizer):
        CandidateState.__init__(self, optimizer)        
        self.V = np.full(optimizer.dimensions, np.nan)
        
"""DE Solution class"""     
class Solution(CandidateState):
    def __init__(self, optimizer: Optimizer):
        CandidateState.__init__(self, optimizer)        
        self.CR = None
        self.F = None
        self.V = np.full(optimizer.dimensions, np.nan) # mutant vector

"""ABC Bee class"""
Bee = CandidateState

"""Mutualistic Multi-Optimization class"""
class MMO(Optimizer):
    
    def __init__(self):
        """Initialization"""
        Optimizer.__init__(self)

        self.params = {}        
        self.methods = {}

    def _check_params(self):
        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []
        
        if not self.methods:
            self.methods = {'PSO': 'Vanilla', 
                           'FWA': 'Rank'}
            
        assert len(self.methods) >= 2, \
            'optimizer.methods should provide at least 2 optimization methods'
        
        if 'PSO' in self.methods:      
            
            if 'swarm_size' in self.params:
                self.params['swarm_size'] = int(self.params['swarm_size'])
            
            # default variant
            if self.methods['PSO'] is None: 
                self.methods['PSO'] = 'Vanilla'
    
            if self.methods['PSO'] == 'Vanilla':
                mandatory_params += 'swarm_size inertia cognitive_rate social_rate'.split()
                if 'swarm_size' not in self.params:
                    self.params['swarm_size'] = max(10, self.dimensions)
                    defined_params += 'swarm_size'.split()
                if 'inertia' not in self.params:
                    self.params['inertia'] = 0.72
                    defined_params += 'inertia'.split()
                if 'cognitive_rate' not in self.params:
                    self.params['cognitive_rate'] = 1.0
                    defined_params += 'cognitive_rate'.split()
                if 'social_rate' not in self.params:
                    self.params['social_rate'] = 1.0
                    defined_params += 'social_rate'.split()
                optional_params += 'akb_model akb_fun_start akb_fun_stop'.split()
            elif self.methods['PSO'] == 'TVAC':
                mandatory_params += 'swarm_size inertia'.split()
                if 'swarm_size' not in self.params:
                    self.params['swarm_size'] = max(10, self.dimensions)
                    defined_params += 'swarm_size'.split()
                if 'inertia' not in self.params:
                    self.params['inertia'] = 0.72
                    defined_params += 'inertia'.split()
                optional_params += 'akb_model akb_fun_start akb_fun_stop'.split()
            else:
                assert False, f"Unknown PSO variant! {self.methods['PSO']}"
        
        if 'FWA' in self.methods:
            
            self.cX = None
            
            if 'n' in self.params:
                self.params['n'] = int(self.params['n'])
            if 'm1' in self.params:
                self.params['m1'] = int(self.params['m1'])
            if 'm2' in self.params:
                self.params['m2'] = int(self.params['m2'])
                
            # default variant
            if self.methods['FWA'] is None: 
                self.methods['FWA'] = 'Rank'
            
            if self.methods['FWA'] == 'Vanilla':
                mandatory_params += 'n m1 m2'.split()
                if 'n' not in self.params:
                    self.params['n'] = self.dimensions
                    defined_params += 'n'.split()
                if 'm1' not in self.params:
                    self.params['m1'] = self.dimensions // 2
                    defined_params += 'm1'.split()
                if 'm2' not in self.params:
                    self.params['m2'] = self.dimensions // 2
                    defined_params += 'm2'.split()    
                optional_params += ''.split()
            elif self.methods['FWA'] == 'Rank':
                mandatory_params += 'n m1 m2'.split()
                if 'n' not in self.params:
                    self.params['n'] = self.dimensions
                    defined_params += 'n'.split()
                if 'm1' not in self.params:
                    self.params['m1'] = self.dimensions // 2
                    defined_params += 'm1'.split()
                if 'm2' not in self.params:
                    self.params['m2'] = self.dimensions // 2
                    defined_params += 'm2'.split()
                optional_params += ''.split()
            else:
                assert False, f"Unknown FWA variant \'{self.methods['FWA']}\'"
            
            if self.constraints > 0:
                assert self.methods['FWA'] == 'Rank', f"FWA variant '{self.methods['FWA']}' does not support constraints! Use 'Rank' method instead"
                
        if 'DE' in self.methods:
            
            if 'pop_init' in self.params:
                self.params['pop_init'] = int(self.params['pop_init'])
                
            # default variant
            if self.methods['DE'] is None: 
                self.methods['DE'] = 'SHADE'
            
            if self.methods['DE'] == 'SHADE':
                mandatory_params += 'pop_init f_archive hist_size p_mutation'.split()
                if 'pop_init' not in self.params:
                    self.params['pop_init'] = self.dimensions * 18
                    defined_params += 'pop_init'.split()
                if 'f_archive' not in self.params:
                    self.params['f_archive'] = 2.6
                    defined_params += 'f_archive'.split()
                if 'hist_size' not in self.params: # a.k.a. H
                    self.params['hist_size'] = 6
                    defined_params += 'hist_size'.split()
                if 'p_mutation' not in self.params:
                    self.params['p_mutation'] = 0.11
                    defined_params += 'p_mutation'.split()    
                optional_params = ''.split()
            elif self.methods['DE'] == 'LSHADE':
                mandatory_params += 'pop_init f_archive hist_size p_mutation'.split()
                if 'pop_init' not in self.params:
                    self.params['pop_init'] = self.dimensions * 18
                    defined_params += 'pop_init'.split()
                if 'f_archive' not in self.params:
                    self.params['f_archive'] = 2.6
                    defined_params += 'f_archive'.split()
                if 'hist_size' not in self.params: # a.k.a. H
                    self.params['hist_size'] = 6
                    defined_params += 'hist_size'.split()
                if 'p_mutation' not in self.params:
                    self.params['p_mutation'] = 0.11
                    defined_params += 'p_mutation'.split()  
                optional_params = ''.split()
            else:
                assert False, f"Unknown DE variant! {self.methods['DE']}"

            if self.constraints > 0:
                assert False, 'DE does not support constraints'

        if 'ABC' in self.methods:
            
            # default variant
            if self.methods['ABC'] is None: 
                self.methods['ABC'] = 'Vanilla'
            
            if self.methods['ABC'] == 'Vanilla':
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
            
            elif self.methods['ABC'] == 'FullyEmployed':
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
                assert False, f"Unknown ABC variant! {self.methods['ABC']}"

        if 'PSO' in self.methods:
            
            """ Anakatabatic Inertia a.k.a. Polynomial PFIDI """
            if self.params['inertia'] == 'anakatabatic':
                assert ('akb_fun_start' in defined_params \
                        and 'akb_fun_stop' in defined_params) \
                        or 'akb_model' in defined_params, \
                        'Anakatabatic inertia requires either akb_model parameter or akb_fun_start and akb_fun_stop parameters'
                optional_params += 'akb_fun_start akb_fun_stop'.split()
                
                if 'akb_model' in defined_params:                    
                    optional_params += 'akb_model'.split()
    
                    if self.params['akb_model'] in ['FlyingStork', 'MessyTie', 'RightwardPeaks', 'OrigamiSnake']:   # w-list-based named akb_models                
                        if self.params['akb_model'] == 'FlyingStork':
                            w_start = [-0.86, 0.24, -1.10, 0.75, 0.72]
                            w_stop = [-0.81, -0.35, -0.26, 0.64, 0.60]
                            splinetype = 'linear'
                            if self.methods['PSO'] != 'Vanilla':
                                self._log('Warning: akb_model \'FlyingStork\' was designed for Vanilla PSO')                    
                        elif self.params['akb_model'] == 'MessyTie':
                            w_start = [-0.62, 0.18, 0.65, 0.32, 0.77]
                            w_stop = [0.36, 0.73, -0.62, 0.40, 1.09]
                            splinetype = 'linear'
                            if self.methods['PSO'] != 'Vanilla':
                                self._log('Warning: akb_model \'MessyTie\' was designed for Vanilla PSO')   
                        elif self.params['akb_model'] == 'RightwardPeaks':
                            w_start = [-1.79, -0.33, 2.00, -0.67, 1.30]
                            w_stop = [-0.91, -0.88, -0.84, 0.67, -0.36]
                            splinetype = 'linear'
                            if self.methods['PSO'] != 'TVAC':
                                self._log('Warning: akb_model \'RightwardPeaks\' was designed for TVAC PSO')
                        elif self.params['akb_model'] == 'OrigamiSnake':
                            w_start = [-1.36, 2.00, 1.00, -0.60, 1.22]
                            w_stop = [0.30, 1.03, -0.21, 0.40, 0.06]
                            splinetype = 'linear'
                            if self.methods['PSO'] != 'TVAC':
                                self._log('Warning: akb_model \'OrigamiSnake\' was designed for TVAC PSO')
                        # code shared for all w-list-based named akb_models
                        Th = np.linspace(np.pi/4, 5*np.pi/4, 5)
                        self.params['akb_fun_start'] = \
                                            interp1d(Th, w_start, kind=splinetype)
                        self.params['akb_fun_stop'] = \
                                            interp1d(Th, w_stop, kind=splinetype) 
                    else:
                        if self.params['akb_model'] != 'Languid':
                            self._log('Warning: Unknown akb_model. Defaulting to \'Languid\'')
                            self.params['akb_model'] = 'Languid'
                    if self.params['akb_model'] == 'Languid':
                        def akb_fun_languid(Th):
                            w = (0.72 + 0.05) * np.ones_like(Th)
                            for i, th in enumerate(Th):
                                if th < 4*np.pi/4: 
                                    w[i] = 0
                            return w
                        self.params['akb_fun_start'] = akb_fun_languid
                        self.params['akb_fun_stop'] = akb_fun_languid 
        
        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)

        
    def _init_method(self):
               
        # not sure if this is necessary
        self.lb = np.array(self.lb)
        self.ub = np.array(self.ub)
               
        if 'PSO' in self.methods:
            
            """ Initialize PSO """
            # Bounds for velocity
            self.v_max = 0.2 * (self.ub - self.lb)
    
            # Generate a swarm
            self.cS = np.array([Particle(self) for c in range(self.params['swarm_size'])], dtype=Particle)
            
            # Prepare arrays
            self.dF = np.full(self.params['swarm_size'], np.nan)
    
            # Generate initial positions
            self._initialize_X(self.cS)
            for p in range(self.params['swarm_size']):
                
                # Using specified particles initial positions
                if self.X0:
                    if p < np.shape(self.X0)[0]:
                        self.cS[p].X = self.X0[p]
                        
                # Generate velocity
                self.cS[p].V = np.random.uniform(-self.v_max, self.v_max)
    
                # No fitness change at the start
                self.dF[p] = 0.0
    
            # Evaluate
            self._collective_evaluation(self.cS)   
            
            # if all candidates are NaNs       
            if np.isnan([cP.f for cP in self.cS]).all():
                self._err_msg = 'ALL CANDIDATES FAILED TO EVALUATE'

            # Use initial particles as best ones
            self.cB = np.array([cP.copy() for cP in self.cS])
            
            # Update the overall best
            self.p_best = np.argmin(self.cB)
                
            # # Update history
            # #self.results.cHistory = [self.cB[self.p_best].copy()] # superseded by progress_log()
            # self.progress_log()
            
            self.BI = np.zeros(self.params['swarm_size'], dtype=int)
            self.TOPO = np.zeros([self.params['swarm_size'], self.params['swarm_size']], dtype=np.bool_)
    
            self._reinitialize_topology()
            self._find_neighbourhood_best()
        
        if 'FWA' in self.methods:
            
            """ Initialize FWA """
            self.cX = np.array([CandidateState(self) for p in range(self.params['n'])])
            
            # Generate initial positions
            self._initialize_X(self.cX)
            
            # Using specified initial positions
            for p in range(self.params['n']):
                if self.X0:
                    if p < np.shape(self.X0)[0]:
                        self.cX[p].X = self.X0[p]
    
            # Evaluate all
            self._collective_evaluation(self.cX)
            
            # if all candidates are NaNs       
            if np.isnan([p.f for p in self.cX]).all():
                self._err_msg = 'ALL CANDIDATES FAILED TO EVALUATE'
    
            # Sort
            self.cX = np.sort(self.cX)
        
        if 'DE' in self.methods:
            
            """ Initialize DE """
            # Generate a population
            self.Pop = np.array([Solution(self) for c in \
                                 range(self.params['pop_init'])], dtype=Solution)
            
            # Generate a trial population
            self.Trials = np.array([Solution(self) for c in \
                                    range(self.params['pop_init'])], dtype=Solution)
            
            # Initalize Archive
            self.A = np.empty([0])
            
            # Prepare historical memory
            self.M_CR = np.full(self.params['hist_size'], 0.5)
            self.M_F = np.full(self.params['hist_size'], 0.5)
    
            # Generate initial positions
            n0 = 0 if self._cS0 is None else self._cS0.size
            
            self._initialize_X(self.Pop)
            
            # Using specified particles initial positions
            for i in range(self.params['pop_init']):
                if i < n0:
                    self.Pop[i] = self._cS0[i].copy()

            # Evaluate
            self._collective_evaluation(self.Pop)
            
            # if all candidates are NaNs       
            if np.isnan([p.f for p in self.Pop]).all():
                self._err_msg = 'ALL CANDIDATES FAILED TO EVALUATE'
        
        if 'ABC' in self.methods:
            
            """ Initialize ABC """
            # Generate employed bees
            if self.methods['ABC'] == 'FullyEmployed':
                self.ABC_cS_em = np.array([Bee(self) for _ in range(self.params['pop_size'])], dtype=Bee)
            else:
                self.ABC_cS_em = np.array([Bee(self) for _ in range(self.params['pop_size']//2)], dtype=Bee)
            self.ABC_cS_em_v = np.copy(self.ABC_cS_em)
            self.trials_em = np.zeros(np.size(self.ABC_cS_em), dtype=np.int32)
            self.probability = np.zeros(np.size(self.ABC_cS_em))
            
            # Generate onlooker bees
            if not self.methods['ABC'] == 'FullyEmployed':
                self.ABC_cS_on = np.array([Bee(self) for _ in range(self.params['pop_size']//2)], dtype=Bee)
                self.ABC_cS_on_v = np.copy(self.ABC_cS_on)
                self.trials_on = np.zeros(np.size(self.ABC_cS_on), dtype=np.int32)
            
            self._evaluate_initial_candidates()
            n0 = 0 if self._cS0 is None else self._cS0.size
            
            # Random position
            self._initialize_X(self.ABC_cS_em)
            if not self.methods['ABC'] == 'FullyEmployed':
                self._initialize_X(self.ABC_cS_on)
            
            # Using specified particles initial positions
            for p in range(np.size(self.ABC_cS_em)):
                if p < n0:
                    self.ABC_cS_em[p] = self._cS0[p].copy()
                
            # Evaluate
            if n0 < np.size(self.ABC_cS_em):
                self._collective_evaluation(self.ABC_cS_em[n0:])
            if not self.methods['ABC'] == 'FullyEmployed':
               self._collective_evaluation(self.ABC_cS_on)

            # if all candidates are NaNs       
            if np.isnan([cP.f for cP in self.ABC_cS_em]).all():
                self._err_msg = 'ALL CANDIDATES FAILED TO EVALUATE'
        
        """ After all methods are initialized... """
        self._finalize_iteration()
 
       
    """ PSO functions """
        
    def _reinitialize_topology(self, k=3):
        self.TOPO[:, :] = False
        for p in range(self.params['swarm_size']):
            links = np.random.randint(self.params['swarm_size'], size=k)
            self.TOPO[p, links] = True
            self.TOPO[p, p] = True  

    def _find_neighbourhood_best(self):
        for p in range(self.params['swarm_size']):
            links = np.where(self.TOPO[p, :])[0]
            #best = np.argmin(self.BF[links])
            p_best = np.argmin(self.cB[links])
            p_best = links[p_best]
            self.BI[p] = p_best


    """ FWA functions """
        
    def _explosion(self):
        eps=0.001
        amp=10
        a=0.01
        b=10
        F = np.array([cP.f for cP in self.cX])
        fmin = np.min(F)
        fmax = np.max(F)
        
        explosion_sparks = []
        for p in range(self.params['n']):
               
            cFw = self.cX[p].copy()
            #print(cFw.X)
            
            if self.methods['FWA'] == 'Vanilla':
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
                
            if self.methods['FWA'] == 'Rank':
                
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

        return explosion_sparks        
    
    def _gaussian_mutation(self):
        mutation_sparks = []
        for j in range(self.params['m2']):
            cFw = self.cX[np.random.randint(self.params['n'])].copy()
            g = np.random.normal(1, 1)
            for k in range(self.dimensions):
                if(np.random.choice([True, False])):
                    cFw.X[k] *= g
            mutation_sparks.append(cFw)
        return mutation_sparks  

    def _mapping_rule(self, sparks, lb, ub, dimension):
        for i in range(len(sparks)):
            for j in range(dimension):
                if(sparks[i].X[j] > ub[j] or sparks[i].X[j] < lb[j]):
                    sparks[i].X[j] = lb[j] + \
                        (sparks[i].X[j] - lb[j]) % (ub[j] - lb[j])
  
    def _selection(self, sparks, n, function):        
        self._collective_evaluation(sparks)
        self.cX = np.append(self.cX, sparks)   

    def _min_max_round(self, s, smin, smax):
        return int(np.round(np.min([np.max([s, smin]), smax]))) 

    def _round(self, s, m, a, b):
        if (s < a * m):
            return round(a * m)
        elif (s > b * m):
            return round(b * m)
        else:
            return round(s)
    
    
    """ DE functions """
    
    # no special DE functions
    
    
    """ ABC functions """
    
    # no special ABC functions
        

    """ MMO run function """
    def _run(self):
        
        self._check_params()      
        self._init_method()

        """ Prepare PSO """
        if 'PSO' in self.methods:   
            if 'inertia' in self.params.keys():
                w = self.params['inertia']
            if 'cognitive_rate' in self.params.keys():
                c1 = self.params['cognitive_rate']
            if 'cognitive_rate' in self.params.keys():
                c2 = self.params['social_rate']

        """ Prepare FWA """
        if 'FWA' in self.methods:
            n = self.params['n']
        
        """ Prepare DE """
        # no special preparement needed
        
        """ Prepare ABC """
        # no special preparement needed
        
        """ Main run loop """
        while True:
            
            """ PSO iteration """
            if 'PSO' in self.methods:
                R1 = np.random.uniform(0, 1, [self.params['swarm_size'], self.dimensions])
                R2 = np.random.uniform(0, 1, [self.params['swarm_size'], self.dimensions])
    
                if self.params['inertia'] == 'LDIW':
                    w = 1.0 - (1.0 - 0.4) * self._progress_factor()
    
                if self.methods['PSO'] == 'TVAC':
                    c1 = 2.5 - (2.5 - 0.5) * self._progress_factor()
                    c2 = 0.5 + (2.5 - 0.5) * self._progress_factor()
    
                if self.params['inertia'] == 'anakatabatic':  
                    theta = np.arctan2(self.dF, np.min(self.dF))
                    theta[theta < 0] = theta[theta < 0] + 2 * np.pi  # 3rd quadrant
                    # fix for atan2(0,0)=0
                    theta0 = theta < 1e-300
                    theta[theta0] = np.pi / 4 + \
                        np.random.rand(np.sum(theta0)) * np.pi
                    w_start = self.params['akb_fun_start'](theta)
                    w_stop = self.params['akb_fun_stop'](theta)
                    #print(w_start)
                    w = w_start * (1 - self._progress_factor()) \
                        + w_stop * self._progress_factor()

                w = w * np.ones(self.params['swarm_size']) # ensure w is a vector
                
                # Calculate new velocity and new position
                
                for p, cP in enumerate(self.cS):
    
                    cP.V = w[p] * cP.V + \
                                   c1 * R1[p, :] * (self.cB[p].X - cP.X) + \
                                   c2 * R2[p, :] * (self.cB[self.BI[p]].X - cP.X)
                    cP.X = cP.X + cP.V        
                    
                    # Correct position to the bounds
                    cP.clip(self)
                    
                # Get old fitness
                f_old = np.array([cP.f for cP in self.cS])
    
                # Evaluate swarm
                self._collective_evaluation(self.cS)
    
                for p, cP in enumerate(self.cS):
                    # Calculate dF
                    self.dF[p] = cP.f - f_old[p]
                    
                for p, cP in enumerate(self.cS):
                    # Update personal best
                    if cP <= self.cB[p]:
                        self.cB[p] = cP.copy()  
                
                # Update the overall best
                self.p_best = np.argmin(self.cB)
                
                # Update swarm topology
                if np.max(self.dF) >= 0.0:
                    self._reinitialize_topology()
                    
                # Find best particles in neighbourhood 
                self._find_neighbourhood_best()
            
            """ FWA iteration """
            if 'FWA' in self.methods:
                explosion_sparks = self._explosion()
                mutation_sparks = self._gaussian_mutation()
    
                #self._mapping_rule(sparks, self.lb, self.ub, self.dimensions)
                for cS in (explosion_sparks + mutation_sparks):
                    
                    ilb = cS.X < self.lb
                    cS.X[ilb] = self.lb[ilb]
                    iub = cS.X > self.ub
                    cS.X[iub] = self.ub[iub]
    
                    self.cX = np.append(self.cX, [cS])
    
                self._collective_evaluation(self.cX[n:])
    
                self.cX = np.sort(self.cX)[:n]
            
            """ DE iteration """
            if 'DE' in self.methods:
                K = 0 # memory index
                    
                S_CR = np.empty([0])
                S_F = np.empty([0])
                S_df = np.empty([0])
                
                # find pbest
                top = max(round(np.size(self.Pop) * self.params['p_mutation']), 1)
                pbest = np.random.choice(np.sort(self.Pop)[0:top])
                
                for p, t in zip(self.Pop, self.Trials):
                    
                    # Update CR, F
                    r = np.random.randint(self.params['hist_size'])
                    if np.isnan(self.M_CR[r]):
                        p.CR = 0
                    else:
                        p.CR = np.random.normal(self.M_CR[r], 0.1)
                        p.CR = np.clip(p.CR, 0, 1)
                    p.F = -1
                    while p.F <= 0:
                        p.F = min(cauchy.rvs(self.M_F[r], 0.1), 1)
                    
                    # Compute mutant vector
                    r1 = r2 = p
                    while r1 is r2 or r1 is p or r2 is p:
                        r1 = np.random.choice(self.Pop)
                        r2 = np.random.choice(np.append(self.Pop, self.A))
                    p.V = p.X + p.F * (pbest.X - p.X) + p.F * (r1.X - r2.X)
                    p.V = np.clip(p.V, (p.X + self.lb)/2, (p.X + self.ub)/2)
                    
                    # Compute trial vector
                    t.CR = p.CR
                    t.F = p.F
                    jrand = np.random.randint(self.dimensions)
                    for j in range(self.dimensions):
                        if np.random.rand() <= p.CR or j == jrand:
                            t.X[j] = p.V[j]
                        else:
                            t.X[j] = p.X[j]
    
                # Evaluate population
                self._collective_evaluation(self.Trials)
                
                # Survival for next generation
                for p, t in zip(self.Pop, self.Trials):
                    if t.f < p.f:
                        # Update external archive
                        self.A = np.append(self.A, p)
                        if np.size(self.A) > round(np.size(self.Pop) * self.params['f_archive']):
                            self.A = np.delete(self.A, 
                                               np.random.randint(np.size(self.A)))
                        S_CR = np.append(S_CR, t.CR) 
                        S_F = np.append(S_F, t.F)
                        S_df = np.append(S_df, p.f - t.f)
                        # Update population
                        p.X = np.copy(t.X)
                        p.f = t.f
    
                # Memory update
                if np.size(S_CR) != 0 and np.size(S_F) != 0:
                    w_DE = S_df / np.sum(S_df)
                    if np.isnan(self.M_CR[K]) or np.max(S_CR) < 1e-100:
                        self.M_CR[K] = np.nan
                    else:
                        self.M_CR[K] = np.sum(w_DE * S_CR**2) / np.sum(w_DE * S_CR)
                    self.M_F[K] = np.sum(w_DE * S_F**2) / np.sum(w_DE * S_F)
                    K += 1
                    if K >= self.params['hist_size']:
                        K = 0
                        
                # Linear Population Size Reduction (LPSR)
                if self.methods['DE'] == 'LSHADE':
                    N_init = self.params['pop_init']
                    N_new = round((4 - N_init) * self._progress_factor() + N_init)
                    if N_new < np.size(self.Pop):
                        self.Pop = np.sort(self.Pop)[:N_new]
                        self.Trials = self.Trials[:N_new]          
            
            """ ABC iteration """
            if 'ABC' in self.methods:
                
                """employed bees phase"""                 
                for p, cP in enumerate(self.ABC_cS_em):
                    
                    self.ABC_cS_em_v[p] = cP.copy()
                    
                    informer = np.random.choice(np.delete(self.ABC_cS_em, p))
                    d = np.random.randint(0, self.dimensions)
                    phi = np.random.uniform(-1, 1)
                    
                    self.ABC_cS_em_v[p].X[d] = cP.X[d] + phi*(cP.X[d] - informer.X[d])
                    
                    self.ABC_cS_em_v[p].clip(self)

                self._collective_evaluation(self.ABC_cS_em_v)
                
                for p, cP in enumerate(self.ABC_cS_em_v):
                    
                    if cP < self.ABC_cS_em[p]:
                        self.ABC_cS_em[p] = cP.copy()
                        self.trials_em[p] = 0
                    else:
                        self.trials_em[p] += 1
                
                if not self.methods['ABC'] == 'FullyEmployed':
                
                    """probability update"""
                    ranks = np.argsort(np.argsort(self.ABC_cS_em))
                    self.probability = (np.max(ranks) - ranks) / np.sum(np.max(ranks) - ranks)
                    
                    # # original probability (fitness based)
                    # fits = np.array([c.f for c in self.ABC_cS_em])
                    # self.probability = (np.max(fits) - fits) / np.sum(np.max(fits) - fits)

                    """onlooker bee phase"""
                    for p, cP in enumerate(self.ABC_cS_on):
                        
                        self.ABC_cS_on_v[p] = cP.copy()
                        
                        informer = np.random.choice(self.ABC_cS_em, p=self.probability) 
                        d = np.random.randint(0, self.dimensions)
                        phi = np.random.uniform(-1, 1)
                        
                        self.ABC_cS_on_v[p].X[d] = cP.X[d] + phi*(cP.X[d] - informer.X[d])
                        
                        self.ABC_cS_on_v[p].clip(self)
        
                    self._collective_evaluation(self.ABC_cS_on_v)
                    
                    for p, cP in enumerate(self.ABC_cS_on_v):
                        
                        if cP < self.ABC_cS_on[p]:
                            self.ABC_cS_on[p] = cP.copy()
                            self.trials_on[p] = 0
                        else:
                            self.trials_on[p] += 1

                """scout bee phase"""
                for p, cP in enumerate(self.ABC_cS_em):
                    if self.trials_em[p] > self.params['trial_limit']:
                        cP.X = np.random.uniform(self.lb, self.ub)
                        self.trials_em[p] = 0
                
                if not self.methods['ABC'] == 'FullyEmployed':
                    for p, cP in enumerate(self.ABC_cS_on):
                        if self.trials_on[p] > self.params['trial_limit']:
                            cP.X = np.random.uniform(self.lb, self.ub)
                            self.trials_on[p] = 0
                
                self.ABC_cS_all = list(self.ABC_cS_em)
                if not self.methods['ABC'] == 'FullyEmployed':
                    self.ABC_cS_all += list(self.ABC_cS_on)
                
                    
            """ Methods cooperating """
            bests = {}
            if 'PSO' in self.methods:
                bests['PSO'] = self.cB[self.p_best].f
            if 'FWA' in self.methods:
                bests['FWA'] = np.min(self.cX).f
            if 'DE' in self.methods:
                bests['DE'] = np.min(self.Pop).f
            if 'ABC' in self.methods:
                bests['ABC'] = np.min(self.ABC_cS_all).f
            
            if min(bests, key=bests.get) == 'PSO': # PSO best is THE BEST
                if 'FWA' in self.methods:
                    FWAworst = np.max(self.cX)
                    FWAworst.X = np.copy(self.best.X) 
                    FWAworst.f = self.best.f
                if 'DE' in self.methods:
                    DEworst = np.max(self.Pop)
                    DEworst.X = np.copy(self.best.X) 
                    DEworst.f = self.best.f
                if 'ABC' in self.methods:
                    ABCworst = np.max(self.ABC_cS_all)
                    ABCworst.X = np.copy(self.best.X) 
                    ABCworst.f = self.best.f
                #print('PSO updated others')
            elif min(bests, key=bests.get) == 'FWA': # FWA best is THE BEST
                if 'PSO' in self.methods:
                    PSOworst = np.max(self.cB)
                    PSOworst.X = np.copy(self.best.X) 
                    PSOworst.f = self.best.f 
                    PSOworst.dF = 0.0
                    self._find_neighbourhood_best()
                if 'DE' in self.methods:
                    DEworst = np.max(self.Pop)
                    DEworst.X = np.copy(self.best.X) 
                    DEworst.f = self.best.f
                if 'ABC' in self.methods:
                    ABCworst = np.max(self.ABC_cS_all)
                    ABCworst.X = np.copy(self.best.X) 
                    ABCworst.f = self.best.f
                #print('FWA updated others')
            elif min(bests, key=bests.get) == 'DE': # DE best is THE BEST
                if 'PSO' in self.methods:
                    PSOworst = np.max(self.cB)
                    PSOworst.X = np.copy(self.best.X) 
                    PSOworst.f = self.best.f 
                    PSOworst.dF = 0.0
                    self._find_neighbourhood_best()
                if 'FWA' in self.methods:
                    FWAworst = np.max(self.cX)
                    FWAworst.X = np.copy(self.best.X) 
                    FWAworst.f = self.best.f
                if 'ABC' in self.methods:
                    ABCworst = np.max(self.ABC_cS_all)
                    ABCworst.X = np.copy(self.best.X) 
                    ABCworst.f = self.best.f
                #print('DE updated others')
            elif min(bests, key=bests.get) == 'ABC': # ABC best is THE BEST
                if 'PSO' in self.methods:
                    PSOworst = np.max(self.cB)
                    PSOworst.X = np.copy(self.best.X) 
                    PSOworst.f = self.best.f 
                    PSOworst.dF = 0.0
                    self._find_neighbourhood_best()
                if 'FWA' in self.methods:
                    FWAworst = np.max(self.cX)
                    FWAworst.X = np.copy(self.best.X) 
                    FWAworst.f = self.best.f
                if 'DE' in self.methods:
                    DEworst = np.max(self.Pop)
                    DEworst.X = np.copy(self.best.X) 
                    DEworst.f = self.best.f
                #print('ABC updated others')
            
            """ Wrap up iteration """
            if self._finalize_iteration():
                break
        
        return self.best
    