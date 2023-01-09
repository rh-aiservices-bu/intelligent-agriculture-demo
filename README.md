# Intelligent Agriculture Demo

This demo aims at showcasing different technologies in an intelligent agriculture context:

* AI model training and serving for disease recognition in crops
* 5G slices for two way communications between IoT/Field "devices"
* Edge computing at Telco location (MEC)
* Path optimization using Optapy and a PathFinding algorithm
* Automated model updates

## Screenshots

### Training the model

![Model training](docs/img/training-1.png)

![Model training](docs/img/training-2.png)

### Path finding

![Obstacles](docs/img/pathfinder_base.png)
*Defining the obstacles*

![Options](docs/img/pathfinder_options.png)
*Finding options*

![Obstacles](docs/img/pathfinder_optimal.png)
*Optimal path*

### Path optimization

![Path optimization](docs/img/optapy.png)
*Optimization with OptaPy*

### Application

![Path optimization](docs/img/crops_ill.png)
*Some crops are ill*

![Path optimization](docs/img/crops_healthy.png)
*Everything healthy again*

## Architecture

```mermaid
sequenceDiagram
    participant drone as Drone
    participant classification as Classification API
    participant model as Model Serving API
    participant tractor as Tractor
    participant path as Path Services API

    rect rgb(255,255,255)
    note right of drone: Image classification
        drone ->> classification: Status of this field? (/classify)
        classification ->> model: Prediction for this field? (/prediction)
        note over model: Make prediction and score
        model ->> classification: Here are the results
        alt Field must be treated
            classification ->> path: Add this field to destinations (/destination)
        end
        classification ->> drone: Update field according to status
    end

    rect rgb(255,255,255)
    note right of tractor: Tractor route computation (multiple destinations)
        loop Every 10s if tractor Route is empty
            tractor ->> path: Fields to treat? (/routefinder)
        end
        alt Destinations is empty
            path ->> tractor: No, you're clear
        else Destinations has entries
            note over path: Find best route within tractor capacity
            path ->> tractor: Yes, here is your full route
        end
    end
    

    rect rgb(255,255,255)
    note right of tractor: Tractor movement
        tractor ->> path: What's the path to go there? (/pathfinder)
        path ->> tractor: Here is the path to follow
        tractor ->> path: I have treated this field
        note over path: Remove field from destinations
        path ->> tractor: Ack, go to next destination
    end
```
