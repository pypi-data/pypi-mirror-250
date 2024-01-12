
import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure

import numpy as np

from ..base import plotting as cP

from ..classes.core import StatArray
from .Inference1D import Inference1D

class Inference1D_debug(Inference1D):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.prior_v = StatArray.StatArray(2 * self.n_markov_chains, name='prior')
        self.proposal_v = StatArray.StatArray(2 * self.n_markov_chains, name='proposal')
        self.likelihood_v = StatArray.StatArray(2 * self.n_markov_chains, name='likelihood')
        self.posterior_v = StatArray.StatArray(2 * self.n_markov_chains, name='posterior')

        self.test_prior_v = StatArray.StatArray(2 * self.n_markov_chains, name='test prior')
        self.test_proposal_v = StatArray.StatArray(2 * self.n_markov_chains, name='test proposal')
        self.test_likelihood_v = StatArray.StatArray(2 * self.n_markov_chains, name='test likelihood')
        self.test_posterior_v = StatArray.StatArray(2 * self.n_markov_chains, name='test posterior')


    def update(self):
        super().update()

        self.prior_v[self.iteration] = self.prior
        self.test_prior_v[self.iteration] = self.test_prior

        self.proposal_v[self.iteration] = self.proposal
        self.test_proposal_v[self.iteration] = self.test_proposal

        self.likelihood_v[self.iteration] = self.likelihood
        self.test_likelihood_v[self.iteration] = self.test_likelihood

        self.posterior_v[self.iteration] = self.posterior
        self.test_posterior_v[self.iteration] = self.test_posterior

    def _init_posterior_plots(self, gs=None, **kwargs):
        super()._init_posterior_plots(gs, **kwargs)

        self.fig_debug = kwargs.pop('fig', plt.figure(facecolor='white', figsize=(16, 9)))

        self.ax_debug = self.fig_debug.subplots(4, 1)
        for a in self.ax_debug:
            cP.pretty(a)

    def plot_posteriors(self, axes=None, title="", increment=None, **kwargs):
        super().plot_posteriors(axes, title, increment, **kwargs)

        plot = True
        if increment is not None:
            if (np.mod(self.iteration, increment) != 0):
                plot = False

        if plot:
            plt.sca(self.ax_debug[0]); plt.cla()
            (self.test_prior_v - self.prior_v).plot(x = self.iRange, i=np.s_[:self.iteration], log=10)
            plt.sca(self.ax_debug[1]); plt.cla()
            (self.proposal_v - self.test_proposal_v).plot(x = self.iRange, i=np.s_[:self.iteration], log=10)
            plt.sca(self.ax_debug[2]); plt.cla()
            (self.test_likelihood_v - self.likelihood_v).plot(x = self.iRange, i=np.s_[:self.iteration], log=10)
            plt.sca(self.ax_debug[3]); plt.cla()
            self.test_posterior_v.plot(x = self.iRange, i=np.s_[:self.iteration], log=10)


            if self.fig_debug is not None:
                self.fig_debug.canvas.draw()
                self.fig_debug.canvas.flush_events()

            cP.pause(1e-9)