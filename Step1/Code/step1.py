import os
import json
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
        self.master.geometry('700x600')
        # Add a tittle on window
        self.master.title("PPEC - Inventory System")

        # Create instance for menu frame, this is the Menu Frame in the Main Window
        self._menu_frame = ttk.LabelFrame(
            self.master, text=' Menu ', style="Blue.TLabelframe")
        # Create instance for menu frame, this is the New Batch Frame in the Main Window
        self._create_batch_frame = ttk.LabelFrame(
            self.master, text=' Create New Batch ', style="Blue.TLabelframe")
        self._show_details_frame = ttk.LabelFrame(
            self.master, text=' Batch Details', style="Blue.TLabelframe")
        
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

        # Create a Tkinter variable
        self.tk_var = StringVar(self)  # Dropdown
        self.entry_batch_no = StringVar(self)  # input
        self.entry_components = StringVar(self)  # Input
        self.entry_type_comp = StringVar(self)  # Dropdown
        self.entry_size_fitment = StringVar(self)  # Dropdown

        # Call methods
        self.create_menu()
        self.create_json_file()

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
    
    # this method manage the choice you make on the dropdown options menu, display in the frame below the menu the choice you made
    def change_dropdown(self, *args):
        option = self.tk_var.get()
        if option == '1':
            # Call methods
            self.create_new_batch()
        else:
            self.close_app()

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
    def check_batch_exist(self):
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
            val = int(value) # check if the params is numeric
            return True # if so return True
        except (TypeError, ValueError): # if the params is not numeric the exception is a TypeError or ValueError
            return False # return False

    # This method create a menu with a dropdown to choice options
    def create_menu(self):
        # Create a container to hold all label for menu
        self._menu_frame.grid(column=0, row=8, padx=10,
                              pady=10, ipadx=40, sticky=tk.W)

        # Dictionary with options
        choices = {'2', '1'}
        # set the default label in the dropdown option
        self.tk_var.set('Options')

        # Create the Dropdown Menu Option
        OptionMenu(self._menu_frame, self.tk_var, *sorted(choices)).grid(column=1, row=2, ipadx=5)

        # Place labels into the container element menu_frame
        ttk.Label(self._menu_frame, text="1. Create a New Batch").grid(
            column=0, row=0, sticky=tk.W)
        ttk.Label(self._menu_frame, text="2. Quit").grid(
            column=0, row=1, sticky=tk.W)
        ttk.Label(self._menu_frame, text="Choose the option:").grid(
            column=0, row=2, ipady=10, sticky=tk.W)

        # link function to change dropdown
        self.tk_var.trace('w', self.change_dropdown)

        for child in self._menu_frame.winfo_children():
            child.grid_configure(padx=10, pady=4)

    # This method create a frame with all input to create a new batch
    def create_new_batch(self):
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
        ttk.Button(self._create_batch_frame, text="Create Batch", command=self.check_batch_exist).grid(
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
            self.save_batch_to_json_file()

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
        self._show_details_frame.grid(
            column=0, row=10, padx=10, pady=10, ipadx=40, sticky=(tk.N, tk.W, tk.E, tk.S))
        # Place labels into the container element create new batch
        ttk.Label(self._show_details_frame, text="Batch number:\t{}".format(batch_num)).grid(column=0, row=0, padx=10, pady=10,
                                                                                             sticky=tk.W)
        ttk.Label(self._show_details_frame, text="Manufacture Date:\t{}".format(date_manufacture)).grid(column=0, row=1, padx=10, pady=10,
                                                                                                        sticky=tk.W)
        ttk.Label(self._show_details_frame, text="Component type:\t{}".format(entry_type_comps)).grid(column=0, row=2, padx=10, pady=10,
                                                                                                      sticky=tk.W)
        ttk.Label(self._show_details_frame, text="Component Size/Fitment type: {}".format(entry_size_fit)).grid(column=0, row=3, padx=10,
                                                                                                                pady=10, sticky=tk.W)
        ttk.Label(self._show_details_frame, text="SerialNumbers: {}".format(sn)).grid(column=0, row=4, padx=10,
                                                                                            pady=10, sticky=tk.W)
        ttk.Label(self._show_details_frame, text="Component Status:[\n\t{}\n\t]".format(comps)).grid(column=0, row=5, padx=10,
                                                                                                                     pady=10, sticky=tk.W)
        ttk.Label(self._show_details_frame, text="Component Location: {}".format(comp_location)).grid(column=0, row=6, padx=10,
                                                                                                                     pady=10, sticky=tk.W)

    """ The method save_batch_to_json_file() is called when you click "yes" on the message box that appear 
        when click "Create batch" button and save all data in BatchIndex.json file.
    """
    def save_batch_to_json_file(self):
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
        data = self.create_json_file()
        temp_list = []
        for dic_obj in data["Batch"]:
            temp_list.append(dic_obj)
        qty_comp = entry_no_comps
        temp_list.append(
            {'number': batch_num, 
            'quantity_comp': qty_comp,
            'location': new_batch._location,
            'manufacture_date': manufacture_date,
            'component': sn_comps
            })
        data["Batch"] = temp_list
        a_dict["Batch"] = data["Batch"]
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
