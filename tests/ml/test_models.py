import unittest
import torch
from ml.models.baseline import BaselineFloodModel
from ml.models.ann import FloodSusceptibilityANN


class TestMLModels(unittest.TestCase):
    def test_baseline_model_instantiation(self):
        baseline = BaselineFloodModel()
        model = baseline.build_model()
        self.assertIsNotNone(model)
        self.assertEqual(model.max_iter, 1000)

    def test_ann_model_forward_pass_synthetic(self):
        """
        Test ANN initialization and forward pass using synthetic tensor fixture
        to verify network architecture without training or fake flood data.
        """
        batch_size = 4
        input_dim = 10
        synthetic_features = torch.randn(batch_size, input_dim)

        ann = FloodSusceptibilityANN(input_dim=input_dim, hidden_dims=[16, 8])
        ann.eval()

        with torch.no_grad():
            output = ann(synthetic_features)

        self.assertEqual(output.shape, (batch_size, 1))
        # Sigmoid bounds check
        self.assertTrue((output >= 0.0).all())
        self.assertTrue((output <= 1.0).all())


if __name__ == "__main__":
    unittest.main()
