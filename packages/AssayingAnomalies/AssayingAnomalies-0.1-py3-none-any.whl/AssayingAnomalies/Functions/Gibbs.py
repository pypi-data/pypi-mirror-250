import numpy as np
from scipy.stats import truncnorm, multivariate_normal
from scipy.linalg import sqrtm

def q_draw(p, q, c, varu, print_level):
    # Check if the lengths of p and q are equal. If not, raise an error.
    if len(p) != len(q):
        raise ValueError("p and q are of different lengths.")

    # Check if c and varu are scalar values. If not, raise an error.
    if not np.isscalar(c) or not np.isscalar(varu):
        raise ValueError("c and varu should be scalars.")

    # Create a boolean array where True indicates non-zero elements in q.
    q_nonzero = q != 0

    # Duplicate each element in p and q to create p2 and q_double, both are 2D arrays.
    p2 = np.tile(p, (2, 1)).T
    q_double = np.tile(q, (2, 1)).T

    # Define a constant to determine how many elements to skip in the loop.
    n_skip = 2

    # Create an array where each element is the remainder of division by n_skip.
    mod_p = np.mod(np.arange(len(p)), n_skip)

    # Calculate u for all pairs in q_double:
    # cq is the product of cost parameter c and q_double.
    # v is the difference between each pair of prices in p2 and cq.
    # u is the difference between consecutive elements in v.
    cq = c * q_double
    v = p2 - cq
    u = v[1:] - v[:-1]

    # Compute s for each time step:
    # s is the squared elements of u divided by twice the variance varu.
    s = (u ** 2) / (2 * varu)

    # Extend s to have the same length as p:
    # Append zeros to the bottom of s to match the length of p2.
    s_extended = np.vstack([s, np.zeros((len(p2) - len(s), 2))])

    # Calculate s_sum_all:
    # This involves a complex reshaping and addition of s_extended to itself.
    s_sum_all = np.vstack((s_extended[:, 0], np.zeros(len(p2)))).T + np.vstack((np.zeros(len(p2)), s_extended[:, 1])).T

    # Iterate over each skip interval (0 and 1 in this case).
    for i_start in range(n_skip):
        if print_level > 0:
            # Print the current skip interval for debugging.
            print(f"qDraw. iStart: {i_start}")

        # k is a boolean array where True corresponds to elements in mod_p equal to i_start.
        # jnz contains indices where both k is True and q is non-zero.
        k = mod_p == i_start
        jnz = np.where(k & q_nonzero)[0]

        if len(jnz) > 0:
            # Select relevant rows from s_sum_all:
            # For each index in jnz, select the corresponding row in s_sum_all.
            s_sum = s_sum_all[jnz, :]

            # Calculate log odds:
            # log_odds is the difference between the second and first column of s_sum.
            log_odds = s_sum[:, 1] - s_sum[:, 0]

            # Adjust log odds to avoid overflow in the exp function.
            log_okay = log_odds < 500
            odds = np.exp(log_odds * log_okay)

            # Calculate the probability of buying (p_buy):
            # It is the odds divided by the sum of odds and 1, adjusted by log_okay.
            p_buy = odds / (1 + odds)
            p_buy = p_buy * log_okay

            # Generate random uniform values and calculate qknz:
            # qknz is an updated value of q based on whether the random value is greater than p_buy.
            ru = np.random.uniform(size=len(p_buy))
            qknz = 1 - 2 * (ru > p_buy)

            # Update the elements of q at indices jnz with qknz.
            q[jnz] = qknz

    # Return the updated q array.
    return q


