import pickle


def save_var(to_save, path):
    with open(path, 'wb') as file:
        pickle.dump(to_save, file)


def load_var(path):
    with open(path, 'rb') as file:
        var = pickle.load(file)
        return var
