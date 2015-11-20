''' LustreFS tuner application '''

#Черновой вариант, нужно прогнать через VS Code перез pylint-ом

import binascii

class LustreTuner:
	''' Tuner that check and configure
	    params of Lustre MDT and OST 
	    devices 
	'''
	
	def __init__(self):
		#TODO:Сюда добавить инифиализацию конфига
		self.kenel = self.check_kernel()
		self.ip = self.get_ip()
		#TODO:Узнать у пользователя, используется ли на
		# машине MDT и записать результат в on_mdt_host
		self.on_mdt_host = None
		self.interface = self.get_interface()

	def check_kernel(self):
		''' Checking kernel name to contain 'lustre'
		    and checking if mkfs.lustre is available
		'''

		return None

	def get_ip(self):
		''' Getting IP of mgsnode if launched on MDT
		    or ask user for mdsnode if launched on OST
		'''
		#TODO:Вызвать ifconfig или что-то такое, чтобы
		# получить IP интерфейса

		return None

	def get_interface(self):
		''' Asking user for interface type and checking
		    /etc/modprobe.d/lnet.conf
		'''
		
		return None

	def perform(self, command):
		''' Recognize and perform command '''
		

	def format_device(self):
		''' Performing format of device by user input '''

	def check_index(self):
		''' Checking for invalid (dublicate) index of OST/MDT '''

if __name__ == '__main__':
	#Откючаю сообщения pylint о константах
        # pylint: disable=C0103
	lustre_tuner = LustreTuner()	

	
