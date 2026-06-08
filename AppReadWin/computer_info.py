import platform
import winreg
import wmi

class ComputerInfo:

	def hardware_dict(self):
		memory_type_ddr = {20: 'DDR', 21:'DDR2', 24: 'DDR3', 26: 'DDR4', 27: 'DDR5'}

		if platform.system() == "Windows":
			try:
				hardware_info_dict = {
					'processor': {},
					'base_board': {},
					'physical_memory_total':0,
					'physical_memory':{},
					'gpu':{}
				}

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
					mem_capacity_gb = mem_capacity / 1024**3
					if mem_capacity_gb < 0:
						mem_capacity_gb = mem_capacity_gb * (-1)

					mem_speed = memory.Speed
					
					memory_dict = {
						'type_code': memory.MemoryType,
						'type': memory_type_ddr.get(memory.MemoryType, f"Desconhecido({memory.MemoryType})"),
						'capacity': mem_capacity,
						'capacityGB': mem_capacity_gb,
						'capacityGB_text': f"{mem_capacity_gb:.2f} GB",
						'speed': mem_speed,
						'speed_text': f"{mem_speed} MHz",
						'manufacturer': f"{memory.Manufacturer.strip()}",
						'serial_number': f"{memory.SerialNumber}"
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