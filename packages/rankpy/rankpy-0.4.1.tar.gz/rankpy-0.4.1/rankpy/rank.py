# Import pkgs
import numpy as np
from pandas import DataFrame, concat, cut
from quadprog import solve_qp
from jenkspy import jenks_breaks

# Constants

# Functions
def check_symmetry(m):
    # https://stackoverflow.com/questions/42908334/checking-if-a-matrix-is-symmetric-in-numpy
    return np.allclose(m, m.T, equal_nan=True)


def get_r2(Y_bar, star_binary, weights_df_ind):
    """
    Compute r^2.
    Calculates r-squared based upon the average flows, number of comparisons, and ranking.
    :param Y_bar: list-like (i.e. avg_flow)
    :param star_binary: numpy array (nee ranks)
    :param weights_df_ind: DataFrame (nee comparisons_)
    :return float
    """ 
    Y_bar = DataFrame(Y_bar).fillna(0).to_numpy()  # avg_flow, but modified for use in the denominator
    num = []  # numerator
    for i in range(0,Y_bar.shape[0]):
        for j in range(i+1, Y_bar.shape[0]):
            tmp = (star_binary[j]-star_binary[i])*(weights_df_ind[i,j])
            num.append(tmp)

    numerator = np.square(np.linalg.norm(num, ord=2))

    den = []  # denominator
    for i in range(0,Y_bar.shape[0]-1):
        for j in range(i+1, Y_bar.shape[0]):
            tmp = Y_bar[i,j]*(weights_df_ind[i,j])
            den.append(tmp)
            
    denominator = np.square(np.linalg.norm(den, ord=2))

    return numerator/denominator


def apply_hodge(df_flow, df_weights):
    """""
    Apply HodgeRank to flows and weights
    :param df_flow: DataFrame of flows
    :param df_weights: DataFrame of weights
    :return: hodge_ranking
    """""
    Y_bar = df_flow.to_numpy()

    # Weighting matrix is just laplacian
    weights_df_ind = np.where(df_weights > 1, 1, df_weights)

    # Compute HodgeRank
    delo = -1*weights_df_ind
    np.fill_diagonal(delo, weights_df_ind.sum(axis=1))
    tdelo = np.linalg.pinv(delo)
    tdelo = -1*tdelo
    y_binary = DataFrame(Y_bar).fillna(0).sum(axis=1)
    hodge_ranking = np.matmul(y_binary, tdelo)

    return hodge_ranking, weights_df_ind


def hodge_rank(flows_, comparisons_, use_unweighted_comparisons=True, show_r2=True):
    """
    :Info: Given two matrices of (1) net flows between pairs and (2) total number of comparisons,
            produce a Hodge ranking.  
            Ensure that each matrix shares indices and column headers (within and across matrices).
    :param flows_: DataFrame
    :param comparisons_: DataFrame
    :param use_unweighted_comparisons: bool (True if comparisons matrix should only indicate adjacency as binary)
    :param show_r2: bool (True if r^2 should be displayed)
    :return options_with_hodge_rank: DataFrame
    """
    THRESHOLD_R2 = 0.33  # Could make this a passed parameter

    # TODO: ensure that README explains variable mappings (e.g. delta_naught, Y_bar)
    # FUTURE: Allow flows & comparisons to be passed as numpy matrix (vs DataFrame)

    # Check that comparisons matrix is symmetric
    if not check_symmetry(comparisons_):
        print(comparisons_)
        raise ValueError("Comparisons matrix is not symmetric")

    # Ensure that indices and columns (across both matrices) are the same
    if not ((flows_.columns.values == comparisons_.columns.values).all() 
        & (flows_.index.values == comparisons_.index.values).all()
        & (flows_.columns.values == comparisons_.index.values).all()):
        print(flows_.columns.values)
        print(comparisons_.columns.values)
        print(flows_.index.values)
        print(comparisons_.index.values)
        raise ValueError("Passed matrices have unmatched columns and indices.")

    # Divide flow (i.e. net pair preferences) by comparisons (i.e. weights) to get average flow
    # avg_flow = flows_.div(comparisons_, fill_value=0)  # i.e. Y_bar (Eq. 9) from Jiang paper
    ## We should ask for average flow as input, not raw flow
    avg_flow = flows_

    if use_unweighted_comparisons:  # Cap values at 1 (i.e. binary adjacency matrix)
        comparisons = np.where(comparisons_ > 1, 1, comparisons_)
    else:  # e.g. use an aggreate number of comparisons
        comparisons = comparisons_.to_numpy()
    
    delta_naught = -1*comparisons  # delta naught s (i.e. Eq. #25 in Jiang et al)
    np.fill_diagonal(delta_naught, comparisons.sum(axis=1)) # Need to fill i=j with sum of weights for each option
    mp_inv_delta_naught = np.linalg.pinv(delta_naught)  # Moore-Penrose pseudo-inverse (in case divide by 0)
    mp_inv_delta_naught = -1 * mp_inv_delta_naught  # Need to negate to get correct sign

    # Note net_flows will give equal weight to option pairs ranked once and those ranked many times
    net_flows = avg_flow.fillna(0).sum(axis=0)  # Use axis=0 (rows) to ensure highest ranked is positive edge weight; nee y_binary

    hodge_ranks = np.matmul( net_flows, mp_inv_delta_naught)  # (i.e s_star (Eq. 26) -- the Hodge ranking calculation)

    options_with_hodge_rank = DataFrame({'option':avg_flow.index.values, 'hodge_rank':hodge_ranks}).sort_values(by='hodge_rank', ascending=False)

    if show_r2:
        r2 = get_r2(avg_flow, hodge_ranks, comparisons)

        if r2 < THRESHOLD_R2:
            print(f"WARNING: r^2 is {r2} (which is lower than the threshold of {THRESHOLD_R2}.  This suggests the rank order may not be accurate representation of underlying data.")
        else:
            print(f"The r^2 is {r2} (which is higher than the threshold of {THRESHOLD_R2}.  This suggests the rank order does well at explaining underlying data.")

    return options_with_hodge_rank


