import math
from unittest.mock import call

import pytest

from ex02.robot import Robot, MotionController, Wheel, EnergySupplier
from ex02.motion import Translation, Rotation
from ex02.geometry import Point


def get_values_from_call_list(call_list):
    return list(a[0][0] for a in call_list)

class TestMotionController:

    @pytest.fixture()
    def init_controller(self, mocker):
        robot = mocker.Mock(spec=Robot)
        right_wheel = mocker.Mock(spec=Wheel)
        left_wheel = mocker.Mock(spec=Wheel)
        energy_supplier = mocker.Mock(spec=EnergySupplier)
        configuration = {}
        ctrl = MotionController(right_wheel=right_wheel,
                                left_wheel=left_wheel,
                                configuration=configuration)

        return ctrl, robot, right_wheel, left_wheel, configuration, energy_supplier


    def test_translation(self, init_controller):
        # --given--
        ctrl, robot, right_wheel, left_wheel, _, energy_supplier = init_controller
        tr = Translation(Point(0, 0), Point(10, 0))

        # --when--
        ctrl.run_translation(tr, energy_supplier)

        # --then--
        assert right_wheel.run.call_count == 1000
        assert left_wheel.run.call_count == 1000
        right_wheel.run.assert_called_with(0.01)
        left_wheel.run.assert_called_with(0.01)



    def test_rotation_on_the_spot(self, init_controller):
        # --given--
        ctrl, robot, right_wheel, left_wheel, _, energy_supplier  = init_controller
        center = Point(1,0)
        rot = Rotation(start=center,
                       end=center,
                       start_vector=Point(0, 1),
                       end_vector=Point(-1, 0))
        assert rot.arc.angle == math.pi/2

        # --when--
        ctrl.run_rotation(rot, energy_supplier)

        # --then--
        right_args = get_values_from_call_list(right_wheel.run.call_args_list)
        left_args = get_values_from_call_list(left_wheel.run.call_args_list)
        supplier_args = get_values_from_call_list(energy_supplier.consume.call_args_list)

        # same nb of calls
        assert len(right_args) == len(left_args)
        # energy supplier call for both wheel
        assert len(supplier_args) == len(right_args)
        assert len(right_args) == 78
        # same nb of diff. value
        assert len(set(right_args)) == len(set(left_args)) == len(set(supplier_args)) == 1

        # inversed value
        assert right_args[0] == -left_args[0]
        assert right_args[0] == (math.pi/4)/78

    def test_rotation_with_center(self, init_controller):
        # --given--
        ctrl, robot, right_wheel, left_wheel, _, energy_supplier = init_controller
        center = Point(0,0)
        rot = Rotation(start=Point(10,0),
                       end=Point(0,10),
                       start_vector=Point(0, 1),
                       end_vector=Point(-1, 0))

        assert math.isclose(rot.arc.angle, math.pi/2)
        assert rot.arc.center ==  center

        # --when--
        ctrl.run_rotation(rot, energy_supplier)

        # --then--
        right_args = get_values_from_call_list(right_wheel.run.call_args_list)
        left_args = get_values_from_call_list(left_wheel.run.call_args_list)
        supplier_args = get_values_from_call_list(energy_supplier.consume.call_args_list)
        # same nb of calls
        assert len(right_args) == len(left_args)
        # energy supplier call two time more
        assert len(supplier_args) == len(right_args)
        assert len(right_args) == 1649
        # same nb of diff. value
        assert len(set(right_args)) == len(set(left_args)) == 1
        assert len(set(supplier_args)) == 1

        half_axis_len = MotionController.DEFAULT_WHEEL_AXIS_LENGTH/2
        ratio = (rot.arc.radius + half_axis_len)/(rot.arc.radius - half_axis_len)
        ratio_from_step = right_args[0]/left_args[0]
        assert ratio == pytest.approx(ratio_from_step)
        assert right_args[0] == pytest.approx((math.pi/2)/1649*(rot.arc.radius + 1/2))
