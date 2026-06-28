from create_file_1 import CreateFile1
from tkinter import font
from tkinter import ttk
import sys
import tkinter as tk
import tkinter.filedialog as fdlg
import tkinter.scrolledtext as tkst
import tkinter.messagebox as tkmsg

class my_App:

	def __init__(self, **kw):
		self.root = tk.Tk()
		self.root.title("AppReadWin_Manager - Consolidador de dados coletados sobre Sistema Operacional Microsoft\u2122 Windows\u2122")
		#self.root.title("Leitor de informações sobre computador com Sistema Operacional Microsoft\u00AE Windows\u00AE")
		self.root.geometry('%dx%d+%d+%d'%(800,250,0,0))
		self.root.resizable(width=False, height=False)

		self.create_initial_area()


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
		self.mainframe.grid(row=0, column=0, sticky='ns', pady=5)

		# Frame LEFT (Origin path)
		self.frm_left = tk.Frame(self.mainframe, borderwidth=1, relief="groove", bg='light grey')
		self.frm_left.grid(row=1, column=0, columnspan=2, padx=(5,11), sticky='ns')

		# Frame RIGHT (Destiny path)
		self.frm_right = tk.Frame(self.mainframe, borderwidth=1, relief="groove", bg='light grey')
		self.frm_right.grid(row=1, column=2, columnspan=3, padx=(11,5), sticky='ns')


		# Frame LEFT >> Origem
		self.btn_orig_path = tk.Button(self.frm_left,
		                                text='Informar pasta com arquivos',
		                                cursor='hand2',
		                                bg='light grey',
		                                borderwidth=1,
		                                activebackground='grey',
		                                font=font.Font(size=9, weight='bold', slant='italic'),
		                                command=self.get_origin_path)
		self.btn_orig_path.grid(row=0, column=0, columnspan=2, sticky='we', padx=5, pady=5)

		self.lbl_origin_path = tk.Label(self.frm_left, text='Diretório de origem:', font=font.Font(size=10, weight='bold'), bg='light grey')
		self.lbl_origin_path.grid(row=1, column=0, padx=5, pady=5)

		self.input_origin_path = tkst.ScrolledText(
			self.frm_left,
			font=font.Font(size=10, weight='normal'),
			width=50,
			height=3,
			wrap='word',
			background='light grey',
			#state='disabled'
			)
		self.input_origin_path.grid(row=2, column=0, padx=5, pady=5)


		# Frame RIGHT >> Destino
		self.btn_destiny_path = tk.Button(
			self.frm_right,
			text='Informar pasta para gravar',
			cursor='hand2',
			bg='light grey',
			borderwidth=1,
			activebackground='grey',
			font=font.Font(size=9, weight='bold', slant='italic'),
			command=self.get_destiny_path )
		self.btn_destiny_path.grid(row=0, column=0, columnspan=2, sticky='we', padx=5, pady=5)

		self.lbl_destiny_path = tk.Label(self.frm_right, text='Diretório de destino:', font=font.Font(size=10, weight='bold'), bg='light grey')
		self.lbl_destiny_path.grid(row=1, column=0, padx=5, pady=5)

		self.input_destiny_path = tkst.ScrolledText(
			self.frm_right,
			font=font.Font(size=10, weight='normal'),
			width=50,
			height=3,
			wrap='word',
			background='light grey',
			#state='disabled'
			)
		self.input_destiny_path.grid(row=2, column=0, padx=5, pady=5)


	    # Final -----------------------------------------------------------------------------------------
		final_row_init = 21

		self.btn_create_file_1 = tk.Button(
			self.mainframe,
			text="Consolidar Dados",
			font=tk.font.Font(size=12, weight='bold'),
			background='#1a1aff',
			foreground='#dddddd',
			command=self.export_file_1
		)
		self.btn_create_file_1.grid(row=final_row_init, columnspan=10, sticky='we', padx=5, pady=10)

		self.label_msg = tk.Label(
			self.mainframe,
			text='Atualizando... aguarde pelo término!',
			font=tk.font.Font(size=9, slant="italic"),
			fg="red",
			justify=tk.CENTER,
			anchor="center",
		)
		

		# Container Footer ------------------------------------------------------------------------------
		sep = tk.ttk.Separator(self.mainframe, orient='horizontal')
		sep.grid(row=final_row_init+1, column=0, columnspan=10, stick='we', padx=5, pady=(15,5))

		created_by = tk.Label(self.mainframe, text="Criado por Cleber Almeida Pereira", font=tk.font.Font(size=7), bg='light grey')
		created_by.grid(row=final_row_init+2, column=0, columnspan=10, padx=5, pady=1, stick='we')
		contact = tk.Label(self.mainframe, text="contato: (67) 99607-6081", font=tk.font.Font(size=7), bg='light grey')
		contact.grid(row=final_row_init+3, column=0, columnspan=10, padx=5, pady=1, stick='we')
		# Container Footer ---------------------------------------------------------------------- FIM ---


	def get_origin_path(self):
		orig_path = fdlg.askdirectory()     # "Caminho Original"
		self.input_origin_path.delete("0.0", "end")
		self.input_origin_path.insert("1.0", orig_path)


	def get_destiny_path(self):
		destiny_path = fdlg.askdirectory()  # "Caminho de Destino"
		self.input_destiny_path.delete("0.0", "end")
		self.input_destiny_path.insert("1.0", destiny_path)


	def export_file_1(self):

		self.label_msg.grid(row=22, column=0, columnspan=4, padx=6, pady=0)
		self.mainframe.update()
		self.run_export_file_1()


	def run_export_file_1(self):
		origin_dir = self.input_origin_path.get("1.0","end").strip()
		destiny_dir = self.input_destiny_path.get("1.0","end").strip()

		execute = True

		if len(origin_dir) == 0 or len(destiny_dir) == 0:
			execute = False
			tkmsg.showerror("Não posso continuar!", "Para continuar você deverá informar as pastas de origem e de destino.")

		if execute:
			cf = CreateFile1(origin_dir, destiny_dir)
			response, message = cf.create()

			if response:
				tkmsg.showinfo("Que bom!", message)
			else:
				tkmsg.showerror("Ah! Algo deu errado...", message)

			self.label_msg.grid_forget()

		else:
			self.label_msg.grid_forget()



def main(args):
	app = my_App()
	app.execute()
	return 0


if __name__ == '__main__':
	sys.exit(main(sys.argv))