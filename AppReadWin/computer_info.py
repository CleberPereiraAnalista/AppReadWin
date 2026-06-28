import platform
import winreg
import wmi

class ComputerInfo:

	def hardware_dict(self):
		memory_type_ddr = {
			0: 'Desconhecido', 1: 'Outro', 2: 'DRAM', 3: 'DRAM Síncrona', 4: 'Cache DRAM',
			5: 'EDO', 6: 'EDRAM', 7: 'VRAM', 8: 'SRAM', 9: 'RAM', 10: 'ROM', 11: 'Flash', 
			12: 'EEPROM', 13: 'FEPROM', 14: 'EPROM', 15: 'CDRAM', 16: '3DRAM', 17: 'SDRAM', 18: 'SGRAM', 19: 'RDRAM', 
			20: 'DDR', 21:'DDR2', 22:'DDR2 FB-DIMM', 24: 'DDR3', 26: 'DDR4', 27: 'DDR5', 28: 'LPDDR', 34: 'DDR5'
		}

		if platform.system() == "Windows":
			try:
				hardware_info_dict = {
					'processor': {},
					'base_board': {},
					'physical_memory_total':0,
					'physical_memory':{},
					'gpu':{},
					'disk':{}
				}

				# Inicializa o namespace padrão do WMI
				w = wmi.WMI()


				# Placa-mãe
				for i, board in enumerate(w.Win32_BaseBoard()):
					base_board_dict = {
						'manufacturer': board.Manufacturer,
						'model': board.Product,
						'version': board.Version,
						'serial_number': board.SerialNumber
					}
					hardware_info_dict['base_board'][f"{i+1}"] = base_board_dict


				# Processadores
				for i, cpu in enumerate(w.Win32_Processor()):
					cpu_dict = {
						'model': cpu.Name.strip(),
						'manufacturer': cpu.Manufacturer,
						'physical_cores': cpu.NumberOfCores
					}
					hardware_info_dict['processor'][f"{i+1}"] = cpu_dict


				# Memória RAM
				total_memory = 0
				for i, memory in enumerate(w.Win32_PhysicalMemory()):
					mem_capacity = int(memory.Capacity)
					total_memory += mem_capacity
					mem_capacity_gb = mem_capacity / (1024**3)
					if mem_capacity_gb < 0:
						mem_capacity_gb = mem_capacity_gb * (-1)

					mem_speed = memory.Speed
					mem_type = memory.SMBIOSMemoryType
					
					memory_dict = {
						'type_code': mem_type,
						'type': memory_type_ddr.get(mem_type, f"Desconhecido({mem_type})"),
						'capacity': mem_capacity,
						'capacityGB': mem_capacity_gb,
						'capacityGB_text': f"{mem_capacity_gb:.2f} GB",
						'speed': mem_speed,
						'speed_text': f"{mem_speed} MHz",
						'manufacturer': f"{memory.Manufacturer.strip()}",
						'part_number_mem': f"{memory.PartNumber.strip() if memory.PartNumber else 'N/A'}",
						'serial_number_mem': f"{memory.SerialNumber.strip() if memory.SerialNumber else 'N/A'}"
					}
					hardware_info_dict['physical_memory'][f"{i+1}"] = memory_dict
				
				hardware_info_dict['physical_memory_total'] = total_memory


				# Placas de Vídeo
				for i, gpu in enumerate(w.Win32_VideoController()):
					mem_capacity = int(gpu.AdapterRAM) if gpu.AdapterRAM else 0
					mem_capacity_mb = mem_capacity/(1024 * 1024)
					if mem_capacity_mb < 0:
						mem_capacity_mb = mem_capacity_mb * (-1)
					gpu_dict ={
						'model': gpu.Name,
						'driver': gpu.DriverVersion,
						'capacity': mem_capacity,
						'capacityMB': mem_capacity_mb,
						'capacityMB_text': f"{mem_capacity_mb} MB",
					}
					hardware_info_dict['gpu'][f"{i+1}"] = gpu_dict

				# Discos e Partições ---------------------------------------
				
				## Inicializa o namespace de armazenamento (storage)
				w_storage = wmi.WMI(namespace="root/Microsoft/Windows/Storage")

				## Mapa para os tipos de mídia da classe MSFT_PhysicalDisk
				MEDIA_TYPES = {
					3: "HDD",
					4: "SSD",
					5: "SCM",
					0: "Indefinido ou HDD antigo"
				}

				## Mapa para obter o id utilizado de cada disco 
				# { <modelo>: <index do hardware_info_dict['disk']> }
				disk_dict = {} 

				## Cria um dicionário para mapear o número do disco físico ao seu tipo de mídia (HDD/SSD)
				disk_types = {}
				try:
					for i, disk in enumerate(w_storage.MSFT_PhysicalDisk()):
							# O DeviceID mapeia diretametne para o Index do Win32_DiskDrive
							disk_types[str(disk.DeviceID)] = MEDIA_TYPES.get(disk.MediaType, "Desconhecido")
							size = int(getattr(disk, 'Size', '0'))
							
							disk_total_gb = 0
							if size > 0:
								disk_total_gb = size / (1024**3) 
							else:
								disk_total_gb = 0

							disk_dict[disk.Model] = f"{i+1}"
							
							hardware_info_dict['disk'][f"{i+1}"] = {
								'model': disk.Model,
								'disk_total_gb': disk_total_gb, 
								'disk_total_gb_text': f"{disk_total_gb:.2f} GB",
								'partitions': {}
							}
				except Exception:
					# Caso o sistema não tenha suporte ao namespace Storage (versões muito antigas)
					pass

				# Percorre todas as partições lógicas (ex: C:, D:)
				for i, drive in enumerate(w.Win32_LogicalDisk(DriveType=3)):
					device = drive.DeviceID
					file_system = drive.FileSystem

					# Cálculos de espaço em Gigabytes (GB)
					total_gb = int(drive.Size or 0) / (1024 ** 3)
					free_gb = int(drive.FreeSpace or 0) / (1024 ** 3)
					used = (total_gb - free_gb) 
					used_gb = used if used > 0 else 0
					used_percent = (used_gb / total_gb) if used > 0 else 0.0
					free_percent = (free_gb / total_gb)

					# Encontra o disco físico associado à partição
					for partition in drive.associators("Win32_LogicalDiskToPartition"):
						# Encontra o disco físico associado à partição
						for disk in partition.associators("Win32_DiskDriveToDiskPartition"):
							disk_brand_model = disk.Model
							disk_manufacturer = getattr(disk, 'Manufacturer', 'Desconhecido')
							disk_serial_number = disk.SerialNumber.strip()

							partition_dict = {
								'device': device,
								'file_system': file_system,
								'disk_brand_model': disk_brand_model,
								'disk_manufacturer': disk_manufacturer,
								'disk_serial_number': disk_serial_number,
								'total_gb': total_gb, 
								'total_gb_text': f'{total_gb:.2f} GB',
								'used_gb': used_gb,
								'used_gb_text': f'{used_gb:.2f} GB',
								'free_gb': free_gb, 
								'free_gb_text': f'{free_gb:.2f} GB',
								'used_percent': used_percent,
								'used_percent_text': f'{(used_percent*100):.2f} %',
								'free_percent': free_percent,
								'free_percent_text': f'{(free_percent*100):.2f} %'
							}	

							disk_dict_id = disk_dict.get(disk_brand_model)

							partition_id = len(hardware_info_dict['disk'][disk_dict_id]['partitions'].keys()) + 1

							hardware_info_dict['disk'][disk_dict_id]['partitions'][f"{partition_id}"] = partition_dict
				

			except Exception as er:
				#print("ERRO", er)
				hardware_info_dict = {}
		else:
			try:
				hardware_info_dict = {
					'processor': platform.processor(),
				}
			except:
				hardware_info_dict = {}

		
		return hardware_info_dict


	def operating_system_dict(self):

		operating_system_info_dict = {
			'name': platform.system(),
			'release': platform.release(),
			'version': platform.version(),
			'architecture': platform.machine()
		}

		return operating_system_info_dict


	def win_app_list(self):
		apps_win_list = []
		
		registry_paths =  [
			(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
			(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
			(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
		]

		for hkey, subkey in registry_paths:
			try:
				reg = winreg.ConnectRegistry(None, hkey)
				key = winreg.OpenKey(reg, subkey)
				for i in range(winreg.QueryInfoKey(key)[0]):
					try:
						software_key_name = winreg.EnumKey(key, i)
						software_key = winreg.OpenKey(key, software_key_name)
						software_name = winreg.QueryValueEx(software_key, "DisplayName")[0]
						apps_win_list.append(software_name)
					except Exception:
						continue

			except WindowsError:
				continue

		return apps_win_list