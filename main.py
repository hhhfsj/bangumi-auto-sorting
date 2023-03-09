import re
import os
import shutil

config = {
    1: {
        "input_dir": "H:\Baha",
        "output_dir": "H:\Baha",
        "Season_add_zero": False  # 是否在季度编号为1时给季度加0（老问题了）
    },
    2: {
        "input_dir": "H:\Bilibili",
        "output_dir": "H:\Bilibili",
        "Season_add_zero": True
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
        "bangumi_name": bangumi_name_cut[0],
        "season": bangumi_season,
        "episode": bangumi_name_cut[-1],
        "tags": temp_list,
        "file_suffix": filename
    }
    return output


for index in config.keys():
    input_dir= config[index]["input_dir"]
    output_dir = config[index]["output_dir"]
    Season_add_zero = config[index]["Season_add_zero"]

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
                print(f"[Debug]{FileName_info}")
                if FileName_info["tags"][0] == "[ANi]":
                    if not os.path.exists(f"{output_dir}/{FileName_info['bangumi_name']}"):
                        os.mkdir(f"{output_dir}/{FileName_info['bangumi_name']}")
                    if not os.path.exists(
                            f"{output_dir}/{FileName_info['bangumi_name']}/S{FileName_info['season']}"):
                        os.mkdir(f"{output_dir}/{FileName_info['bangumi_name']}/S{FileName_info['season']}")

                    if os.path.exists(f"{output_dir}/{FileName_info['bangumi_name']}") and os.path.exists(
                            f"{output_dir}/{FileName_info['bangumi_name']}/S{FileName_info['season']}"):
                        OutputFile_path: str = f"{output_dir}/{FileName_info['bangumi_name']}/S{FileName_info['season']}"
                        try:
                            shutil.move(f"{input_dir}/{FileName_info['FileName']}", f"{OutputFile_path}")
                            os.rename(f"{OutputFile_path}/{FileName_info['FileName']}",
                                      f"{OutputFile_path}/S{FileName_info['season']}E{FileName_info['episode']} {FileName_info['FileName']}")
                        except:
                            print(f"[Error]移动{FileName_info['FileName']}时发生错误")
