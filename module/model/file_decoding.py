import re
from pathlib import Path
from module.tools.logger import logger

def file_decoding(filename: str):
    video_filename = Path(filename)
    bangumi_name: str = re.search("] .* \[", filename).group()[2:-2]  # 取出番剧名
    bangumi_name_cut: list = bangumi_name.split(" ")
    for index, tag in enumerate(bangumi_name_cut):
        if tag == "-":
            del bangumi_name_cut[index]

    def analyze_season(bangumi_name: str) -> str:
        # logger.debug(bangumi_name)
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
        # logger.debug(bangumi_name)

        if "季" in bangumi_name:
            if re.search("第\D季", bangumi_name):
                bangumi_season: str = re.match("第\D季", bangumi_name).group()
                for key, value in Digital_mapping.items():
                    if key in bangumi_season:
                        bangumi_season = f"0{value}"
            elif re.search("第\d季", bangumi_name):
                bangumi_season: str = re.match("第\d季", bangumi_name).group()[1:-1]
        elif 'season' in bangumi_name:
            bangumi_season: str = re.findall(r'\d+', bangumi_name)[0]
        elif re.search('[!|！]{2,}', bangumi_name):
            temp = re.match('[!|！]{2,}', bangumi_name).group()
            bangumi_season = str(len(temp))
            del temp
        elif re.search('\dnd', bangumi_name):
            cut = re.match('\dnd', bangumi_name).group()
            bangumi_season = re.match('\d', cut).group()
            del cut
        elif re.search(' \d*$', bangumi_name):
            bangumi_season = re.match(' \d*$', bangumi_name).group()[1:]

        # logger.debug(bangumi_season)
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
        words_list = [r'season\d ' ,r'season \d', r'第[\d|\D]季', r'[!|！]{2,}', '\dnd Attack', '\dnd']
        for key in words_list:
            bangumi_name = re.sub(key, "", bangumi_name)
        temp = True
        while temp:
            if bangumi_name[-1:] == ' ':
                bangumi_name = bangumi_name[:-1]
            else:
                temp = False
        return bangumi_name

    def analyze_AIi(path):
        logger.debug(f'[ANi-文件名解析]正在解析{filename}')
        logger.debug(f'[ANi-文件名解析]文件名解析结果\n'
                     f'视频文件名：{path.name}\n'
                     f'番剧名：{del_season_words(bangumi_name[:bangumi_name.find(" - ")])}\n'
                     f'季号：{analyze_season(bangumi_name_cut[1])}\n'
                     f'集号：{bangumi_name_cut[-1]}\n'
                     f'tag：{cut_tags(path.name)}\n'
                     f'文件后缀：{path.suffix}')
        return {
            "FileName": path.name,
            "bangumi_name": del_season_words(bangumi_name[:bangumi_name.find(" - ")]),
            "season": analyze_season(bangumi_name_cut[1]),
            "episode": bangumi_name_cut[-1],
            "tags": cut_tags(path.name),
            "file_suffix": path.suffix
        }

    def analyze_Airota(path):
        logger.debug(f'[Airota-文件名解析]正在解析{filename}')
        logger.debug(f'[Airota-文件名解析]文件名解析结果\n'
                     f'视频文件名：{path.name}\n'
                     f'番剧名：{cut_tags(path.name)[1]}\n'
                     f'季号：null\n'
                     f'集号：{cut_tags(path.name)[2]}\n'
                     f'tag：{cut_tags(path.name)}\n'
                     f'文件后缀：{path.suffix}')
        return {
            "FileName": path.name,
            "bangumi_name": cut_tags(path.name)[1],
            "season": 1,
            "episode": cut_tags(path.name)[2],
            "tags": cut_tags(path.name),
            "file_suffix": path.suffix
        }

    def analyze_MCE(path):
        logger.debug(f'[MCE-文件名解析]正在解析{filename}')
        logger.debug(f'[MCE-文件名解析]文件名解析结果\n'
                     f'视频文件名：{path.name}\n'
                     f'番剧名：{cut_tags(path.name)[1]}\n'
                     f'季号：null\n'
                     f'集号：{cut_tags(path.name)[2]}\n'
                     f'tag：{cut_tags(path.name)}\n'
                     f'文件后缀：{path.suffix}')
        return {
            "FileName": path.name,
            "bangumi_name": cut_tags(path.name)[1],
            "season": 1,
            "episode": cut_tags(path.name)[2],
            "tags": cut_tags(path.name),
            "file_suffix": path.suffix
        }

    if "[ANi]" in video_filename.name:
        return analyze_AIi(video_filename)
    elif "[Airota]" in video_filename.name:
        return analyze_Airota(video_filename)
    elif "[MCE]" in video_filename.name:
        analyze_MCE(video_filename)
    else:
        return False
