import datetime
import os
import json


class jsonDate(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return obj.strftime("%Y-%m-%d %H:%M:%S.%f")
		elif isinstance(obj, datetime.date):
			return obj.strftime("%Y-%m-%d")
		else:
			return json.JSONEncoder.default(self, obj)


class _cls_base:
	def __init__(self, base: str):
		pass

	@property
	def slash(self):
		if os.name == 'nt':
			return '\\'
		else:
			return '/'


class _cls_log_txt(_cls_base):
	# noinspection PyMissingConstructor
	def __init__(self, log_dir: str = None):
		self.log_file_dir = log_dir
		self.log_file_path = None

	def check_path(self):
		now_path = os.getcwd()

		arr_now_path = now_path.split(self.slash)

		log_file_dir = None

		for i in arr_now_path:
			dir_name = i
			if dir_name != 'module':
				if log_file_dir is None:
					log_file_dir = dir_name
				else:
					log_file_dir = log_file_dir + self.slash + dir_name
			else:
				break

		today = datetime.date.today()

		self.log_file_path = self.log_file_dir + self.slash + "log" + self.slash + f"rst_{today}.log"

	def add(self, new_log):
		if self.log_file_path is None:
			self.check_path()
		else:
			pass

		try:
			f = open(self.log_file_path, 'a', encoding='utf-8')
			f.writelines("\n")

			if new_log is None:
				log = {'gmt0': datetime.datetime.utcnow(), 'rst': new_log}
			else:
				log = {'gmt0': datetime.datetime.utcnow(), 'rst': new_log}

			log = json.dumps(log, ensure_ascii=False, cls=jsonDate)

			f.writelines(log)
			f.close()
		except Exception as e:
			# self.set_error(e.__str__())
			print("Log Write Error:" + e.__str__())


class _cls_aide_rst_base(_cls_base):
	# noinspection PyMissingConstructor
	def __init__(self, module: str, log_level: int = 1):
		self.__dict_rst = {"state": False,
						   "msg": None,
						   "data": None,
						   "dur": None,
						   'process': None,
						   'module': module}

		self.log = _cls_log_txt()
		self.log_level = log_level

		self.start_time = None

	@staticmethod
	def now():
		return datetime.datetime.now()

	@property
	def dur(self,
			my_time_earlier: datetime.datetime = None,
			my_time_later: datetime.datetime = None):

		if my_time_later is None:
			my_time_later = datetime.datetime.now()
		else:
			pass

		if my_time_earlier is None:
			if isinstance(self.start_time, datetime.datetime):
				my_time_earlier = self.start_time
			else:
				return None
		else:
			pass

		diff_second = (my_time_later - my_time_earlier).seconds

		return diff_second

	@staticmethod
	def __get_dict_value(my_dict_rst, my_key):
		if my_dict_rst.__contains__(my_key):
			return my_dict_rst[my_key]
		else:
			return None

	@property
	def state(self):
		return self.__get_dict_value(self.__dict_rst, "state")

	def set_state(self, new_state: bool = False):
		self.__dict_rst["state"] = new_state

		if self.log_level == 0:
			pass
		elif self.log_level == 1:
			if new_state is False:
				self.log.add(self.all)
			else:
				pass
		elif self.log_level == 2:
			if new_state in [False, 2]:
				self.log.add(self.all)
			else:
				pass
		elif self.log_level == 3:
			self.log.add(self.all)

	@property
	def msg(self):
		return self.__get_dict_value(self.__dict_rst, "msg")

	def set_msg(self, new_msg: object = None):
		self.__dict_rst["msg"] = new_msg

	@property
	def data(self):
		return self.__get_dict_value(self.__dict_rst, "data")

	def set_data(self, new_data: object = None):
		self.__dict_rst["data"] = new_data

	@property
	def process(self):
		return self.__get_dict_value(self.__dict_rst, "process")

	def set_process(self, new_process_name: str = None):
		self.__dict_rst["process"] = new_process_name

	@property
	def all(self):
		return self.__dict_rst

	def set(self, new_state: object, new_msg: object = None, new_data: object = None, new_process: str = None):

		if isinstance(new_state, dict):
			state = new_state["state"]
			msg = new_state["msg"]
			data = new_state["data"]
		else:
			state = new_state
			msg = new_msg
			data = new_data

		self.set_msg(msg)
		self.set_data(data)
		if new_process is not None:
			self.set_process(new_process)
		else:
			pass

		# fang zai zui hou ,chu fa ri zhi
		self.set_state(state)

	def print(self):
		print(self.all)

	def addlog(self):
		self.log.add(self.all)
