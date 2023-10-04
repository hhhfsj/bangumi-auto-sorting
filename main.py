from time import sleep
from pathlib import Path

from module.model.anitomy import Anitomy
from module.model.file_decoding import file_decoding
from module.tools.config import config, config_all
from module.tools.file_tools import *
from module.tools.logger import logger


def run():
    # 循环配置文件
    for config_item in config:
        # 将配置文件保存到变量中
        model = config_item["Model"]
        input_dir = config_item["input_dir"]
        output_dir = config_item["output_dir"]
        Season_add_zero = config_item["Season_add_zero"]
        copy = config_item["Copy_model"]
        del_input_file = config_item["Del_original_file"]

        # 检测输入输出文件夹是否存在
        if not os.path.exists(input_dir):
            logger.error(f"输入文件夹{input_dir}不存在，已跳过")
            continue
        if not os.path.exists(output_dir):
            logger.info(f"输出文件夹{output_dir}不存在，已自动创建")
            mkdir(output_dir)

        # 检测是否有文件
        if len(os.listdir(input_dir)) <= 0:
            logger.debug(f'{input_dir}输入目录无文件，已跳过')
            continue

        logger.debug(f"正在执行配置文件\n"
                     f"模式：{model}\n"
                     f"输入文件夹：{input_dir}\n"
                     f"输出文件夹：{output_dir}\n"
                     f"是否在季度编号为1时给季度加0：{Season_add_zero}\n"
                     f"是否使用复制模式：{copy}\n"
                     f"（在复制模式下启用）是否删除已复制完成的原文件：{del_input_file}")

        for filename in Path(input_dir).iterdir():

            if filename.suffix in [".!qB", ".jpg", ".png", ".webp"] or filename.is_dir():
                logger.debug(filename.name, "已跳过")
                continue

            filename = str(filename.name)

            if is_used(os.path.join(input_dir, filename)):
                continue

            # 判断数据源
            if model == 'File_name':
                try:
                    result = file_decoding(filename)
                except Exception as err:
                    logger.error(f"[Mode:File_name]文件：{filename}解析错误\n{err}")
                    continue
                else:
                    if not result:
                        logger.debug(filename, "已跳过")
                        continue
                    season = result['season']
                    episode = result['episode']
                    bangumi_name = result['bangumi_name']
                    fileName = result['FileName']
            elif model == 'Anitomy':
                try:
                    result = Anitomy(filename)
                except Exception as err:
                    logger.error(f"[Mode:Anitomy]文件：{filename}解析错误\n{err}")
                    continue
                else:
                    if not result:
                        logger.debug(filename, "已跳过")
                        continue
                    season = "1"
                    episode = result['episode_number']
                    bangumi_name = result['anime_title']
                    fileName = result['file_name']
            else:
                break

            # 判断是否加0
            if Season_add_zero and season == "1":
                season = f"0{season}"

            # 检测并创建对应番剧的文件夹
            output_bangumi_dir = os.path.join(output_dir, bangumi_name)
            if not os.path.exists(output_bangumi_dir):
                mkdir(output_bangumi_dir)
            outputfile_path = os.path.join(output_dir, bangumi_name, "S" + season)  # 包含季度的文件路径
            if not os.path.exists(outputfile_path):
                mkdir(outputfile_path)
            if os.path.exists(output_bangumi_dir) and os.path.exists(outputfile_path):
                InputFile_Path = os.path.join(input_dir, fileName)  # 输入文件
                Out_dir_Original_File_Name = os.path.join(outputfile_path, fileName)  # 包含季度的原文件名
                if episode == 'null':
                    Final_Out_file_name = os.path.join(outputfile_path, f"S{season} {fileName}")  # 最终的文件名
                else:
                    Final_Out_file_name = os.path.join(outputfile_path, f"S{season}E{episode} {fileName}")  # 最终的文件名

                logger.debug(f"\n输入文件名：{InputFile_Path}\n"
                             f"包含季度的输出路径：{outputfile_path}\n"
                             f"包含季度的源文件名：{Out_dir_Original_File_Name}\n"
                             f"最终文件名：{Final_Out_file_name}")
                # 判断输出文件夹内是否有未改名的文件，如果有需要删除
                if os.path.exists(Out_dir_Original_File_Name):
                    del_file(Out_dir_Original_File_Name)
                # 在复制模式下启用；判断目标文件夹内是否已经有完整的文件，如果有了需尝试删除输入文件夹内的文件
                if copy and os.path.exists(Final_Out_file_name) and del_input_file:
                    if not is_used(InputFile_Path) and not is_used(Final_Out_file_name):  # 检测文件是否被占用
                        if Compare_file_md5(InputFile_Path, Final_Out_file_name):  # 校验MD5
                            if not is_used(InputFile_Path):  # 检查输入文件是否被占用
                                del_file(InputFile_Path)
                                logger.warning(InputFile_Path+"已删除")
                        else:
                            logger.warning("文件MD5校验失败，尝试重新复制")
                            if del_file(Final_Out_file_name):
                                copy_file(InputFile_Path, outputfile_path)
                                rename_file(Out_dir_Original_File_Name, Final_Out_file_name)
                                logger.success(InputFile_Path + "-->" + Final_Out_file_name)
                if not os.path.exists(Final_Out_file_name):
                    if copy:  # 复制模式
                        if not is_used(InputFile_Path):
                            if not copy_file(InputFile_Path, outputfile_path):
                                continue
                        else:
                            continue
                    else:
                        if not is_used(InputFile_Path):
                            if not move_file(InputFile_Path, outputfile_path):
                                continue
                        else:
                            continue
                    rename_file(Out_dir_Original_File_Name, Final_Out_file_name)
                    logger.success(InputFile_Path+"-->"+Final_Out_file_name)
                elif os.path.exists(Final_Out_file_name) and not copy:
                    del_file(Final_Out_file_name)


if __name__ == "__main__":
    while True:
        run()
        sleep(config_all['sleep_time'])
