import numpy as np
class State:
    def __init__(self, label, basis, ketcoefficients=np.nan, bracoefficients=np.nan, ort_labels=[]):
        self.label = label

        if ketcoefficients is not np.nan:
            ketcoefficients = np.asarray(ketcoefficients)
            self.ketcoef = ketcoefficients
            self.bracoef = np.conjugate(ketcoefficients)
        elif bracoefficients is not np.nan:
            bracoefficients = np.asarray(bracoefficients)
            self.bracoef = bracoefficients
            self.ketcoef = np.conjugate(bracoefficients)
        else:
            self.ketcoef = np.nan
            self.bracoef = np.nan
        self.basis = basis
        self.basislabels = basis.statelabels

        self.ket = Ket(label, self.basis, self.ketcoef)
        self.bra = Bra(label, self.basis, self.bracoef)
        self.ortlabels=np.asarray(ort_labels)
        
    def __repr__(self):
        return f"State:{self.label}"
    
    def add_ortlabels(self, labels):
        self.ortlabels=np.concatenate((self.ortlabels,np.asarray(labels)))



class Ket:
    def __init__(self, label, basis=None, coefficients=np.nan, ort_labels=[]):
        self.label = label
        self.coef = np.asarray(coefficients)
        self.basis = basis
        self.ortlabels=np.asarray(ort_labels)

    def __repr__(self):
        return f"|{self.label}>"

    def add_ortlabels(self, labels):
        self.ortlabels=np.concatenate((self.ortlabels,np.asarray(labels)))

    def dagger(self):
        bra = Bra(self.label, self.basis, np.conjugate(self.coef), ort_labels=self.ortlabels)
        return bra


class Bra:
    def __init__(self, label, basis=None, coefficients=np.nan, ort_labels=[]):
        self.label = label
        self.coef = np.asarray(coefficients)
        self.basis = basis
        self.ortlabels=np.asarray(ort_labels)
        
    def __repr__(self):
        return f"<{self.label}|"

    def add_ortlabels(self, labels):
        self.ortlabels=np.concatenate((self.ortlabels,np.asarray(labels)))

    def dagger(self):
        ket = Ket(self.label, self.basis, np.conjugate(self.coef), ort_labels=self.ortlabels)
        return ket


class Basis:
    def __init__(self, state_labels):
        self.statelabels = state_labels

        kets = [Ket(label) for label in state_labels]
        kets = np.asarray(kets)
        
        for ket in kets:
            ket.add_ortlabels(list(set(state_labels) - {ket.label}))

        self.kets = kets

    def __repr__(self):
        return f"Base({', '.join([str(ket) for ket in self.kets])})"
