import numpy as np
np.get_include()
cimport numpy as np
cimport cython
from ortools.sat.python import cp_model

model = cp_model.CpModel()

# @cython.boundscheck(False)
# @cython.wraparound(False)
def all_diff(int num_prod, int num_sup, int num_perech, list bools_list):
    print("num_prod ", num_prod, " - ", type(num_prod))
    print("num_sup ", num_sup, " - ", type(num_sup))
    print("num_perech ", num_perech, " - ", type(num_perech))
    print("bools_list ", bools_list, " - ", type(bools_list))
    print("bools_list ", bools_list[1][1][1], " - ", type(bools_list[1][1][1]))

    # cdef np.ndarray[:,:,:] all_diff_arr = np.ndarray[num_prod, num_sup, num_perech]
    cdef np.ndarray all_diff_arr = np.ndarray[num_prod, num_sup, num_perech]
    cdef np.ndarray bools_list_arr = np.array(bools_list)
    cdef unsigned int i, j, k, i_in


    for i in range(num_prod):  # per drug
        for j in range(num_sup):  # per supplier
#             # Adds an all-different constrai12. Select one price per row of all perechs.
#             # If one perech price is selected -> do not select other perech price variants
            for k in range(num_perech + 1):
#                 cdef np.ndarray[:] tmp_arr = np.delete(bools_list_arr[:,j], k, 1).flatten()
                all_diff_arr[i,j,k] = np.delete(bools_list_arr[:,j], k, 1).flatten()
                for i_in in range(all_diff_arr[i,j,k]):
                    all_diff_arr[i,j,k][i_in] = all_diff_arr[i,j,k][i_in].Not()
                    print("as")
    
    return all_diff_arr
