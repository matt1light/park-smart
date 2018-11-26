def localize_objects(path):
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    coords = []

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image, ).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
        if object_.name == "Car" or object_.name == "Motorcycle":
            vertices = object_.bounding_poly.normalized_vertices
            left = vertices[0].x
            right = vertices[1].x
            top = vertices[0].y
            bottom = vertices[2].y

            coords.append([left, right, top, bottom])

    return coords


