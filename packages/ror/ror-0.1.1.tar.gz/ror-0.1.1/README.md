<p align="center">
  <img src="https://github.com/PatrickTourniaire/ror/blob/main/docs/source/_static/logo_blue.png?raw=true" height=50 />
</p>

<h1 align="center"> ROR </h1>

<div align="center">

<a href="">![Unittesting](https://github.com/patricktourniaire/pypipeline/actions/workflows/python-unittesting.yml/badge.svg)</a>
<a href="">[![Documentation](https://github.com/PatrickTourniaire/pypipeline/actions/workflows/documentation.yml/badge.svg)](https://github.com/PatrickTourniaire/pypipeline/actions/workflows/documentation.yml)</a>
<a href="">[![PyPI Deployment](https://github.com/PatrickTourniaire/pypipeline/actions/workflows/python-release-pypi.yml/badge.svg)](https://github.com/PatrickTourniaire/pypipeline/actions/workflows/python-release-pypi.yml)</a>

</div>

ROR is a pipelining framework for Python which makes it easier to define complex ML and
data-processing stages.

## Install it from PyPI

```bash
pip install ror
```

## Usage

To get started with creating your first pipeline, you can base it on this example which
defines a simple GMM pipeline. Firstly, we import the relevant packages.

```py
  import matplotlib.pyplot as plt
  from sklearn import datasets
  from sklearn.mixture import GaussianMixture
  from sklearn.decomposition import PCA
  from sklearn.preprocessing import StandardScaler

  from dataclasses import dataclass
  from typing import Tuple

  from ror.schemas import BaseSchema
  from ror.schemas.fields import field_perishable, field_persistance
  from ror.stages import IInitStage, ITerminalStage, IForwardStage
  from ror.controlers import BaseController
```

Then we can define the schemas which will determine the structure of the data communicated between the different stages.

```py
  @dataclass
  class InitStageInput(BaseSchema):
      data: object = field_perishable()

  @dataclass
  class InitStageOutput(BaseSchema):
      X_pca: object = field_persistance()
      X_std: object = field_perishable()
      model: object = field_persistance()

  @dataclass
  class InferenceStageOutput(BaseSchema):
      X_pca: object = field_perishable()
      model: object = field_perishable()
      labels: object = field_persistance()

  @dataclass
  class VisStageOutput(BaseSchema):
      labels: object = field_persistance()
```

We can then define the logical stages which will be utilizing these schemas as input
and output between stages.

```py
  class VisStage(ITerminalStage[InferenceStageOutput, VisStageOutput]):
      def compute(self) -> None:
          # Visualize the clusters
          plt.figure(figsize=(8, 6))
          colors = ['r', 'g', 'b']

          for i in range(3):
              plt.scatter(
                  self.input.X_pca[self.input.labels == i, 0],
                  self.input.X_pca[self.input.labels == i, 1],
                  color=colors[i],
                  label=f'Cluster {i+1}'
              )

          plt.title('Gaussian Mixture Model Clustering')
          plt.xlabel('Principal Component 1')
          plt.ylabel('Principal Component 2')
          plt.legend()
          plt.show()

          self._output = self.input.get_carry()

      def get_output(self) -> VisStageOutput:
          return VisStageOutput(**self._output)

  class InferenceStage(IForwardStage[InitStageOutput, InferenceStageOutput, VisStage]):
      def compute(self) -> None:
          # Fit Guassian mixture to dataset
          self.input.model.fit(self.input.X_std)

          # Predict the labels
          labels = self.input.model.predict(self.input.X_std)

          self._output = {
              "labels": labels,
              **self.input.get_carry()
          }

      def get_output(self) -> Tuple[VisStage, InferenceStageOutput]:
          return VisStage(), InferenceStageOutput(**self._output)


  class InitStage(IInitStage[InitStageInput, InitStageOutput, InferenceStage]):
      def compute(self) -> None:
          # Load the dataset
          X = self.input.data.data

          # Standardize the features
          scaler = StandardScaler()
          X_std = scaler.fit_transform(X)

          # Apply PCA to reduce dimensionality for visualization
          pca = PCA(n_components=2)
          X_pca = pca.fit_transform(X_std)

          # Fit a Gaussian Mixture Model
          gmm = GaussianMixture(n_components=3, random_state=42)

          self._output = {
              "X_pca": X_pca,
              "X_std": X_std,
              "model": gmm,
              **self.input.get_carry()
          }

      def get_output(self) -> Tuple[InferenceStage, InitStageOutput]:
          return InferenceStage(), InitStageOutput(**self._output)
```

Then we can define a simple controller which will be given an instance of the init stage and the input data to be passed through the pipeline.

```py
  iris = datasets.load_iris()

  input_data = InitStageInput(data=iris)
  controller = BaseController(init_data=input_data, init_stage=InitStage)
  controller.discover() # Shows a table of the connected stages

  output, run_id = controller.start()
```

And that's it! With this you can define logical processing stages for your ML inference
pipelines whilst keeping a high level of seperation.
