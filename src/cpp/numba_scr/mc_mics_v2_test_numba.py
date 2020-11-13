import itertools
import os
from multiprocessing import Pool, Process

import numpy as np
from joblib import Parallel


class AllDiffParallel:
    def __init__(self, model, num_prod, num_sup, num_perech, bools_list):
        self.model = model
        self.num_prod = num_prod
        self.num_sup = num_sup
        self.num_perech = num_perech
        self.bools_list = bools_list


    def all_diff_numba(self, i, j, k):
        print(i, ' - ',j, ' - ', k)
        # num of vars and bools in perech list (apprx 2 * 3=6)

        same_sup_bools = list(itertools.chain(
            *[self.bools_list[i_in][j][:k] + self.bools_list[i_in][j][k + 1:]
              for i_in in np.arange(self.num_prod).tolist()]
        ))
        self.model.AddBoolAnd(list(map(lambda d: d.Not(), same_sup_bools))).OnlyEnforceIf(self.bools_list[i][j][k])


    def run(self):
        with Pool(processes=4) as pool:
            # pool.imap_unordered(self.all_diff_numba, self.bools_list)
            for i in range(self.num_prod):  # per drug
                for j in range(self.num_sup):  # per supplier
                    #     Adds an all-different constrai12. Select one price per row of all perechs.
                    #     If one perech price is selected -> do not select other perech price variants
                    for k in range(self.num_perech + 1):
                        #     num of vars and bools in perech list (apprx 2 * 3=6)
                        pool.apply_async(self.all_diff_numba, args=(i, j, k))
                        # p = Process(target=self.all_diff_numba, args=(i, j, k))
                        # p.start()
                        # p.join()
        return self.model


    def run_joblib(self):
        with Parallel(n_jobs=4) as parallel:
            for i in range(self.num_prod):  # per drug
                #     print(i)
                for j in range(self.num_sup):  # per supplier
                    #     Adds an all-different constrai12. Select one price per row of all perechs.
                    #     If one perech price is selected -> do not select other perech price variants
                    for k in range(self.num_perech + 1):
                        #     num of vars and bools in perech list (apprx 2 * 3=6)
                        same_sup_bools = list(itertools.chain(
                            *[self.bools_list[i_in][j][:k] + self.bools_list[i_in][j][k + 1:]
                              for i_in in np.arange(self.num_prod).tolist()]
                        ))

                        self.model.AddBoolAnd(list(map(lambda d: d.Not(), same_sup_bools))).OnlyEnforceIf(
                            self.bools_list[i][j][k])
        return self.model