def q_draw_vec(p, q, c, varu, print_level):
    # Validate the lengths of the input arrays
    if len(p) != len(q):
        raise ValueError("p and q are of different lengths.")

    # Check that c and varu are either scalars or arrays of appropriate lengths
    if not (np.isscalar(c) or len(c) == len(p)) or not (np.isscalar(varu) or len(varu) == len(p) - 1):
        raise ValueError("Invalid dimensions for c or varu.")

    # Create a boolean array indicating where q is not zero
    q_nonzero = q != 0

    # Duplicate the price array p and the trade direction array q
    p2 = np.tile(p, (2, 1)).T
    q_double = np.tile(q, (2, 1)).T

    # Define a constant for the number of elements to skip in the loop
    n_skip = 2

    # Create an array for modulo calculations to determine the update pattern
    mod_p = np.mod(np.arange(len(p)), n_skip)

    for i_start in range(n_skip):
        # Print the current iteration for debugging if print_level is greater than 0
        if print_level > 0:
            print(f"qDrawVec. iStart: {i_start}")

        # Calculate indices for updating q based on the current iteration and nonzero elements in q
        k = mod_p == i_start
        jnz = np.where(k & q_nonzero)[0]

        if len(jnz) > 0:
            # Update the elements of q_double to be alternately 1 and -1 for the indices in jnz
            q_double[jnz, 0] = 1
            q_double[jnz, 1] = -1

            # Calculate cq based on whether c is a scalar or a vector
            if np.isscalar(c):
                cq = c * q_double
            else:
                c2 = np.vstack((c, c)).T
                cq = c2 * q_double

            # Compute the difference between doubled prices and cq
            v = p2 - cq
            u = v[1:] - v[:-1]

            # Calculate s based on whether varu is a scalar or a vector
            if np.isscalar(varu):
                s = (u ** 2) / (2 * varu)
            else:
                varu2 = 2 * np.vstack((varu, varu)).T
                s = (u ** 2) / varu2

            # Extend s to have the same length as p
            s_extended = np.vstack([s, np.zeros((len(p2) - len(s), 2))])

            # Calculate s_sum_all by combining s_extended with itself
            s_sum_all = np.vstack((s_extended[:, 0], np.zeros(len(p2)))).T + np.vstack(
                (np.zeros(len(p2)), s_extended[:, 1])).T

            # Select the relevant rows from s_sum_all
            s_sum = s_sum_all[jnz, :]
            log_odds = s_sum[:, 1] - s_sum[:, 0]

            # Adjust log odds to avoid overflow and calculate the odds
            log_okay = log_odds < 500
            odds = np.exp(log_odds * log_okay)

            # Calculate the probability of buying and adjust it based on log_okay
            p_buy = odds / (1 + odds)
            p_buy = p_buy * log_okay

            # Generate random uniform values and calculate qknz
            ru = np.random.uniform(size=len(p_buy))
            qknz = 1 - 2 * (ru > p_buy)

            # Update q at the indices specified in jnz
            q[jnz] = qknz

    # Return the updated q array
    return q


def bayes_regression_update(prior_mu, prior_cov, y, X, d_var):
    if prior_mu.shape[1] != 1:
        raise ValueError("priorMu should be a column vector")
    if X.shape[0] < X.shape[1]:
        raise ValueError("X has fewer rows than columns")
    if X.shape[0] != y.shape[0] or y.shape[1] != 1:
        raise ValueError("Dimensions of X and y are not compatible")
    if prior_mu.shape[0] != X.shape[1]:
        raise ValueError("priorMu and X are not conformable")
    if prior_cov.shape[0] != prior_cov.shape[1] or prior_cov.shape[0] != prior_mu.shape[0]:
        raise ValueError("Dimensions of priorCov are not compatible with priorMu")

    cov_inv = np.linalg.inv(prior_cov)
    Di = (1 / d_var) * np.dot(X.T, X) + cov_inv
    D = np.linalg.inv(Di)
    dd = (1 / d_var) * np.dot(X.T, y) + np.dot(cov_inv, prior_mu)
    post_mu = np.dot(D, dd)
    post_cov = D

    return post_mu, post_cov


def bayes_variance_update(prior_alpha, prior_beta, u):
    """
    Updates the posterior alpha and beta parameters for an inverted gamma distribution.

    Parameters:
    prior_alpha (float): The prior alpha parameter of the inverted gamma distribution.
    prior_beta (float): The prior beta parameter of the inverted gamma distribution.
    u (numpy.ndarray): Vector of estimated disturbances.

    Returns:
    post_alpha (float): Updated posterior alpha parameter.
    post_beta (float): Updated posterior beta parameter.
    """

    # Update the posterior alpha parameter
    post_alpha = prior_alpha + len(u) / 2

    # Update the posterior beta parameter
    post_beta = prior_beta + np.sum(u ** 2) / 2

    return post_alpha, post_beta


def rand_std_norm_t(zlow, zhigh):
    PROBNLIMIT = 6
    eps = 1e-30  # A small epsilon value

    if zlow == float('-inf') and zhigh == float('inf'):
        return np.random.normal()
    if zlow > PROBNLIMIT and (zhigh == float('inf') or zhigh > PROBNLIMIT):
        return zlow + 100 * eps
    if zhigh < -PROBNLIMIT and (zlow == float('-inf') or zlow < -PROBNLIMIT):
        return zhigh - 100 * eps

    a, b = zlow, zhigh
    if zlow == float('-inf'):
        a = -np.inf
    if zhigh == float('inf'):
        b = np.inf

    return truncnorm.rvs(a, b, loc=0, scale=1)


def mvnrnd_t(mu, cov, v_lower, v_upper):
    f = sqrtm(cov)
    n = np.prod(mu.shape)
    eta = np.zeros(n)

    for k in range(n):
        etasum = np.dot(f[k, :k], eta[:k])
        low = (v_lower[k] - mu[k] - etasum) / f[k, k]
        high = (v_upper[k] - mu[k] - etasum) / f[k, k]
        eta[k] = rand_std_norm_t(low, high)

    return mu + np.dot(f, eta)


