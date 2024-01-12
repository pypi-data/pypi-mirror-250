# -*- encoding: utf-8 -*-
"""
@File    :   ColorInfo.py
@Time    :   2022-10-19 16:01
@Author  :   坐公交也用券
@Version :   1.1.9
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   彩色日志
"""
import inspect
from datetime import datetime
from os import path, environ
import platform
from sys import exit


class ColorLogger:
	def __init__(self, file=None, txt=False, class_name=None, cover=False, fileinfo=False, basename=True):
		"""
		初始化日志模块
		:param file: 设置日志文件
		:param txt: 是否启用文本记录功能
		:param class_name: 调用的Class名称
		:param cover: 当使用文本记录的时候，是否覆盖原内容
		:param fileinfo: 是否显示日志文件信息
		:param basename: 设置日志文件显示信息,True(只显示文件名), False(显示绝对路径)
		"""

		self.Red = "\033[31m"  # 红色
		self.Greet = "\033[32m"  # 绿色
		self.Yellow = '\033[33m'  # 黄色
		self.Blue = '\033[34m'  # 蓝色
		self.RESET_ALL = '\033[0m'  # 清空颜色
		self.basename = basename
		self.fileinfo = fileinfo
		self.cover = cover
		self.class_name = class_name
		# 是否启用txt
		self.txt_mode = txt
		# 日志文件显示名称
		self.file_name = None
		# 日志文件绝对路径
		self.file_path = file
		# 日期
		self.date = str(datetime.now()).split('.')[0]
		# 行数
		self.line_ = 1
		# 模块名称
		self.module_name = None
		# 文件名称
		self.filename = None
		# 日志内容
		self.msg1 = None
		# 是否启用文件名
		self.format_filename = True
		# 是否启用日期
		self.format_date = True
		# 是否启用时间
		self.format_time = True
		# 是否显示类名称
		self.format_class = True
		# 是否显示函数名称
		self.format_fun = True
		# 是否显示行数
		self.format_line = True
		# 是否显示 等级
		self.format_level = True
		# 设置等级关系
		self.level_dic = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
		# 设置文件记录最低等级
		self.level_text = 0
		# 设置控制台显示最低等级
		self.level_console = 0
		# 初始化实例参数
		self._init_fun()

	def _init_fun(self):
		"""
		初始化函数
		:return:
		"""
		#
		if self.file_path is None and self.txt_mode:
			if platform.system().lower() == 'linux'.lower():
				file = path.join(environ['HOME'], 'ColorInfo.log')
			else:
				file = path.join(environ["USERPROFILE"], 'ColorInfo.log')
			self.file = str(file)
			self.file_path = path.abspath(self.file)
		else:
			self.file_name = " "
		# 如果开启了文本记录模式,则实例化一个读写
		if self.txt_mode:
			try:
				# 日志写入实例
				self.txt_wr = open(file=self.file_path, mode='a+', encoding='utf-8')
				if self.txt_mode:
					self.txt_wr.close()
					self.txt_wr = open(file=self.file_path, mode='a+', encoding='utf-8')
					if self.cover:
						self.txt_wr.close()
						self.txt_wr = open(file=self.file_path, mode='w+', encoding='utf-8')
			except Exception as e:
				print(e)
				exit(1)
			if self.basename:
				self.file_name = path.basename(str(self.file_path))

	def set_format(self, date_on=True, time_on=True, filename_on=True, class_on=True, fun=True, line=True, level=True):
		"""
		设置格式开关,默认全开
		:param level: 是否显示等级(默认: True)-DEBUG
		:param line: 是否显示行号(默认: True)-line: 230
		:param fun: 是否显示函数(默认: True)
		:param class_on: 是否显示类(默认: True)
		:param date_on: 是否显示日期(默认: True)-2022-11-03
		:param time_on: 是否显示时间(默认: True)-20:42:24
		:param filename_on: 是否显示文件名(源码文件)(默认: True)-ColorInfo.py
		:return:
		"""
		self.format_date = date_on
		self.format_filename = filename_on
		self.format_time = time_on
		self.format_class = class_on
		self.format_fun = fun
		self.format_line = line
		self.format_level = level

	def set_level(self, console="DEBUG", text="DEBUG"):
		"""
		设置显示等级,当实际等级低于设置等级的时候将不会显示/写入
		:param console: 设置控制台显示最低等级(DEBUG/INFO/WARNING/ERROR)
		:param text: 设置文本记录最低等级(DEBUG/INFO/WARNING/ERROR)
		:return:
		"""
		level_list = ["DEBUG", "INFO", "WARNING", "ERROR"]
		if console.upper() not in level_list:
			console = "DEBUG"
		if text.upper() not in level_list:
			text = "DEBUG"
		self.level_console = self.level_dic[console.upper()]
		self.level_text = self.level_dic[text.upper()]

	def fun_info(self, info):
		"""
		获取function信息
		:param info:
		:return:
		"""
		self.line_ = info[1]
		self.module_name = info[2]
		filename = info[0]
		filename = str(filename).split('/')[-1]
		if platform.system().lower() == 'windows'.lower():
			filename = path.split(filename)[1]
		self.filename = filename

	def _create_msg(self, msg, level='DEBUG'):
		"""
		创建信息
		:param msg: 信息
		:param level: 信息级别
		:return:
		"""
		msg1 = ''
		date_ = self.date.split(' ')[0]
		time_ = self.date.split(' ')[1]
		if self.format_date:
			msg1 = date_ + str(msg1)
		if self.format_time:
			msg1 = str(msg1) + ' ' + str(time_)
		if self.format_filename:
			msg1 = msg1 + " " + self.filename
		if self.format_line:
			msg1 = str(msg1) + "  line: " + str(self.line_)
		if self.class_name is not None and self.format_class:
			msg1 = str(msg1) + " - Class: " + str(self.class_name)
		if self.module_name != '<module>' and self.format_fun:
			msg1 = str(msg1) + " Function: " + self.module_name
		if self.format_level:
			msg1 = str(msg1) + " - %s : " % str(level) + str(msg)
		self.msg1 = msg1

	def _wr(self):
		try:
			# 如果开启了文本日志
			if self.txt_mode:
				self.txt_wr.write(self.msg1)
				self.txt_wr.write("\n")
		except Exception as e:
			print(self.Red + str(e) + self.RESET_ALL)

	def _arg(self, arg):
		"""
		解析参数
		:param arg:
		:return:
		"""
		arg_ = ''
		for i in arg:
			arg_ = arg_ + str(i)
		return arg_

	def _get_time(self):
		self.date = str(datetime.now()).split('.')[0]

	def info(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:return:
		"""
		fun_info = inspect.getframeinfo(inspect.currentframe().f_back)
		self.fun_info(info=fun_info)
		self._get_time()
		if arg:
			msg = str(msg) + str(self._arg(arg=arg))
		if kwarg:
			msg = str(msg) + str(self._arg(arg=kwarg))
		self._create_msg(msg=msg, level="INFO")
		mess = str(self.Greet + self.msg1 + self.RESET_ALL)
		if self.fileinfo and self.txt_mode:
			mess = str(self.Greet + str(self.file_name) + ' <<-- ' + self.msg1 + self.RESET_ALL)
		if self.level_console <= 1:
			print(mess)
		if self.level_text <= 1:
			self._wr()

	def debug(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:return:
		"""
		fun_info = inspect.getframeinfo(inspect.currentframe().f_back)
		self.fun_info(info=fun_info)
		self._get_time()
		if arg:
			msg = str(msg) + str(self._arg(arg=arg))
		if kwarg:
			msg = str(msg) + str(self._arg(arg=kwarg))
		self._create_msg(msg=msg)
		mess = str(self.Blue + self.msg1 + self.RESET_ALL)
		if self.fileinfo and self.txt_mode:
			mess = str(self.Blue + str(self.file_name) + ' <<-- ' + self.msg1 + self.RESET_ALL)
		if self.level_console == 0:
			print(mess)
		if self.level_text <= 0:
			self._wr()

	def warning(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:return:
		"""
		fun_info = inspect.getframeinfo(inspect.currentframe().f_back)
		self.fun_info(info=fun_info)
		self._get_time()
		if arg:
			msg = str(msg) + str(self._arg(arg=arg))
		if kwarg:
			msg = str(msg) + str(self._arg(arg=kwarg))
		self._create_msg(msg=msg, level="WARNING")
		mess = str(self.Yellow + self.msg1 + self.RESET_ALL)
		if self.fileinfo and self.txt_mode:
			mess = str(self.Yellow + str(self.file_name) + ' <<-- ' + self.msg1 + self.RESET_ALL)
		if self.level_console <= 2:
			print(mess)
		if self.level_text <= 2:
			self._wr()

	def error(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:return:
		"""
		fun_info = inspect.getframeinfo(inspect.currentframe().f_back)
		self.fun_info(info=fun_info)
		self._get_time()
		if arg:
			msg = str(msg) + str(self._arg(arg=arg))
		if kwarg:
			msg = str(msg) + str(self._arg(arg=kwarg))
		self._create_msg(msg=msg, level="ERROR")
		mess = str(self.Red + self.msg1 + self.RESET_ALL)
		if self.fileinfo and self.txt_mode:
			mess = str(self.Red + str(self.file_name) + ' <<-- ' + self.msg1 + self.RESET_ALL)
		if self.level_console <= 3:
			print(mess)
		if self.level_text <= 3:
			self._wr()


if __name__ == "__main__":
	log = ColorLogger(fileinfo=True, basename=True, txt=True)
	log.info(msg='1', x="23")
	log.error('2', '22', '222')
	log.set_level(console="INFO")
	log.debug('3', '21')
	log.warning('4', '20', 22)
