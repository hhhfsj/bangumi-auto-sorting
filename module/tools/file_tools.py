import hashlib
import os
import shutil
from module.tools.logger import logger


def Compare_file_md5(file1: str, file2: str) -> bool:
    def get_file_md5(file: str) -> str:
        logger.debug(f"[Get MD5]正在尝试获取：{file}")
        md5_hash = hashlib.md5()
        with open(file, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()
    logger.debug(f"[Get MD5]\n"
                 f"File1:{get_file_md5(file1)}\n"
                 f"File2:{get_file_md5(file2)}")
    return get_file_md5(file1) == get_file_md5(file2)


def is_used(file_name):
    if os.path.exists(file_name):
        try:
            with open(file_name, 'rb+') as f:
                logger.debug(f"文件{file_name}未被占用")
                return False  # File is not locked
        except IOError as error:
            logger.error(f"文件{file_name}测试失败，可能已被占用\n{error}")
            return True  # File is locked
    else:
        logger.error(f"文件{file_name}不存在！")
        return True


def copy_file(source: str, directory: str):
    '''
	复制文件
	:param source: 源文件
	:param directory: 目标文件夹
	:return: 成功：True 失败：False
	'''
    logger.debug(f"[复制]复制文件：{source} --> {directory}")
    if not os.path.exists(source) or not os.path.exists(directory):
        if not os.path.exists(source):
            logger.error(f"[复制]源文件{source}不存在")
        elif not os.path.exists(directory):
            logger.error(f"[复制]目标文件{directory}已存在")
        return False
    try:
        shutil.copy(source, directory)
        logger.debug(f"[复制]复制文件：{source} --> {directory}成功")
        return True
    except Exception as e:
        logger.error(f"[复制]复制文件：{source} --> {directory}失败\n原因：{e}")
        return False


def move_file(source: str, directory: str):
    '''
	移动文件
	:param source: 源文件
	:param directory: 目标文件夹
	:return: 成功：True 失败：False
	'''
    if not is_used(source):
        logger.debug(f"[移动]移动文件：{source} --> {directory}")
        if not os.path.exists(source) or not os.path.exists(directory):
            if not os.path.exists(source):
                logger.error(f"[移动]源文件{source}不存在")
            elif not os.path.exists(directory):
                logger.error(f"[移动]目标文件{directory}已存在")
            return False
        try:
            shutil.move(source, directory)
            logger.debug(f"[移动]移动文件：{source} --> {directory}成功")
            return True
        except Exception as e:
            logger.error(f"[移动]移动文件：{source} --> {directory}失败\n原因：{e}")
            return False
    else:
        return False


def rename_file(file_path: str, new_file_name: str):
    '''
	重命名文件
	:param file_path: 要重命名的文件
	:param new_file_name: 新文件名
	:return: 成功：True 失败：False
	'''
    if not is_used(file_path):
        logger.debug(f"[重命名]：{file_path} --> {new_file_name}")
        if not os.path.exists(file_path) or os.path.exists(new_file_name):
            if not os.path.exists(file_path):
                logger.error(f"[重命名]文件{file_path}不存在")
            elif os.path.exists(new_file_name):
                logger.error(f"[重命名]目标文件名{new_file_name}已存在")
            return False
        try:
            os.rename(file_path, new_file_name)
            logger.debug(f"[重命名]：{file_path} --> {new_file_name}成功")
            return True
        except Exception as e:
            logger.error(f"[重命名]重命名文件：{file_path} --> {new_file_name}失败\n原因：{e}")
            return False
    else:
        return False


def del_file(file_path: str):
    '''
	删除文件
	:param file_path: 要删除的文件
	:return: 成功：True 失败：False
	'''

    if not is_used(file_path):
        logger.info(f"[删除]{file_path}")
        if not os.path.exists(file_path):
            logger.error(f"[删除]目标文件{file_path}不存在")
            return False
        else:
            try:
                os.remove(file_path)
                logger.debug(f"[删除]删除文件：{file_path}成功")
                return True
            except Exception as e:
                logger.error(f"[删除]文件：{file_path}删除失败\n原因：{e}")
                return False
    else:
        return False


def mkdir(directory_name: str):
    '''
	创建文件夹
	:param directory_name: 要创建的文件夹名
	:return: 成功：True 失败：False
	'''
    logger.info(f"[新建]新建文件夹{directory_name}")
    if not os.path.exists(directory_name):
        try:
            os.mkdir(directory_name)
            logger.debug(f"[新建]新建文件夹{directory_name}成功")
            return True
        except Exception as e:
            logger.error(f"[新建]新建文件夹{directory_name}失败\n原因：{e}")
            return False
    else:
        logger.error(f'[新建]文件夹{directory_name}已存在')
        return True
