from module.tools.logger import logger
import anitopy

def Anitomy(filename:str):
    try:
        result = anitopy.parse(filename)
        output = {
            'anime_title': result['anime_title'] if 'anime_title' in result else 'null',
            'anime_year': result['anime_year'] if 'anime_year' in result else 'null',
            'audio_term': result['audio_term'] if 'audio_term' in result else 'null',
            'episode_number': result['episode_number'] if 'episode_number' in result else 'null',
            'episode_title': result['episode_title'] if 'episode_title' in result else 'null',
            'file_checksum': result['file_checksum'] if 'file_checksum' in result else 'null',
            'file_extension': result['file_extension'] if 'file_extension' in result else 'null',
            'file_name': result['file_name'],
            'release_group': result['release_group'] if 'release_group' in result else 'null',
            'release_version': result['release_version'] if 'release_version' in result else 'null',
            'video_resolution': result['video_resolution'] if 'video_resolution' in result else 'null',
            'video_term': result['video_term'] if 'video_term' in result else 'null'
        }
        logger.debug("[Anitomy]解析结果\n"
                     f"源文件名：{output['file_name']}\n"
                     f"动画标题：{output['anime_title']}\n"
                     f"动画年份：{output['anime_year']}\n"
                     f"剧集编号：{output['episode_number']}\n"
                     f"剧集标题：{output['episode_title']}\n"
                     f"文件类型：{output['file_extension']}\n"
                     f"字幕组/发布组：{output['release_group']}\n"
                     f"发布版本：{output['release_version']}\n"
                     f"音频类型：{output['audio_term']}\n"
                     f"视频分辨率：{output['video_resolution']}\n"
                     f"视频编码格式：{output['video_term']}")
        return output
    except Exception as err:
        logger.error(f"[Anitomy]解析文件{filename}时发生错误\n{err}")
        return False

if __name__ == "__main__":
    Anitomy("[ANi] 文豪野犬 第四季（僅限港澳台地區） - 05 [1080P][Bilibili][WEB-DL][AAC AVC][CHT CHS].mp4")
    Anitomy("[Airota][Kono Subarashii Sekai ni Bakuen wo!][03][1080p AVC AAC][CHS].mp4")
    Anitomy("[GJ.Y] AI no Idenshi - 02 (CR 1920x1080 AVC AAC MKV) [63E3D4D2].mkv")
    Anitomy("[DMG&LoliHouse] Kono Subarashii Sekai ni Bakuen wo! - 05 [WebRip 1080p HEVC-10bit AAC ASSx2].mkv")
    Anitomy("[KTXP][Fatestrange Fake -Whispers of Dawn][BIG5][1080P][MP4].mp4")