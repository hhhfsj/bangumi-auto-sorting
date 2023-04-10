import re
import os
import shutil
import hashlib
from time import sleep
from json import load, dump
from pathlib import Path
from sys import stderr

from loguru import logger
from datetime import datetime

default_config = {
    "sleep_time": 30,
    "debug": True,
    "Input-Output_Config": {
        "1": {
            "input_dir": "input",
            "output_dir": "output",
            "Season_add_zero": False,
            "Copy_mode": True,
            "Del_original_file": False
        },
        "2": {
            "input_dir": "input",
            "output_dir": "output",
            "Season_add_zero": False,
            "Copy_mode": True,
            "Del_original_file": False
        }
    }
}

if not os.path.exists('./config.json'):
    dump(default_config, open("./config.json", 'w'), indent='\t', ensure_ascii=False)
    print("配置文件已生成，请配置完后重新启动")
    os.system('pause')
    exit()

with open('./config.json', 'r+') as config_json_file:
    config_all = load(config_json_file)

config = config_all['Input-Output_Config']
debug = config_all['debug']

# 检查是否存在logs文件夹
logs = os.path.join('logs')
if not os.path.exists(logs):
    os.mkdir(logs)

if not debug:
    logger.remove()
    logger.add(stderr, level="INFO")
logger.add(f"./logs/output_{datetime.strftime(datetime.now(), '%Y-%m-%d')}.log",
           format="[{time:MM-DD HH:mm:ss}] - {level}: {message}", rotation="00:00")


def file_decoding(filename: str) -> dict:
    video_filename = Path(filename)
    bangumi_name: str = re.search("] .* \[", filename).group()[2:-2]  # 取出番剧名
    bangumi_name_cut: list = bangumi_name.split(" ")
    for index, tag in enumerate(bangumi_name_cut):
        if tag == "-":
            del bangumi_name_cut[index]

    def analyze_season(bangumi_name: str) -> str:
        Digital_mapping: dict = {
            "零": 0,
            "一": 1,
            "二": 2,
            "三": 3,
            "四": 4,
            "五": 5,
            "六": 6,
            "七": 7,
            "八": 8,
            "九": 9,
            "十": 10
        }
        bangumi_season = "1"
        bangumi_name = bangumi_name.lower()

        if "季" in bangumi_name:
            if re.search("第\D季", bangumi_name):
                bangumi_season: str = re.match("第\D季", bangumi_name).group()
                for key, value in Digital_mapping.items():
                    if key in bangumi_season:
                        bangumi_season = f"0{value}"
            elif re.search("第\d季", bangumi_name):
                bangumi_season: str = re.match("第\d季", bangumi_name).group()[1:-1]
        elif 'season' in bangumi_name:
            bangumi_season: str = re.match("season \d", bangumi_name).group()
        elif re.search('[!|！]{2,}', bangumi_name):
            temp = re.match('[!|！]{2,}', bangumi_name).group()
            bangumi_season = str(len(temp))
        return bangumi_season

    def cut_tags(filename) -> list:
        if not isinstance(filename, str):
            filename = filename.name
        file_tag_list: list = []
        if filename.find("[") == -1 or filename.find("]") == -1:
            raise "无法解析的文件名"
        while filename.find("[") != -1 and filename.find("]") != -1:
            temp = filename[filename.find("["):filename.find("]") + 1]
            file_tag_list.append(temp)
            filename = filename[filename.find("]") + 1:]
        return file_tag_list

    def del_season_words(bangumi_name: str):
        bangumi_name = bangumi_name.lower()
        words_list = [r'season \d', r'第[\d|\D]季', r'[!|！]{2,}']
        for key in words_list:
            bangumi_name = re.sub(key, "", bangumi_name)
        return bangumi_name

    def analyze_AIi(path):
        logger.debug(f'[ANi-文件名解析]正在解析{filename}')
        logger.debug(f'[ANi-文件名解析]文件名解析结果\n'
                     f'视频文件名：{video_filename.name}\n'
                     f'番剧名：{del_season_words(bangumi_name[:bangumi_name.find(" - ")])}\n'
                     f'季号：{analyze_season(bangumi_name_cut[1])}\n'
                     f'集号：{bangumi_name_cut[-1]}\n'
                     f'tag：{cut_tags(video_filename)}\n'
                     f'文件后缀：{video_filename.suffix}')
        return {
            "FileName": video_filename.name,
            "bangumi_name": del_season_words(bangumi_name[:bangumi_name.find(" - ")]),
            "season": analyze_season(bangumi_name_cut[1]),
            "episode": bangumi_name_cut[-1],
            "tags": cut_tags(video_filename),
            "file_suffix": video_filename.suffix
        }

    if "[ANi]" in video_filename.name:
        return analyze_AIi(video_filename)


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


