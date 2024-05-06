def get_prediction(model, data_encoded, data):
    result = model.predict(data_encoded)

    # Add results as column in dataframe
    data['prediction'] = result

    return data


