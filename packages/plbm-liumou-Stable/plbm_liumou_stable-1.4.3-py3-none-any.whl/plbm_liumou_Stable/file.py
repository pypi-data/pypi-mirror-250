# -*- encoding: utf-8 -*-
"""
@File    :   file.py
@Time    :   2023-11-10 10:17
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
import mimetypes

import magic


def get_file_type(file_path):
	# 获取文件的MIME类型
	mime = magic.Magic(mime=True)
	file_type = mime.from_file(file_path)
	mime_type = mimetypes.guess_extension(file_type)
	# 返回文件类型
	return mime_type


if __name__ == '__main__':
	get_file_type(file_path="./py")
	get_file_type(file_path="xls")
