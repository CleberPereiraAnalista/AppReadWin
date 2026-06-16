from computer_info import ComputerInfo
from encryption_tool import EncryptionTool
from tkcalendar import DateEntry
from tkinter import font
from tkinter import ttk
import os
import platform
import psutil
import winreg
import datetime
import json
import sys
import tkinter as tk
import tkinter.filedialog as fdlg
import tkinter.messagebox as tkmsg



class my_App:

	def __init__(self, **kw):
		self.root = tk.Tk()
		self.root.title("AppReadWin - Leitor de informações sobre computador com Sistema Operacional Microsoft\u2122 Windows\u2122")
		#self.root.title("Leitor de informações sobre computador com Sistema Operacional Microsoft\u00AE Windows\u00AE")
		self.root.geometry('%dx%d+%d+%d'%(908,600,0,0))
		self.root.resizable(width=False, height=False)

		encrypt_key = b'4KMn4L_Pd7ycmJ7WVmxKoIQ2WjPAEYNqKw-Kw8LzCW4='
		self.encrypt_tool = EncryptionTool(encrypt_key.strip())

		self.create_initial_area()
		self.read_initial_data()


	def execute(self):
		self.root.mainloop()

	def end_app(self):
		self.root.quit()

	def create_initial_area(self):
		style = ttk.Style()
		style.configure("LIGHTGREY.TFrame", background='light grey')

		title_frame_size = 9
		label_font_size = 8
		label_item_size = 7
		label_msg_size = 7

		self.mainframe = ttk.Frame(master=self.root, style="LIGHTGREY.TFrame")
		self.mainframe.grid(row=1, column=0, sticky='ns', padx=0, pady=0)

		# Container 1 -----------------------------------------------------------------------------------
		self.frm_1 = tk.LabelFrame(
			self.mainframe, 
			text="Identificação",
			background='light grey',
			labelanchor='nw',
			relief="groove",
			font=tk.font.Font(size=title_frame_size, weight='bold')
		)
		self.frm_1.grid(row=0, column=0, sticky='nw', padx=5, pady=(5,2))
		
		## Data (Atual)
		self.input_date = DateEntry(
			self.frm_1,
			width=12,
			background='darkblue',
			foreground="white",
			borderwidth=2,
			date_pattern='yyyy-mm-dd'
		)
		self.input_date.grid(row=0, column=0, sticky='w', padx=5, pady=(5,0))

		msg_info_name = "Obrigatório preencher o nome completo."
		self.label_key_msg_name = tk.Label(self.frm_1, text=msg_info_name, bg='light grey', fg='red', font=tk.font.Font(size=label_msg_size, weight='bold'))
		self.label_key_msg_name.grid(row=0, column=1, sticky='e', padx=5, pady=(5,0))

		## Nome do Usuário (Responsável pelo Computador)
		self.label_username = tk.Label(self.frm_1, text="Nome do Colaborador:", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))
		self.label_username.grid(row=2, column=0, sticky='e', padx=5, pady=(0,5))
		self.input_username = tk.Entry(self.frm_1, width=50, background='white')
		self.input_username.grid(row=2, column=1, stick='we', padx=5, pady=(0,5), ipady=1)

		## Coordenação
		self.label_coord = tk.Label(self.frm_1, text="Coordenação/Departamento:", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))
		self.label_coord.grid(row=3, column=0, sticky='e', padx=5, pady=(0,5))
		self.input_coord = tk.Entry(self.frm_1, width=50, background='white')
		self.input_coord.grid(row=3, column=1, stick='we', padx=5, pady=(0,5), ipady=1)

		## Setor
		self.label_sector = tk.Label(self.frm_1, text="Setor:", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))
		self.label_sector.grid(row=4, column=0, sticky='e', padx=5, pady=(0,5))
		self.input_sector = tk.Entry(self.frm_1, width=50, background='white')
		self.input_sector.grid(row=4, column=1, stick='we', padx=5, pady=(0,5), ipady=1)

		
		# Container 2 -----------------------------------------------------------------------------------
		# Gabinete 
		self.frm_2 = tk.LabelFrame(
			self.mainframe,
			text="Computador Desktop (Gabinete) ou Notebook",
			background="light grey",
			labelanchor='nw',
			relief="groove",
			font=tk.font.Font(size=title_frame_size, weight='bold')
		)
		self.frm_2.grid(row=1, column=0, sticky='nw', padx=5, pady=(2,5))

		## Tipo (desktop ou notebook)
		self.var_device_type = tk.StringVar(value='desktop')
		self.label_device_type = tk.Label(self.frm_2, text="Tipo:", bg="light grey", font=tk.font.Font(size=label_font_size, weight='bold'))
		self.label_device_type.grid(row=0, column=0,  stick='e', padx=5, pady=0)
		rb_device_type_1 = tk.Radiobutton(self.frm_2, text="Desktop",  variable=self.var_device_type, value="desktop", bg='light grey', font=tk.font.Font(size=label_item_size))
		rb_device_type_1.grid(row=0, column=1, sticky='w', padx=(5,0), pady=2)
		rb_device_type_2 = tk.Radiobutton(self.frm_2, text="Notebook",  variable=self.var_device_type, value="notebook", bg='light grey', font=tk.font.Font(size=label_item_size))
		rb_device_type_2.grid(row=0, column=2, sticky='w', padx=(0,5), pady=2)

		## Nº do Patrimônio (targeta ou placa)
		self.label_assets_code = tk.Label(self.frm_2, text="Nº do Registro (Patrimônio):", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))
		self.label_assets_code.grid(row=1, column=0, stick='e', padx=5, pady=(5,0))
		self.input_assets_code = tk.Entry(self.frm_2, width=35, background='white', justify="center")
		self.input_assets_code.grid(row=1, column=1, columnspan=2, stick='we', padx=5, pady=(5,0), ipady=1)

		## Código Local - CTEC (ex: CAA000)
		self.label_local_code = tk.Label(self.frm_2, text="Código Local:", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))
		self.label_local_code.grid(row=2, column=0, stick='e', padx=5, pady=(0,5))
		self.input_local_code = tk.Entry(self.frm_2, width=35, background='white', justify="center")
		self.input_local_code.grid(row=2, column=1, columnspan=2, stick='we', padx=5, pady=(0,5), ipady=1)

		msg_info_device = "Obrigatório preencher um dos campos acima."
		self.label_key_msg_device = tk.Label(self.frm_2, text=msg_info_device, bg='light grey', fg='red', font=tk.font.Font(size=label_msg_size, weight='bold'))
		self.label_key_msg_device.grid(row=3, column=1, columnspan=2, sticky='e', padx=5, pady=(0,0))

		

		
		# Container 3 -----------------------------------------------------------------------------------
		## Teclado
		self.frm_3 = tk.LabelFrame(
			self.mainframe,
			text="Teclado",
			background="light grey",
			labelanchor='nw',
			relief="groove",
			font=tk.font.Font(size=title_frame_size, weight='bold')
		)
		self.frm_3.grid(row=0, column=1, sticky='nw', padx=5, pady=5)

		### Nº de Identificação (targeta ou placa)
		self.label_key_number = tk.Label(self.frm_3, text="Nº de Identificação:", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))
		self.label_key_number.grid(row=0, column=0, stick='e', padx=5, pady=2)
		self.input_key_number = tk.Entry(self.frm_3, width=30, background='white', justify="center")
		self.input_key_number.grid(row=0, column=1, columnspan=2, stick='we', padx=5, pady=2, ipady=1)

		### conectividade (com fio ou sem fio)
		self.var_key_connectivity = tk.StringVar(value='com fio')
		self.label_key_connectivity = tk.Label(self.frm_3, text="Conectividade:", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))
		self.label_key_connectivity.grid(row=1, column=0, sticky='e', padx=5, pady=0)
		rb_key_connectivity_1 = tk.Radiobutton(self.frm_3, text="Com Fio", variable=self.var_key_connectivity, value="com fio", bg='light grey', font=tk.font.Font(size=label_item_size))
		rb_key_connectivity_1.grid(row=1, column=1, sticky='w', padx=(5,0), pady=2)
		rb_key_connectivity_2 = tk.Radiobutton(self.frm_3, text="Sem Fio", variable=self.var_key_connectivity, value="sem fio", bg='light grey', font=tk.font.Font(size=label_item_size))
		rb_key_connectivity_2.grid(row=1, column=2, sticky='w', padx=(0,5), pady=2)
		
		### Propriedade (Público ou Particular)
		self.var_key_property = tk.StringVar(value='pública')
		self.label_key_property = tk.Label(self.frm_3, text="Propriedade:", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))
		self.label_key_property.grid(row=2, column=0, sticky='e', padx=5, pady=5)
		rb_key_property_1 = tk.Radiobutton(self.frm_3, text="Pública", variable=self.var_key_property, value="pública", bg='light grey', font=tk.font.Font(size=label_item_size))
		rb_key_property_1.grid(row=2, column=1, sticky='w', padx=(5,0), pady=2)
		rb_key_property_2 = tk.Radiobutton(self.frm_3, text="Particular", variable=self.var_key_property, value="particular", bg='light grey', font=tk.font.Font(size=label_item_size))
		rb_key_property_2.grid(row=2, column=2, sticky='w', padx=(0,5), pady=2)
		msg_info_key = "Marque a opção 'Particular' somente se o teclado pertencer ao servidor."
		self.label_key_msg_info = tk.Label(self.frm_3, text=msg_info_key, bg='light grey', fg='blue', font=tk.font.Font(size=label_msg_size, weight='bold'))
		self.label_key_msg_info.grid(row=3,column=0, columnspan=3, sticky='e', padx=5, pady=(0,5))

		
		# Container 4 -----------------------------------------------------------------------------------
		# Mouse
		## Nº de Identificação (targeta ou placa)
		## conectividade (com fio ou sem fio)
		## Propriedade (Público ou Particular) 
		self.frm_4 = tk.LabelFrame(
			self.mainframe,
			text="Mouse",
			background="light grey",
			labelanchor='nw',
			relief="groove",
			font=tk.font.Font(size=title_frame_size, weight='bold')
		)
		self.frm_4.grid(row=1, column=1, sticky='nw', padx=5, pady=5)

		### Nº de Identificação (targeta ou placa)
		self.label_mouse_number = tk.Label(self.frm_4, text="Nº de Identificação:", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))
		self.label_mouse_number.grid(row=0, column=0, stick='e', padx=5, pady=(5,0))
		self.input_mouse_number = tk.Entry(self.frm_4, width=30, background='white', justify="center")
		self.input_mouse_number.grid(row=0, column=1, columnspan=2, stick='we', padx=5, pady=(5,0), ipady=1)

		### conectividade (com fio ou sem fio)
		self.var_mouse_connectivity = tk.StringVar(value='com fio')
		self.label_mouse_connectivity = tk.Label(self.frm_4, text="Conectividade:", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))
		self.label_mouse_connectivity.grid(row=1, column=0, sticky='e', padx=5, pady=0)
		rb_mouse_connectivity_1 = tk.Radiobutton(self.frm_4, text="Com Fio", variable=self.var_mouse_connectivity, value="com fio", bg='light grey', font=tk.font.Font(size=label_item_size))
		rb_mouse_connectivity_1.grid(row=1, column=1, sticky='w', padx=(5,0), pady=0)
		rb_mouse_connectivity_2 = tk.Radiobutton(self.frm_4, text="Sem Fio", variable=self.var_mouse_connectivity, value="sem fio", bg='light grey', font=tk.font.Font(size=label_item_size))
		rb_mouse_connectivity_2.grid(row=1, column=2, sticky='w', padx=(0,5), pady=0)
		
		### Propriedade (Público ou Particular)
		self.var_mouse_property = tk.StringVar(value='pública')
		self.label_mouse_property = tk.Label(self.frm_4, text="Propriedade:", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))
		self.label_mouse_property.grid(row=2, column=0, sticky='e', padx=5, pady=0)
		rb_mouse_property_1 = tk.Radiobutton(self.frm_4, text="Pública", variable=self.var_mouse_property, value="pública", bg='light grey', font=tk.font.Font(size=label_item_size))
		rb_mouse_property_1.grid(row=2, column=1, sticky='w', padx=(5,0), pady=0)
		rb_mouse_property_2 = tk.Radiobutton(self.frm_4, text="Particular", variable=self.var_mouse_property, value="particular", bg='light grey', font=tk.font.Font(size=label_item_size))
		rb_mouse_property_2.grid(row=2, column=2, sticky='w', padx=(0,5), pady=0)
		msg_info_mouse = "Marque a opção 'Particular' somente se o mouse pertencer ao servidor."
		self.label_mouse_msg_info = tk.Label(self.frm_4, text=msg_info_mouse, bg='light grey', fg='blue', font=tk.font.Font(size=label_msg_size, weight='bold'))
		self.label_mouse_msg_info.grid(row=3,column=0, columnspan=3, sticky='e', padx=5, pady=(0,5))

	
		
		# Container 5 -----------------------------------------------------------------------------------
		self.frm_5 = tk.LabelFrame(
			self.mainframe,
			text="Monitores",
			background="light grey",
			labelanchor='nw',
			relief="groove",
			font=tk.font.Font(size=title_frame_size, weight='bold')
		)
		self.frm_5.grid(row=2, column=0, columnspan=2, sticky='nw', padx=5, pady=5)
		# Monitores
		## Propriedade (Público ou Particular) 
		## Modelo
		## Polegadas
		## Marca
		## Nº do Patrimônio

		monitor_title_1 = tk.Label(self.frm_5, text="Modelo", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'), justify='center')
		monitor_title_2 = tk.Label(self.frm_5, text="Polegadas", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'), justify='center')
		monitor_title_3 = tk.Label(self.frm_5, text="Marca", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'), justify='center')
		monitor_title_4 = tk.Label(self.frm_5, text="Nº do Patrimônio", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'), justify='center')
		monitor_title_5 = tk.Label(self.frm_5, text="Propriedade", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'), justify='center')
		monitor_title_6 = tk.Label(self.frm_5, text="Altura", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'), justify='center')
		monitor_title_7 = tk.Label(self.frm_5, text="Modo", bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'), justify='center')

		monitor_title_1.grid(row=0, column=1, sticky='we', padx=5, pady=5)
		monitor_title_2.grid(row=0, column=2, sticky='we', padx=5, pady=5)
		monitor_title_3.grid(row=0, column=3, sticky='we', padx=5, pady=5)
		monitor_title_4.grid(row=0, column=4, sticky='we', padx=5, pady=5)
		monitor_title_5.grid(row=0, column=5, columnspan=2, sticky='we', padx=5, pady=5)
		monitor_title_6.grid(row=0, column=7, sticky='we', padx=5, pady=5)
		monitor_title_7.grid(row=0, column=8, sticky='we', padx=5, pady=5)

		
		# identificador da linha
		monitor_1_label = tk.Label(self.frm_5, text="1:", width=5, bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))
		monitor_2_label = tk.Label(self.frm_5, text="2:", width=5, bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))
		monitor_3_label = tk.Label(self.frm_5, text="3:", width=5, bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))
		monitor_4_label = tk.Label(self.frm_5, text="4:", width=5, bg='light grey', font=tk.font.Font(size=label_font_size, weight='bold'))

		monitor_1_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
		monitor_2_label.grid(row=2, column=0, sticky='e', padx=5, pady=5)
		monitor_3_label.grid(row=3, column=0, sticky='e', padx=5, pady=5)
		monitor_4_label.grid(row=4, column=0, sticky='e', padx=5, pady=5)

		
		# Monitor 1
		self.input_monitor_1_model = tk.Entry(self.frm_5, width=20, background='white', justify="center")
		self.input_monitor_1_inches = tk.Entry(self.frm_5, width=10, background='white', justify="center")
		self.input_monitor_1_brand = tk.Entry(self.frm_5, width=20, background='white', justify="center")
		self.input_monitor_1_assets_code = tk.Entry(self.frm_5, width=20, background='white', justify="center")
		self.var_monitor_1_property = tk.StringVar(value='pública')
		self.rb_monitor_1_property_A = tk.Radiobutton(self.frm_5, text="Pública", variable=self.var_monitor_1_property, value="pública", bg='light grey', font=tk.font.Font(size=label_item_size))
		self.rb_monitor_1_property_B = tk.Radiobutton(self.frm_5, text="Particular", variable=self.var_monitor_1_property, value="particular", bg='light grey', font=tk.font.Font(size=label_item_size))
		self.var_monitor_1_ajustable = tk.StringVar(value='0')
		self.check_btn_monitor_1_ajustable = tk.Checkbutton(self.frm_5, text="Ajustável", variable=self.var_monitor_1_ajustable, onvalue="1", offvalue="0", bg='light grey', font=tk.font.Font(size=label_item_size))
		self.var_monitor_1_portrait_mode = tk.StringVar(value='0') # Modo Retrato
		self.check_btn_monitor_1_portrait_mode = tk.Checkbutton(self.frm_5, text="Retrato", variable=self.var_monitor_1_portrait_mode, onvalue="1", offvalue="0", bg='light grey', font=tk.font.Font(size=label_item_size))
		
		self.input_monitor_1_model.grid(row=1, column=1, sticky='w', padx=5, pady=5, ipady=1)
		self.input_monitor_1_inches.grid(row=1, column=2, sticky='w', padx=5, pady=5, ipady=1)
		self.input_monitor_1_brand.grid(row=1, column=3, sticky='w', padx=5, pady=5, ipady=1)
		self.input_monitor_1_assets_code.grid(row=1, column=4, sticky='w', padx=5, pady=5, ipady=1)
		self.rb_monitor_1_property_A.grid(row=1, column=5, sticky='w', padx=(5,0), pady=5)
		self.rb_monitor_1_property_B.grid(row=1, column=6, sticky='w', padx=(0,5), pady=5)
		self.check_btn_monitor_1_ajustable.grid(row=1, column=7, sticky='w', padx=(5,0), pady=5)
		self.check_btn_monitor_1_portrait_mode.grid(row=1, column=8, sticky='w', padx=(0,5), pady=5)
		

		# Monitor 2
		self.input_monitor_2_model = tk.Entry(self.frm_5, width=20, background='white', justify="center")
		self.input_monitor_2_inches = tk.Entry(self.frm_5, width=10, background='white', justify="center")
		self.input_monitor_2_brand = tk.Entry(self.frm_5, width=20, background='white', justify="center")
		self.input_monitor_2_assets_code = tk.Entry(self.frm_5, width=20, background='white', justify="center")
		self.var_monitor_2_property = tk.StringVar(value='pública')
		self.rb_monitor_2_property_A = tk.Radiobutton(self.frm_5, text="Pública", variable=self.var_monitor_2_property, value="pública", bg='light grey', font=tk.font.Font(size=label_item_size))
		self.rb_monitor_2_property_B = tk.Radiobutton(self.frm_5, text="Particular", variable=self.var_monitor_2_property, value="particular", bg='light grey', font=tk.font.Font(size=label_item_size))
		self.var_monitor_2_ajustable = tk.StringVar(value='0')
		self.check_btn_monitor_2_ajustable = tk.Checkbutton(self.frm_5, text="Ajustável", variable=self.var_monitor_2_ajustable, onvalue="1", offvalue="0", bg='light grey', font=tk.font.Font(size=label_item_size))
		self.var_monitor_2_portrait_mode = tk.StringVar(value='0') # Modo Retrato
		self.check_btn_monitor_2_portrait_mode = tk.Checkbutton(self.frm_5, text="Retrato", variable=self.var_monitor_2_portrait_mode, onvalue="1", offvalue="0", bg='light grey', font=tk.font.Font(size=label_item_size))

		self.input_monitor_2_model.grid(row=2, column=1, sticky='w', padx=5, pady=5, ipady=1)
		self.input_monitor_2_inches.grid(row=2, column=2, sticky='w', padx=5, pady=5, ipady=1)
		self.input_monitor_2_brand.grid(row=2, column=3, sticky='w', padx=5, pady=5, ipady=1)
		self.input_monitor_2_assets_code.grid(row=2, column=4, sticky='w', padx=5, pady=5, ipady=1)
		self.rb_monitor_2_property_A.grid(row=2, column=5, sticky='w', padx=(5,0), pady=5)
		self.rb_monitor_2_property_B.grid(row=2, column=6, sticky='w', padx=(0,5), pady=5, ipady=1)
		self.check_btn_monitor_2_ajustable.grid(row=2, column=7, sticky='w', padx=(5,0), pady=5)
		self.check_btn_monitor_2_portrait_mode.grid(row=2, column=8, sticky='w', padx=(0,5), pady=5)
		

		# Monitor 3
		self.input_monitor_3_model = tk.Entry(self.frm_5, width=20, background='white', justify="center")
		self.input_monitor_3_inches = tk.Entry(self.frm_5, width=10, background='white', justify="center")
		self.input_monitor_3_brand = tk.Entry(self.frm_5, width=20, background='white', justify="center")
		self.input_monitor_3_assets_code = tk.Entry(self.frm_5, width=20, background='white', justify="center")
		self.var_monitor_3_property = tk.StringVar(value='pública')
		self.rb_monitor_3_property_A = tk.Radiobutton(self.frm_5, text="Pública", variable=self.var_monitor_3_property, value="pública", bg='light grey', font=tk.font.Font(size=label_item_size))
		self.rb_monitor_3_property_B = tk.Radiobutton(self.frm_5, text="Particular", variable=self.var_monitor_3_property, value="particular", bg='light grey', font=tk.font.Font(size=label_item_size))
		self.var_monitor_3_ajustable = tk.StringVar(value='0')
		self.check_btn_monitor_3_ajustable = tk.Checkbutton(self.frm_5, text="Ajustável", variable=self.var_monitor_3_ajustable, onvalue="1", offvalue="0", bg='light grey', font=tk.font.Font(size=label_item_size))
		self.var_monitor_3_portrait_mode = tk.StringVar(value='0') # Modo Retrato
		self.check_btn_monitor_3_portrait_mode = tk.Checkbutton(self.frm_5, text="Retrato", variable=self.var_monitor_3_portrait_mode, onvalue="1", offvalue="0", bg='light grey', font=tk.font.Font(size=label_item_size))
		
		self.input_monitor_3_model.grid(row=3, column=1, sticky='w', padx=5, pady=5, ipady=1)
		self.input_monitor_3_inches.grid(row=3, column=2, sticky='w', padx=5, pady=5, ipady=1)
		self.input_monitor_3_brand.grid(row=3, column=3, sticky='w', padx=5, pady=5, ipady=1)
		self.input_monitor_3_assets_code.grid(row=3, column=4, sticky='w', padx=5, pady=5, ipady=1)
		self.rb_monitor_3_property_A.grid(row=3, column=5, sticky='w', padx=(5,0), pady=5)
		self.rb_monitor_3_property_B.grid(row=3, column=6, sticky='w', padx=(0,5), pady=5)
		self.check_btn_monitor_3_ajustable.grid(row=3, column=7, sticky='w', padx=(5,0), pady=5)
		self.check_btn_monitor_3_portrait_mode.grid(row=3, column=8, sticky='w', padx=(0,5), pady=5)
		

		self.input_monitor_4_model = tk.Entry(self.frm_5, width=20, background='white', justify="center")
		self.input_monitor_4_inches = tk.Entry(self.frm_5, width=10, background='white', justify="center")
		self.input_monitor_4_brand = tk.Entry(self.frm_5, width=20, background='white', justify="center")
		self.input_monitor_4_assets_code = tk.Entry(self.frm_5, width=20, background='white', justify="center")
		self.var_monitor_4_property = tk.StringVar(value='pública')
		self.rb_monitor_4_property_A = tk.Radiobutton(self.frm_5, text="Pública", variable=self.var_monitor_4_property, value="pública", bg='light grey', font=tk.font.Font(size=label_item_size))
		self.rb_monitor_4_property_B = tk.Radiobutton(self.frm_5, text="Particular", variable=self.var_monitor_4_property, value="particular", bg='light grey', font=tk.font.Font(size=label_item_size))
		self.var_monitor_4_ajustable = tk.StringVar(value='0')
		self.check_btn_monitor_4_ajustable = tk.Checkbutton(self.frm_5, text="Ajustável", variable=self.var_monitor_4_ajustable, onvalue="1", offvalue="0", bg='light grey', font=tk.font.Font(size=label_item_size))
		self.var_monitor_4_portrait_mode = tk.StringVar(value='0') # Modo Retrato
		self.check_btn_monitor_4_portrait_mode = tk.Checkbutton(self.frm_5, text="Retrato", variable=self.var_monitor_4_portrait_mode, onvalue="1", offvalue="0", bg='light grey', font=tk.font.Font(size=label_item_size))

		self.input_monitor_4_model.grid(row=4, column=1, sticky='w', padx=5, pady=5, ipady=1)
		self.input_monitor_4_inches.grid(row=4, column=2, sticky='w', padx=5, pady=5, ipady=1)
		self.input_monitor_4_brand.grid(row=4, column=3, sticky='w', padx=5, pady=5, ipady=1)
		self.input_monitor_4_assets_code.grid(row=4, column=4, sticky='w', padx=5, pady=5, ipady=1)
		self.rb_monitor_4_property_A.grid(row=4, column=5, sticky='w', padx=(5,0), pady=5)
		self.rb_monitor_4_property_B.grid(row=4, column=6, sticky='w', padx=(0,5), pady=5)
		self.check_btn_monitor_4_ajustable.grid(row=4, column=7, sticky='w', padx=(5,0), pady=5)
		self.check_btn_monitor_4_portrait_mode.grid(row=4, column=8, sticky='w', padx=(0,5), pady=5)
		

		msg_info_monitor = "1. Marque a opção 'Particular' somente se o monitor tiver sido adquirido pelo servidor."
		msg_info_monitor += "\n2. Se o seu monitor possui ajuste de inclinação, altura ou giro marque a opção 'Ajustável'."
		msg_info_monitor += "\n3. Se o seu monitor é ajustável e possui opção de giro para leitura modo retrato (Vertical) marque a opção 'Retrato'."
		msg_info_monitor += "\n4. Se estiver utilizando notebook, preencha apenas se estiver utilizando monitor secundário não vinculado a outra estação de trabalho."
		self.label_monitor_msg_info = tk.Label(self.frm_5, text=msg_info_monitor, bg='light grey', fg='blue', font=tk.font.Font(size=label_msg_size, weight='bold'), justify="left")
		self.label_monitor_msg_info.grid(row=10, column=1, columnspan=5, sticky='w', padx=5, pady=(0,5))


		# Final -----------------------------------------------------------------------------------------
		final_row_init = 21

		self.btn_export_file = tk.Button(
			self.mainframe,
			text="Exportar Dados",
			font=tk.font.Font(size=12, weight='bold'),
			background='#1a1aff',
			foreground='#dddddd',
			command=self.export_file
		)
		self.btn_export_file.grid(row=final_row_init, columnspan=10, sticky='we', padx=5, pady=10)

		

		# Container Footer ------------------------------------------------------------------------------
		sep = tk.ttk.Separator(self.mainframe, orient='horizontal')
		sep.grid(row=final_row_init+1, column=0, columnspan=10, stick='we', padx=5, pady=(15,5))

		created_by = tk.Label(self.mainframe, text="Criado por Cleber Almeida Pereira", font=tk.font.Font(size=7), bg='light grey')
		created_by.grid(row=final_row_init+2, column=0, columnspan=10, padx=5, pady=(1,0), stick='we')
		contact = tk.Label(self.mainframe, text="contato: (67) 99607-6081", font=tk.font.Font(size=7), bg='light grey')
		contact.grid(row=final_row_init+3, column=0, columnspan=10, padx=5, pady=(0,5), stick='we')
		# Container Footer ---------------------------------------------------------------------- FIM ---



	def read_initial_data(self):
		
		file_path = os.path.join(os.getcwd(),'user_info.txt')
		if os.path.exists(file_path):
			with open(file_path, 'rb') as file:
				data = file.read()

			if len(data) > 0:

				# Descriptografar e converter de volta para dicionário
				#decrypted_data = fernet.decrypt(data).decode('utf-8')
				decrypted_data = self.encrypt_tool.decrypt(data)
				data_dict = json.loads(decrypted_data)

				if data_dict['username']: self.input_username.insert(0, data_dict['username'])
				if data_dict['coord']: self.input_coord.insert(0, data_dict['coord'])
				if data_dict['sector']: self.input_sector.insert(0, data_dict['sector'])
				if data_dict['computer']['local_code']: self.input_local_code.insert(0, data_dict['computer']['local_code'])
				if data_dict['computer']['assets_code']: self.input_assets_code.insert(0, data_dict['computer']['assets_code'])
				if data_dict['computer']['device_type']: self.var_device_type.set(data_dict['computer']['device_type'])

				# Teclado
				if data_dict['peripherals']['keyboard']['number']: self.input_key_number.insert(0, data_dict['peripherals']['keyboard']['number'])
				if data_dict['peripherals']['keyboard']['conectivity']: self.var_key_connectivity.set(data_dict['peripherals']['keyboard']['conectivity'])
				if data_dict['peripherals']['keyboard']['property']: self.var_key_property.set(data_dict['peripherals']['keyboard']['property'])

				# mouse
				if data_dict['peripherals']['mouse']['number']: self.input_mouse_number.insert(0, data_dict['peripherals']['mouse']['number'])
				if data_dict['peripherals']['mouse']['conectivity']: self.var_mouse_connectivity.set(data_dict['peripherals']['mouse']['conectivity'])
				if data_dict['peripherals']['mouse']['property']: self.var_mouse_property.set(data_dict['peripherals']['mouse']['property'])

				# monitores
				if len(data_dict['peripherals']['monitor'].keys()) > 0:
					
					entries_monitors = {
						'1':{
							'model':self.input_monitor_1_model,
							'inches':self.input_monitor_1_inches,
							'brand':self.input_monitor_1_brand,
							'assets_code':self.input_monitor_1_assets_code,
							'property':self.var_monitor_1_property,
							'ajustable':self.var_monitor_1_ajustable,
							'portrait_mode':self.var_monitor_1_portrait_mode,
						},
						'2':{
							'model':self.input_monitor_2_model,
							'inches':self.input_monitor_2_inches,
							'brand':self.input_monitor_2_brand,
							'assets_code':self.input_monitor_2_assets_code,
							'property':self.var_monitor_2_property,
							'ajustable':self.var_monitor_2_ajustable,
							'portrait_mode':self.var_monitor_2_portrait_mode,
						},
						'3':{
							'model':self.input_monitor_3_model,
							'inches':self.input_monitor_3_inches,
							'brand':self.input_monitor_3_brand,
							'assets_code':self.input_monitor_3_assets_code,
							'property':self.var_monitor_3_property,
							'ajustable':self.var_monitor_3_ajustable,
							'portrait_mode':self.var_monitor_3_portrait_mode,
						},
						'4':{
							'model':self.input_monitor_4_model,
							'inches':self.input_monitor_4_inches,
							'brand':self.input_monitor_4_brand,
							'assets_code':self.input_monitor_4_assets_code,
							'property':self.var_monitor_4_property,
							'ajustable':self.var_monitor_4_ajustable,
							'portrait_mode':self.var_monitor_4_portrait_mode,
						},
					}

					for monitor_id, monitor in data_dict['peripherals']['monitor'].items():
						entries_monitors[monitor_id]['model'].delete(0, 'end')
						entries_monitors[monitor_id]['inches'].delete(0, 'end')
						entries_monitors[monitor_id]['brand'].delete(0, 'end')
						entries_monitors[monitor_id]['assets_code'].delete(0, 'end')

						entries_monitors[monitor_id]['model'].insert(0, monitor['model'])
						entries_monitors[monitor_id]['inches'].insert(0, monitor['inches'])
						entries_monitors[monitor_id]['brand'].insert(0, monitor['brand'])
						entries_monitors[monitor_id]['assets_code'].insert(0, monitor['assets_code'])
						entries_monitors[monitor_id]['property'].set(monitor['property'])
						entries_monitors[monitor_id]['ajustable'].set(monitor['ajustable'])
						entries_monitors[monitor_id]['portrait_mode'].set(monitor['portrait_mode'])

		else:
			file = open(file_path, 'w')
			file.close()


	def export_file(self):
		run_export_file = True

		# Obtem dados informados
		selected_date = self.input_date.get_date()
		username = self.input_username.get().strip()
		local_code = self.input_local_code.get().strip() # Código Local
		assets_code = self.input_assets_code.get().strip()  # Código do Patrimônio
		
		if len(username) == 0  or len(username.split(' ')) < 2:
			run_export_file = False
			tkmsg.showerror("Faltando Informação!", "O campo 'Nome' deve ser preenchido com o nome completo do responsável pelo computador.")
		elif len(local_code) == 0 and len(assets_code) == 0 :
			run_export_file = False
			tkmsg.showerror("Faltando Informação!", "Pelo menos um dos campos 'Código Local' ou 'Nº do Patrimônio' deve estar preenchido.")

		if run_export_file:
			selected_local = fdlg.askdirectory()

			# capitalize username
			user_name_capitalized = []
			for name in username.split(' '):
				if name in ['de', 'da', 'di', 'e']:
					user_name_capitalized.append(name)
				else:
					user_name_capitalized.append(name.capitalize())
			username = " ".join(user_name_capitalized)

			coord = self.input_coord.get().strip().upper() if len(self.input_coord.get()) > 0 else "Não informado"
			sector = self.input_sector.get().strip().upper() if len(self.input_sector.get().strip()) > 0 else "Não informado"
			selected_device_type = self.var_device_type.get()
			
			key_number = self.input_key_number.get().strip() if len(self.input_key_number.get().strip()) > 0 else "Não informado"
			selected_key_connectivity = self.var_key_connectivity.get()
			selected_key_property = self.var_key_property.get()
			
			mouse_number = self.input_mouse_number.get().strip() if len(self.input_mouse_number.get().strip()) > 0 else "Não informado"
			selected_mouse_connectivity = self.var_mouse_connectivity.get()
			selected_mouse_property = self.var_mouse_property.get()

			# Monitores ---------------------------------------------------------------------------------------------------------------------------------
			monitors_list = []

			## 1
			monitor_1_model = self.input_monitor_1_model.get() if len(self.input_monitor_1_model.get()) > 0 else "Não informado" # modelo
			monitor_1_inches = self.input_monitor_1_inches.get() if len(self.input_monitor_1_inches.get()) > 0 else "Não informado" # polegadas
			monitor_1_brand = self.input_monitor_1_brand.get() if len(self.input_monitor_1_brand.get()) > 0 else "Não informado" # marca
			monitor_1_assets_code = self.input_monitor_1_assets_code.get() if len(self.input_monitor_1_assets_code.get()) > 0 else "Não informado" # Código Público (Nº do Patrimônio)
			monitor_1_property = self.var_monitor_1_property.get() # propriedade
			monitor_1_ajustable = self.var_monitor_1_ajustable.get() # Ajustável
			monitor_1_portrait_mode = self.var_monitor_1_portrait_mode.get() # Modo Retrato

			if monitor_1_model == "Não informado" and monitor_1_inches == "Não informado" and monitor_1_brand == "Não informado" and monitor_1_assets_code == "Não informado":
				# monitor 1 não será incluído
				pass
			else:
				monitor = {'modelo': monitor_1_model, 'polegadas': monitor_1_inches, 'marca': monitor_1_brand, 'nº de patrimônio': monitor_1_assets_code, 'propriedade': monitor_1_property, 'ajustável': monitor_1_ajustable, 'retrato': monitor_1_portrait_mode}
				monitors_list.append(monitor)

			## 2
			monitor_2_model = self.input_monitor_2_model.get() if len(self.input_monitor_2_model.get()) > 0 else "Não informado" # modelo
			monitor_2_inches = self.input_monitor_2_inches.get() if len(self.input_monitor_2_inches.get()) > 0 else "Não informado" # polegadas
			monitor_2_brand = self.input_monitor_2_brand.get() if len(self.input_monitor_2_brand.get()) > 0 else "Não informado" # marca
			monitor_2_assets_code = self.input_monitor_2_assets_code.get() if len(self.input_monitor_2_assets_code.get()) > 0 else "Não informado" # Código Público (Nº do Patrimônio)
			monitor_2_property = self.var_monitor_2_property.get() # propriedade
			monitor_2_ajustable = self.var_monitor_2_ajustable.get() # Ajustável
			monitor_2_portrait_mode = self.var_monitor_2_portrait_mode.get() # Modo Retrato

			if monitor_2_model == "Não informado" and monitor_2_inches == "Não informado" and monitor_2_brand == "Não informado" and monitor_2_assets_code == "Não informado":
				# monitor 2 não será incluído
				pass
			else:
				monitor = {'modelo': monitor_2_model, 'polegadas': monitor_2_inches, 'marca': monitor_2_brand, 'nº de patrimônio': monitor_2_assets_code, 'propriedade': monitor_2_property, 'ajustável': monitor_2_ajustable, 'retrato': monitor_2_portrait_mode}
				monitors_list.append(monitor)

			## 3
			monitor_3_model = self.input_monitor_3_model.get() if len(self.input_monitor_3_model.get()) > 0 else "Não informado" # modelo
			monitor_3_inches = self.input_monitor_3_inches.get() if len(self.input_monitor_3_inches.get()) > 0 else "Não informado" # polegadas
			monitor_3_brand = self.input_monitor_3_brand.get() if len(self.input_monitor_3_brand.get()) > 0 else "Não informado" # marca
			monitor_3_assets_code = self.input_monitor_3_assets_code.get() if len(self.input_monitor_3_assets_code.get()) > 0 else "Não informado" # Código Público (Nº do Patrimônio)
			monitor_3_property = self.var_monitor_3_property.get() # propriedade
			monitor_3_ajustable = self.var_monitor_3_ajustable.get() # Ajustável
			monitor_3_portrait_mode = self.var_monitor_3_portrait_mode.get() # Modo Retrato

			if monitor_3_model == "Não informado" and monitor_3_inches == "Não informado" and monitor_3_brand == "Não informado" and monitor_3_assets_code == "Não informado":
				# monitor 3 não será incluído
				pass
			else:
				monitor = {'modelo': monitor_3_model, 'polegadas': monitor_3_inches, 'marca': monitor_3_brand, 'nº de patrimônio': monitor_3_assets_code, 'propriedade': monitor_3_property, 'ajustável': monitor_3_ajustable, 'retrato': monitor_3_portrait_mode}
				monitors_list.append(monitor)

			## 4
			monitor_4_model = self.input_monitor_4_model.get() if len(self.input_monitor_4_model.get()) > 0 else "Não informado" # modelo
			monitor_4_inches = self.input_monitor_4_inches.get() if len(self.input_monitor_4_inches.get()) > 0 else "Não informado" # polegadas
			monitor_4_brand = self.input_monitor_4_brand.get() if len(self.input_monitor_4_brand.get()) > 0 else "Não informado" # marca
			monitor_4_assets_code = self.input_monitor_4_assets_code.get() if len(self.input_monitor_4_assets_code.get()) > 0 else "Não informado" # Código Público (Nº do Patrimônio)
			monitor_4_property = self.var_monitor_4_property.get() # propriedade
			monitor_4_ajustable = self.var_monitor_4_ajustable.get() # Ajustável
			monitor_4_portrait_mode = self.var_monitor_4_portrait_mode.get() # Modo Retrato

			if monitor_4_model == "Não informado" and monitor_4_inches == "Não informado" and monitor_4_brand == "Não informado" and monitor_4_assets_code == "Não informado":
				# monitor 4 não será incluído
				pass
			else:
				monitor = {'modelo': monitor_4_model, 'polegadas': monitor_4_inches, 'marca': monitor_4_brand, 'nº de patrimônio': monitor_4_assets_code, 'propriedade': monitor_4_property, 'ajustável': monitor_4_ajustable, 'retrato': monitor_4_portrait_mode}
				monitors_list.append(monitor)

			
			monitors_dict = {}
			for i, monitor in enumerate(monitors_list):
				monitors_dict[f"{i+1}"] = {
					'model': monitor['modelo'],
					'inches': monitor['polegadas'],
					'brand': monitor['marca'],
					'assets_code': monitor['nº de patrimônio'],
					'property': monitor['propriedade'],
					'ajustable': monitor['ajustável'],
					'portrait_mode': monitor['retrato'],
				}

			# Monitores ------------------------------------------------------------------------------------------------------------------------- FIM ---

			file_dict = {
				'date': selected_date.isoformat(),
				'username': username,
				'coord': coord,
				'sector': sector,
				'computer':{
					'local_code': local_code,
					'assets_code': assets_code,
					'device_type': selected_device_type,
					'hardwares_info': {},
					'installed_apps': [],
					'operating_system_info': {},
				},
				'peripherals':{
					'keyboard':{
						'number': key_number,
						'conectivity': selected_key_connectivity,
						'property': selected_key_property
					},
					'mouse':{
						'number': mouse_number,
						'conectivity': selected_mouse_connectivity,
						'property': selected_mouse_property
					},
					'monitor': monitors_dict
				}
			}


			# Informações Iniciais ======================================================================================================================
			
			## 1. Converter o dicionário para string JSON
			info_dict_json = json.dumps(file_dict.copy())
			
			## 2. Criptografar a string dict_json 
			encrypted_data_info = self.encrypt_tool.encrypt(info_dict_json)

			## 3. Salvar os dados criptografados em um arquivo txt
			file_path = os.path.join(os.getcwd(),'user_info.txt')
			with open(os.path.join(os.getcwd(), file_path), 'w', encoding='utf-8') as file:
				file.write(encrypted_data_info)



			# Dados Obtidos =============================================================================================================================
			if not selected_local:
				pass
			else:

				file_name = ""
				if local_code:
					# Cria o nome 
					file_name += f"{selected_date}_{local_code.upper()}_0.txt" # '0' indica que o código a seguir é local_code
				else:
					file_name += f"{selected_date}_{assets_code.upper()}_1.txt" # '1' indica que o código a seguir é assets_code (patrimônio)

				check_files = True
				# Verifica se existe arquivo local nesta data e deleta para evitar duplicidade
				for file in os.listdir(selected_local):
					if file.startswith(f"{selected_date}"):
						if file == file_name:
							file_name_check = file
							check_files = False

				if not check_files:
					confirm = tkmsg.askyesno("Deletar?", "Foram encontrados 1 ou mais arquivos desta data.\nO aplicativo irá deletá-los para evitar duplicidade.\n\nDeseja continuar?")

					if confirm:
						check_files = True
						if os.path.exists(os.path.join(selected_local, file_name_check)):
							os.remove(os.path.join(selected_local, file_name_check))

				if check_files:

					computer_info = ComputerInfo()
					file_dict['computer']['hardwares_info'] = computer_info.hardware_dict()
					file_dict['computer']['operating_system_info'] = computer_info.operating_system_dict()
					
					import platform
					operating_system = platform.system()
					if operating_system == 'Windows':
						file_dict['computer']['installed_apps'] = computer_info.win_app_list()
					elif operating_system == 'Darwin': # macOS
						pass
					elif operating_system == 'Linux':
						pass


					## 1. Converter o dicionário para string JSON
					dict_json = json.dumps(file_dict.copy())

					## 2. Criptografar a string dict_json 
					encrypted_data = self.encrypt_tool.encrypt(dict_json)

					## 3. Salvar os dados criptografados em um arquivo txt
					with open(os.path.join(selected_local, file_name), 'w', encoding='utf-8') as file:
						file.write(encrypted_data)
					
					# Teste
					#with open(os.path.join(os.getcwd(), file_name), 'w', encoding='utf-8') as file:
					#	json.dump(file_dict, file, ensure_ascii=False, indent=4)


def main(args):
	app = my_App()
	app.execute()
	return 0


if __name__ == '__main__':
	sys.exit(main(sys.argv))