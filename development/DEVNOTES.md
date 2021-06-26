# BioCalculator Development Notes

## Progress

Starting from 6/15/2021, please start to commit your changes to the `development` branch instead of the main branch! The main branch has been synced with the deployed website so any changes made there will be reflected on the actual website. Make sure that the things function before merging things into the main branch :)

### 1. Calculator Implementation

- Concentration change calculator completed.
- Deployment completed and tested, ready to be deployed when needed.
- Unit conversion being tested and bug fixing.
- Cutting reaction being implemented and tested.
- PCR calculator being implemented: basic functionalities implemented, waiting to be refined; output not rendered.

### 2. Website general

- Aesthetics to be improved.

### 3. Miscellaneous

- Requirements for development in `requirements.txt` in the development folder. In order to install all the required dependencies, do `pip3 install -r requirements.txt`.

### 4. Guides

#### 4.1 Guide to create and render a complete calculator

- You should implement your calculator by referencing [calculatorDilution.py](https://github.com/tommyfuu/BioCalculator/blob/main/homepage/calculatorDilution.py).
- You should implement your visual with an html file by referencing [concentrationCalc.html](https://github.com/tommyfuu/BioCalculator/blob/main/homepage/templates/concentrationCalc.html).
- You should add your html file to the url file [here](https://github.com/tommyfuu/BioCalculator/blob/main/homepage/urls.py).
- You should render your calculator in the `dilution_input_view` function in [views.py](https://github.com/tommyfuu/BioCalculator/blob/main/homepage/views.py).

### in case you forget about how to run django again

```
python manage.py runserver # running it
python manage.py migrate # add changes to remote
python manage.py createsuperuser
```