def file_is_openState(file_path):
    if os.path.exists(file_path):
        logger.error(f"[文件测试]要测试的文件{file_path}不存在！")
        return False
    try:
        logger.debug(f"[文件测试]正在测试：{file_path}是否可写")
        open(file_path, "w").close()
        return False
    except Exception as e:
        logger.debug(f"[文件测试]文件：{file_path}不可写\n原因：{e}")
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


def rename_file(file_path: str, new_file_name: str):
    '''
    重命名文件
    :param file_path: 要重命名的文件
    :param new_file_name: 新文件名
    :return: 成功：True 失败：False
    '''
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


def del_file(file_path: str):
    '''
    删除文件
    :param file_path: 要删除的文件
    :return: 成功：True 失败：False
    '''
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


def run():
    # 循环配置文件
    for index in config.keys():
        # 将配置文件保存到变量中
        input_dir = config[index]["input_dir"]
        output_dir = config[index]["output_dir"]
        Season_add_zero = config[index]["Season_add_zero"]
        copy = config[index]["Copy_mode"]
        del_input_file = config[index]["Del_original_file"]

        # 检测输入输出文件夹是否存在
        if not os.path.exists(input_dir):
            logger.error(f"[{index}]输入文件夹{input_dir}不存在，已跳过")
            continue
        if not os.path.exists(output_dir):
            logger.info(f"[{index}]输出文件夹{output_dir}不存在，已自动创建")
            mkdir(output_dir)

        # 检测是否有文件
        if len(os.listdir(input_dir)) <= 0:
            logger.debug(f'配置文件{index}输入目录无文件，已跳过')
            continue

        logger.debug(f"正在执行配置文件{index}\n"
                     f"输入文件夹：{input_dir}\n"
                     f"输出文件夹：{output_dir}\n"
                     f"是否在季度编号为1时给季度加0：{Season_add_zero}\n"
                     f"是否使用复制模式：{copy}\n"
                     f"（在复制模式下启用）是否删除已复制完成的原文件：{del_input_file}")

        for filename in Path(input_dir).iterdir():
            filename = str(filename.name)
            FileName_info = file_decoding(filename)
            # 判断是否加0
            if Season_add_zero and FileName_info['season'] == "1":
                FileName_info['season'] = f"0{FileName_info['season']}"
            # 检测并创建对应番剧的文件夹
            if not os.path.exists(f"{output_dir}/{FileName_info['bangumi_name']}"):
                mkdir(f"{output_dir}/{FileName_info['bangumi_name']}")
            if not os.path.exists(f"{output_dir}/{FileName_info['bangumi_name']}/S{FileName_info['season']}"):
                mkdir(f"{output_dir}/{FileName_info['bangumi_name']}/S{FileName_info['season']}")
            if os.path.exists(f"{output_dir}/{FileName_info['bangumi_name']}") and os.path.exists(
                    f"{output_dir}/{FileName_info['bangumi_name']}/S{FileName_info['season']}"):
                InputFile_Path = f"{input_dir}/{FileName_info['FileName']}"  # 输入文件
                OutputFile_path = f"{output_dir}/{FileName_info['bangumi_name']}/S{FileName_info['season']}"  # 包含季度的文件路径
                Out_dir_Original_File_Name = f"{OutputFile_path}/{FileName_info['FileName']}"  # 包含季度的原文件名
                Final_Out_file_name = f"{OutputFile_path}/S{FileName_info['season']}E{FileName_info['episode']} {FileName_info['FileName']}"  # 最终的文件名
                logger.debug(f"\n输入文件名：{InputFile_Path}\n"
                             f"包含季度的输出路径：{OutputFile_path}\n"
                             f"包含季度的源文件名：{Out_dir_Original_File_Name}\n"
                             f"最终文件名：{Final_Out_file_name}")
                # 判断输出文件夹内是否有未改名的文件，如果有需要删除
                if os.path.exists(Out_dir_Original_File_Name):
                    del_file(Out_dir_Original_File_Name)
                # 在复制模式下启用；判断目标文件夹内是否已经有完整的文件，如果有了需尝试删除输入文件夹内的文件
                if copy and os.path.exists(Final_Out_file_name) and del_input_file:
                    if Compare_file_md5(InputFile_Path, Final_Out_file_name):
                        if not file_is_openState(InputFile_Path):
                            del_file(InputFile_Path)
                    else:
                        logger.info("文件MD5校验失败，尝试重新复制")
                        if del_file(Final_Out_file_name):
                            copy_file(InputFile_Path, OutputFile_path)
                            rename_file(Out_dir_Original_File_Name, Final_Out_file_name)
                if not os.path.exists(Final_Out_file_name):
                    if copy:  # 复制模式
                        if not copy_file(InputFile_Path, OutputFile_path):
                            continue
                    else:
                        if not move_file(InputFile_Path, OutputFile_path):
                            continue
                    rename_file(Out_dir_Original_File_Name, Final_Out_file_name)


if __name__ == "__main__":
    while True:
        run()
        sleep(config_all['sleep_time'])
