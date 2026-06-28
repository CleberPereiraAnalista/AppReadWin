from encryption_tool import EncryptionTool
import json
import os
from pandas import DataFrame, ExcelWriter, json_normalize

class CreateFile1():

	def __init__(self, origin_dir, destiny_dir):
		self.origin_dir = origin_dir
		self.destiny_dir = destiny_dir

		encrypt_key = b'4KMn4L_Pd7ycmJ7WVmxKoIQ2WjPAEYNqKw-Kw8LzCW4='
		self.encrypt_tool = EncryptionTool(encrypt_key.strip())

		self.data_records = []



	def create(self):
		
		# Lê cada arquivo e os armazena em uma lista
		for file in os.listdir(self.origin_dir):
			file_path = os.path.join(self.origin_dir,file)

			if os.path.exists(file_path):
				with open(file_path, 'rb') as file:
					data = file.read()

				if len(data) > 0:
					decrypted_data = self.encrypt_tool.decrypt(data)
					data_dict = json.loads(decrypted_data)
					
					self.data_records.append(data_dict)


		if len(self.data_records) > 0:
			"""
			cria string em formato csv para cada tipo de arquivo:
			file_dict_1 : informações sobre cada usuário
			file_dict_2 : informações sobre hardware de cada computador
			file_dict_3 : informações sobre apps de cada computador
			file_dict_4 : informações sobre sistema operacional de cada computador
			file_dict_5 : informações sobre periférico de cada computador
			"""

			file_dict_1 = {
				'código':[],
				'data':[],
				'usuário':[],
				'coord':[],
				'setor':[],
				'tipo':[],
				'código local':[],
				'patrimônio':[],
				'memória RAM':[],
				'monitores':[],
				'monitores particular':[],
				'mouse particular': [],
				'teclado particular': [],
			}

			file_dict_2 = {
				'código da estação':[],
				'código':[],
				'hardwares':[],
				'especificações':[],
				'definição':[],
				'valor':[]
			}

			file_dict_3 = {
				'código da estação':[],
				'aplicações':[]
			}

			file_dict_4 = {
				'código da estação':[],
				'nome':[],
				'lançamento':[],
				'versão':[],
				'arquitetura':[]
			}

			file_dict_5 = {
				'código da estação':[],
				'recurso':[], # hardware, aplicativos, teclado, mouse, monitor
				'código':[],
				'especificação':[],
				'valor':[],
			}

			# Discos (Particões) chave composta tripla
			file_dict_6 = {
				'código da estação':[],
				'código do disco':[],
				'código':[],
				'especificações':[],
				'definição':[],
				'valor':[]
			}

			for i, record in enumerate(self.data_records):
				code = i+1
				date_record = record['date'].split('-')
				date = f"{date_record[2]}/{date_record[1]}/{date_record[0]}"
				username = record['username']
				coord = record['coord']
				sector = record['sector']
				device_type = record['computer']['device_type']
				local_code = record['computer']['local_code']
				assets_code = record['computer']['assets_code']

				monitores_total = 0 
				monitores_particular_total = 0
				mouse_particular_total = 0
				teclado_particular_total = 0
				if record['computer']['hardwares_info']:
					if 'physical_memory_total' in record['computer']['hardwares_info'].keys():
						memoria_ram_total = record['computer']['hardwares_info']['physical_memory_total']/(1024**3)
					else:
						memoria_ram_total = 0
				else:
					memoria_ram_total = 0

				file_dict_1['código'].append(code)
				file_dict_1['data'].append(date)
				file_dict_1['usuário'].append(username)
				file_dict_1['coord'].append(coord)
				file_dict_1['setor'].append(sector)
				file_dict_1['tipo'].append(device_type)
				file_dict_1['código local'].append(local_code)
				file_dict_1['patrimônio'].append(assets_code)

				# Declaração de Conjuntos (colunas)

				## Hardware
				hard_workstation_record_code = [] # código da estação (FK)
				hard_order = [] # código de ordenação do hardware durante a leitura das informações
				hardwares = []
				hard_specifications = [] 
				hard_definition = [] 
				hard_value = [] 

				## Hardware - Disk - Partitions
				partition_workstation_record_code = []
				partition_disk_code = []
				partition_order = []
				partition_specifications = []
				partition_definition = []
				partition_value = []

				## Apps
				app_workstation_record_code = []
				apps = []

				## Sistema Operacional
				so_workstation_record_code = []
				so_name = []
				so_release = []
				so_version = []
				so_architecture = []

				# Periféricos
				periph_workstation_record_code = []
				periph_order = []
				periph_resource = []
				periph_specification = []
				periph_value = []

				
				# iterar em cada nível e obter as informações que compõem as colunas. Alguns serão preenchidos em vazio

				## A. Computador
				
				### A.1 - Computer - Hardwares
				nickname_item_dict = {'processor': 'Processador', 'base_board': 'Placa-mãe', 'physical_memory':'Memória RAM', 'gpu':'Vídeo', 'disk':'Disco'}
				nickname_specifications_to_definition = {
					'manufacturer': 'Fabricante',
					'model': 'Modelo',
					'version': 'Versão',
					'serial_number': 'Serial',
					'part_number_mem': 'Serial',
					'serial_number_mem': 'Serial (Lote)',
					'driver': 'Driver',
					'type': 'Tipo',
					'type_code': 'Tipo (código)',
					'capacityGB_text': 'Capacidade (GB)',
					'capacityMB_text': 'Capacidade (MB)',
					'speed_text': 'Velocidade',
					'device': 'Unidade',
					'disk_brand_model': 'Marca (Modelo)',
					'disk_manufacturer': 'Fabricante',
					'disk_serial_number': 'Serial',
					'file_system': 'Sistema de Arquivos',
					'disk_total_gb_text': 'Espaço Total (GB)',
					'total_gb_text': 'Espaço Total (GB)',
					'used_gb_text': 'Espaço Usado (GB)',
					'free_gb_text': 'Espaço Livre (GB)',
					'used_percent_text': 'Espaço %',
					'free_percent_text': 'Espaço %',
					}
				nickname_specifications_to_value = {
					'physical_cores': 'Núcleos Físicos',
					'capacity': 'Capacidade',
					'disk_total_gb': 'Capacidade',
					'total_gb': 'Capacidade',
					'used_gb': 'Capacidade',
					'free_gb': 'Capacidade',
					'used_percent': 'Percentual',
					'free_percent': 'Percentual',
					#'capacityGB': 'Capacidade (GB)',
					#'capacityMB': 'Capacidade (MB)',
					#'speed': 'Velocidade',
				}
				reference_value = {
					'speed_text': 'speed',
					'capacityGB_text': 'capacityGB',
					'capacityMB_text': 'capacityMB',
					'disk_total_gb_text': 'disk_total_gb',
					'total_gb_text': 'total_gb',
					'used_gb_text': 'used_gb',
					'free_gb_text': 'free_gb',
					'used_percent_text': 'used_percent',
					'free_percent_text': 'free_percent',

				}

				if record['computer']['hardwares_info']:
					for hardware, specifications in record['computer']['hardwares_info'].items():
						if isinstance(specifications, dict):
							for order_id, specification_dict in specifications.items():
								for specification, value in specification_dict.items():
									if specification in nickname_specifications_to_definition.keys():
										if specification in reference_value.keys():
											hard_workstation_record_code.append(code)
											hard_order.append(str(order_id))
											hardwares.append(nickname_item_dict[hardware])
											hard_specifications.append(nickname_specifications_to_definition[specification])
											hard_definition.append(value)
											key = reference_value[specification]
											val = record['computer']['hardwares_info'][hardware][order_id][key]
											hard_value.append(val)
										elif not specification in nickname_specifications_to_value.keys():
											hard_workstation_record_code.append(code)
											hard_order.append(str(order_id))
											hardwares.append(nickname_item_dict[hardware])
											hard_specifications.append(nickname_specifications_to_definition[specification])
											hard_definition.append(value)
											hard_value.append(0)
									elif specification in nickname_specifications_to_value.keys():
										if specification in reference_value.keys():
											hard_workstation_record_code.append(code)
											hard_order.append(str(order_id))
											hardwares.append(nickname_item_dict[hardware])
											hard_specifications.append(nickname_specifications_to_value[specification])
											hard_definition.append('')
											hard_value.append(value)
									#if specification == 'partitions':
									#	print(f"\n{}\n")

					file_dict_2['código da estação'] += hard_workstation_record_code
					file_dict_2['código'] += hard_order
					file_dict_2['hardwares'] += hardwares
					file_dict_2['especificações'] += hard_specifications
					file_dict_2['definição'] += hard_definition
					file_dict_2['valor'] += hard_value

					### A.1 - Computer - Hardwares - Disks - Partitions
					for disk_code, disk in record['computer']['hardwares_info']['disk'].items():
						for partition_id, specifications in disk['partitions'].items():
							for specification, value in specifications.items():
								if specification in nickname_specifications_to_definition.keys():
									if specification in reference_value.keys():
										partition_workstation_record_code.append(code)
										partition_disk_code.append(disk_code)
										partition_order.append(partition_id)
										partition_specifications.append(nickname_specifications_to_definition[specification])
										partition_definition.append(value)
										key = reference_value[specification]
										val = record['computer']['hardwares_info']['disk'][disk_code]['partitions'][partition_id][key]
										partition_value.append(val)
									elif not specification in nickname_specifications_to_value.keys():
										partition_workstation_record_code.append(code)
										partition_disk_code.append(disk_code)
										partition_order.append(partition_id)
										partition_specifications.append(nickname_specifications_to_definition[specification])
										partition_definition.append(value)
										partition_value.append(0)
								elif specification in nickname_specifications_to_value.keys():
									if specification in reference_value.keys():
										partition_workstation_record_code.append(code)
										partition_disk_code.append(disk_code)
										partition_order.append(partition_id)
										partition_specifications.append(nickname_specifications_to_definition[specification])
										partition_definition.append('')
										partition_value.append(value)
					file_dict_6['código da estação'] += partition_workstation_record_code
					file_dict_6['código do disco'] += partition_disk_code
					file_dict_6['código'] += partition_order
					file_dict_6['especificações'] += partition_specifications
					file_dict_6['definição'] += partition_definition
					file_dict_6['valor'] += partition_value
			

				### A.2 - Computer - Apps
				if record['computer']['installed_apps']:
					for app in record['computer']['installed_apps']:
						app_workstation_record_code.append(code)
						apps.append(app)
					file_dict_3['código da estação'] += app_workstation_record_code
					file_dict_3['aplicações'] += apps


				### A.3 - Computer - Sistema Operacional
				if record['computer']['operating_system_info']:
					so_workstation_record_code.append(code)
					so_name.append(record['computer']['operating_system_info'].get('name'))
					so_release.append(record['computer']['operating_system_info']['release'])
					so_version.append(record['computer']['operating_system_info']['version'])
					so_architecture.append(record['computer']['operating_system_info']['architecture'])

					file_dict_4['código da estação'] += so_workstation_record_code
					file_dict_4['nome'] += so_name
					file_dict_4['lançamento'] += so_release
					file_dict_4['versão'] += so_version
					file_dict_4['arquitetura'] += so_architecture

				
				## B. Periféricos
				nickname_periph_dict = {
					'number':'número', 
					'conectivity':'conectividade', 
					'property':'propriedade',
					'model':'modelo',
					'inches':'polegadas',
					'brand':'marca',
					'assets_code':'nº de patrimônio',
					'ajustable':'ajustável',
					'portrait_mode':'retrato',
				}

				### B.1 - Peripherals - Teclado
				for specification, value in record['peripherals']['keyboard'].items():
					if value == "particular":
						teclado_particular_total += 1
					periph_workstation_record_code.append(code)
					periph_order.append('1')
					periph_resource.append('teclado')
					periph_specification.append(nickname_periph_dict[specification])
					periph_value.append(value)

				### B.2 - Peripherals - Mouse
				for specification, value in record['peripherals']['mouse'].items():
					if value == 'particular':
						mouse_particular_total += 1
					periph_workstation_record_code.append(code)
					periph_order.append('1')
					periph_resource.append('mouse')
					periph_specification.append(nickname_periph_dict[specification])
					periph_value.append(value)

				### B.3 - Peripherals - Monitor

				for order_id, specifications in record['peripherals']['monitor'].items():
					monitores_total += 1
					for specification, value in specifications.items():
						if value == 'particular':
							monitores_particular_total += 1
						periph_workstation_record_code.append(code)
						periph_order.append(str(order_id))
						periph_resource.append('monitor')
						periph_specification.append(nickname_periph_dict[specification])
						periph_value.append(value)

				file_dict_5['código da estação'] += periph_workstation_record_code
				file_dict_5['código'] += periph_order
				file_dict_5['recurso'] += periph_resource
				file_dict_5['especificação'] += periph_specification
				file_dict_5['valor'] += periph_value

				
				file_dict_1['memória RAM'].append(memoria_ram_total) 
				file_dict_1['monitores'].append(monitores_total)
				file_dict_1['monitores particular'].append(monitores_particular_total)
				file_dict_1['mouse particular'].append(mouse_particular_total)
				file_dict_1['teclado particular'].append(teclado_particular_total)


			df1 = DataFrame(file_dict_1)
			df2 = DataFrame(file_dict_2)
			df6 = DataFrame(file_dict_6)
			df3 = DataFrame(file_dict_3)
			df4 = DataFrame(file_dict_4)
			df5 = DataFrame(file_dict_5)

			message = ""
			try:
				with ExcelWriter(os.path.join(self.destiny_dir,'info_computadores.xlsx')) as writer:
					df1.to_excel(writer, sheet_name='EstaçãoDeTrabalho', index=False)
					df2.to_excel(writer, sheet_name='Hardware', index=False)
					df6.to_excel(writer, sheet_name='DiscoPartições', index=False)
					df3.to_excel(writer, sheet_name='Aplicativos', index=False)
					df4.to_excel(writer, sheet_name='SistemaOperacional', index=False)
					df5.to_excel(writer, sheet_name='Periféricos', index=False)

				message = f"Arquivo 'info_computadores.xlsx' criado com sucesso.\n - LOCAL: {self.destiny_dir}\n\nEspero que goste!"
				return True, message
			except Exception as err:
				message = f"Ocorreu um erro durante a gravação.\n\nCaso o erro ocorra novamente entre me contato com o desenvolvedor deste aplicativo e informe este erro:\n- {err}"
				return False, message


	def create_file_0(self):
		"""
		Arquivo normalizado onde cada arquivo compõe uma linha
		Poderá gerar problema devido diferenças nas quantidades de cada item (ex: quantidade de chips de memória RAM)
		"""
		file_path_destin = os.path.join(self.destiny_dir,'info_computadores.xlsx')
		df = json_normalize(self.data_records)
		df.to_excel(file_path_destin)