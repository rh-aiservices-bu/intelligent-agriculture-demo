# List of variables and values

## Scene variables

* _configurationJSON, String: JSON string returned when reading the configuration file
* _configuration, Structure: Configuration object
  * classificationURL, String: URL of classification service
  * droneSpeed, String: Drone speed
  * illCropInitialPercentage, String: Percentage of crops ill at start (1-100)
* _randomResult, Number: Temp var to store random result
* _dronePositionNumber, Number: Drone position on path Array
* _dronePositionLegs, Number: number of legs in the path
* _droneDestinationX, Number: X destination of drone
* _droneDestinationY, Number: Y destination of drone
* _droneRestart, Boolean: True if drone needs to be sent back at start
* _classificationResultJSon, String: JSON string returned when calling the classification service
* _classificationResult, Structure: Classification object result
  * status, String: Status of crop in {"healthy", "ill"}
  * disease, String: Type of disease in {"wheat_yellow_rust", "wheat_brown_rust", "corn_common_rust", "corn_gray_leaf_spot", "corn_northern_leaf_blight", "potato_early_blight", "potato_late_blight"}
* _errorMessage, String: Text to be displayed for errors

## Object Variables

For all crops types:

* status, String: Status of crop in {"healthy", "ill"}
* disease, String: Type of disease in {"wheat_yellow_rust", "wheat_brown_rust", "corn_common_rust", "corn_gray_leaf_spot", "corn_northern_leaf_blight", "potato_early_blight", "potato_late_blight"}
* frame, Number: frame number in animation for object CropPicture
