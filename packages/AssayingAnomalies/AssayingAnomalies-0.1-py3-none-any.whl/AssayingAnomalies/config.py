# config.py
import os
class Config:
    def __init__(self):
        self.username = None
        self.password = None
        self.sample_start = None
        self.sample_end = None
        self.domComEqFlag = None
        self.data_storage_path = None
        self.data_folder = None
        self.crspFolder = None
        self.compFolder = None
        self.daily_crsp_folder = None
        self.ff_data_folder = None
        self.num_cpus = None

    def prompt_user(self):
        self.username = str(input("Enter your WRDS username: "))
        self.password = str(input("Enter your WRDS password: "))
        self.sample_start = int(input("Enter sample start year: "))
        self.sample_end = int(input("Enter sample end year: "))

        # For Boolean input, check the string entered
        domComEqInput = input("Enter True if you would like only domestic common equity otherwise False: ")
        self.domComEqFlag = domComEqInput.strip().lower() == 'true'
        remoteInput = input("Enter True if you are using BlueHive or CIRC, otherwise False: ")
        self.remote_or_not = remoteInput.strip().lower() == 'true'

        self.data_storage_path = input("Enter the path to where you would like the downloaded data and variables"
                                       " stored. If you are using CIRC and are unsure, enter /scratch/user_id: ")

        if self.remote_or_not:
            self.num_cpus = int(input("Enter the number of CPUs. If unsure, enter 1: "))

    def make_folders(self):
        paths = []
        self.data_folder = os.path.join(self.data_storage_path, 'AA_Data')
        paths.append(self.data_folder)
        self.crspFolder = os.path.join(self.data_folder, 'CRSP')
        paths.append(self.crspFolder)
        self.compFolder = os.path.join(self.data_folder, 'COMPUSTAT')
        paths.append(self.compFolder)
        self.daily_crsp_folder = os.path.join(self.crspFolder, 'Daily')
        paths.append(self.daily_crsp_folder)
        self.ff_data_folder = os.path.join(self.data_folder, 'FFData')
        paths.append(self.ff_data_folder)
        for path in paths:
            os.makedirs(path, exist_ok=True)

    def set_up(self):
        self.prompt_user()
        self.make_folders()

# test = Config()
# test.prompt_user()

