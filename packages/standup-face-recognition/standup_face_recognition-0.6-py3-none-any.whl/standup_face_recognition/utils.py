import numpy as np
import cv2
import os
import torchvision.transforms as transforms
import torch


def resize_images(images, resize_size):
    resized_images = []

    for img in images:
        current_height, current_width, _ = img.shape

        # Calculate the new dimensions to be 5 times divisible by 2
        new_width = int(np.ceil(current_width / 2 ** 5) * 2 ** 5)
        new_height = int(np.ceil(current_height / 2 ** 5) * 2 ** 5)

        # Check if either dimension is smaller than 128
        if new_width < resize_size or new_height < resize_size:
            # Calculate the scaling factor to ensure both dimensions are at least 80
            scaling_factor = max(resize_size / new_width, resize_size / new_height)
            # Upscale both dimensions with the same factor
            new_width = int(new_width * scaling_factor)
            new_height = int(new_height * scaling_factor)

        scaling_factor_width = current_width / new_width
        scaling_factor_height = current_height / new_height

        # Resize the image using OpenCV or any other library of your choice
        resized_img = cv2.resize(img, (new_width, new_height))
        resized_images.append([resized_img, current_height, current_width, scaling_factor_height, scaling_factor_width])

    return resized_images


def resize_images_tensor(images, resize_size):
    resized_images = []
    resized_images_total = []
    for index, img in enumerate(images[0][0]):

        # Convert PyTorch tensor to NumPy array
        img_np = img.cpu().numpy()
        current_height, current_width, _ = img_np.shape

        # Calculate the new dimensions to be 5 times divisible by 2
        new_width = int(np.ceil(current_width / 2 ** 5) * 2 ** 5)
        new_height = int(np.ceil(current_height / 2 ** 5) * 2 ** 5)

        # Check if either dimension is smaller than 128
        if new_width < resize_size or new_height < resize_size:
            # Calculate the scaling factor to ensure both dimensions are at least 80
            scaling_factor = max(resize_size / new_width, resize_size / new_height)
            # Upscale both dimensions with the same factor
            new_width = int(new_width * scaling_factor)
            new_height = int(new_height * scaling_factor)

        # Resize the image using OpenCV or any other library of your choice
        resized_img = cv2.resize(img_np, (new_width, new_height))

        # Convert the resized image back to a PyTorch tensor
        resized_img_tensor = torch.from_numpy(resized_img).cuda()

        # Append information along with the resized image to the list
        resized_images.append(resized_img_tensor)

    resized_images_total.append(resized_images)
    resized_images_total.append(images[1])  # append box coor
    resized_images_total.append(images[2])  # append score
    return resized_images_total


def show_face(frame, resized_faces):
    # Plot bounding boxes
    for index, faces in enumerate(resized_faces[1][0]):
        if faces is not None:
            # for face in faces[2][0]: # uncomment if all face boxes should be visualized
            face_x1, face_y1, face_x2, face_y2 = faces
            cv2.rectangle(frame, (round(face_x1), round(face_y1)), (round(face_x2), round(face_y2)), (0, 255, 0), 2)
            # Add name to frame
            max_key = None
            max_value = float('-inf')
            for d in resized_faces[3+index]:
                # Find the key with the maximum value in the current dictionary
                current_max_key = max(d, key=d.get)
                current_max_value = d[current_max_key]

                # Update the overall maximum key and value if necessary
                if current_max_value > max_value:
                    max_key = current_max_key
                    max_value = current_max_value

            text = f"'{max_key}'"
            cv2.putText(frame, text, (round(face_x1), round(face_y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        else:
            continue

    # out.write(frame)
    cv2.imshow('Webcam output', frame)


def imread_templates(folder_path):
    image_dict = {}
    # Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # List all files in the folder
        files = os.listdir(folder_path)

        # Filter only files with specific extensions (e.g., '.png', '.jpg')
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        # Read each image and append it to the list
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = transforms.ToTensor()(image).unsqueeze(0).cuda()
            image_name = image_file.split('.')[0]
            if image is not None:
                image_dict[image_name] = image
            else:
                print(f"Failed to read image: {image_path}")
    else:
        print("Folder not found.")
    return image_dict

