import os
import io
from google.cloud import vision
from google.cloud.vision import types

# Validate credentials for this application
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.getcwd()+"/json/text-extraction-key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/rodarg/Documents/Citi/Sprint4/json/text-extraction-key.json"


def detect_text(images, path="images/"):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    # Temp, make it so that we iterate through all images instead of just accessing [0]
    image_name = images[0]

    with io.open(path+image_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    receipts = []
    for text in texts:
        text_payload = '\n"{}"'.format(text.description)
        receipts.append(text_payload)
        print(text_payload)

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    # receipts[0] is the whole text, subsequent indexes are the individual words
    return receipts[0]