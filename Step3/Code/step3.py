import os
import json
import pickle
import datetime
import tkinter as tk
from tkinter import (
    ttk,
    OptionMenu,
    StringVar,
    messagebox
)


class Component(object):
    def __init__(self, serial_number=None, component_type='Winglet Strut', size_fit='A320 Series', status='Manufactured-Unfinished'):
        """Constructor"""
        self._serial_number = serial_number         # 1 to 99
        # Winglet Dtrut, Door handle, Rudder Pin
        self._component_type = component_type
        # A320 Series, A380 Series, 10x75, 12x100, 16x150
        self._size_fit = size_fit
        self._status = status                       # Polish, Paint

    # get_serial_number() function is accessible to class Batch
    def get_serial_number(self):
        return self._serial_number

    # set_serial_number is accessible outside the class
    def set_serial_number(self, serial_number):
        self._serial_number = serial_number

class Batch(Component):
    def __init__(self, batch_number, serial_number, location="Not Allocated"):
        """Constructor"""
        super(Batch, self).__init__(serial_number)
        self._date_manufacture = datetime.datetime.today().strftime('%Y%m%d')
        self._batch_create = datetime.datetime.today().strftime('%H%M')
        self._batch_number = batch_number
        self._location = location

    def create_sn_component(self, component_type, size_fit):
        sn = []
        x = 1
        
        sn_component = int(self.get_serial_number())
        while x <= sn_component:
            sn.append({
                "sn_component": self.create_batch_number() + '-' + self.add_zero(x),
                'type_components': component_type, 
                'size_fitment_comps': size_fit, 
                'status': self._status
            })
            x += 1
        return sn

    def create_batch_number(self):
        batch_num = int(self._batch_number)

        return self._date_manufacture + self.add_zero(batch_num)

    # I have used a static method because I don't need  the self to be passed as the first argument
    @staticmethod
    def add_zero(arg):
        x = 1
        batch = None
        while x <= arg:
            if x < 10:
                batch = '000' + str(x)
            elif 10 <= x < 100:
                batch = '00' + str(x)
            elif 100 <= x < 1000:
                batch = '0' + str(x)
            else:
                batch = str(x)

            x += 1

        return batch