def quadprog_solve_qp(P, q, G, h, A=None, b=None):
    # make sure P is symmetric 
    qp_G = .5 * (P + P.T) + np.eye(P.shape[0])*0.000000000001
    qp_a = -q
    if A is not None:
        qp_C = -np.vstack([A, G]).T
        qp_b = -np.hstack([b, h])
        meq = A.shape[0]
    else:  # no equality constraint
        qp_C = -G.T
        qp_b = -h
        meq = 0
    return solve_qp(qp_G, qp_a, qp_C, qp_b, meq)[0]


def quadprog_solve_qp_unconstr(P, q):
    # make sure P is symmetric 
    qp_G = .5 * (P + P.T) + np.eye(P.shape[0])*0.000000000001
    qp_a = -q
    return solve_qp(qp_G, qp_a)[0]


def get_upper_tri(arr_):
    """
    :param arr_: 
    :returns vec: np.array
    """
    vec = []
    for i in range(1, arr_.shape[1]):
        for j in range(0, i):
            # Create a vector of the upper triangle of the array
            vec.append(arr_[j,i])
    # convert list to numpy array
    vec = np.array(vec)
    return vec


def create_inputs(ex_df, ex_weights):
    """
    Info:
    :param ex_df: 
    :param ex_weights: 
    :returns gradient_matrix, flow_vec, constr_matrix
    """
    # Turn upper triangle of gradient matrix into a vector
    comp_vec = get_upper_tri(ex_weights)

    # Replace all >1 values with 1
    comp_vec = np.where(comp_vec > 1, 1, comp_vec)

    # Turn upper triangle of gradient matrix into a vector
    flow_vec = get_upper_tri(ex_df)

    # Remove values from flow_vec that are 0 in comp_vec
    flow_vec = flow_vec[comp_vec != 0]

    count = 0
    comp_df = DataFrame(comp_vec, columns=['comp'])
    for j in range(1,ex_df.shape[0]):
        for i in range(0,j):
            row = i
            col = j
            # Add index to comp_df
            comp_df.loc[count, 'row'] = row
            comp_df.loc[count, 'col'] = col
            count = count + 1

    comp_df = comp_df[comp_df['comp'] != 0]
    comp_df.drop(columns=['comp'], inplace=True)


    # Create a dataframe that has 360 rows and 48 columns
    nRows = comp_df.shape[0]
    nCols = ex_df.shape[0]
    gradient_matrix = DataFrame(index=range(nRows),columns=range(nCols))
    gradient_matrix.fillna(0, inplace=True)


    for i in range(0, nRows):
        # Get the row and column of the gradient matrix we want to fill in
        row = int(comp_df.iloc[i,0])
        col = int(comp_df.iloc[i,1])
        # Fill in the gradient matrix
        gradient_matrix.iloc[i,col] = 1
        gradient_matrix.iloc[i,row] = -1

    gradient_matrix = gradient_matrix.to_numpy()

    constr_matrix = np.zeros((nCols, nCols))

    return gradient_matrix, flow_vec, constr_matrix


