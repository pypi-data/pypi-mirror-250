from unittest import TestCase

from deepmol.pipeline import Pipeline
from deepmol.datasets import SmilesDataset


class TestPipeline(TestCase):
    def test_coiso(self):
        from deepmol.pipeline import Pipeline
        from deepmol.datasets import SmilesDataset

        def get_predictions(molecules, pipeline):
            """
            Get predictions from a dataset and a pipeline
            """
            dataset = SmilesDataset(smiles=molecules, mode="regression")
            pipeline = Pipeline.load(pipeline)
            predictions = pipeline.predict_proba(dataset)
            return predictions

        print(get_predictions(["CC(=O)OC1=CC=CC=C1C(=O)O", "CC(=O)NC1=CC=C(C=C1)O"], "logS_pipeline_to_deploy"))