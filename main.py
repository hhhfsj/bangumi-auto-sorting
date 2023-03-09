import re
import os
import shutil
import hashlib

config = {
    1: {
        "input_dir": "input",
        "output_dir": "output",
        "Season_add_zero": False,  # 是否在季度编号为1时给季度加0（老问题了）
        "Copy_mode": True  # 是否使用复制模式
    }
}

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


def file_decoding(filename: str) -> dict:
    video_filename: str = filename
    temp_list: list = []
    bangumi_name: str = re.search("] .* \[", filename).group()[2:-2]  # 取出番剧名
    bangumi_name_cut: list = bangumi_name.split(" ")
    if "季" in bangumi_name_cut[1]:
        bangumi_season: str = re.match("第.*季", bangumi_name_cut[1]).group()
    else:
        bangumi_season = "1"
    for key, value in Digital_mapping.items():
        if key in bangumi_season:
            bangumi_season = f"0{value}"
    for index, tag in enumerate(bangumi_name_cut):
        if tag == "-":
            del bangumi_name_cut[index]
    if filename.find("[") == -1 or filename.find("]") == -1:
        raise "无法解析的文件名"
    while filename.find("[") != -1 and filename.find("]") != -1:
        temp = filename[filename.find("["):filename.find("]") + 1]
        temp_list.append(temp)
        filename = filename[filename.find("]") + 1:]
    output = {
        "FileName": video_filename,
        "bangumi_name": bangumi_name[:bangumi_name.find(" - ")],
        "season": bangumi_season,
        "episode": bangumi_name_cut[-1],
        "tags": temp_list,
        "file_suffix": filename
    }
    return output


def Compare_file_sizes(file1: str, file2: str) -> bool:
    def get_file_md5(file: str) -> str:
        md5_hash = hashlib.md5()
        with open(file, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()

    return get_file_md5(file1) == get_file_md5(file2)


for index in config.keys():
    input_dir = config[index]["input_dir"]
    output_dir = config[index]["output_dir"]
    Season_add_zero = config[index]["Season_add_zero"]
    copy = config[index]["Copy_mode"]

    if not os.path.exists(input_dir):
        os.mkdir(input_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for filename in os.listdir(input_dir):
        if filename[-4:] == ".mp4":
            try:
                FileName_info = file_decoding(filename)
                if Season_add_zero and FileName_info['season'] == "1":
                    FileName_info['season'] = f"0{FileName_info['season']}"
            except:
                print(f"[Error]获取{filename}数据时发生错误")
            else:
                # print(f"[Debug]{FileName_info}")
                if FileName_info["tags"][0] == "[ANi]":
                    if not os.path.exists(f"{output_dir}/{FileName_info['bangumi_name']}"):
                        os.mkdir(f"{output_dir}/{FileName_info['bangumi_name']}")
                    if not os.path.exists(
                            f"{output_dir}/{FileName_info['bangumi_name']}/S{FileName_info['season']}"):
                        os.mkdir(f"{output_dir}/{FileName_info['bangumi_name']}/S{FileName_info['season']}")

                    if os.path.exists(f"{output_dir}/{FileName_info['bangumi_name']}") and os.path.exists(
                            f"{output_dir}/{FileName_info['bangumi_name']}/S{FileName_info['season']}"):
                        OutputFile_path: str = f"{output_dir}/{FileName_info['bangumi_name']}/S{FileName_info['season']}"
                        # 判断输出文件夹内是否有未改名的文件，如果有需要删除
                        if os.path.exists(f"{OutputFile_path}/{FileName_info['FileName']}"):
                            try:
                                os.remove(f"{OutputFile_path}/{FileName_info['FileName']}")
                                print(f"[Info]删除：{OutputFile_path}/{FileName_info['FileName']}")
                            except:
                                print(f"[Error]文件{OutputFile_path}/{FileName_info['FileName']}删除失败")
                        # 在复制模式下启用；判断目标文件夹内是否已经有完整的文件，如果有了需尝试删除输入文件夹内的文件
                        if copy and os.path.exists(
                                f"{OutputFile_path}/S{FileName_info['season']}E{FileName_info['episode']} {FileName_info['FileName']}"):
                            if Compare_file_sizes(f"{input_dir}/{FileName_info['FileName']}",
                                                  f"{OutputFile_path}/S{FileName_info['season']}E{FileName_info['episode']} {FileName_info['FileName']}"):
                                try:
                                    os.remove(f"{input_dir}/{FileName_info['FileName']}")
                                    print(f"删除：{input_dir}/{FileName_info['FileName']}")
                                except:
                                    print(f"[Error]文件{input_dir}/{FileName_info['FileName']}删除失败")
                            else:
                                print("文件大小不相同？")

                        if not os.path.exists(
                                f"{OutputFile_path}/S{FileName_info['season']}E{FileName_info['episode']} {FileName_info['FileName']}"):
                            if copy:  # 复制模式
                                try:
                                    shutil.copy(f"{input_dir}/{FileName_info['FileName']}", f"{OutputFile_path}")
                                    print(
                                        f"[Info]复制：{input_dir}/{FileName_info['FileName']} -> {OutputFile_path}/{FileName_info['FileName']}")
                                except:
                                    print(
                                        f"[Error]复制{input_dir}/{FileName_info['FileName']} -> {OutputFile_path}/{FileName_info['FileName']}失败")
                                    continue
                            else:
                                try:
                                    shutil.move(f"{input_dir}/{FileName_info['FileName']}", f"{OutputFile_path}")
                                    print(
                                        f"[Info]移动：{input_dir}/{FileName_info['FileName']} -> {OutputFile_path}/{FileName_info['FileName']}")
                                except:
                                    print(
                                        f"[Error]移动{input_dir}/{FileName_info['FileName']} -> {OutputFile_path}/{FileName_info['FileName']}失败")
                                    continue
                            try:
                                os.rename(f"{OutputFile_path}/{FileName_info['FileName']}",
                                          f"{OutputFile_path}/S{FileName_info['season']}E{FileName_info['episode']} {FileName_info['FileName']}")
                                print(
                                    f"[Info]文件重命名：{FileName_info['FileName']} -> S{FileName_info['season']}E{FileName_info['episode']} {FileName_info['FileName']}")
                            except:
                                print(
                                    f"[Error]文件重命名{FileName_info['FileName']} -> S{FileName_info['season']}E{FileName_info['episode']} {FileName_info['FileName']}失败")
