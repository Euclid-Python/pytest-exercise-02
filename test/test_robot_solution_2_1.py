import pytest
import pytest_mock

from ex02.motion import Translation, Rotation
from ex02.robot import Robot, Transmitter, MotionController, Navigator, EnergySupplier
from ex02.telecom import Telecom, Command


class TestRobotSolution_2_1:

    def test_mocking_a_robot(self, mocker):
        robot = mocker.Mock(spec=Robot)

    @pytest.fixture()
    def init_robot(self, mocker):
        transmitter = mocker.Mock(spec=Transmitter)
        motion_controller = mocker.Mock(spec=MotionController)
        navigator = mocker.Mock(spec=Navigator)
        energy_supplier = mocker.Mock(spec=EnergySupplier)

        robot = Robot(transmitter=transmitter,
                      motion_controller=motion_controller,
                      navigator=navigator,
                      energy_supplier=energy_supplier)

        return robot, transmitter, motion_controller, navigator, energy_supplier



    def test_is_moving_default_not(self, init_robot):
        # -- given --
        robot, *_ = init_robot
        # -- then --
        assert not robot.is_moving()

    def test_is_moving(self, init_robot):
        # -- given --
        robot, *_ = init_robot
        # -- when --
        robot.status = Robot.STATUS_MOVING
        # -- then --
        assert robot.is_moving()


    def test_exchange_through_transmitter(self, init_robot):
        # -- given --
        robot, transmitter, *_ = init_robot
        # -- when --
        robot.exchange(Telecom(command=Command.MOVING))
        # -- then --
        transmitter.exchange.assert_called_once()

    def test_load_positions_when_energy_supplier_has_enough_energy(self, init_robot):
        # -- given --
        robot, _, _, navigator, energy_supplier = init_robot
        motions = []
        navigator.compute_motions.return_value = motions
        # -- when--
        energy_supplier.has_enough.return_value = True
        robot.load_positions([])
        # -- then --
        assert robot.motions is motions


    def test_load_positions_when_energy_supplier_has_NOT_enough_energy(self, init_robot):
        # -- given --
        robot, _, _, navigator, energy_supplier = init_robot
        motions = []
        navigator.compute_motions.return_value = motions
        # -- when--
        energy_supplier.has_enough.return_value = False
        with pytest.raises(ValueError):
            robot.load_positions(motions)
        # -- then --
        assert len(robot.motions) == 0

    def test_load_positions_calls(self, init_robot):
        # -- given --
        robot, transmitter, motion_controller, navigator, energy_supplier = init_robot
        # -- when--
        energy_supplier.has_enough.return_value = True
        robot.load_positions([])
        # -- then --
        navigator.compute_motions.assert_called_once
        navigator.compute_total_distance.assert_called_once
        motion_controller.get_required_energy_for.assert_called_once
        energy_supplier.has_enough.assert_called_once


    def test_run_without_motions(self, init_robot):
        # --given--
        robot, *_ = init_robot

        # -- when--
        robot.motions = []
        with pytest.raises(ValueError):
            robot.run()


    def test_run_with_motions(self, mocker, init_robot):
        # -- given --
        robot, transmitter, motion_controller, navigator, energy_supplier = init_robot
        # -- when--
        translation = mocker.Mock(spec=Translation)
        rotation = mocker.Mock(spec=Rotation)
        robot.motions = [translation, rotation, translation]
        robot.run()
        # -- then --
        # - get the arguments
        assert motion_controller.move.call_count == 3
