import unittest
from tests.utils.fiqus_test_classes import FiQuSSolverTests
from fiqus.data.DataFiQuS import FDM


class TestSolvers(FiQuSSolverTests):
    def test_Pancake3D(self):
        """
        Checks if Pancake3D solvers work correctly by comparing the results to the
        reference results that were checked manually.
        """
        with self.subTest(msg="tsa linear weakly coupled"):
            model_name = "TEST_Pancake3D_TSA"
            data_model: FDM = self.get_data_model(model_name)

            data_model.magnet.solve.type = "weaklyCoupled"

            self.solve(data_model, model_name)

            # Compare the pro files:
            pro_file = self.get_path_to_generated_file(
                file_name=model_name, file_extension="pro"
            )
            reference_pro_file = self.get_path_to_reference_file(
                file_name=model_name, file_extension="pro"
            )
            self.compare_text_files(pro_file, reference_pro_file)

            # Compare the results files:
            pos_file = self.get_path_to_generated_file(file_name="Temperature-DefaultFormat", file_extension="pos")
            reference_pos_file = self.get_path_to_reference_file(file_name="Temperature-DefaultFormat", file_extension="pos")
            self.compare_pos_files(pos_file, reference_pos_file)

        with self.subTest(msg="tsa linear strongly coupled"):
            model_name = "TEST_Pancake3D_TSA"
            data_model = self.get_data_model(model_name)

            data_model.magnet.solve.type = "stronglyCoupled"
            data_model.magnet.solve.ti.cooling = "fixedTemperature"

            self.solve(data_model, model_name)

        with self.subTest(msg="tsa linear electromagnetic"):
            model_name = "TEST_Pancake3D_TSA"
            data_model = self.get_data_model(model_name)

            data_model.magnet.solve.type = "electromagnetic"
            del data_model.magnet.solve.t.adaptive.postOperationTolerances[1]

            self.solve(data_model, model_name)


if __name__ == "__main__":
    unittest.main()
