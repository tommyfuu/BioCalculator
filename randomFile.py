import os, random, shutil


def chooseRandomFile(src_dir, num_of_images, dest):
    # get all the file names
    all_image_files = []
    for _, _, files in os.walk(src_dir):
        print(files)
        for name in files:
            print("name", name)
            if ".jpg" in name:
                all_image_files.append(name)

    print("all_image_files", all_image_files)
    chosen_random_images = random.sample(all_image_files, num_of_images)
    chosen_random_jsons = [
        image.split(".")[0] + ".json" for image in chosen_random_images
    ]
    chosen_files_all = chosen_random_images + chosen_random_jsons
    print("all images", str(len(chosen_random_images)), chosen_random_images)
    # loop through to copy all chosen files
    for file_name in chosen_files_all:
        print("current file", file_name)
        full_file_name = os.path.join(src_dir, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dest)

    print("copying done")
    return


chooseRandomFile(
    "/Users/chenlianfu/Documents/Github/BioCalculator/homepage/AGAR_rearranged/train",
    15,
    "/Users/chenlianfu/Documents/Github/BioCalculator/homepage/AGAR_rearranged/randomTrial",
)
