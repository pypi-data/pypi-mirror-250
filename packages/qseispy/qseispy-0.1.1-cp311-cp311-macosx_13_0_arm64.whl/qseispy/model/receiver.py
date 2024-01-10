import numpy as np


class ReceiverModel(object):
    """
    Receiver model.

    Example:
    >>> from qseispy import ReceiverModel
    >>> receiver = ReceiverModel(dt=0.01,
                                npts=1024,
                                constant_factor=[1.0, 0.0],
                                root_positions=[[0.0, 0.0], [0.0, 0.0]],
                                pole_positions=[[-4.35425, 4.44222], [-4.35425,-4.44222]])
    >>> receiver.add(distance=np.array([1, 2, 3]), depth=0, unit="km")
    >>> receiver.add(distance=np.array([1, 2, 3]), depth=10, unit="deg")
    """

    def __init__(
        self,
        dt,
        npts,
        constant_factor=[1.0, 0.0],
        root_positions=[],
        pole_positions=[],
    ):
        self.dt = dt
        self.npts = npts
        self.constant_factor = constant_factor
        self.root_positions = root_positions
        self.pole_positions = pole_positions

        self.distances = []
        self.depths = []
        self.units = []
        self.num = 0

    def __repr__(self):
        return f"ReceiverModel: dt={self.dt}, npts={self.npts}, constant_factor={self.constant_factor}, root_positions={self.root_positions}, pole_positions={self.pole_positions}"

    def add(self, distance, depth, unit="km"):
        self.distances.append(distance)
        self.depths.append(float(depth))
        self.units.append(unit)
        self.num += len(distance)