def roll_gibbs_beta(p, pm, q, n_sweeps, reg_draw, varu_draw, q_draw_bool, varu_start, c_start, beta_start, print_level):
    """
    Perform Gibbs sampling to estimate parameters in the Roll model.

    Parameters:
    p (numpy.ndarray): Vector of trade prices.
    pm (numpy.ndarray): Vector of mid prices.
    q (numpy.ndarray): Vector of trade directions.
    n_sweeps (int): Number of Gibbs sampling iterations.
    reg_draw (bool): Flag to perform regression draw.
    varu_draw (bool): Flag to perform variance draw.
    q_draw_bool (bool): Flag to perform q draw.
    varu_start (float): Initial value of variance.
    c_start (float): Initial value of cost parameter c.
    beta_start (float): Initial value of beta.
    print_level (int): Verbosity level for printing diagnostics.

    Returns:
    numpy.ndarray: Output matrix with parameters from each sweep. Columns are c, beta, and varu.
    """
    n_obs = len(p)

    # Check for length mismatch
    if len(q) != n_obs or len(pm) != n_obs:
        print('RollGibbsBeta length mismatch')
        return None

    # Calculate price change
    dp = p[1:] - p[:-1]

    # Initialize q based on price sign changes if required
    if q_draw_bool:
        q_initial = np.sign(dp)
        q_initial = np.append(q_initial, 1)  # Extend to match length of q
        q = np.where(q != 0, q_initial, q)

    # Initialize variance, cost, and beta parameters
    varu = max(varu_start, 0.001)
    c = max(c_start, 0.01)
    beta = max(beta_start, 1)

    # Output matrix initialization
    parm_out = np.zeros((n_sweeps, 3))

    for sweep in range(n_sweeps):
        # Calculate changes in trade directions and mid prices
        dq = q[1:] - q[:-1]
        dpm = pm[1:] - pm[:-1]

        # Perform regression draw if enabled
        if reg_draw:
            prior_mu = np.array([[0], [1]])  # Prior mean
            prior_cov = np.diag([1, 2])  # Prior covariance
            X = np.column_stack((dq, dpm))  # Design matrix
            post_mu, post_cov = bayes_regression_update(prior_mu, prior_cov, dp.reshape(-1, 1), X, varu)
            coeff_lower = np.array([0, float('-inf')])
            coeff_upper = np.array([float('inf'), float('inf')])
            coeff_draw = mvnrnd_t(post_mu.flatten(), post_cov, coeff_lower, coeff_upper)
            c, beta = coeff_draw[0], coeff_draw[1]  # Extract c and beta

        # Perform variance draw if enabled
        if varu_draw:
            u = dp - c * dq[:len(dp)] - beta * dpm[:len(dp)]  # Calculate disturbances
            prior_alpha = 1e-12
            prior_beta = 1e-12
            post_alpha, post_beta = bayes_variance_update(prior_alpha, prior_beta, u)
            varu = 1 / np.random.gamma(post_alpha, 1 / post_beta)

        # Update q if required
        if q_draw_bool:
            p2 = p - beta * pm
            q = q_draw(p2, q, c, varu, 0)

        # Store parameters in output array
        parm_out[sweep, :] = [c, beta, varu]

    return parm_out

#
# "Testing bayes_regression_update and roll_gibbs_beta"
# # Example test data
# np.random.seed(0)  # for reproducibility
# n_samples = 100
# n_features = 2
#
# X_test = np.random.randn(n_samples, n_features)  # Design matrix
# y_test = np.random.randn(n_samples, 1) * 0.5  # Dependent variable with some noise
#
# prior_mu_test = np.zeros((n_features, 1))  # Prior mean (zero)
# prior_cov_test = np.eye(n_features)  # Prior covariance (identity matrix)
# d_var_test = 0.5  # Variance of error
#
# # Run bayes_regression_update
# post_mu, post_cov = bayes_regression_update(prior_mu_test, prior_cov_test, y_test, X_test, d_var_test)
#
# # Print or inspect the results
# print("Posterior Mean (post_mu):", post_mu)
# print("Posterior Covariance (post_cov):", post_cov)
#
# # Example test data for roll_gibbs_beta
# p_test = np.random.normal(size=100)
# pm_test = np.random.normal(size=100)
# q_test = np.random.choice([-1, 1], size=100)
#
# # Parameters for the Gibbs sampler
# n_sweeps_test = 1000
# reg_draw_test = True
# varu_draw_test = True
# q_draw_test = True
# varu_start_test = 0.001
# c_start_test = 0.01
# beta_start_test = 1
# print_level_test = 1
#
# # Run roll_gibbs_beta
# results = roll_gibbs_beta(p_test, pm_test, q_test, n_sweeps_test, reg_draw_test, varu_draw_test, q_draw_test, varu_start_test, c_start_test, beta_start_test, print_level_test)
#
# # Inspect results
# print("Results from RollGibbsBeta:", results)
#
