from fastapi import File, UploadFile, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from tensorflow import expand_dims
from tensorflow.nn import relu
from numpy import argmax
from numpy import max
from numpy import array
from json import dumps
from uvicorn import run
import os
import uuid

# App creation
app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)

# Model loading and preparation
model_dir = "crops_96.31.h5"
model = load_model(model_dir)
class_predictions = array([
    'Corn___Common_Rust',
    'Corn___Gray_Leaf_Spot',
    'Corn___Healthy',
    'Corn___Northern_Leaf_Blight',
    'Potato___Early_Blight',
    'Potato___Healthy',
    'Potato___Late_Blight',
    'Rice___Brown_Spot',
    'Rice___Healthy',
    'Rice___Leaf_Blast',
    'Rice___Neck_Blast',
    'Wheat___Brown_Rust',
    'Wheat___Healthy',
    'Wheat___Yellow_Rust'
])


# Base API
@app.get("/")
async def root():
    return {"message": "Status:OK"}


# Model API
@app.post("/prediction")
async def get_net_image_prediction(file: UploadFile = File(...)):
    # Save the file locally, with uuid to avoid collision
    try:
        contents = file.file.read()
        filename = str(uuid.uuid4())
        with open('/tmp/' + filename, 'wb') as f:
            f.write(contents)
        print("File received")
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    # Loads the image formatted to the trained model size
    img = load_img(
        '/tmp/' + filename,
        target_size=(200, 200)
    )

    # Transform image to array
    img_array = img_to_array(img)
    img_array = expand_dims(img_array, 0)

    # Do the prediction
    pred = model.predict(img_array)

    # Retrieve result
    class_prediction = class_predictions[argmax(pred[0])]
    score = max(pred[0])
    print(f'Class prediction: {class_prediction}')
    model_score = round(max(score) * 100, 2)
    print(f'Model score: {model_score}')

    # Cleanup saved file
    try:
        os.remove('/tmp/' + filename)
    except Exception:
        return {"message": "There was an error deleting the file"}

    # Return JSON-formatted results
    return {
        "model_prediction": class_prediction,
        "model_prediction_confidence_score": model_score
    }

# Launch the FastAPI server
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    run(app, host="0.0.0.0", port=port)