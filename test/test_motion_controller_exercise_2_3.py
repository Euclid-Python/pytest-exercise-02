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

    def test_default_values_are_well_known(self, init_controller):
        """Assertions about implicit values"""
        ctrl, *_ = init_controller

        assert MotionController.DEFAULT_WHEEL_AXIS_LENGTH == 1
        assert MotionController.CONSUMPTION_PER_LENGTH_UNIT == 1
        assert MotionController.DEFAULT_SPEED == 0.1
        assert MotionController.CONSUMPTION_PER_LENGTH_UNIT == 1
        assert MotionController.DEFAULT_TIME_STEP == 0.1

        assert ctrl.speed == MotionController.DEFAULT_SPEED
        assert ctrl.consumption_per_length_unit == MotionController.CONSUMPTION_PER_LENGTH_UNIT
        assert ctrl.time_step == MotionController.DEFAULT_TIME_STEP

    def test_translation(self, init_controller):
        # --given--
        ctrl, robot, right_wheel, left_wheel, _, energy_supplier = init_controller
        tr = Translation(Point(0, 0), Point(10, 0))
        assert tr.length == 10

        expected_nb_call = 1000
        len_step_per_call = 0.01

        assert expected_nb_call * len_step_per_call == tr.length

        # --when--
        ctrl.run_translation(tr, energy_supplier)

        # --then--
        assert right_wheel.run.call_count == expected_nb_call
        assert left_wheel.run.call_count == expected_nb_call

        right_wheel.run.assert_called_with(len_step_per_call)
        left_wheel.run.assert_called_with(len_step_per_call)

    def test_rotation_on_the_spot(self, init_controller):
        # --given--
        ctrl, robot, right_wheel, left_wheel, _, energy_supplier = init_controller
        center = Point(1, 0)
        rot = Rotation(start=center,
                       end=center,
                       start_vector=Point(0, 1),
                       end_vector=Point(-1, 0))
        angle = math.pi / 2
        radius = 0
        expected_nb_of_wheel_run_call = 78
        
        self._do_assertions_about_params(rot, center, angle, radius)


        # --when--
        ctrl.run_rotation(rot, energy_supplier)

        # --then--
        right_args = self.extract_values(right_wheel, 'run')
        left_args = self.extract_values(left_wheel, 'run')
        supplier_args = self.extract_values(energy_supplier, 'consume')

        self._do_assertions_nb_of_call(right_args,
                                     left_args,
                                     supplier_args,
                                     expected_nb_of_wheel_run_call)

        self._do_assertions_nb_of_distinct_values(right_args,
                                                left_args,
                                                supplier_args,
                                                1)


        # inversed value
        assert right_args[0] == -left_args[0]
        assert right_args[0] == (rot.arc.angle/2) / expected_nb_of_wheel_run_call

    @pytest.mark.parametrize("params", [
        {'rotation': Rotation(start=Point(10, 0),
                              end=Point(0, 10),
                              start_vector=Point(0, 1),
                              end_vector=Point(-1, 0)),
         'center': Point(0, 0),
         'angle': math.pi / 2,
         'radius': 10,
         'expected_nb_of_wheel_run_call': 1649
         },
        {'rotation': Rotation(start=Point(0, 5),
                              end=Point(0, 0),
                              start_vector=Point(1, -1),
                              end_vector=Point(-1, -1)),
         'center': Point(-2.5, 2.5),
         'angle': -3*math.pi / 2,
         'radius': 3.5355339059327373,
         'expected_nb_of_wheel_run_call': 1901
         }

    ])
    def test_rotation_with_center(self, params, init_controller):
        # --given--
        ctrl, robot, right_wheel, left_wheel, _, energy_supplier = init_controller

        center = params['center']
        rot = params['rotation']
        angle = params['angle']
        radius = params['radius']
        expected_nb_of_wheel_run_call = params['expected_nb_of_wheel_run_call']

        self._do_assertions_about_params(rot, center, angle, radius)

        # --when--
        ctrl.run_rotation(rot, energy_supplier)

        # --then--
        right_args = self.extract_values(right_wheel, 'run')
        left_args = self.extract_values(left_wheel, 'run')
        supplier_args = self.extract_values(energy_supplier, 'consume')

        # same nb of calls
        self._do_assertions_nb_of_call(right_args,
                                     left_args,
                                     supplier_args,
                                     expected_nb_of_wheel_run_call)

        self._do_assertions_nb_of_distinct_values(right_args,
                                                left_args,
                                                supplier_args,
                                                1)

        self._do_assertions_lenght_values_for_both_wheels(rot,
                                                        right_args,
                                                        left_args,
                                                        expected_nb_of_wheel_run_call,
                                                        angle)

    def _do_assertions_about_params(self, rot, center, angle, radius):
        assert math.isclose(rot.arc.angle, angle)
        assert rot.arc.center == center
        assert rot.arc.radius == radius

    def _do_assertions_nb_of_call(self, right_args, left_args, supplier_args,
                                expected_nb_of_wheel_run_call):
        assert len(right_args) == len(left_args)
        # energy supplier call two time more
        assert len(supplier_args) == len(right_args)
        assert len(right_args) == expected_nb_of_wheel_run_call

    def _do_assertions_nb_of_distinct_values(self, right_args, left_args, supplier_args, nb_arg):
        # same nb of diff. value
        assert len(set(right_args)) == len(set(left_args)) == nb_arg
        assert len(set(supplier_args)) == nb_arg

    def _do_assertions_lenght_values_for_both_wheels(self, rotation,
                                                   right_args,
                                                   left_args,
                                                   expected_nb_of_wheel_run_call,
                                                   angle):
        """Does assertions about length values for both wheels"""
        half_axis_len = MotionController.DEFAULT_WHEEL_AXIS_LENGTH / 2

        big_radius = (rotation.arc.radius + half_axis_len)
        short_radius = (rotation.arc.radius - half_axis_len)

        ratio = big_radius / short_radius

        right_value = right_args[0]
        left_value = left_args[0]

        max_value = max(right_value, left_value)
        min_value = min(right_value, left_value)

        ratio_from_step = max_value / min_value
        assert ratio == pytest.approx(ratio_from_step), "ratio assertion"

        expected_max_value = math.fabs(angle / expected_nb_of_wheel_run_call * (rotation.arc.radius + half_axis_len))

        assert max_value == pytest.approx(expected_max_value), "max value for rotation"


    def extract_values(self, mock, param):
        """Extracts values from mock's call_args_list"""
        args = getattr(mock, param).call_args_list
        return get_values_from_call_list(args)
