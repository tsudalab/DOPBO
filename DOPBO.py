import numpy as np
import random
import physbo


######################
# parameters

filename = "data.csv" # target dataset, final row indicates the present objective function and amounts of liquid samples

drainage_index = 4 # drainage_index * 10 % is the maximum amount of drainage

delta = 0.1 # minimum unit of injection amounts

add_max = 10 # Delta = delta * add_max is the maximum total injection amounts

random_seed = 1

######################

def read_initial_data(filename):

    arr = np.genfromtxt(filename, skip_header=1, delimiter=',')

    return arr


def bayesianopt(arr, seed_index, emi_num):

    num_search_each_probe = 1
    score = 'TS'
    num_random_selection = 1


    t_train, X_all, train_actions, test_actions, recipe = load_data(arr, emi_num)

    X_all_concent=[]

    for i in range(len(X_all)):
        X_all_concent.append(X_all[i]/sum(X_all[i]))

    X_all_concent = np.array(X_all_concent)



    if len(t_train) > num_random_selection:

        calculated_ids=train_actions

        t_initial=np.array(t_train)

        X = physbo.misc.centering( X_all_concent )

        policy = physbo.search.discrete.policy(test_X=X,initial_data=[calculated_ids, t_initial])

        policy.set_seed(seed_index)

        actions = policy.bayes_search(max_num_probes=1, num_search_each_probe=num_search_each_probe,
                  simulator=None, score=score, interval=0,  num_rand_basis = 5000)

    else:
        actions = [random.choice(test_actions)]


    recommendation = X_all[actions[0]]

    add_recommendation = [recipe[actions[0]][i+1]*delta for i in range(3)]

    reduce_volume = sum(X_all[len(train_actions)-1])*0.1*recipe[actions[0]][0]

    print("present concentration:", X_all[len(train_actions)-1], )
    print("drainage:", np.round(reduce_volume, decimals=4))
    print("injection:", np.round(add_recommendation, decimals=4))
    print("next concentration:", recommendation)

    return recommendation, sum(add_recommendation), reduce_volume, sum(recommendation)





def load_data(arr, emi_num):

    if arr.ndim == 1:
        X_train = [arr[1:]]
        t_train = [arr[0]]

    else:
        X_train = arr[:, 1:]
        t_train = arr[:, 0]

    X_all=[]
    recipe=[]

    #training
    for i in range(len(X_train)):
        X_all.append(X_train[i])
        recipe.append([0, 0, 0, 0])

    for emit in range(emi_num+1):

        for k in range(1,add_max+1):
            X_all.append([X_train[len(X_train)-1][0]*(1-emit*0.1)+k*delta,X_train[len(X_train)-1][1]*(1-emit*0.1),X_train[len(X_train)-1][2]*(1-emit*0.1)])
            recipe.append([emit, k, 0, 0])

            for i in range(k):
                a = k-i-1
                for j in range(k-a+1):
                    b = j
                    c = k-a-b

                    X_all.append([X_train[-1][0]*(1-emit*0.1)+a*delta, X_train[-1][1]*(1-emit*0.1)+b*delta, X_train[-1][2]*(1-emit*0.1)+c*delta])
                    recipe.append([emit, a, b, c])

    X_all = np.round(X_all, decimals=5)
    all_actions = [i for i in range(len(X_all))]
    train_actions = [i for i in range(len(X_train))]
    test_actions = list(set(all_actions) - set(train_actions))

    test_actions.sort()

    return t_train, X_all, train_actions, test_actions, recipe


if __name__ == '__main__':

    data = read_initial_data(filename)

    recommendation, cost, reduce, amount = bayesianopt(data, random_seed, drainage_index)
