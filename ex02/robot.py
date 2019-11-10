import math

from ex02.motion import Translation, Rotation
from ex02.telecom import Telecom, Exchanger
from typing import List


class RobotComponent:
    """
    Class for robot's component needing direct access to robot instance.
    """

    def __init__(self):
        self.robot = None

    def register(self, robot: 'Robot'):
        """
        Registers component to robot
        :param robot:
        :return:
        """
        self.robot = robot

class Transmitter(RobotComponent, Exchanger):
    """
    Transmitter Class
    """

    def exchange(self, tc: Telecom) -> Telecom:
        pass

class Wheel:

    def run(self, length):
        pass


class EnergySupplier(RobotComponent):
    """Energy supplier is an energy tank"""

    def __init__(self, quantity: float = 1000.0):
        self.quantity = quantity

    def consume(self, quantity: float) -> float:
        self.quantity = self.quantity - quantity

    def has_enough(self, quantity: float) -> float:
        return quantity < self.quantity


class MotionController(RobotComponent):

    def run_translation(self, translation: 'Translation', energy_supplier: 'EnergySupplier'):
        """
        Runs translation
        :param translation:
        :param energy_supplier: EnergySupplier to supply energy for translation
        :return:
        """
        pass

    def run_rotation(self, rotation: 'Rotation', energy_supplier: 'EnergySupplier'):
        """
        Runs rotation
        :param rotation:
        :param energy_supplier:
        :return:
        """
        pass

    def move(self, motion, energy_supplier):
        pass

    def get_required_energy_for(self, length: float):
        pass


class Navigator(RobotComponent):

    def __init__(self, arranger: 'Arranger'):
        self.arranger = arranger

    def compute_motions(self, positions):
        pass

    def compute_total_distance(self, motions):
        return super(len(m) for m in motions)

    def arrange_translations(self, translations):
        return self.arranger.arrange(translations)

    def to_points(self, positions):
        return list([Point.new(xy) for xy in positions])

    def to_translations(self, points):
        pass


class Arranger:

    def arrange(self, motions: List) -> List:
        pass

class Robot(Exchanger):
    STATUS_MOTIONLESS = 'motionless'
    STATUS_MOVING = 'moving'

    def __init__(self, transmitter: Transmitter,
                 motion_controller: MotionController,
                 navigator: Navigator,
                 energy_supplier: EnergySupplier):
        self.transmitter = transmitter
        self.motion_controller = motion_controller
        self.navigator = navigator
        self.energy_supplier = energy_supplier
        self.status = None
        self.motions = []

    def exchange(self, tc: Telecom) -> Telecom:
        return self.transmitter.exchange(tc)

    def load_positions(self, positions: List):
        motions = self.navigator.compute_motions(positions)
        total_length = self.navigator.compute_total_distance(motions)
        total_energy = self.motion_controller.get_required_energy_for(total_length)
        if not self.energy_supplier.has_enough(total_energy):
            raise ValueError("Not enough energy")
        self.motions = motions

    def run(self):
        if len(self.motions) > 0:
            self.status = Robot.STATUS_MOVING
            for motion in self.motions:
                self.motion_controller.move(motion)
            self.status = Robot.STATUS_MOTIONLESS
        else:
            raise ValueError("Empty motion list")

    def is_moving(self) -> bool :
        return self.status == Robot.STATUS_MOVING
