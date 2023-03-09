# bangumi-auto-sorting
将ANi的流媒体镜像自动分类为jellyfin可识别的目录树

``` dir tree
动画
├── 狼与香辛料
│   ├── S00
│   │   └── S00E01 - 狼与香辛料的原视频文件名.mkv
│   ├── S01
│   │   ├── S01E01 - 狼与香辛料的原视频文件名.mkv
│   │   └── ……
│   └── S02
│       ├── S02E01 - 狼与香辛料的原视频文件名.mkv
│       └── ……
└── ……
```

请按需修改main.py内容后运行
``` python
config = {
    1: {  # 配置文件序号
        "input_dir": "H:\Baha",  # 输入目录
        "output_dir": "H:\Baha",  # 输出目录
        "Season_add_zero": False  # 是否在季度编号为1时给季度加0（老问题了）
    },
    2: {
        "input_dir": "H:\Bilibili",
        "output_dir": "H:\Bilibili",
        "Season_add_zero": True
    }
}
```
