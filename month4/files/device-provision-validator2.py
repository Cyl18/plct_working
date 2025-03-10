import toml
import os
import re
from subprocess import PIPE, Popen
import concurrent.futures
packages_index_path = "/home/cyan/.cache/ruyi/packages-index/manifests/board-image/"
# execute ruyi --version
def get_ruyi_version():
    p = Popen("ruyi --version", shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    regex = r'Ruyi (\d+\.\d+\.\d+)'
    match = re.search(regex, stdout.decode())
    if match:
        return match.group(1)
    return None

images = []

def search(s):
    p = Popen("ruyi device provision", shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    input = 'y\n' + s
    stdout, stderr = p.communicate(input=bytes(input, 'utf-8'))
    # get the last line of the output
    lines = stdout.decode().split('\n')
    last_line = lines[-1]
    # Choice? (1-30)
    # regex extract 30
    regex = r'Choice\? \((\d+)\-(\d+)\)'
    match = re.search(regex, last_line)
    if match:
        loop_count = int(match.group(2))
        if loop_count > 10:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(search_wrapper, s, i) for i in range(1, loop_count + 1)]
            concurrent.futures.wait(futures)
        else:
            for i in range(1, loop_count + 1):
                search(s + str(i) + "\n")
        # run this loop as parallel
    else:
        regex2 = r'board-image/(.*)$'
        for line in lines:
            match2 = re.search(regex2, line)
            if match2:
                images.append(match2.group(1))

def search_wrapper(s, i):
    search(s + str(i) + "\n")

def run_device_provision_search():
    search("")
    images1 = list(set(images))
    return images1

# --------------------

def get_packages_index_board_images():
    # get all folder names in packages_index_path
    folders = [f for f in os.listdir(packages_index_path) if os.path.isdir(os.path.join(packages_index_path, f))]
    return folders
    

#print(run_device_provision_search())
#print(get_packages_index_board_images())
# 检查 board-image 是不是都被 device provision 引用
packages_index_board_images = get_packages_index_board_images()
device_provision_board_images = run_device_provision_search()
not_referenced_images = []
#not_referenced_images2 = []

for image in packages_index_board_images:
    if image not in device_provision_board_images:
        not_referenced_images.append(image)

#for image in device_provision_board_images:
#    if image not in packages_index_board_images:
#        not_referenced_images2.append(image)

for image in not_referenced_images:
    print("Image %s is not referenced by device provision" % image)

#for image in not_referenced_images2:
#    print("Image %s is not in packages index" % image)