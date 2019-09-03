import unittest
import logging
from os.path import join as pjoin

from pymc3.plots import kdeplot
import numpy as num
from numpy import array

from beat.sampler import base
from pyrocko import util
from beat.models import load_model

import matplotlib.pyplot as plt


homedir = '/home/vasyurhm/BEATS'
smc_res_dir = pjoin(homedir, 'LaquilaJointPonlyUPDATE_DC_var_PT_smc')
pt_res_dir = pjoin(homedir, 'LaquilaJointPonlyUPDATE_DC_var_PT_long')

km = 1000.

logger = logging.getLogger('test_sampler')


class SamplerTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):

        self.plot = 1

        unittest.TestCase.__init__(self, *args, **kwargs)
        self.normal = base.NormalProposal(1.)
        self.cauchy = base.CauchyProposal(1.)
        self.mvcauchy = base.MultivariateCauchyProposal(num.array([[1.]]))

    def test_proposals(self):

        nsamples = 100000
        discard = 1000

        ndist = self.normal(nsamples)

        cdist = self.cauchy(nsamples)
        cdist.sort(0)
        cdist = cdist[discard:-discard:1]

        mvcdist = self.mvcauchy(nsamples)
        mvcdist.sort(0)
        mvcdist = mvcdist[discard:-discard:1]

        if self.plot:
            ax = plt.axes()
            for d, color in zip(
                    [ndist, cdist, mvcdist], ['black', 'blue', 'red']):

                ax = kdeplot(d, ax=ax, color=color)

        ax.set_xlim([-10., 10.])
        plt.show()

    def test_smc_vs_pt(self):
        problem_smc = load_model(smc_res_dir, 'geometry', build=True)
        problem_pt = load_model(pt_res_dir, 'geometry', build=True)

        print('Loaded models')
        step_smc = problem_smc.init_sampler(False)
        print('compiled smc')
        step_pt = problem_pt.init_sampler(False)
        print('compiled pt')

        maxpoint = {
            'depth': array([1.]),
            'dip': array([42.]),
            'duration': array([8.]),
            'east_shift': array([-4.]),
            'h_any_P_0_Z': array(
                [3., 3., 3., 3., 3., 3., 3., 3., 3., 3., 3., 3., 3., 3., 3., 3.,
                 3.,
                 3., 3., 3., 3., 3., 3., 3., 3., 3., 3., 3., 3., 3., 3., 3., 3.,
                 3.,
                 3.]),
            'magnitude': array([6.2]),
            'north_shift': array([-4.]),
            'rake': array([-110.]),
            'strike': array([120.]),
            'time': array([-7.4])}

        point = problem_smc.get_random_point()
        point_smc, _ = step_smc.step(point)
        point_pt, _ = step_pt.step(point)

        print(point_pt, point_smc)


if __name__ == '__main__':
    util.setup_logging('test_sampler', 'debug')
    unittest.main()
