# BioCalculator Development Notes

## Progress

### 1. Calculator Implementation

- Dilution calculation implemented, functions to undergo testing; need to add unit conversion later.
- Unit conversion waiting to be implemented.
- PCR calculator being implemented: basic functionalities implemented, waiting to be refined; output not rendered.

### 2. Website general

- About/Contact pages waiting to be made better.
- Within-site hotlinks need to be fixed.

### 3. Miscellaneous

- Requirements for developement in `requirements.txt` in thr development folder. In order to install all the required dependencies, do `pip3 install -r requirements.txt`.

### 4. Guides

#### 4.1 Guide to create and render a complete calculator

- You should implement your calculator by referencing [calculatorDilution.py](https://github.com/tommyfuu/BioCalculator/blob/main/homepage/calculatorDilution.py).
- You should implement your visual with an html file by referencing [concentrationCalc.html](https://github.com/tommyfuu/BioCalculator/blob/main/homepage/templates/concentrationCalc.html).
- You should add your html file to the url file [here](https://github.com/tommyfuu/BioCalculator/blob/main/homepage/urls.py).
- You should render your calculator in the `dilution_input_view` function in [views.py](https://github.com/tommyfuu/BioCalculator/blob/main/homepage/views.py).
