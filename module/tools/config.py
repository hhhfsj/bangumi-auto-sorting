import os
from json import load, dump


default_config = {
    "sleep_time": 30,
    "debug": True,
    "Configs": [
        {
            "Model": "File_name",
            "input_dir": "input",
            "output_dir": "output",
            "Season_add_zero": False,
            "Copy_model": True,
            "Del_original_file": False
        },
        {
            "Model": "Anitomy",
            "input_dir": "input",
            "output_dir": "output",
            "Season_add_zero": False,
            "Copy_model": True,
            "Del_original_file": False
        }
    ]
}

if not os.path.exists('./config.json'):
    dump(default_config, open("./config.json", 'w',encoding="utf-8"), indent='\t', ensure_ascii=False)
    print("配置文件已生成，请配置完后重新启动")
    os.system('pause')
    exit()

with open('./config.json', 'r+',encoding="utf-8") as config_json_file:
    config_all = load(config_json_file)
    # print(config_all)

config = config_all['Configs']
debug = config_all['debug']