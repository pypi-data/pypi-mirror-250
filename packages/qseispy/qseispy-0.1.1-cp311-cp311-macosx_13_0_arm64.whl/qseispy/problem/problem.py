import numpy as np


class SFInv:
    def __init__(self, strike, dip, rake):
        self.mw = None
        self.latitude = None
        self.longitude = None
        self.depth = None
        self.strike = strike
        self.dip = dip
        self.rake = rake


class DCInv:
    def __init__(self, strike, dip, rake):
        self.mw = None
        self.latitude = None
        self.longitude = None
        self.depth = None
        self.strike = strike
        self.dip = dip
        self.rake = rake


class MTInv:
    def __init__(self, mrr, mtt, mpp, mrt, mrp, mtp):
        self.mw = None
        self.latitude = None
        self.longitude = None
        self.depth = None
        self.mrr = mrr
        self.mtt = mtt
        self.mpp = mpp
        self.mrt = mrt
        self.mrp = mrp
        self.mtp = mtp


def misfit():
    pass