def hodge_rank_using_qp(gradient_matrix, flow_vec, constr_matrix, nCols):
    """
    :param gradient_matrix:
    :param flow_vec: 
    :param constr_matrix: 
    :param nCols: int
    :returns solution: 
    """
    M = gradient_matrix
    P = np.matmul(M.T, M)
    q = -np.matmul(M.T, flow_vec)
    G = constr_matrix
    h = np.zeros((nCols,1))

    # Recast all arrays
    P = P.astype(np.double)
    q = q.astype(np.double).reshape(nCols)
    G = G.astype(np.double)
    h = h.astype(np.double).reshape(nCols)

    solution = quadprog_solve_qp_unconstr(P, q)

    return solution


def get_normed_ranking(hodge_ranking_df, avg_flow_df, weights_df_ind, uncons_r2, gradient_matrix, flow_vec):
    """
    Get normed ranking
    :param hodge_ranking_df: DataFrame
    :param avg_flow_df: DataFrame
    :param weights_df_ind: 
    :param uncons_r2: 
    :param gradient_matrix: 
    :param flow_vec: 
    :returns hodge_rank_output
    """
    
    # Loop over index of sorterd solution vector
    ranked = []
    for idx in hodge_ranking_df.sort_values(by=['binary_ranking'], ascending=True).index.values:
        # Append the index of the avg_flow dataframe
        ranked.append(idx)

    ranked = np.array(ranked)


    # Create a dataframe that saves the r2 value for each pair
    r2_df = DataFrame(columns=['r2', 'index_high', 'index_low'])

    for r in range(0, len(ranked)-1):

        nCols = avg_flow_df.shape[0]

        constr_matrix = np.zeros((nCols,nCols))
        constr_matrix[r,0] = -1
        constr_matrix[r+1,0] = 1

        M = gradient_matrix
        P = np.matmul(M.T, M)
        q = -np.matmul(M.T, flow_vec)
        G = constr_matrix.T
        h = np.zeros((nCols,1))

        # Recast all arrays
        P = P.astype(np.double)
        q = q.astype(np.double).reshape(nCols)
        G = G.astype(np.double)
        h = h.astype(np.double).reshape(nCols)

        solution = quadprog_solve_qp(P, q, G, h, A=None, b=None)

        r2 = get_r2(avg_flow_df.to_numpy(), solution, weights_df_ind)

        # Get diff in binary ranking
        diff = hodge_ranking_df.iloc[r]['binary_ranking'] - hodge_ranking_df.iloc[r+1]['binary_ranking']

        # Label index_high and index_low with 'charge' in binary ranking
        index_high = hodge_ranking_df.iloc[r]['charge']
        index_low = hodge_ranking_df.iloc[r+1]['charge']

        
        # Save r,  r+1, and r2 to dataframe
        tmp = DataFrame({'r2': r2, 'index_high': index_high, 'index_low': index_low, 'score_diff': diff}, index=[0])
        r2_df = concat([r2_df, tmp], ignore_index=True)

    # Pull in the unconstrianed r2 value and compute delta_r2
    r2_df['uncons_r2'] = uncons_r2
    r2_df['delta_r2'] = r2_df['r2'] - r2_df['uncons_r2']


    # Create a df that is merge of r2_df and hodge_ranking_df
    hodge_rank_output = r2_df.merge(hodge_ranking_df, left_on='index_high', right_on='charge', how='right')

    # Create rank col that is cumsum of delta_r2
    hodge_rank_output.sort_values(by=['binary_ranking'], ascending=True)
    hodge_rank_output['cum_delr2'] = hodge_rank_output['delta_r2'].cumsum()

    # Start rank at 1 and subtract delta_r2 from previous row
    hodge_rank_output['rank'] = 1
    for i in range(1, hodge_rank_output.shape[0]):
        hodge_rank_output['rank'].iloc[i] = hodge_rank_output['rank'].iloc[i-1] + hodge_rank_output['delta_r2'].iloc[i-1]
        

    # Create jenks breaks for rank
    breaks = jenks_breaks(hodge_rank_output['rank'], 4)


    hodge_rank_output['cut_jenks'] = cut(
                                        hodge_rank_output['rank'],
                                        bins=breaks,
                                        labels=['1st', '2nd', '3rd', '4th'],
                                        include_lowest=True
                                    )


    # Convert rank to a variable between 0 and 1\
    hodge_rank_output['rank_norm'] = (hodge_rank_output['rank'] - hodge_rank_output['rank'].min()) / (hodge_rank_output['rank'].max() - hodge_rank_output['rank'].min())

    return hodge_rank_output