class App(tk.Frame):
    # Initialize Method
    def __init__(self, master):
        """Constructor"""
        tk.Frame.__init__(self, master)
        # Set the Font and color of Nee Batch Frame
        s = ttk.Style()
        s.configure('Blue.TLabelframe.Label', font=('courier', 13, 'bold'))
        s.configure('Blue.TLabelframe.Label', foreground='#374e9b')
        # get screen width and height
        self.master.geometry('800x820')
        # Add a tittle on window
        self.master.title("PPEC - Inventory System")

        # Create instance for menu frame, this is the Menu Frame in the Main Window
        self._menu_frame = ttk.LabelFrame(
            self.master, text=' Menu ', style="Blue.TLabelframe")
        # Create instance for menu frame, this is the New Batch Frame in the Main Window
        self._create_batch_frame = ttk.LabelFrame(
            self.master, text=' Create New Batch ', style="Blue.TLabelframe")
        self._list_batch_frame = ttk.LabelFrame(
            self.master, text=' List All Batches ', style="Blue.TLabelframe")
        self._detail_batch_frame = ttk.LabelFrame(
            self.master, text=' View Details Batch ', style="Blue.TLabelframe")
        self._detail_comp_frame = ttk.LabelFrame(
            self.master, text=' View Details Component ', style="Blue.TLabelframe")
        self._show_details_frame = ttk.LabelFrame(
            self.master, text=' Batch Details', style="Blue.TLabelframe")
        self._comp_allocation_frame = ttk.LabelFrame(
            self.master, text=' Allocation Stock ', style="Blue.TLabelframe")
        
        # Initialize path and filename of json file
        self.path = '../Data'
        self.filename = 'BatchIndex'
        self.file_path_name_w = './' + self.path + '/' + self.filename + '.json'

        # Dictionary for dropdown components type
        self.choices_comp = {'Door handle': ['A320 Series', 'A380 Series'],
                             'Rudder Pin': ['A320 Series', 'A380 Series','10x75', '12x100', '16x150'],
                             'Winglet Strut': ['A320 Series', 'A380 Series']
                            }
        
        # Place Dropdown into the container element create a new status
        self.choices_status = {'Paint': ['AJ74','AB76', 'BT98', 'DF56', 'BE43'],
                                'Polished': ['No Code']
                            }

        # Create a Tkinter variable for dropdown
        self.tk_var = StringVar(self) 
        self.entry_type_comp = StringVar(self)
        self.entry_size_fitment = StringVar(self)
        self.entry_choose_location = StringVar(self)
        # Create a Tkinter variable for input
        self.entry_batch_no = StringVar(self)  
        self.entry_components = StringVar(self) 

        # Call methods
        self.create_menu()
        self._inventory = self.create_json_file()
        self.create_batch_pkl_file()
        self.create_comp_pkl_file()
    
    # Create json file and save all batch created
    def create_json_file(self):
        # Input the try except in a while loop, because try to see if file exist if not exist give an error that is catch by except,
        # the exception take the data and save into file and create, and start the loop again, this time check that file exist so open the file
        while True:
            try:
                fh = open(self.file_path_name_w, 'rb+')
                data_file = json.load(fh)
                return data_file
                break
            except FileNotFoundError:
                data = {'Batch': []}
                self.save_data(data)
                continue

    def save_data(self, datafile):
        # Write Data
        with open(self.file_path_name_w, 'w+') as fp:
            fp.write(json.dumps(datafile, indent=2, sort_keys=False))
        fp.close()
    
    # Create batch pickle file from json file
    def create_batch_pkl_file(self):
        # list to collect data from json file  and save into pickle file
        with open('../Data/BatchIndex.json') as json_file:
            # load the json file to check data saved inside
            data = json.load(json_file)

            # Check json file inside the Batch List all Ojects and save each object in a single pickle file with value of key:number
            for batch_obj in data['Batch']:
                number = batch_obj['number']
                qty_comp = batch_obj['quantity_comp']
                manufacture_date = batch_obj['manufacture_date']
                location = batch_obj['location']
                component = batch_obj['component']

                i = 0
                comps = []
                
                while i < len(component):
                    sn_component = component[i]['sn_component']
                    type_components = component[i]['type_components']
                    size_fitment_comps = component[i]['size_fitment_comps']
                    status = component[i]['status']
                    comps.append([sn_component,type_components,size_fitment_comps,status])
                
                    i += 1
                    
                self.file_path_name_pkl_w = './' + self.path + '/' + batch_obj['number'] + '.pkl'

                batch = [number, qty_comp, manufacture_date, location, comps]
                batch_dict = { batch[0]: batch }
                self.save_batch_pkl_data(batch_dict)
                
    def save_batch_pkl_data(self, pkl_batch_file):
        # Write Data
        with open(self.file_path_name_pkl_w, 'wb') as fhp:
            pickle.dump(pkl_batch_file, fhp)
        fhp.close()

    # Create components pickle file from json file
    def create_comp_pkl_file(self):
         # list to collect data from json file  and save into pickle file
        with open('../Data/BatchIndex.json') as json_file:
            # load the json file to check data saved inside
            data = json.load(json_file)

            # Check json file inside the Batch List all Ojects and save each object in a single pickle file with value of key:number
            for batch_obj in data['Batch']:
                
                for comp_obj in batch_obj['component']:
                    sn_component = comp_obj['sn_component']
                    type_components = comp_obj['type_components']
                    size_fitment_comps = comp_obj['size_fitment_comps']
                    manufacture_date = batch_obj['manufacture_date']
                    status = comp_obj['status']
                    number = batch_obj['number']
                    location = batch_obj['location']

                    self.file_path_name_comp_pkl_w = './' + self.path + '/' + comp_obj['sn_component'] + '.pkl'

                    # batch = [sn_component, type_components, size_fitment_comps, manufacture_date, status, number]
                    # data[batch_obj['sn_component'][comp_obj]] = batch
                    comp = [sn_component, type_components, size_fitment_comps, manufacture_date, status, location, number]
                    comp_dict = { comp[0]: comp }
                    self.save_comp_pkl_data(comp_dict)
    
    def save_comp_pkl_data(self, pkl_comp_file):
        # Write Data
        with open(self.file_path_name_comp_pkl_w, 'wb') as fhcp:
            pickle.dump(pkl_comp_file, fhcp)
        fhcp.close()
    
    # this method manage the choice you make on the dropdown options menu, display in the frame below the menu the choice you made
    def change_dropdown(self, *args):
        option = self.tk_var.get()
        # set a dictionary with coice for menu
        choice_dict = {
            '1': self.create_new_batch,
            '2': self.list_all_batches,
            '3': self.view_details_batch,
            '4': self.view_details_comp,
            '5': self.show_frame_allocation,
            '6': self.close_app
        }
        # call the methods that user choose from the dropdown menu
        choice_dict.get(option, self.create_menu)()

    """ this method manage the choice you do for the component, for one type component you choose, 
        display the size/fit for the this specific component """
    def search_product_options(self, *args):
        comp_types = self.choices_comp[self.entry_type_comp.get()]
        self.entry_size_fitment.set(comp_types[0])
    
        menu = self.optionmenu_size_fitment['menu']
        menu.delete(0, 'end')

        for comp_type in comp_types:
            menu.add_command(label=comp_type, command=lambda c_type=comp_type: self.entry_size_fitment.set(c_type))

    # Check if number of batch exist
    def check_batch_number_exist(self):
        entry_batch_no = self.entry_batch_no.get()
        # Check if the bacth insert is a number
        if self.isNumber(entry_batch_no):
            new_batch = Batch(entry_batch_no, None)
            batch_num = new_batch.create_batch_number() 

            try:
                data = self.create_json_file()
                temp_list = []
                # Access data
                for dict_obj in data['Batch']:
                    temp_list.append(dict_obj['number'])

                if batch_num in temp_list:
                    messagebox.showinfo('Oooops!!', 'The batch number ' + batch_num + ' already exist')
                else:
                    self.show_msg_before_save()
            except (ValueError, KeyError, TypeError):
                messagebox.showerror('Comp Json Error', 'Is not a number, enter a valid number.')
        else:
            messagebox.showerror('Warning', 'Is not a number, enter a valid number.')
    
    # Check the input is a number
    def isNumber(self, value):
        try:
            val = int(value) # check if the parameter passed is numeric
            return True # if so return True
        except (TypeError, ValueError): # if the params is not numeric the exception is a TypeError or ValueError
            return False # return False

    # This method create a menu with a dropdown to choice options
    def create_menu(self):
        # Create a container to hold all label for menu
        self._menu_frame.grid(column=0, row=8, padx=10, pady=10, ipadx=40, sticky=tk.W)

        # Dictionary with options
        choices = {'1', '2', '3', '4', '5', '6'}
        # set the default label in the dropdown option
        self.tk_var.set('Options')

        # Create the Dropdown Menu Option
        OptionMenu(self._menu_frame, self.tk_var, *sorted(choices)).grid(column=1, row=8, ipadx=5)

        # Place labels into the container element menu_frame
        ttk.Label(self._menu_frame, text="1. Create a New Batch").grid(
            column=0, row=0, sticky=tk.W)
        ttk.Label(self._menu_frame, text="2. List All Batches").grid(
            column=0, row=1, sticky=tk.W)
        ttk.Label(self._menu_frame, text="3. View details of a Batch").grid(
            column=0, row=2, sticky=tk.W)
        ttk.Label(self._menu_frame, text="4. View Details of Components").grid(
            column=0, row=3, sticky=tk.W)
        ttk.Label(self._menu_frame, text="5. Allocate Manufactured Stock").grid(
            column=0, row=4, sticky=tk.W)
        ttk.Label(self._menu_frame, text="6. Quit").grid(
            column=0, row=5, sticky=tk.W)
        ttk.Label(self._menu_frame, text="Choose the option:").grid(
            column=0, row=8, ipady=10, sticky=tk.W)

        # link function to change dropdown and pass the choice as an argument
        self.tk_var.trace('w', self.change_dropdown)

        for child in self._menu_frame.winfo_children():
            child.grid_configure(padx=10, pady=4)

    # This method create a frame with all input to create a new batch
    def create_new_batch(self):
        self._show_details_frame.grid_remove()
        self._list_batch_frame.grid_remove()
        self._detail_batch_frame.grid_remove()
        self._detail_comp_frame.grid_remove()
        self._comp_allocation_frame.grid_remove()

        # Create a new Object from Batch class
        new_batch = Batch(batch_number='0', serial_number='0')
        # remove the button for exit to application
        self._show_details_frame.grid_remove()
        # Create a container to hold all label for menu
        self._create_batch_frame.grid(
            column=0, row=10, padx=10, pady=10, ipadx=40, sticky=(tk.N, tk.W, tk.E, tk.S))
        # Place labels into the container element create new batch
        ttk.Label(self._create_batch_frame, text="Batch number:").grid(
            column=0, row=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self._create_batch_frame, text="{}".format(new_batch._date_manufacture)).grid(
            column=1, row=0, padx=0, pady=10, sticky=tk.W)
        ttk.Label(self._create_batch_frame, text="How many components\n in this Batch (1 to 9999):").grid(
            column=0, row=1, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self._create_batch_frame, text="Select component type:").grid(
            column=0, row=2, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self._create_batch_frame, text="Select Size/Fitment type:").grid(
            column=0, row=3, padx=10, pady=10, sticky=tk.W)
        # Place Entry into the container element create new batch
        ttk.Entry(self._create_batch_frame, textvariable=self.entry_batch_no).grid(
            column=1, row=0, padx=52, pady=10)
        ttk.Entry(self._create_batch_frame, textvariable=self.entry_components).grid(
            column=1, row=1)
        # Place Dropdown into the container element create a new batch
        self.entry_type_comp.trace('w', self.search_product_options)

        self.optionmenu_type_comp = OptionMenu(self._create_batch_frame, self.entry_type_comp, *sorted(self.choices_comp.keys()))
        self.optionmenu_size_fitment = OptionMenu(self._create_batch_frame, self.entry_size_fitment, '')

        self.entry_type_comp.set('Door handle')

        self.optionmenu_type_comp.grid(column=1, row=2, padx=20, pady=10, ipadx=5)
        self.optionmenu_size_fitment.grid(column=1, row=3, padx=20, pady=10, ipadx=5)

        # Place Buttons into the container element create new batch and call the methods check_batch_number_exist
        ttk.Button(self._create_batch_frame, text="Create Batch", command=self.check_batch_number_exist).grid(
            column=0, row=4, padx=10, pady=10, sticky=tk.W)

    # Show the message on separated windows of the batch created.
    def show_msg_before_save(self):
        entry_batch_no = self.entry_batch_no.get()
        entry_no_comps = self.entry_components.get()
        entry_type_comps = self.entry_type_comp.get()
        entry_size_fit = self.entry_size_fitment.get()
        # Call Date Class
        new_batch = Batch(entry_batch_no, entry_no_comps)
        sn_comps = new_batch.create_sn_component(entry_type_comps, entry_size_fit)
        batch_num = new_batch.create_batch_number()
        # Save in a variable the value return from Batch Object
        date_manufacture = new_batch._date_manufacture
        # Setting up the message box
        show_msg_saving = messagebox.askyesno(
            'Warning!',
            'This batch No {}\ncreated at {}\ncontains {} {} {}\n\n\tis this correct!'.format(
                batch_num, date_manufacture, len(sn_comps), entry_size_fit, entry_type_comps, _icon='warning')
        )
        # If click "yes" the details insert is saved on BatchIndex.json file
        if show_msg_saving:
            # Setting up the messagebox for show batch detail
            show_msg_details = messagebox.askyesno(
                'Batch Created',
                'Batch and Component records created at {} on {}\n\nShow Batch details?'.format(
                    new_batch._batch_create, date_manufacture, _icon='info')
            )
            # If click "Yes" The batch details are displayed
            if show_msg_details:
                self.show_details_batch()
            # Call the method that Save the detail on json file
            self.save_batch_to_json_file(self._inventory)
            self.create_batch_pkl_file()
            self.create_comp_pkl_file()

    # Show the details of the batch created
    def show_details_batch(self):
        print('New Batch Details Method Called')
        entry_batch_no = self.entry_batch_no.get()
        entry_no_comps = self.entry_components.get()
        entry_type_comps = self.entry_type_comp.get()
        entry_size_fit = self.entry_size_fitment.get()
        # Call Date Class
        new_batch = Batch(entry_batch_no, entry_no_comps)
        sn_comps = new_batch.create_sn_component(entry_type_comps,entry_size_fit)
        batch_num = new_batch.create_batch_number()
        comp_location = new_batch._location

        sn = []
        comps = []
        for item in sn_comps:
            sn.append(item['sn_component'] )
            comps.append(item['sn_component'] + ' ' + item['status'])

        comps = "\n\t".join(comps)

        # Save in a variable the value return from Batch Object
        date_manufacture = new_batch._date_manufacture
        # remove the button for exit to application
        self._create_batch_frame.grid_remove()
        # Create a container to hold all label for menu
        self._show_details_frame.grid(column=0, row=10, padx=10, pady=10, ipadx=40, sticky=(tk.N, tk.W, tk.E, tk.S))
        # Place labels into the container element create new batch
        ttk.Label(self._show_details_frame, text="Batch number:\t{}".format(batch_num)).grid(
            column=0, row=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self._show_details_frame, text="Manufacture Date:\t{}".format(date_manufacture)).grid(
            column=0, row=1, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self._show_details_frame, text="Component type:\t{}".format(entry_type_comps)).grid(
            column=0, row=2, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self._show_details_frame, text="Component Size/Fitment type: {}".format(entry_size_fit)).grid(
            column=0, row=3, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self._show_details_frame, text="SerialNumbers: {}".format(sn)).grid(
            column=0, row=4, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self._show_details_frame, text="Component Status: [\n\t{}\n\t]".format(comps)).grid(
            column=0, row=5, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self._show_details_frame, text="Component Location: {}".format(comp_location)).grid(
            column=0, row=6, padx=10, pady=10, sticky=tk.W)

    # This method show all batches
    def list_all_batches(self):
        self._show_details_frame.grid_remove()
        self._create_batch_frame.grid_remove()
        self._detail_batch_frame.grid_remove()
        self._detail_comp_frame.grid_remove()
        self._comp_allocation_frame.grid_remove()

        # Open file json for retrieving all batch saved
        fh = open(self.file_path_name_w, 'r')
        data_file = json.load(fh)
        fh.close() 

        # Loop for display all list Batches
        r = 1
        for list_batch in data_file['Batch']:
            batch_number = list_batch['number']
            quantity_comp = list_batch['quantity_comp']
            allocated_location = list_batch['location']
            for comp in list_batch['component']:
                type_components = comp['type_components']
                size_fitment_comps = comp['size_fitment_comps']
            
            # Place labels into the container element create row for each batch
            ttk.Label(self._list_batch_frame, text=batch_number).grid(column=0, row=r, padx=10, pady=10, sticky=tk.W)
            ttk.Label(self._list_batch_frame, text=type_components).grid(column=1, row=r, padx=10, pady=10, sticky=tk.W)
            ttk.Label(self._list_batch_frame, text=size_fitment_comps).grid(column=2, row=r, padx=10, pady=10, sticky=tk.W)
            ttk.Label(self._list_batch_frame, text=quantity_comp).grid(column=3, row=r, padx=10, pady=10, sticky=tk.W)
            ttk.Label(self._list_batch_frame, text=allocated_location).grid(column=4, row=r, padx=10, pady=10, sticky=tk.W)

            r += 1

        # Create a container to hold all label for menu
        self._list_batch_frame.grid(column=0, row=10, padx=10, pady=10, ipadx=40, sticky=(tk.N, tk.W, tk.E, tk.S))
        # Place labels into the container element create new batch
        ttk.Label(self._list_batch_frame, text="Batch number").grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self._list_batch_frame, text="Type").grid(column=1, row=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self._list_batch_frame, text="Size/Fitment").grid(column=2, row=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self._list_batch_frame, text="Quantity Made").grid(column=3, row=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self._list_batch_frame, text="Location").grid(column=4, row=0, padx=10, pady=10, sticky=tk.W)

    # Show detail of the batch   
    def view_details_batch(self):
        self._show_details_frame.grid_remove()
        self._create_batch_frame.grid_remove()
        self._detail_comp_frame.grid_remove()
        self._list_batch_frame.grid_remove()
        self._comp_allocation_frame.grid_remove()

        # Create a container to hold all label for menu
        self._detail_batch_frame.grid(
            column=0, row=10, padx=10, pady=10, ipadx=40, sticky=(tk.N, tk.W, tk.E, tk.S))
        # Place labels into the container element create new batch
        ttk.Label(self._detail_batch_frame, text="Batch number:").grid(
            column=0, row=0, padx=10, pady=10, sticky=tk.W)
        # Place Entry into the container element create new batch
        ttk.Entry(self._detail_batch_frame, textvariable=self.entry_batch_no).grid(
            column=1, row=0, padx=52, pady=10)
        # Place Buttons into the container element create new batch
        ttk.Button(self._detail_batch_frame, text="Show Details", command=lambda : self.check_batch_exist(self.entry_batch_no.get())).grid(
            column=0, row=9, padx=10, pady=10, sticky=tk.W)

    # Check if batch exist, receive parameter from view_details_batch()
    def check_batch_exist(self, code):
        # Check if the bacth insert is a number
        if self.isNumber(code):
            
            if os.path.exists('../Data/' + code + '.pkl'):
                fhb = open('../Data/' + code + '.pkl', 'rb+')
                data = pickle.load(fhb)
                comps = []
                compStatus = []

                if code in data.keys():
                    # if the code is correct and exist execute the statement
                    batchDetail = data[code]  # pass to variable the element value to collect the right elements from the same list
                    ttk.Label(self._detail_batch_frame, text="Batch Number:\t{}".format(batchDetail[0])).grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
                    ttk.Label(self._detail_batch_frame, text="Location:\t{}".format(batchDetail[3])).grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)
                    ttk.Label(self._detail_batch_frame, text="Manufacture date:\t{}".format(batchDetail[2])).grid(column=0, row=3, padx=10, pady=10, sticky=tk.W)
                    ttk.Label(self._detail_batch_frame, text="Type:\t{}".format(batchDetail[4][0][1])).grid(column=0, row=4, padx=10, pady=10, sticky=tk.W)
                    ttk.Label(self._detail_batch_frame, text="Size/Fit:\t{}".format(batchDetail[4][0][2])).grid(column=0, row=5, padx=10, pady=10, sticky=tk.W)
                    ttk.Label(self._detail_batch_frame, text="Number Components in Batch:\t{}".format(batchDetail[1])).grid(column=0, row=6, padx=10, pady=10, sticky=tk.W)
                    n_comps = int(batchDetail[1])
                    i = 0
                    for i in range(n_comps):
                        comps.append(batchDetail[4][i][0])
                        compStatus.append(batchDetail[4][i][0] + ' ' + batchDetail[4][i][3])
                        
                    ttk.Label(self._detail_batch_frame, text="SN Component:\t{}".format(comps)).grid(column=0, row=7, padx=10, pady=10, sticky=tk.W)
                    ttk.Label(self._detail_batch_frame, text="Component Status: [\n\t{}\n\t]".format("\n\t".join(compStatus))).grid(column=0, row=8, padx=10, pady=10, sticky=tk.W)
                
                return True
                
            else:
                messagebox.showwarning('Warning','Batch not found')
                return False
        else:
            messagebox.showerror('Warning', 'Is not a number, enter a valid number.')

    # Show detail of components
    def view_details_comp(self):
        self._show_details_frame.grid_remove()
        self._create_batch_frame.grid_remove()
        self._detail_batch_frame.grid_remove()
        self._list_batch_frame.grid_remove()
        self._comp_allocation_frame.grid_remove()

        # Create a container to hold all label for menu
        self._detail_comp_frame.grid(
            column=0, row=10, padx=10, pady=10, ipadx=40, sticky=(tk.N, tk.W, tk.E, tk.S))
        # Place labels into the container element create new batch
        ttk.Label(self._detail_comp_frame, text="Component SN:").grid(
            column=0, row=0, padx=10, pady=10, sticky=tk.W)
        # Place Entry into the container element create new batch
        ttk.Entry(self._detail_comp_frame, textvariable=self.entry_components).grid(
            column=1, row=0, padx=52, pady=10)
        # Place Buttons into the container element create new batch
        ttk.Button(self._detail_comp_frame, text="Show Details", command=lambda : self.check_comp_exist(self.entry_components.get())).grid(
            column=0, row=7, padx=10, pady=10, sticky=tk.W)
    
    # This method allocate a batch
    def show_frame_allocation(self):
        self._show_details_frame.grid_remove()
        self._create_batch_frame.grid_remove()
        self._detail_batch_frame.grid_remove()
        self._list_batch_frame.grid_remove()
        self._detail_comp_frame.grid_remove()

        # Dictionary for dropdown location
        choices_location = {'Dubai','Paisley'}
        # set the default label in the dropdown option
        self.entry_choose_location.set('Paisley')

        # Create a container to hold all label for menu
        self._comp_allocation_frame.grid(
            column=0, row=10, padx=10, pady=10, ipadx=40, sticky=(tk.N, tk.W, tk.E, tk.S))
        # Place labels into the container element create new batch
        ttk.Label(self._comp_allocation_frame, text="Enter Batch Number:").grid(
            column=0, row=0, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self._comp_allocation_frame, text="Choose Location:").grid(
            column=0, row=1, padx=10, pady=10, sticky=tk.W)
        # Place Entry into the container element create new batch
        ttk.Entry(self._comp_allocation_frame, textvariable=self.entry_batch_no).grid(
            column=1, row=0, padx=52, pady=10)

        # Place Dropdown into the container element create a new batch
        OptionMenu(self._comp_allocation_frame, self.entry_choose_location, *
                   sorted(choices_location)).grid(column=1, row=1, padx=20, pady=10, ipadx=5)

        # Place Buttons into the container element create new batch
        ttk.Button(self._comp_allocation_frame, text="Allocate", command=lambda : self.check_allocation(self.entry_choose_location.get(), self.entry_batch_no.get())).grid(
            column=0, row=7, padx=10, pady=10, sticky=tk.W)
    
    def check_allocation(self, loc, code):
        # Check if the bacth insert is a number
        if self.isNumber(code):
            # Check if file exist, if so open and read
            if os.path.exists('../Data/' + code + '.pkl'):
                fhb = open('../Data/' + code + '.pkl', 'rb+')
                data = pickle.load(fhb)
                fhb.close()

                if code in data.keys():
                    # if the code is correct and exist execute the statement
                    batchDetail = data[code]  # pass to variable the element value to collect the right elements from the same list
                    if (batchDetail[3] != 'Not Allocated'):
                        messagebox.showwarning('warning', 'Batch Already Allocated')
                    else:
                        yes_allocate_comp = messagebox.askyesno('Allocation', 'Batch Not Allocated, do you like to allocate batch num: {}?'.format(batchDetail[0]))
                        if yes_allocate_comp:
                            self.update_allocation_batch(loc, code)
            else:
                messagebox.showwarning('Warning','Batch not found')
        else:
            messagebox.showerror('Warning', 'Is not a number, enter a valid number.')

    def update_allocation_batch(self, loc, batchN):
        # Open json file and read and load data in a variable
        with open(self.file_path_name_w, 'r+') as f:
            data = json.load(f)
            for list_batch in data['Batch']:
                if (list_batch['number'] == batchN):
                    list_batch['location'] = loc

            f.seek(0)        # should reset file position to the beginning.
            json.dump(data, f, indent=2)
            f.truncate()     # remove remaining part
            f.close()        # close the file
            # update also pickle file
            self.create_batch_pkl_file()
            self.create_comp_pkl_file()

            messagebox.showinfo('Allocate', 'This Batch is now allocated and will be shipped to the {} location'.format(loc))
 
    # Check if component exist by receiving parameter from view_details_comp()
    def check_comp_exist(self, code):
        # Check if file exist, if so open and read
        if os.path.exists('../Data/' + code + '.pkl'):
            fhb = open('../Data/' + code + '.pkl', 'rb+')
            data = pickle.load(fhb)

            if code in data.keys():
                # if the code is correct and exist execute the statement
                compDetail = data[code]  # pass to variable the element value to collect the right elements from the same list
                ttk.Label(self._detail_comp_frame, text="Component Detail for:\t{}".format(compDetail[0])).grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
                ttk.Label(self._detail_comp_frame, text="Type:\t{}".format(compDetail[1])).grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)
                ttk.Label(self._detail_comp_frame, text="Size/Fit:\t{}".format(compDetail[2])).grid(column=0, row=3, padx=10, pady=10, sticky=tk.W)
                ttk.Label(self._detail_comp_frame, text="Date of Manufacture:\t{}".format(compDetail[3])).grid(column=0, row=4, padx=10, pady=10, sticky=tk.W)
                ttk.Label(self._detail_comp_frame, text="Current Status:\t{}".format(compDetail[4])).grid(column=0, row=5, padx=10, pady=10, sticky=tk.W)
                ttk.Label(self._detail_comp_frame, text="Part of Batch:\t{}".format(compDetail[6])).grid(column=0, row=6, padx=10, pady=10, sticky=tk.W)
            
            return True
            
        else:
            messagebox.showwarning('Warning','Component not found')
            return False

    """ The method save_batch_to_json_file() is called when you click "yes" on the message box that appear 
        when click "Create batch" button and save all data in BatchIndex.json file.
    """
    def save_batch_to_json_file(self, inventory):
        entry_batch_no = self.entry_batch_no.get()
        entry_no_comps = self.entry_components.get()
        entry_type_comps = self.entry_type_comp.get()
        entry_size_fit = self.entry_size_fitment.get()
        # Call Date Class
        new_batch = Batch(entry_batch_no, entry_no_comps)
        sn_comps = new_batch.create_sn_component(entry_type_comps,entry_size_fit)
        batch_num = new_batch.create_batch_number()
        manufacture_date = new_batch._date_manufacture
        # Dictionary to collect data and save into json file
        a_dict = {}
        #data = self.create_json_file()
        temp_list = []
        for dic_obj in inventory["Batch"]:
            temp_list.append(dic_obj)
        qty_comp = entry_no_comps
        temp_list.append(
            {'number': batch_num, 
            'quantity_comp': qty_comp,
            'location': new_batch._location,
            'manufacture_date': manufacture_date,
            'component': sn_comps
            })
        inventory["Batch"] = temp_list
        a_dict["Batch"] = inventory["Batch"]
        self.save_data(a_dict)
        # Clear the entry one the file is created to set with empty string
        self.entry_batch_no.set('')
        self.entry_components.set('')

    # Method that close Application
    def close_app(self):
        # Below line is just for testing if everything work
        msgbox_exit = messagebox.askyesno(
            'Exit Program', 'Are you sure want to EXIT!', icon='warning')
        if msgbox_exit:
            # Below line is just for testing if everything work
            print('Close App method Called')
            self.quit()
        else:
            # Below line is just for testing if everything work
            print('Return to menu')


# ====================
# Start GUI
# ====================
if __name__ == "__main__":
    _frame = tk.Tk()
    app = App(_frame)
    app.mainloop()
