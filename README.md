# bangumi-auto-sorting
将ANi的流媒体镜像自动分类为jellyfin可识别的目录树  
ANi文件名格式：[ANi] 番剧名（僅限港澳台地區） - 01 [1080P][平台][WEB-DL][AAC AVC][CHT CHS].mp4

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

请按需修改config.json内容后运行
``` json
{
	"sleep_time": 30, //等待时间（秒）
	"debug": true, //调试模式
	"Configs": [ //配置列表
		{
			"Model": "File_name", // 获取方式（可选：File_name|Anitomy）
			"input_dir": "input", // 输入文件夹
			"output_dir": "output", // 输出文件夹
			"Season_add_zero": false, // 是否给1加0
			"Copy_model": true, // 是否启用复制模式
			"Del_original_file": false // 是否删除源文件（仅复制模式）
		},
		{
			"Model": "Anitomy",
			"input_dir": "input",
			"output_dir": "output",
			"Season_add_zero": false,
			"Copy_model": true,
			"Del_original_file": false
		}
	]
}
```
